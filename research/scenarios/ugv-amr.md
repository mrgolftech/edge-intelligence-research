# UGV / 自动驾驶 / AMR 端侧智能应用与计算需求

- 状态：v0.1
- 日期：2026-09-30

## 1. 自动驾驶车辆：完整实时闭环

Autoware 当前官方能力已经形成完整工程事实链：

- sensing
- localization
- perception
- prediction / ML
- planning
- control
- simulation/validation

Waymo 当前 fully autonomous Driver 则使用 camera、lidar、radar 与 onboard AI compute，并在车上实时完成 localization、perception、prediction、planning。

因此城市自动驾驶是典型的：
> 多传感器高带宽 + 高计算 + 严格实时 + 安全冗余

而不是单纯“多跑几个检测模型”。

## 2. AMR：更结构化，但不是低复杂度

2026 Annual Review of Control, Robotics, and Autonomous Systems 的 warehouse/logistics robotics 综述覆盖：

- SLAM
- path planning
- perception/manipulation
- multi-robot coordination
- task allocation
- fleet management
- human-robot collaboration
- safety

MiR250 是当前真实 AMR：
- 用于内部物料运输
- 配置前后 safety laser scanner
- 3D camera 做 pallet/obstacle detection
- proximity sensors
- 支持安全功能
- 可接入 MiR Fleet

说明 AMR 的计算需求至少分为：
- local navigation / safety
- perception
- mission
- fleet-level orchestration

## 3. 单机与车队是两类负载

### 单机端侧
必须优先本地：
- localization
- obstacle detection
- local planning
- motion control
- safety stop

### Fleet / Edge
更适合集中或边缘服务器：
- mission assignment
- traffic management
- fleet scheduling
- historical optimization
- facility/MES/WMS integration

## 4. E2E 的变化

Autoware 2.0 当前已经提出 Generator-Selector：
- rule-based / optimization planners
- E2E models
- learned/sampling-based planners
可并行生成候选轨迹，再由 Selector 做安全检查和选择。

这是重要事实：学习型 planning 正进入工程架构，但不是简单替代安全框架。

## 5. 工程结论

UGV/AMR 的平台需求必须区分：
- vehicle-level real-time compute
- fleet/edge compute

自动驾驶车辆偏高带宽、多模态、高算力与功能安全；
仓储 AMR 可能更偏 CPU/SLAM/安全传感器，但 fleet 系统会引入网络、服务器和调度优化负载。

## 6. References

1. Autoware Documentation. https://docs.autoware.org/main/home/
2. Autoware Architecture v1. https://docs.autoware.org/main/design/autoware-architecture-v1/
3. Autoware Architecture v2. https://docs.autoware.org/main/design/autoware-architecture-v2/
4. Waymo Driver. https://waymo.com/waymo-driver/
5. Waymo 6th-generation Driver, 2026. https://waymo.com/blog/2026/02/ro-on-6th-gen-waymo-driver/
6. Pallottino, Robotics for Warehouses and Logistics, Annual Review of Control, Robotics, and Autonomous Systems, 2026.  
   https://www.annualreviews.org/content/journals/10.1146/annurev-control-032724-020213
7. MiR250. https://mobile-industrial-robots.com/products/robots/mir250/specifications
