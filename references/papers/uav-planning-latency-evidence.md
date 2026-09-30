# UAV 局部规划计算时延：论文与官方实现证据

- 获取日期：2026-09-30
- 状态：verified-public-evidence
- 目的：回答“路径规划计算本身占多少时延”，并防止把 planner runtime 等同于端到端避障响应

## 1. EGO-Planner 论文

论文：
Zhou X, Wang Z, Ye H, Xu C, Gao F. EGO-Planner: An ESDF-Free Gradient-Based Local Planner for Quadrotors. IEEE RA-L, 2021.

官方作者 PDF：
https://zhepeiwang.github.io/pubs/ral_2021_egoplan.pdf

DOI：
https://doi.org/10.1109/LRA.2020.3047728

论文 Table III：
- EWOK：ESDF 6.43 ms；planning 1.39 ms
- Fast-Planner：ESDF 4.01 ms；planning 3.29 ms
- EGO-Planner：无 ESDF update；planning **0.81 ms**

真实飞行：
- cluttered indoor environment 中达到 **3.56 m/s**
- outdoor forest 中速度超过 **3 m/s**
- 论文强调 limited camera FOV 下需要在发现新目标/碰撞威胁后快速生成可行轨迹

### 证据边界

Table III 的 planning benchmark 与 3.56 m/s real-world flight 是同一论文中的不同实验，**不能拼成一个“3.56m/s 时端到端反应=0.81ms”的结论**。

仅做距离数量级说明时：
- 3.56 m/s × 0.81 ms ≈ 2.9 mm

这个算术只用于说明：
> millisecond 级 planner solver 时间可能远小于 sensor/vision/vehicle-response 的百毫秒量级。

它不是 measured collision-response distance。

## 2. EGO-Planner 官方代码的调度/安全默认值

官方仓库：
https://github.com/ZJU-FAST-Lab/ego-planner

当前 master 中：
- README：planner total planning time “around 1ms”
- `execFSMCallback` timer：0.01 s → **100 Hz**
- `checkCollisionCallback` timer：0.05 s → **20 Hz**
- simulation/default launch：
  - max_vel = 2.0 m/s
  - max_acc = 3.0 m/s²
  - max_jerk = 4.0 m/s³
  - planning_horizon = 7.5 m
  - depth_filter_maxdist = 5.0 m
  - max_ray_length = 4.5 m
  - emergency_time = 1.0 s

来源文件：
- https://github.com/ZJU-FAST-Lab/ego-planner/blob/master/src/planner/plan_manage/src/ego_replan_fsm.cpp
- https://github.com/ZJU-FAST-Lab/ego-planner/blob/master/src/planner/plan_manage/launch/run_in_sim.launch
- https://github.com/ZJU-FAST-Lab/ego-planner/blob/master/src/planner/plan_manage/launch/advanced_param.xml

### 边界

这些是开源工程的默认/仿真配置，不是无人机行业标准，也不是本项目需求。

100 Hz FSM / 20 Hz safety timer 只说明软件状态机调度路径；不代表 camera/perception/planner 的真实端到端输出都达到对应频率。

## 3. FASTER：高速飞行事实锚点

论文：
Tordesillas J, Lopez BT, Everett M, How JP. FASTER: Fast and Safe Trajectory Planner for Navigation in Unknown Environments.

arXiv：
https://arxiv.org/abs/2001.04420

论文报告：
- unknown cluttered environment 中真实飞行速度最高达到 **7.8 m/s**
- 方法通过始终保留 free-known space 内的 safe backup trajectory 来保证可行/安全路径

### 本项目用途

7.8 m/s 证明公开研究中确实存在远高于 3–4 m/s 的未知环境自主飞行。

但该结果不能转化成：
- “所有 UAV 应按 8 m/s 设计”
- “需要某固定 FPS/TOPS”

它只适合作为高动态 stress anchor：
> 速度越高，同样 10/20/30 ms latency 所对应的空间位移越大，sensor range 与 reaction horizon 必须共同提高。

## 4. 关键结论

公开证据支持以下判断：

1. planner solver 可以做到毫秒量级；
2. 完整避障闭环仍可能由 sensor/vision/queueing/vehicle response 主导；
3. 因此 Benchmark 必须分别记录：
   - `T_sample`
   - `T_sensor/ISP`
   - `T_perception`
   - `T_map/fusion`
   - `T_planner`
   - `T_command`
   - `T_vehicle`
4. 只报“planner 1ms”或“YOLO 10ms”都不能证明系统可安全避障。
