# W6 Planning / Optimization Workload Profile

- 状态：v0.1
- 日期：2026-09-30

## 第一版 CPU 基线：Nav2 MPPI

官方当前文档：
- Model Predictive Path Integral
- sampling-based predictive controller
- supports Differential / Omnidirectional / Ackermann
- measured 100+ Hz on modest 4th-gen Intel i5

官方 example：
- controller_frequency = 30Hz
- time_steps = 56
- model_dt = 0.05
- batch_size = 2000
- iteration_count = 1
- visualize = false

## Benchmark

Baseline 保持上述 example 参数，记录：
- mean cycle time
- P95/P99
- deadline miss
- CPU/core utilization
- memory
- power

Scaling：
- batch_size
- time_steps
- obstacle density
- control frequency

## 与 Learned Planner 分开

经典优化 planner 和 E2E/learned planner 分别测，不强行换算成同一 TOPS。

## 边界

官方 30Hz/100+Hz 数据只作为 Nav2 MPPI reference，不代表所有机器人规划频率要求，也不能把 x86 成绩直接外推到 ARM。

## Reference
- https://docs.nav2.org/rolling/configuration_and_development/configuration_guide/controller_plugins/mppi_controller/configuring_mppic/
