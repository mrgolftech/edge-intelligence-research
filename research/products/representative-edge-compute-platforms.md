# 代表性端侧计算平台事实底座

- 日期：2026-09-30
- 状态：v0.4
- 目的：记录代表性平台的官方事实、产品形态和证据边界，不用于简单 TOPS 排名
- 适配分析：[`workload-platform-fit-matrix.md`](workload-platform-fit-matrix.md)
- 证据索引：[`platform-workload-evidence-2026.md`](../../references/webpages/platform-workload-evidence-2026.md)

## 1. 产品形态

本文件按形态分组：
1. 通用/AIoT SoC
2. 机器人/工业异构 SoC
3. GPU/Physical AI SoM
4. 车规智能驾驶 SoC
5. PCIe/M.2 独立 AI Accelerator
6. 边缘计算整机/组合方案

不同形态不可直接用峰值算力横排。

## 2. 代表产品

### Rockchip RK3588

**形态**：通用高端 AIoT SoC

**官方已确认**
- 4× Cortex-A76 + 4× Cortex-A55
- Mali-G610 MC4
- triple-core NPU，6 TOPS
- dual ISP、多路 MIPI CSI
- 8K H.265/H.264 video codec
- PCIe、SATA、双 GbE 等

**公开 Benchmark / 论文**
- Rockchip 官方 RKNN Model Zoo：RK3588 single-core NPU、INT8、640×640 下，YOLOv8n 73.5 FPS、YOLO11n 60.0 FPS；默认只统计 model inference。
- Sensors 2026 的 ROIV-SLAM 在 RK3588 上运行 RGB-D 30Hz + IMU 200Hz + 2D LiDAR 12Hz + wheel odometry 的融合 SLAM。

**证据边界**
单模型 DNN 与 SLAM 系统均已有证据，但“多路 camera + SLAM + DNN + planning”并发仍无高可信公开 benchmark。

来源：
- https://www.rock-chips.com/a/en/products/RK35_Series/2022/0926/1660.html
- https://github.com/airockchip/rknn_model_zoo
- https://doi.org/10.3390/s26134053

### Qualcomm Flight RB5 / Robotics RB5

**形态**：机器人/无人机 reference platform，QRB5165

**官方已确认**
- 15 TOPS AI Engine
- Kryo CPU + Adreno GPU + Hexagon Tensor Accelerator
- 7 路并发 Camera
- Spectra 480 ISP
- Linux/Ubuntu/ROS2
- 5G/Wi-Fi 6
- Flight RB5 官方明确列出 VIO、SLAM、DFS、object detection/tracking、stereo depth、path planning、obstacle avoidance

**工程意义**
这是目前公开资料中“无人机端一体化异构计算”的直接 reference-design 证据之一。

来源：
- https://www.qualcomm.com/internet-of-things/products/flight-rb5-platform
- https://www.qualcomm.com/content/dam/qcomm-martech/dm-assets/documents/qualcomm-robotics-rb5-platform-product-brief.pdf

### Qualcomm Dragonwing IQ-9075

**形态**：工业/机器人异构 SoC / EVK

**官方已确认**
- 50 / 100 dense INT8 TOPS
- 最高 36GB LPDDR5 inline ECC
- 最多 16 concurrent cameras
- 8-core Kryo + Adreno GPU + dual Hexagon Tensor Processor
- 4-core real-time MCU subsystem
- 2.5GbE TSN、CAN-FD、PCIe

**官方机器人软件证据**
- QRB ROS Camera：CSI/GMSL、多 stream、DMA-BUF zero-copy、ROS Jazzy。
- QRB ROS AMR Service：2D LiDAR SLAM、mapping/localization、Nav2 P2P、path following。
- QRB ROS Samples：YOLOv8 detection、segmentation、pose、depth、Follow Me、SLAM、Navigation2。

**公开 Partner Benchmark**
Innodisk iQ-Studio 使用 YOLOv10n INT8、640×640、1080p30 H.264：
- 1 stream：29.46 E2E FPS/channel
- 4 streams：29.47
- 9 streams：28.41
- 16 streams：15.90
- CPU 从 24.2% 上升到 99.8%

**工程意义**
多流边缘感知的真实边界会受到 CPU/解码/调度影响，不能由 100 TOPS 单独解释。

**证据边界**
16-stream benchmark 主要是 H.264 文件流，不是 16 路物理 CSI/GMSL camera；六摄像头同步、VIO/visual SLAM 与完整自主栈并发仍未验证。

来源：
- https://www.qualcomm.com/internet-of-things/products/iq9-series/iq-9075
- https://github.com/qualcomm-qrb-ros/qrb_ros_camera
- https://github.com/qualcomm-qrb-ros/qrb_ros_amr_service
- https://github.com/InnoIPA/iQ-Studio/tree/main/benchmarks/iqs-streampipe

