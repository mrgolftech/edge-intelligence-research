# 无人装备端侧智能应用场景与能力分级

- 状态：v0.1
- 日期：2026-09-29
- 性质：研究基线
- 证据状态：公开资料 + 工程推断

## 研究问题

端侧智能计算调研首先需要回答的不是“哪一块算力卡有多少 TOPS”，而是：

1. 无人装备需要在端侧完成哪些智能任务？
2. 不同任务产生什么数据流和算法负载？
3. 能力从基础视觉发展到自主导航、VLM/Agent 时，系统资源需求如何变化？
4. 哪些任务属于实时安全链路，哪些任务属于高层认知链路？
5. 如何建立一个后续可以映射到芯片与平台的能力分级体系？

## 背景

无人装备的机载/车载计算不是单一 AI 模型推理问题。

以视觉无人平台为例，真实链路可能同时包含：

```text
Camera / IMU / GNSS / LiDAR
        ↓
采集、时间同步、ISP、编解码
        ↓
检测 / 跟踪 / 分割 / 深度估计
        ↓
多传感器融合 / VIO / SLAM
        ↓
障碍地图 / 局部规划 / 全局规划
        ↓
控制与任务执行
        ↓
VLM / LLM / Agent（可选的高层认知）
```

不同环节对硬件的要求差异很大：

- 视频采集更关注接口、ISP、DMA、编解码和内存带宽；
- CNN/Transformer 推理更关注 GPU/NPU 算力和算子支持；
- VIO/SLAM 同时依赖 CPU/GPU、低时延同步、内存访问和实时性；
- VLM/LLM 更关注模型容量、内存容量、内存带宽以及低精度大模型推理能力；
- 飞控和安全关键控制更关注确定性与低时延，不应简单交给大模型。

因此，必须先建立任务和工作负载模型，再讨论计算平台。

---

## 已知事实

### 1. 视觉定位与避障是无人机端侧计算的成熟需求

PX4 官方文档将计算机视觉用于：

- Optical Flow：二维速度估计；
- Visual Inertial Odometry：融合视觉与 IMU，输出三维位姿和速度；
- Collision Prevention：碰撞预防；
- 相关视觉任务通常由 Companion Computer 承担。

这说明无人平台上的视觉计算不仅是“识别目标”，还直接参与定位和导航链路。

证据摘要：[`references/webpages/px4-computer-vision.md`](../../references/webpages/px4-computer-vision.md)

### 2. 自主导航本身是一条完整计算链路

ROS 2 Nav2 官方资料将自主导航拆分为：

- State Estimation
- Environmental Representation
- Planning
- Control
- Behaviors / Behavior Trees

Nav2 的插件体系还包括 costmap、planner、controller、behavior 和 navigator。

因此，“自主导航”不能被压缩成一个单独的 AI TOPS 指标。

证据摘要：[`references/webpages/nav2-navigation.md`](../../references/webpages/nav2-navigation.md)

### 3. 现代机器人端侧平台同时处理感知、定位、建图和规划

NVIDIA Isaac ROS 官方资料覆盖：

- AI perception / inference
- Visual SLAM
- 3D scene reconstruction
- depth estimation
- pose estimation/tracking
- motion planning

这说明高性能端侧平台的价值通常来自完整机器人计算流水线，而不是单模型峰值性能。

截至 2026-09-29，Isaac ROS Visual SLAM 文档还记录了多摄像头 VIO / SLAM、RGB-D 支持等演进；2026-09-21 文档记录该包更名为 `isaac_ros_cuvslam`。

证据摘要：[`references/webpages/nvidia-isaac-ros.md`](../../references/webpages/nvidia-isaac-ros.md)

### 4. VLM/VLA 正在进入机器人高层任务与动作研究

OpenVLA 展示了视觉-语言-动作模型将视觉、语言指令与机器人动作连接起来的技术路线。

但 OpenVLA 主要面向通用机器人操作研究，并不是无人机实时飞控的直接证据。

因此，本项目把 VLM/VLA/Agent 放在高级认知和任务级智能层，而不是把它们作为基础自主导航的必要条件。

证据摘要：[`references/papers/openvla.md`](../../references/papers/openvla.md)

---

## 项目能力分级

