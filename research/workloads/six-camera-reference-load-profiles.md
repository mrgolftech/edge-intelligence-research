# 六摄像头参考工作负载档位：从公开系统到可计算 W1 基线

- 状态：v0.1
- 日期：2026-09-30
- 数据：`data/calculations/six-camera-reference-profiles.csv`
- 脚本：`scripts/calc_six_camera_reference_profiles.py`
- 目的：在本项目六摄像头实际分辨率/FPS/像素格式尚未冻结时，用公开数据集和真实机器人系统建立**参考负载档位**，而不是凭空指定产品需求。

## 1. 规则

本文件严格区分三类量：

1. **公开事实**：来源明确给出的分辨率、帧率、Camera 数量/类型、同步机制；
2. **算术缩放**：把公开的单/双 Camera 配置换算成 6 路等效 pixel rate；
3. **敏感性分析**：对 8/10/12/16/24 bpp 表示计算 payload。

只有第 1 类是外部系统事实。第 2、3 类是本项目计算，不代表行业标准，也不代表六摄像头产品最终需求。

## 2. 四类事实锚点

### R1 — EuRoC MAV：低分辨率 VIO/MAV 锚点

ETH 官方：
- stereo WVGA monochrome；
- 2×20 FPS；
- IMU 200 Hz；
- shutter-centric temporal alignment。

来源：
https://projects.asl.ethz.ch/datasets/euroc-mav/

使用公开论文常用的 752×480 分辨率进行计算。

六路等效：
- 6 × 752 × 480 × 20
- **43.315 MP/s**

这个档位适合回答：
> 如果相机主要服务于 VIO/SLAM，而不是高清目标识别，W1 的像素吞吐可以处于什么数量级？

它不是六摄像头 UAV 行业门槛。

### R2 — TUM VI：高分辨率 VIO 锚点

TUM 官方：
- stereo grayscale 1024×1024 @20 Hz；
- IMU 200 Hz；
- Camera/IMU hardware synchronization。

来源：
https://cvg.cit.tum.de/data/datasets/visual-inertial-dataset

六路等效：
- **125.829 MP/s**
- 若以 16-bit grayscale representation 计算，单次完整帧表示约 **251.66 MB/s**

这里的“六路”是算术扩展，不是 TUM 系统本身有六路 Camera。

### R3 — nuScenes：原生六摄像头感知锚点

nuScenes 官方 devkit：
- 6 cameras；
- 图像 sample metadata：1600×900；
- 官方 data-collection 说明 Camera 运行约 12 Hz；
- 12 Hz 本身就是为了降低 compute / bandwidth / storage load。

来源：
https://www.nuscenes.org/tutorials/nuscenes_tutorial.html
https://forum.nuscenes.org/t/clarification-on-timestamps-and-capture-frequency-of-sweeps/481

原生六路 pixel rate：
- **103.680 MP/s**

如果仅做“一份 RGB888 frame representation”的算术：
- **311.04 MB/s**

注意：这不是 nuScenes 车载链路实际 RAW/MIPI 带宽，也不是 DDR 总带宽；只是把有效像素展开成 RGB888 后的一次完整图像表示。

### R4/R5 — NVIDIA Hawk：高分辨率机器人多相机锚点

NVIDIA 当前 Isaac ROS Hawk setup：
- Hawk 是 **stereo camera module**；
- 每个模块包含两个同步 global-shutter 1920×1200 imager；
- setup 页面当前发布 left/right raw stream 为 1920×1200 @30 FPS。

Nova platform 文档还给出 Hawk 1920×1200 @60 FPS 的 sensor capability。

来源：
https://nvidia-isaac-ros.github.io/getting_started/sensors/hawk_setup.html
https://nvidia-isaac-ros.github.io/nova/getting_started/platforms/adapting_nova.html

若只把“单个 image stream”按六路等效计算：

| 档位 | 六路 Pixel Rate | RGB888 一次完整表示 |
|---|---:|---:|
| 1920×1200 @30 | 414.720 MP/s | 1244.16 MB/s |
| 1920×1200 @60 | 829.440 MP/s | 2488.32 MB/s |

**重要：这不是 6 个 Hawk 模块。**

1 个 Hawk = 2 个同步 imager。因此这里仅借用“单 image stream 的 resolution/FPS”做六路算术敏感性分析。

## 3. 数据量为什么不能直接等于 MIPI / DDR 带宽

CSV 中的 payload 只计算：

`N × W × H × FPS × bpp`

