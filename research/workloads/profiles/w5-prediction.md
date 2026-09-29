# W5 Prediction / Situation Understanding Workload Profile

- 状态：v0.1
- 日期：2026-09-30

## 公共基线：Waymo Open Motion Dataset

官方当前数据：
- 103,354 segments
- each 20 seconds
- object tracks at 10Hz
- 574 hours
- 9-second windows：1s history + 8s future
- vehicles / pedestrians / cyclists
- 3D map context

## 指标

Waymo Motion Dataset论文：
- minADE
- minFDE
- Miss Rate
- Overlap Rate
- mAP

2025 Interaction Prediction challenge：
- primary metric: Soft-mAP
- tie-break: minADE

## 端侧测试

第一版：
- 官方 10Hz sample replay 作为**数据集原速回放基线**
- 5 / 10 / 20Hz scheduler 作为工程压力测试

记录：
- inference latency
- P95/P99
- max tracked agents
- memory
- CPU/GPU/NPU
- power

## 边界

- 10Hz 是数据集速率，不是所有无人系统的行业要求
- UAV/USV prediction 不应直接套 Waymo 目标分布
- 如果加入 VLM semantic reasoning，应额外归入 W7

## References
- https://waymo.com/open/data/motion/
- https://waymo.com/open/about/
- https://openaccess.thecvf.com/content/ICCV2021/html/Ettinger_Large_Scale_Interactive_Motion_Forecasting_for_Autonomous_Driving_The_Waymo_ICCV_2021_paper.html
