# Jetson AGX Orin / Nova Carter：物理多相机自主感知整图 Benchmark

- 日期：2026-09-30
- 状态：verified-public-evidence
- 软件基线：Isaac ROS release-3.2（历史版本基线；不是当前 latest 性能声明）
- 目的：记录目前公开资料中最接近“物理多 Camera + VSLAM + DNN 深度 + 3D Mapping”组合 workload 的系统级证据。

## 1. 为什么这组数据重要

大量边缘 AI benchmark 只测单模型 inference。Nova Carter / Isaac Perceptor 的价值在于：

- 输入来自真实多摄像头机器人平台；
- 有硬件同步；
- Benchmark 对象包含完整 ROS graph；
- Visual SLAM、DNN Stereo Depth、Nvblox 可以形成组合路径；
- NVIDIA 公布了 live graph 的持续吞吐，而不是只给峰值 TOPS。

因此它更适合本项目用于建立 W1+W2+W3+W4 的“系统级量级锚点”。

## 2. 物理传感器与同步

Nova Carter 使用 Jetson AGX Orin，并包含：
- 4× HAWK stereo camera module，1920×1200，60 FPS；
- **一个 Hawk 模块内部包含两个同步的 global-shutter 1920×1200 imagers**；
- 4× OWL fisheye camera，1920×1200，120 FPS；
- 32-beam 360° LiDAR、2× planar LiDAR、IMU 等。

官方文档给出的同步能力：
- hardware timestamp + PTP；
- sensor acquisition time < 10 μs；
- 单一 hardware trigger 下所有 camera simultaneous capture within 100 μs；
- sensor capture to rosbag 可到 4 GB/s。

来源：
https://nvidia-isaac-ros.github.io/v/release-3.1/robots/nova_carter/index.html

## 3. Isaac ROS release-3.2 Live Graph 数据

来源：
https://nvidia-isaac-ros.github.io/v/release-3.2/performance/index.html

| Live Graph | 输入 | 公开结果 |
|---|---|---|
| Data Recorder | 4 Hawk stereo modules, 1200p | 22.4 FPS/stream avg；0 dropped frames avg |
| Multicam Visual SLAM | 4 Hawk stereo modules, 1200p | 30.1 FPS |
| DNN Stereo Disparity | 3 Hawk stereo modules, 1200p；1×Full ESS + 2×throttled Light ESS | Full 30.2 FPS；Light 15.2 FPS avg |
| Perceptor | 3 Hawk stereo modules, 1200p | Visual Odometry 30.0 FPS；Nvblox ESDF 9.45 FPS；Mesh 2.63 FPS |

## 4. Benchmark 方法

NVIDIA 对该页面的统一说明：
- 使用 Isaac ROS Benchmark；
- 配置文件可通过各 benchmark launch script 复现；
- FPS 是 accelerated computational pipeline 的 maximum sustained framerate；
- 测量范围为 input node → graph of node(s) → output node；
- input rate 自动调节，以寻找 dropped frames <5% 下的峰值持续吞吐；
- FPS 为 5 次运行结果去掉最大/最小后的平均值；
- latency 在 30Hz publishing rate 下测量。

因此这组 live graph 数据应视为 **BENCH**，而不是 Demo。

## 5. Perceptor 的 workload 组成

Isaac Perceptor 官方说明：
- Visual SLAM：机器人定位 / Visual Odometry；
- ESS：learning-based stereo depth；
- Nvblox：局部 3D reconstruction / ESDF；
- Image Pipeline：GPU accelerated image processing。

来源：
https://nvidia-isaac-ros.github.io/v/release-3.2/reference_workflows/isaac_perceptor/tutorials_on_carter/demo_perceptor.html
https://nvidia-isaac-ros.github.io/v/release-3.1/reference_workflows/isaac_perceptor/technical_details.html

因此 Perceptor 3-camera graph 可映射为：
- W1 Sensor/Image Pipeline
- W2 Visual Odometry / SLAM
- W3 DNN Stereo Depth
- W4 3D Mapping / ESDF

## 6. 证据边界

这组数据仍然不能直接回答本项目六摄像头系统：
- Hawk 是 stereo module，官方表中的“3/4 Hawk”不能机械等同于 3/4 个单目 image stream；
- 不是与本项目 6 个独立 Camera 完全同构的 graph；
- W3 是 stereo depth，不是 YOLO object detection；
- 未在性能汇总表中给出系统功耗、CPU/GPU/DDR utilization；
- release-3.2 是历史固定软件版本，不能自动代表当前 release-5.x；
- NVIDIA release notes 还披露过高 CPU load 下 multi-cam frame drop 等已知限制，版本差异必须冻结。

所以可用于：
> **证明一体化 SoM 上“物理多 Camera + VSLAM + DNN depth + Mapping”的系统路径与公开吞吐量级。**

不可用于：
> **推出六摄像头 YOLO+SLAM 需要多少 TOPS，或宣称任何平台优于另一平台。**


## 7. 2026-09-30 补充：Isaac ROS 5.0 当前 Orin 时延锚点

Isaac ROS 5.0.0 已于 2026-09-21 发布，Jetson Orin / JetPack 7.2 仍在官方支持矩阵。

固定版本性能：
- Stereo Disparity Node 1080p：124 FPS，8.6ms @30Hz；
- Stereo Disparity Graph 1080p：117 FPS，9.3ms @30Hz；
- DNN Stereo Full 576p：66.5 FPS，17ms @30Hz；
- DetectNet 544p：73.5 FPS，15ms @30Hz；
- RT-DETR 720p：87.3 FPS，13ms @30Hz。

Nvblox AGX Orin core：
- TSDF：0.5–0.8ms（dataset dependent）；
- ESDF：1.5–1.7ms。

5.0 Visual SLAM / Nvblox Camera requirements：
- ≥30Hz target image rate；
- frame jitter ±2ms；
- stereo 内图像 offset ±100μs；
- 跨 stereo camera 图像 offset ±100μs。

详细见：
`references/benchmarks/isaac-ros-5.0-latency-anchors.md`

### 版本使用规则

release-3.2 与 5.0 不拼成一个“端到端总延迟”：
- 3.2 用来证明 Nova 物理多相机系统路径；
- 5.0 用来提供当前 Orin 固定版本 graph/component latency。
