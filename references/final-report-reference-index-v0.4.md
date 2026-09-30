# 最终调研报告参考文献索引 v0.4

- 日期：2026-09-30
- 对应报告：`reports/drafts/secure-trusted-edge-intelligence-report-v0.4.md`
- 目的：为最终报告提供可点击、可追溯的证据入口，特别说明 W1–W9、C1–C5、架构分类和 Trust Plane 等“本项目抽象”分别建立在什么行业事实之上。
- 引用规则：正文使用 `[Rxx]` 编号；编号对应本索引。优先采用标准/官方文档/同行评审论文，其次为厂商官方产品资料。厂商产品数据只证明对应 SKU/产品公开能力，不自动等同第三方实测。

> **重要说明**：W1–W9 与 C1–C5 的编号和名称是本项目为“应用 → 工作负载 → 资源 → 架构”分析而建立的研究分类，不是某个国际标准直接给出的九级或五级体系。其内容来源于 PX4、Nav2、Autoware、Waymo 等成熟工程栈以及无人系统/机器人论文综述。报告必须先陈述这些来源，再说明本项目如何进行跨领域抽象。

---

## A. 自主性、功能栈与跨领域方法依据

<a id="r01"></a>
### R01 — NIST ALFUS：Autonomy Levels for Unmanned Systems
- 类型：标准/政府研究框架
- 机构：NIST
- 主要用途：支撑“不使用跨 UAV/UGV/USV/Robot 的自创线性 L1–L5”；支撑 Mission Complexity、Environmental Complexity、Human Independence 等多维描述。
- 官方入口：https://www.nist.gov/publications/framework-autonomy-levels-unmanned-systems-alfus-0
- Framework Volume II：https://www.nist.gov/publications/autonomy-levels-unmanned-systems-alfus-frameworkvolume-ii-framework-models-initial
- 仓库摘要：`references/standards/nist-alfus.md`

<a id="r02"></a>
### R02 — SAE J3016_202609
- 类型：行业标准
- 机构：SAE International
- 当前版本：J3016_202609（2026-09-20）
- 主要用途：说明道路车辆 Level 0–5 是 On-Road Motor Vehicle Driving Automation 专用术语，不能直接覆盖 UAV/USV/机器人。
- 官方入口：https://saemobilus.sae.org/topics/electrical-electronics-and-avionics/automation
- 仓库摘要：`references/standards/sae-j3016.md`

<a id="r03"></a>
### R03 — IMO MASS Code / Autonomous Shipping FAQ
- 类型：国际组织规范
- 机构：IMO
- 当前事实：2026 年 5 月通过非强制 MASS Code，2026-07-01 生效；强调 functional approach、人类监督、连接与网络安全。
- 官方入口：https://www.imo.org/en/mediacentre/hottopics/pages/autonomous-shipping.aspx
- 采用公告：https://www.imo.org/en/mediacentre/pressbriefings/pages/imo-adopts-mass-code.aspx
- 仓库摘要：`references/standards/imo-mass.md`

<a id="r04"></a>
### R04 — PX4 Computer Vision
- 类型：官方工程文档
- 机构：PX4 / Dronecode
- 主要用途：证明 UAV 视觉计算不只有目标检测，还包括 Optical Flow、VIO、Collision Prevention；Companion Computer 是现实架构。
- 官方入口：https://docs.px4.io/main/en/advanced/computer_vision
- 仓库摘要：`references/webpages/px4-computer-vision.md`

<a id="r05"></a>
### R05 — PX4 Visual Inertial Odometry
- 类型：官方工程文档
- 主要用途：支撑 W2 状态估计/定位；VIO 通过视觉与 IMU 估计 3D 位姿、速度，并用于 GNSS 不可用或不可靠环境。
- 官方入口：https://docs.px4.io/main/en/computer_vision/visual_inertial_odometry
- 仓库摘要：`references/webpages/px4-computer-vision.md`

<a id="r06"></a>
### R06 — PX4 Collision Prevention
- 类型：官方工程文档
- 主要用途：支撑避障闭环、探测距离、速度与响应时延之间存在直接工程关系。
- 官方入口：https://docs.px4.io/main/en/computer_vision/collision_prevention
- 仓库摘要：`references/webpages/px4-collision-prevention-timing.md`

