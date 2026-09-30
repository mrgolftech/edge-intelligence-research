# 平台闭环时延证据缺口审计（2026-09）

- 日期：2026-09-30
- 状态：v0.1
- 目的：对六摄像头无人平台当前最关键的时延 GAP 做一次可追溯审计，记录“已找到的公开方法、已发布的数字、不能使用的数字、下一步复现实验”。
- 机器可读表：`data/benchmarks/latency-gap-audit.csv`

## 1. 为什么要记录“负证据”

持续调研中有两类常见错误：

1. **因为厂商提供了 Benchmark 工具，就误写成已经有 Benchmark 结果。**
2. **因为某个数字带有 bandwidth / latency / FPS 字样，就把它放进错误的系统阶段。**

因此本项目把以下状态也作为长期资产：
- 官方方法存在，但目标平台公开数字未找到；
- 有硬件/模型级数字，但不能覆盖 Camera→AI→Planning；
- 有社区数字，但定义冲突，不能升级主证据；
- 某工具测的是芯片内部带宽，而不是 PCIe H2D/D2H。

“没有找到足够证据”本身不是失败；它用于约束后续结论和避免重复搜索。

## 2. IQ-9075：官方测量框架已经存在，但目标数字仍是 GAP

### 2.1 Qualcomm 官方 qrb_ros_benchmark

官方仓库：
https://github.com/qualcomm-qrb-ros/qrb_ros_benchmark

当前 README 明确：
- 目标是评估 Qualcomm robotics platform 上 ROS component performance；
- Supported Target 包含 **Dragonwing IQ-9075 EVK**；
- 基于/扩展 ROS2 Benchmark；
- 支持 QRB transport：
  - Image
  - IMU
  - PointCloud2
  - TensorList
- 支持 DMA-BUF transport：
  - Image
  - PointCloud2
- benchmark template 可配置 publisher lower/upper frequency、buffer size 等。

这意味着以下实验不是“本项目自创方法”，而是可以直接沿用官方框架：

```text
rosbag / physical source
→ QrbPlaybackNode
→ QRB/DMABUF transport
→ target ROS node(s)
→ QrbMonitorNode
→ latency / jitter / missed frames / CPU
```

### 2.2 当前官方仓库并没有发布 IQ-9075 Camera/NN 数字

截至 2026-09-30 检查当前仓库 tree：
- `results/` 公开结果仅发现 `qrb_ros_imu_qcm6490.json`；
- 该结果设备是 **QCM6490**，不是 IQ-9075；
- 未发现 Camera benchmark result；
- 未发现 NN inference benchmark result。

QCM6490 IMU JSON 说明这个框架能够输出：
- mean frame rate
- missed frames
- first/last input latency
- max/min/mean latency
- jitter
- CPU utilization
- benchmark config / OS / hostname metadata

但这些 QCM6490 数字**不能搬到 IQ-9075**。

因此 IQ-9075 当前结论是：

> **measurement method = REF；physical Camera→QNN/VIO numeric latency = GAP。**

### 2.3 qrb_ros_nn_inference 与 qrb_ros_transport

官方：
https://github.com/qualcomm-qrb-ros/qrb_ros_nn_inference
https://github.com/qualcomm-qrb-ros/qrb_ros_transport

确认：
- `qrb_ros_nn_inference` 支持 IQ-9075 EVK；
- 封装 Qualcomm AI Engine Direct / QNN Delegate；
- 输入 TensorList topic → inference → 输出 TensorList；
- 官方 README 给出 YOLOv8 detection 使用路径；
- `qrb_ros_transport` 以 DMA-BUF fd 传递 image，而不是复制图像内容；
- Camera / GPU / EVA 可通过 mmap DMA buffer 共享图像。

仍未发现：
- physical Camera → preprocessing → QNN → output 的公开 P95/P99；
- VIO/Visual SLAM 的 latency distribution；
- multi-camera + NN + SLAM 并发 Frame Age。

