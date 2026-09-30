# Workload Composition Library：典型端侧智能任务组合

- 状态：v0.1
- 日期：2026-09-30
- 阶段：Phase 2 — Requirement & Architecture Synthesis
- 目的：把跨领域应用映射成可复用的 workload composition，而不是自创 L1–L5 等级
- 证据基础：
  - `research/scenarios/application-workload-matrix.md`
  - `research/workloads/workload-taxonomy.md`
  - `research/workloads/quantitative-workload-baselines.md`
  - 已有 UAV/UGV/USV/AMR/Robot/Fixed Edge 事实资料

## 1. Composition 不是能力等级

本文件中的 C1–C5 只是**工作负载组合 ID**，不是：
- 自主等级；
- 能力高低等级；
- TOPS 档位；
- 产品成熟度。

同一系统可同时拥有多个 composition，或在不同工况之间切换。

---

## C1 — Multi-Camera Analytics

### 现实对应

典型：
- 固定式多摄像头视频分析；
- 工业视觉；
- 多路监控检测/跟踪；
- 无定位/运动控制要求的边缘感知节点。

事实基础：
- 固定 Edge 场景反复出现 ingest/decode、detection、tracking、cross-camera analytics；
- 不需要机器人 localization/planning/control 是它与自主移动系统最大的结构差异。

### Workload

```text
W1 Sensor / Video
+ W3 DNN Perception
+ W5 Tracking / Situation
(+ W7 on-demand VLM query)
```

### 主导资源

优先级不是“高低分”，而是容易成为瓶颈的资源：

1. ISP/VPU / video decode；
2. DDR image-plane traffic；
3. NPU/GPU inference throughput；
4. CPU pre/post/tracking；
5. network/storage；
6. optional VLM memory。

### 实时性

核心是：
- per-stream effective FPS；
- Frame Age；
- dropped frames；
- cross-camera tracking latency。

通常不包含车辆响应，因此闭环 deadline 比自主移动系统简单。

### 架构倾向

可考虑：
- Integrated SoC；
- Host + Accelerator；
- Edge server。

独立 AI accelerator 在这个 composition 中更容易发挥作用，因为 Host 不必额外承担 W2/W6。

### 主要 Gate

- Gate A Sensor/I/O
- Gate C Memory/DDR
- Gate D Compute
- Gate E Concurrency
- Gate F Thermal
- Gate G Software

Gate B Real-Time Control 通常不适用。

---

## C2 — Visual Autonomy

### 现实对应

典型：
- GNSS拒止 UAV；
- 视觉导航 AMR；
- 视觉自主机器人；
- 多摄像头避障/自主导航。

事实基础：
- UAV GNSS拒止资料反复出现 VIO/SLAM、感知、地图和规划；
- Nova/Isaac Perceptor 给出物理多相机 VSLAM + depth + mapping 的真实系统路径；
- PX4 当前 Collision Prevention 将 sensor/delay/vehicle dynamics 联合用于速度约束。

### Workload

```text
W1
+ W2 Localization / VIO / SLAM
+ W3 Perception / Depth
+ W4 Local Mapping
+ W6 Planning
+ W9 Safety / Control supervision
```

W5 可按任务加入。

### 主导资源

这个 composition 与 C1 的关键区别是：
- CPU latency-sensitive workload 显著增加；
- GPU 可能参与 VIO/depth/map；
- Camera/IMU synchronization 成为算法输入要求；
- DDR 同时承载 image、SLAM/map、DNN；
- planning/W9 引入 deadline，而不仅是 FPS。

主要关注：
1. Camera/IMU timing；
2. CPU tail latency；
3. GPU/NPU concurrency；
4. DDR contention；
5. map memory；
6. closed-loop Frame Age；
7. real-time partition。

### 实时性

必须使用闭环：

```text
Sensor
→ VIO / perception / map
→ planner
→ FCU / motion controller
→ vehicle response
```

因此不能只用 W3 FPS。

### 架构倾向

优先比较：
- Integrated heterogeneous SoC/SoM + external FCU/MCU；
- Host + Accelerator + external FCU/MCU。

Host+Accelerator 只有当 Host 已能稳定承担 W1/W2/W4/W6 时才有意义。

### 主要 Gate

A/B/C/D/E/F/G 全部适用。

---

## C3 — Multi-Sensor Autonomy

### 现实对应

典型：
- Robotaxi / 高阶 UGV；
- 多传感器自主车；
- 雷达+视觉 USV 避碰；
- LiDAR/Camera/IMU 融合机器人。

事实基础：
- Autoware / Waymo 类系统具有 localization、perception、prediction、planning、control 完整链；
- USV 公开系统采用 Radar/AIS/Camera/GNSS 等融合；
- nuScenes/Waymo 提供多 Camera + LiDAR/Radar 的现实数据结构。

### Workload

```text
W1
+ W2
+ W3
+ W4
+ W5 Prediction / Tracking
+ W6
+ W9
```

### 相对 C2 的新增压力