<a id="r07"></a>
### R07 — Nav2 Navigation Concepts
- 类型：官方工程文档
- 项目：ROS 2 Navigation2
- 主要用途：支撑 State Estimation、Environmental Representation、Planning、Control、Behavior Tree 等模块化导航链。
- 官方入口：https://docs.nav2.org/rolling/getting_started/navigation_concepts/
- 仓库摘要：`references/webpages/nav2-navigation.md`

<a id="r08"></a>
### R08 — Autoware Architecture
- 类型：官方工程文档
- 机构：Autoware Foundation
- 主要用途：支撑 Sensing、Map、Localization、Perception、Planning、Control、Vehicle Interface 的完整自动驾驶功能栈。
- 官方入口：https://docs.autoware.org/main/design/autoware-architecture-v1/
- 仓库摘要：`references/webpages/autoware-architecture.md`

<a id="r09"></a>
### R09 — Autoware Perception Component
- 类型：官方工程文档
- 主要用途：支撑感知包括 Object Recognition、Obstacle Segmentation、Traffic Light、Occupancy 等，不等同单一 Detection。
- 官方入口：https://docs.autoware.org/main/design/autoware-architecture-v1/components/perception/
- 仓库摘要：`references/webpages/autoware-architecture.md`

<a id="r10"></a>
### R10 — Waymo Driver FAQ
- 类型：真实系统官方说明
- 机构：Waymo
- 主要用途：Waymo 将自动驾驶软件公开归纳为“Where am I? What’s around me? What will happen next? What should I do?”；支撑定位、感知、预测、决策的通用分解。
- 官方入口：https://waymo.com/faq/
- 仓库摘要：`references/webpages/deployed-autonomous-systems.md`

---

## B. UAV / Robot / USV / Edge 应用事实与综述

<a id="r11"></a>
### R11 — GNSS-Denied UAV Navigation Review
- 类型：同行评审综述
- 文献：Gnss-denied unmanned aerial vehicle navigation: analyzing computational complexity, sensor fusion, and localization methodologies
- 期刊：Satellite Navigation, 2025
- 主要用途：支撑 VIO、SLAM、LiDAR/vision/inertial fusion 是 UAV 自主导航现实计算负载。
- DOI/页面：https://link.springer.com/article/10.1186/s43020-025-00162-z
- 仓库摘要：`references/papers/uav-gnss-denied-navigation-2025.md`

<a id="r12"></a>
### R12 — Multi-Robot Navigation Survey
- 类型：同行评审综述
- 文献：A survey of autonomous robots and multi-robot navigation: Perception, planning and collaboration
- 期刊：Biomimetic Intelligence and Robotics, 2025
- 主要用途：支撑 W8 中 perception / planning / collaboration、distributed state、multi-robot communication 等负载。
- 页面：https://www.sciencedirect.com/science/article/pii/S2667379724000615
- 仓库摘要：`references/papers/multi-robot-navigation-2025.md`

<a id="r13"></a>
### R13 — USV Overview
- 类型：同行评审综述
- 文献：An overview of Unmanned Surface Vehicles: Methods, practices, and applications
- 期刊：Control Engineering Practice, 2025
- 主要用途：支撑 USV 的 navigation / guidance / control / perception / path planning 与长航时系统问题。
- 页面：https://www.sciencedirect.com/science/article/pii/S0967066125002412
- 仓库摘要：`references/papers/usv-overview-2025.md`

<a id="r14"></a>
### R14 — Edge Computing and Its Application in Robotics
- 类型：Open Access Review
- 作者：Nazish Tahir, Ramviyas Parasuraman
- 期刊：Journal of Sensor and Actuator Networks, 2025, 14(4):65
- 主要用途：支撑 robot/edge/cloud 分层；低时延、本地处理、网络波动和 task offloading。
- DOI：https://doi.org/10.3390/jsan14040065
- 仓库摘要：`references/papers/edge-robotics-2025.md`

