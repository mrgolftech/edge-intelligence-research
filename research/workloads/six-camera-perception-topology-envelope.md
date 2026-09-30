# 六摄像头 UAV：PER_VIEW vs FUSED_MULTI_VIEW Perception Envelope

- 状态：v0.1
- 日期：2026-09-30
- 目的：在 Project Nominal 尚未冻结时，用统一 Camera 几何和 20/30Hz reference points 比较两种 W3 topology 的资源结构
- 数据：`data/calculations/six-camera-perception-topology-envelope.csv`
- 脚本：`scripts/calc_six_camera_perception_topology_envelope.py`
- 路由定义：`cases/six-camera-uav/phase-2-camera-workload-routing.md`

## 1. 统一分析条件

只用于 BENCHMARK_BASELINE：

```text
Capture:
6 × 1072 × 1280
NV12
20 / 30 Hz

VIO reference branch:
2 views
same 20 / 30 Hz for arithmetic

Depth reference branch:
2 views
same 20 / 30 Hz for arithmetic

PER_VIEW W3:
2 / 4 / 6 views

FUSED W3:
6 views/call

Benchmark input analysis representation:
640 × 640 × 3 bytes
```

这里把 VIO/depth 也设成同频，仅为了构造 fan-out sensitivity，不是项目需求。

---

## 2. PER_VIEW 调用率

| Profile | Views | Hz | Model Calls/s | 单串行服务通道平均 service interval |
|---|---:|---:|---:|---:|
| P20-2 | 2 | 20 | 40 | 25.0 ms |
| P20-4 | 4 | 20 | 80 | 12.5 ms |
| P20-6 | 6 | 20 | 120 | 8.33 ms |
| P30-2 | 2 | 30 | 60 | 16.67 ms |
| P30-4 | 4 | 30 | 120 | 8.33 ms |
| P30-6 | 6 | 30 | 180 | 5.56 ms |

这里的 service interval 只表示：

```text
1000 / ModelCallsPerSecond
```

只有在“单一串行 service channel”假设下，平均 service time 大于该值才一定无法无界排队。

它**不是 latency requirement**，也不适用于：
- 多 NPU core；
- 多 engine；
- batching；
- pipeline overlap。

---

## 3. FUSED_MULTI_VIEW 调用率

| Profile | Views/call | Hz | Model Calls/s | Input Views/s | 单串行服务通道平均 service interval |
|---|---:|---:|---:|---:|---:|
| F20-6 | 6 | 20 | 20 | 120 | 50.0 ms |
| F30-6 | 6 | 30 | 30 | 180 | 33.33 ms |

对比 P20-6 / P30-6：

```text
P20-6:
120 single-view calls/s
120 input views/s

F20-6:
20 fused calls/s
120 input views/s
```

因此：

> fused topology 改变 model-call granularity，但没有让六路源图像消失。

---

## 4. 640×640 RGB8 分析输入的 payload

每个 640×640×3-byte view：

```text
1.2288 MB
```

因此：

| Profile | Input Views/s | 640×640 RGB8 payload |
|---|---:|---:|
| P20-2 | 40 | 49.152 MB/s |
| P20-4 | 80 | 98.304 MB/s |
| P20-6 | 120 | 147.456 MB/s |
| P30-2 | 60 | 73.728 MB/s |
| P30-4 | 120 | 147.456 MB/s |
| P30-6 | 180 | 221.184 MB/s |
| F20-6 | 120 | 147.456 MB/s |
| F30-6 | 180 | 221.184 MB/s |

这只是一个 **preprocessed input representation** 的算术。

不能直接解释为：
- PCIe effective bandwidth；
- accelerator tensor traffic；
- GPU tensor bandwidth；
- DDR 实测。

实际 runtime 可能使用 NV12、RGB、UINT8、FP16、zero-copy、packed tensor 或内部 layout。

---

## 5. Camera Fan-out 一遍式分析

Source NV12 frame：

```text
1072 × 1280 × 1.5
= 2.05824 MB
```

假设：
- capture 写一次；
- W2 每个 view 读一次完整 source；
- W3 每个 input view 读一次完整 source；
- depth branch 每个 view 读一次完整 source；
- 暂不加入 W4 map tensor、model activation、codec、OS；
- 暂不考虑缩放后直接输出、缓存或共享结果。

