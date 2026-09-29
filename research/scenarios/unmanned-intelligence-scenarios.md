# 无人系统端侧智能应用、功能栈与自主性框架

- 状态：v0.2
- 日期：2026-09-29
- 性质：跨域研究基线
- 证据：标准/官方架构/综述/现有产品

## 1. 研究问题

端侧算力需求不能由某个芯片的 TOPS 倒推，也不能围绕一个六摄像头案例建立全部结论。

本研究首先回答：

1. 当前无人系统有哪些真实应用模式？
2. 行业内如何拆分自主系统功能？
3. “自主程度”如何客观描述？
4. 不同功能对应什么计算工作负载？
5. 未来的 E2E、World Model、VLM/VLA、多机协同会增加哪些新负载？
6. 最后哪些端侧计算平台能满足这些需求？

---

## 2. 为什么不采用项目自定义 L1–L5

此前版本使用 L1–L5 组织讨论，但没有对应跨无人系统的行业标准依据，因此本版本撤销。

### 已确认事实：跨域自主性本身就是多维问题

NIST 的 ALFUS（Autonomy Levels for Unmanned Systems）面向多类无人系统，核心不是简单按算力或功能数量排成一条线，而是用多个维度描述 Contextual Autonomous Capability。

其经典三个方面是：

- Mission Complexity：任务复杂度
- Environmental Complexity：环境复杂度
- Human Independence：人类独立性/人机交互程度

ALFUS 还强调不同 unmanned systems 的任务、环境、人机关系差别很大，需要任务上下文。

### 领域专用标准并不通用

**SAE J3016** 描述的是道路机动车驾驶自动化，Level 0–5 围绕 Dynamic Driving Task 和驾驶员角色定义，不能直接拿来定义无人机、无人船或机器人。

**IMO MASS** 面向 Maritime Autonomous Surface Ship。IMO 早期监管梳理提出自动化/远控/自主等不同运作方式，并明确同一航程可处于一个或多个自主程度；2026 年 IMO 又采用了 MASS Code，强调对具体船舶功能采用 functional approach。

### 项目结论

本项目不再构造一个“所有无人设备从 L1 升到 L5”的线性体系。

改为：

> **任务场景 + 功能栈 + 自主性画像 + 工作负载画像**

四个维度联合描述。

---

## 3. 当前无人系统的应用事实底座

### 3.1 UAV / UAS

近年综述和 PX4 工程体系反复出现的应用/能力包括：

**任务应用**
- 监视与侦察
- 基础设施/电力/工业巡检
- 测绘与三维重建
- 农业监测与作业
- 搜索与救援
- 物流/运输
- 环境监测
- 应急/灾害响应

**自主相关任务**
- GNSS/INS 导航
- Optical Flow
- VIO / SLAM
- 目标/障碍物感知
- 路径规划
- Collision Avoidance
- GNSS-denied localization
- 多机协同

UAV 的突出工程约束是 SWaP、续航、振动、传感器同步和弱/断网络下的本机可用性。

### 3.2 UGV / 自动驾驶车辆

Autoware 当前公开架构覆盖完整 autonomous driving stack：

- Sensing
- Map
- Localization
- Perception
- Planning
- Control
- Vehicle Interface

其当前公开能力还包括多传感器融合、动态目标跟踪、NDT/GNSS/IMU 定位、动态避障、E2E driving model 支持。

典型应用包括：
- Robotaxi
- 城市/园区运输
- Cargo Delivery
- Shuttle
- 特种无人车
- 自动驾驶乘用车

这类平台通常拥有更高功耗预算，但传感器数量、3D感知、功能安全和冗余要求也更高。

### 3.3 AMR / 移动机器人

仓储/物流 AMR 文献中的核心能力长期稳定在：

- Perception
- Localization & Mapping
- Global/Local Planning
- Motion Control
- Fleet Coordination / Task Allocation

应用包括：
- 仓内物料运输
- 制造物流
- 巡检
- 医疗/服务移动机器人
- 多机器人协同

与无人车相比，AMR 常工作在更结构化环境，但长期自主运行、动态人群、地图变化和多机调度成为重要负载。

### 3.4 USV / 无人船

近年 USV 综述将核心能力集中在：

- Navigation
- Guidance
- Control
- Perception
- Path Planning
- Collision Avoidance
- Decision Making
- Human-Machine Interface

实际任务包括：
- 海洋测绘/调查
- 环境监测
- 巡检
- 监视
- 科研
- 工程/商业与防务任务

