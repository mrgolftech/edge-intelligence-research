# 平台—工作负载适配证据索引（2026-09）

- 状态：v0.5
- 日期：2026-09-30
- 目的：为“workload → compute resource → platform”适配矩阵提供可追溯事实依据
- 原则：本文件只记录公开证据及其能支撑的结论，不把厂商定位、峰值算力或系统案例自动外推为所有 workload 的实测能力

## 1. 证据标签

- **CASE**：已公开的命名产品、量产项目或实际系统案例
- **BENCH**：公开 benchmark / 实测，且有明确模型、输入或平台条件
- **PARTNER_BENCH**：合作伙伴实测，测试条件较明确，但不是芯片厂商独立复测
- **REF**：官方 reference design / 官方明确给出的应用路径
- **SPEC**：官方 Datasheet / Product Brief / Developer Guide 明确能力
- **PAPER**：论文中的平台实测
- **INFER**：由已确认架构事实推导的工程判断，尚未被上述证据直接验证
- **GAP**：当前未找到足够公开证据

这些标签描述“证据类型”，不是产品评分。

## 2. NVIDIA Jetson Orin

### E01 — Jetson AGX Orin Technical Brief
- 类型：SPEC
- 来源：NVIDIA
- URL：https://www.nvidia.com/content/dam/en-zz/Solutions/gtcf21/jetson-orin/nvidia-jetson-agx-orin-technical-brief.pdf
- 已确认：
  - AGX Orin 64GB：275 sparse INT8 TOPS
  - 64GB LPDDR5，204.8 GB/s
  - 12-core Cortex-A78AE
  - Ampere GPU + Tensor Cores + 2×NVDLA + PVA
  - 最多 6 路物理 CSI camera（16 virtual channels）
  - H.265 编码最高可到 16×1080p30
- 支撑：W1、多任务异构并发的硬件基础。
- 限制：峰值 TOPS 不能直接代表 W2/W4/W6 等系统 workload 性能。

### E02 — Isaac ROS Performance Summary
- 类型：BENCH
- 来源：NVIDIA Isaac ROS
- URL：https://nvidia-isaac-ros.github.io/performance/index.html
- 访问日期：2026-09-30
- 已确认的 AGX Orin 示例：
  - 1080p Stereo Disparity：124 FPS，8.6 ms @30Hz 条件
  - 720p AprilTag：189 FPS，5.3 ms @30Hz
  - 1080p H.264 encode：公开 I/P frame benchmark
  - 同一软件栈包含 cuVSLAM、Nvblox、occupancy/localization、DNN inference 等包
- 支撑：W1/W3；并为 W2/W4 提供官方软件实现路径。
- 限制：单节点 benchmark 不能替代完整机器人并发性能。

### E03 — Skydio X10
- 类型：CASE
- 来源：Skydio 官方
- URL：https://www.skydio.com/x10
- URL：https://support.skydio.com/hc/en-us/articles/18919821734683-Skydio-X10-Frequently-Asked-Questions
- 已确认：
  - 机载 NVIDIA Jetson Orin
  - 6 路 32MP navigation cameras，360°视觉
  - GPS-denied / high-EMI 环境自主飞行
  - obstacle avoidance、tracking、自动任务
  - 可在机上构建 2D map / 3D model
- 支撑：真实 UAV 场景中的 W1/W2/W3/W4/W5/W6 组合负载存在性。
- 限制：Skydio 未公开每个模块在 Jetson/飞控/其他处理器之间的精确任务划分，因此不能把系统功能全部等价为“Orin 单芯片 benchmark”。

### E04 — Jetson-ORB-SLAM3
- 类型：PAPER
- 来源：arXiv，2026-08
- URL：https://arxiv.org/abs/2608.17874
- 已确认：
  - Jetson Orin Nano
  - ORB-SLAM3 GPU front-end + CPU mapping/optimization
  - EuRoC monocular-inertial mean 32 FPS
  - 7W 平台条件下 CNN loop closure 可与 tracking 并行
- 支撑：W2 在低功耗 Orin 平台上的 CPU/GPU 协同路线。
- 限制：预印本；不能代替本项目实测。

