# AGENTS.md

## 1. 项目定位

本仓库用于持续研究无人装备、机器人和边缘智能系统的端侧计算需求、技术路线与实现平台，并沉淀可追溯资料、分析、数据、Benchmark、脚本和最终报告。

核心方法：

> **应用/任务场景 → 功能栈 → 自主性画像 → 数据与算法工作负载 → 算力与系统资源 → 部署架构 → 芯片/模组/产品 → Benchmark 验证**

禁止从某个产品的 TOPS 参数反推应用需求。

## 2. 研究范围

覆盖但不限于：

- UAV / UAS
- UGV / 自动驾驶车辆
- AMR / AGV
- USV / 无人船
- 移动机器人与操作机器人
- 固定式边缘感知设备
- 多无人系统 / 多机器人
- 边云协同自主系统

六摄像头无人平台是重要工程 Case，但不是项目总体研究范围的中心。

## 3. 能力框架原则

### 3.1 不自创跨域线性等级
不得把项目自定义的 L1/L2/L3/L4/L5 当作行业能力等级。
跨 UAV、UGV、USV、机器人不存在可直接通用的单一线性等级时，应明确说明，并采用多维度描述。

### 3.2 功能栈采用行业常用术语
优先按：
- Sensing / Data Acquisition
- State Estimation / Localization
- Mapping / World Modeling
- Perception
- Prediction / Tracking
- Planning / Decision
- Control / Execution
- Mission / Task Management
- Human-Machine Interaction / Remote Operation
- Multi-Agent Coordination / Fleet Management
- Safety / Security / Health Monitoring
- Edge-Cloud Collaboration

具体领域可按 PX4、Nav2、Autoware、ROS 2/Isaac ROS 等公开架构调整。

### 3.3 自主性采用多维画像
跨域自主性优先参考 NIST ALFUS：
- Mission Complexity
- Environmental Complexity
- Human Independence / HRI

领域专用标准仅用于适用领域：
- SAE J3016：道路车辆
- IMO MASS：海上自主船

## 4. 应用研究方法

研究任何应用时，先明确：
1. 平台；
2. 任务；
3. 环境；
4. 人类参与；
5. 传感器；
6. 功能模块；
7. 实时/安全关键任务；
8. 可学习化/可边云协同任务。

之后才建立工作负载和计算需求。

## 5. 工作负载建模

至少分析：
- 传感器数量/分辨率/帧率/采样率
- 视频/点云/雷达/IMU吞吐
- 时间同步/标定
- 模型类型/规模/输入/精度
- 多任务并发
- CPU/GPU/NPU/DSP/MCU
- 内存/带宽/Cache
- ISP/VPU/DMA/零拷贝
- PCIe/Ethernet/MIPI/SerDes/CAN
- P50/P95/P99、Frame Age、deadline
- 功耗/热/SWaP-C
- 长时间稳定性

不得用“需要XX TOPS”替代工作负载分析。

## 6. Benchmark 证据规则

第一版公共基线包括：
- W1：EuRoC / TUM-VI / nuScenes sensor profiles
- W2：ORB-SLAM3 + EuRoC / TUM-VI
- W3：MLPerf Inference Edge YOLOv11
- W4：MLPerf PointPainting + BEVFormer / nuScenes
- W5：Waymo Open Motion Dataset
- W6：Nav2 MPPI
- W7：OpenVLA + LIBERO / LIBERO-Plus
- W8：基于 MRTA/Multi-Robot 文献定义参数化 scaling experiment

必须区分：
- **公开 benchmark 条件**
- **行业需求门槛**
- **本项目工程压力测试档位**

三者不得混写。

数据集的 10Hz/20Hz、模型论文 FLOPs、论文运行平台都只能作为具体测试条件，不自动成为产品要求。

## 7. 计算平台评价

TOPS 只能作为一个指标。必须同时关注：
- CPU
- GPU
- NPU/AI ASIC
- INT4/INT8/FP16/BF16/FP32
- 内存容量/带宽
- 视频/视觉硬件
- I/O
- 软件生态
- 实时性/隔离
- SWaP-C
- 可靠性/温度/供货
- 国产化
- 实际 Benchmark

必须区分：
> 理论峰值算力、模型吞吐、端到端延迟、多任务并发、持续热稳态性能。

## 8. 技术路线

长期跟踪：
- MCU/实时控制 + Companion Computer
- 高集成异构 SoC
- GPU 边缘计算
- NPU / AI ASIC
- PCIe / M.2 / MXM AI 加速器
- 车规/机器人专用 SoC
- Edge Server / Compute Box
- Edge-Cloud
- Multi-Robot / Swarm Distributed Computing

不得混淆芯片、SOM、开发板、加速卡、整机。

## 9. 未来趋势

