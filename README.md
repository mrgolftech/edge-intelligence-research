# Edge Intelligence Research

面向无人装备、机器人与边缘智能系统的端侧计算研究仓库。

本仓库不以“收集算力卡参数”或“按 TOPS 排名”为目标，而是建立一套可复用的工程方法：

> **应用/任务场景 → 功能栈 → 自主性画像 → 数据与算法工作负载 → 计算/系统资源 → 部署架构 → 芯片/模组/产品 → Benchmark 验证**

## 研究对象

研究范围不局限于六摄像头项目，覆盖：

- UAV / UAS：巡检、测绘、搜救、监视、物流、GNSS拒止导航、协同无人机等
- UGV / 自动驾驶：道路车辆、特种无人车、园区车辆、AMR/AGV
- USV / 无人船：测绘、巡检、监视、海洋作业、自主航行与避碰
- 移动/操作机器人：仓储、工业、服务、巡检、具身智能
- 固定式边缘智能：多摄像头感知、视频分析、工业视觉、边缘推理节点
- 多无人系统：多机协同、任务分配、共享感知、边云协同

六摄像头无人平台仅作为本项目的一个工程 Case Study，用于验证方法和 Benchmark。

## 研究框架

### 1. 任务与应用场景

先回答“系统在什么环境中完成什么任务”，包括任务复杂度、环境复杂度、传感器配置、人机关系和安全约束。

### 2. 通用自主系统功能栈

参考 PX4、Nav2、Autoware 以及近年无人系统/机器人综述，采用业内常见功能划分：

**Sensing / Data Acquisition → State Estimation & Localization → Perception & World Modeling → Prediction / Tracking → Planning & Decision → Control & Execution**

在此基础上扩展：

- Mission / Task Management
- Human-Machine Interaction / Remote Operation
- Multi-Agent Coordination / Fleet Management
- Edge-Cloud Collaboration
- Safety / Security / Health Monitoring

这是一套“功能分解”，不是自定义的自主等级。

### 3. 自主性画像

跨无人系统不使用项目自创的 L1–L5。

通用分析优先参考 NIST ALFUS 的多维思想：

- Mission Complexity：任务复杂度
- Environmental Complexity：环境复杂度
- Human Independence：人类独立性/人机交互程度

不同领域另参考其专用术语和标准，例如：

- 道路车辆：SAE J3016
- 海上自主船：IMO MASS
- 无人机/机器人：结合具体任务、系统架构和行业文献描述，不强行套用道路车辆等级

详见：[无人系统端侧智能应用、功能栈与自主性框架](research/scenarios/unmanned-intelligence-scenarios.md)

## 算力研究原则

平台评估至少同时分析：

- CPU / GPU / NPU / DSP / MCU
- INT4 / INT8 / FP16 / BF16 / FP32 等精度
- 内存容量、带宽、Cache
- ISP、多路视频编解码、Camera/SerDes
- PCIe、Ethernet、CAN、USB、MIPI 等 I/O
- ROS2、Linux、PyTorch、ONNX、厂商 SDK、算子覆盖
- 实时性、任务并发、数据搬运
- SWaP-C：尺寸、重量、功耗、成本
- 热稳定性、可靠性、供货与国产化
- 实际模型性能与系统级持续性能

始终区分：

> **理论峰值算力 ≠ 单模型 Benchmark ≠ 多任务系统性能 ≠ 可产品化能力**

## 当前事实底座

### 标准/框架
- [NIST ALFUS](references/standards/nist-alfus.md)
- [SAE J3016](references/standards/sae-j3016.md)
- [IMO MASS](references/standards/imo-mass.md)

### 工程架构
- [PX4 Computer Vision](references/webpages/px4-computer-vision.md)
- [Nav2](references/webpages/nav2-navigation.md)
- [Autoware Architecture](references/webpages/autoware-architecture.md)
- [NVIDIA Isaac ROS](references/webpages/nvidia-isaac-ros.md)

### 综述/趋势
- [UAV 自主系统综述索引](references/papers/uav-autonomy-surveys.md)
- [USV / AMR / 多机器人综述索引](references/papers/usv-robotics-autonomy-surveys.md)
- [Foundation Models / VLM / VLA / Edge Robotics](references/papers/foundation-models-robotics.md)

### 现有计算平台
- [代表性端侧计算平台事实底座](research/products/representative-edge-compute-platforms.md)

## 工程 Case

- [六摄像头无人平台](cases/six-camera-uav/README.md)
- [六摄像头工作负载模型](research/workloads/six-camera-workload-model.md)

## 当前研究判断

1. 不存在一个可直接横跨 UAV、道路车辆、USV、AMR、操作机器人的统一“L1–L5 算力等级”；自主性应结合任务、环境和人类参与程度描述。
2. 感知、定位/建图、规划、控制是当前自主系统反复出现的核心功能链；任务管理、多机协同和人机交互位于更上层。
3. AI/ML 正从单点感知模块扩展到预测、规划、端到端策略、世界模型和 VLM/VLA，但经典/确定性模块仍大量存在，混合架构是重要现实形态。
4. 大模型进入机器人端侧已经有真实产品和研究依据，但其价值与算力需求必须按具体任务评估，不能把“支持 LLM/VLM”作为所有无人装备的默认需求。
5. 端侧与边缘/云协同将长期并存：低时延、安全关键和断网可用能力倾向本地执行，训练、全局知识、重计算和群体信息可按任务放到近端边缘或云端。

## 下一阶段

1. 建立“平台类型 × 任务场景 × 功能栈 × 自主性画像”的需求矩阵；
2. 分别形成 UAV、UGV/AMR、USV、机器人四类场景研究；
3. 建立典型工作负载族：视频感知、VIO/SLAM、BEV/Transformer、规划控制、VLM/VLA、多机协同；
4. 对 NVIDIA、Qualcomm、瑞芯微、地平线、黑芝麻、后摩、Hailo、Axelera 等平台按统一字段建立事实数据；
5. 用六摄像头 Case 和公开 Benchmark 验证平台边界。

研究和提交规范以 [AGENTS.md](AGENTS.md) 为准。
