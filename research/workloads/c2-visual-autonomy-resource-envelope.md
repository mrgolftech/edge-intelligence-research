# C2 Visual Autonomy：可量化资源包络与 Gate 输入模型

- 状态：v0.2
- 日期：2026-09-30
- 对象：C2 Visual Autonomy
- 对应 workload：W1 + W2 + W3 + W4 + W6 + W9（可选 W5）
- 证据锚点：`references/webpages/c2-visual-autonomy-resource-anchors-2026.md`
- 配套数据：`data/calculations/c2-visual-autonomy-reference-envelope.csv`
- 配套脚本：`scripts/calc_c2_visual_autonomy_reference_envelope.py`

## 1. 目标

把 C2 从“资源结构 HIGH/MEDIUM”推进为可计算的工程模型：

```text
Sensor / Camera
→ image-plane / buffer
→ W2 localization
→ W3 perception/depth
→ W4 map
→ W6 planner
→ FCU / W9
→ vehicle response
```

输出不是“需要多少 TOPS”，而是：

- Camera pixel rate；
- image representation rate；
- buffer footprint；
- model invocation rate；
- 每个 compute engine 的 service demand；
- queue / Frame Age；
- closed-loop deadline；
- SWaP/thermal；
- 最终 Architecture Gate 的可验证条件。

---

## 2. W1：Camera 与图像数据率

### 2.1 Pixel Rate

```text
PixelRate = Σ(N_i × W_i × H_i × FPS_i)
```

### 2.2 单份图像表示流量

```text
ImagePlaneRate =
Σ(PixelRate_i × BytesPerPixel_i)
```

必须注明 representation：

- RAW10/RAW12；
- YUV/NV12；
- RGB888；
- grayscale；
- tensor。

不能混用。

### 2.3 Buffer Memory

```text
M_buffer =
Σ(N_stream × W × H × BytesPerPixel × QueueDepth)
```

这只是 frame buffer，不包括：
- ISP internal buffers；
- tensor；
- VIO state；
- map；
- codec；
- model weights；
- runtime。

### 六摄当前已知几何的计算

当前只确认：

- N_capture = 6；
- downstream geometry = 1072×1280；
- observed representation = NV12；
- actual FPS = GAP。

单帧：

```text
1072 × 1280 × 1.5
= 2.05824 MB / stream
```

六路同一时刻一组 frame：

```text
6 × 2.05824
= 12.34944 MB
```

如果仅做 queue-depth 敏感性：

- depth 1：12.35 MB；
- depth 4：49.40 MB。

这只是 frame queue，不能当整机 memory requirement。

若假设性分析：

| FPS | Pixel Rate | 一份 NV12 image-plane |
|---:|---:|---:|
| 20 | 164.659 MP/s | 246.989 MB/s |
| 30 | 246.989 MP/s | 370.483 MB/s |
| 60 | 493.978 MP/s | 740.966 MB/s |

其中 20/30/60 Hz 目前分别是 sensitivity/stress 点，**不是项目已确认 FPS**。

---

## 3. DDR：用 data movement 建模，不用峰值带宽拍脑袋

定义：

```text
BW_DDR_working ≈
Σ(ImagePlaneRate × effective_pass_equivalent)
+ W2 state/map traffic
+ W3 tensors
+ W4 map update
+ codec
+ OS/runtime
```

`effective_pass_equivalent` 不能永久假设为 3、5 或 8。

它需要未来通过：
- DMA / zero-copy 路径分析；
- memory controller counter；
- profiler；
- ROS transport；
- accelerator H2D/D2H

进行测量。

当前阶段正确做法是：

```text
BW_DDR = f(copy_count, zero_copy, model, map, codec)
```

并把 copy count 作为架构变量。

---

## 4. W3：先计算 invocation rate，再绑定 Benchmark

```text
InferenceRate_total =
Σ(N_detection_i × DetectionHz_i)
```

例如：

```text
4 cameras × 15 Hz = 60 inference/s
6 cameras × 20 Hz = 120 inference/s
```

以上只是算式示例，不代表项目需求。

### 4.1 Service Demand

对一个明确 engine（CPU / GPU / NPU / Accelerator），定义：

```text
Demand_engine =
Σ(InvocationRate_i × ServiceTime_i)
```

其中：
- InvocationRate：次/s；
- ServiceTime：同一平台、同一模型/输入/精度/软件条件下的 measured service time；
- Demand 为“每秒需要多少秒的该 engine 服务时间”。

如果同一 engine 完全串行，Demand > 1 表示该 workload 组合没有排队稳定余量。

但：

> Demand < 1 也不能证明 P99 满足。

因为还存在：
- batching；
- pipeline overlap；
- multi-core/multi-engine；
- pre/postprocess；
- DDR contention；
- runtime scheduling；
- queue jitter。

因此这个公式用于**资源可行性初筛**，不是 P99 预测器。

---

## 5. W2/W4/W6：不要折算成 NPU TOPS

### W2 VIO/SLAM

至少记录：

- N_vio；
- mono/stereo/multi-camera；
- Camera/IMU rate；
- CPU thread/core time；
- optional GPU time；
- map/state memory；
- update latency P95/P99；
- synchronization error。

### W4 Local Mapping

至少记录：

- depth source；
- map representation；
- voxel/grid size；
- map range；
- update Hz；
- map memory；
- CPU/GPU service time。

### W6 Planning

至少记录：

- planner；
- update Hz；
- horizon/samples；
- CPU/GPU service time；
- P99/WCET；
- deadline miss。