### E05 — NeRF-VINS
- 类型：PAPER
- 来源：IEEE ICRA 2024
- URL：https://ieeexplore.ieee.org/document/10610051/
- 已确认：NeRF-aided VINS 在 Jetson AGX Orin 上达到 15 Hz 实时定位。
- 支撑：W2/W4 高级定位/地图表达的嵌入式实现证据。

### E06 — Edge LLM on Jetson AGX Orin
- 类型：PAPER
- 来源：arXiv 2025
- URL：https://arxiv.org/abs/2506.09554
- 已确认：在 AGX Orin 64GB 上测试 2.7B–32.8B LLM 的量化、序列长度、功耗与吞吐。
- 支撑：W7 可在高内存 Jetson 上进行端侧 LLM 研究。
- 限制：LLM benchmark 不等于 VLA 闭环实时性能。

## 3. Qualcomm

### E07 — Qualcomm Flight RB5 5G Platform
- 类型：REF + SPEC
- 来源：Qualcomm 官方
- URL：https://www.qualcomm.com/internet-of-things/products/flight-rb5-platform
- 已确认：
  - 15 TOPS AI Engine
  - 7-camera concurrency
  - Spectra 480 ISP
  - 官方明确列出 VIO、SLAM、DFS、computer vision
  - 官方应用说明包含 multi-object detection/tracking、stereo depth cues、path planning、obstacle avoidance
  - Wi-Fi 6 / 5G，官方提及 drone-to-drone / swarm
- 支撑：UAV W1/W2/W3/W5/W6/W8 的 reference-design 证据。
- 限制：官方 reference design，不等于独立第三方 benchmark；安全飞控 W9 的执行边界未公开。

### E08 — Dragonwing IQ-9075
- 类型：SPEC
- 来源：Qualcomm 官方
- URL：https://www.qualcomm.com/internet-of-things/products/iq9-series/iq-9075
- URL：https://www.qualcomm.com/developer/hardware/qualcomm-iq-9075-evaluation-kit-evk
- 已确认：
  - 100 dense TOPS variant
  - 最高 36GB LPDDR5，inline ECC
  - 最多 16 concurrent cameras
  - CPU + GPU + NPU + 4-core real-time MCU subsystem
  - Ubuntu / Qualcomm Linux
  - 官方产品页给出 Llama 2 7B up to 22 tokens/s，并称平台可运行 13B 参数模型
  - 目标应用明确包含 Robotics、AMR、Drones
- 支撑：W1/W3/W7/W9 的结构性能力；后续 E27–E31 已补官方 ROS2 Reference 与多流 partner benchmark。
- 限制：W2/W6 已有官方功能路径，但 VIO/SLAM/navigation 的定量 latency/CPU/power 仍缺公开统一 benchmark。

## 4. 地平线 Journey 6

### E09 — Journey 6 产品页
- 类型：SPEC
- 来源：地平线官方
- URL：https://www.horizon.auto/solutions/horizon-journey/horizon-journey6
- 已确认：
  - 系列覆盖 10+ / 80 / 128 / 560 TOPS 等档位
  - BPU + CPU + GPU + MCU
  - 原生支持大参数 Transformer
  - 面向端到端与高阶辅助驾驶
- 支撑：W3/W4/W5/W6 的车端异构计算路线。

### E10 — Journey 6M 量产上车
- 类型：CASE
- 来源：地平线官方，2026-09-03
- URL：https://www.horizon.auto/news/product/473
- 已确认：
  - 截至 2026-08，Journey 6M 已落地 20+ 车企、70+ 量产上市车型
  - 7 家品牌实现城区辅助驾驶平台化上车
  - 6M 为 128 TOPS，支持一段式端到端城区辅助驾驶
- 支撑：车端 W1–W6 组合 workload 的量产系统级证据。
- 限制：公开材料没有披露 perception/prediction/planning 等模块在芯片各计算单元上的具体负载分配。

## 5. 黑芝麻智能 A2000

### E11 — 华山 A2000
- 类型：SPEC
- 来源：黑芝麻智能官方
- URL：https://www.blacksesame.com.cn/zh/huashan-a2000/
- 已确认：
  - NPU 支持 INT8/FP8/FP16 等混合精度
  - 针对 Transformer 做硬件加速
  - 三层内存架构强调高带宽与 DDR 利用率
  - 官方面向 BEV + Transformer、Multi-Modal LM、E2E
  - Safety NPU
