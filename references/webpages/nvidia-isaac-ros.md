# NVIDIA Isaac ROS 资料摘要

- 来源类型：官方开发者文档
- 机构：NVIDIA
- 获取日期：2026-09-29
- 可信度：高
- 用途：机器人端侧异构计算任务链路参考

## 原始资料

1. NVIDIA Isaac ROS  
   https://developer.nvidia.com/isaac/ros

2. Isaac ROS Visual SLAM / cuVSLAM  
   https://nvidia-isaac-ros.github.io/repositories_and_packages/isaac_ros_visual_slam/index.html

## 关键内容

Isaac ROS 面向 ROS 2 机器人计算，官方列出的能力包括：

- AI perception / inference
- localization and mapping
- Visual SLAM
- 3D scene reconstruction
- stereo depth
- pose estimation/tracking
- motion planning

官方资料说明 NITROS 用于优化 ROS 2 数据通路和 GPU 加速处理。

Visual SLAM 文档还记录了多摄像头与 RGB-D 等支持能力。

截至获取日期，Visual SLAM 页面更新记录显示：

- 2024-05-30：加入 multi-cam VIO；
- 2024-12-10：加入 multi-cam SLAM mode；
- 2026-02-02：加入 RGBD cameras 支持；
- 2026-09-21：文档记录 `isaac_ros_visual_slam` 包更名为 `isaac_ros_cuvslam`。

## 支撑的项目结论

**已确认事实**

现代机器人端侧软件栈往往同时覆盖感知、定位、建图、深度和规划，而不是单独运行一个神经网络。

**工程推断**

因此高性能端侧平台需要评估完整 pipeline 的并发性能和数据搬运效率，单一模型 FPS 或峰值 TOPS 不足以代表系统性能。

## 限制

Isaac ROS 是 NVIDIA 生态，不能直接代表其他硬件平台；官方 Benchmark 也需要结合具体 Jetson 型号、软件版本、传感器和功耗模式理解。
