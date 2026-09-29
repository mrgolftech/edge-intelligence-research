# UAV / UAS 端侧智能应用与计算需求

- 状态：v0.1
- 日期：2026-09-30
- 范围：不限定六摄像头，覆盖当前无人机典型任务、自主导航与未来智能演进

## 1. 已确认的典型应用

公开综述和现有产品共同支持 UAV 的以下应用：

- 基础设施/工业巡检
- 测绘与三维重建
- 环境/农业监测
- 监视与侦察
- 搜索与救援
- 物流/运输
- GNSS拒止自主导航
- 多机协同

2023 GPS-denied UAV review 明确列举 terrain exploration、disaster assistance、industrial inspection 等；2025 GNSS-denied review 分析了 132 篇近期论文，并将 vision、LiDAR、INS、terrain-aided navigation、SLAM、VO、VIO、多模态融合纳入同一定位体系。

Skydio X10 当前官方产品则提供依赖视觉环境理解和避障的自主飞行，包括低/零光条件下的 NightSense，说明“机载感知 + 本地导航”已经是现实产品能力，而不仅是实验室概念。

## 2. UAV 需求不是一个单一负载

### A. Payload Intelligence

巡检/监视主要负载可能是：
- 高分辨率可见光/IR
- detection / tracking / segmentation
- encode / record / uplink

计算关注：
- ISP/VPU
- NPU/GPU
- DDR
- storage/network

### B. Navigation Intelligence

GNSS拒止/室内/复杂低空：
- Optical Flow
- VIO
- SLAM
- LiDAR/vision/inertial fusion
- obstacle perception
- planning

计算关注：
- CPU/GPU
- synchronization
- low latency
- memory bandwidth
- robustness

### C. Mission Intelligence

更高层：
- semantic scene understanding
- target prioritization
- multi-step mission
- human-language interaction
- swarm task allocation

这类负载可能引入：
- Transformer
- VLM/LLM
- distributed planning

但当前不能视为所有 UAV 的标配。

## 3. SWaP 是 UAV 特有的核心约束

GNSS-denied综述明确把 Size, Weight, and Power 与 real-time feasibility 作为实际架构选择因素。

因此 UAV 平台不能只问“性能够不够”，还要问：

- 每瓦性能
- 散热器/载板重量
- 电池续航影响
- vibration/environment
- camera/IMU timestamp
- 断网情况下能否继续安全执行

## 4. 工程结论

### 已确认事实
- VIO/SLAM、多传感器融合和 obstacle/collision prevention 是无人机自主导航的重要技术路线。
- Companion Computer 是 PX4 体系中承载复杂视觉计算的典型架构。
- 商用自主无人机已经本地执行视觉避障与导航。

### 工程推断
UAV 计算平台应分开评估：
1. payload AI；
2. localization/navigation；
3. mission AI。

一颗 NPU 的峰值 TOPS 很难同时说明这三类能力。

## 5. References

1. Jarraya et al., Gnss-denied unmanned aerial vehicle navigation: analyzing computational complexity, sensor fusion, and localization methodologies, Satellite Navigation, 2025.  
   https://link.springer.com/article/10.1186/s43020-025-00162-z
2. Chang et al., A review of UAV autonomous navigation in GPS-denied environments, Robotics and Autonomous Systems, 2023.  
   https://www.sciencedirect.com/science/article/pii/S0921889023001720
3. PX4 Computer Vision.  
   https://docs.px4.io/main/en/advanced/computer_vision
4. Skydio X10.  
   https://www.skydio.com/x10
