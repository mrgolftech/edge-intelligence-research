# W2 State Estimation / VIO / SLAM Workload Profile

- 状态：v0.1
- 日期：2026-09-30

## 基准算法

第一版采用 **ORB-SLAM3** 作为公开 SLAM/VIO common baseline。

已确认：
- open-source
- real-time Visual / Visual-Inertial / Multi-Map SLAM
- monocular / stereo / RGB-D
- 官方提供 EuRoC、TUM-VI 示例

该选择只用于复现和平台比较，不代表“最佳算法”。

## 输入

### EuRoC stereo-inertial
- 2×752×480 @20Hz
- IMU 200Hz

### TUM-VI stereo-inertial
- 2×1024×1024 @20Hz
- IMU 200Hz

## 指标

算法：
- ATE
- RPE
- tracking failure / relocalization

实时：
- processing latency
- estimator update rate
- P95/P99
- frame age

资源：
- CPU/core distribution
- GPU（若使用）
- memory
- DDR
- power
- temperature

## 并发测试

先测 ORB-SLAM3 单独运行，再逐步叠加：
- camera encode
- DNN perception
- depth
- network transmission

观察 ATE/RPE、丢帧、latency 和 CPU/DDR 竞争。

## 边界

NPU TOPS 不能直接代表 ORB-SLAM3 性能，因为 pipeline 含 feature、matching、optimization、loop closure 等非纯 DNN 操作。

## References
- https://doi.org/10.1109/TRO.2021.3075644
- https://github.com/UZ-SLAMLab/ORB_SLAM3
- https://projects.asl.ethz.ch/datasets/euroc-mav/
- https://cvg.cit.tum.de/data/datasets/visual-inertial-dataset
