# 代表性端侧计算平台事实底座

- 日期：2026-09-29
- 状态：v0.1
- 目的：证明当前产业的产品形态与工作负载正在分化，不用于简单 TOPS 排名

## 1. 产品形态

本文件故意把产品按形态分组，而不是按 TOPS 排序：

1. 通用/AIoT SoC
2. 机器人专用异构平台
3. GPU/Physical AI 模组
4. 车规智能驾驶 SoC
5. 独立 AI 加速器
6. 边缘计算整机/组合方案

不同形态不可直接以峰值算力比较。

## 2. 代表产品

### Rockchip RK3588

**形态**：通用高端 AIoT SoC

**官方已确认**
- 4× Cortex-A76 + 4× Cortex-A55
- Mali-G610 MP4 GPU
- 6 TOPS NPU
- 强视频编解码能力
- MIPI CSI、PCIe、双 GMAC 等接口
- 目标应用含 AI Camera、Edge Computing、NVR 等

**工程意义**
适合用来研究“CPU/GPU/NPU + ISP/VPU + 丰富 I/O”的低功耗一体化路线。其价值不能只用 6 TOPS 描述。

来源：
- Rockchip RK3588 Brief Datasheet
- Rockchip 官方产品/开发板资料

### Qualcomm Robotics RB5

**形态**：机器人/无人机开发平台，QRB5165

**官方已确认**
- 15 TOPS AI Engine
- 8-core Kryo CPU + GPU + Hexagon Tensor Accelerator
- 支持 7 路并发 Camera
- 集成 ISP/CV 能力
- 支持 Linux/Ubuntu/ROS2
- 可扩展 4G/5G
- 官方定位 consumer / enterprise / industrial robots and drones

**工程意义**
体现机器人平台需要同时解决 AI、Camera、连接、传感器和 ROS，而不只是 NPU。

来源：
https://www.qualcomm.com/content/dam/qcomm-martech/dm-assets/documents/qualcomm-robotics-rb5-platform-product-brief.pdf

### NVIDIA Jetson Orin

**形态**：GPU 异构 SoM / 开发平台

**官方已确认**
- Orin 系列覆盖不同性能档位
- AGX Orin 64GB：最高 275 sparse INT8 TOPS
- 最高 64GB LPDDR5
- 204.8 GB/s 内存带宽
- Arm CPU + Ampere GPU + Tensor Cores + NVDLA + PVA
- 官方面向 robotics / autonomous machines / multi-sensor fusion / 3D perception

**工程意义**
适合研究通用 GPU 与 AI 加速器协同，对 VIO/SLAM、CUDA算法、多模型并发和复杂机器人软件栈更有代表性。

来源：
https://www.nvidia.com/en-us/lp/embedded-computing/robotics-edge-ai-tech-brief/

### NVIDIA Jetson Thor

**形态**：Physical AI / Robotics 高性能 SoM

**官方已确认**
- Blackwell GPU
- 最高 2070 sparse FP4 TFLOPS
- 128GB LPDDR5X
- 273 GB/s
- 40–130W
- MIG 支持资源隔离
- 官方定位 Agentic AI / Physical AI / Robotics / generative models

**工程意义**
表明机器人端计算需求正在从传统 INT8 CV 模型扩展到大模型、VLM/VLA 和混合关键度任务。其 FP4 TFLOPS 也进一步说明不能跨产品只比较“TOPS”。

来源：
https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-thor/

### 地平线征程 6

**形态**：车规智能驾驶 SoC 系列

**官方已确认/厂商宣称**
- 系列算力覆盖约 10+～560 TOPS
- 集成 BPU、CPU、GPU、MCU
- 原生支持大参数 Transformer
- 产品覆盖不同辅助驾驶/全场景智能驾驶需求

**工程意义**
体现汽车端的“系列化工作负载覆盖”和高度集成路线，适合研究 BEV/Transformer/E2E 等车端负载。

来源：
https://www.horizon.auto/solutions/horizon-journey/horizon-journey6

### 黑芝麻智能华山 A2000

**形态**：车规智能驾驶 SoC