- 支撑：W3/W4/W6/W7 与安全相关异构架构方向。
- 限制：本轮尚未获得 A2000 与公开标准 workload 对应的系统 benchmark；因此暂不与量产 Journey 6M 或 Isaac ROS 实测直接横向比较。

## 6. Axelera AI Metis

### E12 — Metis AIPU Benchmarks
- 类型：BENCH
- 来源：Axelera AI 官方
- URL：https://axelera.ai/metis-aipu-benchmarks
- 已确认示例：
  - YOLOv5m 640×640：456 inference-only FPS
  - YOLOv8s 640×640：610 inference-only FPS
  - 页面同时给出 end-to-end FPS
  - 测试注明 host 为 Intel Core i9-13900K
- 支撑：W3 视觉推理。
- 限制：结果依赖强 host；不能直接代表低功耗 ARM host 或无人机整机性能。

### E13 — DroneStar AI
- 类型：CASE
- 来源：Axelera AI 官方客户案例
- URL：https://axelera.ai/blog/how-dronestar-ai-scaled-one-operator-into-a-whole-pack
- 已确认：
  - 无人机搭载 Metis M.2
  - 机上实时 object detection + tracking
  - 光学/热成像输入
  - 面向搜索救援，多机由一名操作员监督
- 支撑：W3/W5 在 UAV 上的实际系统案例；也说明独立加速器可以进入严格 SWaP 场景。
- 限制：路线规划与飞行控制虽存在于系统，但公开材料没有证明由 Metis AIPU 承担。

### E14 — Voyager SDK pipeline / host acceleration
- 类型：SPEC
- 来源：Axelera AI 官方文档
- URL：https://docs.axelera.ai/sdk/
- URL：https://docs.axelera.ai/sdk/user-guides/hw-acceleration/
- 已确认：
  - Metis 为 PCIe/M.2 accelerator
  - 视频 decode、pre/post-processing 可依赖 host 的 VA-API/OpenCL
  - SDK 公开 System FPS / Host FPS / CPU usage 等端到端指标
- 支撑：独立 NPU 必须把 W1、host CPU/GPU 和 PCIe 数据搬运纳入系统评估。

## 7. Hailo

### E15 — Bluewhite autonomous farming robot
- 类型：CASE
- 来源：Hailo 官方客户故事
- URL：https://hailo.ai/resources/industries/automotive/bluewhite-vehicle-agnostic-self-driving-robot-kit-for-agricultural-farms/
- 已确认：
  - 农业装备改装为全自动车辆
  - Hailo 处理 object detection、semantic segmentation、lane detection 等视觉任务
  - 强调实时响应与低功耗
- 支撑：W3 在真实自主移动设备中的案例。
- 限制：planning/control 由系统其他计算资源承担的边界未完全公开。

### E16 — Hailo-8 Astrial drone
- 类型：CASE / DEMO
- 来源：Hailo 官方
- URL：https://hailo.ai/resources/industries/security/system-electronics-astrial-board-on-a-drone-platform/
- 已确认：
  - Drone + Astrial board + Hailo-8 26 TOPS
  - real-time people counting / face detection
- 支撑：UAV W3 低功耗视觉推理。
- 限制：这是视觉 demo，不是完整自主导航 benchmark。

### E17 — Hailo-10H
- 类型：SPEC
- 来源：Hailo 官方 Product Brief
- URL：https://hailo.ai/hailo-files/hailo-10h-product-brief-en/
- 已确认：
  - 40 TOPS INT4 / 20 TOPS INT8
  - 典型 2.5W
  - 视觉 + generative AI，面向 on-device LLM/VLM
- 支撑：W7 的低功耗独立加速路线。
- 限制：LLM/VLM 功能不能外推为 W2/W6/W9 能力。

## 8. 后摩智能 M50 / LQ50

### E18 — LQ50 M.2 用户指南
- 类型：SPEC
- 来源：后摩智能官方开发文档
- URL：https://developer.houmoai.com/hmdoc/m50/hardware-manuals/latest/product-manuals/lq50-m.2/LQ50_M.2_guidelines/intro/index.html
- 访问日期：2026-09-30
- 已确认（LQ50-24GB 型号）：
  - 160 TOPS
  - 100 TFLOPS @ bFP16
  - 24GB LPDDR5/LPDDR5X
  - 153.6 GB/s
  - PCIe Gen4 ×4
  - 22×80 mm
  - 典型 13W
