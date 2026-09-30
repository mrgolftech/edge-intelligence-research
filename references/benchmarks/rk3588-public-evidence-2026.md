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


## 3. 并发与三核 NPU 的公开证据边界

### 3.1 官方支持的并行机制

Rockchip 官方 RKNPU2 API 已确认：

- `rknn_dup_context` 可复制 RKNN context；
- `rknn_set_core_mask` 可选择 NPU core；
- RK3588 支持 `CORE_0`、`CORE_1`、`CORE_2`、`CORE_0_1`、`CORE_0_1_2`；
- 官方 `rknn_benchmark` 支持通过 `core_mask` 指定 1/2/3 核组合。

来源：
- https://github.com/airockchip/rknpu2/blob/master/runtime/RK3588/Linux/librknn_api/include/rknn_api.h
- https://github.com/airockchip/rknn-toolkit2/blob/master/rknpu2/examples/rknn_benchmark/README.md

这足以证明：
> **RK3588 的 RKNN 软件栈存在多 context / 多 NPU core 的官方调度路径。**

但它不是吞吐 Benchmark，不能据此假设“三核 = 三倍 FPS”。

### 3.2 版本必须冻结

Rockchip 官方 RKNN Model Zoo 明确说明：
- demos 按最新 RKNPU SDK 验证；
- 使用更低版本时，inference performance 和 inference results 可能错误；
- 当前 Model Zoo 2.3.2 对应 RKNPU2 SDK >= 2.3.2。

因此以后任何 RK3588 Benchmark 必须同时记录：
- RKNN Toolkit / Model Zoo revision
- librknnrt / RKNPU2 SDK
- kernel NPU driver
- model export / quantization version
- NPU core mask
- CPU / DDR / NPU frequency

### 3.3 社区问题只能作为风险信号

官方 issue 中存在旧版本多核/多线程部署问题报告，例如：
- 2025-12 的 issue #474：SDK 1.5.2 / driver 0.9.8 下，三个线程分别绑定三个 NPU core 跑 YOLOv5s，用户报告偶发结果串扰；
- 2024 的 issue #129：用户报告 YOLOv5s 使用 3-core core_mask 时并未获得线性加速。

这些都是**用户问题报告**，不是经 Rockchip 确认的当前版本缺陷或 Benchmark。

因此本项目只把它们用于确定验证项：
- 多 context 隔离；
- 多 core scaling；
- SDK/driver version sensitivity；
- 长时间并发稳定性。

不得写成“RK3588 三核并行有已知缺陷”或“多核没有收益”。

## 4. 当前结论

RK3588 当前证据已经分成三层：

1. **W3 单模型性能：BENCH** —— 官方 RKNN Model Zoo；
2. **W2/W4 真实 SLAM 系统：PAPER(system)** —— ROIV-SLAM；
3. **NPU 并行实现路径：REF** —— 官方 context/core-mask API 与 benchmark 工具。

仍然缺失的是最关键的系统级数据：
> **多路物理 Camera + SLAM/VIO + 多模型 DNN 的并发吞吐、deadline、DDR、功耗和热稳态。**

因此这一项继续保持 GAP，而不是根据三核 NPU 或单模型 FPS做线性推算。