> **重要说明：以下 L1–L5 是本项目内部研究框架，不是行业标准。**
>
> 其目的不是给产品贴标签，而是把“能力升级”转换为“工作负载升级”，后续再映射到平台资源。

### L1：基础视觉处理

**目标**

完成多路传感器数据的可靠获取和基础视觉处理。

**典型任务**

- 摄像头采集
- 多摄像头同步
- ISP
- 畸变校正
- Resize / Crop / Color Convert
- 视频编码/解码
- 图像拼接
- 轻量传统视觉算法

**计算特征**

AI 算力未必是主要瓶颈，更容易受以下资源限制：

- MIPI / SerDes 接入能力
- ISP 吞吐
- DMA
- 内存带宽
- 视频编解码单元
- CPU 图像处理效率

**工程判断**

六路甚至更多摄像头场景下，即使暂时没有复杂 AI 模型，也可能因数据搬运、图像格式转换、拼接和编码造成较高系统负载。

因此 L1 不能简单理解为“低 TOPS = 没有难度”。

---

### L2：实时环境感知

**目标**

让无人平台知道“周围有什么”。

**典型任务**

- 目标检测
- 分类/识别
- 多目标跟踪
- 语义/实例分割
- 深度估计
- 光流
- 双目/多目匹配
- 障碍物检测
- 多摄像头感知融合

**主要输出**

- Bounding Box
- Track ID
- Semantic Mask
- Depth Map
- Optical Flow
- Obstacle List

**计算特征**

开始形成持续 AI 推理负载：

```text
多路视频输入
  ↓
预处理
  ↓
一个或多个视觉模型
  ↓
后处理 / 跟踪 / 融合
```

关键指标从单纯的模型 FPS 扩展到：

- 多路并发 FPS
- 端到端延迟
- 模型切换/并发能力
- 内存带宽
- 预处理与后处理开销
- NPU/GPU 实际利用率

**工程判断**

这一等级通常是 AI 加速器最直接发挥作用的阶段，但“标称 TOPS”仍不能代表真实系统能力。

---

### L3：定位、SLAM 与自主导航

**目标**

不仅知道“有什么”，还要知道：

- 我在哪里？
- 障碍物在哪里？
- 应该往哪里走？
- 如何实时避开障碍物？

**典型任务**

- Visual Odometry
- VIO
- SLAM / VSLAM
- GNSS/INS/视觉融合
- 局部/全局地图
- Occupancy / Cost Map
- 障碍物融合
- 局部路径规划
- 全局路径规划
- 自主避障

**典型链路**

```text
Camera + IMU + GNSS
       ↓
时间同步 / 标定
       ↓
VO / VIO / SLAM
       ↓
位姿 + 地图
       ↓
感知障碍物融合
       ↓
Cost Map
       ↓
Path Planning
       ↓
Control Setpoint
```

**计算特征**

L3 与 L2 的关键差别是：

1. AI 模型不再是唯一负载；
2. CPU 和 GPU 通用计算的重要性上升；
3. 传感器时间同步和标定直接影响系统质量；
4. 数据链路延迟比单个模型 FPS 更重要；
5. 系统需要持续运行多个相互依赖的节点。

**工程判断**

纯 NPU 型平台即使拥有较高 INT8 TOPS，也未必适合复杂 SLAM/VIO。

评估 L3 平台时，应显著提高以下指标权重：

- CPU
- GPU/通用并行计算
- 内存带宽
- ROS2 支持
- 传感器时间戳和同步
- 系统实时性
- 长时间稳定性

---

### L4：Transformer / BEV / VLM 高级感知

**目标**

从“检测物体”进一步发展为理解复杂环境和关系。

**可能任务**

- Vision Transformer
- BEV 感知
- 多摄像头时空融合
- 开放词汇检测
- VLM 场景问答
- 场景描述
- 语义关系理解
- 多模态传感器理解

**计算特征**

相比传统 CNN 感知，可能明显提高：

- Transformer 算力需求
- 内存容量
- 内存带宽
- 中间特征存储
- 多摄像头融合开销
- FP16/BF16/INT8/INT4 混合精度需求

**工程判断**

进入这一等级后，仅用 INT8 TOPS 进行跨平台比较会越来越失真。

