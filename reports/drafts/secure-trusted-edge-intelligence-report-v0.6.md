# 面向无人装备的安全可信端侧智能计算平台技术调研报告

> 版本：v0.6（应用现状与伴飞计算机需求驱动增强版）  
> 日期：2026-10-23  
> 状态：正式报告初稿 / 应用与案例增强；尚未完成项目实测  
> 研究仓库：edge-intelligence-research  
> 参考文献索引：[`references/final-report-reference-index-v0.5.md`](../../references/final-report-reference-index-v0.5.md)  
> 产品资料时效复核：[`references/webpages/product-refresh-2026-10-08.md`](../../references/webpages/product-refresh-2026-10-08.md)

---

# 摘要

**本版更新要点。** 以既有 v0.5 的完整工作负载、产品、可信计算研究为底稿，补充现有 UAV/UGV 的真实端侧与边侧能力及部署边界，新增伴飞计算机产品对照与本项目吊舱 ATR、双目避障、任务管理、多机协同的独立需求论证。工程主张不预设“必须加 M.2 卡”或“必须上 LLM”，先以算法实现、并发资源及真实任务收益验证是否需要扩展。


面向无人机、无人车、无人船、自主移动机器人以及固定式边缘智能设备，端侧智能计算平台正在由传统的视频处理节点或单一神经网络推理加速器，演变为集多传感器接入、异构计算、定位导航、环境感知、地图构建、任务规划、实时控制协同和安全可信于一体的系统级计算平台。

本报告围绕“应用场景—智能任务—工作负载—系统资源—计算架构—芯片与产品—工程验证”主线开展研究。报告首先基于 PX4、Nav2、Autoware、Waymo 以及无人系统相关论文和标准，梳理无人装备通用功能链；在此基础上，为满足硬件资源预算与平台选型需求，将跨领域反复出现的计算任务抽象为 W1～W9 九类工作负载，并进一步形成 C1～C5 五类典型工作负载组合。上述分类属于本项目面向资源分析的研究方法，不作为行业标准或自主等级使用。

报告认为，无人装备计算平台不能以 TOPS 作为唯一选型依据。除神经网络推理能力外，多摄像头接入能力、ISP/VPU、CPU/GPU、内存容量与带宽、Camera/SerDes/PCIe/Ethernet/CAN 等接口、P95/P99 尾延迟、Frame Age、功耗与散热、ROS 2/模型工具链以及安全可信能力同样决定系统最终可用性。

在产品调研方面，本报告对 NVIDIA Jetson、Qualcomm Dragonwing IQ-9075、Rockchip RK3588、Huawei Atlas 200I A2、SOPHGO BM1688、Houmo LQ50、Axelera Metis、Hailo-10H、Firefly AIBOX PRO、Seeed reComputer、Advantech MIC-733、Horizon Journey 6、Black Sesame A2000 等代表性产品和平台进行分类分析。调研表明，当前市场已形成高集成 SoC/SoM、GPU 机器人平台、独立 M.2/PCIe AI 加速卡、Host+Accelerator 异构计算盒、工业机器人计算机以及车规/Physical AI SoC 等多条技术路线。不同产品形态在数据通路、实时性、软件生态、SWaP 和工程成熟度方面差异明显，不宜直接按 TOPS 横向排名。

针对公司在密码安全和可信计算方面的技术基础，本报告提出“Compute Plane + Real-Time Plane + Trust Plane”三平面安全可信无人智能计算平台架构，并结合 GB/T 38638-2020、GB/T 29829-2022、GM/T 0011-2023、GM/T 0012-2020、GM/T 0028-2024 等国内可信计算与商用密码标准，给出设备身份、可信启动、平台度量、远程证明、模型可信、通信安全、安全升级和设备失陷处置等能力建议。

六摄像头无人平台作为本报告的工程案例，用于验证“需求—工作负载—资源—候选架构—Benchmark”方法。当前阶段建议优先冻结摄像头实际帧率、Camera Routing、VIO/Depth/Detection 路数、飞行速度、有效探测距离、机体响应和 SWaP 约束，并在此基础上对一体化 SoC、GPU SoM 和 Host+Accelerator 等路线开展系统级 Benchmark。

**关键词：** 无人装备；端侧智能；异构计算；视觉自主；VIO；SLAM；VLM；AI 加速器；安全可信；商用密码；可信计算

---

# 1 调研概述

## 1.1 调研背景