<a id="r15"></a>
### R15 — MiR250 / MiR Fleet
- 类型：真实 AMR 产品官方资料
- 主要用途：证明工业 AMR 采用 safety laser、3D camera、proximity sensor，并存在 Fleet 级任务和交通管理。
- 产品规格：https://mobile-industrial-robots.com/products/robots/mir250/specifications
- Fleet/产品入口：https://mobile-industrial-robots.com/
- 仓库摘要：`references/webpages/deployed-autonomous-systems.md`

<a id="r16"></a>
### R16 — Saildrone Voyager
- 类型：真实 USV 产品官方资料
- 主要用途：证明 USV 长航时、多传感器、Radar/AIS/IR Camera、持续海上任务的实际产品形态。
- 官方入口：https://www.saildrone.com/platform/voyager
- 仓库摘要：`references/webpages/deployed-autonomous-systems.md`

---

## C. BEV、Foundation Model、VLM/VLA 与未来负载

<a id="r17"></a>
### R17 — BEVFormer
- 类型：ECCV 2022 论文
- 主要用途：证明 multi-camera + spatial cross-attention + temporal self-attention 的 BEV 感知是真实工作负载；支撑 W4/W5 的多视图时空融合分析。
- ECVA 页面：https://www.ecva.net/papers/eccv_2022/papers_ECCV/html/694_ECCV_2022_paper.php
- 仓库摘要：`references/papers/bevformer.md`

<a id="r18"></a>
### R18 — PaLM-E
- 类型：ICML 2023 论文
- 文献：PaLM-E: An Embodied Multimodal Language Model
- 主要用途：支撑机器人中视觉、连续状态与语言融合的 Foundation Model 路线。
- 页面：https://proceedings.mlr.press/v202/driess23a.html
- 仓库索引：`references/papers/foundation-models-robotics.md`

<a id="r19"></a>
### R19 — RT-2
- 类型：Google DeepMind 官方研究
- 主要用途：支撑 Vision-Language-Action 模型把视觉/语言映射为机器人动作的真实技术路线。
- 页面：https://deepmind.google/blog/rt-2-new-model-translates-vision-and-language-into-action/
- 仓库索引：`references/papers/foundation-models-robotics.md`

<a id="r20"></a>
### R20 — OpenVLA
- 类型：论文 + 开源项目
- 主要事实：7B 参数；基于 970k real-world robot demonstrations 训练。
- 主要用途：支撑 W7 的模型规模、内存和动作输出工作负载。
- 项目：https://openvla.github.io/
- 论文：https://arxiv.org/abs/2406.09246
- 仓库索引：`references/papers/foundation-models-robotics.md`

<a id="r21"></a>
### R21 — Efficient Vision-Language-Action Models Survey
- 类型：系统综述
- 主要用途：支撑 VLA 部署的 computational demand、memory demand、real-time requirement、latency 与 onboard constraints。
- 页面：https://arxiv.org/abs/2510.17111
- 仓库摘要：`references/papers/vla-efficiency-2025.md`

---

## D. Benchmark、数据集与系统性能证据

<a id="r22"></a>
### R22 — NVIDIA Isaac ROS
- 类型：官方机器人软件栈
- 主要用途：证明机器人端侧平台同时覆盖 perception、Visual SLAM、depth、mapping、pose、motion planning 等 workload。
- 官方入口：https://developer.nvidia.com/isaac/ros
- 仓库摘要：`references/webpages/nvidia-isaac-ros.md`

<a id="r23"></a>
### R23 — Isaac ROS 5.0 Performance
- 类型：固定软件版本官方 Benchmark
- 主要用途：提供 Jetson Orin 节点/graph latency 与 throughput 锚点；强调版本化 Benchmark。
- 页面：https://nvidia-isaac-ros.github.io/v/release-5.0/performance/index.html
- 仓库摘要：`references/benchmarks/isaac-ros-5.0-latency-anchors.md`

<a id="r24"></a>
### R24 — Isaac ROS 3.2 Nova Carter Live Graph
- 类型：固定版本物理多摄像头系统 Benchmark
- 主要用途：提供物理多 Camera VSLAM / depth / mapping 的整图证据；不能自动等同六摄 YOLO。
- 页面：https://nvidia-isaac-ros.github.io/v/release-3.2/performance/index.html
- 仓库摘要：`references/benchmarks/jetson-nova-multicamera-perceptor-2026.md`