### 2.4 下一步复现路径

如果后续获得 IQ-9075 实机，优先使用官方框架做：

```text
Physical CSI/GMSL Camera
→ qrb_ros_camera
→ qrb_ros_transport / DMABUF
→ preprocess
→ qrb_ros_nn_inference
→ QrbMonitorNode
```

记录：
- Camera source timestamp
- first/mean/max latency
- P50/P95/P99（必要时扩展 calculator）
- missed frames
- jitter
- CPU
- NPU utilization
- DDR
- power
- 1/2/4/6 Camera scaling

再加入 VIO/SLAM 节点形成 W1+W2+W3。

## 3. Axelera Metis：数据传输可以被隐藏，但吞吐优化会增加 Frame Age

官方 Voyager SDK：
https://github.com/axelera-ai-hub/voyager-sdk/blob/latest/docs/tutorials/axruntime-python/double-buffering.md

Double Buffering 文档明确：
- inference N 计算时可传输 inference N+1 输入；
- 用于 overlap data transfer with computation；
- 文档称在 transfer overhead 显著的 workload 中通常可提高约 10–30% throughput；
- 代价是结果产生 **2×N frame delay**（N 为 workers 数）；
- 官方明确建议 latency-critical workload 不使用 double buffering。

这条证据非常重要，因为它直接说明：

> **更高 throughput 不等于更低 Frame Age。**

对 30 FPS 输入：
- 1 worker，2-frame delay 的纯帧周期量级约 66.7 ms；
- 2 workers，按文档 2×N frame delay 则为 4 frames，约 133.3 ms。

以上只是按照 frame period 的算术解释，不是 Metis 实测 H2D latency。

### 3.1 Voyager 1.8 已提供适合本项目的统计工具

Release notes：
https://github.com/axelera-ai-hub/voyager-sdk/blob/latest/RELEASE_NOTES.md

`axzoo benchmark` 可输出：
- min / mean
- P50 / P95 / P99 / P99.9 / max
- stddev / jitter
- per-operator breakdown
- per-frame device-vs-host split
- throughput
- host CPU
- peak memory
- JSON

因此 Metis 后续不缺“怎么测”的方法。

仍缺：
- RK3588 Host 上明确的 H2D/D2H absolute latency；
- live Camera → accelerator → result Frame Age；
- VIO/SLAM 同时运行时的 tail latency；
- total system power。

## 4. Hailo：硬件 inference latency 可测，但不能替代 live Camera Frame Age

官方 Hailo Model Zoo：
https://github.com/hailo-ai/hailo_model_zoo/blob/master/docs/BENCHMARKS.rst

官方建议：
`hailortcli benchmark <model>.hef`

它可以报告：
- FPS(hw_only)
- streaming FPS
- hardware latency
- streaming power

文档示例对 `resnet_v1_50.hef` 展示约：
- 1328.83 FPS(hw_only)
- 2.93646 ms hardware latency
- 3.19395 W average streaming power

但该示例页面没有把结果绑定到本项目所需的具体 Hailo SKU / Camera Host / input pipeline，因此不进入跨平台定量排序。

对于 RPi5 + Hailo，本项目真正缺的是：

```text
Camera exposure
→ rpicam/GStreamer
→ resize/color
→ Hailo queue
→ HW inference
→ postprocess
→ ROS/consumer
```

的 Frame Age P95/P99，而不是 HEF 的纯硬件 latency。

另外，Hailo Apps 中出现的 `pipeline_latency` 配置值不得当作实测结果。

## 5. Houmo M50/LQ50：bandwidth_perf 不是 PCIe Host↔Device 带宽

官方 Model Zoo：
https://github.com/houmo-ai/postmo-modelzoo/tree/release_xh2_v1.3.0/tools/bandwidth_perf

README 说明该工具用于测试：
> 后摩芯片进行模型推理的实际带宽。

