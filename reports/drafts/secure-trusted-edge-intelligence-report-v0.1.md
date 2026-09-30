# 面向无人装备的安全可信端侧智能计算平台技术调研与产品化建议

> 版本：v0.1（正式报告初稿）  
> 日期：2026-09-30  
> 状态：Phase 3 — Final Report Draft  
> 研究仓库：edge-intelligence-research  
> 说明：本稿已进入正式报告写作阶段。所有关键判断继续遵循 FACT / CASE / BENCH / PAPER / SPEC / INFER / GAP 证据规则；尚未冻结的项目参数不以猜测补齐。

---

# 执行摘要

随着无人机、无人车、无人船、移动机器人和固定式边缘智能设备持续提升自主感知、定位导航和任务决策能力，端侧计算平台正在从“视频处理器”或“单一 AI 推理加速器”演化为同时承担多传感器采集、异构计算、实时任务协同、模型运行和安全可信功能的系统级计算节点。

本次调研不以“哪一种芯片 TOPS 最高”为出发点，而是建立如下需求驱动方法：

```text
应用/任务场景
→ 功能栈
→ 工作负载
→ 数据与实时性需求
→ CPU/GPU/NPU/内存/带宽/接口等系统资源
→ 计算架构
→ 芯片/模组/加速卡/整机
→ Benchmark 与工程验证
```

在此基础上，针对无人装备进一步增加安全可信横向主线：

```text
Mission + Threat Model
→ AI/RT Workload + Trust Requirement
→ Compute Resource + Security Resource
→ Compute Architecture + Trust Architecture
→ Platform + Root of Trust / Crypto
→ Verification + Lifecycle
```

## 一、主要结论

### 1. 无人装备的端侧算力需求本质上是“异构系统资源需求”，而不是一个 TOPS 数字

无人系统通常同时存在视频采集与 ISP、VIO/SLAM、DNN 感知、地图构建、规划优化、控制监督以及可选 VLM/VLA 等负载。不同负载分别依赖 CPU、GPU、NPU、DSP/MCU、ISP/VPU、DDR、Camera/SerDes、PCIe、Ethernet 和实时调度能力。

因此：

> **理论 AI TOPS 只能描述某类算术峰值，不能代表完整无人系统性能。**

平台选择必须至少同时考虑 Sensor/I/O、Real-Time、Memory/DDR、Compute、Concurrency/Tail Latency、SWaP/Thermal 和 Software/Productization 七类 Gate。

### 2. 无人装备智能能力不能简单按统一“L1–L5”与算力绑定

NIST ALFUS、SAE J3016、IMO MASS 等体系的适用边界说明，不同无人系统的自主能力需要结合任务复杂度、环境复杂度和人类参与程度描述。

本项目采用：

> **任务场景 + 功能栈 + 自主性画像 + 工作负载画像**

而不是自创跨领域线性智能等级。

### 3. 当前无人系统的主要端侧负载可归纳为 W1–W9 九类

- W1：Sensor I/O / Video Pipeline
- W2：State Estimation / Localization
- W3：DNN Perception
- W4：3D Mapping / World Representation
- W5：Prediction / Tracking / Situation Understanding
- W6：Planning / Optimization / Decision
- W7：Foundation Model / VLM / LLM / VLA
- W8：Multi-Agent / Fleet / Distributed Computing
- W9：Safety / Control Supervision

典型系统不是选择其中之一，而是多个 workload 并发运行。

### 4. 多摄像头无人系统首先受数据路径、同步和并发架构约束

“六个摄像头”并不意味着“六路都执行同一模型”。

需要首先定义：

```text
C = physical capture cameras
V = VIO/SLAM camera subset
P = PER_VIEW perception subset
F = FUSED_MULTI_VIEW camera subset
D = depth/stereo subset
R = recording subset
```

并区分 PER_VIEW、FUSED_MULTI_VIEW 和 MIXED perception topology。只有明确 Camera Routing，才能正确计算像素率、内存搬运、模型调用率和并发资源。

### 5. 实时性必须从闭环任务反推，而不能只比较单模型 FPS

对避障、自主导航等任务，应计算：

```text
T_reaction =
T_sample
+ T_sensor/ISP
+ T_queue
+ T_perception
+ T_fusion/map
+ T_planner
+ T_command
+ T_vehicle_response

D_reaction = speed × T_reaction
```

真正影响工程可用性的指标是 P95/P99 Frame Age、deadline miss、并发后的尾延迟以及热稳态性能，而不仅是单模型平均推理时间。

### 6. 当前端侧计算已经形成多种成熟产品形态

主要包括：

- Integrated SoC / SoM
- GPU Robotics Computer
- NPU / AI ASIC
- M.2 / PCIe / MXM Accelerator
- Host + Accelerator Heterogeneous Box
- Real-Time Controller + Companion Computer
- Rugged Industrial / Robotics Computer
- Edge Server / Edge-Cloud

不同产品形态解决的问题不同，不能混在同一 TOPS 排名中。

### 7. 对公司而言，更有差异化价值的方向不是复制一款通用 AI 算力盒，而是形成“安全可信无人智能计算平台”

市场上已有大量通用 AI Box、SoM、M.2 accelerator 和工业计算机。若仅从 TOPS、接口和尺寸维度进入，容易陷入同质化。

结合公司已有密码安全和可信技术积累，更值得形成的能力组合是：

> **智能计算 + 实时控制协同 + 密码安全 + 平台可信**

平台可划分为：

- Compute Plane：CPU/GPU/NPU/ISP/VPU
- Real-Time Plane：FCU/MCU/RT subsystem
- Trust Plane：Root of Trust、设备身份、Secure/Measured Boot、密钥、远程证明、模型可信、安全通信、安全升级、物理捕获处置

这类产品的核心价值不再是“提供多少 TOPS”，而是：

> **在无人装备被部署到弱网络、高风险、可能被物理获取的环境中，持续证明设备身份、软件状态和 AI 模型状态可信，并确保关键任务链安全运行。**

### 8. 六摄像头无人平台可作为上述方法的工程验证 Case