<a id="r25"></a>
### R25 — MLPerf Inference
- 类型：行业 Benchmark
- 机构：MLCommons
- 主要用途：作为 W3 等统一模型/输入/精度比较的公共基准入口。
- 官方入口：https://mlcommons.org/benchmarks/inference-datacenter/
- 仓库摘要：`references/benchmarks/mlperf-edge.md`

<a id="r26"></a>
### R26 — EuRoC MAV Dataset
- 类型：公开 UAV/VIO 数据集
- 主要用途：W2 VIO/SLAM 统一验证。
- 官方入口：https://projects.asl.ethz.ch/datasets/doku.php?id=kmavvisualinertialdatasets
- 仓库摘要：`references/benchmarks/euroc-tumvi.md`

<a id="r27"></a>
### R27 — TUM VI Dataset
- 类型：公开 Visual-Inertial Dataset
- 主要用途：W2 VIO/SLAM 统一验证。
- 官方入口：https://cvg.cit.tum.de/data/datasets/visual-inertial-dataset
- 仓库摘要：`references/benchmarks/euroc-tumvi.md`

---

## E. Security / Trust / Remote Attestation

<a id="r28"></a>
### R28 — ROS 2 Security / DDS-Security
- 类型：官方工程文档
- 主要用途：支撑 ROS 2 中身份认证、访问控制、加密/认证等安全能力；同时不能把 middleware security 等同 OS-level sandbox。
- 官方入口：https://docs.ros.org/en/rolling/Concepts/Intermediate/About-Security.html
- 仓库证据：`references/webpages/secure-edge-intelligence-evidence-2026.md`

<a id="r29"></a>
### R29 — PX4 Security
- 类型：官方工程文档
- 主要用途：证明 UAV 产品化需要 Secure Boot、MAVLink 安全、生产配置等安全加固；MAVLink Signing 与 payload encryption 必须区分。
- 官方入口：https://docs.px4.io/main/en/security/
- 仓库证据：`references/webpages/secure-edge-intelligence-evidence-2026.md`

<a id="r30"></a>
### R30 — IETF RFC 9334: RATS Architecture
- 类型：IETF 标准化架构
- 主要用途：Remote Attestation 中 Attester、Verifier、Relying Party、Evidence、Attestation Result 的术语与角色依据。
- 官方入口：https://www.rfc-editor.org/rfc/rfc9334.html

<a id="r31"></a>
### R31 — NIST SP 800-193 Platform Firmware Resiliency Guidelines
- 类型：NIST 指南
- 主要用途：支撑平台固件“保护—检测—恢复”、Root of Trust、安全更新和恢复机制。
- 官方入口：https://csrc.nist.gov/pubs/sp/800/193/final

<a id="r32"></a>
### R32 — NVIDIA Jetson Security
- 类型：官方开发文档/产品能力案例
- 主要用途：证明现实机器人 SoC 可组合 Secure Boot、OP-TEE、Secure Storage、Disk Encryption、fTPM、Rollback Protection。
- 官方入口：https://docs.nvidia.com/jetson/archives/r36.4.4/DeveloperGuide/SD/Security.html

<a id="r33"></a>
### R33 — NVIDIA fTPM / Measured Boot
- 类型：官方开发文档
- 主要用途：说明 Secure Boot 与 Measured Boot 不同；PCR/measurement 可用于平台状态验证；fTPM 需要每设备 provisioning。
- Boot Flow：https://docs.nvidia.com/jetson/archives/r39.2.1/DeveloperGuide/SD/Security/FirmwareTPM/BootFlow.html
- Provisioning：https://docs.nvidia.com/jetson/archives/r39.2/DeveloperGuide/SD/Security/FirmwareTPM/Provisioning.html

<a id="r34"></a>
### R34 — Arm Platform Security Architecture
- 类型：架构规范/官方技术框架
- 主要用途：支撑把 Crypto、Secure Storage、Attestation、Firmware Update 等能力抽象成统一安全服务。
- 官方入口：https://www.arm.com/architecture/security-features/platform-security
- 仓库分析：`research/architecture/trust-plane-implementation-options.md`

