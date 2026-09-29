# Benchmark Reference：Nav2 MPPI

- 项目：Navigation2
- 获取日期：2026-09-30
- 用途：W6 Planning / Optimization

## 官方事实

MPPI Controller：
- sampling-based Model Predictive Path Integral
- Differential / Omnidirectional / Ackermann
- current docs: 100+ Hz on modest 4th-gen Intel i5

Example：
- controller_frequency: 30.0
- time_steps: 56
- model_dt: 0.05
- batch_size: 2000
- iteration_count: 1
- visualize: false

文档指出 visualization 会增加计算开销。

来源：
https://docs.nav2.org/rolling/configuration_and_development/configuration_guide/controller_plugins/mppi_controller/configuring_mppic/

这些数字只作为 reference software baseline，不能作为所有机器人的规划频率标准。
