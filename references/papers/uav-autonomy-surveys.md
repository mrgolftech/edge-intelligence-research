# UAV 自主系统综述索引

- 获取日期：2026-09-29
- 目的：建立无人机端侧需求的论文事实底座

## 1. Autonomous Object-Goal Navigation Review

论文：UAV control in autonomous object-goal navigation: a systematic literature review  
期刊：Artificial Intelligence Review

核心任务划分包括：
- Control
- Planning
- Localization
- Mapping
- Perception

文献指出感知、定位、建图和规划是自主 UAV navigation 的关键子任务，SLAM、视觉传感器、目标/障碍物识别均反复出现。

来源：
https://link.springer.com/article/10.1007/s10462-024-10758-7

## 2. UAV Localization Review

论文：From GPS to AI: A comprehensive review of Unmanned Aerial Vehicle (UAV) localization solutions  
期刊：ISPRS Journal of Photogrammetry and Remote Sensing, 2025

覆盖：
- GNSS
- radio
- vision
- inertial
- lidar
- magnetic/acoustic/ultrasonic
- deep learning

说明 UAV 定位是多模态、多传感器问题，不应被简化为视觉 NPU 需求。

来源：
https://www.sciencedirect.com/science/article/pii/S0924271625003727

## 3. GNSS-Denied Navigation Review

论文：State-of-the-art and future directions in autonomous navigation for UAVs in GNSS-denied environments

关注：
- SLAM
- VIO
- LIO
- 多模态融合
- SWaP
- 实时性
- 故障检测/恢复

这是本项目分析无人机端侧计算资源的重要方向。

## 4. Search and Rescue Application Review

论文：Unmanned aerial systems in search and rescue: A global perspective on current challenges and future applications  
2025

强调：
- sensor integration
- payload
- multi-UAV coordination
- AI
- digital twins

说明 UAV 任务需求还包括任务级协同和系统级资源，而非只有自主飞行。

## 5. UAV Payload/Application Review

2025 低空载荷综述列出的典型场景包括：
- crop monitoring / precision agriculture
- aerial transportation
- power line inspection
- emergency rescue
- logistics

来源：
https://www.frontiersin.org/journals/plant-science/articles/10.3389/fpls.2025.1721484/full

## 工程结论

UAV 端侧需求应至少覆盖：
- payload processing
- perception
- localization
- mapping
- planning/avoidance
- control support
- communications
- mission/task
- multi-UAV collaboration

不能以“六摄像头视觉”代表 UAV 全部应用。
