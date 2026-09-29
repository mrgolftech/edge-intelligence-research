# W1 Sensor I/O / Video Pipeline Workload Profile

- 状态：v0.1
- 日期：2026-09-30

## 目标

量化端侧系统在 AI 推理之前必须承担的数据入口和数据搬运负载。

## 公共传感器基线

### EuRoC MAV
- stereo grayscale，2×752×480 @20Hz
- IMU 200Hz
- camera/IMU hardware synchronized
- 8-bit grayscale pixel payload ≈ 14.44 MB/s

### TUM-VI
- stereo 1024×1024 @20Hz
- IMU 200Hz
- hardware synchronization
- 8-bit grayscale pixel payload ≈ 41.94 MB/s

### nuScenes
- 6 cameras，1600×900 ROI @12Hz
- 1×32-beam LiDAR @20Hz，最高约1.39M points/s
- 5 radar @13Hz
- GPS/IMU
- 按每像素1个8-bit channel计算，camera pixel payload ≈ 103.68 MB/s

注意：nuScenes 的 103.68 MB/s 只是统一算术基线，不代表实际图像编码格式或链路带宽。

## 公式

```text
PixelPayload = camera_count × width × height × fps × bytes_per_pixel
DDR ≈ Σ(buffer_size × read_write_passes × rate)
```

## Benchmark

测量：
- capture success / dropped frame
- timestamp jitter
- queue depth
- DDR bandwidth
- CPU%
- ISP/VPU utilization
- encode throughput
- board/system power

## 禁止推断

- PixelPayload ≠ MIPI lane bandwidth
- camera FPS ≠ AI inference FPS
- 不得假定 RGB24/YUV/RAW10，除非 sensor/driver 已确认
- 数据集传感器规格不是产品统一要求

## References
- https://projects.asl.ethz.ch/datasets/euroc-mav/
- https://cvg.cit.tum.de/data/datasets/visual-inertial-dataset
- https://www.nuscenes.org/
