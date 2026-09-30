# 六摄像头自主避障：闭环时延预算 → 平台架构映射

- 状态：v0.1
- 日期：2026-09-30
- 目的：把避障的 deadline 从“一个总毫秒数”拆到架构阶段，并用公开证据标记可量化项与证据空白
- 输入：
  - `research/workloads/avoidance-latency-budget.md`
  - `data/benchmarks/pipeline-latency-evidence.csv`

## 1. 先算“还能留给计算链多少时间”

已有模型：

```text
D_required =
D_keepout
+ v × (T_sample + T_pipeline + T_vehicle)
+ D_brake_or_turn
```

反过来，如果任务已经给出：

- usable detection distance `D_detect`
- speed `v`
- sensor update rate `f`
- measured vehicle response `T_vehicle`
- keep-out `D_keepout`
- measured/validated braking-or-turning distance `D_maneuver`

则平台计算链的最大允许时间为：

```text
T_pipeline,max =
(D_detect - D_keepout - D_maneuver) / v
- 1/f
- T_vehicle
```

如果结果 ≤ 0：

> **即使计算平台“零延迟”，当前 sensor range / update rate / vehicle dynamics 组合也不满足该筛查条件。**

这时继续加 TOPS 没有意义，应修改探测距离、传感器频率、速度或车辆响应。

## 2. T_pipeline 不按拍脑袋百分比分配

```text
T_pipeline =
T_sensor/ISP
+ T_queue/preprocess
+ T_W2_localization
+ T_W3_perception
+ T_W4_mapping/fusion
+ T_W6_planning
+ T_command
```

本项目不预设：
- perception 50%
- SLAM 20%
- planning 10%

之类比例。

正确做法是：
1. 用公开 BENCH/REF 给已有阶段填量级；
2. 对本项目运行时测 P95/P99；
3. 未知项保持 GAP；
4. 最终看各阶段 P99 之和及异步 queue/frame-age，而不是平均值简单相加。

## 3. 当前公开阶段时延证据

### Jetson Orin / 一体 SoM

Isaac ROS 5.0 / AGX Orin：
- Stereo Disparity Graph 1080p：9.3 ms @30Hz；
- DNN Stereo Full 576p：17 ms @30Hz；
- DetectNet Graph 544p：15 ms @30Hz；
- RT-DETR Graph 720p：13 ms @30Hz；
- Nvblox TSDF：0.5–0.8 ms（dataset dependent）；
- Nvblox ESDF：1.5–1.7 ms（dataset dependent）。

强项：
- W1/W2/W3/W4 可共享一体化 GPU/内存数据路径；
- 当前软件明确支持 Jetson Orin；
- VSLAM/Nvblox 直接给出 camera timing requirements。

缺口：
- 当前 5.0 未给出与六摄像头同构的 W1+W2+W3+W4+W6 P99；
- 公开 graph latency 不是 P99；
- 没有本项目 1072×1280×6 + YOLO/VIO workload；
- command/vehicle response 不由 Orin 决定。

### IQ-9075 / 一体 SoC

已有：
- W1 Camera timestamp → ROS stamp 路径；
- DMA-BUF zero-copy Reference；
- 1/4/9/16 stream W1+W3 throughput；
- ROS2 SLAM/Nav2 Reference；
- EtherCAT ~100 μs round-trip / <8 μs jitter partner benchmark。

但对本时延预算真正缺少的是：
- physical camera → QNN result latency；
- VIO/visual SLAM latency；
- map/fusion latency；
- SLAM+AI+planning P95/P99。

所以当前不能因为 100 TOPS 或 16-camera capability 给出闭环 deadline 判断。

### RK3588 / 一体 SoC

已有：
- RKNN 单模型 INT8 throughput；
- SLAM 论文系统证据；
- 三核 NPU / multi-context 官方调度路径。

缺少：
- 官方 RKNN FPS 对应的统一 E2E latency/P99；
- 多 Camera capture + VIO + DNN 并发 Frame Age；
- DDR / queue / thermal 下的 tail latency。

因此 RK3588 当前最大的证据缺口不是“能不能跑 YOLO”，而是：
> **并发后 Frame Age 会变成多少。**

### RK3588 + M50 / Host+Accelerator