当前项目已经确认 6 路 Camera 采集需求，单路 downstream 已观测 1072×1280 NV12，并计划逐步实现同步采集、检测/跟踪、多摄像头融合、深度/障碍检测、VIO/SLAM、避障和自主导航。

但 actual FPS、六路 mode、一部分 workload cardinality、飞行速度、探测距离和整机 SWaP 等参数仍未冻结，因此现阶段不应得出“需要 XX TOPS”的结论。

该项目更适合被用于验证：

> **Requirement → Workload → Resource → Architecture → Gate → Benchmark**

整套方法。

---

# 第一章 调研背景与研究方法

## 1.1 调研背景

无人装备正在从“远程操控设备”逐步向具备本地环境感知、状态估计、自主导航和任务决策能力的智能系统演进。

以无人机为例，早期平台的机载计算主要服务于飞控、视频编码和遥测；随着视觉避障、目标识别、GNSS 拒止导航、多摄像头融合和自主规划的加入，端侧计算平台逐渐需要同时处理：

- 多路 Camera / LiDAR / Radar / IMU 等传感器数据；
- ISP、视频编解码和零拷贝数据通路；
- DNN / Transformer 推理；
- VIO / SLAM / 图优化；
- 地图和世界模型；
- 局部路径规划和避障；
- 任务管理与通信；
- 可选 VLM / VLA / 多模态模型；
- 安全、身份、密钥、可信启动和远程管控。

因此，无人装备端侧计算已经从“AI 加速”问题演化为系统架构问题。

## 1.2 调研需要回答的核心问题

本报告重点回答以下问题：

1. 无人机、无人车、无人船、AMR、机器人和固定式边缘设备当前有哪些典型智能应用；
2. 这些应用对应哪些通用功能和工作负载；
3. 各类 workload 对 CPU、GPU、NPU、Memory、DDR、ISP/VPU、I/O 和实时性提出什么要求；
4. Integrated SoC、Host+Accelerator、Companion Computer、Edge Server 等架构分别适合什么场景；
5. 当前国内外代表性平台和产品已经发展到什么程度；
6. Foundation Model / VLM / VLA 是否会改变端侧计算需求；
7. 无人装备面临哪些安全可信问题；
8. 公司如何利用密码安全和可信计算能力形成差异化产品；
9. 如何通过六摄像头项目和后续 Benchmark 验证这些判断。

## 1.3 研究边界

本调研覆盖：

- UAV / UAS；
- UGV / 自动驾驶与园区无人车；
- USV / 无人船；
- AMR / 移动机器人；
- 操作机器人 / 具身智能；
- 固定式多摄像头边缘智能；
- 多无人平台与边云协同。

六摄像头无人平台仅作为一个工程 Case，不用于代替全行业需求。

## 1.4 研究方法

本报告采用需求驱动路线：

```text
Mission
→ Sensor / Function
→ Workload
→ Resource Budget
→ Latency Budget
→ Architecture Gate
→ Candidate Platform
→ Validation
```

在产品安全方面增加：

```text
Threat Model
→ Trust Requirement
→ Trust Architecture
→ Root of Trust / Crypto
→ Verification / Lifecycle
```

### 1.4.1 Requirement Vector

目标系统至少形成：

```text
R = {
  Mission,
  Sensors,
  DataRate,
  Synchronization,
  WorkloadSet,
  Concurrency,
  UpdateRate,
  Deadline,
  Memory,
  I/O,
  SWaP-C,
  Safety,
  Security,
  Software,
  Productization
}
```

### 1.4.2 证据规则

本报告区分：

- FACT：已有可靠资料支持；
- CASE：命名产品或真实系统案例；
- BENCH：测试条件明确的 Benchmark；
- PAPER：学术论文；
- SPEC：官方规格/开发文档；
- VENDOR：厂商宣称；
- INFER：基于事实的工程推断；
- GAP：证据或需求仍不完整。

产品适配不能仅因“TOPS 足够”直接判定。

## 1.5 为什么不能以 TOPS 为核心

TOPS 通常只描述某种精度和运算类型下的峰值 AI 算力，无法回答：

- Camera 能不能接入；
- ISP 是否足够；
- 视频能不能实时编码；
- VIO 的 CPU/GPU 是否足够；
- DDR 是否被多路图像和模型共享访问压满；
- 多模型并发后 P99 是否失控；
- PCIe accelerator 是否造成额外数据搬运；
- 规划线程能否按 deadline 执行；
- 长时间高温是否降频；
- ROS2、ONNX、PyTorch、厂商 SDK 是否成熟；
- Secure Boot、设备身份、模型保护是否具备。

因此本报告将 TOPS 作为“计算规格之一”，而不是选型主轴。

---

# 第二章 无人装备智能化应用与计算任务

## 2.1 通用自主系统功能栈

综合 PX4、Nav2、Autoware 及无人系统相关综述，本报告采用以下功能栈：

```text
F1 Sensing / Data Acquisition
        ↓
F2 State Estimation / Localization
        ↓
F3 Mapping / World Modeling
        ↓
F4 Perception
        ↓
F5 Prediction / Situation Understanding
        ↓
F6 Planning / Decision
        ↓
F7 Control / Execution
```

横向还包括：

- F8 Mission / HMI / Remote Operation；
- F9 Multi-Agent / Fleet / Collaboration；
- F10 Safety / Security / Health。

其中 F10 不是“更高等级的智能”，而是产品化系统必须考虑的横向能力。

## 2.2 UAV / UAS

当前 UAV 典型任务包括：

- 巡检、测绘、监视；
- 搜索救援；
- 物流运输；
- 环境监测；
- 应急响应；
- GNSS 拒止导航；
- 多机协同。

典型功能逐步由：

```text
飞控 + GNSS/INS
```

扩展为：

```text
Camera/IMU
→ VIO/SLAM
→ Obstacle Perception
→ Local Map
→ Planning
→ Collision Avoidance
→ Autonomous Mission
```

无人机的主要约束是 SWaP、续航、振动、同步和网络不可用时的本机闭环能力。

## 2.3 UGV / 自动驾驶与园区车辆

该类系统通常具备更高功耗预算，但同时有更多 Camera、LiDAR、Radar 和更复杂的安全需求。

