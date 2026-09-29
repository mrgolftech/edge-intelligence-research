# USV / 无人船端侧智能应用与计算需求

- 状态：v0.1
- 日期：2026-09-30

## 1. 当前真实应用

2025 Control Engineering Practice 的 USV 综述指出，USV 已从研究概念走向科学、工程、商业和防务实际应用，核心方法围绕：

- navigation
- guidance
- control
- learning/data-driven systems

当前商业系统进一步证明典型任务：

### Saildrone Voyager
- persistent coastal surveillance
- nearshore mapping
- maritime domain awareness
- 长航时无人执行
- radar / AIS / IR camera / environmental sensors 等多种 payload

### Sea Machines
当前商业系统包括：
- transit autonomy
- remote command & control
- collision & obstacle avoidance
- collaborative autonomy
- AI-powered vessel vision

其 collision avoidance 方案融合：
- radar
- GPS
- AIS
- electronic charts
- computer vision

并进行目标跟踪、自动改航/调速，以及考虑适用 COLREG 响应。

## 2. USV 的负载特征

与 UAV / UGV 相比，USV 有明显不同：

### 长航时
Saildrone Voyager 官方列出 100 days between service stops。

因此：
- 持续功耗
- 热稳态
- 可靠性
- 存储
- 通信
比短时 benchmark 更重要。

### 远距离、多源感知
典型：
- radar
- AIS
- camera/IR
- GNSS/IMU
- chart
- weather/ocean sensors

### 海上避碰
算法不仅是几何 obstacle avoidance，还要处理：
- moving vessel tracking
- sequential decision
- COLREG / navigation rules
- uncertainty / sea conditions

2025 DRL collision avoidance review 表明学习型方法正在成为研究方向，但同时强调 reward、robustness、safety/regulations、sim-to-real 等问题。

## 3. 端侧与远程

优先本地：
- navigation
- state estimation
- target tracking
- collision avoidance
- control
- lost-link fallback

可放远端：
- mission supervision
- intelligence fusion
- fleet coordination
- map/survey post-processing
- historical analytics

## 4. 工程结论

USV 对平台的要求不能照搬无人机：
- 可容纳更高功耗算力，但要求长时间可靠运行；
- radar/AIS fusion 和通信比纯视觉平台更重要；
- 网络常不稳定，因此 safety/nav 必须具备本地闭环；
- 对边缘/卫星通信的带宽管理是系统设计的一部分。

## 5. References

1. An overview of Unmanned Surface Vehicles: Methods, practices, and applications, Control Engineering Practice, 2025.  
   https://www.sciencedirect.com/science/article/pii/S0967066125002412
2. Deep reinforcement learning for collision avoidance in unmanned surface vehicles: State-of-the-art, Applied Ocean Research, 2025.  
   https://www.sciencedirect.com/science/article/pii/S0141118725003645
3. Saildrone Voyager. https://www.saildrone.com/platform/voyager
4. Sea Machines Collision & Obstacle Avoidance.  
   https://sea-machines.com/why-sea-machines/solutions/collision-obstacle-avoidance/
5. Sea Machines Transit Autonomy.  
   https://sea-machines.com/why-sea-machines/solutions/transit-autonomy/