- heterogeneous sensor ingest；
- larger timestamp/calibration graph；
- point cloud/radar processing；
- W5 temporal history / prediction；
- larger map/world representation；
- redundancy / safety architecture。

### 主导资源

常见资源问题：
- Camera + LiDAR/Radar I/O；
- CPU/GPU/NPU heterogeneity；
- memory capacity；
- DDR bandwidth；
- safety isolation；
- deterministic scheduling。

### 架构倾向

更倾向于高集成异构 SoC/车规平台或多计算单元架构。

但这不是“集成 SoC 一定最好”，而是因为 workload 不再是单一 DNN accelerator 可以覆盖。

---

## C4 — Foundation-Model Augmented Robotics

### 现实对应

典型：
- VLM 场景理解机器人；
- VLA 操作机器人；
- 自然语言任务规划；
- edge generative AI 增强的自主系统。

事实基础：
- OpenVLA 7B / LIBERO 已作为本仓库 W7 公共基线；
- VLA/edge robotics 综述都把模型规模、内存、实时性视为主要端侧约束；
- Hailo-10H、IQ-9075、M50 等公开路线已经明确把 LLM/VLM 作为端侧能力方向。

### Workload

```text
Base autonomy composition
+ W7 Foundation Model
```

Base autonomy 可以是 C1/C2/C3。

### 增量资源

与传统 autonomy 相比，新增重点通常不是单纯 INT8 TOPS：

1. memory capacity；
2. memory bandwidth；
3. model load/residency；
4. KV cache/context；
5. visual encoder；
6. TTFT；
7. action/token generation；
8. W7 与 W2/W3/W6 的资源隔离。

### 安全边界

W7 不应默认进入：
- hard real-time flight control；
- safety-critical collision avoidance；
- low-level actuator loop。

更合理的第一版角色：
- semantic understanding；
- task decomposition；
- human interaction；
- non-hard-real-time decision support。

具体系统可不同，但必须有证据才能扩大 W7 权限。

### 架构倾向

可能需要：
- high-memory integrated SoM；
- Host + high-memory accelerator；
- edge-cloud split。

平台的“模型能装下”只是第一门槛，必须继续看实时自主栈是否被干扰。

---

## C5 — Cooperative Autonomy

### 现实对应

典型：
- UAV swarm；
- AMR fleet；
- cooperative perception；
- distributed task allocation；
- edge-assisted multi-robot。

事实基础：
- multi-robot/MRTA 研究与现实 Fleet 产品说明 W8 是独立 workload；
- Flight RB5 公开路线包含 drone-to-drone/swarm connectivity；
- AMR fleet 系统把单机导航与全局调度分开。

### Workload

```text
Single-platform autonomy composition
+ W8 Multi-Agent / Fleet
```

### 增量资源

新增重点：
- network bandwidth / jitter；
- peer/fleet state；
- task allocation；
- global optimization；
- shared map/perception；
- central edge compute。

### 安全原则

单机的：
- W2 local state estimation；
- W3 safety perception；
- W6 local collision avoidance；
- W9 control

不应依赖持续网络连接。

W8 故障时应降级为单机安全模式，而不是失去本地闭环。

### 架构倾向

自然形成：
```text
Onboard autonomy
+ network
+ edge/fleet compute
```

因此评估对象从单板扩展为系统级资源。

---

## 2. 五类 Composition 的资源侧差异

| Composition | 主要新增 workload | 最可能的重要资源 | 典型硬约束 |
|---|---|---|---|
| C1 Multi-Camera Analytics | W1 W3 W5 | ISP/VPU, NPU/GPU, DDR | streams/FPS/drop |
| C2 Visual Autonomy | +W2 W4 W6 W9 | CPU, GPU, DDR, sync, NPU | Frame Age / closed loop |
| C3 Multi-Sensor Autonomy | +heterogeneous W1 +W5 | I/O, memory, GPU/NPU/CPU, safety | fusion + redundancy |
| C4 FM-Augmented Robotics | +W7 | memory capacity/BW, GPU/NPU | TTFT/action latency + isolation |
| C5 Cooperative Autonomy | +W8 | network, CPU/server, state DB | network loss/jitter + local fallback |

这张表只说明**资源结构变化**，不是算力等级。

---

## 3. Composition → Architecture 的原则

### C1
AI Accelerator 可能是非常自然的路线，因为 Host 主要承担视频和应用逻辑。

### C2
首先确认 W2/W4/W6 Host 能力，再看是否需要独立 W3 accelerator。

### C3
优先关注异构 I/O / memory / safety，不应把单 NPU TOPS 当主导指标。

### C4
先解决 memory residency 与 resource isolation，再谈 token/s。

### C5
把 onboard compute 和 fleet/edge compute 分成两个预算，不要用服务器能力替代本地安全闭环。

---

## 4. 后续定量化方式

每个 composition 后续建立三种 profile：

### Reference
来自公开系统/数据集的事实锚点。

### Project Nominal
由具体项目 Requirement Card 冻结。

### Stress
用于 Benchmark 的工程压力档位，不冒充项目需求。

这样保持：
> **公开事实 ≠ 项目要求 ≠ 压力测试档位**