---

## F. 代表性端侧产品/平台来源

<a id="r35"></a>
### R35 — NVIDIA Jetson Orin / Developer Kits / Lifecycle
- 类型：官方产品资料
- 主要用途：Integrated GPU SoM / Dev Kit 产品形态参考。
- Developer Kits：https://developer.nvidia.com/embedded/jetson-developer-kits
- Lifecycle：https://developer.nvidia.com/embedded/lifecycle
- 仓库产品索引：`references/webpages/commercial-products-solutions-2026.md`

<a id="r36"></a>
### R36 — Qualcomm Dragonwing IQ-9075
- 类型：官方产品资料
- 主要用途：机器人/无人机专用高集成 SoC/EVK 代表；公开多 Camera、RT subsystem、内存等能力。
- 官方入口：https://www.qualcomm.com/internet-of-things/products/iq9-series/iq-9075
- 仓库产品索引：`references/webpages/commercial-products-solutions-2026.md`

<a id="r37"></a>
### R37 — Firefly AIBOX PRO
- 类型：官方产品资料
- 主要用途：Host + M.2 Accelerator 已产品化的直接案例。
- 官方入口：https://www.t-firefly.com/products/aibox-pro-edge-computing-computer
- 仓库产品索引：`references/webpages/commercial-products-solutions-2026.md`

<a id="r38"></a>
### R38 — Houmo LQ50 M.2
- 类型：官方硬件指南
- 主要用途：独立 M.2 AI Accelerator 代表；说明 accelerator 自带算力/内存但仍依赖 Host。
- 官方入口：https://developer.houmoai.com/hmdoc/m50/hardware-manuals/latest/product-manuals/lq50-m.2/LQ50_M.2_guidelines/intro/index.html
- 仓库产品索引：`references/webpages/commercial-products-solutions-2026.md`

<a id="r39"></a>
### R39 — Axelera Metis / Embedded 113m
- 类型：官方产品/开发文档
- 主要用途：独立 AI accelerator、ARM Host 路线参考。
- 官方入口：https://docs.axelera.ai/docs/hardware/getting-started/start/embedded-113m/
- 仓库产品索引：`references/webpages/commercial-products-solutions-2026.md`

<a id="r40"></a>
### R40 — Hailo-10H M.2
- 类型：官方产品资料
- 主要用途：低功耗 CV + GenAI/VLM accelerator 路线参考。
- 官方入口：https://hailo.ai/zh-hans/products/ai-accelerators/hailo-10h-m-2-generative-ai-acceleration-module/
- 仓库产品索引：`references/webpages/commercial-products-solutions-2026.md`

<a id="r41"></a>
### R41 — Huawei Atlas 200I A2
- 类型：官方产品资料
- 主要用途：国产高集成边缘计算模块；官方面向机器人/无人机。
- 官方入口：https://www.hiascend.com/zh/hardware/accelerator-module-A2
- 仓库产品索引：`references/webpages/commercial-products-solutions-2026.md`

<a id="r42"></a>
### R42 — Firefly Core/AIO-1688JD4 / SOPHGO BM1688
- 类型：官方产品资料
- 主要用途：国产视觉计算板级方案，公开出现 6-channel sensor input；不能自动等同本项目六路同步模式。
- 官方入口：https://www.t-firefly.com/products/core-1688jd4-core-board
- 仓库产品索引：`references/webpages/commercial-products-solutions-2026.md`

<a id="r43"></a>
### R43 — Seeed reComputer Robotics
- 类型：官方产品/文档
- 主要用途：Robot Computer 产品形态，展示 GMSL、CAN、宽压等系统级集成。
- 官方入口：https://wiki.seeedstudio.com/recomputer_robotics_j401_getting_started/
- 仓库产品索引：`references/webpages/commercial-products-solutions-2026.md`

