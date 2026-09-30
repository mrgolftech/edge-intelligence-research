# 系统资源预算模型：从 W1–W9 到 CPU/GPU/NPU/DDR/I/O

- 状态：v0.1
- 日期：2026-09-30
- 性质：工程计算框架
- 证据基础：本仓库已有 workload profiles、public benchmark、platform evidence
- 注意：公式用于结构化需求，不等于产品验收标准

## 1. 输出目标

把应用需求转成以下预算：

```text
CPU budget
GPU/NPU budget
DDR capacity
DDR traffic
Camera/ISP/VPU
PCIe/network/I/O
latency/deadline
power/thermal
software/runtime
```

重点是识别：
> **哪个资源先成为约束。**

---

## 2. W1 Sensor / Video

输入：

```text
N_capture
resolution
FPS
format
N_record
codec
sync requirement
```

计算：

```text
PixelRate = Σ(N×W×H×FPS)
FramePayload = Σ(N×W×H×FPS×bytes_per_pixel)
```

资源：
- CSI/SerDes；
- ISP；
- VPU；
- DDR；
- DMA；
- buffer；
- storage/network。

关键指标：
- drop；
- frame jitter；
- timestamp；
- sync error；
- sustained ingest。

---

## 3. W2 Localization / SLAM

输入：
- Camera/IMU/LiDAR 数量；
- sensor rate；
- algorithm；
- map/state size；
- update rate。

资源：
- CPU latency-sensitive threads；
- optional GPU；
- memory/cache；
- synchronization。

输出：
- update Hz；
- ATE/RPE；
- P95/P99 compute latency；
- missed deadline；
- CPU/GPU；
- map memory。

不能用 NPU TOPS 推断 W2。

---

## 4. W3 DNN Perception

输入：
- model；
- input；
- precision；
- N_detection；
- inference rate。

```text
InferenceRate = Σ(N_detection_i × Hz_i)
```

资源：
- NPU/GPU；
- CPU pre/post；
- DDR/tensor；
- queue。

输出：
- single inference latency；
- P95/P99；
- aggregate inf/s；
- per-camera effective Hz；
- drop；
- accuracy；
- power。

---

## 5. W4 Mapping / World Representation

输入：
- depth/pointcloud/BEV；
- voxel/grid resolution；
- map range；
- update rate。

资源：
- GPU/CPU；
- large memory traffic；
- map memory。

关注：
- map update latency；
- TSDF/ESDF/occupancy；
- map age；
- memory growth。

---

## 6. W5 Tracking / Prediction

输入：
- track count；
- horizon；
- update rate；
- representation。

资源可能是：
- CPU optimization；
- GPU/NPU learned prediction；
- state memory。

不能默认属于 NPU。

---

## 7. W6 Planning / Optimization

输入：
- planner type；
- horizon；
- samples/nodes；
- control/update rate。

资源：
- CPU；
- optional GPU；
- deterministic latency。

核心指标：
- P99 / WCET；
- deadline miss；
- planning success；
- path quality。

---

## 8. W7 VLM / LLM / VLA

最低内存模型：

```text
Memory =
Weights
+ Runtime
+ Activations
+ KV Cache
+ Vision Encoder
+ Buffers
+ Safety Margin
```

不能把：
`parameter_count × bits`
当成完整运行内存。

核心：
- TTFT；
- token/s；
- action latency；
- context；
- multimodal input；
- concurrent interference with W2/W3/W6。

---

## 9. W8 Multi-Agent / Fleet

重点资源：
- network；
- state sync；
- global optimization；
- edge/cloud server；
- database/storage。

端侧必须保留单机安全闭环。

---

## 10. W9 Safety / Control

通常需要与 Linux AI workload 分开看：
- FCU/MCU/RT subsystem；
- watchdog；
- safety monitor；
- vehicle interface；
- fail-safe。

安全控制不应被“AI TOPS”覆盖。

---

## 11. 并发预算

真实资源不是各 workload 峰值简单相加。

定义：

```text
C = {W_i(t)}
```

即每个 workload 的运行占空、周期、并发。

至少建立三种工况：
- Nominal；
- Peak；
- Degraded/Fallback。

例如：

```text
Nominal:
W1 6-camera always
W2 stereo VIO 30Hz
W3 4-camera detection 15Hz
W6 20Hz
W7 off

Peak:
W1 6-camera
W2 stereo VIO
W3 6-camera detection
W4 depth/map
W6
recording on

Fallback:
W1 reduced
W2
W6
W9
disable noncritical W3/W7
```

以上只是格式示例；具体数字必须由项目 requirement card 冻结。

---

## 12. 资源余量

建议分别记录：

```text
Headroom_compute
Headroom_memory
Headroom_DDR
Headroom_I/O
Headroom_power
Headroom_latency
```

不建议用单一“30%系统余量”覆盖所有维度。

每种 margin 应说明来源：
- requirement uncertainty；
- software evolution；
- thermal；
- model upgrade；
- manufacturing；
- safety。

---

## 13. 资源瓶颈分类

最终输出瓶颈类型：

- SENSOR_IO_LIMITED
- ISP_VPU_LIMITED
- CPU_LATENCY_LIMITED
- NPU_THROUGHPUT_LIMITED
- GPU_LIMITED
- DDR_BANDWIDTH_LIMITED
- MEMORY_CAPACITY_LIMITED
- PCIE_LIMITED
- THERMAL_LIMITED
- POWER_LIMITED
- SOFTWARE_OPERATOR_LIMITED
- REALTIME_ISOLATION_LIMITED
- EVIDENCE_GAP

这比“算力不够”更能指导产品设计。
