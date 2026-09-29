# 代表性端侧计算平台事实底座

- 日期：2026-09-30
- 状态：v0.2
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
- dual ISP，多路 MIPI CSI
- 8K H.265/H.264 video codec
- PCIe、SATA、双 GbE 等

**证据边界**
官方资料证明 W1/W3 的硬件基础，但本轮没有找到条件完整、可与 Orin/Metis 等同口径比较的自主导航系统 benchmark。W2/W4/W6 暂不从 6 TOPS 推断。

来源：
- https://www.rock-chips.com/a/en/products/RK35_Series/2022/0926/1660.html
- https://www.rock-chips.com/a/en/download/index.html

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

**形态**：新一代工业/机器人异构 SoC / EVK

**官方已确认**
- 100 dense TOPS variant
- 最高 36GB LPDDR5，inline ECC
- 最多 16 concurrent cameras
- 8-core Kryo CPU + GPU + NPU
- 4-core real-time MCU subsystem
- Ubuntu / Qualcomm Linux
- 官方面向 Robotics、AMR、Drones
- 官方称可运行 13B 模型；EVK 页面有约 12 tokens/s 示例

**工程意义**
与 RB5 相比，IQ-9075 更值得作为 2026 后续机器人/无人平台候选跟踪；它同时覆盖多摄像头、AI、较大内存和实时子系统。

**证据边界**
尚缺公开的 VIO/SLAM/ROS2 端到端机器人 benchmark。

来源：
- https://www.qualcomm.com/internet-of-things/products/iq9-series/iq-9075
- https://www.qualcomm.com/developer/hardware/qualcomm-iq-9075-evaluation-kit-evk

### NVIDIA Jetson Orin

**形态**：GPU 异构 SoM / 开发平台

**官方已确认**
- AGX Orin 64GB：275 sparse INT8 TOPS
- 64GB LPDDR5，204.8 GB/s
- Arm CPU + Ampere GPU + Tensor Cores + NVDLA + PVA
- 最多 6 个物理 CSI cameras（16 virtual channels）
- 完整 JetPack / CUDA / TensorRT / Isaac ROS 软件栈

**公开案例/benchmark**
- Isaac ROS 提供 AGX Orin 的 Stereo Disparity、DNN、视频编解码等 benchmark。
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
证明 Host + Accelerator 可以用于 UAV，但评估必须包含 host、PCIe、视频解码和总功耗。

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

**工程意义**
Hailo-8 的现实证据集中在 W3；Hailo-10H 将路线扩展到 W7。两者都不应被视为完整机器人主控或安全飞控。

来源：
- https://hailo.ai/resources/industries/automotive/bluewhite-vehicle-agnostic-self-driving-robot-kit-for-agricultural-farms/
- https://hailo.ai/resources/industries/security/system-electronics-astrial-board-on-a-drone-platform/
- https://hailo.ai/hailo-files/hailo-10h-product-brief-en/

### 后摩智能 M50 / LQ50 M.2

**形态**：M.2 独立 AI Accelerator

**官方已确认**
后摩开发者文档当前明确列出 LQ50-24GB：
- 1× M50，2 个 IPU 核
- 最高 160 TOPS
- 最高 100 TFLOPS @ bFP16
- 24GB LPDDR5/LPDDR5X
- 153.6 GB/s
- PCIe Gen4 ×4
- 22×80 mm
- 典型功耗 13W

M50 产品页还给出：
- INT8/INT16/FP16/FP32/bFP16/bFP24
- 最大 48GB LPDDR5
- 典型芯片功耗 10W

**厂商展示**
2025 WAIC 材料给出 7B/8B 模型 25+ tokens/s，并把 M50/LQ50 定位于端边大模型、机器人等场景。

**工程意义**
LQ50 已不能再只依据 Firefly 二手材料描述；官方资料已足够确认其硬件规格和 W7 路线。

**证据边界**
当前尚缺公开、条件完整的 W3 视觉 benchmark，以及无人机 W2/W3/W6 端到端案例。160 TOPS 不构成这些 workload 的适配证明。

来源：
- https://developer.houmoai.com/hmdoc/m50/hardware-manuals/latest/product-manuals/lq50-m.2/LQ50_M.2_guidelines/intro/index.html
- https://houmoai.com/60/ProductType.html
- https://www.houmoai.com/1/40/NewsDetails.html

## 3. 当前产业观察

### 事实 1：平台形态决定“还缺什么”
高集成 SoC/SoM 自带更多 CPU/ISP/VPU/I/O；独立 Accelerator 必须依赖 host。即使后者 TOPS 更高，也不能直接替代前者。

### 事实 2：真实系统是 workload 组合
Skydio X10、Flight RB5、Journey 6M 等都指向 W1–W6 的组合，而不是单一 DNN inference。

### 事实 3：独立加速器公开证据目前主要集中在 W3/W7
Metis/Hailo 已有真实视觉案例；LQ50 目前官方证据更偏大模型。W2/W6/W9 要看 host 和完整系统。

### 事实 4：大模型端侧化已经是产品事实，但不是所有无人平台的必需项
Jetson、IQ-9075、Hailo-10H、M50/A2000 都在公开支持 LLM/VLM/Multi-Modal/E2E，但是否投入 UAV 仍需按任务价值和 SWaP-C 判断。

## 4. 下一步

1. 将产品事实转成结构化 CSV/JSON；
2. 补各平台 model/input/precision/software/host/power 条件明确的 benchmark；
3. 优先补 RK3588、IQ-9075、LQ50 的机器人/视觉实测；
4. 对六摄像头 Case 分别验证“一体 SoC”和“Host + AI Accelerator”两条路线。
