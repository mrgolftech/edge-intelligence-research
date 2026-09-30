# 六摄像头无人平台：Phase 2 Requirement Card

- 状态：v0.1
- 日期：2026-09-30
- 性质：需求基线 + 待冻结项
- 原则：已确认事实与工程场景变量分开

## 1. 已确认输入

| 项目 | 当前值 | 状态 |
|---|---|---|
| N_capture | 6 | 已确认 |
| downstream width | 1072 | 单路已观测 |
| downstream height | 1280 | 单路已观测 |
| downstream format | NV12 | 单路已观测 |
| 六路 mode 一致性 | 未确认 | GAP |
| actual FPS | 未确认 | GAP |
| Sensor RAW format | 未确认 | GAP |
| multi-camera sync | 需要研究/实现 | 已确认需求方向 |

禁止把已观测 downstream NV12 反推为 Sensor RAW。

---

## 2. 先形成 workload cardinality

必须冻结：

| 参数 | 含义 | 当前 |
|---|---|---|
| N_capture | 持续采集 | 6 |
| N_detection | DNN检测 | 待定 |
| N_tracking | tracking | 待定 |
| N_depth | 深度/双目 | 待定 |
| N_vio | VIO/SLAM | 待定 |
| N_record | 编码录像 | 待定 |
| N_vlm | VLM输入 | 0 / 按需，待任务确认 |

这是 Phase 2 最重要的需求输入之一。

---

## 3. 已观测 mode 的 W1 敏感性

仅以已观测的 1072×1280 NV12 做算术，不代表实际六路 FPS：

| FPS scenario | 6路 Pixel Rate | 单份 NV12 image-plane payload |
|---:|---:|---:|
| 10 | 82.33 MP/s | 123.49 MB/s |
| 20 | 164.66 MP/s | 246.99 MB/s |
| 30 | 246.99 MP/s | 370.48 MB/s |
| 60 | 493.98 MP/s | 740.97 MB/s |
| 120 | 987.96 MP/s | 1481.93 MB/s |

这些数字只是一份 image representation。

如果存在：
- ISP write；
- resize read/write；
- AI read；
- codec read；
- copy；

DDR working traffic 会是其倍数。

所以这张表用于：
> 发现 data path 的量级，不用于直接判定某 LPDDR 峰值够/不够。

---

## 4. 能力包，而不是 TOPS 档位

### Package A — Capture / Sync / Video

Workload：
- W1
- 6 Camera capture
- synchronization
- optional encode

必须满足：
- Camera I/O；
- ISP/VPU；
- DDR；
- timestamp；
- no/drop target。

平台判断首先看 Camera subsystem，不看 NPU TOPS。

### Package B — Detection / Tracking

增加：
- W3 detection
- W5 tracking

关键参数：
- N_detection
- model/input/precision
- detection Hz
- track count

计算：
```text
inf/s = N_detection × detection_hz
```

### Package C — Obstacle / Depth / Local Avoidance

增加：
- W3 depth/obstacle
- W4 local map
- W6 local planning
- W9 safety/vehicle interface

此时开始受闭环 deadline 约束。

### Package D — VIO / SLAM / Navigation

增加：
- W2
- W4
- W6
- Camera/IMU synchronization

需要独立预算 CPU/GPU，不允许仅增加 NPU TOPS。

### Package E — Optional VLM

增加 W7，但优先级低于安全闭环。

需要：
- memory；
- TTFT；
- token/s；
- task value；
- resource isolation。

上述 Package 是产品功能组合，不是行业自主等级。

---

## 5. 第一版系统架构候选

当前只保留“候选”，不排优劣。

### Candidate 1 — Integrated SoC: RK3588

```text
6 Camera
→ RK ISP/VPU
→ DDR
→ RKNN NPU + CPU/GPU
→ FCU
```

已有证据：
- W1 SoC multimedia/camera specs；
- W3 official model benchmark；
- W2/W4 published SLAM system；
- NPU multi-context/core scheduling API。

关键未知：
- 6-camera actual ingest；
- W2+W3 concurrent Frame Age；
- DDR；
- thermal；
- actual Package C/D boundary。

### Candidate 2 — Integrated SoM: Jetson Orin

```text
6 Camera/SerDes
→ Jetson
→ CUDA/TensorRT/Isaac ROS
→ FCU
```

已有：
- Nova physical multi-camera system case；
- VSLAM/depth/mapping graph；
- current Isaac ROS graph latency。

未知：
- 本项目 1072×1280×6；
- YOLO+VIO exact concurrency；
- target power/weight。

### Candidate 3 — Integrated Robotics SoC: IQ-9075

已有：
- up to 16 Camera product capability；
- QRB ROS Camera / DMA-BUF；
- ROS SLAM/Nav2 references；
- multi-stream AI partner benchmark；
- qrb_ros_benchmark method。

未知：
- physical multi-camera/VIO numeric latency；
- full stack tail latency；
- project integration maturity。

### Candidate 4 — RK3588 Host + Accelerator

Accelerator options currently studied:
- LQ50/M50
- Metis
- Hailo

职责拆分：

```text
RK3588:
W1 ISP/VPU
W2 VIO/SLAM
W6 planning
host orchestration

Accelerator:
mainly W3
possibly W7
```

优势需要验证而不能假定：
- W3 offload；
- model capacity/scaling。

代价：
- PCIe；
- board；
- power；
- H2D/D2H；
- host remains critical。

---

## 6. 现阶段不能做的结论

现在仍不能说：
- “六摄像头需要 50/100/160 TOPS”；
- “160 TOPS LQ50 一定比 6 TOPS RK3588 更适合无人机”；
- “Jetson 一定最快”；
- “一体 SoC 一定比 accelerator 延迟低”；
- “VLM 是六摄像头无人机必需能力”。

因为 requirement vector 仍未冻结。

---

## 7. 当前最值得冻结的 8 个需求

即使暂时不能实测，也可以通过产品需求/系统设计确定：

1. 实际 Camera FPS；
2. 六路是否同 mode；
3. N_detection；
4. N_vio / N_depth；
5. 是否需要 N_record=6；
6. 最大飞行速度与目标避障工况；
7. usable detection range / keep-out；
8. 整机计算功耗、尺寸、重量边界。

这 8 项比继续搜索更多芯片参数更能推进选型。

---

## 8. Phase 2 的判断流程

```text
Requirement Card
→ W1/W2/W3/W4/W6 composition
→ resource budget
→ latency budget
→ architecture gates
→ candidate platforms
→ unresolved evidence
→ future benchmark
```

只有走完这一链，才进入产品配置建议。
