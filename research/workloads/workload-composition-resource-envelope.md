# Workload Composition 资源包络：从任务组合到系统资源

- 状态：v0.1
- 日期：2026-09-30
- 目的：给 C1–C5 建立资源需求“结构包络”，不在输入不足时虚构 GB/s、TOPS 或功耗数值
- 配套：`data/calculations/workload-composition-resource-envelope.csv`

## 1. 包络不是固定数值档位

资源包络回答：
- 哪些资源必须建模；
- 哪些资源通常同时受到压力；
- 哪些指标是架构硬门槛；
- 哪些维度公开证据还不足。

在 Requirement Vector 未冻结前，不给：
- “C2 需要 50 TOPS”
- “C4 至少 32GB”
- “C1 需要 20GB/s DDR”

这类伪精确阈值。

---

## 2. C1 Multi-Camera Analytics

### 资源方程

```text
W1:
PixelRate = Σ(N×W×H×FPS)

DDR_image ≈
frame_stream × memory_passes

W3:
InferenceRate = Σ(N_detection × Hz)

W5:
TrackUpdate ≈ tracks × update_rate
```

### 首要资源

- Sensor/Network I/O
- ISP/VPU
- DDR
- NPU/GPU
- CPU postprocess/tracking
- storage

### 瓶颈征兆

- 解码/ISP 已满但 NPU 低利用；
- NPU benchmark 很高但多路视频 FPS 下降；
- CPU pre/post 先到 100%；
- DDR copy 增加导致 tail latency；
- 编码与 inference 相互影响。

---

## 3. C2 Visual Autonomy

在 C1 数据通路基础上增加：

```text
W2 localization
+ W4 local map
+ W6 planner
+ W9 safety
```

### 首要资源

- time synchronization
- CPU latency-sensitive cores
- GPU for VIO/depth/map depending implementation
- NPU/GPU perception
- DDR
- FCU/RT partition

### 资源耦合

典型冲突：
- DNN 与 VIO 共用 GPU；
- Camera/ISP 与 map 争 DDR；
- ROS queue 增加 Frame Age；
- recording/encoding 抢内存带宽；
- thermal throttling 同时拖慢 W2/W3。

因此 C2 的关键指标是：
> **Concurrent Frame Age，不是单任务 peak FPS。**

---

## 4. C3 Multi-Sensor Autonomy

新增：
- LiDAR/Radar/AIS 等 W1；
- sensor fusion；
- W5 prediction；
- redundancy。

### 首要资源

- heterogeneous I/O
- calibration/timestamp
- CPU/GPU/NPU
- memory capacity
- memory bandwidth
- functional/redundant safety path

### 典型风险

即使总数据率不一定比高分辨率 Camera 高，point cloud / BEV / temporal fusion 也可能使：
- GPU；
- memory；
- intermediate tensor；
- temporal buffer

成为主要压力。

---

## 5. C4 Foundation-Model Augmented Robotics

资源模型：

```text
Memory_total =
Base autonomy
+ W7 weights
+ activation
+ KV/context
+ visual encoder
+ runtime
```

### 首要资源

- memory capacity
- memory bandwidth
- accelerator precision support
- model compiler/runtime
- resource isolation

### 关键冲突

W7 的 token throughput 很高，但如果：
- VIO deadline miss；
- perception Frame Age 上升；
- DDR saturated；

则不能视为可产品化。

因此至少测试：
```text
base autonomy only
vs
base autonomy + W7
```

比较 tail latency degradation。

---

## 6. C5 Cooperative Autonomy

资源预算分两层。

### Onboard

```text
Single-vehicle autonomy
+ peer communication
+ local coordination
```

### Edge/Fleet

```text
state aggregation
+ global optimization
+ mission allocation
+ database/map
```

核心指标：
- network RTT/jitter/loss；
- stale state age；
- task allocation latency；
- graceful degradation。

---

## 7. 架构筛查顺序

任何 composition 都按：

1. Sensor/I/O
2. Real-Time Partition
3. Memory Capacity
4. DDR/Data Movement
5. Compute Engine
6. Concurrent Tail Latency
7. SWaP/Thermal
8. Software/Productization

顺序很重要。

例如：
- Camera 接不进来，NPU 再强也无意义；
- 车辆响应 deadline 不满足，模型 FPS 再高也不能说明安全；
- Host CPU 无法承担 SLAM，外挂 accelerator 也解决不了 W2。

---

## 8. 从“资源包络”到“平台 Candidate”

平台进入 Candidate 的最低条件：

### 已确认
- 产品形态清楚；
- I/O 基本覆盖；
- 至少有对应 workload 的 SPEC/REF/CASE/BENCH/PAPER。

### 未确认允许保留
- exact P99；
- sustained thermal；
- final power。

但这些必须成为 validation gap。

如果关键硬 Gate 已知不满足，则是 Constraint，而不是 Candidate。

---

## 9. 下一步

下一步将 C2 Visual Autonomy 套入六摄像头 Case，形成：

```text
Project Requirement
→ Nominal composition
→ Peak composition
→ Fallback composition
→ candidate architecture gate matrix
```

这会成为六摄像头项目真正的第一版系统架构比较。
