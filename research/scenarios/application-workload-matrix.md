# 无人装备端侧智能应用—工作负载需求矩阵

- 状态：v0.1
- 日期：2026-09-30
- 目的：建立“应用事实 → 功能栈 → 工作负载 → 端侧资源”的中间桥梁
- 证据原则：应用模式/功能链来自论文、标准或当前官方产品；资源侧为工程推断，后续需要 Benchmark 定量验证

## 1. 使用方法

本矩阵不输出“某场景需要 XX TOPS”。

每个场景先描述：

1. 现实任务与部署方式；
2. 典型传感器；
3. 人类参与方式；
4. 必需功能栈；
5. 对应 W1–W9 工作负载族；
6. 哪些功能必须在端侧；
7. 哪些功能可能卸载到近端边缘/云；
8. 推导出的主要系统资源。

工作负载定义见：
[`research/workloads/workload-taxonomy.md`](../workloads/workload-taxonomy.md)

---

## 2. 第一版跨域矩阵

| 平台/场景 | 现实应用与事实依据 | 传感器/输入 | 人机关系与环境 | 核心功能 | 工作负载族 | 必须优先端侧执行 | 可考虑边缘/云 | 主要资源关注（工程推断） |
|---|---|---|---|---|---|---|---|---|
| UAV：巡检/测绘/监视 | UAV综述与当前行业应用覆盖工业巡检、测绘、环境监测、应急等；Skydio X10提供自主避障/夜间导航 | RGB/变焦/IR、GNSS、IMU；测绘可能增加高分辨率相机/LiDAR | 多为人给任务/航线，系统执行；户外、光照变化、风扰 | acquisition、定位、感知、任务执行、避障、编码/回传 | W1 W2 W3 W6 W9 | 飞控、状态估计、基础避障、关键感知 | 大规模后处理、三维重建、历史分析 | ISP/VPU、NPU/GPU、CPU、带宽、SWaP |
| UAV：GNSS拒止自主导航/搜救 | 2025/2026 GNSS-denied综述明确覆盖 VIO、SLAM、LiDAR/vision/inertial fusion、SWaP、动态环境、故障恢复 | Camera/IR、IMU、LiDAR/UWB/terrain data（按方案） | 人给任务或监督；GNSS-denied、复杂动态环境 | VIO/SLAM、感知、地图、规划、避障、故障恢复 | W1 W2 W3 W4 W6 W9 | 定位、地图局部更新、障碍感知、规划、控制 | 全局地图更新、非实时语义分析 | CPU/GPU/NPU协同、DDR、同步、低延迟、SWaP |
| UAV：多机协同 | 多机器人综述、MRTA研究和 Flight RB5 的 drone-to-drone/swarm 支持说明协同是现实路线 | 单机传感器 + peer state/mission data | 多机、通信不稳定、人监督或目标级指挥 | 单机导航 + task allocation + cooperative perception/planning | W1-W6 W8 W9 | 单机安全闭环、局部避障、关键协同状态 | 全局任务重规划、历史/全局融合 | 网络QoS、CPU优化、分布式状态、边缘节点 |
| UGV：城市自动驾驶/Robotaxi | Waymo当前fully autonomous Driver与Autoware production stack证明多传感器、定位、感知、预测、规划、控制的完整链路 | Camera、LiDAR、Radar、GNSS/IMU、map | 高动态城市道路；高人类独立性，严格安全约束 | localization、perception、fusion、prediction、planning、control | W1-W6 W9；高级方案含W7 | 全部安全关键实时驾驶链 | 训练、地图生产、离线分析、fleet intelligence | 高CPU/GPU/NPU、超高传感器带宽、内存、冗余、功能安全 |
| UGV/园区车：限定区域物流 | Autoware覆盖 cargo delivery、shuttle；环境相对受限但仍需动态避障 | Camera/LiDAR/Radar、GNSS/IMU | 园区/封闭道路；可远程监督 | localization、perception、planning、control、remote ops | W1-W6 W8 W9 | 定位/避障/控制 | fleet、调度、地图/日志 | 中高计算、网络、长期稳定性 |
| AMR：单机仓储搬运 | 2026 Annual Review与MiR250现有产品证明 SLAM、path planning、动态障碍感知和安全协作是成熟应用 | Safety LiDAR、3D camera、proximity、encoder | 结构化室内但人员/叉车动态；人不持续遥控 | localization/map、obstacle、local/global planning、control | W1 W2 W3 W4 W6 W9 | 定位、避障、运动控制 | 任务下发、数据分析 | CPU为主 + 视觉/NPU可选、可靠传感器、低延迟 |
| AMR：多机物流/Fleet | Annual Review突出 multirobot coordination/task allocation/fleet management；MiR Fleet是现实产品 | 单机状态 + map + mission + network | 多机器人共享空间，中央或分布式调度 | fleet scheduling、traffic control、MRTA、local nav | W1-W6 W8 W9 | 每台机器人的local nav/safety | fleet optimizer、历史分析 | 网络、服务器/边缘计算、数据库、优化算法 |
| USV：长航时监视/测绘 | Saildrone Voyager用于 coastal surveillance、mapping，100天级续航与多传感器负载展示长航时无人船现实需求 | Radar、AIS、PTZ IR camera、GNSS、环境/水文传感器、sonar按任务 | 开阔海域、长航时、通信受限；远程监督 | navigation、mission execution、sensor processing、communications | W1 W2 W3 W6 W8 W9 | navigation/control、碰撞安全、关键传感器处理 | 大规模测绘处理、情报融合、任务重规划 | 长期可靠性、低功耗、存储、网络/卫星链路 |
| USV：自主航行/避碰 | 2025 USV综述和 Sea Machines 实际产品明确 radar/GPS/AIS/chart/CV融合、COLREG相关避碰和自主航行 | Radar、AIS、Camera、GNSS/IMU、chart/weather | 动态海况、目标稀疏但作用距离大；可远程接管 | perception/fusion、tracking、path planning、COLAV、control | W1 W2 W3 W5 W6 W9 | 目标跟踪、避碰、航迹控制 | fleet/mission supervision、非实时分析 | CPU/GPU/NPU、雷达/AIS融合、鲁棒性、网络 |
| Robot：工业/服务移动操作 | 2026 warehouse robotics综述覆盖 perception/manipulation、SLAM、planning、人机协作 | Camera/depth/LiDAR、joint/force、语言指令 | 室内动态环境；人与机器人协作 | navigation + pose/perception + manipulation + task sequencing | W1-W6 W9；高级系统含W7 | 低层运动/碰撞安全、局部感知 | 任务知识、长时规划（按网络条件） | GPU/NPU + CPU、实时运动控制、传感器同步 |
| Robot：VLA/具身智能 | OpenVLA及2025 VLA综述证明 vision-language-action 正在将视觉、语言、动作统一；efficient VLA综述指出计算/内存与端侧实时约束冲突 | multi-camera/depth/proprioception + text | 开放任务、人给自然语言目标；操作环境复杂 | multimodal encoder、reasoning、action generation + safety/control | W1 W3 W5 W6 W7 W9 | 安全监控、低层控制；端侧模型取决于平台 | 大模型推理/记忆/规划可混合部署 | 大内存、高带宽、GPU/NPU、低精度推理、资源隔离 |
| Fixed Edge：多摄像头视频分析 | NVIDIA Metropolis当前覆盖 multi-camera tracking、工业视觉、交通、零售等；streaming video analytics文献也将cross-camera inference作为重要维度 | 多路 IP/CSI Camera、可选音频/传感器 | 固定节点，无自身定位/运动控制 | ingest/decode、detection、tracking、cross-camera analytics、VLM query | W1 W3 W5；高级含W7 | 视频接入、低延迟推理、隐私敏感分析 | 长时视频检索、集中式模型/知识 | VPU/ISP、NPU/GPU、DDR、网络、存储 |

