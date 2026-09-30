# 六摄像头 UAV：避障闭环时延预算与空间裕量模型

- 状态：v0.1
- 日期：2026-09-30
- 目标：把“需要多少 FPS / 多低 latency”转换为由飞行速度、探测距离、控制响应和算法链共同约束的参数化问题
- 原则：公开系统参数只作为事实锚点；本项目目标值必须由实际任务与飞行器动力学冻结
- 数据：
  - `data/calculations/avoidance-timing-fact-anchors.csv`
  - `data/calculations/six-camera-observed-mode-sensitivity.csv`
- 工具：`scripts/calc_avoidance_latency_budget.py`

## 1. 为什么不能先规定“30 FPS”

无人机从障碍物进入可探测范围，到飞行器真正产生足够的速度/轨迹变化，中间不是一个 DNN inference：

```text
Obstacle becomes observable
→ wait for next sensor sample/exposure
→ sensor readout / CSI / ISP
→ buffer / format conversion
→ detection / depth / tracking
→ map / fusion
→ local planner
→ command transport
→ flight controller / vehicle response
→ actual trajectory changes
```

因此必须区分：

- **Update Rate**：新观测/新结果产生的频率；
- **Compute Latency**：某个算法模块的计算时间；
- **Frame Age**：从图像采样到对应结果被消费时的年龄；
- **Closed-loop Response**：从障碍物可观测到飞行器实际响应的总时间。

只有最后两项最接近避障实时性的系统指标。

## 2. 当前最有用的公开事实锚点

### 2.1 PX4 Collision Prevention：速度不是由 FPS 单独决定

PX4 当前文档：
https://docs.px4.io/main/en/computer_vision/collision_prevention

公开事实：

- `CP_DELAY` 表示 **sensor delay + vehicle velocity setpoint tracking delay**；
- 外部视觉系统 sensor delay 可能高达约 **0.2 s**；
- vehicle velocity setpoint tracking delay 需从日志测量，PX4 给出的典型量级约 **0.1–0.5 s**；
- 允许速度同时受 sensor range、`CP_DIST`、`CP_DELAY`、`MPC_JERK_MAX`、`MPC_ACC_HOR` 等约束；
- 超过 **0.5 s** 没有 range data 时，Collision Prevention 会把 xy 方向 movement setpoint 约束为 0；持续约 5 s 后进入 HOLD；
- Companion/external sensor 的最低消息频率取决于车辆速度；
- 文档保留的初始测试锚点为 **4 m/s + 10 Hz OBSTACLE_DISTANCE**。

但当前文档也明确把 companion implementation/setup 标为 **untested**，原 companion project 已停止维护。因此 4 m/s/10 Hz 只能作为历史工程锚点，不能变成本项目要求。

### 2.2 PX4 历史 Path Planning Interface：频率与任务速度配对存在先例

PX4 v1.14 历史文档：
https://docs.px4.io/v1.14/en/computer_vision/obstacle_avoidance

记录过：
- local planner：约 **30 Hz** setpoint stream，mission speed 约 **3 m/s**；
- global planner：约 **10 Hz**，mission speed 约 **1–1.5 m/s**；
- setpoint 超过约 0.5 s 未更新时进入 HOLD。

当前 PX4 Path Planning Interface 页面已明确说明：该旧接口从 **v1.15 起被移除**，旧代码因架构限制不再维护。

因此这组数据只标记为 **HISTORICAL_REF**，用途是说明“控制/规划更新率需要结合任务速度讨论”，不能作为新系统规范。

### 2.3 EGO-Planner：planner solver 可以很快，但不等于闭环很快

EGO-Planner 论文：
https://zhepeiwang.github.io/pubs/ral_2021_egoplan.pdf

论文 Table III：
- EWOK：ESDF 6.43 ms；planning 1.39 ms；
- Fast-Planner：ESDF 4.01 ms；planning 3.29 ms；
- EGO-Planner：不需要 ESDF update；planning **0.81 ms**。

同一论文的真实飞行实验：
- cluttered indoor environment 达到 **3.56 m/s**；
- outdoor forest 超过 **3 m/s**。

重要边界：
> 0.81 ms planning benchmark 与 3.56 m/s real flight 是同一论文中的不同实验，不能拼成“3.56 m/s 时系统总反应 0.81 ms”。

只做数量级算术：
- 3.56 m/s × 0.81 ms ≈ **2.9 mm**

它只能说明：millisecond 级 planner solver 往往不是整个视觉避障闭环中最大的时延项。