**官方已确认/厂商宣称**
- 集成 CPU、DSP、GPU、NPU、MCU、ISP、CV 等单元
- 支持 INT4/INT8/INT16、FP8/FP16 等精度
- 面向 BEV + Transformer、Multi-Modal LM、E2E
- 多芯片可扩展

**工程意义**
体现高阶智驾计算已经从 CNN 感知转向 Transformer、多模态和 E2E，并强调内存/数据闭环和异构计算。

来源：
https://www.blacksesame.com.cn/zh/huashan-a2000/

### Axelera Metis

**形态**：PCIe / M.2 独立 AI Accelerator

**官方已确认**
- Digital In-Memory Compute
- 约 214 INT8 TOPS
- PCIe Gen3 x4
- 不同产品/版本提供约 4GB 或 16GB memory 配置
- 典型应用功耗为个位数至十余瓦，视产品形态而定
- Voyager SDK
- 官方文档明确：真实 pipeline 性能取决于模型、PCIe传输和前后处理，不应只看 peak TOPS

**工程意义**
是“Host + 独立 NPU”路线的典型代表；必须额外评价 host CPU、视频处理和 PCIe 数据搬运。

来源：
https://docs.axelera.ai/sdk/reference/system/hardware/
https://axelera.ai/ai-accelerators/aipu/metis

### Hailo-10H

**形态**：M.2 / Chip-on-board GenAI Edge Accelerator

**官方已确认/厂商宣称**
- 40 TOPS INT4 / 20 TOPS INT8
- 典型功耗约 2.5W
- 支持视觉 AI 与生成式 AI
- 官方强调 on-device LLM/VLM
- LPDDR4/4X

**工程意义**
代表低功耗独立加速器开始从传统视觉推理扩展到小型生成式 AI/VLM。

来源：
https://hailo.ai/company-overview/newsroom/news/hailo-announces-general-availability-of-hailo-10h-edge-ai-accelerator-with-generative-ai-capabilities/

### Firefly + 后摩 LQ50 模组

**形态**：第三方边缘平台中的 M.2 AI 模组

**第三方/合作方资料**
Firefly 当前公开的 RK1828 AI 双卡算力阵列套件页面列出：
- 后摩 LQ50
- 48GB LPDDR5
- 160 TOPS INT8
- 页面宣称可运行 35B 以内大模型

**证据限制**
当前本项目只取得 Firefly 公开页面，不能把这些数据标记为“后摩官方独立确认”。后续必须补后摩官方 Datasheet/SDK/Benchmark。

来源：
https://community.t-firefly.com/eco-hardware/rk1828-kit

## 3. 初步产业观察

### 事实 1：产品形态已经明显分化

同样被称为“端侧算力”，实际可能是：
- 集成 SoC
- SOM
- 机器人平台
- 车规 SoC
- M.2/PCIe 加速器
- 计算盒/边缘服务器

因此不能直接横向 TOPS 排名。

### 事实 2：新平台开始公开强调 Transformer、VLM/LLM、E2E

Jetson Thor、Hailo-10H、Axelera 当前产品，及地平线/黑芝麻车规路线，都已经公开面向 Transformer、生成式 AI、多模态或 E2E。

这证明“大模型/多模态进入端侧”是产业事实，但其是否适合 UAV 等严格 SWaP 场景仍需任务级分析。

### 事实 3：传统视觉/机器人负载仍然重要

RB5、RK3588、Jetson Orin 的产品特征仍大量围绕：
- Camera
- ISP/Video
- 多传感器
- ROS
- CV
- 实时推理

说明未来不是“大模型取代一切”，而更可能是多类工作负载并存。

## 4. 待补充

后续优先补齐：
- 后摩官方产品/SDK/Benchmark
- NVIDIA Orin NX/AGX Orin完整功耗/Camera参数
- Hailo-8/Hailo-15
- Axelera不同模块/板卡形态
- 地平线征程6具体型号
- 黑芝麻 A2000 Lite/Pro
- 昇腾/寒武纪/算能适合无人端侧的具体产品
- Qualcomm 新一代 Robotics / Dragonwing 平台