完整链路通常包括：

```text
Sensing
→ Localization
→ Perception
→ Prediction
→ Planning
→ Control
```

随着 BEV、Occupancy、Transformer、E2E driving 等方法发展，车端算力从单一感知推理逐渐转向时空多模态融合和大内存异构计算。

## 2.4 AMR / 移动机器人

AMR 的典型任务为：

- 仓储物流；
- 制造物料运输；
- 巡检；
- 服务机器人；
- 多机器人协同。

核心能力包括 Localization & Mapping、Global/Local Planning、Motion Control 和 Fleet Coordination。

与道路车辆相比，AMR 环境通常更结构化，但长期连续运行、多机调度、人机混行和地图变化是重要工程问题。

## 2.5 USV / 无人船

USV 常见任务包括：

- 海洋测绘；
- 环境监测；
- 巡检；
- 监视；
- 科研和工程作业。

其特有负载包括：

- Radar / AIS / Camera / GNSS 融合；
- 海况与天气处理；
- COLREGs 约束下的避碰；
- 长航时和远距离通信。

## 2.6 操作机器人与具身智能

传统操作机器人重点是：

- 目标识别与姿态估计；
- Motion Planning；
- Manipulation；
- Force / Impedance Control。

近年来 VLM/VLA 开始进入机器人任务理解和动作策略，例如 PaLM-E、RT-2、OpenVLA、GR00T 等路线。

但这说明“Foundation Model 已成为真实技术路线”，并不意味着所有无人装备都必须运行大模型。

## 2.7 固定式边缘智能

固定边缘设备可能没有定位、规划和控制，但会产生极重的视频负载：

- 多路视频采集；
- 解码/编码；
- Detection；
- Tracking；
- Cross-camera analytics；
- 可选 VLM 语义检索。

因此“算力大”与“自主程度高”不是同一概念。

## 2.8 自主性描述

跨领域不采用统一 L1–L5，而使用三个维度描述：

- Mission Complexity；
- Environmental Complexity；
- Human Independence。

这样可以避免把不同无人系统的能力强行投影到一个失真的等级轴上。

---

# 第三章 典型工作负载与组合模型

## 3.1 W1：Sensor I/O / Video Pipeline

包括：

- Camera capture；
- ISP；
- HDR / denoise；
- resize / crop / color conversion；
- encode / decode；
- timestamp / synchronization；
- DMA / zero-copy。

主要资源：

- ISP / VPU；
- DDR；
- Camera / MIPI / SerDes / Ethernet；
- DMA 和内存 fabric；
- CPU 驱动。

关键指标：

- Pixel/s；
- image-plane MB/s / GB/s；
- timestamp jitter；
- dropped frame；
- codec channels；
- host copy count。

## 3.2 W2：State Estimation / Localization

包括：

- EKF / UKF；
- GNSS/INS；
- Optical Flow；
- VO / VIO；
- LiDAR-Inertial Odometry；
- NDT / map matching。

主要依赖：

- CPU；
- SIMD/GPU；
- 低延迟内存；
- 高精度同步；
- 实时调度。

因此 W2 不能用 NPU TOPS 替代。

## 3.3 W3：DNN Perception

包括：

- Detection；
- Classification；
- Segmentation；
- Depth；
- Pose；
- Free-space；
- 多模态感知。

主要资源：

- NPU/GPU；
- DDR；
- ISP/预处理；
- CPU 后处理；
- Model Runtime / Compiler。

需要同时记录模型、输入尺寸、精度、batch/stream mode、前后处理和并发流数量。

## 3.4 W4：Mapping / World Representation

包括：

- SLAM；
- Occupancy Grid；
- Point Cloud Map；
- 3D Reconstruction；
- BEV / Occupancy；
- Semantic Map。

这类任务往往同时消耗 CPU/GPU、内存容量和 DDR。

## 3.5 W5：Prediction / Tracking / Situation Understanding

包括：

- Multi-object Tracking；
- Trajectory Prediction；
- Intent Prediction；
- Scene Understanding；
- Semantic Reasoning。

随着时序 Transformer 和多模态模型加入，W5 对内存和时序历史状态的需求明显增加。

## 3.6 W6：Planning / Optimization / Decision

包括：

- A* / Dijkstra；
- RRT / RRT*；
- trajectory optimization；
- MPC；
- behavior planning；
- learned policy / RL。

这一 workload 更应关注 worst-case latency 和 deadline，而不是平均吞吐。

## 3.7 W7：Foundation Model / VLM / LLM / VLA

典型任务：

- 开放词汇场景理解；
- 自然语言指令；
- 任务分解；
- Long-horizon Planning；
- Vision-Language-Action。

主要新增资源：

- 大内存容量；
- 高内存带宽；
- INT4 / INT8 / FP8 / FP16；
- KV Cache；
- multimodal encoder；
- TTFT / token generation。

W7 不应默认进入 hard real-time safety loop。

## 3.8 W8：Multi-Agent / Fleet

包括：

- task allocation；
- fleet scheduling；
- cooperative perception；
- collaborative mapping；
- swarm coordination。

除计算外，网络 QoS、分布式状态和身份安全成为系统资源。

## 3.9 W9：Safety / Control Supervision

包括：

- Flight / Motion Control；
- supervisor；
- fault detection；
- health monitoring；
- emergency fallback。

这类 workload 强调确定性、Worst-Case Latency 和故障隔离。

## 3.10 Workload Composition

为避免把 workload 误解为能力等级，本报告定义五种典型组合。

### C1 Multi-Camera Analytics

```text
W1 + W3 + W5 (+ W7 on-demand)
```

适合固定式边缘、多路视频分析。

### C2 Visual Autonomy

```text
W1 + W2 + W3 + W4 + W6 + W9
```

适合视觉自主 UAV、AMR、多摄像头避障。

### C3 Multi-Sensor Autonomy

```text
W1 + W2 + W3 + W4 + W5 + W6 + W9
```

适合自动驾驶、Radar/Camera/LiDAR 融合系统。

### C4 Foundation-Model Augmented Robotics

```text
Base Autonomy Composition + W7
```

Foundation Model 是增量 workload，而不是替代底层安全闭环。