### 2.4 EGO-Planner 官方代码：调度频率也不等于感知频率

官方仓库：
https://github.com/ZJU-FAST-Lab/ego-planner

当前 master 默认/仿真路径：
- FSM timer：0.01 s → **100 Hz**
- collision safety check timer：0.05 s → **20 Hz**
- default simulation max_vel：2.0 m/s
- max_acc：3.0 m/s²
- max_jerk：4.0 m/s³
- planning_horizon：7.5 m
- depth_filter_maxdist：5.0 m
- max_ray_length：4.5 m
- emergency_time：1.0 s

这些是软件默认/仿真配置，不是行业门槛；100 Hz FSM 也不代表 Camera 或 DNN 以 100 Hz 输出。

### 2.5 FASTER：高动态场景确实存在

FASTER：
https://arxiv.org/abs/2001.04420

论文在 unknown cluttered environment 的真实飞行中报告最高约 **7.8 m/s**。

它用于本项目的意义不是规定“无人机要 7.8 m/s”，而是提供高动态 stress anchor：速度升高后，每毫秒 delay 对应的空间代价线性增加。

## 3. 参数化闭环模型

定义：

- `v`：当前飞行速度；
- `f_sensor`：障碍信息有效更新率；
- `T_sample`：最坏采样等待，简化取 `1/f_sensor`；
- `T_sensor`：exposure/readout/transport/ISP；
- `T_queue`：buffer/queue；
- `T_perception`：detection/depth/tracking；
- `T_fusion`：地图/多相机/状态融合；
- `T_planner`：局部规划；
- `T_command`：companion → FCU；
- `T_vehicle`：命令到实际飞行器响应；
- `D_keepout`：机体/桨叶/安全余量；
- `D_brake`：真实减速/转向所需距离。

则：

```text
T_pipeline =
T_sensor + T_queue + T_perception + T_fusion + T_planner + T_command

T_reaction_worst =
T_sample + T_pipeline + T_vehicle

D_reaction =
v × T_reaction_worst

D_required =
D_keepout + D_reaction + D_brake
```

### 3.1 为什么使用“最坏采样等待”

如果障碍物刚好在上一帧曝光结束后进入可观测区域，则系统可能等待接近一个完整 update period 才获得下一帧。

因此实时系统不能只用平均半周期 `1/(2f)` 做安全筛查。

### 3.2 理想匀减速公式只能做初筛

可以用：

```text
D_brake_ideal = v² / (2a)
```

做简单 sensitivity screening。

但 PX4 Collision Prevention 实际考虑 jerk 与 acceleration，真实多旋翼的姿态变化、推力余量、控制器 tracking 都会改变停止/转向距离。

因此：
> `v²/(2a)` 只能用于早期算术筛查，产品决策必须使用实机日志或经过验证的车辆动力学模型。

## 4. 更新频率的空间含义

下面仅计算“一个 update period 内的前进距离”：

| 速度 | 10 Hz | 20 Hz | 30 Hz | 60 Hz |
|---:|---:|---:|---:|---:|
| 1.5 m/s | 0.150 m | 0.075 m | 0.050 m | 0.025 m |
| 3.0 m/s | 0.300 m | 0.150 m | 0.100 m | 0.050 m |
| 4.0 m/s | 0.400 m | 0.200 m | 0.133 m | 0.067 m |
| 7.8 m/s | 0.780 m | 0.390 m | 0.260 m | 0.130 m |

这张表不包含任何算法 latency 或 vehicle response。

因此“30 Hz 足够吗？”必须改写为：

> 在目标速度、有效探测距离、P95/P99 Frame Age 和实机 vehicle response 下，30 Hz 是否给安全距离留下足够裕量？

## 5. PX4 4 m/s / 10 Hz 锚点的距离量级

只用同一 PX4 当前页面给出的公开量级做算术：

- 4 m/s × 100 ms sample period = **0.4 m**
- external vision sensor delay 0.2 s → **0.8 m**
- tracking delay 0.1–0.5 s → **0.4–2.0 m**

若简单相加 sensor + tracking：
- 0.3–0.7 s
- 位移 **1.2–2.8 m**

再加“最坏等待一帧”100 ms：
- 简化 reaction distance ≈ **1.6–3.2 m**

这**不是 stopping distance**，因为还没有加入：
- jerk/acceleration braking；
- `CP_DIST`；
- 机体尺寸；
- 动态障碍物；
- false negative；
- queue jitter；
- 转向而非刹停的轨迹约束。

