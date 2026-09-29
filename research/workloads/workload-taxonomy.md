# 端侧自主系统工作负载分类

- 状态：v0.1
- 日期：2026-09-30
- 目的：把不同 UAV / UGV / AMR / USV / Robot / Fixed Edge 应用映射到统一的“可计算负载族”
- 方法：依据公开工程架构与综述提炼；资源判断与已确认事实分离

## 1. 为什么按工作负载族分析

自主系统的功能栈具有较强共性，但不同平台的具体算法、数据量和实时性差异很大。

例如：

- UAV 的 VIO 与 AMR 的 2D LiDAR localization 都属于定位，但数据类型和计算结构不同；
- 固定多摄像头系统可能没有定位/规划，却有非常重的视频与推理负载；
- VLA 操作机器人可能没有长距离导航，却需要大模型、多模态编码和动作生成。

因此不能用“自主等级”直接等价为算力等级。

本项目采用以下工作负载族，对具体场景再实例化参数。

---

## W1：Sensor I/O / Video Pipeline

### 典型输入
- RGB / IR Camera
- LiDAR / Radar
- IMU / GNSS
- AIS / Audio
- Joint / Force / Encoder

### 典型处理
- Camera capture
- ISP
- Demosaic / HDR / denoise
- Resize / crop / color conversion
- Video encode/decode
- Timestamp / synchronization
- DMA / zero-copy
- Sensor packet parsing

### 主要资源（工程推断）
- ISP / VPU
- DDR bandwidth
- Camera/SerDes/MIPI/Ethernet
- DMA / memory fabric
- CPU 驱动和数据编排

### 核心指标
- Pixel/s
- GB/s
- sensor timestamp jitter
- dropped frames
- encode/decode channels
- host copy count

---

## W2：State Estimation / Localization

### 典型算法
- EKF / UKF
- GNSS/INS
- Optical Flow
- VO / VIO
- LiDAR-Inertial Odometry
- NDT / map matching

### 事实依据
PX4 将 Optical Flow、VIO 用于无人机速度/位姿估计；Autoware 把 localization 作为独立核心 stack；GNSS-denied UAV 综述将 VIO、SLAM、LiDAR/vision/inertial fusion 作为关键路线。

### 主要资源（工程推断）
- CPU 标量/向量计算
- GPU 可选
- 低延迟内存
- 高精度时钟同步
- 实时调度

### 核心指标
- estimator rate
- end-to-end latency
- trajectory drift
- ATE/RPE
- CPU/GPU utilization
- failure recovery

---

## W3：DNN Perception

### 典型算法
- Detection
- Classification
- Tracking
- Semantic / Instance Segmentation
- Depth
- Pose
- Free-space
- Multi-sensor fusion

### 事实依据
Autoware perception 覆盖 object recognition、obstacle segmentation、traffic-light recognition、occupancy 等；Waymo 当前系统使用 camera/lidar/radar + AI/ML 做实时 perception；Skydio X10 依靠视觉感知进行自主避障/导航。

### 主要资源（工程推断）
- NPU/GPU
- DDR bandwidth
- ISP/预处理
- CPU 后处理
- 模型 runtime / compiler

### 核心指标
- model latency
- FPS
- AP / IoU / tracking metrics
- concurrent streams
- utilization
- power

---

## W4：3D Mapping / World Representation

### 典型算法
- SLAM
- Occupancy Grid
- Point Cloud Map
- 3D reconstruction
- BEV / Occupancy
- Semantic Map

### 事实依据
Nav2 使用 environmental representation / costmaps；Autoware 使用地图、occupancy、3D感知；UAV GNSS-denied 综述反复讨论 SLAM 和语义建图。

### 主要资源（工程推断）
- CPU/GPU
- 内存容量
- DDR bandwidth
- point-cloud acceleration
- storage

### 核心指标
- map update rate
- memory growth
- map accuracy
- latency
- bandwidth

---

## W5：Prediction / Tracking / Situation Understanding

### 典型算法
- Multi-object tracking
- trajectory prediction
- intent prediction
- scene understanding
- semantic reasoning

### 事实依据
Waymo 将系统问题概括为 “Where am I? What’s around me? What will happen next? What should I do?”；Autoware 当前公开能力包含 data-driven trajectory prediction。

### 主要资源（工程推断）
- CPU/GPU/NPU
- temporal model memory
- transformer acceleration（高级方案）
- shared world state