特有负载还包括：
- Radar/AIS/视觉融合
- COLREGs 约束下的避碰
- 长航时和高可靠通信
- 海况、天气、低纹理水面等复杂环境

### 3.5 操作机器人 / 具身机器人

传统机器人主要是：
- 目标/姿态感知
- 状态估计
- Motion Planning
- Manipulation
- Force/Impedance Control

2023–2026 年公开研究又出现：
- PaLM-E：Embodied multimodal language model
- RT-2：Vision-Language-Action
- OpenVLA：开源 VLA
- NVIDIA GR00T N1/N1.x：机器人 foundation model
- Gemini Robotics / On-Device：VLA 与 embodied reasoning

这证明 Foundation Model / VLM / VLA 已成为真实研究和产品路线，但不能据此认为所有无人装备都需要大模型。

### 3.6 固定式边缘智能

常见应用：
- 多路视频分析
- 工业视觉
- NVR / IPC
- 交通/安防
- 多摄像头检测与跟踪
- 本地生成式 AI

这些系统可能没有 localization/planning/control，却可能具有很重的视频和推理负载，说明“算力需求”和“自主程度”不是同一个轴。

---

## 4. 通用自主系统功能栈

综合 Autoware、PX4、Nav2、UAV/AMR/USV 文献，本项目采用以下功能分类。

### F1 Sensing / Data Acquisition

负责获取和同步原始环境/本体数据：

- RGB / IR Camera
- LiDAR
- Radar
- IMU
- GNSS
- Ultrasonic
- AIS
- Audio
- Encoder / Joint / Force sensors

典型计算资源：
- ISP
- VPU
- DMA
- MCU
- Camera/SerDes I/O
- DDR bandwidth

### F2 State Estimation / Localization

回答“我在哪里、以什么状态运动”。

包括：
- GNSS/INS
- EKF/UKF
- Optical Flow
- VO / VIO
- LiDAR-Inertial Odometry
- Visual/LiDAR localization

典型资源：
- CPU
- SIMD/GPU
- 低时延内存
- 精确时间同步

### F3 Mapping / World Modeling

建立环境表示：

- 2D/3D Mapping
- SLAM
- Occupancy Grid
- Point Cloud Map
- BEV / Occupancy
- Semantic Map
- Dynamic World Model

典型资源：
- CPU/GPU
- 内存容量/带宽
- 3D计算
- 持久化存储

### F4 Perception

回答“周围有什么”。

包括：
- Detection / Classification
- Tracking
- Segmentation
- Depth
- Pose
- Free-space / Obstacle
- Traffic / Maritime object perception
- Multi-modal fusion

典型资源：
- GPU/NPU
- ISP
- DDR
- Video pipeline

### F5 Prediction / Situation Understanding

回答“周围对象接下来可能做什么、当前局势意味着什么”。

包括：
- Multi-object tracking/prediction
- Intent prediction
- Scene understanding
- Interaction modeling
- VLM-based semantic reasoning

传统感知系统可能很轻；自动驾驶/高级机器人可能很重。

### F6 Planning / Decision

回答“下一步应该怎么走/做”。

包括：
- Mission Planning
- Global Route Planning
- Local Planning
- Trajectory Planning
- Behavior Planning
- Collision Avoidance
- Task Allocation
- Learned/E2E policy

计算可能由 CPU优化算法、GPU/NPU学习模型或两者混合承担。

### F7 Control / Execution

包括：
- Flight control
- Motion control
- Trajectory tracking
- MPC/PID
- Actuator control
- Manipulator control

安全关键控制通常强调：
- 确定性
- 周期性
- Worst-case latency
- 功能安全/故障安全

其需求不能用 AI TOPS 衡量。

### F8 Mission / HMI / Remote Operation

包括：
- 任务管理
- 任务状态机
- 遥控/远程接管
- 人机交互
- 自然语言任务输入
- 任务解释/报告

### F9 Multi-Agent / Fleet / Collaboration

包括：
- Fleet management
- Task allocation
- Cooperative perception
- Collaborative localization/mapping
- Multi-robot planning
- Swarm coordination

新增计算和通信负载：
- 网络
- 分布式状态
- 多机数据融合
- 协同优化

### F10 Safety / Security / Health

包括：
- Fault detection
- Health monitoring
- Safety supervisor
- Redundancy
- Cybersecurity
- Trusted identity/secure communication

这是产品化无人系统的横向能力，不属于“更高 TOPS”。

---

## 5. 自主性画像：采用 ALFUS 思路而不是算力等级

对每个场景记录至少三个维度。

### A. Mission Complexity

例如：
- 固定航线采集
- 动态目标跟踪
- 开放环境搜救
- 多步骤任务执行
- 多机协同任务