### NVIDIA Jetson Orin

**形态**：GPU 异构 SoM / 开发平台

**官方已确认**
- AGX Orin 64GB：275 sparse INT8 TOPS
- 64GB LPDDR5，204.8 GB/s
- Arm CPU + Ampere GPU + Tensor Cores + NVDLA + PVA
- 最多 6 个物理 CSI cameras（16 virtual channels）
- 完整 JetPack / CUDA / TensorRT / Isaac ROS 软件栈

**公开案例/benchmark**
- Isaac ROS 提供 AGX Orin 的单节点/Graph benchmark；release-3.2 还提供 Nova Carter 物理多相机 Live Graph：4×1200p Multicam VSLAM 30.1 FPS、3×1200p Perceptor 中 Visual Odometry 30.0 FPS / Nvblox ESDF 9.45 FPS。
- Skydio X10 使用 Jetson Orin + 6 路导航相机，支持 GPS-denied navigation、obstacle avoidance、tracking 和机上 2D/3D mapping。
- 2024–2026 论文已有 Jetson AGX Orin / Orin Nano 上的 VINS、ORB-SLAM3 和 LLM 实测。

**工程意义**
当前公开证据最完整的“通用 GPU + AI + robotics stack”路线之一，尤其适合 W1–W7 的跨 workload 研究。

**证据边界**
Skydio 等整机案例没有公开每个模块的精确处理器分区；不能把整机功能都当成 Orin 单芯片性能。

来源：
- https://www.nvidia.com/content/dam/en-zz/Solutions/gtcf21/jetson-orin/nvidia-jetson-agx-orin-technical-brief.pdf
- https://nvidia-isaac-ros.github.io/performance/index.html
- https://www.skydio.com/x10

### NVIDIA Jetson Thor

**形态**：Physical AI / Robotics 高性能 SoM

**官方已确认**
- Blackwell GPU
- 最高 2070 sparse FP4 TFLOPS
- 128GB LPDDR5X
- 273 GB/s
- 40–130W
- MIG
- 面向 Agentic AI / Physical AI / Robotics / generative models

**工程意义**
更适合研究高端机器人 W7/VLA、复杂多模型和资源隔离，不应与十几瓦级 UAV 加速卡按单一算力指标直接比较。

来源：
- https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson/back-to-school/

### 地平线 Journey 6

**形态**：车规智能驾驶 SoC 系列

**官方已确认**
- 系列覆盖多个算力档位
- BPU + CPU + GPU + MCU
- 原生支持大参数 Transformer
- 支持端到端智能驾驶路线

**量产事实**
2026-09-03 地平线公开：截至 2026-08，Journey 6M 已落地 20+ 车企、70+ 量产上市车型；7 家品牌已实现城区辅助驾驶平台化上车。6M 为 128 TOPS。

**工程意义**
可作为 W1–W6 高并发车端 workload 的量产参考，但汽车的散热、供电、功能安全和传感器配置与 UAV 不同。

来源：
- https://www.horizon.auto/solutions/horizon-journey/horizon-journey6
- https://www.horizon.auto/news/product/473

### 黑芝麻智能华山 A2000

**形态**：车规智能驾驶 SoC

**官方已确认/厂商宣称**
- NPU 混合精度支持 INT8/FP8/FP16
- Transformer 硬件加速
- 三层内存架构
- 面向 BEV + Transformer、Multi-Modal LM、E2E
- Safety NPU

**证据边界**
本轮以产品架构事实为主，尚未得到可与公开 benchmark 直接对照的系统性能数据。

来源：
- https://www.blacksesame.com.cn/zh/huashan-a2000/

### Axelera Metis

**形态**：PCIe / M.2 独立 AI Accelerator

**官方已确认/公开 benchmark**
- Digital In-Memory Compute
- Voyager SDK
- 官方公开 YOLOv5/YOLOv8 等 FPS 和 end-to-end FPS
- benchmark 页面注明 host 条件，例如 Intel Core i9-13900K
- Voyager 文档明确 host 参与视频 decode 和 pre/post-processing

**真实案例**
DroneStar 搜救无人机使用 Metis M.2，在机上运行光学/热成像的 detection + tracking。

**工程意义**
证明 Host + Accelerator 可以用于 UAV。Axelera 2026 官方 ARM Host 页面还验证了 Firefly ITX-3588J、Orange Pi 5 Plus、NanoPC-T6（RK3588）、Raspberry Pi 5、Jetson Orin Nano/NX；因此 ARM Host 可行性已确认，但评估仍必须包含 host、PCIe、视频解码和总功耗。