### C5 Cooperative Autonomy

在单机 autonomy 基础上叠加 W8，用于多无人平台协同。

---

# 第四章 从工作负载推导端侧系统资源

## 4.1 先算数据，再算 AI

对多摄像头系统：

```text
PixelRate = Σ(N × Width × Height × FPS)

ImagePayload =
PixelRate × bytes_per_pixel
```

但必须进一步区分：

- Sensor physical link；
- ISP output；
- DDR image-plane；
- codec read/write；
- resize / copy；
- AI tensor；
- recording。

同一帧图像被多个 consumer 重复读取时，DDR working traffic 可能显著高于单份 image payload。

## 4.2 Camera Routing Set

多摄像头系统先定义：

```text
C = Capture
V = VIO
P = Per-view perception
F = Fused multi-view
D = Depth
R = Recording
```

集合可重叠。

禁止直接使用：

```text
N_capture = N_detection = N_vio = N_depth = N_record
```

## 4.3 Perception Topology

### PER_VIEW

每路独立模型：

```text
InferenceRate =
N_detection × detection_hz
```

### FUSED_MULTI_VIEW

一次 model call 消费多个 views：

```text
ModelCallRate = perception_update_hz

InputViewRate =
N_views_per_call × perception_update_hz
```

因此六路输入不等于每个周期六次独立 inference。

## 4.4 CPU

CPU 主要承担：

- 驱动和系统编排；
- ROS2 / middleware；
- VIO / 图优化；
- tracking 后处理；
- planning；
- network / storage；
- AI runtime orchestration。

对自主系统，CPU 的 P95/P99 和 scheduler 行为往往比平均占用率更关键。

## 4.5 GPU

GPU 可能承担：

- VIO / SLAM 并行计算；
- Depth；
- Point Cloud；
- BEV / Occupancy；
- CUDA/OpenCL 算法；
- Transformer；
- VLM/VLA。

因此拥有高 NPU TOPS 但 GPU/CPU 较弱的平台，不一定适合复杂 Visual Autonomy。

## 4.6 NPU / AI ASIC

NPU 适合：

- Detection；
- Segmentation；
- Depth 网络；
- Transformer；
- 部分 LLM/VLM。

但实际能力取决于：

- 算子覆盖；
- compiler；
- precision；
- tensor layout；
- dynamic shape；
- multi-context / multi-stream；
- pre/post；
- host integration。

## 4.7 内存容量

运行内存必须容纳：

```text
OS
+ Runtime
+ Model Weights
+ Activation / Workspace
+ Camera Buffers
+ VIO / SLAM State
+ Map
+ Queues
+ VLM KV Cache（如有）
+ Safety Margin
```

因此不能用“模型文件大小”代表系统内存需求。

## 4.8 DDR 带宽

建议预算：

```text
BW_working ≈
Σ(image/tensor bytes × effective passes)
+ map/SLAM
+ codec
+ CPU/GPU/NPU shared traffic
+ runtime overhead
```

LPDDR 标称峰值仅可作为物理上限参考，不能直接作为可持续业务带宽。

## 4.9 ISP / VPU

多 Camera 场景往往首先受到 ISP/VPU 约束。

需要确认：

- input lanes / virtual channels；
- simultaneous Camera；
- HDR / 3A；
- resize / colorspace；
- H.264/H.265 encode/decode；
- hardware timestamp；
- zero-copy。

这些能力无法通过外置 NPU 补齐。

## 4.10 I/O

需要按系统拓扑验证：

- MIPI CSI；
- GMSL / FPD-Link；
- PCIe；
- Ethernet；
- USB；
- CAN / CAN-FD；
- UART / SPI / I2C / GPIO。

接口数量不是唯一问题，还需要考虑实际 lane、switch、bridge、timestamp 和带宽共享。

## 4.11 闭环时延

对于避障、自主导航：

```text
T_total =
T_sample
+ T_sensor/ISP
+ T_queue
+ T_preprocess
+ T_W2/W3/W4
+ T_W6
+ T_command
+ T_vehicle
```

反向求平台 deadline：

```text
T_pipeline,max =
(D_detect - D_keepout - D_maneuver) / v
- 1/f_sensor
- T_vehicle
```

因此平台是否满足需求，应由 P95/P99 Frame Age 与系统闭环约束判断。

## 4.12 并发与 Service Demand

多 workload 并发时可先按 compute engine 做初筛：

```text
Demand_engine =
Σ(InvocationRate_i × measured ServiceTime_i)
```

但 Demand < 1 不意味着实时性一定满足，还需要考虑：

- batching；
- pipeline overlap；
- DDR contention；
- PCIe；
- runtime scheduling；
- queue；
- thermal throttling。

---

# 第五章 端侧计算技术路线

## 5.1 Integrated Heterogeneous SoC / SoM

典型特征：

```text
CPU + GPU/NPU + ISP/VPU + Memory + I/O
```

优势：

- 数据路径短；
- 共享内存；
- 板级复杂度较低；
- 更适合 SWaP 受限平台。

风险：

- 算法生态受厂商约束；
- CPU/GPU/NPU 资源可能互相争抢 DDR；
- SKU 的 Camera/安全能力必须逐项核实。

适合：

- UAV companion computer；
- AMR；
- 小型机器人；
- 集成视觉节点。

## 5.2 GPU Edge Computer

代表路线以 Jetson 类平台为典型。

优势：

- 通用 GPU；
- CUDA/TensorRT/Isaac ROS 等成熟生态；
- 多模型、VIO、Depth、Transformer 等异构 workload 更容易统一部署。

限制：

- 功耗和散热；
- 小型 UAV SWaP；
- 成本；
- 国产化要求。

## 5.3 NPU / AI ASIC

优势：

- 高能效；
- DNN throughput；
- 小尺寸 accelerator。

限制：

- 不能代替 Host；
- 非 DNN workload 支持有限；
- 编译器和算子覆盖决定实际模型可用性。

## 5.4 Host + Accelerator

结构：

```text
Sensor
→ Host ISP/VPU
→ Host DDR / Preprocess
→ PCIe
→ Accelerator
→ Host Postprocess
→ VIO / Mapping / Planner
```

