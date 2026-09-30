# Isaac ROS 5.0 / Jetson Orin：当前时延与同步证据锚点

- 获取日期：2026-09-30
- 状态：verified-current-public-evidence
- 版本：Isaac ROS 5.0.0（2026-09-21）
- 平台：Jetson Orin / JetPack 7.2
- 目的：为六摄像头避障闭环的 W2/W3/W4 阶段提供**当前固定版本**的公开时延锚点。

## 1. 为什么从 latest URL 改成 release-5.0

Isaac ROS 5.0.0 于 2026-09-21 发布。

官方 Release Notes：
https://nvidia-isaac-ros.github.io/v/release-5.0/releases/index.html

5.0：
- ROS 2 Lyrical Luth；
- Ubuntu 24.04；
- Jetson Orin + JetPack 7.2 仍在官方支持矩阵；
- 消息/加速数据路径发生架构迁移，NITROS API 被 rosidl::Buffer/CUDA buffer backend 替代。

因此历史 benchmark 如果只写 `latest` URL，会随着页面更新失去可复现性。本项目从本轮开始优先记录 versioned URL。

## 2. Isaac ROS 5.0 AGX Orin 性能锚点

官方 Performance Summary：
https://nvidia-isaac-ros.github.io/v/release-5.0/performance/index.html

### W3 视觉/深度

| Graph/Node | Input | AGX Orin Throughput | 30Hz Latency |
|---|---:|---:|---:|
| Stereo Disparity Node | 1080p | 124 fps | 8.6 ms |
| Stereo Disparity Graph | 1080p | 117 fps | 9.3 ms |
| DNN Stereo Full | 576p | 66.5 fps | 17 ms |
| DNN Stereo Light | 288p | 75.5 fps | 24 ms |
| DetectNet Graph | 544p | 73.5 fps | 15 ms |
| RT-DETR SyntheticaDETR Graph | 720p | 87.3 fps | 13 ms |

官方方法：
- FPS 为 input node → accelerated pipeline → output node 的 observed throughput；
- 自动调输入速率，以 <5% frame loss 为目标；
- 5 次运行去掉最大/最小后平均；
- latency 是同一 benchmark 的**独立 30 Hz trial**，从 first sent frame 到 first received frame；
- 无有效 30Hz measurement 时官方不显示 latency。

### 边界

这些 latency：
- 是固定 graph/node 的 30Hz latency；
- 不是 P95/P99；
- 不是六路同时跑 detection/depth/VSLAM；
- 不能直接相加成系统闭环 latency。

## 3. W4 Nvblox 当前组件时延

官方 Nvblox 5.0：
https://nvidia-isaac-ros.github.io/v/release-5.0/repositories_and_packages/isaac_ros_nvblox/index.html

AGX Orin，voxel size 0.05 m：

| Dataset | Component | Timing |
|---|---|---:|
| Replica | TSDF | 0.8 ms |
| Replica | ESDF | 1.7 ms |
| Redwood | TSDF | 0.5 ms |
| Redwood | ESDF | 1.5 ms |

这些是 nvblox core component timing，不是完整：
`depth+pose → ROS graph → costmap → planner`
的端到端时延。

## 4. W2/W4 对 Camera 时序的明确要求

Isaac ROS 5.0 Visual SLAM / Nvblox 文档均给出 Camera system requirements：

- minimum target image framerate：**30 Hz**
- maximum permissible image-frame jitter：**±2 ms**
- stereo camera 内 image offset：**±100 μs**
- 跨 stereo camera image offset：**±100 μs**

来源：
https://nvidia-isaac-ros.github.io/v/release-5.0/repositories_and_packages/isaac_ros_visual_slam/index.html
https://nvidia-isaac-ros.github.io/v/release-5.0/repositories_and_packages/isaac_ros_nvblox/index.html

### 工程意义

这是非常有价值的“算法输入条件”证据：

> 对 VSLAM/多 Camera mapping，算力不是唯一门槛；Camera timing quality 本身就是明确的输入规范。

但必须注意：
- 这是 Isaac ROS 软件包要求；
- 不是整个 UAV 行业统一要求；
- 本项目最终同步指标仍需根据所选算法确认。

## 5. 与 release-3.2 Nova 数据的关系

仓库仍保留 release-3.2 Nova Carter：
- 物理多 Camera；
- hardware trigger / timestamp；
- Multicam VSLAM；
- Perceptor W1+W2+W3+W4 live graph throughput。

5.0 数据解决的是另一个问题：
> 当前 Jetson Orin 软件基线下，单个 graph/component 的 latency 量级是多少？

因此两个版本分工：
- **3.2 Nova：物理多相机系统 CASE/BENCH**
- **5.0：当前 Orin graph/component latency BENCH**

不能把不同版本的数值拼成一个单次完整 pipeline。
