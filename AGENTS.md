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

优先按以下自主系统功能分解：

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

具体领域可按其公开架构调整，例如 PX4、Nav2、Autoware、ROS 2/Isaac ROS。

### 3.3 自主性采用多维画像

跨域自主性分析优先参考 NIST ALFUS：

- Mission Complexity
- Environmental Complexity
- Human Independence / HRI

领域专用标准仅用于适用领域：

- SAE J3016：道路车辆驾驶自动化
- IMO MASS：海上自主船
- 其他无人系统：采用相应标准/论文/行业术语，不把 SAE 等级生搬硬套

## 4. 应用研究方法

研究任何应用时，先回答：

1. 平台是什么：UAV/UGV/USV/AMR/机器人/固定边缘设备？
2. 任务是什么：巡检、监视、测绘、搜救、物流、操作、导航、协同等？
3. 环境是什么：室内/室外、动态/静态、GNSS可用性、天气/光照、海况/道路等？
4. 人如何参与：遥控、监督、自主执行、远程接管？
5. 传感器是什么：Camera/IR/LiDAR/Radar/IMU/GNSS/AIS/Audio 等？
6. 需要哪些功能模块？
7. 哪些任务必须实时、确定性执行？
8. 哪些任务可由学习模型、大模型或边云协同承担？

之后才建立工作负载和计算需求。

## 5. 工作负载建模

至少分析：

- 传感器数量、分辨率、帧率、采样率
- 视频/点云/雷达/IMU 等数据吞吐
- 时间同步和标定
- 模型类型、规模、输入尺寸、精度
- 多模型/多任务并发
- CPU/GPU/NPU/DSP/MCU 分工
- 内存容量、带宽、Cache
- ISP、视频编解码、DMA、零拷贝
- PCIe、Ethernet、MIPI、SerDes、CAN
- 实时性、P95/P99延迟、Frame Age
- 功耗、散热、尺寸、重量、成本
- 长时间稳定性

不得直接用“需要 XX TOPS”替代工作负载分析。

## 6. 计算平台评价

TOPS 只能作为一个指标。

必须同时关注：

- CPU通用性能
- GPU通用并行与图形/视觉能力
- NPU/AI ASIC及实际算子覆盖
- INT4/INT8/FP16/BF16/FP32
- 内存容量与带宽
- 视频与视觉硬件
- I/O与传感器接入
- 软件生态和模型迁移成本
- 实时性与任务隔离
- SWaP-C
- 可靠性、温度范围、供货
- 国产化
- 实际 Benchmark

必须区分：

> 理论峰值算力、模型吞吐、端到端延迟、多任务并发性能、持续热稳态性能。

## 7. 技术路线

长期跟踪：

- MCU/实时控制 + Companion Computer
- 高集成异构 SoC
- GPU 边缘计算
- NPU / AI ASIC
- PCIe / M.2 / MXM AI 加速器
- 车规/机器人专用计算 SoC
- Edge Server / Compute Box
- Edge-Cloud Collaborative Computing
- Multi-Robot / Swarm Distributed Computing

不得把芯片、SOM、开发板、加速卡和整机直接混为一类比较。

## 8. 未来技术趋势

趋势研究必须有论文、官方技术路线或真实产品作为依据，重点跟踪：

- 多传感器融合与 3D/BEV/Occupancy 表征
- Transformer 与学习增强的感知/规划
- End-to-End 自动驾驶/自主系统
- World Models
- Foundation Models for Robotics
- VLM / VLA / Embodied Reasoning
- 端侧 Generative AI
- 多机器人协作与任务分配
- Edge-Cloud / On-device 协同
- 安全约束下的学习系统与传统确定性系统融合

趋势不等于成熟量产能力。必须区分研究原型、厂商宣称、量产应用和工程推断。

## 9. 当前工程 Case：六摄像头无人平台

用于验证：

- 多摄像头采集/同步
- 视频处理
- 检测/跟踪
- 多摄像头融合
- 深度/障碍物检测
- VIO/SLAM
- 自主避障/规划
- 可选 VLM/多模态任务

该 Case 的结论不得未经验证外推到所有无人系统。

## 10. 信息源与证据

优先级：

1. 标准组织/监管机构/官方规范
2. 官方 Datasheet / Manual / Developer Guide
3. 官方 GitHub
4. 同行评审论文与高质量综述
5. 厂商技术博客/白皮书
6. 权威研究报告
7. 行业媒体
8. 开发者社区/Reddit/X

