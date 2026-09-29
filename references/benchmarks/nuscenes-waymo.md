# Benchmark Reference：nuScenes / Waymo Open Dataset

- 获取日期：2026-09-30
- 用途：W4 3D/BEV、W5 Prediction

## nuScenes

官方：
- 1000 scenes ×20s
- 6 cameras
- 1 LiDAR
- 5 radar
- GPS/IMU
- ~1.4M camera images
- ~390k lidar sweeps

传感器参数：
- cameras: 1600×900 ROI @12Hz
- LiDAR: 32 beams @20Hz，up to ~1.39M points/s
- radar: 5× @13Hz

6路相机每像素1个8-bit channel：
6×1600×900×12 = 103,680,000 B/s ≈ 103.68 MB/s

该值不是实际链路/DDR带宽。

来源：
https://www.nuscenes.org/
https://www.nuscenes.org/nuscenes

## Waymo Open Dataset

### Motion Dataset
- 103,354 segments
- 20s @10Hz
- >20M frames
- 574 hours
- 10.8M tracked objects
- 9s windows：1s history + 8s future

Motion paper metrics：
- minADE
- minFDE
- Miss Rate
- Overlap Rate
- mAP

2025 Interaction Prediction：
- primary: Soft-mAP
- tie-break: minADE

来源：
https://waymo.com/open/about/
https://waymo.com/open/data/motion/