### B. Environmental Complexity

例如：
- 结构化室内
- 固定园区
- 城市道路
- 复杂低空
- GNSS拒止
- 动态海况
- 高密度动态障碍

### C. Human Independence

例如：
- 人持续遥控
- 人在环决策
- 人监督、必要时接管
- 系统自主完成任务、人仅给目标

注意：这些描述不强行映射成一个统一 0–5 数字。

---

## 6. 从功能到计算：工作负载类型

后续算力需求按“负载族”建立，而不是按自主等级建立。

| 工作负载族 | 典型算法 | 主要硬件关注 |
|---|---|---|
| Sensor I/O / Video | ISP、编解码、同步 | ISP/VPU、I/O、DDR |
| Classical Estimation | EKF、VIO、图优化 | CPU、GPU、内存、实时性 |
| DNN Perception | YOLO、Seg、Depth | NPU/GPU、DDR、算子 |
| 3D / Mapping | SLAM、Point Cloud、BEV | CPU/GPU、内存、带宽 |
| Planning / Optimization | A*、RRT、MPC、优化器 | CPU/GPU、确定性 |
| Learned Planning / E2E | Transformer、Diffusion、Policy | GPU/NPU、FP16/INT8、DDR |
| Foundation Model | VLM/LLM/VLA | 内存容量/带宽、INT4/FP8/FP16 |
| Collaboration | 多机融合/任务分配 | 网络、CPU/GPU、分布式状态 |
| Safety/Control | RT loop、supervisor | MCU/CPU、实时OS、冗余 |

---

## 7. 当前主流技术形态

### 7.1 经典模块化自主系统

Sensing → Localization/Perception → Planning → Control

仍然是 PX4、Nav2、Autoware 等成熟工程体系的重要基础。

优点：
- 模块边界清楚
- 可验证/可调试
- 便于安全隔离

### 7.2 学习增强的模块化系统

用 DNN/Transformer 替代或增强：
- Perception
- Prediction
- Depth
- Planning
- Sensor fusion

这是当前大量量产/工程应用的现实路径。

### 7.3 End-to-End / Learned Policy

Autoware 2.0 已明确讨论传统固定 pipeline 与 E2E/diffusion model 的共存，并引入 generator-selector 思路对候选 trajectory 做 safety check 和选择。

这说明 E2E 已进入工程框架讨论，但仍需要显式安全约束。

### 7.4 Foundation Model / VLM / VLA

RT-2、OpenVLA、GR00T、Gemini Robotics 代表从视觉/语言理解向动作策略扩展。

其端侧计算特征：
- 权重更大
- 内存容量要求更高
- KV Cache/多模态 encoder
- INT4/FP8/FP16 等多精度
- latency 与控制频率矛盾更突出

### 7.5 Edge-Cloud / Distributed Autonomy

2025 年 Edge Robotics 综述强调低时延机器人任务适合在边缘处理，同时云/边缘计算用于补充本机资源。

未来需要研究：
- On-device 必须常驻的安全/实时功能
- Near-edge 可卸载的重计算
- Cloud 训练/知识/全局优化
- 断网降级策略
- 多机器人共享感知与协作

---

## 8. 现有产品对需求演进的客观印证

当前产品本身已经体现不同负载方向：

- **RK3588**：6 TOPS NPU + 强视频/ISP/CPU/GPU，说明轻量边缘视觉不仅需要 NPU，还需要多媒体与 I/O。
- **Qualcomm Robotics RB5**：15 TOPS、7路并发相机、ROS2、5G，直接面向 robots/drones，强调异构计算、视觉和连接。
- **Jetson Orin**：最高 275 TOPS、最高 64GB、CUDA/NVDLA/PVA，面向多传感器和多并发 AI。
- **Jetson Thor**：128GB、273GB/s、FP4/FP8、40–130W，官方直接定位 Physical AI/Agentic AI/Robotics，体现 foundation model 负载进入机器人平台。
- **地平线征程6**：10+～560 TOPS系列，集成 CPU/GPU/MCU/BPU，原生支持 Transformer，体现自动驾驶从基础 ADAS 到全场景智驾的不同负载。
- **黑芝麻 A2000**：支持 BEV+Transformer、Multi-Modal LM、E2E 和多精度，体现车端算法从感知向多模态/E2E演进。
- **Axelera Metis**：独立 PCIe/M.2 AI 加速器，约214 INT8 TOPS；官方文档明确指出实际吞吐仍取决于模型、PCIe 和 pipeline。
- **Hailo-10H**：40 INT4 / 20 INT8 TOPS、典型2.5W，定位视觉 + GenAI/VLM/LLM 端侧加速。
- **Firefly 后摩 LQ50 模组**：Firefly 公开页面宣称 160 INT8 TOPS、48GB LPDDR5、可运行较大模型；当前证据来自合作方/产品页，后续需补后摩官方资料验证。

