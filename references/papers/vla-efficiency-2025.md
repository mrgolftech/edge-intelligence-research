# 文献摘要：Efficient VLA and Edge Constraints (2025)

- 文献：Efficient Vision-Language-Action Models for Embodied Manipulation: A Systematic Survey
- 发布时间：2025-10
- 类型：Systematic Survey
- URL：https://arxiv.org/abs/2510.17111
- 获取日期：2026-09-30

## 已确认事实

论文指出 VLA 将自然语言指令和视觉观察映射为机器人动作。

论文明确把以下问题视为 VLA 端侧/机器人部署核心矛盾：
- massive computational demand
- memory demand
- real-time requirement
- onboard mobile platform constraints
- latency
- memory footprint
- training/inference cost

综述从以下方向讨论效率优化：
- model architecture
- perception feature
- action generation
- training/inference strategy

## 补充事实

2025 systematic review：
Vision Language Action Models in Robotic Manipulation: A Systematic Review
https://arxiv.org/abs/2507.10672

系统分析：
- 102 VLA models
- 26 datasets
- 12 simulation platforms

OpenVLA：
https://arxiv.org/abs/2406.09246
- 7B parameters
- 970k real-world robot demonstrations

## 对本项目支撑

VLA 应纳入未来工作负载，但不能直接按传统 INT8 CV TOPS 评估。

必须增加：
- memory capacity
- bandwidth
- low precision support
- TTFT/action latency
- model footprint
- concurrent real-time workload