适合：

- 现有 Host AI 能力不足；
- W3/W7 可清晰卸载；
- 需要可扩展模块化产品。

关键问题：

- H2D/D2H；
- PCIe latency；
- copy；
- Host CPU/DDR；
- 总功耗和热；
- system-level P99。

“160 TOPS M.2 卡”不能等价为“160 TOPS 无人机计算平台”。

## 5.5 Real-Time Controller + Companion Computer

无人平台常见结构：

```text
FCU / MCU / RTOS
        ↕
Companion AI Computer
```

FCU 负责：

- flight/motion control；
- actuator；
- hard real-time loop；
- failsafe。

Companion 负责：

- perception；
- VIO/SLAM；
- map；
- planning；
- mission intelligence。

这种分区可以避免 Linux/AI workload 直接侵入安全关键硬实时控制链。

## 5.6 Edge Server / Edge-Cloud

适合：

- 大型无人平台；
- 多机器人；
- 全局任务规划；
- 非实时大模型；
- 地图融合；
- fleet intelligence。

必须设计断网降级和本地最小安全能力。

---

# 第六章 主流端侧计算产品与解决方案现状

## 6.1 产品分类原则

本报告区分：

- Dev Kit / EVK；
- Production SoM/Core；
- Carrier/Development Board；
- M.2/PCIe/MXM Accelerator；
- Robotics/Industrial Computer；
- Heterogeneous Edge Box；
- Edge Server；
- Solution Ecosystem。

不同类别不能直接横向用 TOPS 排序。

## 6.2 高集成 SoM / Robotics Platform

当前代表性路线包括：

- NVIDIA Jetson Orin / Thor；
- Qualcomm Dragonwing IQ-9075；
- RK3588 / RK3588J；
- Huawei Atlas 200I A2；
- SOPHGO BM1688；
- AMD Kria K26；
- 自动驾驶专用 SoC 等。

它们体现的共同趋势是：

> **CPU/GPU/NPU/ISP/视频/实时子系统正在向高集成异构计算发展。**

## 6.3 Independent Accelerator

代表：

- Houmo LQ50 / M50；
- Axelera Metis；
- Hailo-10H；
- Cambricon MLU220 M.2 等。

这类产品适合增加 DNN 或 Foundation Model 能力，但最终系统仍必须描述 Host。

## 6.4 Host + Accelerator 已进入产品化

Firefly AIBOX PRO 等现成产品说明：

```text
RK3588 / RK3576 Host
+
M.2 AI Accelerator
```

已经是现实工程路线，而不是理论组合。

其价值在于：

- Host 负责 Camera/ISP/CPU workload；
- Accelerator 增加 W3/W7 能力；
- 产品可按任务模块化扩展。

但 exact Camera/VIO/P99 仍必须测试。

## 6.5 Rugged Robotics / Industrial Computer

Seeed、Advantech 等产品说明工业机器人平台已经将：

- GMSL；
- CAN；
- 宽压；
- M12；
- fanless；
- industrial temperature

等能力产品化。

这类系统更适合 UGV、USV、工业机器人和固定边缘；对小型 UAV 仍受重量和功耗限制。

## 6.6 国产化观察

目前国内已覆盖：

### Integrated SoC / Module

- RK3588；
- BM1688；
- Atlas 200I A2；
- 车规/机器人 SoC。

### Accelerator

- Houmo LQ50；
- Cambricon MLU 等。

### Heterogeneous Complete Box

- RK Host + 国产 accelerator。

这表明国产路线已经从“单芯片”逐渐扩展到 SoM、加速卡和完整异构边缘盒。

当前主要短板不是缺少 TOPS，而是公开工程证据仍不足，尤其包括：

- Physical multi-camera；
- VIO/SLAM；
- ROS2；
- heterogeneous workload concurrency；
- P95/P99；
- SWaP；
- 长时间热稳定性。

---

# 第七章 安全可信型无人装备端侧智能计算平台

## 7.1 为什么安全可信不能作为附加功能

无人装备可能工作在：

- 弱网络；
- 无人值守；
- 对抗环境；
- 高价值任务；
- 可能被物理获取的环境。

端侧计算节点不仅处理算法，也保存：

- 设备身份；
- 任务配置；
- 地图；
- 视频；
- AI 模型；
- 密钥；
- 控制链路凭据。

因此安全不能只等价为“通信加密”或“增加安全芯片”。

## 7.2 主要威胁

包括：

- 非法设备/节点接入；
- 固件/OS/应用替换；
- AI 模型/参数替换；
- 敏感数据泄露；
- 控制命令注入；
- ROS topic/service 越权；
- 物理捕获/拆卸；
- 恶意应用横向移动；
- 合法证书对应的软件栈已失陷；
- 恶意/回滚升级；
- Fleet 中失陷节点继续参与协同。

## 7.3 安全可信能力向量

建议至少形成：

- S1 Hardware Root of Trust；
- S2 Device Identity & Key；
- S3 Secure Boot & Anti-Rollback；
- S4 Measured Boot / Runtime Integrity；
- S5 Remote Attestation；
- S6 Secure Storage / Data Protection；
- S7 Trusted Runtime / Isolation；
- S8 Secure Communication & Access Control；
- S9 Secure Update & Recovery；
- S10 AI Artifact Trust；
- S11 Physical Capture Resistance；
- S12 Fleet Trust Management。

## 7.4 Safety 与 Security 必须分开

功能安全常关注：

- lockstep；
- ECC；
- watchdog；
- ASIL；
- fault detection。

Cybersecurity / Trust 关注：

- Secure Boot；
- Root of Trust；
- TEE；
- TPM/TCM；
- key storage；
- attestation；
- identity。

两者可以协同，但不能相互替代。

## 7.5 Trust Plane

建议产品采用：

```text
             Ground / Fleet Trust Service
      CA / KMS / Verifier / Policy / OTA
                      │
                      ▼
┌──────────────────────────────────────────────┐
│ Secure Trusted Edge Intelligence Node       │
│                                              │
│ Trust Plane                                  │
│ Root of Trust / SE / TPM/TCM / TEE          │
│ Identity / Key / Measurement / Attestation   │
│ Model Verify / Secure Storage / Crypto       │
│                                              │
│ Compute Plane                                │
│ CPU / GPU / NPU / ISP / VPU                 │
│ ROS2 / AI Runtime / VIO / Planner            │
│                                              │
│ Real-Time Plane                              │
│ FCU / MCU / RT subsystem                     │
└──────────────────────────────────────────────┘
```

