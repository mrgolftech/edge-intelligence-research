# PX4：Computer Vision / VIO 资料摘要

- 来源类型：官方开发文档
- 机构：PX4 / Dronecode
- 获取日期：2026-09-29
- 可信度：高
- 用途：证明无人机视觉计算覆盖光流、视觉定位、VIO 与碰撞预防等任务

## 原始资料

1. Computer Vision (Optical Flow, MoCap, VIO, Avoidance)  
   https://docs.px4.io/main/en/advanced/computer_vision

2. Visual Inertial Odometry (VIO)  
   https://docs.px4.io/main/en/computer_vision/visual_inertial_odometry

## 关键内容

PX4 官方文档将计算机视觉用于：

- Optical Flow：二维速度估计；
- Motion Capture：外部视觉三维位姿；
- VIO：融合视觉与 IMU，估计三维位姿和速度；
- Collision Prevention：碰撞预防。

VIO 文档指出，VIO 常用于 GNSS 不存在或不可靠的环境；示例架构使用相机、IMU、Companion Computer 和 ROS，将视觉里程计信息提供给 PX4。

## 支撑的项目结论

**已确认事实**

1. 无人机端侧视觉任务不只有目标检测，还包括定位/速度估计和避障。
2. VIO 需要视觉与 IMU 融合。
3. Companion Computer 是承载这类高级视觉计算的一种典型系统架构。

**工程推断**

因此，评估无人机端侧计算平台时，需要同时关注 CPU/GPU、传感器同步、ROS/中间件和系统延迟，不能只看 NPU TOPS。

## 限制

PX4 文档证明任务链路存在，但不能直接给出特定无人机所需 TOPS 或具体硬件规格；实际资源需求仍需由传感器和算法负载推导。