- 支撑：独立端侧大模型/AI accelerator 的硬件基础。
- 限制：它是 M.2 accelerator，不包含 UAV 的 camera ISP、SLAM CPU、飞控等完整系统资源。

### E19 — M50 官方发布与应用
- 类型：SPEC / vendor benchmark
- 来源：后摩智能
- URL：https://www.houmoai.com/1/35/NewsDetails.html
- URL：https://www.houmoai.com/1/40/NewsDetails.html
- 已确认/厂商宣称：
  - M50 面向端边大模型推理
  - 7B/8B 模型约 25+ tokens/s（厂商展示数据）
  - 应用方向包括 PC、智能语音、机器人、端边推理
- 支撑：W7。
- 限制：当前没有找到与 MLPerf Edge / Isaac ROS / EuRoC 同口径的公开 W2/W3/W4/W6 benchmark。

## 9. Rockchip RK3588

### E20 — RK3588 官方产品页 / Brief Datasheet
- 类型：SPEC
- 来源：Rockchip
- URL：https://www.rock-chips.com/a/en/products/RK35_Series/2022/0926/1660.html
- URL：https://www.rock-chips.com/a/en/download/index.html
- 已确认：
  - 4× Cortex-A76 + 4× Cortex-A55
  - Mali-G610 MC4
  - 6 TOPS triple-core NPU
  - dual ISP、multiple MIPI CSI-2
  - 8K H.265/H.264 encoder / decoder
  - PCIe / SATA / dual GbE 等
- 支撑：W1/W3 的一体化 SoC 硬件基础。
- 限制：本轮尚未找到高可信、条件完整、可与 Orin/Metis 等直接比较的 RK3588 自主导航系统 benchmark，因此 W2/W4/W6 只保留工程验证入口，不给出“已适配”结论。

## 10. 2026-09-30 增补证据

### E21 — 华山 A2000 家族 2026 最新官方披露
- 类型：SPEC + DEMO
- 来源：黑芝麻智能官方，2026 WNEVC / WAIC
- URL：https://www.blacksesame.com/zh/list_11/1010.html
- URL：https://www.blacksesame.com/zh/list_8/994.html
- 已确认/厂商公开：
  - A2000N/A2000L/A2000U/A2000X 家族覆盖约 200–1000 TOPS；
  - 全链路支持 INT4/INT8/FP8/FP16/FP32；
  - 官方称片上专用高速缓存带宽达到 8TB/s；
  - 星眸 ISP 支持 4 曝光、150dB HDR、3DNR、RAW 直通 NPU；
  - 官方明确面向 VLA 与世界模型；
  - WAIC 2026 展示 Qwen VLM 在 A2000 平台端侧实时交互。
- 支撑：W3/W4/W7 与车规/物理 AI 平台演进方向。
- 限制：
  - 1000 TOPS 是家族最高规格，不能套用到全部 SKU；
  - “实时交互”是厂商演示，不是公开可复现 benchmark；
  - 不能直接外推到 UAV 的 SWaP-C 和软件生态。

### E22 — Hailo-10H GenAI / Vision 厂商 Benchmark
- 类型：BENCH（厂商）
- 来源：Hailo 官方，2025-07-22
- URL：https://hailo.ai/company-overview/newsroom/news/hailo-announces-general-availability-of-hailo-10h-edge-ai-accelerator-with-generative-ai-capabilities/
- 已确认/厂商公开：
  - 多种 2B 语言模型和 VLM：first-token latency < 1s，>10 tokens/s；
  - YOLOv11m 可处理 real-time 4K video stream；
  - 产品典型功耗 2.5W。
- 支撑：W3/W7 的低功耗 accelerator 路线。
- 限制：
  - 未完整披露模型 revision、量化、上下文和精确 FPS；
  - 2.5W 为产品典型功耗，不能当作每条 benchmark 的独立实测功耗；
  - 不能据此推断 W2/W6/W9。