## 7.6 TEE、TPM/TCM、商密安全芯片的边界

### Secure Boot

回答：

> 未授权软件能否启动？

### TEE

回答：

> 高权限 OS/应用失陷后，敏感服务是否仍可隔离？

### TPM/TCM

更适合：

- measurement；
- PCR；
- sealed key；
- quote；
- remote attestation。

### 商密 SE / 安全芯片

更适合：

- SM2/SM3/SM4；
- TRNG；
- device key；
- certificate；
- non-exportable key。

一个普通商密安全芯片不能自动替代完整 TPM/TCM。

## 7.7 AI Artifact Trust

建议把以下对象纳入可信链：

```text
Model Weight
+ Model Manifest
+ Runtime Version
+ Config
+ Threshold
+ Pre/Post
+ Planner Parameters
```

至少实现：

- 签名；
- hash；
- version；
- authorization；
- load-time verification；
- rollback control。

进一步可将 model key / mission key 的释放绑定到 platform attestation result。

## 7.8 Physical Capture

无人装备失陷后，需要考虑：

- debug lock；
- encrypted storage；
- non-exportable keys；
- tamper event；
- credential revocation；
- mission key rotation；
- remote deny / decommission policy。

这类能力是无人装备区别于普通机房 Edge AI Server 的重要产品特征。

---

# 第八章 面向典型任务的配置思路

## 8.1 配置 A：Multi-Camera Analytics Node

Workload：

```text
W1 + W3 + W5
```

资源重点：

- ISP/VPU；
- DDR；
- NPU；
- video codec；
- network/storage。

适合：

- 固定多摄；
- 视频智能；
- 非自主导航任务。

架构可选：

- Integrated SoC；
- Host + Accelerator；
- Edge Server。

## 8.2 配置 B：Visual Autonomy Companion Computer

Workload：

```text
W1 + W2 + W3 + W4 + W6 + W9
```

资源重点：

- Camera/IMU sync；
- CPU；
- GPU/NPU；
- DDR；
- tail latency；
- FCU interface。

适合：

- UAV；
- AMR；
- 小型机器人。

建议采用：

```text
Companion AI Computer + Independent FCU/MCU
```

## 8.3 配置 C：Multi-Sensor Autonomy Platform

在 Visual Autonomy 上增加：

- LiDAR；
- Radar；
- W5 Prediction；
- 更大 world model。

更适合高性能 SoC、车规计算平台或多计算单元架构。

## 8.4 配置 D：Foundation-Model Augmented Platform

在 C1/C2/C3 上增量叠加 W7。

资源新增：

- 16GB/32GB 乃至更高内存容量；
- 大模型量化；
- KV cache；
- visual encoder；
- resource isolation。

工程原则：

> VLM/VLA 应首先作为任务理解、语义理解和非硬实时规划的增强层，不应未经验证直接替代安全关键底层闭环。

## 8.5 配置 E：Secure Trusted Unmanned Compute Platform

在上述任一计算配置上增加：

- Root of Trust；
- Device Identity；
- Secure/Measured Boot；
- Model Trust；
- Secure Communication；
- Remote Attestation；
- Secure Update；
- Physical Capture Handling。

这应成为公司后续产品化重点方向。

---

# 第九章 六摄像头无人平台 Case Study

## 9.1 已确认输入

当前确认：

| 参数 | 当前状态 |
|---|---|
| N_capture | 6 |
| downstream width | 1072 |
| downstream height | 1280 |
| downstream format | NV12 |
| actual FPS | GAP |
| 六路 mode 一致性 | GAP |
| Sensor RAW | GAP |
| multi-camera sync | 已确认需求方向 |

禁止将 downstream NV12 直接解释为 Sensor RAW。

## 9.2 单份 Image-Plane Payload 敏感性

仅使用已观测 1072×1280 NV12 做算术：

| FPS | 六路 Pixel Rate | 单份 NV12 Image-Plane Payload |
|---:|---:|---:|
| 10 | 82.33 MP/s | 123.49 MB/s |
| 20 | 164.66 MP/s | 246.99 MB/s |
| 30 | 246.99 MP/s | 370.48 MB/s |
| 60 | 493.98 MP/s | 740.97 MB/s |
| 120 | 987.96 MP/s | 1481.93 MB/s |

这些数字只代表一份 image representation，不代表真实 DDR traffic。

## 9.3 能力包

### Package A — Capture / Sync / Video

```text
W1
+ 6 Camera
+ Synchronization
+ Optional Encode
```

首先检查 Camera subsystem，而不是 NPU。

### Package B — Detection / Tracking

增加：

- W3；
- W5。

需要冻结：

- N_detection；
- model；
- input；
- precision；
- detection Hz；
- topology。

### Package C — Obstacle / Depth / Local Avoidance

增加：

- depth / obstacle；
- W4 local map；
- W6 local planning；
- W9 safety。

此时必须进入闭环 latency 分析。

### Package D — VIO / SLAM / Navigation

增加：

- W2；
- W4；
- W6；
- Camera/IMU synchronization。

CPU/GPU 需求会显著提高。

### Package E — Optional VLM

W7 作为增量能力，不进入基础安全闭环。

## 9.4 当前候选架构

### Candidate 1：Integrated RK3588

```text
6 Camera
→ ISP/VPU
→ DDR
→ NPU + CPU/GPU
→ FCU
```

优势：

- 高集成；
- 成本和生态；
- 视频能力。

GAP：

- exact six-camera ingest；
- W2+W3 concurrency；
- DDR；
- thermal；
- P99 Frame Age。

### Candidate 2：Jetson Orin

优势：

- CUDA/TensorRT；
- Isaac ROS；
- VSLAM/Depth/Mapping 生态；
- 多 workload 能力。

GAP：