<a id="r44"></a>
### R44 — Advantech MIC-733-AO
- 类型：官方工业计算机产品
- 主要用途：Rugged/Industrial Robotics Computer 形态参考。
- 官方入口：https://www.advantech.com/en-us/products/965e4edb-fb98-429e-89ed-9a0a8435a7be/mic-733/mod_09861425-4950-46ab-ad39-1b5522881218
- 仓库产品索引：`references/webpages/commercial-products-solutions-2026.md`

<a id="r45"></a>
### R45 — AMD Kria K26 / KR260
- 类型：官方产品资料
- 主要用途：FPGA + Arm、可编程 I/O、机器人/ROS 2 路线参考，说明 TOPS 并非唯一价值维度。
- 官方入口：https://www.amd.com/en/products/system-on-modules/kria/k26.html
- Robotics：https://www.amd.com/en/products/system-on-modules/kria/k26/robotics.html
- 仓库产品索引：`references/webpages/commercial-products-solutions-2026.md`

<a id="r46"></a>
### R46 — Intel Robotics AI Suite
- 类型：官方解决方案生态
- 主要用途：CPU/GPU/NPU workload consolidation、ROS 2/OpenVINO 与工业机器人软件生态参考。
- 官方入口：https://builders.intel.com/intel-technologies/software/edge-ai-suites/robotics-ai-suite
- 仓库产品索引：`references/webpages/commercial-products-solutions-2026.md`

---

## G. 参考文献如何支撑 W1–W9

| 本项目工作负载 | 主要行业来源 | 依据说明 |
|---|---|---|
| W1 Sensor I/O / Video Pipeline | R04、R08、R22、R42 | PX4/Autoware/Isaac ROS 均以 sensing/camera 为上游；现有 SoC/板卡也把 ISP、视频、Camera 作为一级能力 |
| W2 State Estimation / Localization | R05、R07、R08、R11、R22 | PX4 VIO、Nav2 State Estimation、Autoware Localization、UAV GNSS-denied 综述共同证明该负载长期独立存在 |
| W3 DNN Perception | R09、R10、R22、R25 | Autoware Perception、Waymo、Isaac ROS、MLPerf 均提供感知/AI 推理事实依据 |
| W4 Mapping / World Representation | R07、R09、R17、R22 | Nav2 costmap/environment representation、Autoware occupancy、BEVFormer、Isaac ROS mapping 支撑 |
| W5 Prediction / Tracking / Situation Understanding | R10、R17、R12 | Waymo “What will happen next”、时空 BEV、多机器人态势/协作支撑 |
| W6 Planning / Optimization / Decision | R07、R08、R10、R13 | Nav2 Planner/Controller、Autoware Planning、Waymo “What should I do”、USV guidance/planning 支撑 |
| W7 Foundation Model / VLM / LLM / VLA | R18、R19、R20、R21 | PaLM-E、RT-2、OpenVLA、VLA efficiency survey 支撑 |
| W8 Multi-Agent / Fleet | R12、R15、R16 | Multi-robot survey、MiR Fleet、长航时/联网 USV 系统支撑 |
| W9 Safety / Control Supervision | R03、R06、R07、R08、R15 | MASS、PX4 collision prevention、Nav2 control、Autoware control、MiR safety functions 支撑 |

### 解释

W1–W9 不是对任何单一框架的逐字抄录，而是将上述不同领域中反复出现的工程模块转化为“可做资源预算”的跨领域 workload taxonomy。其价值是把同一类计算问题在 UAV、UGV、USV、AMR、机器人中统一描述；其边界必须由上述原始资料约束，不能再随意扩展为“行业标准等级”。

---

## H. 参考材料可信度使用顺序

最终报告默认：
1. 标准、政府/国际组织规范；
2. 官方工程文档、Datasheet、Developer Guide；
3. 同行评审论文和高质量综述；
4. 官方 Benchmark；
5. 厂商产品资料/白皮书；
6. 合作伙伴公开资料；
7. 社区结果。

其中产品页面、厂商 Benchmark 均应明确标注 VENDOR/SPEC，不能写成“独立实测”。


---

## I. C1–C5 组合原型与固定边缘参考