来源：
- https://axelera.ai/metis-aipu-benchmarks
- https://axelera.ai/blog/how-dronestar-ai-scaled-one-operator-into-a-whole-pack
- https://docs.axelera.ai/sdk/

### Hailo-8 / Hailo-10H

**形态**：M.2 / Chip-on-board AI Accelerator

**Hailo-8 公开案例**
- Bluewhite 农业无人车：object detection、semantic segmentation、lane detection
- Astrial drone：Hailo-8 26 TOPS，实时 people counting / face detection
- Limelight 4 robot controller：视觉 AI 与 3D localization 系统案例

**Hailo-10H 官方已确认**
- 40 TOPS INT4 / 20 TOPS INT8
- 典型 2.5W
- 视觉 + Generative AI
- on-device LLM/VLM

**ARM Host / 多流 Reference**
Raspberry Pi 5 官方将 Hailo-8L/8/10H 集成到 AI HAT 与 camera stack；Hailo Apps 的 multisource pipeline 支持 USB/RTSP/file 多源并行 decode/scale 后送入 accelerator。官方对 RPi 的配置指导为 up to 3 sources optimal、15 FPS、默认 640×640；这是 REF，不是统一 Benchmark。

**工程意义**
Hailo-8 的现实证据集中在 W3；Hailo-10H 将路线扩展到 W7。两者都不应被视为完整机器人主控或安全飞控。

来源：
- https://hailo.ai/resources/industries/automotive/bluewhite-vehicle-agnostic-self-driving-robot-kit-for-agricultural-farms/
- https://hailo.ai/resources/industries/security/system-electronics-astrial-board-on-a-drone-platform/
- https://hailo.ai/hailo-files/hailo-10h-product-brief-en/

### 后摩智能 M50 / LQ50 M.2

**形态**：M.2 独立 AI Accelerator

**官方硬件事实**
LQ50-24GB：1×M50 / 2 IPU cores、160 TOPS INT8、100 TFLOPS@bFP16、24GB LPDDR5/LPDDR5X、153.6GB/s、PCIe Gen4×4、典型13W。

**官方 Model Zoo 证据**
后摩官方 `postmo-modelzoo` 中，MiniCPM-o 明确“部署到 M50”且“只适用于 xh2”；Qwen3 Pipeline 也以 M50 为 device 并使用 Xh2HalBackend。由此 xh2 至少明确包含 M50 target。

M50-compatible xh2 参考：
- YOLOv5s 640×640：Inference 6.668ms；E2E 9.715ms / P99 9.834ms；4-thread 410.350 qps；mAP50-95 0.355790。
- YOLO11m 640×640：Inference 17.069ms；E2E 19.917ms / P99 20.207ms；4-thread 199.962 qps；mAP50-95 0.489875。

**系统级证据**
BX50 = RK3588 host + M50，厂商称支持 32 路视频分析。

**证据边界**
YOLO 页未写具体 LQ50 SKU、M50 core frequency、板级功耗；BX50 也未公开 32 路视频的分辨率/FPS/模型。因此 M50 W3 可升级为 VENDOR_BENCH，但 LQ50+host 多流视频/PCIe/total power 仍需证据。

来源：
- https://developer.houmoai.com/hmdoc/m50/hardware-manuals/latest/product-manuals/lq50-m.2/LQ50_M.2_guidelines/intro/index.html
- https://github.com/houmo-ai/postmo-modelzoo
- https://www.houmoai.com/58/10/Product.html

## 3. 当前产业观察

### 事实 1：平台形态决定“还缺什么”
高集成 SoC/SoM 自带更多 CPU/ISP/VPU/I/O；独立 Accelerator 必须依赖 host。即使后者 TOPS 更高，也不能直接替代前者。

### 事实 2：真实系统是 workload 组合
Skydio X10、Flight RB5、Journey 6M 等都指向 W1–W6 的组合，而不是单一 DNN inference。

### 事实 3：独立加速器公开证据目前主要集中在 W3/W7
Metis/Hailo 已有真实视觉案例；M50 也已有官方 YOLO 模型级 benchmark，但独立 accelerator 的 W1/W2/W6/W9 仍取决于 host 和完整系统。

### 事实 4：大模型端侧化已经是产品事实，但不是所有无人平台的必需项
Jetson、IQ-9075、Hailo-10H、M50/A2000 都在公开支持 LLM/VLM/Multi-Modal/E2E，但是否投入 UAV 仍需按任务价值和 SWaP-C 判断。

## 4. 下一步

1. 将产品事实转成结构化 CSV/JSON；
2. 补各平台 model/input/precision/software/host/power 条件明确的 benchmark；
3. 优先补 RK3588、IQ-9075、LQ50 的机器人/视觉实测；
4. 对六摄像头 Case 分别验证“一体 SoC”和“Host + AI Accelerator”两条路线。
