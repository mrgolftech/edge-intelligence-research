# 六摄像头 UAV Requirement Reference Anchors（2026-09）

- 日期：2026-09-30
- 性质：公开事实锚点，不是本项目产品需求
- 目的：为 Phase 2 Requirement Profile 提供可追溯的 Reference / Benchmark / Stress 依据
- 规则：任何外部系统参数都不得直接写入 Project Nominal，除非产品设计明确采用同一条件

## 1. Camera / VIO 频率锚点

### nuScenes — 原生六摄像头感知
- 6 cameras；
- Camera 约 12 Hz；
- 官方说明降低到约 12 Hz 的目的之一是降低 perception compute / bandwidth / storage load。
来源：
- https://www.nuscenes.org/
- https://forum.nuscenes.org/t/clarification-on-timestamps-and-capture-frequency-of-sweeps/481

### EuRoC MAV
- stereo WVGA monochrome；
- 2×20 FPS；
- IMU 200 Hz；
- shutter-centric temporal alignment。
来源：
https://projects.asl.ethz.ch/datasets/euroc-mav/

### TUM VI
- stereo 1024×1024 @20 Hz；
- IMU 200 Hz；
- Camera / IMU hardware synchronized。
来源：
https://cvg.cit.tum.de/data/datasets/visual-inertial-dataset

### NVIDIA Hawk / Isaac ROS
- stereo；
- two synchronized 1920×1200 global-shutter imagers；
- ROS streams 1920×1200 @30 fps。
来源：
https://nvidia-isaac-ros.github.io/getting_started/sensors/hawk_setup.html

这些数据只作为 Reference Anchor，不定义项目 FPS。

## 2. Multi-Camera Perception Topology

nuScenes 提供原生 6-camera 360°视图；BEVFormer 是典型的 fused multi-camera perception：
- 单个 perception model 联合消费多个 camera views；
- 通过 spatial cross-attention 融合多摄像头信息；
- 输出统一 BEV representation。

来源：
https://arxiv.org/abs/2203.17270

因此“6 Camera 进入感知”不等于“每个周期运行 6 次独立 detector”。

必须区分：
1. PER_VIEW；
2. FUSED_MULTI_VIEW；
3. MIXED。

## 3. Detection Benchmark 输入锚点

公开平台资料中 640×640 INT8 YOLO-family 很常见：
- RK3588 官方 RKNN Model Zoo：YOLOv8n / YOLOv10n / YOLO11n 等；
- IQ-9075 Partner Benchmark：YOLOv10n INT8 640×640；
- M50-compatible xh2：YOLOv5s / YOLO11m 640×640。

用途：
- 640×640 INT8 可作为未来统一 W3 Benchmark 的候选起点；
- 现有公开结果 model variant 不一致，不能直接横向排名。

未来定量比较必须使用 exact same model + input + precision。

## 4. Multi-Camera VSLAM / Depth Anchor

Nova Carter / Isaac ROS release-3.2 公开：
- 4 Hawk stereo modules Multicam Visual SLAM：30.1 FPS；
- 3 Hawk stereo modules DNN Stereo：Full 30.2 FPS、Light 15.2 FPS；
- 3 Hawk Perceptor：Visual Odometry 30.0 FPS、Nvblox ESDF 9.45 FPS。

来源：
https://nvidia-isaac-ros.github.io/v/release-3.2/performance/index.html

边界：
- Hawk 是 stereo module，不等于 monocular stream；
- 不是六摄 UAV exact workload；
- release-3.2 是历史固定版本。

## 5. Flight Speed / Avoidance Anchors

### PX4 Collision Prevention
当前文档：
- initial companion test：4 m/s；
- OBSTACLE_DISTANCE：10 Hz；
- external vision sensor delay 可到约 0.2 s；
- vehicle tracking delay 典型约 0.1–0.5 s；
- CP_DIST 为车辆/项目配置量，需要为机体/桨叶保留安全余量。
来源：
https://docs.px4.io/main/en/computer_vision/collision_prevention

### EGO-Planner
真实飞行：
- cluttered indoor：3.56 m/s。
官方配置锚点：
- depth_filter_maxdist = 5.0 m；
- local_update_range_x/y = 5.5 m；
- local_update_range_z = 4.5 m。
来源：
https://zhepeiwang.github.io/pubs/ral_2021_egoplan.pdf
https://github.com/ZJU-FAST-Lab/ego-planner

### FOAM
- outdoor real-time quadcopter：4.5 m/s。
来源：
https://arxiv.org/abs/2109.09159

### FASTER
- unknown cluttered real hardware：up to 7.8 m/s。
来源：
https://arxiv.org/abs/2001.04420

解释：
- 3.56 / 4.0 / 4.5 m/s 可形成真实系统参考簇；
- 7.8 m/s 可作为高动态 stress anchor；
- 不是行业速度等级。

## 6. 不存在可直接迁移的数值

### Keep-out distance
PX4 CP_DIST 是 user/vehicle-specific configuration，没有一个可跨无人机复用的固定值。
R17 必须由机体几何、桨叶包络、感知/定位误差、控制裕量和安全策略决定。

### Compute power / mass / volume
候选平台规格不能反向定义 UAV 产品允许的 W/g/mm³。
R19/R20/R21 必须由产品/任务定义。

## 7. 证据使用规则

每个 Requirement 的数值只能属于：
- PROJECT_CONFIRMED
- REFERENCE_ANCHOR
- BENCHMARK_BASELINE
- STRESS_ANCHOR

严禁把后三类静默提升为 Project Nominal。