它不包含：
- blanking；
- MIPI packet/ECC/CRC；
- sensor packing；
- ISP internal format；
- stride/alignment；
- Camera buffer queue；
- GPU/NPU intermediate tensor；
- read-modify-write；
- video encoder；
- ROS2 / application copy。

因此必须分别建模：

`Sensor payload ≠ link bandwidth ≠ memory traffic ≠ AI tensor traffic`

## 4. 一个非常关键的 DDR 解释方法

如果某工作点的“完整帧表示”是 X MB/s，那么：

- ISP 写一次内存：约增加 1×X 的完整帧流量；
- resize/color-convert 读+写：可能再增加约 2×X；
- CPU/GPU/NPU 再完整读取：每次又增加约 1×X；
- 编码器、显示、录像等还会继续增加。

这不是说实际系统一定有 N 次 full-frame copy，而是提示：

> **数据路径设计和 zero-copy 能把系统带宽需求拉开数倍。**

例如六路 1920×1200@30：
- RGB888 一份 frame representation = **1.244 GB/s**
- 如果软件路径额外发生 4 次完整图像等价读写，单纯 image-plane traffic 就可能多出约 **4.98 GB/s**

这还没有计算模型 activation、SLAM map、codec 和 OS。

所以“内存带宽够不够”不能只拿 sensor pixel rate 与 LPDDR 峰值带宽比较。

## 5. W3 推理调用率：先算 inference/s，不先算 TOPS

如果每个 Camera 都独立跑一次检测：

`InferenceRate_total = CameraCount_for_DNN × PerCameraInferenceHz`

可用公开系统频率做**测试点**而不是需求：

| DNN Camera 数 | 12 Hz | 20 Hz | 30 Hz |
|---:|---:|---:|---:|
| 2 | 24 inf/s | 40 inf/s | 60 inf/s |
| 4 | 48 inf/s | 80 inf/s | 120 inf/s |
| 6 | 72 inf/s | 120 inf/s | 180 inf/s |

频率来源的意义：
- 12 Hz：nuScenes 六 Camera acquisition 量级；
- 20 Hz：EuRoC/TUM-VI VIO Camera 量级；
- 30 Hz：Nova/Isaac ROS 多 Camera live graph 常见实时量级。

这些不是“检测必须达到 12/20/30 Hz”的规范。

真正的平台判断应回答：
- 72/120/180 inf/s 能否持续？
- P95/P99 latency 是否满足？
- Camera frame 是否排队？
- Host preprocessing 是否先饱和？
- VIO/SLAM 同时运行后下降多少？

## 6. W2 与 W3 不应默认处理同样的 Camera 集合

公开系统已经说明这一点：

- EuRoC/TUM-VI 的 VIO 是 stereo；
- Nova Perceptor 使用 stereo/depth/VSLAM graph；
- nuScenes 六 Camera 面向环视感知；
- 本项目目前并没有证据要求“六路 Camera 全部同时进入 VIO/SLAM”。

因此后续参数必须拆开：

- `N_capture`：物理采集 Camera 数；
- `N_detection`：进入 DNN 的 Camera 数；
- `N_vio`：进入 VIO/SLAM 的 Camera 数；
- `N_depth`：进入 depth/stereo 的 Camera 数；
- `N_record`：需要编码/录像的 Camera 数。

这比一个统一“6 路都跑 AI”的假设更接近真实系统。

## 7. 当前对六摄像头 Case 的工程判断

在实际参数未冻结前，目前只能得出以下可靠判断：

1. **W1 的合理研究区间至少跨一个数量级。** 六路等效公开参考从约 43 MP/s 到 829 MP/s；
2. 相同 Camera 数量下，resolution/FPS 比“Camera 数=6”本身更决定吞吐；
3. ISP/VPU、zero-copy 和 DDR data path 是一等变量；
4. W2 与 W3 的有效 Camera 数必须分别定义；
5. 只有在 W1、DNN inference rate、VIO input、deadline 冻结后，才有资格进入平台资源需求和算力推导。

## 8. 下一步冻结顺序

由于当前无法实测，建议按“先事实、后需求”的顺序继续：

1. 从实际硬件资料确认 Camera sensor / active mode；
2. 确认实际输出 width/height/FPS/pixel format；
3. 明确 6 路是否都需要持续采集；
4. 定义 `N_detection / N_vio / N_depth / N_record`；
5. 用任务速度/障碍距离推导 deadline，而不是直接指定检测 FPS；
6. 再将该 workload 分别映射到：
   - RK3588 一体 SoC；
   - Jetson Orin；
   - Qualcomm IQ-9075；
   - RK3588 + Metis/Hailo/M50。

这一步完成之前，继续拒绝用 TOPS 直接给方案下结论。
