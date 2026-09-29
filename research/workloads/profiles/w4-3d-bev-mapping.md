# W4 3D Perception / BEV / Mapping Workload Profile

- 状态：v0.1
- 日期：2026-09-30

## 两类基准

### A. MLPerf PointPainting
公开参数：
- Waymo Open Dataset
- 44M parameters
- 3T FLOPs
- FP32 reference mAP 54.25%
- Edge SingleStream

用于多传感器 3D perception 基线。

### B. BEVFormer
论文事实：
- multi-camera images
- unified BEV representation
- spatial cross-attention
- temporal self-attention
- nuScenes
- paper reports 56.9 NDS

用于 multi-camera spatiotemporal Transformer 研究基线。

## nuScenes 输入锚点

- 6 cameras，1600×900 @12Hz
- 1 LiDAR，20Hz，32 beams，最高约1.39M points/s
- 5 radar @13Hz
- GPS/IMU

## 指标

- mAP / NDS / task metric
- frame latency
- memory footprint
- DDR bandwidth
- GPU/NPU/CPU
- temporal cache
- camera-count scaling
- power

## 工程判断

3D/BEV 比单帧2D detection更容易暴露：
- memory bandwidth
- intermediate tensors
- cross-camera fusion
- temporal cache
- host/accelerator coordination

所以“YOLO很快”不等于适合 BEV/PointPainting/SLAM。

## References
- https://docs.mlcommons.org/inference/benchmarks/automotive/3d_object_detection/pointpainting/
- https://www.ecva.net/papers/eccv_2022/papers_ECCV/html/694_ECCV_2022_paper.php
- https://www.nuscenes.org/
