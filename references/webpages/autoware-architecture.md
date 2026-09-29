# Autoware Architecture 参考摘要

- 项目：Autoware
- 来源：Autoware Foundation 官方文档
- 获取日期：2026-09-29

## 当前架构事实

Autoware 官方描述其覆盖完整 autonomous driving stack。

传统高层架构包含：
- Sensing
- Map
- Localization
- Perception
- Planning
- Control
- Vehicle Interface

Perception 接收 sensing/localization/map 信息，输出动态物体、障碍物、交通信号、occupancy 等语义信息供 planning 使用。

Autoware 2.0 文档还明确指出传统固定 pipeline：
Sensing → Perception → Localization → Planning → Trajectory
对 E2E / diffusion 等新方法不够灵活，因此提出 Generator-Selector 概念，让传统规划、E2E或学习型生成器并存，并由 Selector 进行安全检查和选择。

## 对本项目的意义

1. sensing/perception/localization/planning/control 是有成熟工程依据的功能栈，不需要自造“能力等级”。
2. 传统模块化与 E2E/学习模型将长期共存。
3. 新模型进入规划链路时，安全检查、系统隔离和验证同样重要。

## 来源

- https://docs.autoware.org/main/home/
- https://docs.autoware.org/main/design/autoware-architecture-v1/
- https://docs.autoware.org/main/design/autoware-architecture-v1/components/perception/
- https://docs.autoware.org/main/design/autoware-architecture-v2/