- 本项目 exact 6-camera mode；
- 目标 SWaP；
- full stack concurrency。

### Candidate 3：IQ-9075

优势：

- 多 Camera SoC capability；
- robotics orientation；
- RT subsystem；
- ROS/Linux 路线。

GAP：

- 本项目 physical multi-camera；
- VIO numeric latency；
- 国内产品成熟度/供应链。

### Candidate 4：RK3588 Host + Accelerator

职责：

```text
RK3588:
W1 + W2 + W4 + W6

Accelerator:
W3
(+ W7)
```

优势：

- 可扩展；
- 可以显著增加 DNN/大模型能力。

风险：

- PCIe；
- Host DDR；
- H2D/D2H；
- 板级和热设计；
- 系统 P99。

## 9.5 安全可信扩展

六摄平台可以作为 Trust Plane 工程验证平台，逐步加入：

1. 设备唯一身份；
2. Secure Boot；
3. 模型签名和完整性；
4. 模型密钥；
5. FCU—Companion 双向认证；
6. ROS2/DDS policy；
7. encrypted mission data；
8. remote attestation；
9. secure OTA；
10. lost/captured device revocation。

这样六摄项目不只是一个避障 Demo，而可成为：

> **安全可信无人智能计算节点的系统级验证平台。**

## 9.6 当前不能形成的结论

现阶段不能声称：

- 六摄需要固定 XX TOPS；
- 160 TOPS 卡一定比 6 TOPS SoC 更适合；
- Jetson 一定具有最低系统延迟；
- 一体 SoC 一定低于 Host+Accelerator；
- VLM 是基础无人机必需能力。

这些都需要先冻结 Requirement Vector 并完成实测。

---

# 第十章 技术发展趋势

## 10.1 多传感器与时空融合

感知正在从单帧、单 Camera 检测向：

- multi-camera；
- temporal fusion；
- LiDAR/Radar；
- BEV；
- Occupancy

发展。

影响：

- DDR 增加；
- 多模型并发；
- Transformer 比例上升；
- calibration / sync 重要性提升。

## 10.2 模块化系统与 End-to-End 并存

未来一段时间更可能是：

```text
Classical / Modular Safety Backbone
+
Learned Perception / Prediction / Planning
```

而不是所有传统模块一次性被 E2E 替代。

## 10.3 VLM / VLA

VLM/VLA 将推动机器人具备：

- open-vocabulary understanding；
- natural language interaction；
- semantic task planning；
- long-horizon reasoning。

但端侧应用受到：

- memory；
- bandwidth；
- latency；
- power；
- safety verification

约束。

## 10.4 World Model

World Model 更适合：

- prediction；
- planning；
- simulation；
- data generation；
- policy learning。

其完整训练和大规模推理未必都在无人装备本机完成，端侧可能更多部署压缩后的预测和策略模型。

## 10.5 多机器人协作

未来单机平台将逐渐成为 fleet system 中的节点。

因此计算平台需要同时支持：

- local autonomy；
- peer communication；
- distributed state；
- task allocation；
- cooperative perception；
- identity；
- trust posture。

## 10.6 Edge-Cloud

工程趋势不是“所有计算上云”，而是明确：

- hard real-time / safety：必须本地；
- mission-critical perception：优先本地；
- global optimization：可近边缘；
- training / large knowledge：可云端。

必须设计网络退化模式。

## 10.7 安全与 AI 平台深度融合

未来端侧 AI 产品的竞争点将逐步从：

> 只有算力

转向：

> **算力 + 数据链路 + 软件栈 + 生命周期 + Security / Trust。**

---

# 第十一章 对后续产品研发的建议

## 11.1 产品定位

不建议把产品定义为：

> “一款 XX TOPS 的国产 AI 算力盒。”

更建议定义为：

> **面向无人装备的安全可信端侧智能计算平台。**

目标是把公司已有安全密码技术与无人智能计算结合，形成区别于通用 AI Box 的产品能力。

## 11.2 推荐产品架构

建议采用三平面：

### Real-Time Plane

- MCU / FCU；
- real-time task；
- safety supervisor；
- failsafe。

### Compute Plane

- CPU；
- GPU/NPU；
- ISP/VPU；
- Camera；
- ROS2；
- VIO/SLAM；
- AI Runtime；
- Planning。

### Trust Plane

- Root of Trust；
- SM2/SM3/SM4/TRNG；
- Device Identity；
- Key Lifecycle；
- Secure Boot；
- Measured Boot；
- Attestation；
- Secure Storage；
- Model Trust；
- Communication Security；
- OTA；
- Capture Response。

## 11.3 建议形成平台化而非单一 SKU

### 轻量型

目标：

- UAV；
- 小型机器人；
- 多 Camera；
- 低功耗。

特点：

- 10–30W 级系统目标应作为后续产品定义变量；
- Integrated SoC 优先；
- 独立 FCU；
- 基础 Trust Plane。

### 高性能型

目标：

- UGV；
- USV；
- 高级机器人；
- VLM/VLA。

特点：

- 大内存；
- GPU/NPU；
- 多 sensor；
- 高速网络；
- 更完整 Trust Plane。

### Accelerator 扩展型

采用：

```text
Host + M.2 / PCIe AI Accelerator
```

适用于产品系列扩算力。

但 Host 应作为产品的一等变量。

## 11.4 安全能力产品化建议

建议把底层不同安全器件统一抽象为 Trust Service API，例如：

```text
/device/identity
/crypto/sign
/crypto/encrypt
/key/unseal
/model/verify
/platform/measure
/platform/attest
/update/verify
/security/event
```

上层 AI/ROS/mission 应用不直接绑定特定 TPM、TEE 或商密安全芯片。

这种抽象有利于：

- 换 SoC；
- 换安全器件；
- 国产化；
- 产品系列复用；
- 统一安全 SDK。

## 11.5 Benchmark 建议

后续平台选型必须建立统一测试条件。

### B1 Camera / Video

- 多路同步采集；
- drop；
- jitter；
- ISP；
- encoding；
- DDR。

### B2 VIO / SLAM

- EuRoC / TUM-VI；
- trajectory accuracy；
- CPU/GPU；
- latency。

### B3 DNN