### 核心指标
- prediction horizon
- latency
- trajectory error
- model concurrency

---

## W6：Planning / Optimization / Decision

### 典型算法
- A*
- Dijkstra
- RRT / RRT*
- optimization-based planning
- MPC
- behavior planning
- trajectory generation
- learned policy / RL

### 事实依据
Nav2 以 planner/controller/behavior server 组织导航；USV 文献将 path planning / collision avoidance / guidance / control 列为核心；Autoware 2.0 允许 rule-based、optimization、E2E、learned generator 并存。

### 主要资源（工程推断）
- CPU
- GPU（部分优化/采样/学习规划）
- NPU（learned planning）
- 实时调度

### 核心指标
- replanning frequency
- worst-case latency
- success rate
- collision rate
- constraint violation

---

## W7：Foundation Model / VLM / LLM / VLA

### 典型任务
- scene description
- open-vocabulary reasoning
- natural-language instruction
- task decomposition
- long-horizon planning
- vision-language-action policy
- embodied reasoning

### 事实依据
OpenVLA 是 7B VLA；2025 VLA systematic review 汇总超过 100 个 VLA；高效 VLA 综述明确指出大模型的计算/内存需求与机器人端实时约束存在冲突。

### 主要资源（工程推断）
- 大内存容量
- 高内存带宽
- GPU/NPU tensor compute
- INT4/INT8/FP8/FP16
- KV cache
- multimodal encoder

### 核心指标
- model fit
- TTFT
- tokens/s
- action frequency
- memory footprint
- task success
- real-time coexistence

---

## W8：Multi-Agent / Fleet / Distributed Computing

### 典型任务
- task allocation
- fleet scheduling
- cooperative perception
- collaborative localization / mapping
- multi-agent planning
- swarm coordination

### 事实依据
2025 multi-robot navigation survey以 perception、planning、collaboration 为主轴；2026 MRTA review 系统梳理 task allocation / path planning；MiR Fleet 是当前工业 AMR 的真实 fleet-level orchestration 产品。

### 主要资源（工程推断）
- Ethernet/Wi-Fi/5G
- distributed state
- CPU/GPU optimization
- database/message bus
- network QoS

### 核心指标
- fleet size
- task throughput
- communication latency
- bandwidth
- conflict/deadlock rate
- scalability

---

## W9：Safety-Critical Control / Supervision

### 典型任务
- flight control
- motion control
- actuator loop
- safety supervisor
- health monitoring
- fault detection
- redundancy
- emergency stop

### 事实依据
Autoware 独立 control / vehicle interface；PX4 负责飞行控制闭环；MiR250 公开列出 safety functions 和 safety laser scanners。

### 主要资源（工程推断）
- MCU / real-time CPU
- RTOS/Linux RT
- watchdog
- redundant I/O
- deterministic communication

### 核心指标
- control period
- worst-case execution time
- jitter
- failover time
- safety integrity evidence

---

## 2. 负载族之间的并发关系

真实系统通常是并发组合而不是单一负载：

```text
W1 Sensor I/O
 ├─→ W2 Localization ─→ W4 Map ─┐
 ├─→ W3 Perception ─→ W5 Pred ─┼─→ W6 Planning ─→ W9 Control
 └─→ W7 VLM/VLA (optional) ─────┘
                         ↑
                  W8 Multi-Agent
```

因此平台选型必须评估：
- 并发
- 数据搬运
- 内存竞争
- 任务优先级
- 热稳态
- 故障隔离

而不是将各模块的峰值算力简单相加。

## 3. 参考资料

- PX4 Computer Vision: https://docs.px4.io/main/en/advanced/computer_vision
- Nav2: https://docs.nav2.org/
- Autoware Architecture: https://docs.autoware.org/main/design/autoware-architecture-v1/
- Waymo Driver: https://waymo.com/waymo-driver/
- Jarraya et al., GNSS-denied UAV navigation review, 2025: https://link.springer.com/article/10.1186/s43020-025-00162-z
- Chen et al., Multi-robot navigation survey, 2025: https://www.sciencedirect.com/science/article/pii/S2667379724000615
- Tahir & Parasuraman, Edge Computing and Its Application in Robotics, 2025: https://www.mdpi.com/2224-2708/14/4/65
- OpenVLA: https://arxiv.org/abs/2406.09246