### E23 — RKNN Model Zoo / RK3588 官方模型性能
- 类型：BENCH
- 来源：Rockchip 官方 GitHub（airockchip/rknn_model_zoo）
- URL：https://github.com/airockchip/rknn_model_zoo
- 访问日期：2026-09-30
- 已确认：
  - 性能表明确标注 RK3588 为 `@single_core`；
  - YOLOv8n，INT8，输入 [1,3,640,640]：73.5 FPS；
  - YOLOv8s：38.0 FPS；YOLOv8m：16.2 FPS；
  - YOLO11n：60.0 FPS；YOLO11s：33.0 FPS；YOLO11m：12.7 FPS；
  - 数据按各平台最大 NPU 频率采集；
  - 默认只统计 model inference，不含未特别注明的 pre/post-processing。
- 支撑：RK3588 的 W3 DNN perception 已有官方可量化 benchmark，不再仅停留在 6 TOPS 规格层。
- 限制：
  - 单 NPU 核、单模型 inference-only；
  - 不能代表六摄像头并发、视频 decode/ISP、CPU post-process、SLAM 同时运行时的端到端性能；
  - toolkit/runtime/模型导出方式会影响实际结果，复现时必须冻结版本和频率。

### E24 — ROIV-SLAM on RK3588
- 类型：PAPER
- 来源：Sensors 2026, 26(13), 4053，同行评审
- DOI：https://doi.org/10.3390/s26134053
- URL：https://www.mdpi.com/1424-8220/26/13/4053
- 已确认：
  - 感知计算单元采用 RK3588 embedded platform；
  - RGB-D：30 Hz，RGB 1920×1080、Depth 640×480；
  - IMU：200 Hz；
  - 2D LiDAR：12 Hz，20,000 points/s；
  - 系统执行视觉、LiDAR、IMU、wheel odometry 融合，包含前端估计、factor-graph back-end 与 loop closure；
  - 论文报告真实机器人实验与建图/轨迹比较。
- 支撑：RK3588 上 W2 Localization/SLAM 与 W4 Mapping 的真实论文系统证据。
- 限制：
  - 不是 ORB-SLAM3；
  - 未给出可直接用于平台横比的 CPU/GPU/NPU 占用、每帧 latency、DDR、功耗；
  - 不能说明与 YOLO、多路摄像头并发后的性能边界。

### E25 — IQ-9075 + acontis EC-Master 实时控制 Benchmark
- 类型：PARTNER_BENCH
- 来源：acontis partner benchmark，发布于 Qualcomm Partner Network，2026-06-22
- URL：https://www.qualcomm.com/support/partner/blog/acontis-iq9
- 已确认：
  - EC-Master 运行在 Dragonwing IQ-9075；
  - Linux CLOCK_MONOTONIC real-time scheduling；
  - target cycle time 1 ms；
  - 完整 EtherCAT frame processing，包括 send/receive/application workload；
  - acontis 标准测试台：7 slaves，512-byte process data；
  - 连续稳定 round-trip 约 100 μs；
  - jitter 为个位数微秒，文章标题明确称 under 8 μs；
  - 文中给出 ROS 2 integration 路径。
- 支撑：IQ-9075 的 W9 deterministic control / real-time communication 有实际量化证据，不再只是“存在 4-core MCU”的规格推断。
- 限制：
  - 合作伙伴 Benchmark，不等于 Qualcomm 独立 Benchmark；
  - EtherCAT timing 不等于整机飞控 WCET/安全认证；
  - 没有同时公布 AI+EtherCAT 满负载下的完整资源占用。

### E26 — M50/BX50 多路视频分析系统路线
- 类型：SPEC（系统级厂商资料）
- 来源：后摩智能官方
- URL：https://www.houmoai.com/1/35/NewsDetails.html
- URL：https://www.houmoai.com/58/10/Product.html
- 已确认/厂商宣称：
  - 后摩发布资料称 BX50 计算盒子支持 32 路视频分析与本地大模型；
  - BX50 采用 RK3588 CPU/GPU host + 1×M50 NPU；
  - BX50 官方页面列出 Ubuntu 20.04、整机典型功耗 ≤25W；
  - M50 为 160 TOPS INT8 / 100 TFLOPS bFP16，PCIe Gen4 x4。
- 支撑：M50 可以进入“Host + accelerator”的多路视频分析系统，不应再把其产业定位仅理解为 LLM。
- 限制：
  - 没有公开 32 路视频的 codec、分辨率、FPS、模型、精度、检测 FPS/latency；
  - 这是 BX50 整机资料，不能直接等价为任意 LQ50 + 任意 host 的 W3 性能；
  - 因此 LQ50 直接 W3 benchmark 仍然是 GAP。