<a id="r47"></a>
### R47 — NVIDIA Metropolis / Intelligent Video Analytics
- 类型：官方解决方案/应用平台
- 主要用途：支撑 C1“多摄像头智能分析”不是假设场景，而是现实 fixed-edge video analytics 产品形态；应用覆盖 multi-camera tracking、traffic、inspection、robot safety、VLM/CV 等。
- 官方入口：https://www.nvidia.com/en-us/autonomous-machines/intelligent-video-analytics-platform/
- 仓库摘要：`references/webpages/deployed-autonomous-systems.md`

---

## J. 中国可信计算 / 商用密码标准

<a id="r48"></a>
### R48 — GB/T 38638-2020《信息安全技术 可信计算 可信计算体系结构》
- 类型：国家标准，推荐性，现行；2025-12-08 复审结论“继续有效”。
- 主要用途：支撑“可信计算是体系而非单颗器件”，为国产 Trust Plane 总体结构提供国家标准依据。
- 官方入口：https://std.samr.gov.cn/gb/search/gbDetailed?id=A47A713B763F14ABE05397BE0A0ABB25
- 仓库索引：`references/standards/china-trusted-computing-crypto-standards-2026.md`

<a id="r49"></a>
### R49 — GB/T 29829-2022《信息安全技术 可信计算密码支撑平台功能与接口规范》
- 类型：国家标准，推荐性，现行。
- 主要用途：支撑可信密码支撑平台、功能与接口层设计，以及 Trust Service 的平台化抽象。
- 官方入口：https://std.samr.gov.cn/gb/search/gbDetailedCNF?id=DD3D95E5C12171EBE05397BE0A0AF33F

<a id="r50"></a>
### R50 — GM/T 0011-2023《可信计算 可信密码支撑平台功能与接口规范》
- 类型：密码行业标准，推荐性，现行；2024-06-01 实施，替代 GM/T 0011-2012。
- 主管部门：国家密码管理局。
- 主要用途：无人装备 Trust Plane 中可信密码平台/服务层的直接行业标准依据。
- 官方入口：https://std.samr.gov.cn/hb/search/stdHBDetailed?id=1BF26B7A9FF8FD76E06397BE0A0A81D8
- 国家密码管理局公告：https://oscca.gov.cn/sca/xxgk/2023-12/23/content_1061160.shtml

<a id="r51"></a>
### R51 — GM/T 0012-2020《可信计算 可信密码模块接口规范》
- 类型：密码行业标准，推荐性，现行。
- 主要用途：TCM 可信密码模块接口与系统集成依据。
- 官方入口：https://std.samr.gov.cn/hb/search/stdHBDetailed?id=C60C676BC20A358AE05397BE0A0AFABB

<a id="r52"></a>
### R52 — GM/T 0013-2021《可信计算 可信密码模块接口符合性测试规范》
- 类型：密码行业标准，推荐性，现行。
- 主要用途：TCM 接口实现的符合性测试依据。
- 官方入口：https://std.samr.gov.cn/hb/search/stdHBDetailed?id=E66CC4F6F8D88B7FE05397BE0A0A6C55

<a id="r53"></a>
### R53 — GM/T 0058-2018《可信计算 TCM服务模块接口规范》
- 类型：密码行业标准。
- 主要用途：支持“底层 TCM → service module → 上层应用”的分层服务设计。
- 官方入口：https://www.oscca.gov.cn/sca/xxgk/2018-05/02/content_1029272.shtml

<a id="r54"></a>
### R54 — GM/T 0079-2020《可信计算平台直接匿名证明规范》
- 类型：密码行业标准，推荐性，现行。
- 主要用途：支撑国内可信计算平台的证明能力，说明 Trust Plane 不应只停留在 Secure Boot/Key Storage。
- 官方入口：https://std.samr.gov.cn/hb/search/stdHBDetailed?id=C60C676BC20C358AE05397BE0A0AFABB

<a id="r55"></a>
### R55 — GM/T 0082-2020《可信密码模块保护轮廓》
- 类型：密码行业标准，推荐性，现行。
- 主要用途：可信密码模块本体安全要求/保护轮廓证据。
- 官方入口：https://std.samr.gov.cn/hb/search/stdHBDetailed?id=C60C676BC20F358AE05397BE0A0AFABB

