# IQ-9075：ROS2 自主栈与多流视觉公开证据

- 日期：2026-09-30
- 状态：verified-public-evidence

## 1. W1：官方 Camera / Zero-Copy 路径
Qualcomm 官方 qrb_ros_camera：https://github.com/qualcomm-qrb-ros/qrb_ros_camera

IQ-9075 EVK 支持 CSI/GMSL、concurrent multiple streams、ROS2 composable node 和 DMA-BUF zero-copy。默认示例 1920×1080@30，并演示第二 stream 1080×720@60。这里属于 REF，不是最大 Camera 吞吐 Benchmark。

### 1.1 Per-frame timestamp 已确认，但 multi-camera hardware sync 未确认

源码证据：
- `qrb_camera/src/qmmf_frame.cpp`：`CameraFrame.timestamp` 取自底层 camera buffer timestamp；
- `qrb_ros_camera/src/camera_node.cpp`：初始化 `time_offset_`，并将 `frame->timestamp + time_offset_` 写入 ROS `header.stamp`；
- CameraNode 同时用该 timestamp 计算 FPS 与采集到发布的平均 latency。

这说明 IQ-9075 的 W1 Camera pipeline 已经具备可用于 ROS 时序处理的 per-frame timestamp 传播机制。

但是当前官方仓库搜索没有发现明确的 multi-camera synchronization / external trigger API。因此当前结论必须严格写成：

> **单帧时间戳传递：已确认；多物理 Camera 硬件同步：未确认。**

后续六摄像头验证仍需测：
- 同一 trigger 下各 Camera exposure/start-of-frame offset；
- timestamp skew；
- frame sequence alignment；
- 长时间 drift；
- dropped frame 后的重新对齐行为。

## 2. W2/W6：官方 SLAM / Nav2 路径
qrb_ros_amr_service：https://github.com/qualcomm-qrb-ros/qrb_ros_amr_service

功能包括 2D LiDAR SLAM mapping/localization、P2P navigation、path following、mapping service 与 Nav2。Supported target 明确为 IQ-9075 EVK。

因此 W2/W6 可升级为 REF，但没有 ATE/RPE、SLAM Hz、planner latency、CPU/DDR/power 等定量结果。

## 3. W1+W3：iQS-Streampipe 可复现多流 Benchmark
来源：https://github.com/InnoIPA/iQ-Studio/tree/main/benchmarks/iqs-streampipe

条件：EXMP-Q911（IQ-9075）、8 CPU cores、Normal power、NPU、TFLite/QNN 2.32、YOLOv10n INT8 640×640、1080p30 H.264、warm-up 180s、test 300s。

| Streams | CPU | Memory | Avg E2E FPS/channel |
|---:|---:|---:|---:|
| 1 | 24.2% | 6.6% | 29.46 |
| 4 | 51.0% | 8.6% | 29.47 |
| 9 | 93.6% | 12.0% | 28.41 |
| 16 | 99.8% | 17.7% | 15.90 |

工程含义：1→9 streams 时 per-channel 接近 30FPS；16 streams 时 CPU 达 99.8%，FPS 降到 15.90，说明完整 pipeline/CPU 编排会先于理论 NPU TOPS 暴露瓶颈。

关键限制：这些是 H.264 文件流，不是 16 路物理 CSI/GMSL Camera。

## 4. 10-stream InnoPPE：1 路真实 UVC
来源：https://github.com/InnoIPA/iQ-Studio/blob/main/benchmarks/innoppe/README.md

条件：IQ-9075 EVK、YOLOv10n INT8/QNN、10×1080p30、1 UVC MJPEG + 9 H.264 files。

结果图：25.0 FPS（UVC channel）、CPU 99.6%、memory 14.6%、accelerator 67.2%。只有 1 路 live camera，所以仍不是 10-camera benchmark。

## 5. 官方 AI/Robotics Samples
https://github.com/qualcomm-qrb-ros/qrb_ros_samples

IQ-9075 EVK 支持示例包含 YOLOv8 detection、segmentation、pose、Depth Anything V2、Follow Me、2D LiDAR SLAM、Navigation2。均属于 REF，不是 BENCH。

## 6. 对六摄像头 Case 的剩余问题
公开证据已经能证明多流视频+DNN、ROS2 camera/zero-copy、SLAM/Nav2、实时 EtherCAT 都有真实实现路径。

仍不能证明：
1. 6 个物理 Camera 的硬件同步、timestamp skew、drop/jitter（per-frame timestamp 传播已确认，但同步机制未确认）；
2. Camera→ISP→DMA-BUF→QNN 的六路端到端性能；
3. VIO/visual SLAM 定量性能；
4. W1+W2+W3+W6 全并发；
5. 持续功耗、热稳态和降频。