它的唯一用途是说明：
> 如果闭环里存在数百毫秒量级 delay，空间损失可能远大于毫秒级 planner solver 本身。

## 6. 本项目已观测 Camera 输出：只能作为一层已知事实

既往单路调试记录已确认 downstream media output：
- **1072 × 1280**
- **NV12**

但当前证据仍不足以确认：
- 六路都使用完全相同的 mode；
- 六路都为 SC132GS；
- 实际 FPS；
- Sensor RAW bit-depth；
- 实际 MIPI lane rate；
- 六路 hardware sync skew。

因此建立：
`data/calculations/six-camera-observed-mode-sensitivity.csv`

它只做一个问题：
> 如果六路最终都输出 1072×1280 NV12，那么在 10/20/30/60/120 Hz 下，内存图像表示和 frame period 分别是多少？

| FPS 假设 | 六路 Pixel Rate | NV12 单份 frame-stream payload | 4 m/s 每帧位移 |
|---:|---:|---:|---:|
| 10 | 82.33 MP/s | 123.49 MB/s | 0.400 m |
| 20 | 164.66 MP/s | 246.99 MB/s | 0.200 m |
| 30 | 246.99 MP/s | 370.48 MB/s | 0.133 m |
| 60 | 493.98 MP/s | 740.97 MB/s | 0.067 m |
| 120 | 987.96 MP/s | 1481.93 MB/s | 0.033 m |

其中：
- NV12 用 1.5 byte/pixel 做 downstream memory representation 算术；
- 这些值**不是 Sensor RAW/MIPI bandwidth，也不是 DDR 总带宽**；
- 120 Hz 只因为 SC132GS 公开规格的 max frame rate 为 120 fps，作为 stress-only sensitivity；**不是项目实际 FPS**。

SC132GS 官方事实见：
`references/datasheets/sc132gs-public-facts.md`

## 7. 平台 Benchmark 应从“FPS”升级为“deadline budget”

后续平台测试至少打这些时间戳：

```text
t0  sensor exposure/start-of-frame
t1  frame available in driver
t2  ISP / NV12 ready
t3  preprocess complete
t4  DNN/depth result ready
t5  fusion/map ready
t6  planner output ready
t7  FCU receives command
t8  vehicle response begins
```

计算：
- `T_sensor = t2 - t0`
- `T_perception = t4 - t2`
- `T_fusion = t5 - t4`
- `T_planner = t6 - t5`
- `T_command = t7 - t6`
- `T_vehicle = t8 - t7`
- `Frame Age at command = t7 - t0`

必须报告：
- P50
- P95
- P99
- maximum
- deadline miss ratio
- dropped frames
- queue depth

平均 FPS 只能作为辅助指标。

## 8. 对平台适配矩阵的影响

这一模型并不直接判定哪个平台“最好”，而是把后续判断变成：

### 一体 SoC / SoM
如 Jetson Orin、IQ-9075、RK3588：
- 能否在 W1+W2+W3+W6 并发下满足 `Frame Age P99`？
- zero-copy / shared buffer 是否减少 `T_queue` 和 DDR traffic？
- CPU/GPU/NPU 是否存在抢占/调度导致 tail latency？

### Host + Accelerator
如 RK3588 + M50 / Metis / Hailo：
- PCIe / host preprocessing 是否增加 `T_queue + T_perception`？
- SLAM/planning 在 Host 上是否与 accelerator feeding 争用 CPU/DDR？
- 加速卡单模型更快，是否真正让 `t7-t0` 下降？
- total system power / thermal 是否允许持续运行？

## 9. 当前仍不能冻结的指标

截至本轮，以下仍不能凭公开资料替本项目决定：

- 目标最大飞行速度；
- 最小有效障碍探测距离；
- 最小 keep-out distance；
- 实机 vehicle tracking delay；
- 最大加速度/jerk 与真实 braking/turning envelope；
- 实际 Camera FPS；
- 避障使用 detection、depth、optical flow、stereo 还是组合；
- `N_detection / N_depth / N_vio`。

因此本项目**暂不发布“避障必须 ≤XX ms / ≥XX FPS”这样的固定要求**。

正确的下一步是冻结上述任务/动力学输入，再由本模型反推出：
- sensor update floor；
- Frame Age P95/P99 budget；
- perception/planning 分配预算；
- 有效 sensor range；
- 各平台应达到的 deadline。
