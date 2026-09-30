# C1–C5 典型工作负载组合的定义依据与中文解释

- 日期：2026-09-30
- 状态：v1
- 目的：解释 C1–C5 从哪些真实系统/文献抽象而来、为什么这样组合。
- 结论：C1–C5 是 **典型 workload composition（工作负载组合原型）**，不是自主等级，也不是性能等级。

## 1. 为什么还需要 C1–C5

W1–W9 描述“单类 workload”，但现实产品从不会只运行一个 workload。

平台选型真正关心的是组合：
- 多 Camera + Detection；
- Camera + VIO + Map + Planner；
- Camera/LiDAR/Radar + Prediction + Planning；
- Autonomy + VLM；
- Single Robot + Fleet Collaboration。

因此需要少量“典型组合”作为资源预算模板。

## 2. 五类组合的定义逻辑

C1–C5 的设计目标不是覆盖世界上所有系统，而是覆盖五种**会显著改变资源结构的典型增量**：

1. **从纯视频/AI分析开始**：没有本体定位与控制 → C1；
2. **加入自身定位、地图、规划、实时控制**：形成单机视觉自主 → C2；
3. **加入 LiDAR/Radar 等异构传感器和 Prediction**：形成多传感器自主 → C3；
4. **在基础自主系统上叠加 Foundation Model**：形成大模型增强 → C4；
5. **在单机自主上叠加网络化协同/Fleet**：形成协同自主 → C5。

这五类不是从 C1 到 C5 的“升级等级”。C4、C5 更准确地说是可叠加 modifier。

## 3. C1：多摄像头智能分析（Multi-Camera Analytics）

### 定义

```text
C1 = W1 + W3 + W5
(+ W7 optional)
```

### 现实依据

- 固定边缘视频分析/工业视觉/交通分析系统：大量 Camera、Detection、Tracking，但通常没有自身 Localization、Planning、Control；
- NVIDIA Metropolis 等 fixed-edge video analytics 公开覆盖 multi-camera tracking、video analytics、inspection 等；
- 因此该类系统资源重点是 Camera/codec/DDR/NPU/network/storage。

### 为什么单独定义

它是“高 AI/视频负载但低自主闭环”的典型反例，可用于证明“AI 算力大 ≠ 自主程度高”。

## 4. C2：视觉自主系统（Visual Autonomy）

### 中文名称

**视觉自主系统 / 视觉自主闭环**

### 定义

```text
C2 = W1 + W2 + W3 + W4 + W6 + W9
```

### 现实依据

- PX4：Camera/IMU → VIO → PX4；
- PX4 Collision Prevention：环境感知进入运动限制/避障；
- Nav2：State Estimation + Environmental Representation + Planning + Control；
- Isaac ROS/Nova：Physical Multi-Camera + VSLAM + Depth + Mapping；
- GNSS-denied UAV 综述：VIO/SLAM/Sensor Fusion 是 UAV 自主导航主线。

### 为什么这样定义

C2 的关键不是“有视觉”，而是视觉真正进入本体闭环：
1. W1 获取视觉；
2. W2 估计自身状态；
3. W3 感知环境；
4. W4 建立局部/全局世界表示；
5. W6 规划；
6. W9 与实时控制/安全监督协同。

这正对应六摄 UAV 的基础目标形态。

## 5. C3：多传感器自主系统（Multi-Sensor Autonomy）

### 定义

```text
C3 = W1 + W2 + W3 + W4 + W5 + W6 + W9
```

### 现实依据

- Autoware：Sensing / Localization / Perception / Planning / Control；
- Waymo：Camera + LiDAR + Radar；Where am I / What’s around me / What will happen next / What should I do；
- USV：Radar/AIS/Camera/GNSS 等多源融合 + tracking + collision avoidance。

### 为什么相对 C2 增加 W5

在复杂动态环境中，仅知道“障碍在哪里”不够，还需要预测目标未来轨迹和交互意图。因此 C3 把 Prediction/Tracking/Situation Understanding 提升为基础组成部分。

C3 的资源变化是：
- 传感器类型更多；
- 时间同步更复杂；
- data association/fusion 更重；
- memory/DDR 更大；
- Prediction workload 更突出。

## 6. C4：基础模型增强机器人/无人系统（Foundation-Model Augmented Robotics）

### 定义

```text
C4 = C1/C2/C3 base + W7
```

### 现实依据

- PaLM-E：视觉、状态、文本融入 embodied multimodal model；
- RT-2：Vision-Language → robot action token；
- OpenVLA：7B VLA；
- VLA efficiency survey：明确指出 onboard compute、memory、latency 约束。

### 为什么不把 C4 定义成“更高自主等级”

VLM/VLA 可以增强语义理解、任务分解和高层策略，但不能自动替代：
- VIO；
- hard real-time control；
- failsafe；
- deterministic safety loop。

所以 C4 是“资源叠加维度”，不是 C2/C3 的高等级版本。

## 7. C5：协同自主系统（Cooperative Autonomy）

### 定义

```text
C5 = C2/C3 base + W8
```

### 现实依据

- Multi-Robot Navigation Survey：Perception / Planning / Collaboration；
- MiR Fleet：任务和交通管理；
- 多无人系统：shared perception、distributed map、task allocation、swarm coordination。

### 为什么单独定义

从单机到多机，新增的核心资源不只是“多一台机器”，而是：
- network bandwidth/QoS；
- distributed state；
- task allocation；
- cooperative perception；
- fleet identity / trust。

这会改变系统架构，因此值得独立成 composition archetype。

## 8. C1–C5 的关系

```text
C1：视频/AI分析
C2：视觉自主闭环
C3：多传感器动态自主
C4：在 C1/C2/C3 上增加 W7
C5：在 C2/C3 上增加 W8
```

因此：
- C1→C2→C3 可以理解为“资源结构复杂度增加”的常见路径，但不是等级；
- C4、C5 是正交叠加；
- 实际项目可以同时属于 C3 + C4 + C5；
- 六摄 UAV 当前基础 = C2，未来 VLM = C2+C4，多机协同 = C2+C5。

## 9. 为什么只定义五类

五类是“代表性预算模板”，不是行业穷举。
选择标准是：加入该组合后会显著改变 CPU/GPU/NPU/Memory/I/O/Network/Real-Time 的资源结构。

如果未来项目出现稳定的新 archetype（例如事件相机高速闭环、纯语言 Agent 系统），可新增组合，但不为了形成“完整分级”机械扩张。