平台比较必须增加：

- 实际 Transformer Benchmark
- 支持的算子和量化精度
- 模型可用内存
- 内存带宽
- 模型编译/转换成熟度

---

### L5：VLM / LLM / Agent 任务级智能

**目标**

让无人平台具备更高层次的：

- 自然语言理解
- 场景推理
- 任务分解
- 人机交互
- 多步骤任务规划
- 工具/API 调用
- 多平台协同任务编排

**可能链路**

```text
视觉/地图/状态/任务指令
          ↓
       VLM / LLM
          ↓
   场景理解 / 任务规划
          ↓
       Agent / VLA
          ↓
受约束的技能或导航指令
          ↓
确定性的导航 / 控制系统
```

**计算特征**

资源压力逐渐从单纯视觉推理转向：

- 模型权重容量
- KV Cache
- 内存容量
- 内存带宽
- INT4 / INT8 / FP16
- 首 Token 延迟
- Token 生成速度
- 多模态输入处理
- 多模型共存

**工程判断**

当前更稳妥的系统架构是：

> **大模型负责高层认知和任务规划，确定性算法负责实时导航和安全关键控制。**

VLM/LLM 是否值得部署到无人机本体，需要根据：

- 飞行器 SWaP
- 通信条件
- 任务自主性
- 延迟容忍度
- 模型规模
- 安全边界

单独评估。

不能因为“端侧支持 LLM”就认为该平台更适合所有无人场景。

---

## 能力等级与资源变化

| 维度 | L1 | L2 | L3 | L4 | L5 |
|---|---|---|---|---|---|
| 摄像头/传感器 I/O | 高 | 高 | 高 | 高 | 中-高 |
| ISP/编解码 | 高 | 高 | 中-高 | 中-高 | 中 |
| CPU | 中 | 中 | **高** | 高 | 高 |
| GPU/NPU | 低-中 | **高** | 高 | **很高** | 高-很高 |
| 内存容量 | 中 | 中 | 中-高 | 高 | **很高** |
| 内存带宽 | 高 | 高 | **高** | **很高** | **很高** |
| 低时延确定性 | 中 | 高 | **很高** | 高 | 视任务而定 |
| ROS/机器人生态 | 低-中 | 中 | **很高** | 高 | 高 |
| 大模型生态 | 低 | 低 | 低 | 中-高 | **很高** |

> 表中“高/低”仅表示同一研究框架中的相对关注度，不代表量化门槛。

---

## 应用场景到任务的映射

### 无人机

常见端侧需求可能包括：

- 多路可见光/红外采集
- 目标检测与跟踪
- 光流
- VIO
- GNSS 拒止环境定位
- 避障
- 地图构建
- 自主航线与任务规划
- 高层场景理解

特点：

- SWaP 约束最强；
- 持续功耗直接影响续航；
- 摄像头、IMU 和飞控时间同步重要；
- 实时控制与高层 AI 必须分层。

### 无人车 / AMR

常见任务：

- 多摄像头/激光雷达感知
- 定位
- 地图
- 障碍物融合
- 路径规划
- 行为规划

相比小型无人机，对功耗和重量的约束通常较宽松，但传感器数量和数据吞吐可能更大。

### 无人船

可能增加：

- 远距离目标识别
- 水面障碍物检测
- 雷达/AIS/视觉融合
- 长时间持续运行
- 高可靠通信

### 机器人

根据移动、操作或复合任务，可能组合：

- VSLAM
- 深度估计
- 6D Pose
- Motion Planning
- VLM/VLA

### 固定式多摄像头边缘设备

主要关注：

- 多路视频接入
- 编解码
- 多模型推理
- 多目标跟踪
- 数据汇聚

这类系统不需要自身定位导航，因此不能直接套用无人平台的 L3 资源需求。

---

## 对算力调研的直接影响

后续调研产品时，不再先问：

> “这张卡是多少 TOPS？”

而应先问：

### 对 L1/L2

- 能接几路相机？
- ISP 和编解码能力如何？
- 多路模型实际能跑多少 FPS？
- 是否有零拷贝/高效数据通路？

### 对 L3

- CPU/GPU 能否支撑 SLAM/VIO？
- ROS2 生态如何？
- 摄像头 + IMU 同步能力如何？
- 多节点并发时的端到端延迟如何？