随着无人装备自主能力不断提升，计算任务已经由早期的飞控、视频编码和遥测，扩展到环境感知、视觉定位、地图构建、自主避障、轨迹规划和任务理解。PX4 已将视觉—惯性里程计（VIO）、光流和 Collision Prevention 纳入无人机计算链路；Nav2 将移动机器人导航划分为状态估计、环境表示、规划和控制；Autoware 则形成 Sensing、Localization、Perception、Planning、Control 等完整自动驾驶软件栈。[R04](../../references/final-report-reference-index-v0.5.md#r04)[R07](../../references/final-report-reference-index-v0.5.md#r07)[R08](../../references/final-report-reference-index-v0.5.md#r08)

上述事实表明，无人装备的“算力”已经不是单一 AI 推理问题，而是多类工作负载在同一平台上的协同问题。平台选型需要同时处理数据吞吐、计算、内存、实时性、接口、软件和安全约束。

## 1.2 调研目标

本报告重点回答以下问题：

1. 无人装备当前主要智能能力和计算任务是什么；
2. 不同任务对应哪些计算工作负载；
3. 工作负载对 CPU、GPU、NPU、DDR、ISP/VPU、I/O、实时性和功耗提出什么要求；
4. 高集成 SoC、GPU 平台、AI 加速卡、Host+Accelerator 和工业计算机分别适用于什么场景；
5. 当前国内外代表性产品已达到什么水平；
6. 六摄像头无人平台应采用何种架构，并需要哪些工程验证；
7. 公司如何结合密码安全和可信计算形成差异化产品方向。

## 1.3 研究方法

本报告采用需求驱动的技术研究方法，技术链如图 1 所示。

**图 1 端侧智能计算平台调研方法**

```mermaid
flowchart LR
    A["应用场景与任务"] --> B["行业功能栈与技术依据"]
    B --> C["工作负载 W1-W9"]
    C --> D["资源预算<br/>CPU/GPU/NPU/DDR/ISP/I/O"]
    D --> E["时延与并发预算<br/>P95/P99 / Frame Age"]
    E --> F["架构 Gate"]
    F --> G["产品形态与候选平台"]
    G --> H["Benchmark / 工程验证"]
    H --> I["产品定义与研发建议"]
```

图源：[`assets/diagrams/final-report-methodology-evidence-chain-v03.mmd`](../../assets/diagrams/final-report-methodology-evidence-chain-v03.mmd)

平台分析不从某个芯片的 TOPS 倒推应用，而是首先建立 Requirement Vector，包括任务、传感器、数据率、同步、并发、更新率、deadline、内存、接口、SWaP-C、安全与软件要求，再进行架构筛选。

## 1.4 证据规则

报告统一使用以下证据状态：

| 类型 | 含义 |
|---|---|
| FACT | 标准、官方规范或可靠公开事实 |
| SPEC | 官方 Datasheet、Manual、Developer Guide |
| CASE | 已存在的真实产品或系统案例 |
| BENCH | 条件明确的 Benchmark |
| PAPER | 同行评审论文或高质量综述 |
| VENDOR | 厂商公开宣称，尚未独立验证 |
| INFER | 基于事实形成的工程推断 |
| GAP | 当前证据或项目参数不足 |

关键判断优先引用标准、官方文档和论文；产品规格引用具体 SKU，不跨型号继承。

---


## 1.5 端侧、边侧与云侧的部署边界

本报告采用**任务数据与实时闭环的物理位置**来区分部署层级，而不把“边缘计算”当作某一种芯片类型。**端侧（onboard/on-device）**指随无人装备运动、与传感器及飞控处于同一装备上的计算；**边侧（near-edge）**指地面站、车载指控节点、现场通信网关、边缘服务器等与装备近距离通信但并不随该装备本体部署的计算；**云侧**指后方数据中心或云平台。某一地面站对上级云而言也是边缘节点，故部署层级必须随研究对象注明。

| 部署位置 | 优先承担 | 不宜单独承担 | 关键约束 |
|---|---|---|---|
| 端侧/机载 | 传感器时序处理、基本态势感知、状态估计、障碍检测、局部规划、失联安全机制、飞控配合 | 需要大规模历史知识、跨区域多机全局优化的重任务 | SWaP、闭环 P99、同步、掉电/热 |
| 近端边侧/地面站 | 多机监控与任务重分配、跨机数据融合、复杂场景研判、模型缓存与边云代理 | 链路中断时需要毫秒级完成的机体避障 | 带宽、链路可靠性、时钟、权限 |
| 云侧/数据中心 | 训练和模型更新、长期数据分析、跨区域任务优化、复杂知识检索 | 失联情况下必须连续执行的安全控制 | 网络可达性、数据治理、合规 |

**设计原则：**“失联仍需完成”不自动等于“端侧需要大模型”。预定义航线、返航、航点管理、地理围栏和局部重规划，多可由有限状态机（FSM）、行为树（BT）、规则引擎与传统规划完成。大模型需要独立证明其在开放语义任务中的增量收益。[P01][P08]

# 2 无人装备端侧智能功能与应用需求

## 2.1 通用功能链

综合 PX4、Nav2、Autoware 和 Waymo 等成熟系统，可将无人装备核心信息处理过程概括为：

**图 2 无人装备通用功能链**

```mermaid
flowchart LR
    S["Sensing<br/>传感器采集"] --> L["Localization<br/>状态估计与定位"]
    L --> M["Mapping / World Model<br/>地图与世界表示"]
    S --> P["Perception<br/>环境感知"]
    P --> M
    M --> PR["Prediction<br/>跟踪与预测"]
    PR --> PL["Planning / Decision<br/>规划与决策"]
    PL --> C["Control / Execution<br/>控制与执行"]
    MM["Mission / HMI / Fleet"] -.-> PL
    SS["Safety / Security / Health"] -.-> S
    SS -.-> C
```

Waymo 对自动驾驶软件的公开描述“Where am I / What’s around me / What will happen next / What should I do”与上述功能链高度一致。[R10](../../references/final-report-reference-index-v0.5.md#r10)

## 2.2 无人机

无人机应用包括巡检、测绘、监视、物流、搜索救援以及 GNSS 拒止环境自主飞行。其端侧计算特点是 SWaP-C 约束最强，同时对快速运动状态下的同步和闭环时延较为敏感。

在 GNSS 不可靠环境中，VIO 通过 Camera 与 IMU 融合持续估计飞行器位置和姿态；当系统增加障碍检测、局部地图和路径规划后，计算节点即进入完整视觉自主闭环。[R05](../../references/final-report-reference-index-v0.5.md#r05)[R06](../../references/final-report-reference-index-v0.5.md#r06)[R11](../../references/final-report-reference-index-v0.5.md#r11)

## 2.3 UGV/自动驾驶

无人车平台通常具备更高功耗预算，可同时部署 Camera、LiDAR、Radar、GNSS/IMU。Autoware 和 Waymo 表明，高阶 UGV 计算不只包含目标检测，还包括多传感器融合、动态对象预测、BEV/Occupancy 表示以及行为和轨迹规划。[R08](../../references/final-report-reference-index-v0.5.md#r08)[R09](../../references/final-report-reference-index-v0.5.md#r09)[R10](../../references/final-report-reference-index-v0.5.md#r10)

该类系统是 C3 多传感器自主计算的典型代表，对内存容量、带宽、传感器同步和异构计算要求较高。

## 2.4 AMR 与机器人

AMR 核心任务包括定位、地图、全局规划、局部避障和 Fleet 管理。Nav2 的架构表明，状态估计、环境表示、planner 和 controller 在移动机器人中是稳定存在的工程模块。[R07](../../references/final-report-reference-index-v0.5.md#r07)

具身机器人进一步引入 VLM/VLA。PaLM-E、RT-2、OpenVLA 表明视觉、语言、状态和动作可以由大模型统一建模，但 onboard memory、latency 和 safety constraints 仍是端侧部署的主要限制。[R18](../../references/final-report-reference-index-v0.5.md#r18)[R19](../../references/final-report-reference-index-v0.5.md#r19)[R20](../../references/final-report-reference-index-v0.5.md#r20)[R21](../../references/final-report-reference-index-v0.5.md#r21)

## 2.5 USV 与固定边缘设备

USV 的典型特点是 Radar/AIS/Camera/GNSS 多源融合、长航时和复杂目标避碰。[R13](../../references/final-report-reference-index-v0.5.md#r13)

固定式边缘设备虽然没有本体定位和控制，但可能需要 8 路、16 路甚至更多视频并发分析。因此，自主程度与计算量并非同一概念，这也是后续划分 C1 多摄像头智能分析的重要原因。

---


## 2.6 当前典型应用、产品事实与成熟度

本节将**产品已披露能力、可复现开源框架、研究演示、工程推断**分开记录。“产品存在”不能证明在本报告任意传感器组合、任意速度与环境下满足指标。

| 装备/场景 | 已有应用和公开案例 | 端侧主要能力 | 边侧主要能力 | 当前证据定位与限制 |
|---|---|---|---|---|
| UAV：巡检、拍摄与安全航行 | Skydio X10 声明机载视觉导航与障碍规避；ModalAI VOXL 2 提供 VIO、立体深度与避障开发链 | 避障、姿态/定位辅助、检测/跟踪、视频 | 任务下发、监控、媒体归档 | 官方产品/SDK 事实；不同整机功能不能等同通用载板指标 [P02][P03][P04] |
| UAV：现场检测与专项任务 | DJI Manifold 3 可承载第三方 AI 负载；Payload SDK 给出机载视频解码及目标检测开发路径 | 指定类别检测、跟踪、ROI/关键帧、局部记录 | 异常复核、跨时段关联和人机协同 | 平台/SDK 公开；本项目吊舱 ATR 模型准确率和硬件性能未验证 [P05][P06] |
| UAV：GNSS 不可靠自主导航 | PX4 官方架构支持 companion 提供 VIO 与环境/障碍信息 | VIO/状态估计、局部避障与保护 | 地图更新、任务管理、回传 | 开源工程框架；环境和机型条件会显著影响可靠性 [P01][P07] |
| UGV/Robotaxi：道路感知与驾驶 | Autoware 公开 Sensing→Localization→Perception→Planning→Control；Waymo 2026 年说明专用边缘计算处理异构实时负载 | 多传感器定位、检测/预测、规划、车辆控制 | 车队运营、数据闭环、远程支持 | 已有真实系统/开源平台；不能拿其整机功耗与小 UAV 直接比较 [P08][P09] |
| UGV/AMR：室内外自主移动 | Nav2 规划与控制体系、定位建图及避障栈 | 定位、Costmap、局部控制、紧急保护 | Fleet 调度、任务分配、地图服务 | 工程成熟；本体闭环不要求每台机器人都运行 LLM [P10] |
| 多 UAV 协同 | 经典任务分配/编队与地面集中调度；端侧自然语言协同尚以研究与有限示例为主 | 任务执行、局部失联保持、基本状态交换 | 集群态势汇聚、任务重分配、权限管理 | 不宜把研究原型表述为“端侧机群 LLM 已普遍成熟” |

从产品演进看，真正稳定存在的是**感知—定位—规划—控制**计算链和飞控安全分区；开放式 VLM/VLA 更适合描述为新兴扩展方向，而非无人装备智能化的必要前提。汽车高算力系统的数据/冗余预算、机器人慢速局部规划和多旋翼高速小型化，属于不同资源包络，必须单独建模。

## 2.7 按任务场景划分的应用与计算资源画像

| 任务画像 | 传感器与算法实例 | 典型计算瓶颈（不是固定需求门槛） | 必须的部署位置 | 对应工作负载 |
|---|---|---|---|---|
| 图像/视频目标识别 ATR | 1 路或多路 EO/IR 吊舱视频；检测、分类、跟踪、稳像 | 解码/ISP、NPU 推理、目标关联、实时视频带宽；图像质量和算法精度 | 弱网下要求即时告警时优先端侧 | W1+W3+W5 |
| 多目空间感知与避障 | 同步双目/多目、标定/校正、视差或单目深度、障碍地图 | 立体匹配的 CPU/GPU/专用模块、内存访问、同步、端到端 Frame Age | 安全相关环节端侧 | W1+W3（可非 DNN）+W4+W6+W9 |
| GNSS 拒止航行 | Camera+IMU、VIO/SLAM、地图/回环、导航 | CPU/GPU 图优化、时间同步、内存与失败恢复 | 定位和安全控制端侧；重建图可边侧 | W1+W2+W4+W6+W9 |
| 道路/复杂 UGV | Camera/LiDAR/Radar/GNSS/IMU、融合、预测、规划 | 大容量 DDR、传感器 I/O、GPU/NPU、冗余与安全域 | 主闭环车载；运营边侧 | C3 |
| 开放语义巡检与解释 | 关键帧/ROI、VLM、结构化事件、任务建议 | 视觉编码、模型内存、TTFT、Token 生成、可靠性与策略校验 | 可端/边分层，低频/异步 | C2/C3 + W7 |
| 多装备协同 | 状态/任务/地图共享、通信与权限、任务分配 | 通信 QoS、一致性、网络安全、边侧汇聚 | 本地安全端侧；全局协调边侧 | W8 与 C2/C3，W7 可选 |

**重要区分：**目标识别 ATR 回答“画面中是什么/在哪里”，双目避障回答“空间中有什么障碍/距离多远/如何规避”，VIO 回答“我在哪里以及如何运动”，任务规划回答“下一步做什么”。它们的输出变量、更新率、精度与失效后果均不同，不能将任何一个 ATR 检测网络直接当作避障、定位或自主决策算法。

## 2.8 从应用需求推导部署架构的基本原则

本报告建议按“任务风险与实时性→传感器→算法→工作负载→主存/总线/算力/功耗”顺序形成需求卡：首先冻结单个工作链的输入源、输出定义、评价指标、失效策略和数据/控制接口，再决定是否可与其他算法合并部署。通用产品的优先目标不是最大 TOPS，而是在允许的体积和功耗下维持**可测的持续任务性能**。

# 3 工作负载模型 W1～W9

## 3.1 分类依据

W1～W9 是本项目面向硬件资源预算建立的 Workload Taxonomy，并非行业标准或自主能力等级。

其外部功能依据主要来自：

- PX4：VIO、Optical Flow、Collision Prevention；[R04](../../references/final-report-reference-index-v0.5.md#r04)[R05](../../references/final-report-reference-index-v0.5.md#r05)[R06](../../references/final-report-reference-index-v0.5.md#r06)
- Nav2：State Estimation、Environment Representation、Planning、Control；[R07](../../references/final-report-reference-index-v0.5.md#r07)
- Autoware：Sensing、Localization、Perception、Planning、Control；[R08](../../references/final-report-reference-index-v0.5.md#r08)[R09](../../references/final-report-reference-index-v0.5.md#r09)
- Waymo：定位、感知、预测、决策；[R10](../../references/final-report-reference-index-v0.5.md#r10)
- GNSS-denied UAV、USV、多机器人综述；[R11](../../references/final-report-reference-index-v0.5.md#r11)[R12](../../references/final-report-reference-index-v0.5.md#r12)[R13](../../references/final-report-reference-index-v0.5.md#r13)
- PaLM-E、RT-2、OpenVLA 等 Foundation Model/VLA 路线。[R18](../../references/final-report-reference-index-v0.5.md#r18)[R19](../../references/final-report-reference-index-v0.5.md#r19)[R20](../../references/final-report-reference-index-v0.5.md#r20)

W1～W9 的划分遵循五项原则：主导资源不同、时延语义不同、状态生命周期不同、验证方法不同、对架构 Gate 的影响不同。详细定义依据见 [W1–W9 工作负载分类定义依据](../../research/workloads/workload-taxonomy-definition-basis-v1.md)。

## 3.2 分类结果

**图 3 W1～W9 工作负载关系**

```mermaid
flowchart TB
    S["Camera / LiDAR / Radar / IMU / GNSS"] --> W1["W1 传感器输入与视频流水线"]
    W1 --> W2["W2 状态估计与定位"]
    W1 --> W3["W3 深度神经网络感知"]
    W2 --> W4["W4 地图与世界表示"]
    W3 --> W4
    W3 --> W5["W5 跟踪/预测/态势理解"]
    W4 --> W6["W6 规划/优化/决策"]
    W5 --> W6
    W6 --> W9["W9 安全监督与控制接口"]
    W7["W7 Foundation Model / VLM / LLM / VLA"] -.-> W3
    W7 -.-> W6
    W8["W8 多机协同 / Fleet"] -.-> W4
    W8 -.-> W6
```

## 3.3 工作负载定义及主要资源

| ID | 中文名称 | 典型算法/功能 | 主要资源 | 主要评价指标 |
|---|---|---|---|---|
| W1 | 传感器输入与视频流水线 | Camera、ISP、resize、codec、同步、DMA | ISP/VPU、DDR、Camera I/O | Pixel Rate、drop、timestamp jitter |
| W2 | 状态估计与定位 | VO、VIO、GNSS/INS、SLAM 前端 | CPU/GPU、低延迟内存 | latency、精度、同步 |
| W3 | 深度神经网络感知 | Detection、Segmentation、Depth、Pose | NPU/GPU、DDR | latency、FPS、模型覆盖 |
| W4 | 地图与世界表示 | SLAM Map、Costmap、BEV、Occupancy | CPU/GPU、Memory/DDR | map update、memory、latency |
| W5 | 跟踪/预测/态势理解 | MOT、Trajectory Prediction、Scene Understanding | CPU/GPU/NPU、时序状态 | update rate、prediction latency |
| W6 | 规划/优化/决策 | A*、RRT、MPC、Behavior Planning | CPU/GPU | worst-case latency |
| W7 | 基础模型/VLM/LLM/VLA | VLM、LLM、VLA | GPU/NPU、Memory/BW | TTFT、token/s、action latency |
| W8 | 多机协同/Fleet | Task Allocation、Shared Map、Cooperative Perception | Network、CPU/GPU | network QoS、state consistency |
| W9 | 安全监督与控制 | FCU、Supervisor、Failsafe、Health | MCU/RT core/CPU | deadline、jitter、fault isolation |

---

# 4 典型工作负载组合 C1～C5

## 4.1 组合定义

C1～C5 用于描述现实系统中常见的多 workload 并发组合。它们是资源预算模板，不是能力等级。详细来源见 [C1–C5 工作负载组合定义依据](../../research/workloads/workload-composition-definition-basis-v1.md)。

**图 4 C1～C5 关系**

```mermaid
flowchart LR
    C1["C1 多摄像头智能分析<br/>W1+W3+W5"] --> C2["C2 视觉自主系统<br/>W1+W2+W3+W4+W6+W9"]
    C2 --> C3["C3 多传感器自主系统<br/>+W5 / LiDAR / Radar"]
    W7["W7 Foundation Model"] -. 增强 .-> C1
    W7 -. 增强 .-> C2
    W7 -. 增强 .-> C3
    W8["W8 Multi-Agent / Fleet"] -. 协同 .-> C2
    W8 -. 协同 .-> C3
```

图源：[`assets/diagrams/final-report-composition-map-v05.mmd`](../../assets/diagrams/final-report-composition-map-v05.mmd)

## 4.2 C1 多摄像头智能分析

C1 对应固定式视频分析、工业视觉和多摄跟踪系统，主要由 W1、W3、W5 组成。NVIDIA Metropolis 等平台长期面向 multi-camera analytics、tracking 和 inspection，说明此类系统具有明确产业基础。[R47](../../references/final-report-reference-index-v0.5.md#r47)

C1 的特点是视频和 AI 负载可能很重，但不存在本体定位和控制，因此适合视频 SoC、NPU accelerator 和 Host+Accelerator 架构。

## 4.3 C2 视觉自主系统/视觉自主闭环

C2 由 W1、W2、W3、W4、W6 和 W9 组成，对应视觉真正参与导航和运动控制的系统。

PX4 VIO、Collision Prevention、Nav2 以及 Isaac ROS 多摄 VSLAM/Depth/Mapping 均体现这一组合。[R05](../../references/final-report-reference-index-v0.5.md#r05)[R06](../../references/final-report-reference-index-v0.5.md#r06)[R07](../../references/final-report-reference-index-v0.5.md#r07)[R24](../../references/final-report-reference-index-v0.5.md#r24)

六摄像头 UAV 当前基础目标最接近 C2。

## 4.4 C3 多传感器自主系统

C3 在 C2 基础上突出 W5 Prediction/Tracking，并引入 LiDAR、Radar 等多类传感器。Autoware、Waymo 和 USV 多源融合体系均属于该类。[R08](../../references/final-report-reference-index-v0.5.md#r08)[R10](../../references/final-report-reference-index-v0.5.md#r10)[R13](../../references/final-report-reference-index-v0.5.md#r13)

C3 对时间同步、内存带宽、动态预测和多传感器 I/O 要求显著高于 C2。

## 4.5 C4 基础模型增强机器人/无人系统

C4 表示在 C1/C2/C3 基础上叠加 W7。Foundation Model 增加了大模型权重、KV Cache、视觉编码器和生成式推理负载。

C4 不是“更高自主等级”，其价值主要体现在任务理解、语义推理和高层策略增强。

## 4.6 C5 协同自主系统

C5 表示在 C2/C3 上增加 W8，用于 Fleet、多机协同和共享感知。核心新增约束是 Network QoS、distributed state、task allocation 以及 Fleet identity/trust。[R12](../../references/final-report-reference-index-v0.5.md#r12)[R15](../../references/final-report-reference-index-v0.5.md#r15)

---


## 4.7 与伴飞计算机拟议功能的对应关系

本项目不是一个连续从 C1 升至 C5 的“自主等级”。吊舱 ATR 属于 **C1 类感知链的机载变体**（W1+W3+W5）；六目立体避障、自主定位和飞控协同属于 **C2**；增加任务语义 VLM/LLM 属于 **C2+C4**；需要机群数据/任务协调则为 **C2+C5**。C4 与 C5 可同时叠加，但它们不取代 C2 的安全闭环，也不自动形成更高的飞行控制等级。

建议采用三个并行需求向量来计算硬件资源：① ATR 的视频/模型吞吐；② 避障/定位/规划的闭环时效；③ 任务/群控的低频计算与网络状态。并发合并前先分开 Benchmark，避免把模型卡的理论吞吐用于证明整个系统稳定可飞。

# 5 端侧计算资源需求分析

## 5.1 数据吞吐与 Camera Routing

对多摄系统，首先计算像素率：

```text
PixelRate = Σ(N × Width × Height × FPS)
```

但实际 DDR 工作流量还受 RAW/NV12/RGB 格式、ISP 输出、resize、codec、AI 和 recording 读写次数影响。

本报告采用 Camera Routing Set：

```text
C = Capture
V = VIO/SLAM
P = Per-view Perception
F = Fused Multi-view
D = Depth
R = Recording
```

其目的在于区分“物理摄像头数量”和“算法实际消费路数”。

## 5.2 CPU

CPU 主要承担 Linux/ROS 2、驱动、VIO 图优化、tracking、planning、network、storage 等任务。对于 C2/C3，CPU 是核心资源之一，而不是 NPU 的附属处理器。

## 5.3 GPU

GPU 适合 VSLAM、Depth、Point Cloud、BEV、Transformer 和自定义并行算法。GPU 的优势是通用性和软件生态，代价是功耗与散热通常高于专用 NPU。

## 5.4 NPU/AI ASIC

NPU 适合 Detection、Segmentation、Depth 网络和量化 Transformer。真实性能取决于算子覆盖、compiler、precision、dynamic shape 和多模型并发能力。

独立 M.2/PCIe accelerator 只能承担可卸载的 W3/W7，不替代 Host 对 W1/W2/W4/W6 的职责。

## 5.5 Memory/DDR

运行内存需求包括 OS、Runtime、Weights、Activation、Camera Buffer、VIO/SLAM 状态、Map、Queue 和 KV Cache。随着 C4 引入 VLM/VLA，内存容量和带宽的重要性进一步提高。

## 5.6 实时性

闭环反应时间应表示为：

```text
T_reaction =
T_sample + T_sensor/ISP + T_queue + T_perception
+ T_fusion/map + T_planner + T_command + T_vehicle
```

对应反应距离：

```text
D_reaction = speed × T_reaction
```

因此避障平台评价应采用 P95/P99 Frame Age、deadline miss 和热稳态数据，而不是单一模型平均 FPS。

---


## 5.7 典型配置参数化算例与不可忽略的开销

若**假设**六个视频流均与已观测单路 downstream 1072×1280 NV12 相同、全部以 30 FPS 输出，则单份未压缩图像面 payload 为：
`6×1072×1280×30×1.5 = 370,483,200 Byte/s ≈ 370.48 MB/s`。
若 20 FPS 则约 246.99 MB/s。**这只是敏感性分析**：项目目前没有证据证明全部六路的模式/FPS 与该假设一致，更不是 DDR 实际总带宽、MIPI 线速或编码后的存储写入速度。项目已有数据参见 `data/calculations/six-camera-observed-mode-sensitivity.csv`。

当 Camera frame 同时送 ATR、图像拼接、双目深度与录像时，完整帧读写次数、色彩转换、ROI 裁剪、NPU 输入复制及 cache miss 才是性能瓶颈来源之一。建议同时统计每条模型链的调用速率 `Calls/s`、每个算力引擎的占用 `Σ(Rate_i×ServiceTime_i)`，并用 trace 测量 P95/P99 与新鲜度，拒绝仅依据模型单次 FPS 结论。

对双目匹配而言，视差搜索范围和图像输出尺寸直接决定代价；深度由焦距、基线和视差关系决定（`Z=fB/d`）。由于深度不确定度会随距离增加而变大，双目能否探测到满足速度需求的远距离障碍，应优先由**光学基线与误差预算**验证，而不是先求提升 NPU TOPS。[P11]

# 6 端侧计算技术路线

## 6.1 高集成 SoC/SoM

CPU、GPU/NPU、ISP/VPU 和 I/O 集成于同一 SoC 或模块，具有数据路径短、共享内存和 SWaP 优势，适合无人机、AMR 和小型机器人。

典型代表包括 RK3588、BM1688、Atlas 200I A2、IQ-9075。

## 6.2 GPU 机器人计算平台

以 Jetson Orin 为代表，具有 GPU 通用并行计算能力和 CUDA/TensorRT/Isaac ROS 软件生态，适合 C2/C3/C4 的多 workload 混合部署。

## 6.3 独立 AI Accelerator

以 LQ50、Metis、Hailo-10H 等为代表，通过 M.2/PCIe 接入 Host，适合增加 W3/W7 推理能力。

## 6.4 Host + Accelerator

Host 负责 Camera、ISP、CPU workload 和规划，Accelerator 负责 DNN/大模型。Firefly AIBOX PRO 表明该路线已经产品化。[R37](../../references/final-report-reference-index-v0.5.md#r37)

## 6.5 实时控制器 + Companion Computer

FCU/MCU 负责姿态和执行机构实时控制，Linux AI Computer 负责感知、SLAM 和规划。该架构可降低 AI/Linux 抖动对硬实时控制的影响。

## 6.6 工业机器人计算机与车规 Physical AI SoC

工业计算机侧重 GMSL/CAN、宽压、工业温度和长期运行；车规 SoC 则强调高算力、多传感器、安全岛和自动驾驶/Physical AI。

二者对 UGV/USV/AMR 具有较强参考意义，但不应直接作为小型 UAV 候选。

**图 5 端侧智能计算产品形态**

```mermaid
flowchart TB
    A["端侧智能计算产品形态"] --> B["高集成 SoC / SoM"]
    A --> C["GPU Robotics Platform"]
    A --> D["独立 AI Accelerator"]
    A --> E["Host + Accelerator Box"]
    A --> F["工业/机器人整机"]
    A --> G["车规 / Physical AI SoC"]
    B --> B1["RK3588 / BM1688 / Atlas / IQ-9075"]
    C --> C1["Jetson Orin / Thor"]
    D --> D1["LQ50 / Metis / Hailo-10H"]
    E --> E1["Firefly AIBOX PRO"]
    F --> F1["Seeed / Advantech"]
    G --> G1["Journey 6 / A2000"]
```

图源：[`assets/diagrams/final-report-product-landscape-v05.mmd`](../../assets/diagrams/final-report-product-landscape-v05.mmd)

---


## 6.7 伴飞计算机的技术边界

伴飞计算机（Companion Computer / Mission Computer）与飞行控制器（FCU）是**逻辑职责分工**，并不要求必须是两块 PCB。PX4 明确：飞控执行基础飞行与安全功能，Linux 侧承担更复杂的视觉、任务和网络软件，通常通过 MAVLink/uXRCE-DDS 等交换状态与高层命令；ModalAI/Auterion 也展示了集成在一块板/模块中的产品形态。[P01][P02][P12]

面向本项目，建议采用“飞控独立安全控制域 + RK3588 视觉伴飞计算域 + 可选 M.2 推理扩展 + 认证授权/安全监控域”的模块化技术路线。ATR、双目深度和任务管理可部署在一个机载计算板上，但必须区分实时优先级、故障影响域与数据隔离。不建议在初始设计中把外接加速卡加入飞控关键闭环的必要路径，除非有系统级故障恢复和 P99 证据。

# 7 国内外现有端侧智能计算产品调研

## 7.1 调研范围与分类原则

产品调研不是对芯片 TOPS 进行排序，而是分析当前市场是否已经形成可采购、可集成和可产品化的计算形态。

本报告区分：

1. SoC/SoM/核心板；
2. GPU Robotics Platform；
3. M.2/PCIe 独立 AI Accelerator；
4. Host+Accelerator 异构计算盒；
5. 工业/机器人整机；
6. 车规/Physical AI SoC。

2026-10-08 对关键官方产品页面再次复核，主要规格与 9 月底产品数据库一致。复核记录见 [产品公开资料复核](../../references/webpages/product-refresh-2026-10-08.md)。

## 7.2 高集成 SoC/SoM

### 7.2.1 NVIDIA Jetson AGX Orin

Jetson AGX Orin 64GB 是当前机器人和自主系统中具有代表性的 GPU SoM。官方规格给出最高 275 TOPS、64GB LPDDR5、约 204.8GB/s 内存带宽，模块功耗档位 15～60W，并同时提供 Arm CPU、Ampere GPU、DLA、视频编解码和高速 I/O。[R35](../../references/final-report-reference-index-v0.5.md#r35)

其工程价值主要在于 CUDA、TensorRT 和 Isaac ROS 软件生态。Isaac ROS 已提供 Visual SLAM、Depth、Mapping 等组件和系统级 Benchmark。[R22](../../references/final-report-reference-index-v0.5.md#r22)[R23](../../references/final-report-reference-index-v0.5.md#r23)[R24](../../references/final-report-reference-index-v0.5.md#r24)

**工程判断：** Jetson Orin 适合 C2/C3/C4，特别适合算法快速演进和复杂 GPU workload，但对小型 UAV 需要重点评估模块、载板、散热器和电源后的整机 SWaP。

### 7.2.2 Qualcomm Dragonwing IQ-9075

IQ-9075 是面向工业 AI、AMR 和 Drone 的高集成异构 SoC。官方当前给出 50/100 Dense INT8 TOPS、最高 36GB LPDDR5 ECC、最多 16 路 Camera、8 核 Kryo CPU、Adreno GPU、Hexagon NPU，以及独立 4 核实时子系统。[R36](../../references/final-report-reference-index-v0.5.md#r36)

该平台同时具备 PCIe Gen4、2.5GbE TSN、CAN-FD 和 Linux/Ubuntu 支持，体现出“机器人 SoC”向 AI + RT + I/O 一体化发展的趋势。

**工程判断：** IQ-9075 对 C2/C3 很有吸引力，尤其适合多摄像头和实时协同。但“最多 16 Camera”属于 SoC capability，不能直接等同具体板卡能无桥接支持本项目六摄同步模式；Full-stack P99 仍需实测。

### 7.2.3 RK3588

RK3588 是国内低成本端侧 AI 平台的重要代表，具备 4×Cortex-A76 + 4×A55、Mali-G610 GPU、6 TOPS NPU、ISP 和 8K 视频能力。其优势是成本、生态和大量现成板卡。

当前公开证据已覆盖官方 DNN Benchmark 和部分 SLAM 论文，但多 Camera + VIO + DNN + Planner 的并发系统性能仍缺统一公开数据。

**工程判断：** RK3588 更适合作为 C1、轻量 C2 和 Host+Accelerator 的 Host。对六摄 UAV 不应因“6 TOPS 较低”直接排除，也不能因“支持多 Camera”直接判定满足 C2。

### 7.2.4 Huawei Atlas 200I A2

Atlas 200I A2 是国产高集成边缘模块，官方给出 20 TOPS INT8、10 TFLOPS FP16、4/8/12GB LPDDR4X ECC、ISP/视频、PCIe/Ethernet/MIPI/SATA/USB/CAN，20 TOPS 版本典型功耗约 25W，尺寸约 82×60×7mm。[R41](../../references/final-report-reference-index-v0.5.md#r41)

官方应用明确包含机器人和无人机。

**工程判断：** Atlas 200I A2 适合作为国产 C1/C2/C3 候选，但需要重点评估 CANN/MindSDK 软件迁移成本、ROS/算法生态和项目所需 Camera 同步能力。

### 7.2.5 BM1688 / Firefly AIO-1688JD4

Firefly BM1688 板级方案公开给出 16 TOPS INT8、4 TFLOPS FP16/BF16、16 路 1080p30 解码、10 路 1080p30 编码，并明确支持 6-channel sensor input 和 ISP。[R42](../../references/final-report-reference-index-v0.5.md#r42)

**工程判断：** 这是当前调研产品中与六摄像头 W1 最直接相关的国产板级方案之一。其“6 路 sensor input”属于很强的 Camera 侧事实证据，但并不能直接证明六路项目模式下的同步、VIO 和 C2 并发能力。

## 7.3 独立 AI Accelerator

### 7.3.1 Houmo LQ50

LQ50-24GB 是基于 M50 的 M.2 2280 加速卡，官方给出 160 TOPS、100 TFLOPS@bFP16、24GB LPDDR5/LPDDR5X、153.6GB/s、PCIe Gen4 x4、典型 13W、约 9g。[R38](../../references/final-report-reference-index-v0.5.md#r38)

较大的板载内存使其具备 W3 和 W7 的潜力，特别适合向已有 Host 增加大模型和视觉推理能力。

**工程判断：** LQ50 是“Host+国产高算力 Accelerator”路线的重要代表，但 160 TOPS 只说明卡本身 AI 计算能力。Camera/ISP、VIO、Map、Planner 和 FCU 接口仍由 Host 承担。

### 7.3.2 Axelera Metis

Metis M.2 产品最高约 214 TOPS，支持 Arm Host，适合计算机视觉推理。其优势是较高能效和可嵌入性。[R39](../../references/final-report-reference-index-v0.5.md#r39)

**工程判断：** 适合作为 W3 专用卸载引擎，但需要将散热器、Host slot power、PCIe 和 Host CPU/DDR 纳入整机评估。

### 7.3.3 Hailo-10H

Hailo-10H M.2 提供 40 TOPS INT4/20 TOPS INT8，并配置 4GB/8GB 板载内存，面向 CV 和端侧生成式 AI。[R40](../../references/final-report-reference-index-v0.5.md#r40)

厂商不同材料对典型功耗存在 <2.5W 和 <3.5W 的条件差异，因此报告不将其合并为单一精确功耗。

**工程判断：** Hailo-10H 适合低功耗 W3/W7 扩展，但仍依赖 Host 完成机器人完整计算链。

## 7.4 Host+Accelerator 与整机产品

### 7.4.1 Firefly AIBOX PRO

AIBOX PRO 采用 RK3588/RK3576 Host，并提供双 M.2 accelerator slot，官方支持后摩 LQ50、RK1828、DeepX DX-M1 等卡，整机提供双 GbE、CAN-FD、RS485、DI/DO 和 9～36V 输入。[R37](../../references/final-report-reference-index-v0.5.md#r37)

其意义在于证明：

> **Host+Accelerator 已经从架构概念进入完整商业产品阶段。**

当前公开资料中 Firefly 对某 LQ50 配置的内存表述与后摩 LQ50-24GB 当前官方指南存在差异，因此 exact accelerator SKU 仍标记为未确认。

**工程判断：** 该路线适合 C1、W3/W7 扩展，并可作为 C2 候选，但必须实测 Camera→Host→PCIe→Accelerator→Host→Planner 的完整 E2E 时延。

### 7.4.2 Seeed reComputer Robotics / Industrial

Seeed reComputer Robotics/Industrial 系列基于 Jetson Orin NX/Nano，并集成 Ethernet、CAN、串口等机器人接口；部分 Robotics 型号提供 GMSL 摄像头能力。[R43](../../references/final-report-reference-index-v0.5.md#r43)

**工程判断：** 该产品形态比 Developer Kit 更接近实际机器人整机，适合 UGV、USV、AMR。已公开 Robotics 产品重量约 1kg 级，对小型 UAV 通常过重。

### 7.4.3 Advantech MIC-733-AO

MIC-733-AO 是基于 Jetson AGX Orin 的工业 AI 计算机，支持 4×GbE、可选 PoE、可选 2 路 GMSL、9～36V、fanless，整机重量约 4.5kg。[R44](../../references/final-report-reference-index-v0.5.md#r44)

**工程判断：** 该产品展示了工业级“芯片→整机”的产品化路径，适合固定边缘、UGV 和工业机器人，但显然不属于小型 UAV SWaP 范围。

## 7.5 车规/Physical AI 平台

### 7.5.1 Horizon Journey 6

Journey 6 系列面向高阶辅助驾驶和智能驾驶。Journey 6M 公开算力约 128 TOPS，并拥有面向车载多传感器和 E2E 的软硬件生态。

**工程判断：** Journey 6 说明国产车规 SoC 已形成较高成熟度的 C3 路线，但其产品形态、接口和开发流程面向车载，不宜直接与无人机 SoM 横向比较。

### 7.5.2 Black Sesame A2000

2026 年官方公开的 A2000N/L/U/X 家族覆盖约 200～1000 TOPS，支持 INT4/INT8/FP8/FP16/FP32，采用近存计算和自研 ISP，并面向 Physical AI、L3/L4 和机器人方向。

**工程判断：** A2000 体现下一代车规/Physical AI SoC 的技术趋势：大算力、混合精度、近存计算、VLM/VLA 和功能安全深度集成。1000 TOPS 属于家族最高规格，不能用于代表全部 A2000 SKU；其对小型 UAV 的 SWaP 和可采购性需要单独评估。

## 7.6 代表产品横向对比

原始数据：[`data/product-specs/final-report-representative-products-v05.csv`](../../data/product-specs/final-report-representative-products-v05.csv)

| 平台/产品 | 形态 | 主要算力/内存 | Camera/视频特点 | SWaP 特点 | 更适合的场景 | 主要未验证项 |
|---|---|---|---|---|---|---|
| Jetson AGX Orin | GPU SoM | 275 TOPS；64GB；204.8GB/s | MIPI CSI、视频、Isaac ROS | 15～60W | C2/C3/C4 | 小型 UAV 整机 SWaP |
| IQ-9075 | Robotics SoC | 50/100 TOPS；36GB ECC | up to 16 Camera；RT subsystem | SoC 3.8～20W | C2/C3/C4 | 本项目六摄同步、Full-stack P99 |
| RK3588 | SoC | 6 TOPS；板级内存 | ISP+8K视频 | 低成本、板型多 | C1、轻量 C2、Host | 多 workload 并发 |
| Atlas 200I A2 | 国产模块 | 20 TOPS；4/8/12GB | ISP/视频/多 I/O | 25W；82×60mm | C1/C2/C3 | 软件迁移、Camera sync |
| BM1688 | 国产视觉 SoC | 16 TOPS | 6 sensor input；多路 codec | 板级 | C1、六摄 W1 候选 | C2 软件/并发 |
| LQ50 | M.2 Accelerator | 160 TOPS；24GB | Host dependent | 13W；约9g | W3/W7 offload | Host+PCIe E2E |
| Metis | M.2 Accelerator | up to 214 TOPS | Host dependent | 低功耗 accelerator | W3 offload | 散热、Host path |
| Hailo-10H | M.2 Accelerator | 40 TOPS INT4；4/8GB | Host dependent | 低功耗 | W3/W7 | 系统级闭环 |
| AIBOX PRO | 异构整机 | RK Host + dual M.2 | Host media + accelerator | 160×111×61mm | C1/C4；C2候选 | Camera/VIO/P99 |
| reComputer Robotics | 机器人整机 | Orin NX | GMSL/CAN 等 | 约 kg 级 | UGV/USV/AMR | 小型 UAV 重量 |
| MIC-733 | 工业整机 | AGX Orin | 4GbE/可选GMSL | 4.5kg | 工业/UGV | 不适小型 UAV |
| Journey 6M | 车规 SoC | 128 TOPS | 车载多传感器 | 车规 | C3 | 非 UAV 产品形态 |
| A2000 family | Physical AI SoC | 200～1000 TOPS family | ISP/车载接口 | 车规 | C3/C4 | SKU、SWaP、可采购性 |

## 7.7 产品调研结论

现有产品调研形成以下结论：

1. **一体化 SoC/SoM 仍是小型无人装备优先路线。** 其优势在于 Camera、ISP、DDR 和计算引擎处于同一内存域，数据路径短，SWaP 较容易控制。
2. **独立 Accelerator 的价值主要是 W3/W7 扩展。** 其 TOPS 不能替代 Host 的 Camera、VIO、Planning 和实时控制能力。
3. **Host+Accelerator 已经形成成熟商业形态。** Firefly AIBOX PRO 是典型例证，但该路线的系统瓶颈从“卡算力”转移到 Host、PCIe、预后处理和散热。
4. **工业整机已具备机器人接口和可靠性设计。** 但重量和体积决定其主要面向 UGV、USV、AMR，而非小型 UAV。
5. **车规/Physical AI SoC 正向高算力、多模态和实时/安全融合发展。** 其技术趋势值得跟踪，但不能直接作为 UAV 产品选型结论。
6. **国产产品已经覆盖 SoC、模块、Accelerator 和整机多个层次。** 当前主要缺口不是“没有算力”，而是 ROS/VIO/多 workload 并发、P95/P99 和完整系统 Benchmark 的公开证据不足。

---


## 7.8 已有无人机伴飞计算机与整机级实现案例

补充本节旨在回答“机载任务计算”是否已有成熟设计，并与第 7.2—7.6 节的**计算芯片/模组/加速卡**形成不同层级的比较。

| 产品/案例及形态 | 官方披露的用途/配置要点 | 可借鉴的技术路线 | 不可直接外推的内容 |
|---|---|---|---|
| **ModalAI VOXL 2**（融合飞控与任务计算的板级平台） | QRB5165、15 TOPS（厂商规格）、8GB LPDDR5、公开 6 路并行图像输入、16g 板级标称；VOXL SDK 含 VIO/SLAM/双目深度/避障 | 多 Camera + CV 算法 + FCU 工程整合；VOXL Vision Hub 可从立体深度点云生成 PX4/ArduPilot 障碍消息 | 16g 不含本项目相机/壳体/供电；厂商能力不等于六路完整闭环实测 [P02][P03] |
| **Auterion Skynode X**（飞控+任务计算+通信模块） | 官方描述集成飞控、Mission Computer 与 LTE；开放视觉 SDK 面向导航/视觉扩展 | 控制—任务—网络平台化、模块式应用开发 | 官方宣传的功能可能为接口和 SDK 可实现性，不能等同特定 ATR/六目部署实测 [P12] |
| **DJI Manifold 3**（外挂机载算力计算机） | 官方标称最高 100 TOPS INT8 **稀疏模型**、16GB LPDDR5、额定 33W、约 120g、98×57×36mm | 机载计算与飞控/吊舱分体、通过开放接口扩展感知算法 | 100 TOPS 不可当密集 INT8 性能；整机系统功率不等于该模块 33W；平台兼容范围应看官方 [P05][P06] |
| **Skydio X10**（完整无人机系统） | 官方发布视觉避障、弱 GNSS 环境辅助自主和任务执行能力 | 系统层证明多传感器视觉自主可形成产品能力 | 不能反向推出使用哪张商用算力卡、算法具体 FPS、模型参数量 [P04] |
| **RK3588 + M.2 AI Accelerator**（Host+Accelerator 通用盒子方案） | 已有 Firefly AIBOX PRO 类 Host+M.2 商业形态；并非已经验证的六目飞行设备 | 主板实现 Camera/ISP/VIO/规划，独立卡承担适合的 DNN/VLM | 扩展卡的 TOPS 不替代视频、定位、实时控制与板级载荷认证；需要 H2D/D2H 和功耗实测 [R37] |

**工程判断：**现成“硬件+基础软件”的自主视觉平台较成熟，但“指定机头相机配置 + 吊舱 ATR + 双目避障 + 编队指控 + 商密可信”的完整组合产品尚**未在本次调研中获得同配置可复现证据**。竞争力的重点应放在系统集成、可复用视觉算法、性能验证、失效处理和信任管理，不宜把外挂算力卡当作核心卖点。

# 8 安全可信端侧智能计算架构

## 8.1 设计需求

无人装备具有无人值守、网络不稳定、设备可能被获取、任务数据和模型敏感等特点，因此安全应从设备启动、运行、通信、升级到失陷处置形成完整链路。

## 8.2 三平面架构

**图 6 安全可信无人智能计算平台总体架构**

```mermaid
flowchart TB
    G["地面/集群可信服务<br/>CA / KMS / Verifier / Policy / OTA"] --> T
    subgraph NODE["安全可信无人智能计算节点"]
      T["Trust Plane<br/>RoT / TEE / TPM-TCM / SE<br/>Identity / Key / Measurement / Attestation"]
      C["Compute Plane<br/>CPU / GPU / NPU / ISP / VPU<br/>ROS2 / VIO / SLAM / DNN / VLM / Planner"]
      R["Real-Time Plane<br/>FCU / MCU / RTOS / Safety Supervisor"]
      T --> C
      T --> R
      C <--> R
    end
    S["Camera / LiDAR / Radar / IMU"] --> C
    R --> V["Vehicle / Actuator"]
```

Compute Plane 负责智能计算；Real-Time Plane 负责确定性闭环；Trust Plane 负责设备、软件、模型和密钥的可信状态。

## 8.3 国内标准依据

国产 Trust Plane 可形成如下标准链：

- GB/T 38638-2020：可信计算体系结构；[R48](../../references/final-report-reference-index-v0.5.md#r48)
- GB/T 29829-2022、GM/T 0011-2023：可信密码支撑平台；[R49](../../references/final-report-reference-index-v0.5.md#r49)[R50](../../references/final-report-reference-index-v0.5.md#r50)
- GM/T 0012-2020：可信密码模块接口；[R51](../../references/final-report-reference-index-v0.5.md#r51)
- GM/T 0013-2021：TCM 接口符合性测试；[R52](../../references/final-report-reference-index-v0.5.md#r52)
- GM/T 0058-2018：TCM 服务模块接口；[R53](../../references/final-report-reference-index-v0.5.md#r53)
- GM/T 0079-2020：可信计算平台直接匿名证明；[R54](../../references/final-report-reference-index-v0.5.md#r54)
- GM/T 0082-2020：可信密码模块保护轮廓；[R55](../../references/final-report-reference-index-v0.5.md#r55)
- GM/T 0028-2024：密码模块安全要求；[R56](../../references/final-report-reference-index-v0.5.md#r56)
- GM/T 0132-2023：信息系统密码应用实施指南；[R57](../../references/final-report-reference-index-v0.5.md#r57)
- GM/T 0115-2021：信息系统密码应用测评要求。[R58](../../references/final-report-reference-index-v0.5.md#r58)

SM2、SM3、SM4 国家标准可分别支撑设备身份/签名、完整性度量和数据保密。[R59](../../references/final-report-reference-index-v0.5.md#r59)[R60](../../references/final-report-reference-index-v0.5.md#r60)[R61](../../references/final-report-reference-index-v0.5.md#r61)

## 8.4 Trust Plane 能力建议

| 能力 | 技术实现方向 |
|---|---|
| 设备身份 | SE/TCM/TEE + SM2 certificate/key |
| Secure Boot | BootROM/eFuse/签名链 |
| Measured Boot | TCM/TPM/PCR-like measurement |
| Remote Attestation | Attester–Verifier–Relying Party |
| Secure Storage | TEE/SE/TCM sealed key + encrypted storage |
| AI Artifact Trust | 模型/配置签名、hash、版本、授权 |
| Communication Security | ROS 2 DDS Security、TLS/IPsec、MAVLink signing 等 |
| Secure OTA | 签名、版本、防回滚、恢复 |
| Capture Response | Debug lock、key revoke、fleet isolate |
| Domestic Crypto | SM2/SM3/SM4/TRNG + GM/T 接口/测评 |

---

# 9 伴飞计算机与六摄像头无人平台 Case Study

## 9.1 伴飞计算机产品定义与本案例的边界

本项目规划中的“伴飞计算机”应定位为**任务/视觉计算平台**：接入机头多目相机与外部吊舱处理结果，完成需要机载执行的视觉处理及局部自主功能，并向现有 FCU 输出经检查的高层感知/规划信息。其职责不是替代 FCU，也不是默认承接全部吊舱视频、全部机载网络、全部机群决策。

必须首先确定**吊舱 ATR 已由独立 RK3588 节点执行**这一系统分工是否保持。如果 ATR 在独立单元已有算法和算力能力，伴飞计算机只需消费带时间戳的结构化目标/轨迹数据，无须再传输/推理全量原始视频；若要求伴飞计算机统一承担 ATR，应重新核算 Camera、视频解码、NPU 资源与链路时延。该差异会直接改变是否需要 M.2 卡及主控内存预算。

### 基础方案的逻辑部署

```text
[机头六摄像头 + IMU] -> 采集/同步/ISP -> (选定双目) 标定/校正/立体匹配 -> 深度/障碍地图
                                  |                |                                   |
                                  +-> 选定视角感知/融合 --> 局部规划/安全仲裁 --------> [FCU]
                                  |
[吊舱 EO/IR] -> [独立 ATR RK3588?] -> 时间戳目标/跟踪结果 ---------------> 任务管理器
                                  |
[地面/边侧指控] <-> 认证通信 <-> 任务管理器 <-> 白名单行为/安全仲裁
                                  ^
                [可选 M.2 VLM/LLM] -> 低频语义事件/任务建议
```

上图是工程部署**候选而非已实现系统**。问号代表尚需澄清的模块边界。



## 9.2 需求状态

当前已确认六路 Camera，单路 downstream 已观测 1072×1280 NV12；实际 FPS、六路模式一致性、N_detection、N_vio、N_depth、N_record、飞行速度、探测距离和 SWaP 仍需冻结。

## 9.3 需求—Workload—资源—候选架构

**图 7 六摄像头项目技术推导链**

```mermaid
flowchart LR
    R["6 Camera / FPS / Sync<br/>Speed / Range / SWaP"] --> WR["Camera Routing<br/>C/V/P/F/D/R"]
    WR --> W["W1/W2/W3/W4/W6/W9"]
    W --> RES["ISP/VPU<br/>CPU/GPU/NPU<br/>DDR<br/>P99 Frame Age"]
    RES --> G{"Architecture Gate"}
    G --> A1["Integrated SoC<br/>RK3588/BM1688"]
    G --> A2["GPU SoM<br/>Jetson Orin"]
    G --> A3["Robotics SoC<br/>IQ-9075"]
    G --> A4["Host + Accelerator<br/>RK3588 + LQ50/Metis/Hailo"]
    A1 --> B["Unified Benchmark"]
    A2 --> B
    A3 --> B
    A4 --> B
```

图源：[`assets/diagrams/six-camera-requirement-resource-architecture-v03.mmd`](../../assets/diagrams/six-camera-requirement-resource-architecture-v03.mmd)

## 9.4 图像数据量敏感性

按 1072×1280 NV12、6 路计算：

| FPS | 六路 Pixel Rate | 一份 NV12 Payload |
|---:|---:|---:|
| 10 | 82.33 MP/s | 123.49 MB/s |
| 20 | 164.66 MP/s | 246.99 MB/s |
| 30 | 246.99 MP/s | 370.48 MB/s |
| 60 | 493.98 MP/s | 740.97 MB/s |
| 120 | 987.96 MP/s | 1481.93 MB/s |

上述仅为单份 image-plane 数据，不是 DDR 实测。实际系统还存在 ISP 写入、resize、DNN、录像和多 consumer fan-out。

## 9.5 候选架构分析

### 一体化 RK3588/BM1688

优势是成本、集成度和短数据路径；BM1688 具有 6-channel sensor input 公开规格。主要风险是 C2 场景下 VIO+DNN+Planning 的完整并发性能和 ROS/工具链成熟度。

### Jetson Orin

优势是 GPU 与 Isaac ROS，特别适合 VSLAM、Depth、Mapping 和多模型并发。风险是功耗、载板、散热和重量。

### IQ-9075

优势是多 Camera、36GB ECC、NPU、GPU 和独立实时子系统一体化。风险是本项目 exact Camera/同步和系统 P99 尚未实测。

### RK3588 + Accelerator

优势是把 W3/W7 从 Host 卸载，并可形成不同算力档位。主要风险是 PCIe 数据搬运、Host DDR、散热和系统 E2E latency。

## 9.6 推荐验证顺序

1. 六路同步采集和稳定性；
2. 六路 Camera + 录像/编码；
3. VIO/SLAM；
4. Detection/Depth；
5. VIO + Detection 并发；
6. Camera + VIO + Detection + Depth + Planner；
7. P50/P95/P99 Frame Age；
8. 30min/1h/2h thermal；
9. FCU 闭环；
10. Trust Plane 启动、模型、通信、OTA 验证。

---


## 9.7 吊舱图像 ATR：应用链路与资源边界

ATR（Automatic Target Recognition，在本报告中按“自动目标检测、分类和识别”统称）应限定在**非武器化感知/巡检和态势辅助**边界内，不能把模型类别预测当作可以直接执行的控制命令。首先区分：对象检测（框与类别）、细粒度识别（类别细分或设备资产身份）、多目标跟踪（连续 ID/轨迹）、跨可见光/红外融合（EO/IR 视角时间匹配）。这些能力所需模型和标注数据不同，不能仅凭“YOLO 可运行”认定完整 ATR 可用。

**推荐的资源预算卡**：1）视频源格式/分辨率/FPS、云台转动/稳定与时间戳；2）ROI/full-frame 输入大小；3）检测、分类、跟踪的模型与触发频率；4）INT8/FP16 量化后指标与端到端 Frame Age；5）恶劣光照/雨雾/遮挡/视角变化的准确率、漏检率和误警率；6）数据结果需要回传给谁。若吊舱现有独立 RK3588 承担 ATR，则本伴飞计算板新增的是**信息接入/融合负载**，不是完整模型负载。只有证实现有单元成为瓶颈，才进行“集中合并 ATR”架构评估。

本项目 ATR 具体模型、数据集、分类层级、最低准确率、夜间/红外表现、跨平台移植等均为 **GAP**。DJI Payload SDK 的机载视频处理/检测示例只证明开发路径存在，不能代替上述验收证据。[P06]

## 9.8 双目测距与避障：从几何条件到闭环指标

双目避障不能简单理解为“两台相机把图像丢给 6 TOPS NPU 计算距离”。经典 StereoSGBM 是**基于半全局匹配思想的视差估计算法**，主要消耗 CPU SIMD/多核、内存读写，亦可研究 GPU 优化或专用硬件替代；不以 NPU 峰值 TOPS 作为首要性能判断。

**光学链：** 采用有稳定基线的**同向重叠视场、严格同步**双目，离线标定内外参并校正图像，再由视差 `d` 求深度 `Z=fB/d`。若六相机采用前后左右分散环视布局，**并不天然形成三组可用双目**；必须核对对应成对相机的重叠视场、基线、同步、快门类型、帧时差、曝光与动态场景的匹配能力。图像拼接、环视覆盖与用于精密测距的双目几何要求并不相同。[P11]

**避障链：** 深度置信度与可见区域 → 障碍点云/栅格 → 局部安全域 → 安全速度/航迹建议 → FCU 执行。需要校验无纹理物体、玻璃/反光、逆光、运动模糊、远距离低视差、细线缆及夜间效果。PX4 Collision Prevention 可接收 companion 的障碍物距离信息；但其官方页面也提示 companion 实现有“未维护/未验证”的部分，故不能将接口存在写成现成即插即用的六目自主避障系统。[P07]

闭环关键不是单帧 StereoSGBM 的运行时间。沿用第 5.6 节 `T_reaction` 和实际速度、可用探测距离、留置安全距离、机体响应模型反推预算，并记录 Frame Age P95/P99、失帧、异常距离时的降级行为。**仅探测到障碍 ≠ 已实现自主绕障**：后者还需要地图、规划、规划结果仲裁及 FCU 接口与安全策略。

## 9.9 机载自主任务与多机协同：LLM 是否必要

应把三类实际问题区分处理：

| 问题 | 无 LLM 的基线 | 可能存在的 VLM/LLM 增量价值 | 目前判断 |
|---|---|---|---|
| 通信中断后沿已知任务继续、返航、等待、重连 | FCU failsafe + FSM/BT + 航点/局部规划 | 对已定义任务通常没有必需性 | **优先无需 LLM** |
| 根据已知故障/安全规则重新分配有限任务 | 规则、有限集合优化、拍卖/分布式任务分配、边侧调度 | 自然语言解释/任务建议 | **先建确定性对照组** |
| 未知情境的开放语义理解、自然语言任务转结构化动作 | 规则式方法覆盖率可能不足 | 事件关键帧 VLM、语言任务分解、低频解释 | **满足任务收益与安全门槛后选择性启用** |
| 对多机群实时“指挥控制” | 地面/边侧 C2、身份/权限、通信协议、状态一致性 | 辅助人机交互与任务复核 | **不能由单机 LLM 直接代替完整指控** |

大模型不应占用 FCU 的硬实时控制权限；建议使用“VLM 提议 → 结构化语义事件 → Mission Manager / BT / FSM → 安全仲裁 → 现有路径规划与 FCU”的路径。模型超时、幻觉或卡掉电不得影响避障基础任务。机载资源不宜持续把六路原始 30 FPS 图像喂给 VLM，优先研究**事件触发关键帧/ROI + 已结构化感知状态**。这既能节省图像 token、内存和 PCIe 带宽，也把语义计算和实时安全闭环解耦。详见仓库 `cases/six-camera-uav/mission-intelligence-llm-vlm-architecture-2026-10.md`。

已有 Rockchip 官方 RK3588 Qwen3-VL-2B W8A8 性能表：文本阶段 decode 约 14.98 tokens/s；另列 448×448 图片编码约 2.08 秒、prefill 约 649 ms。三项是不同阶段/配置的公开锚点，**不能合并为项目端到端实测或图像实时帧率**；即使没有并发，也说明这一量级的模型不适合作为几十毫秒级避障主链。[P13]

后摩 LQ50/M50 的 160 TOPS、24GB 板载内存与 PCIe Gen4 x4，说明可研究相对独立的 W7 推理卸载，但不能保证 RK3588 六摄、双目、VIO、任务调度同时运行所需的端到端响应和整机功耗。本报告保留一体 SoC、独立 ATR 节点、RK3588+M.2 三种分工；**先论证附加卡带来的任务收益，再选择型号**。

## 9.10 伴飞计算机候选分工与阶段性研发建议

| 路线 | 机头六摄/双目深度 | 吊舱 ATR | 任务管理/协同 | 初期优先验证 | 评估状态 |
|---|---|---|---|---|---|
| A：RK3588 单 SoC + 外部 FCU | 由 RK3588 CPU/GPU/ISP 为主处理，NPU 可执行所需检测 | 优先保留原独立 ATR 单元 | FSM/BT + 轻量通信 | 六路接入、StereoSGBM/VIO、P99、热 | **首选基线 / INFER** |
| B：RK3588 + M.2 Accelerator + FCU | 避障实时链仍在 Host | 保留独立，或按真实资源整合 | M.2 优先尝试低频 VLM 或特定 DNN 卸载 | H2D/D2H、SDK 固件、功耗、VLM 共运行不干扰 | **扩展候选 / GAP** |
| C：成熟机器人 GPU/SoM + FCU | GPU/ISP/VSLAM 能力与现成 ROS 工具链较完整 | 可整合但需重测 | 高级任务/VLM 更容易研究 | 整机 SWaP、软件可维护性/国产化 | **对照样机 / INFER** |

与“先加一张卡再寻找用途”不同，建议阶段 1 聚焦**具备工程闭环的机载视觉辅助计算产品**：多路接入、同步、深度/障碍、局部避障、FCU 安全接口；阶段 2 解决 ATR/多源事件融合和安全可信；阶段 3 在明确的开放任务场景中开展 VLM 与多机协同的受控 PoC。分期仅表示功能投入顺序，不是无人系统标准的自主等级。

## 9.11 本案例仍需冻结的关键边界

首先确认：1）六路机头相机**功能角色**、真正成对的双目路数、FOV、基线、内外参与同期曝光；2）吊舱 ATR 在既有独立 RK3588 上还是合并到伴飞板；3）是否必须实时图像拼接、拼接输出消费方；4）飞行速度、最大安全距离、允许反应距离、FCU 控制模式；5）开发阶段供电/热/空间、M.2 PCIe 可用通道与互相抢占；6）多机协同具体指“本机失联执行”“局部邻机数据共享”还是“真正替代地面群控”；7）数据密级、设备身份、失陷响应、模型升级。未冻结之前不得给出确定的 TOPS/卡型号需求。

# 10 Benchmark 与工程验证体系

平台最终选型必须由系统级 Benchmark 收敛。

**图 8 平台筛选流程**

```mermaid
flowchart LR
    R["Requirement Vector"] --> S{"Sensor/I/O"}
    S --> RT{"Real-Time"}
    RT --> M{"Memory/DDR"}
    M --> C{"Compute"}
    C --> Q{"Concurrency/P99"}
    Q --> P{"SWaP/Thermal"}
    P --> SW{"Software/Productization"}
    SW --> SEC{"Security/Trust"}
    SEC --> V["System Benchmark"]
    V --> O["Confirmed-fit / Candidate / Constraint"]
```

图源：[`assets/diagrams/final-report-platform-selection-v05.mmd`](../../assets/diagrams/final-report-platform-selection-v05.mmd)

Benchmark 建议包括：

- W1：多 Camera、drop、timestamp、ISP、codec、DDR；
- W2：EuRoC/TUM-VI VIO/SLAM；
- W3：统一模型/输入/precision DNN；
- Full C2：Camera+VIO+Detection+Depth+Planner；
- Host+Accelerator：H2D/D2H、PCIe、E2E；
- Thermal：持续负载降频；
- Trust：Secure Boot、model tamper、attestation、rollback、unauthorized node。

---


## 10.1 增补 ATR、立体深度、任务层与可信运行测试

| ID | 测试场景 | 必须记录 | 通过准则来源 |
|---|---|---|---|
| T-ATR | 指定视频/EO/IR/变焦场景，检测与跟踪 | 数据集版本、AP/Recall/漏检误报、轨迹连续性、Frame Age、功率 | 业务确认的对象和风险要求，当前 GAP |
| T-STEREO | 规定基线/FOV/光照/速度的双目深度 | 距离误差 vs 距离、失配率、视差范围、同步偏差、CPU/GPU/DDR、P99 | 速度与可用障碍距离反推 |
| T-AVOID | 感知→Map→Planner→FCU 全链路 | 障碍发现至可执行指令的 P99、最小留置距离、超时降级 | 实机动力学、飞控安全规则 |
| T-MISSION | 断网/任务重排的 FSM/BT 基线 | 任务成功率、异常恢复、错误命令拒绝、能耗 | 预先定义任务场景 |
| T-VLM | 在基线之上按需叠加语义模型 | 模型质量、图像编码/TTFT/总延迟、附加能耗、误指令率 | 与无 LLM 对照组比较 |
| T-CO-RUN | ATR/Depth/VIO/Planner/VLM 并发 | P95/P99 Frame Age 漂移、deadline miss、热点/频降、PCIe 传输 | 不降低基础避障安全性 |
| T-TRUST | 启动/更新/权限/模型完整性、链路失效 | 拒绝未授权命令、篡改检测、回滚恢复、证据日志、性能代价 | 系统 Threat Model 与适用标准 |

数据与配置按现有 `data/benchmarks/six-camera-validation-matrix.csv` 与 `cases/six-camera-uav/phase-2-validation-plan.md` 维护；上表是报告层测试覆盖补充，未声称已经实测。

# 11 技术发展趋势

## 11.1 多摄时空融合

BEV/Occupancy 等技术推动感知从逐帧单摄向多摄时空融合发展，增加 DDR、同步、temporal state 和 Transformer 计算需求。[R17](../../references/final-report-reference-index-v0.5.md#r17)

## 11.2 模块化架构与 End-to-End 并存

短中期更可能形成“传统定位/安全骨架 + 学习模型增强”的混合架构，而非全部传统模块一次性被 E2E 替代。

## 11.3 VLM/VLA 进入机器人端侧

PaLM-E、RT-2、OpenVLA 表明 VLM/VLA 已进入机器人研究与工程化阶段，但端侧仍受到 memory、latency、power 和 safety verification 限制。[R18](../../references/final-report-reference-index-v0.5.md#r18)[R19](../../references/final-report-reference-index-v0.5.md#r19)[R20](../../references/final-report-reference-index-v0.5.md#r20)[R21](../../references/final-report-reference-index-v0.5.md#r21)

## 11.4 SoC 向 AI + RT + Safety + Trust 融合

IQ-9075、Journey 6、A2000 等平台表明，新一代端侧芯片正把 NPU、GPU、实时子系统、ISP、功能安全和大模型能力进一步集成。

## 11.5 Fleet 与 Trust 融合

多机器人协同将设备身份、可信状态和网络准入转化为系统架构问题。Remote Attestation 与 Fleet Policy 具有明显结合空间。[R30](../../references/final-report-reference-index-v0.5.md#r30)

---

# 12 产品研发建议

## 12.1 产品定位

不建议把后续产品定义为“XX TOPS 国产算力盒”。建议定位为：

> **面向无人装备的安全可信端侧智能计算平台。**

产品核心能力应包括：

- 多传感器接入；
- CPU/GPU/NPU 异构计算；
- 实时控制协同；
- ROS 2/AI Runtime；
- 商用密码；
- 设备身份；
- Trusted Boot / Attestation；
- 模型可信；
- Secure OTA；
- Fleet Trust。

## 12.2 产品系列建议

### 轻量型 UAV Node

目标：小型无人机、轻量机器人。  
路线：Integrated SoC 优先，独立 FCU，低 SWaP，基础 Trust Plane。

### 高性能 Robotics Node

目标：UGV、USV、AMR、高级机器人。  
路线：GPU/Robotics SoC，大内存、多 Sensor、GMSL/CAN、高速网络。

### Host+Accelerator 扩展型

目标：需要不同 AI 档位或 W7 的产品。  
路线：统一 Host + 可替换 M.2/PCIe accelerator。

### Fleet Trust Service

目标：多设备身份、KMS、Verifier、Revocation、Policy、OTA。

## 12.3 研发优先级

近期优先：
1. 冻结六摄 Requirement；
2. 建立统一 Benchmark；
3. 对比一体 SoC 与 Host+Accelerator；
4. 构建最小 Trust Plane；
5. 用实测收敛产品规格。

---


## 12.4 面向本项目的产品定位与差异化决策

不建议把“ATR + 避障 + LLM + 群控”同时定义为第一代必须交付的功能包。对工程可行性最敏感的不是加速卡 TOPS，而是**算法成熟度不足、双目光学/同步标定、真正的全链路闭环、飞控安全边界和验证场景**。若算法主要外部引入，应把可交付软件包、源码/许可、模型迁移、驱动接口、稳定版本和测试方法明确纳入供应商交付物，避免先设计硬件后发现没有可用算法。

差异化建议围绕**端侧安全可信任务计算节点**：设备身份、机载计算平台完整性、吊舱与伴飞计算节点双向认证、可信数据时间戳、模型/任务策略签名、安全更新、机群授权与故障隔离。基于现有密码技术积累，这是可研究的商业化方向，但实际客户支付意愿、适用标准和测试认证路径仍属于待验证问题。可信启动不能被直接写成模型执行期机密性或完整远程证明，三平面边界需分别验证。

# 13 结论

无人装备端侧智能计算平台的核心问题不是“需要多少 TOPS”，而是在给定任务、传感器、实时性、功耗、尺寸和安全约束下，哪些 workload 需要同时运行，以及它们如何竞争 CPU、GPU、NPU、DDR、ISP、I/O 和实时资源。

W1～W9 和 C1～C5 的作用是把复杂应用转化为可预算、可比较、可验证的工程模型。其中 W1～W9 面向单类工作负载，C1～C5 面向典型系统组合；它们均建立在 PX4、Nav2、Autoware、Waymo、Foundation Model 和多机器人等公开技术事实之上，不作为行业等级使用。

产品调研表明，端侧市场已经从单一 SoC 扩展为 SoM、GPU 机器人平台、AI Accelerator、Host+Accelerator 和工业整机等多层产品形态。NVIDIA 在 GPU 和软件生态方面成熟，Qualcomm 正强化机器人 SoC 的多 Camera 和实时子系统，国产平台已覆盖 RK3588、Atlas、BM1688、后摩 LQ50、Journey 6、A2000 等多条路线。当前国产平台的主要短板更集中在软件生态、公开系统 Benchmark 和多 workload 并发证据，而不是理论算力缺失。

结合公司已有密码与可信计算基础，后续产品不宜只复制通用 AI Box，更适合形成“Compute + Real-Time + Trust”的安全可信无人智能计算平台，并以六摄像头无人平台作为第一阶段系统验证载体。

---

# 附录 A 专业术语与缩略语

| 缩写 | 中文 | 说明 |
|---|---|---|
| CPU | 中央处理器 | 通用计算、OS、规划、图优化 |
| GPU | 图形/并行处理器 | VSLAM、Depth、Transformer 等 |
| NPU | 神经网络处理器 | AI 张量计算 |
| SoC | 片上系统 | CPU/GPU/NPU/ISP/I/O 高集成 |
| SoM | 系统级模块 | SoC+内存+电源等模块化 |
| ISP | 图像信号处理器 | RAW 图像处理 |
| VPU | 视频处理单元 | 视频编码/解码 |
| VIO | 视觉—惯性里程计 | Camera+IMU 位姿估计 |
| SLAM | 同时定位与建图 | 定位并建立地图 |
| BEV | 鸟瞰视角表示 | 多传感器统一空间表示 |
| VLM | 视觉语言模型 | 图像+文本理解 |
| VLA | 视觉语言动作模型 | 图像/文本到机器人动作 |
| FCU | 飞行控制单元 | 飞行实时控制 |
| SWaP-C | 尺寸/重量/功耗/成本 | 端侧产品工程约束 |
| Frame Age | 帧龄 | 结果所依据传感器数据的新鲜度 |
| RoT | 可信根 | 系统信任起点 |
| TEE | 可信执行环境 | 隔离敏感代码/数据 |
| TCM | 可信密码模块 | 国内可信计算密码模块 |
| Attestation | 远程证明 | 证明设备身份与平台状态 |

---


# 附录 B 参考文献与研究资产

## B.1 本版新增的应用与伴飞计算机外部事实来源（2026-10-23 访问）

| 编号 | 原始来源 | 支撑内容与证据边界 |
|---|---|---|
| P01 | PX4, *Companion Computers*, https://docs.px4.io/main/en/companion_computer/ | FCU/Linux companion 职责与常见通信分工，官方文档 |
| P02 | ModalAI, *VOXL 2 Feature Matrix*, https://docs.modalai.com/voxl2-feature-matrix/ | 板级规格、相机、VOXL SDK 能力，厂商文档 |
| P03 | ModalAI, *VOXL Vision Hub Visual Obstacle Avoidance*, https://docs.modalai.com/voa/ | 深度点云到障碍物距离消息的公开实现 |
| P04 | Skydio, *Skydio X10*, https://www.skydio.com/x10 | 视觉自主产品能力，厂商宣称而非独立 Benchmark |
| P05 | DJI, *Manifold 3 Specifications*, https://enterprise.dji.com/manifold-3/specs | 100 稀疏 INT8 TOPS、16GB、额定功率与产品形态 |
| P06 | DJI Developer, *Payload SDK Liveview*, https://developer.dji.com/doc/payload-sdk-tutorial/en/advanced-function/liveview.html | 机载视频接入与检测开发示例；不能推出 ATR 质量 |
| P07 | PX4, *Collision Prevention*, https://docs.px4.io/main/en/computer_vision/collision_prevention | 障碍消息、延迟、覆盖与降级；需留意该页面所示 companion 实现维护/测试边界 |
| P08 | Autoware Foundation, *Autoware Overview*, https://autoware.org/autoware-overview/ | UGV 感知、定位、规划、控制功能链 |
| P09 | Waymo, *A look under our trunk: what’s in our compute*, 2026-08-20, https://waymo.com/blog/2026/08/look-under-our-trunk/ | 自动驾驶异构低延迟计算，企业一手技术叙述 |
| P10 | Nav2, *Navigation Concepts*, https://docs.nav2.org/ | AMR 状态估计、规划、控制架构 |
| P11 | OpenCV, *Depth Map from Stereo Images*, https://docs.opencv.org/4.13.0/dd/d53/tutorial_py_depthmap.html | 双目几何及视差/深度关系，开发文档 |
| P12 | Auterion, *Skynode X*, https://auterion.com/product/skynode-x/ | 飞控+任务计算+通信一体化，厂商产品形态 |
| P13 | Rockchip, *rknn-llm benchmark*, https://github.com/airockchip/rknn-llm/blob/main/benchmark.md | RK3588 RKLLM 分阶段模型数据，官方仓库；应固定 commit 版本后复测 |

**证据标记：** FACT = 可追溯原始事实；VENDOR = 厂商披露/宣称；BENCH = 记录完整条件的性能测量；INFER = 工程推断；GAP = 当前无法确认。所有“候选”“预期”“建议”均不应表述为已完成实测的系统结论。

## B.2 既有参考文献与研究资产

完整参考文献及在线核验入口：

- [最终调研报告参考文献索引 v0.5](../../references/final-report-reference-index-v0.5.md)
- [国产可信计算与商用密码标准](../../references/standards/china-trusted-computing-crypto-standards-2026.md)
- [2026-10-08 产品资料复核](../../references/webpages/product-refresh-2026-10-08.md)

关键数据资产：

- [代表产品调研数据 v0.5](../../data/product-specs/final-report-representative-products-v05.csv)
- [完整 Commercial Product Landscape](../../data/product-specs/commercial-product-landscape-2026.csv)
- [Platform Facts](../../data/product-specs/platform-facts.csv)
- [六摄需求→Workload→资源→架构](../../data/calculations/six-camera-requirement-workload-resource-architecture-v03.csv)

关键图源：

- [方法论与证据链](../../assets/diagrams/final-report-methodology-evidence-chain-v03.mmd)
- [W1–W9 Workload 图](../../assets/diagrams/final-report-workload-map-v03.mmd)
- [C1–C5 组合关系图](../../assets/diagrams/final-report-composition-map-v05.mmd)
- [产品 Landscape 图](../../assets/diagrams/final-report-product-landscape-v05.mmd)
- [平台筛选流程图](../../assets/diagrams/final-report-platform-selection-v05.mmd)
- [安全可信三平面架构图](../../assets/diagrams/secure-trusted-three-plane-v03.mmd)
- [六摄需求—资源—架构图](../../assets/diagrams/six-camera-requirement-resource-architecture-v03.mmd)