M50-compatible xh2：
- YOLOv5s E2E avg 9.715 ms，P99 9.834 ms；
- YOLO11m E2E avg 19.917 ms，P99 20.207 ms。

这是当前候选中少数直接公开 **P99** 的 W3 数据。

但仍缺：
- Camera/ISP → RK3588 preprocess；
- Host→LQ50 PCIe；
- accelerator result→Host；
- W2/W4/W6 与 feeding 同时运行；
- full Frame Age P99。

因此这些 9.8/20.2 ms 只能填 `T_W3_model`，不能填 `T_pipeline`。

### RK3588 + Metis / Host+Accelerator

Axelera Team 的 NanoPC-T6 数据给出：
- YOLOv8n：61 ms OpenCL latency；
- YOLOv8s：77 ms OpenCL latency。

它证明 ARM Host 路线有实际 latency 数据，但条件仍不完整：
- exact Metis SKU/input/precision 未全部公开；
- “OpenCL latency”统计边界需按 SDK 复现；
- Camera/VIO/SLAM/PCIe/full pipeline 未覆盖。

### Raspberry Pi 5 + Hailo / Host+Accelerator

当前官方材料证明：
- Camera stack；
- multisource；
- Hailo offload；
- 多流应用路径。

但没有足够统一的 P95/P99 E2E latency。

因此在 deadline mapping 中继续标 **GAP**，不能拿 TOPS 或“实时”描述替代毫秒证据。

## 4. 架构对时延预算的影响

### 一体 SoC/SoM

```text
Camera
→ ISP
→ shared memory / zero-copy
→ GPU/NPU
→ map/SLAM/planner
→ FCU
```

需要重点看：
- shared DDR contention；
- GPU/NPU并发调度；
- ROS queue；
- thermal throttling；
- tail latency。

优势不能写成“必然更低延迟”，只能写：
> 物理上可减少跨 PCIe accelerator 的一次 host/device 边界，且部分平台已有 zero-copy/shared-buffer 软件路径。

### Host + Accelerator

```text
Camera
→ Host ISP/VPU
→ Host preprocess
→ H2D / PCIe
→ Accelerator
→ D2H / result
→ Host fusion/SLAM/planner
→ FCU
```

新增重点项：
- `T_H2D`
- `T_accel_queue`
- `T_D2H`
- Host DDR copy
- PCIe contention

但是不能预先断言它一定更慢，因为：
- accelerator 的 W3 可能显著更快；
- pipeline 可异步；
- data copy 可优化；
- model output 往往远小于 image input。

最终比较对象仍是：
> **同一 workload 下的 Frame Age P95/P99 + deadline miss + total power。**

## 5. 当前“证据覆盖率”而不是平台评分

| 路线 | W1 Camera时序 | W2 VIO/SLAM latency | W3 latency | W4 map latency | W6 planner | 完整P99 |
|---|---|---|---|---|---|---|
| Jetson Orin | CASE/REF | 系统CASE；当前直接Orin latency不完整 | BENCH | BENCH | 通用planner证据 | GAP |
| IQ-9075 | REF | REF，无量化 | throughput BENCH，latency GAP | REF | Nav2 REF | GAP |
| RK3588 | SPEC | PAPER(system) | throughput BENCH，latency GAP | PAPER(system) | INFER/通用 | GAP |
| RK3588+M50 | Host依赖 | Host依赖 | **VENDOR_BENCH含P99** | Host依赖 | Host依赖 | GAP |
| RK3588+Metis | Host依赖 | Host依赖 | VENDOR_BENCH latency | Host依赖 | Host依赖 | GAP |
| RPi5+Hailo | REF | Host依赖 | REF/厂商量级 | Host依赖 | Host依赖 | GAP |

这里不产生分数，不选“赢家”。

## 6. 下一步最值得补的数字

如果只能继续联网调研，优先级应为：

1. IQ-9075 physical camera → QNN latency / VIO latency；
2. RK3588 RKNN 的可复现 single-frame latency + multi-stream Frame Age；
3. LQ50/Metis 的 H2D/D2H 与 Camera pipeline timing；
4. Hailo RPi5 live-camera end-to-end latency；
5. 任一候选平台的 W1+W2+W3+W6 P95/P99。

这些数据比再补 10 个 TOPS 规格更能改变平台判断。