则：

| Profile | Capture write | Consumer view reads/s | Full-source read equivalent | Capture + read equivalent |
|---|---:|---:|---:|---:|
| P20-2 | 246.99 MB/s | 120 | 246.99 MB/s | 493.98 MB/s |
| P20-4 | 246.99 MB/s | 160 | 329.32 MB/s | 576.31 MB/s |
| P20-6 | 246.99 MB/s | 200 | 411.65 MB/s | 658.64 MB/s |
| P30-2 | 370.48 MB/s | 180 | 370.48 MB/s | 740.97 MB/s |
| P30-4 | 370.48 MB/s | 240 | 493.98 MB/s | 864.46 MB/s |
| P30-6 | 370.48 MB/s | 300 | 617.47 MB/s | 987.96 MB/s |
| F20-6 | 246.99 MB/s | 200 | 411.65 MB/s | 658.64 MB/s |
| F30-6 | 370.48 MB/s | 300 | 617.47 MB/s | 987.96 MB/s |

### 关键解释

P6 与 F6 在同一 FPS 下这里得到相同的一遍式 source-view fan-out。

原因：
- 都消费六路 Camera view；
- VIO/depth branch 相同；
- FUSED 只是把 6 个 view 放进一次联合调用。

所以：

> **FUSED 不是减少 W1/源图像数据率的方案。**

它改变的是：
- model call granularity；
- model internal feature/tensor；
- cross-view attention；
- temporal cache；
- engine/operator 需求。

---

## 6. 为什么不能用 PER_VIEW YOLO latency 估算 FUSED

假设某平台的 YOLO 单视图 service time 是 `T_yolo`。

PER_VIEW 可以做第一轮：

```text
Demand =
CallsPerSecond × T_yolo
```

但 FUSED 必须使用：

```text
Demand =
FusedCallsPerSecond × T_fused_model
```

不能写：

```text
T_fused_model = T_yolo
```

也不能假设：

```text
T_fused_model = 6 × T_yolo
```

因为 fused Transformer/BEV 的：
- feature extractor；
- cross-view attention；
- temporal state；
- BEV queries；
- operator composition

与单视图 detector 不同。

因此 FUSED 当前只能建立 **input/data envelope**，compute envelope 必须绑定具体模型 Benchmark。

---

## 7. 对 Integrated 与 Host+Accelerator 的影响

### Integrated SoC/SoM

PER_VIEW：
- 多独立 inference queue；
- NPU/GPU scheduler；
- shared DDR fan-out；
- per-stream pre/post。

FUSED：
- 更少但更重的 model calls；
- GPU/NPU operator coverage 更关键；
- temporal/BEV memory 可能更大；
- W3/W4 资源边界更模糊。

### Host + Accelerator

PER_VIEW：
- 多 H2D transactions；
- accelerator queue/scaling；
- Host preprocess 可能成为瓶颈。

FUSED：
- 可能变成更少、更大的 multi-view transfer；
- 但 accelerator 必须支持完整 fused model；
- 如果 cross-view/temporal 部分退回 Host/GPU，可能形成新的 split pipeline 和额外拷贝。

因此 Host+Accelerator 不能只问：
> “卡能跑多少 YOLO FPS？”

还必须问：
> “目标 topology 的完整 graph 到底放在哪里？”

---

## 8. 当前可以得出的工程结论

1. 六摄 W3 的资源需求对 topology 高度敏感。
2. P20-6 与 F20-6 都是 120 input views/s，但分别是 120 与 20 model calls/s。
3. “model calls 更少”不等于 fused compute 更轻。
4. 如果全部六路参与 perception，FUSED 不降低源 Camera 数据率。
5. PER_VIEW 更容易直接绑定现有 RK3588/IQ-9075/M50/Metis/Hailo YOLO evidence。
6. FUSED/BEV 路线需要单独建立具体模型的 operator、memory、latency evidence，不能复用 YOLO Benchmark。
7. 下一步平台资源比较应至少分成 **P20/P30 与 F20/F30** 两族，而不是只保留一个“六路 detection”条目。
