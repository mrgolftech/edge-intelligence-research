# Host/Accelerator 与 ROS2 时延复现实验入口

- 日期：2026-09-30
- 状态：v0.1
- 目的：把“公开数字不足”转换成未来拿到硬件后可以直接执行的实验入口。
- 原则：优先复用厂商官方 profiler/benchmark harness；不自行造与厂商 runtime 无关的微基准来替代真实 pipeline。

## IQ-9075

官方组件：
- qrb_ros_camera
- qrb_ros_transport / DMABUF
- qrb_ros_nn_inference
- qrb_ros_benchmark

推荐图：

```text
Physical Camera
→ qrb_ros_camera
→ QRB/DMABUF Image
→ preprocess
→ TensorList
→ qrb_ros_nn_inference
→ postprocess
→ QrbMonitor
```

至少记录：
- source timestamp / result timestamp
- mean / P50 / P95 / P99 / max
- jitter
- missed frames
- CPU
- NPU
- DDR
- 1/2/4/6 camera scaling

第二阶段插入 VIO/SLAM 与 Nav2/Planner。

## Metis

Voyager v1.8 推荐：
- `axzoo benchmark --json`
- per-frame device-vs-host split
- P50/P95/P99/P99.9
- CPU / peak memory

必须做 double buffering A/B：
- OFF：latency-oriented
- ON：throughput-oriented

记录 input→output frame identity，避免 double buffer 导致结果与输入错配。

## Hailo

两层分开测：

### 层1：HEF hardware
```bash
hailortcli benchmark model.hef
```

得到：
- hw latency
- hw/streaming FPS
- power

### 层2：live pipeline

在 Camera source 和 postprocess consumer 打时间戳：
- GStreamer/rpicam
- resize/convert
- Hailo queue
- inference
- postprocess

最终接受指标是 live Frame Age，不是 layer1 的 hw-only latency。

## M50/LQ50

不要使用 `bandwidth_perf` 代替 PCIe 测试。

需要自行拆：
- `T_host_preprocess`
- `T_H2D`
- `T_accel_queue`
- `T_model`
- `T_D2H`
- `T_host_postprocess`

并同时记录：
- PCIe generation/width
- Host DDR
- accelerator utilization
- total power

## RK3588

社区工程实现提示应吸收的是**插桩方法**而不是有冲突的 E2E 数字。

至少打点：
- sensor/capture timestamp
- NV12 ready
- RGA preprocess begin/end
- RKNN submit/complete
- postprocess
- VIO result
- fusion/map result
- planner result

测试：
- 1/2/4/6 streams
- detection only
- VIO only
- detection+VIO
- detection+VIO+mapping/planning
- 30/60/120 min thermal steady state

输出统一使用 P50/P95/P99/max、drop、queue depth 和 Frame Age。