### E27 — QRB ROS Camera on IQ-9075
- 类型：REF
- 来源：Qualcomm 官方 GitHub
- URL：https://github.com/qualcomm-qrb-ros/qrb_ros_camera
- 已确认：
  - Supported target 明确为 Dragonwing IQ-9075 EVK；
  - 支持 CSI 与 GMSL camera、concurrent multiple streams；
  - 支持 ROS 2 composable node；
  - qrb_ros_transport 通过 Linux DMA-BUF 提供 zero-copy image transport；
  - 默认示例为 1920×1080@30，并演示第二路 1080×720@60 stream。
- 支撑：IQ-9075 W1 的 ROS2 camera pipeline、zero-copy 与多 stream 官方实现路径。
- 限制：示例参数不是平台最大 camera throughput benchmark，也没有证明 6/16 个物理 camera 的同步采集稳定性。

### E28 — QRB ROS AMR Service on IQ-9075
- 类型：REF
- 来源：Qualcomm 官方 GitHub
- URL：https://github.com/qualcomm-qrb-ros/qrb_ros_amr_service
- 已确认：
  - Supported target 明确为 Dragonwing IQ-9075 EVK；
  - P2P navigation、path following、mapping service；
  - 2D LiDAR SLAM 提供 mapping/localization；
  - Nav2 提供 P2P navigation；
  - ROS Jazzy / Qualcomm Ubuntu 路径公开。
- 支撑：IQ-9075 W2 与 W6 从“架构推断”升级为官方机器人 Reference。
- 限制：没有公开 ATE/RPE、SLAM Hz、planner latency、CPU/NPU/DDR、功耗；2D LiDAR SLAM/Nav2 不等价于 UAV VIO。

### E29 — Innodisk iQS-Streampipe / IQ-9075 多流视觉
- 类型：PARTNER_BENCH
- 来源：Innodisk 官方 GitHub iQ-Studio
- URL：https://github.com/InnoIPA/iQ-Studio/tree/main/benchmarks/iqs-streampipe
- 测试条件：
  - EXMP-Q911（IQ-9075）；8 CPU cores，Normal power plan；
  - NPU + TFLite / QNN 2.32；
  - YOLOv10n INT8，2.3M parameters，640×640；
  - 1080p@30 H.264；1 / 4 / 9 / 16 channels；
  - warm-up 180s，measurement 300s。
- 公开结果（average E2E FPS/channel）：
  - 1 stream：29.46 FPS，CPU 24.2%；
  - 4 streams：29.47 FPS，CPU 51.0%；
  - 9 streams：28.41 FPS，CPU 93.6%；
  - 16 streams：15.90 FPS，CPU 99.8%。
- 支撑：IQ-9075 的 W1(video pipeline)+W3(DNN) 多流并发有公开可复现实测。
- 工程观察：9→16 streams 时 CPU 接近饱和，per-channel FPS 显著下降，说明系统瓶颈不能只看 NPU TOPS。
- 限制：是 H.264 文件流，不是 16 路物理 CSI/GMSL camera；不测试多 camera 时间同步，也不包含 SLAM/Nav2 并发。

### E30 — Innodisk InnoPPE 10-stream / IQ-9075 EVK
- 类型：PARTNER_BENCH
- 来源：Innodisk 官方 GitHub iQ-Studio
- URL：https://github.com/InnoIPA/iQ-Studio/blob/main/benchmarks/innoppe/README.md
- 测试条件：IQ-9075 EVK，YOLOv10n INT8/QNN，10×1080p@30，1 路 UVC MJPEG + 9 路本地 H.264。
- 结果图：25.0 FPS（UVC channel）、CPU 99.6%、memory 14.6%、accelerator 67.2%。
- 支撑：比纯文件流更接近真实 sensor+video+AI pipeline。
- 限制：只有 1 路 live camera；FPS 只测 UVC channel；硬件表中的 20W 不能直接当成严格墙上功耗实测。

