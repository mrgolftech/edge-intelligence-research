# 端侧自主系统定量工作负载基线

- 状态：v0.1
- 日期：2026-09-30
- 目的：为 W1–W8 建立可复现、可量化、可跨平台复测的第一版 workload baseline
- 原则：优先采用公开数据集、同行评审论文、官方开源实现和行业 benchmark；没有统一基准时明确标注

## 1. 基准选择原则

1. **真实输入**：优先采用公开机器人/自动驾驶数据集中的真实传感器组合。
2. **可复现**：优先选择有官方代码、数据集和评测指标的算法。
3. **可移植**：benchmark 不绑定某一家芯片 SDK。
4. **分层**：先测单 workload，再测并发 workload。
5. **不把 benchmark 采样率当作行业门槛**：公开数据集的 20 Hz / 10 Hz 只是测试输入条件。
6. **不从 FLOPs/TOPS 直接推系统能力**：必须同时测 latency、throughput、CPU/GPU/NPU、DDR、功耗和温度。

## 2. 第一版基准总表

| Workload | 第一版公共基线 | 已确认的量化输入 | 主要输出指标 | 当前状态 |
|---|---|---|---|---|
| W1 Sensor/Video | EuRoC、TUM-VI、nuScenes sensor profiles | camera count/resolution/rate、IMU rate、LiDAR point rate | payload、drop、jitter、DDR、VPU/ISP | 已定义 |
| W2 Localization/SLAM | ORB-SLAM3 + EuRoC/TUM-VI | stereo 20 Hz、IMU 200 Hz | ATE/RPE、实时率、CPU/GPU、功耗 | 已定义 |
| W3 DNN Perception | MLPerf Inference v6.1 YOLOv11 Edge | COCO safe subset；Offline/SingleStream/MultiStream | latency、throughput、accuracy、power | 已定义 |
| W4 3D/BEV | MLPerf PointPainting + BEVFormer/nuScenes | PointPainting 44M/3T FLOPs；nuScenes 6-camera suite | 3D mAP/NDS、latency、memory、DDR | 已定义 |
| W5 Prediction | Waymo Open Motion Dataset | 103,354×20s@10Hz；1s history + 8s future windows | minADE/minFDE/MR/mAP、latency | 已定义为算法/实时回放基线 |
| W6 Planning | Nav2 MPPI | example: 30Hz, 2000 batches, 56 points；官方测得100+Hz on 4th-gen i5 | cycle time、WCET、CPU、success | 已定义 |
| W7 VLM/VLA | OpenVLA + LIBERO/LIBERO-Plus | OpenVLA 7B；建议控制数据约5–10Hz；LIBERO 130 tasks | task success、action latency、memory、power | 已定义 |
| W8 Multi-Agent | MRTA/Multi-Robot survey-derived scaling profile | robots N、tasks M、update rate、network | allocation latency、task throughput、network、scaling | 尚无统一硬件 benchmark，定义参数化实验 |

## 3. 关键量化锚点

### W1 / W2 真实传感器输入

EuRoC：
- stereo monochrome 2×20 FPS
- 752×480（论文/公开复现配置）
- IMU 200 Hz
- 8-bit grayscale 有效像素 payload ≈ **14.44 MB/s**

TUM-VI：
- stereo 1024×1024 @ 20 Hz
- IMU 200 Hz
- 8-bit grayscale 有效像素 payload ≈ **41.94 MB/s**

nuScenes：
- 6 cameras，1600×900 ROI，12 Hz
- 1 LiDAR，20 Hz，最高约 1.39M points/s
- 5 radars，13 Hz
- 仅按每像素 **1 个 8-bit channel** 计算，6-camera pixel payload ≈ **103.68 MB/s**

这些都是有效像素/公开 sensor profile，不代表 MIPI、SerDes 或 DDR 实际总带宽。

### W3 标准化 Edge Detection

截至 2026-09，MLPerf Inference v6.1 已将 **YOLO v11** 纳入 Edge category，支持 Offline、SingleStream、MultiStream 场景。

### W4 3D/BEV

MLPerf PointPainting：
- Waymo dataset
- 44M parameters
- 3T FLOPs
- Edge 3D Object Detection benchmark

BEVFormer：
- multi-camera
- spatial cross-attention
- temporal self-attention
- nuScenes benchmark

### W6 Planning

Nav2 MPPI 当前文档：
- example controller_frequency = 30 Hz
- batch_size = 2000
- time_steps = 56
- 官方称 modest 4th-gen Intel i5 可达到 100+ Hz

这是 CPU/优化 workload 事实基线，不是所有机器人频率要求。

### W7 VLA

OpenVLA：
- 7B parameters
- 970k robot episodes
- 官方代码建议控制数据约 5–10Hz，且未采用 action chunking

仅按 7B 参数裸权重：
- FP16 ≈ 14.0 GB
- INT8 ≈ 7.0 GB
- INT4 ≈ 3.5 GB

这些只表示 raw-weight 下限，不包含 runtime、activation、vision encoder、cache 等。

## 4. Benchmark 执行顺序

### Phase A：单负载
W1 → W2 → W3 → W4 → W6 → W7

### Phase B：典型并发
- W1 + W3
- W1 + W2 + W3
- W2 + W4 + W6
- W1 + W3 + W7
- W1 + W2 + W3 + W6

### Phase C：稳态
Phase B 增加 30 / 60 / 120 min 持续测试，记录温度、频率、功耗与性能退化。

## 5. 统一采集指标

性能：
- throughput
- average latency
- P50 / P95 / P99
- deadline miss
- dropped input

资源：
- CPU%
- GPU%
- NPU%
- DDR bandwidth
- memory footprint
- storage/network bandwidth

工程：
- board/system power
- temperature
- throttling
- software version
- precision
- power/clock mode

## References

- [EuRoC / TUM-VI](../../references/benchmarks/euroc-tumvi.md)
- [MLPerf Edge](../../references/benchmarks/mlperf-edge.md)
- [nuScenes / Waymo](../../references/benchmarks/nuscenes-waymo.md)
- [Nav2 MPPI](../../references/benchmarks/nav2-mppi.md)
- [OpenVLA / LIBERO](../../references/benchmarks/vla-libero.md)
- [BEVFormer](../../references/papers/bevformer.md)
