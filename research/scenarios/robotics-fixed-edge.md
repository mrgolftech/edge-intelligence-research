# 机器人、VLA 与固定边缘智能计算需求

- 状态：v0.1
- 日期：2026-09-30

## 1. 机器人传统负载仍是基础

移动/操作机器人通常同时需要：
- perception
- localization
- planning
- manipulation / motion planning
- control
- HRI
- safety

仓储机器人综述进一步证明 perception/manipulation、SLAM、path planning、多机器人协调均是现实工程问题。

## 2. VLA 是新增负载，而不是“替代全部机器人软件”

OpenVLA：
- 7B parameter
- vision-language-action
- 970k real-world robot demonstrations

2025 VLA systematic review 对 102 个 VLA model 进行系统分析，说明该路线已形成规模化研究体系。

另一篇 2025 efficient VLA survey 明确指出：
- VLA 计算和内存需求很大；
- 与 onboard mobile manipulator 的实时和边缘约束冲突；
- latency、memory footprint、training/inference cost 是核心优化问题。

因此本项目把 VLA 作为独立工作负载族 W7。

## 3. 机器人平台的分层

### 必须确定性/低延迟
- joint/actuator control
- collision safety
- local motion control
- safety supervisor

### 可学习化
- perception
- grasp / pose
- learned planning
- policy
- multimodal reasoning

### 可边云协同
- large model reasoning
- knowledge retrieval
- long-horizon memory
- fleet/task knowledge

这意味着“Physical AI平台”需要同时承载不同关键度任务，而不是只追求大模型吞吐。

## 4. 固定边缘智能：高算力不等于高自主

NVIDIA Metropolis 当前应用包含：
- multi-camera tracking
- automated visual inspection
- intelligent transportation
- industrial automation
- retail
- robot safety
- VLM / video analytics agents

固定系统往往没有：
- localization
- navigation
- motion control

但可能有：
- 多路视频 decode
- 多模型并发
- cross-camera tracking
- 长时存储
- VLM 视频理解

因此这是反例：
> AI算力需求和“自主程度”不是同一个轴。

## 5. Edge / Cloud 边界

2025 Edge Robotics survey 的核心结论之一是：
- time-sensitive robotics 需要低延迟；
- cloud-only 受 network latency / connectivity 影响；
- edge 能把计算放到靠近机器人数据源的位置。

但该综述同时展示了 SLAM、multi-robot 等 offload 研究，说明“全部必须 onboard”也不是正确结论。

更合理的是任务分层：
- safety / hard real-time：on-device
- latency-sensitive heavy compute：on-device / near-edge
- global optimization / training / archival：edge/cloud

## 6. References

1. OpenVLA. https://arxiv.org/abs/2406.09246
2. Vision Language Action Models in Robotic Manipulation: A Systematic Review, 2025.  
   https://arxiv.org/abs/2507.10672
3. Efficient Vision-Language-Action Models for Embodied Manipulation: A Systematic Survey, 2025.  
   https://arxiv.org/abs/2510.17111
4. Edge Computing and Its Application in Robotics: A Survey, 2025.  
   https://www.mdpi.com/2224-2708/14/4/65
5. NVIDIA Metropolis.  
   https://www.nvidia.com/en-us/autonomous-machines/intelligent-video-analytics-platform/