只有把这三类资源与 W3 分开，才能判断：

- 一体 SoC 是否合适；
- Host + Accelerator 是否真的降低 Host 压力；
- 高 TOPS 是否只解决了 W3。

---

## 6. C2 真正的核心：Frame Age 与闭环距离

定义：

```text
T_frame_age =
T_sample_wait
+ T_sensor/ISP
+ T_queue
+ T_preprocess
+ T_W2/W3/W4
+ T_W6
+ T_command
```

完整车辆闭环：

```text
T_closed_loop =
T_frame_age
+ T_vehicle_response
```

反应距离：

```text
D_reaction =
VehicleSpeed × T_closed_loop
```

### PX4 事实锚点

PX4 当前文档给出：

- external vision sensor delay：可高至约 0.2 s；
- velocity-setpoint tracking delay：典型约 0.1–0.5 s；
- 初始 companion 测试点：
  - 4 m/s；
  - OBSTACLE_DISTANCE 10 Hz。

只做 CALC：

```text
0.2 + (0.1 ... 0.5)
= 0.3 ... 0.7 s

4 m/s × delay
= 1.2 ... 2.8 m
```

这已经说明：

> 在 UAV 避障里，几十毫秒 DNN latency 只是闭环的一部分。

若再人为加入一个 10 Hz sampling period 做保守敏感性，则可达到：

```text
0.4 ... 0.8 s
→ 1.6 ... 3.2 m @ 4 m/s
```

但该项可能与 sensor delay 定义重叠，因此不得当成 PX4 的产品结论。

---

## 7. Reference Profile / Project Nominal / Stress 必须拆开

### Reference

来自：
- nuScenes；
- TUM VI；
- NVIDIA Hawk / Isaac ROS；
- PX4；
- 其他公开系统/论文。

作用：
- 给输入量级；
- 给算法/系统结构；
- 给 service-time 或 update-rate 锚点。

### Project Nominal

六摄项目真正长期运行状态。

**当前仍 PENDING。**

缺：
- actual FPS；
- N_detection；
- N_vio；
- N_depth；
- N_record；
- speed；
- usable detection range；
- keep-out；
- power/mass。

### Stress

用于未来验证：

- higher FPS；
- more detection streams；
- recording on；
- depth/map on；
- thermal steady state。

Stress 只能用于验证余量，不能冒充需求。

---

## 8. C2 → Architecture Gate 的量化输入

### Gate A — Sensor / I/O

输入：
- N_capture；
- per-camera mode；
- CSI/SerDes lane；
- sync/timestamp；
- encode requirement。

Pass 条件形式：

```text
target streams sustained
AND no unacceptable drop
AND sync error <= requirement
```

当前项目缺 target FPS 和 sync tolerance。

### Gate B — Real-Time Partition

输入：
- FCU/MCU responsibilities；
- Linux responsibilities；
- failsafe；
- communication deadline。

当前第一版原则仍是：
- flight-control / actuator hard loop 独立；
- Linux AI compute 不默认替代 FCU。

### Gate C — Memory / DDR

Memory：

```text
OS + runtime + models + activation
+ frame queues + VIO/map + codec
+ safety margin
```

DDR：

```text
measured working traffic
< sustainable traffic under target thermal mode
```

不允许用理论 LPDDR peak 直接 Pass。

### Gate D — Compute Engine

分别计算：

- CPU demand；
- GPU demand；
- NPU/accelerator demand；
- ISP/VPU；
- PCIe if external accelerator。

### Gate E — Concurrent Tail Latency

核心判据：

```text
P99 Frame Age <= project deadline
AND deadline miss <= project target
```

当前仍是四条候选路线共同最大 GAP。

### Gate F — SWaP / Thermal

必须冻结：

- steady compute power；
- max power；
- cooling；
- mass；
- envelope；
- mission duration。

### Gate G — Software / Productization

要求：
- target models/operators；
- ROS/Linux；
- profiling；
- diagnostics；
- lifecycle；
- supply；
- domestic sourcing；
- integration effort。

---

## 9. 当前对六摄 Case 的新工程判断

在不虚构需求的前提下，现在已经可以确认：

1. **1072×1280 NV12 六路的一组 frame 本身约 12.35 MB。**
2. 单纯把 queue depth 从 1 增到 4，frame queue 就从约 12.35 MB 增至约 49.40 MB；这还没进入模型和 map。
3. 20/30/60 Hz 下，一份 NV12 image-plane 流量分别约 247 / 370 / 741 MB/s；实际 DDR 工作流量可因 copy/resize/codec/tensor 路径高出多倍。
4. C2 平台的核心不是“峰值 AI throughput”，而是多 workload 的 **service demand + data movement + tail latency**。
5. PX4 的公开 delay 数据表明，vehicle response 量级可能明显大于单模型 10–20 ms 推理；因此必须优先冻结 speed / detection range / keep-out。
6. Project Nominal 仍未冻结，所以当前任何平台只能做 Candidate / Unverified，不能给 Confirmed-fit。

---

## 10. 下一步

下一轮把本模型直接套到六摄像头 Case，形成：

```text
Requirement Variable
→ formula
→ evidence anchor
→ current value / GAP
→ Gate affected
→ benchmark needed
```

重点形成一张 **C2 Requirement-to-Gate Traceability Matrix**。

这张矩阵会把“还缺什么需求”与“为什么无法判平台”一一对应，作为后续方案收敛和最终报告第 4–7 章的骨架。
