# Benchmark Reference：EuRoC MAV / TUM-VI

- 获取日期：2026-09-30
- 用途：W1 Sensor I/O 与 W2 VIO/SLAM

## EuRoC MAV

ETH ASL官方数据：
- stereo WVGA monochrome，2×20 FPS
- IMU 200 Hz
- shutter-centric temporal alignment
- Vicon / Leica ground truth
- intrinsics / extrinsics

公开论文与复现配置给出相机 752×480。

来源：
- https://projects.asl.ethz.ch/datasets/euroc-mav/
- Burri et al., IJRR 2016, DOI 10.1177/0278364915620033

## TUM-VI

TUM官方：
- stereo 1024×1024 @20Hz
- IMU 200Hz
- hardware synchronized
- ground truth 120Hz at sequence start/end

来源：
https://cvg.cit.tum.de/data/datasets/visual-inertial-dataset

## 派生 Pixel Payload

8-bit grayscale：

EuRoC：
2×752×480×20 = 14,438,400 B/s ≈ 14.44 MB/s

TUM-VI：
2×1024×1024×20 = 41,943,040 B/s ≈ 41.94 MB/s

均不含链路、ISP、buffer与多次DDR读写。


## 数据格式补充

TUM VI 原论文的 sensor table 明确记录：
- 2× IDS uEye UI-3241LE-M-GL；
- 20 Hz；
- global shutter；
- 1024×1024；
- **16-bit gray**；
- IMU 200 Hz。

因此仓库早期的 `sensor-payload-baselines.csv` 中 1 byte/pixel 仅保留为统一的“8-bit normalized arithmetic sensitivity”，不能解释为 TUM VI 的真实采集格式。

六摄像头等效与不同 bpp 敏感性计算见：
`research/workloads/six-camera-reference-load-profiles.md`。