### E31 — QRB ROS Samples / IQ-9075
- 类型：REF
- 来源：Qualcomm 官方 GitHub
- URL：https://github.com/qualcomm-qrb-ros/qrb_ros_samples
- 已确认：IQ-9075 EVK 可运行 YOLOv8 detection、segmentation、pose、depth estimation；Robotics samples 包含 2D LiDAR SLAM、Navigation2、Follow Me（detect/track/follow）。
- 支撑：W2/W3/W4/W5/W6 的官方软件 Reference。
- 限制：sample 支持矩阵不是性能 benchmark，simulation sample 不能当作物理机器人实测。

### E32 — 后摩官方 Model Zoo：M50/xh2 与 YOLO
- 类型：VENDOR_BENCH
- 来源：后摩智能官方 GitHub `houmo-ai/postmo-modelzoo`
- URL：https://github.com/houmo-ai/postmo-modelzoo
- 已确认 M50 ↔ xh2 证据链：
  - MiniCPM-o 示例明确写“部署到后摩 M50 芯片设备上”，并同时写“本例只适用于 xh2”；
  - Qwen3 Pipeline 参数明确写 `ndevice` 为 M50 device 数，运行日志使用 `Xh2HalBackend`。
- YOLOv5s xh2：
  - input 640×640，COCO2017 val 5000，build ncore=1；
  - xh2 mAP50-95 0.355790；
  - inference avg 6.668 ms；E2E avg 9.715 ms，P99 9.834 ms；
  - 4-thread throughput 410.350 qps。
- YOLO11m xh2：
  - input 640×640，COCO2017 val 5000，ncore=1；
  - xh2 mAP50-95 0.489875；
  - inference avg 17.069 ms；E2E avg 19.917 ms，P99 20.207 ms；
  - 4-thread throughput 199.962 qps。
- 支撑：M50 W3 已有官方模型级定量证据。
- 限制：YOLO README 没有写具体 LQ50 SKU、M50 core frequency、板级功耗；throughput 是多线程测试；不能外推 LQ50+host 的 PCIe/video/multi-camera 端到端性能。

### E33 — RK3588 RKNN 多核/并发实现路径
- 类型：REF
- 来源：Rockchip 官方 RKNPU2 / RKNN-Toolkit2
- URL：https://github.com/airockchip/rknpu2/blob/master/runtime/RK3588/Linux/librknn_api/include/rknn_api.h
- URL：https://github.com/airockchip/rknn-toolkit2/blob/master/rknpu2/examples/rknn_benchmark/README.md
- 已确认：
  - RKNN API 提供 `rknn_dup_context`；
  - `rknn_set_core_mask` 可选择 RK3588 的 NPU core 0/1/2 或组合；
  - 官方 `rknn_benchmark` 接受 core_mask，可测试 1/2/3 核组合。
- 支撑：RK3588 W3 多 context / 多 NPU core 调度具有官方软件路径。
- 限制：
  - API/工具支持不是多路视频或多模型并发性能 Benchmark；
  - 不允许按 3 个 NPU core 线性推算 3× throughput；
  - 官方 Model Zoo 明确要求匹配最新 RKNPU SDK，否则 performance/results 可能错误，版本必须冻结。
- 风险信号：
  - 社区 issue 存在旧 SDK 下多线程隔离与多核 scaling 的问题报告；
  - 这些不是官方确认的当前缺陷，只用于定义后续验证项。

## 11. 关键结论

1. **有完整自主系统案例的平台，不代表每个 workload 都在同一处理器上执行。** Skydio X10、Journey 6M 等只能证明系统级组合成立，必须保留任务分区未知这一限制。
2. **独立 AI 加速器的证据目前最集中在 W3 和 W7。** Metis/Hailo 有视觉案例/benchmark；M50 现已有官方 xh2 模型级 YOLO benchmark，BX50 有系统级多路视频路线；但 LQ50 板级 + host 的多流端到端性能仍缺公开实测。
3. **公开 benchmark 必须记录 host。** Metis 官方 YOLO benchmark 使用 i9-13900K；若换成 RK3588/ARM host，端到端性能必须重新测试。
4. **六摄像头无人平台不能直接从任何一条产品案例抄结论。** Skydio X10 可作为六物理相机系统案例锚点；IQ-9075 的 16-stream partner benchmark 可作为视频+AI并发锚点，但其输入是文件流而非 16 路物理 camera。RK3588 虽有三核 NPU 官方调度 API，也不能把单模型 FPS 按核心数线性放大。