结论标记：

- **已确认事实**：可靠来源直接支持
- **厂商宣称**：来自厂商材料，未独立验证
- **第三方资料**：来自合作伙伴/经销商/媒体
- **工程推断**：基于事实推导
- **待验证**：证据不足

未知参数写“未确认”，禁止猜测。

## 11. 资料落盘

建议目录：

```text
research/
  scenarios/
  workloads/
  architecture/
  chips/
  vendors/
  products/
  algorithms/
  trends/

references/
  standards/
  datasheets/
  papers/
  reports/
  webpages/
  github/

data/
  product-specs/
  benchmarks/
  calculations/

cases/
  six-camera-uav/

comparisons/
reports/
assets/
scripts/
```

不机械创建空目录。

研究文档尽量包含：

```text
# 研究问题
# 背景
# 已知事实
# 数据
# 分析
# 工程判断
# 风险与限制
# 结论
# 待验证问题
# References
```

网页资料尽量记录标题、机构/作者、发布日期、获取日期、版本、摘要和支撑结论。

## 12. 产品数据

至少记录：

- 厂商/产品/芯片/产品形态
- CPU/GPU/NPU/DSP/MCU
- INT4/INT8/FP16/BF16
- 内存容量/类型/带宽
- ISP/编解码/摄像头接口
- PCIe/网络/CAN/其他I/O
- 功耗/尺寸/重量/温度
- OS/SDK/ROS2/PyTorch/ONNX
- LLM/VLM/VLA支持
- 供货/价格/国产化
- Benchmark条件与结果
- 来源和证据等级

不得按 TOPS 单指标排名。

## 13. Benchmark

纸面参数无法回答时，主动转为实验：

- 多路视频
- 目标检测/跟踪
- 深度/分割
- VIO/SLAM
- 多模型并发
- BEV/Transformer
- VLM/VLA/LLM
- DDR/PCIe/网络带宽
- 功耗/温度/降频
- 长时间稳定性

目标：

> **资料调研 → 工作负载模型 → 可量化 Benchmark → 可复现实验 → 工程结论**

## 14. Agent 工作规则

任何 Agent 修改仓库前：

1. 读取 README.md、AGENTS.md 和相关研究文件；
2. 基于仓库实际状态，不依赖记忆猜测；
3. 先检索已有资料，避免重复；
4. 涉及当前产品、标准、SDK和趋势时查询最新公开来源；
5. 有长期价值的结论和来源应落盘；
6. 图表保存原始数据或生成脚本；
7. 实验保证可复现；
8. 重要阶段形成清晰 Git Commit；
9. 结论变化时同步修订引用和待验证问题；
10. 不提交 API Key、密码、Token 或内部敏感地址。

## 15. 禁止事项

- 禁止自创线性自主等级并表述为行业标准；
- 禁止用道路车辆 SAE 等级直接代表 UAV/USV/机器人；
- 禁止只依据 TOPS 判断适用性；
- 禁止把厂商宣传写成独立验证事实；
- 禁止捏造未知参数；
- 禁止混淆不同产品形态；
- 禁止脱离任务和工作负载讨论算力；
- 禁止用单一 Benchmark 推断完整系统能力；
- 禁止把未来趋势表述为当前成熟能力。

## 16. 当前已确认原则

1. 无人端侧需求研究必须放在广泛应用和行业事实底座上，而不是围绕单个 Case 展开。
2. 通用功能链采用 sensing、state estimation/localization、perception/world model、planning/decision、control/execution 等行业常见划分。
3. 跨域自主性使用多维画像，不采用项目自创 L1–L5。
4. NIST ALFUS 可作为跨无人系统自主性分析的重要参考；SAE J3016、IMO MASS 属于领域专用框架。
5. 六摄像头系统作为工程验证 Case 保留。
6. TOPS 只能作为平台指标之一。
7. 对纸面资料无法判断的问题，通过可复现实验验证。

## 17. 当前优先研究

1. 建立跨 UAV/UGV/USV/AMR/机器人应用事实库；
2. 建立“场景—功能栈—自主性—工作负载”矩阵；
3. 建立典型工作负载族；
4. 按统一数据模型建立当前端侧计算产品事实库；
5. 分析经典模块化、学习增强、E2E、VLM/VLA、World Model 等路线对算力需求的影响；
6. 用六摄像头 Case 进行定量验证；
7. 最终形成需求驱动的端侧计算平台选型方法。
