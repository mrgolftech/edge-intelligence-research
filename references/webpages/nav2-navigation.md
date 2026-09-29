# ROS 2 Nav2 自主导航资料摘要

- 来源类型：官方项目文档
- 项目：Navigation2 (Nav2)
- 获取日期：2026-09-29
- 可信度：高
- 用途：拆解自主导航计算链路

## 原始资料

1. Nav2 Documentation  
   https://docs.nav2.org/

2. Navigation Concepts  
   https://docs.nav2.org/rolling/getting_started/navigation_concepts/

3. Navigation Plugins  
   https://docs.nav2.org/rolling/configuration_and_development/navigation_plugins/

4. Behavior Trees  
   https://docs.nav2.org/rolling/getting_started/navigation_concepts/behavior_trees/

## 关键内容

Nav2 的自主导航体系包含：

- State Estimation
- Environmental Representation / Costmap
- Planning
- Control
- Behaviors
- Behavior Trees

插件体系包括：

- costmap layer
- planner
- controller
- behavior
- navigator

Behavior Tree 用于组织多步骤导航任务、规划、跟踪、恢复等行为。

## 支撑的项目结论

**已确认事实**

自主导航不是单一模型，而是定位、地图表示、规划、控制和行为编排共同构成的系统。

**工程推断**

端侧计算平台如果要支持 L3 自主导航，应同时评估 CPU、通用 GPU、内存、ROS2、实时数据链路和系统稳定性；NPU TOPS 只是其中一个指标。

## 限制

Nav2 主要面向移动机器人。无人机的控制动力学、飞控闭环和三维规划不同，但其“状态估计—地图—规划—控制”的系统分解方法具有参考价值。