<a id="r56"></a>
### R56 — GM/T 0028-2024《密码模块安全要求》
- 类型：密码行业标准，推荐性，现行；2025-07-01 实施。
- 主要用途：独立安全芯片、密码模块、可信密码模块等产品设计、开发与检测的通用安全要求依据。
- 官方入口：https://std.samr.gov.cn/hb/search/stdHBDetailed?id=397D60066A540FA6E06397BE0A0AD887

<a id="r57"></a>
### R57 — GM/T 0132-2023《信息系统密码应用实施指南》
- 类型：密码行业标准，推荐性，现行。
- 主要用途：将“有密码算法/器件”提升为系统级密码应用实施，支撑设备身份、存储、通信、升级与密钥管理的一体化设计。
- 官方入口：https://std.samr.gov.cn/hb/search/stdHBDetailed?id=1BF26B7A9FF4FD76E06397BE0A0A81D8

<a id="r58"></a>
### R58 — GM/T 0115-2021《信息系统密码应用测评要求》
- 类型：密码行业标准，推荐性，现行。
- 主要用途：支撑安全可信平台的密码应用测试/验收设计。
- 官方入口：https://std.samr.gov.cn/hb/search/stdHBDetailed?id=E66CC4F6F8E58B7FE05397BE0A0A6C55

<a id="r59"></a>
### R59 — GB/T 32918.2-2016 / GB/T 32918.4-2016（SM2）
- 类型：国家标准，现行；2025-12-08 复审继续有效。
- 用途：设备身份、固件/模型签名与公钥加密算法依据。
- 数字签名：https://std.samr.gov.cn/gb/search/gbDetailed?id=71F772D811F7D3A7E05397BE0A0AB82A
- 公钥加密：https://std.samr.gov.cn/gb/search/gbDetailed?id=71F772D81348D3A7E05397BE0A0AB82A

<a id="r60"></a>
### R60 — GB/T 32905-2016《信息安全技术 SM3密码杂凑算法》
- 类型：国家标准，现行；2025-12-08 复审继续有效。
- 用途：firmware/model/config/log 完整性度量与 hash 基础。
- 官方入口：https://std.samr.gov.cn/gb/search/gbDetailed?id=71F772D8119BD3A7E05397BE0A0AB82A

<a id="r61"></a>
### R61 — GB/T 32907-2016《信息安全技术 SM4分组密码算法》
- 类型：国家标准，现行；2025-12-08 复审继续有效。
- 用途：任务数据、模型包、存储和链路保密性保护。
- 官方入口：https://std.samr.gov.cn/gb/search/gbDetailed?id=71F772D81199D3A7E05397BE0A0AB82A

<a id="r62"></a>
### R62 — GM/T 0008-2012《安全芯片密码检测准则》
- 类型：密码行业标准，现行。
- 用途：独立商密安全芯片/SE 的密码检测证据入口。
- 官方入口：https://std.samr.gov.cn/hb/search/stdHBDetailed?id=8B1827F1B093BB19E05397BE0A0AB44A

---

## K. C1–C5 组合来源映射

| 组合 | 中文名称 | 主要来源 | 定义动机 |
|---|---|---|---|
| C1 | 多摄像头智能分析 | R47、R22、固定边缘视频产品 | 提取“高视频/AI负载但没有本体定位与控制”的资源原型 |
| C2 | 视觉自主系统/视觉自主闭环 | R04、R05、R06、R07、R24、R11 | 表示 Camera/IMU 真正进入定位—地图—规划—控制闭环 |
| C3 | 多传感器自主系统 | R08、R09、R10、R13 | 在 C2 基础上突出 LiDAR/Radar 等多传感器融合和 Prediction |
| C4 | 基础模型增强机器人/无人系统 | R18、R19、R20、R21 | 在基础自主栈上叠加 W7，增加模型容量、内存、TTFT/action latency |
| C5 | 协同自主系统 | R12、R15 | 在单机自主基础上增加网络、distributed state、task allocation 与 Fleet |

C1–C5 是“资源结构原型”，不是行业等级。C4/C5 更接近正交叠加项。