源码进一步确认：
- 构造 transpose / load / store 类模型；
- 在芯片上运行模型；
- 用模型 data size × rounds / elapsed time 计算 bandwidth；
- 目标是 AI core/model memory read/write bandwidth。

XH2 官方示例约：
- write：123.43 GiB/s
- read：127.14 GiB/s

**这些数字不能解释为：**
- PCIe Gen4 x4 effective bandwidth；
- RK3588→LQ50 H2D；
- LQ50→RK3588 D2H；
- Camera frame copy latency。

因此 G08 的 `T_H2D / T_D2H` 仍然是 GAP。

这条“禁止误用”应长期保留，因为 123/127 GiB/s 很容易被误抄成 Host↔Accelerator 数据搬运能力。

## 6. RK3588：社区分阶段 P99 有启发，但完整 E2E 定义冲突

审计社区仓库：
https://github.com/dongyuzhen/rk3588-yolo/tree/release-v1.0

其 README 报告单路 1080p60、YOLOv5s INT8、RGA/RKNN/MPP pipeline 的阶段数据：
- RGA preprocess avg 2.1 ms / P99 2.6 ms；
- NPU inference avg 25.5 ms / P99 30.6 ms；
- postprocess avg 0.4 ms / P99 0.7 ms；
- RGA blend avg 3.5 ms / P99 5.5 ms；
- MPP encode avg 4.2 ms / P99 5.0 ms。

代码中的 `PerfTimer` 确实使用 steady_clock，保存 sample 并计算 percentile。

但同一仓库存在明显口径冲突：
- 阶段表又写“端到端 avg 16.6 ms / P99 22.3 ms”；
- 这小于同表 NPU 单帧 avg 25.5 ms，若是同一帧完整 E2E 则不成立；
- README 另一处又写“端到端 <200 ms”；
- benchmark plan 的示例则写约 36 ms/frame；
- 当前源码审计没有找到足够清晰的完整 capture timestamp → final result timestamp 定义来消除冲突。

因此本项目处理方式：

> **不把该仓库的 16.6/22.3 ms E2E 加入主 Benchmark 数据集。**

阶段 P99 只作为社区工程实现线索，用于帮助设计 RK3588 自测插桩，不升级 G01。

G01 仍缺：
- multi-camera
- VIO/SLAM
- DNN
- concurrent Frame Age
- DDR/power/thermal
- 明确定义的 P95/P99 E2E。

## 7. 当前缺口审计结论

| 平台/路线 | 官方/可复现测量方法 | 公开目标数字 | 当前结论 |
|---|---|---|---|
| IQ-9075 Camera→QNN | 有，qrb_ros_benchmark + DMABUF + NN node | **未找到 IQ-9075 Camera/NN result** | REF+GAP |
| IQ-9075 VIO | 有 ROS2/SLAM Reference | 无定量 latency | REF+GAP |
| Metis H2D/D2H | 有 runtime / double-buffer / axzoo profiler | 无统一 absolute H2D/D2H | REF+GAP |
| Hailo live Camera Frame Age | 有 HailoRT HW benchmark + Camera apps | HW latency 有；live E2E P99 缺 | REF+GAP |
| LQ50 H2D/D2H | 有模型 benchmark；bandwidth_perf 是内部带宽 | PCIe latency 未找到 | GAP |
| RK3588 W1+W2+W3 | 官方单模型+论文；社区单 Camera stage timing | 高等级完整并发结果未找到 | GAP |

## 8. 方法论更新

后续证据搜索遵循：

1. **方法存在 ≠ 数字存在。**
2. **吞吐优化 ≠ latency 优化。**
3. **芯片内部 bandwidth ≠ Host/PCIe bandwidth。**
4. **pipeline throughput ≠ per-frame Frame Age。**
5. **社区结果定义有自相矛盾时，不进入主 Benchmark。**
6. 已审计但未找到公开数字的 GAP，要记录搜索日期和可复现入口，避免后续重复劳动。