趋势必须有论文/官方路线/真实产品依据，重点：
- 多传感器融合/BEV/Occupancy
- Transformer
- End-to-End
- World Models
- Foundation Models
- VLM/VLA/Embodied Reasoning
- 端侧 Generative AI
- 多机器人协作
- Edge-Cloud
- 学习系统与确定性安全系统融合

趋势不等于成熟量产能力。

## 10. 当前工程 Case：六摄像头无人平台

用于验证：
- 多摄像头采集/同步
- 视频处理
- 检测/跟踪
- 多摄像头融合
- 深度/障碍
- VIO/SLAM
- 规划/避障
- 可选 VLM

不得外推到所有无人系统。

## 11. 信息源与证据

优先级：
1. 标准/监管/官方规范
2. Datasheet / Manual / Developer Guide
3. 官方 GitHub
4. 同行评审论文/高质量综述
5. 厂商白皮书/技术博客
6. 权威报告
7. 行业媒体
8. 社区

标记：
- 已确认事实
- 厂商宣称
- 第三方资料
- 工程推断
- 待验证

未知写“未确认”。

## 12. 资料落盘

建议：
```text
research/scenarios/
research/workloads/
research/architecture/
research/chips/
research/vendors/
research/products/
research/algorithms/
research/trends/
references/standards/
references/benchmarks/
references/datasheets/
references/papers/
references/reports/
references/webpages/
references/github/
data/product-specs/
data/benchmarks/
data/calculations/
cases/six-camera-uav/
comparisons/
reports/
assets/
scripts/
```

不机械创建空目录。

## 13. 产品数据

至少记录：
- 厂商/产品/芯片/形态
- CPU/GPU/NPU/DSP/MCU
- 数值精度
- 内存容量/类型/带宽
- ISP/VPU/Camera
- PCIe/网络/CAN/I/O
- 功耗/尺寸/重量/温度
- OS/SDK/ROS2/PyTorch/ONNX
- LLM/VLM/VLA
- 供货/价格/国产化
- Benchmark条件与结果
- 来源/证据等级

不得按 TOPS 单指标排名。

## 14. Benchmark

目标：
> **资料调研 → 工作负载模型 → 可量化 Benchmark → 可复现实验 → 工程结论**

优先：
- W1多路视频
- W2 VIO/SLAM
- W3 detection
- W4 3D/BEV
- W5 prediction
- W6 planning
- W7 VLM/VLA
- W8 multi-agent
- DDR/PCIe/network
- power/thermal/stability

Benchmark 至少记录：
- software/model/version
- precision
- input
- latency/P95/P99
- throughput
- CPU/GPU/NPU
- memory/DDR
- power/temp
- throttling

## 15. Agent 工作规则

1. 先读 README.md、AGENTS.md 和相关文件；
2. 基于仓库实际状态；
3. 先检索避免重复；
4. 当前产品/标准/SDK/趋势必须查最新来源；
5. 长期价值结论和来源落盘；
6. 图表保存数据/脚本；
7. 实验可复现；
8. 重要阶段提交 Git；
9. 结论变化同步修引用；
10. 禁止提交秘密信息。

## 16. 禁止事项

- 禁止自创线性自主等级并称行业标准；
- 禁止用 SAE 等级覆盖 UAV/USV/机器人；
- 禁止只看 TOPS；
- 禁止把厂商宣传当独立验证；
- 禁止捏造参数；
- 禁止混淆产品形态；
- 禁止脱离任务讨论算力；
- 禁止用单一 Benchmark 推完整系统；
- 禁止把数据集采样率当行业硬门槛；
- 禁止把裸权重内存当整机运行内存；
- 禁止把未来趋势表述为当前成熟能力。

## 17. 当前进展与优先研究

已完成第一版：
- 跨 UAV / UGV / AMR / USV / Robot / Fixed Edge 应用事实库；
- 场景—功能栈—自主性—工作负载矩阵；
- W1–W9 workload taxonomy；
- W1–W8 定量 workload profile；
- EuRoC/TUM-VI、nuScenes/Waymo、MLPerf、Nav2 MPPI、OpenVLA/LIBERO 等公共 benchmark 基线；
- 可复用 sensor payload / model memory calculation data；
- 真实产品案例证据；
- 六摄像头 workload model。

下一阶段：
1. 建立当前端侧计算产品结构化事实数据库；
2. 收集条件明确的产品公开 Benchmark；
3. 建立 workload → compute resource → platform 适配矩阵；
4. 六摄像头 Case 冻结参数并完成 W1/W2/W3 第一轮定量推导；
5. 形成可复现实验脚本；
6. 分析 E2E/VLM/VLA/World Model 的增量资源需求；
7. 形成需求驱动的平台选型方法。