这些产品不是一个维度上的“高低等级”，而是不同系统形态和工作负载定位。

详见：[`research/products/representative-edge-compute-platforms.md`](../products/representative-edge-compute-platforms.md)

---

## 9. 未来趋势对需求的影响

### 趋势 1：感知从单模型走向多模态时空融合

从 Camera 单模型检测发展到 Camera/LiDAR/Radar、BEV、Occupancy、Temporal Fusion。

影响：
- 带宽和内存压力增大
- 多模型并发
- Transformer 算子需求增加

### 趋势 2：定位/规划继续与学习模型融合

UAV/USV/自动驾驶研究均出现 learning-assisted estimation、RL planning、E2E planning。

影响：
- CPU/GPU/NPU并行更复杂
- 不能只买“纯推理 NPU”

### 趋势 3：Foundation Models进入机器人和自动驾驶

公开研究已覆盖：
- multimodal reasoning
- scenario understanding
- long-horizon planning
- VLA action generation

影响：
- 内存容量成为核心指标
- INT4/FP8/BF16等精度重要
- 大模型与实时任务的资源隔离重要

### 趋势 4：世界模型与生成式仿真用于预测、规划和验证

自动驾驶综述中 world model 已用于未来场景生成、行为规划和 prediction-planning interaction。

影响：
- 端侧不一定全部运行世界模型
- 训练/仿真更可能依赖高性能边缘或云
- 端侧可能部署压缩后的 prediction/policy 模型

### 趋势 5：多机器人协作

2025–2026 多机器人综述重点讨论 perception、planning、collaboration，以及 LLM 在 task allocation / planning / HRI 中的作用。

影响：
- 单机算力之外，网络、同步、分布式状态和安全通信成为系统资源。

---

## 10. 结论

本项目后续不再问：

> “无人装备处于 L 几，所以需要多少 TOPS？”

而改为：

> **某个平台，在某一任务和环境中，需要哪些功能模块，以多大自主程度运行；这些模块产生什么工作负载；哪些必须在本机实时完成，哪些可以边缘/云协同；最后推导需要的计算、内存、带宽、I/O、功耗和软件能力。**

六摄像头项目用于验证这套方法，但总体需求研究必须来自 UAV、UGV、USV、AMR、机器人和固定边缘系统的广泛事实底座。

---

## References

### 标准/机构
1. NIST, Autonomy Levels for Unmanned Systems (ALFUS)  
   https://www.nist.gov/publications/autonomy-levels-unmanned-systems-alfus-frameworkvolume-ii-framework-models-initial
2. SAE J3016, Taxonomy and Definitions for Terms Related to Driving Automation Systems for On-Road Motor Vehicles  
   https://saemobilus.sae.org/topics/electrical-electronics-and-avionics/automation/driving-automation/automated-driving-systems
3. IMO, Maritime Autonomous Surface Ships (MASS)  
   https://www.imo.org/en/mediacentre/hottopics/pages/autonomous-shipping.aspx

### 官方工程架构
4. PX4 Computer Vision  
   https://docs.px4.io/main/en/advanced/computer_vision
5. Nav2 Documentation  
   https://docs.nav2.org/
6. Autoware Documentation  
   https://docs.autoware.org/main/home/
7. Autoware Architecture  
   https://docs.autoware.org/main/design/autoware-architecture-v1/
8. NVIDIA Isaac ROS  
   https://developer.nvidia.com/isaac/ros

### 综述/论文
9. UAV control in autonomous object-goal navigation: a systematic literature review, Artificial Intelligence Review
10. From GPS to AI: A comprehensive review of UAV localization solutions, ISPRS JPRS, 2025
11. An overview of Unmanned Surface Vehicles: Methods, practices, and applications, Control Engineering Practice, 2025
12. A survey of autonomous robots and multi-robot navigation: Perception, planning and collaboration, 2025
13. Edge Computing and Its Application in Robotics: A Survey, 2025
14. PaLM-E: An Embodied Multimodal Language Model, ICML 2023
15. RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control, 2023
16. OpenVLA: An Open-Source Vision-Language-Action Model, 2024
17. GR00T N1 / N1.x, NVIDIA Research
18. A Survey of World Models for Autonomous Driving, 2025
