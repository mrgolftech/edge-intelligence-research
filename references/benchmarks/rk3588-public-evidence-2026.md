# RK3588：官方 DNN Benchmark 与 SLAM 论文证据

- 日期：2026-09-30
- 状态：verified-public-evidence

## 1. W3：Rockchip 官方 RKNN Model Zoo

来源：
- https://github.com/airockchip/rknn_model_zoo

当前官方 README 的性能表明确：
- RK3588 列为 `@single_core`
- INT8、[1,3,640,640]
- YOLOv8n 73.5 FPS
- YOLOv8s 38.0 FPS
- YOLOv8m 16.2 FPS
- YOLO11n 60.0 FPS
- YOLO11s 33.0 FPS
- YOLO11m 12.7 FPS

官方同时说明：
- 使用各平台最大 NPU 频率；
- 性能数据默认只计算模型 inference；
- 未特别注明时不包含 pre/post-processing。

### 工程含义
这足以证明 RK3588 的 W3 不应再只写“6 TOPS / 理论可做 detection”，而是存在官方模型级定量证据。

但它仍不能回答：
- 六路视频同时输入；
- 六路分别跑 DNN；
- ISP/VDEC + NPU + CPU 后处理并发；
- SLAM 与 detection 同时运行；
- 长时间热稳态。

这些问题继续保留 GAP。

## 2. W2/W4：ROIV-SLAM 同行评审论文

论文：
Feng C, Ren C, Gao W, et al. ROIV-SLAM: Rotation-Optimized Inertial–Visual SLAM for a Non-Coaxial Two-Wheeled Robot Under Roll Disturbances. Sensors. 2026;26(13):4053.

DOI：
https://doi.org/10.3390/s26134053

实验平台：
- RK3588 embedded platform
- RGB-D 30 Hz
  - RGB 1920×1080
  - Depth 640×480
- IMU 200 Hz
- 2D LiDAR 12 Hz
- LiDAR 20,000 points/s
- wheel odometry

算法链：
- EKF multi-sensor fusion
- RGB-D ground-normal constraint
- SO(3) rotation optimization
- sliding-window factor graph
- visual + LiDAR loop closure

### 工程含义
这是“RK3588 上运行真实多传感器 SLAM/Mapping”的论文证据，可用于 W2/W4 的平台存在性判断。

### 证据边界
论文不是 ORB-SLAM3 benchmark，也没有公开：
- 每帧计算 latency
- CPU/GPU/NPU utilization
- DDR bandwidth
- system power
- 与 DNN 并发时的性能

因此不能用它推导六摄像头项目所需 FPS/TOPS。