---

## 3. 从矩阵得到的第一批工程结论

### 结论 A：不存在“无人装备统一 TOPS 档位”

**已确认事实**
现实场景的传感器、功能链和人机关系差异非常大。

**工程推断**
- 固定视频边缘设备可能有高 AI 推理吞吐，但没有 localization/planning/control；
- GNSS拒止 UAV 峰值 AI TOPS 未必最大，却对 CPU、同步、实时性和 SWaP 极敏感；
- Robotaxi 可能需要最复杂的多传感器并发和安全冗余；
- VLA robot 的内存容量/带宽可能比传统 INT8 TOPS 更关键。

因此不能用单轴算力等级覆盖所有应用。

### 结论 B：端侧“必须本地”的核心不是所有 AI，而是安全/实时闭环

跨平台共同倾向本地执行：
- 状态估计
- 障碍/安全相关感知
- 局部规划
- 控制
- 故障监测
- 断网降级能力

Edge Robotics 综述指出，纯云方案受到通信延迟和连接性的约束，edge computing 的核心价值是降低时延并就近处理时效性任务。

### 结论 C：工作负载正在从“CV推理”扩展为异构并发

成熟系统同时存在：
- traditional estimation
- optimization/planning
- DNN perception
- video pipeline
- safety control

未来又增加：
- E2E / learned planning
- VLM/VLA
- multi-agent

因此最值得调研的不是“AI加速卡峰值”，而是异构系统在并发条件下的真实表现。

### 结论 D：VLM/VLA 需要纳入趋势，但不应泛化到所有无人平台

VLA 是机器人领域明确增长的技术路线，但论文同时指出其计算量、内存和实时性是端侧部署主要矛盾。

因此后续将 VLM/VLA 作为独立 workload family，不作为 UAV/USV/AMR 的默认必选功能。

---

## 4. 下一步定量化顺序

本矩阵 v0.1 先建立“有哪些负载”。

下一步按以下顺序建立可量化 workload profile：

1. W1 多摄像头 / 视频处理
2. W2 VIO / SLAM / localization
3. W3 目标检测 / 分割 / 深度
4. W4 Point Cloud / BEV / Mapping
5. W6 Planning / Optimization
6. W7 VLM / VLA
7. W8 Multi-agent / Fleet

每个 profile 再记录：
- 输入参数
- benchmark algorithm/model
- precision
- target rate
- latency
- CPU/GPU/NPU
- memory
- bandwidth
- power
- reference platform

---

## 5. 主要证据索引

- [UAV GNSS拒止导航综述 2025](../../references/papers/uav-gnss-denied-navigation-2025.md)
- [仓储与物流机器人综述 2026](../../references/papers/amr-logistics-2026.md)
- [多机器人导航综述 2025](../../references/papers/multi-robot-navigation-2025.md)
- [USV方法与应用综述 2025](../../references/papers/usv-overview-2025.md)
- [Edge Robotics综述 2025](../../references/papers/edge-robotics-2025.md)
- [VLA端侧效率问题综述 2025](../../references/papers/vla-efficiency-2025.md)
- [当前真实系统/产品证据](../../references/webpages/deployed-autonomous-systems.md)