### 对 L4

- Transformer/BEV 有哪些实际 Benchmark？
- 内存带宽够不够？
- NPU 算子覆盖如何？

### 对 L5

- 能部署多大的 VLM/LLM？
- INT4/INT8/FP16 支持情况？
- 可用内存和带宽？
- TTFT 和生成吞吐？
- 能否与实时视觉/导航负载共存？

---

## 工程判断

### 判断 1：无人装备“需要 AI 算力”是一个过于粗糙的表述

更准确地说，无人装备需要的是：

> **面向多传感器数据流、实时感知、定位导航和可选高层认知的异构计算能力。**

### 判断 2：能力提升不是简单的 TOPS 线性增长

例如从 L2 到 L3，SLAM/VIO 会显著增加 CPU、GPU通用计算、同步和系统实时性要求，而不只是增加 NPU TOPS。

从 L3 到 L5，则可能突然出现大容量内存和内存带宽需求。

### 判断 3：端侧大模型不是所有无人装备的必选项

目标检测、VIO、SLAM 和自主避障完全可以在没有 LLM/VLM 的情况下实现。

VLM/LLM 的主要价值应优先放在：

- 开放场景理解
- 自然语言交互
- 复杂任务规划
- 多步骤任务编排
- 人机协同

### 判断 4：实时安全链路与认知链路应分层

现阶段工程设计中，不宜让非确定性 VLM/LLM 直接承担毫秒级姿态控制或安全关键闭环。

更合理的结构是：

```text
VLM/LLM/Agent：理解“做什么”
        ↓
任务规划/技能调度：决定“调用什么能力”
        ↓
SLAM/规划/控制：确定“怎么可靠执行”
        ↓
飞控/执行器：完成实时闭环
```

---

## 风险与限制

1. 当前 L1–L5 属于项目自定义框架，需要后续用真实平台和 Benchmark 校正。
2. 不同无人装备的任务差别非常大，不能直接用统一 TOPS 阈值划分。
3. VLM/VLA 发展迅速，目前大量公开成果来自机器人操作而非无人飞行，不能直接外推。
4. 厂商公开的 TOPS、模型 FPS 和功耗测试条件通常不同，后续产品对比必须统一口径。
5. 六摄像头 Case 的分辨率、帧率、算法模型和实时性指标尚需形成明确工作负载基线。

---

## 结论

端侧算力调研应坚持以下顺序：

> **先定义应用和智能能力，再构造工作负载，再推导算力和系统资源，最后做产品选型。**

本项目下一步不应急于制作“大而全的产品 TOPS 排名”，而应先完成六摄像头系统的工作负载模型，并用该模型反向验证不同计算架构。

---

## 待验证问题

1. 六摄像头系统最终分辨率、帧率和同步误差指标是多少？
2. L2 阶段采用哪些检测、跟踪、深度算法作为基准模型？
3. L3 阶段是否需要双目/多目 VIO，还是独立定位相机？
4. SLAM/VIO 与多路检测同时运行时的 CPU、GPU/NPU 占用如何？
5. L4/L5 的 VLM 使用场景是否存在明确任务价值？
6. 无人机本体与边缘计算盒/地面站之间应如何进行算力拆分？

---

## References

1. PX4 Documentation, Computer Vision (Optical Flow, MoCap, VIO, Avoidance)  
   https://docs.px4.io/main/en/advanced/computer_vision

2. PX4 Documentation, Visual Inertial Odometry  
   https://docs.px4.io/main/en/computer_vision/visual_inertial_odometry

3. NVIDIA Isaac ROS  
   https://developer.nvidia.com/isaac/ros

4. NVIDIA Isaac ROS Visual SLAM / cuVSLAM documentation  
   https://nvidia-isaac-ros.github.io/repositories_and_packages/isaac_ros_visual_slam/index.html

5. Nav2 Documentation  
   https://docs.nav2.org/

6. Nav2 Navigation Concepts  
   https://docs.nav2.org/rolling/getting_started/navigation_concepts/

7. Kim et al., OpenVLA: An Open-Source Vision-Language-Action Model, 2024  
   https://arxiv.org/abs/2406.09246