- YOLO；
- identical model/input/precision；
- latency；
- FPS；
- power。

### B4 Multi-Workload Concurrency

```text
Camera
+ VIO
+ Detection
+ Depth
+ Planner
```

重点测：

- P50/P95/P99；
- Frame Age；
- deadline miss；
- DDR；
- power。

### B5 Host + Accelerator

测试：

- H2D/D2H；
- PCIe；
- copy；
- pre/post；
- end-to-end。

### B6 Thermal

- 30min / 1h / 2h；
- temperature；
- clock；
- throttling；
- sustained FPS。

### B7 Security / Trust

- Boot tamper；
- image/model tamper；
- attestation；
- key non-exportability；
- rollback；
- unauthorized ROS2/MAVLink access；
- device capture / revoke。

## 11.6 六摄项目近期优先事项

当前最值得优先冻结：

1. 实际 Camera FPS；
2. 六路 mode；
3. N_detection；
4. N_vio；
5. N_depth；
6. N_record；
7. 飞行速度；
8. usable detection range；
9. vehicle response；
10. 计算节点功耗、尺寸和重量边界。

冻结这些变量的价值高于继续扩充更多芯片型号。

## 11.7 产品路线建议

### 第一阶段：计算平台验证

目标：

- 六 Camera；
- Detection；
- VIO/SLAM；
- 避障；
- FCU interface。

建立系统 Benchmark。

### 第二阶段：安全可信融合

加入：

- secure identity；
- Secure Boot；
- model verify；
- crypto service；
- secure communication；
- encrypted storage。

### 第三阶段：Trust Plane

加入：

- measured boot；
- attestation；
- model key policy；
- fleet CA/KMS/verifier；
- secure OTA；
- capture response。

### 第四阶段：平台系列化

形成：

- Lightweight UAV Node；
- High-Performance Robotics Node；
- Host+Accelerator Expansion；
- Fleet Trust Service。

---

# 结论

无人装备端侧智能计算的核心问题不是“需要多少 TOPS”，而是：

> 在给定任务、传感器、实时性、功耗、尺寸和安全约束下，系统需要运行哪些 workload，这些 workload 如何竞争 CPU/GPU/NPU/DDR/I/O，什么计算架构才能稳定完成闭环任务。

当前产业已经能够提供高集成 SoC、GPU 平台、独立 AI accelerator、Host+Accelerator 和工业机器人整机等多种技术路线。单纯复制现有通用算力盒并不能形成明显差异。

结合无人装备的真实运行环境以及公司的技术基础，更值得进一步推进的产品方向是：

> **以异构端侧智能计算为基础，以实时控制协同为边界，以商用密码和 Root of Trust 为可信根，建立覆盖设备身份、启动链、AI 模型、通信、升级、远程证明和失陷处置的安全可信无人装备智能计算平台。**

六摄像头无人平台可以作为第一阶段工程验证载体，通过真实 Camera、VIO、DNN、Depth、Planner 和 FCU 闭环逐步形成可复现的系统 Benchmark，并以此反向确定最终硬件架构和产品规格。

---

# References / 仓库证据入口

## 场景与功能
- [无人系统端侧智能应用、功能栈与自主性框架](../../research/scenarios/unmanned-intelligence-scenarios.md)
- [应用—工作负载矩阵](../../research/scenarios/application-workload-matrix.md)

## Workload 与资源
- [W1–W9 Workload Taxonomy](../../research/workloads/workload-taxonomy.md)
- [Workload Composition Library](../../research/workloads/workload-composition-library.md)
- [系统资源预算模型](../../research/workloads/system-resource-budget-model.md)
- [避障闭环时延预算](../../research/workloads/avoidance-latency-budget.md)
- [C2 Visual Autonomy Resource Envelope](../../research/workloads/c2-visual-autonomy-resource-envelope.md)

## 架构
- [需求驱动架构选型](../../research/architecture/requirements-to-architecture-selection.md)
- [Host + Accelerator Architecture](../../research/architecture/host-accelerator-edge-architecture.md)
- [Closed-loop Latency Platform Mapping](../../research/architecture/closed-loop-latency-platform-mapping.md)

## 产品
- [Commercial Product Landscape 2026](../../research/products/commercial-product-landscape-2026.md)
- [Representative Edge Compute Platforms](../../research/products/representative-edge-compute-platforms.md)
- [Workload → Platform Fit Matrix](../../research/products/workload-platform-fit-matrix.md)
- [Platform Facts CSV](../../data/product-specs/platform-facts.csv)

## 安全可信
- [安全可信型无人装备端侧智能计算平台](../../research/architecture/secure-trusted-edge-intelligence-platform.md)
- [Trust Plane Implementation Options](../../research/architecture/trust-plane-implementation-options.md)
- [Security Trust Capability Matrix](../../data/product-specs/security-trust-capability-matrix-2026.csv)

## 六摄像头 Case
- [Six-camera UAV README](../../cases/six-camera-uav/README.md)
- [Phase 2 Requirement Card](../../cases/six-camera-uav/phase-2-requirement-card.md)
- [Camera Workload Routing](../../cases/six-camera-uav/phase-2-camera-workload-routing.md)
- [Candidate Architecture Resource Map](../../cases/six-camera-uav/phase-2-candidate-architecture-resource-map.md)
- [Architecture Gate Matrix](../../cases/six-camera-uav/phase-2-architecture-gate-matrix.md)
- [Validation Plan](../../cases/six-camera-uav/phase-2-validation-plan.md)
- [Security Threat Model and Trust Flow](../../cases/six-camera-uav/security-threat-model-and-trust-flow.md)

---

## 下一版重点

v0.2 重点继续完成：

1. 将第6章产品现状收敛为“产品形态 + 代表性平台 + 对应 Workload”对比表；
2. 将第7章 Trust Plane 补成正式产品技术架构图与能力表；
3. 将第9章六摄 Case 补充 Camera Routing、资源预算和 Candidate Gate 总表；
4. 将 References 转为正式编号引用格式；
5. 生成方法论、三平面架构、六摄数据流等核心图；
6. 对正文逐条执行 evidence audit，避免 INFER 被写成 FACT。
