# PX4 Collision Prevention：时延、更新率与速度约束证据

- 获取日期：2026-09-30
- 状态：verified-public-evidence
- 主要来源：PX4 Guide main / stable-era historical docs
- 用途：为六摄像头无人平台的避障端到端时延模型提供事实锚点

## 1. 当前 PX4 Collision Prevention 的关键事实

当前 PX4 Guide：
https://docs.px4.io/main/en/computer_vision/collision_prevention

已确认：

1. `CP_DIST` 是车辆与障碍物之间允许的最小距离；文档明确提醒该距离相对传感器位置定义，需要为机体/桨叶留安全裕量。
2. `CP_DELAY` 用于配置 **sensor delay + vehicle velocity setpoint tracking delay**。
3. 外部视觉系统的 sensor delay **可能高达约 0.2 s**。
4. vehicle velocity setpoint tracking delay 需要从飞行日志测量；PX4 文档给出的典型量级约 **0.1–0.5 s**，取决于机体尺寸和调参。
5. Collision Prevention 的速度限制同时考虑：
   - sensor range；
   - delay；
   - `MPC_JERK_MAX`；
   - `MPC_ACC_HOR`；
   - jerk-optimal velocity controller。
6. 如果超过 0.5 s 没有收到任何 range data，PX4 会禁止 xy 方向运动；持续 5 s 后进入 HOLD。
7. Companion/external sensor 的消息最低更新率与速度有关。文档记录的初始测试为：
   - vehicle speed = **4 m/s**
   - `OBSTACLE_DISTANCE` = **10 Hz**
   - 10 Hz 当时是所用 vision system 的最大输出速率。

### 重要边界

当前文档同时警告：
> companion implementation/setup 当前属于 untested；原 companion project 已不维护并归档。

因此“4 m/s + 10 Hz”只能作为历史/工程量级锚点，不能表述为当前 PX4 官方推荐性能门槛。

## 2. 由同一页事实可做的纯算术

4 m/s、10 Hz：

- update period = 100 ms
- 一次完整更新周期内的位移 = **0.4 m**

如果外部 vision sensor delay 取 PX4 文档给出的“可高达 0.2 s”：
- 仅 sensor delay 对应位移 = **0.8 m**

tracking delay 0.1–0.5 s：
- 对应位移 = **0.4–2.0 m**

若仅做“sensor + tracking delay”的算术相加：
- 0.3–0.7 s
- 4 m/s 时对应 **1.2–2.8 m**

如果再额外考虑“障碍刚好出现在两次 10 Hz 更新之间”的最坏一周期等待：
- 简化筛查位移 = **1.6–3.2 m**

### 这不是停止距离

上面的 1.6–3.2 m 只是：
> sampling wait + sensor delay + tracking delay 期间的直线位移算术。

它 **没有包含**：
- 真正的 jerk-limited braking distance；
- CP_DIST/机体安全裕量；
- perception false negative；
- obstacle motion；
- vehicle attitude/turning maneuver；
- queueing/jitter。

因此只能用来说明“总时延的距离代价”，不能作为安全设计结论。

## 3. 历史 PX4 Path Planning Interface：只能做参考锚点

PX4 v1.14 Obstacle Avoidance 文档：
https://docs.px4.io/v1.14/en/computer_vision/obstacle_avoidance

历史记录：
- local planner setpoint stream 约 **30 Hz**，mission speed 约 **3 m/s**；
- global planner 约 **10 Hz**，mission speed 约 **1–1.5 m/s**；
- 如果超过 0.5 s 不再收到 setpoint，PX4 切换 HOLD。

纯算术：
- 3 m/s @30 Hz：每个 setpoint period 前进约 **0.10 m**
- 1 m/s @10 Hz：约 **0.10 m**
- 1.5 m/s @10 Hz：约 **0.15 m**

但是当前 PX4 Path Planning Interface 页面明确说明：
https://docs.px4.io/main/en/computer_vision/path_planning_interface

> 该接口自 PX4 v1.15 起移除/不再支持，旧代码由于架构限制被放弃。

因此这些频率只能标记为 **HISTORICAL_REF**，不能直接作为新系统设计要求。

## 4. 对本项目的直接意义

PX4 的当前逻辑本身已经证明：

> 避障能力不是“模型 FPS 越高越安全”，而是 sensor range、Frame Age、sensor delay、vehicle tracking delay、acceleration/jerk capability 和 keep-out distance 的组合约束。

所以六摄像头项目必须测/冻结：
- sensor exposure/start-of-frame time；
- frame ready time；
- perception result time；
- map/fusion ready time；
- planner output time；
- flight-controller command receive time；
- actual vehicle response time；
- P50/P95/P99/maximum Frame Age。

不能用单个 YOLO latency 代替闭环时延。
