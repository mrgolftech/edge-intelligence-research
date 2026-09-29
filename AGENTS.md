# AGENTS.md

## 1. 项目定位

本仓库用于持续研究无人装备、机器人和边缘智能系统的端侧计算需求、技术路线与实现平台，并沉淀可追溯资料、分析、数据、Benchmark、脚本和最终报告。

核心方法：

> **应用/任务场景 → 功能栈 → 自主性画像 → 数据与算法工作负载 → 算力与系统资源 → 部署架构 → 芯片/模组/产品 → Benchmark 验证**

禁止从某个产品的 TOPS 参数反推应用需求。

## 2. 研究范围

覆盖但不限于 UAV/UAS、UGV/自动驾驶、AMR/AGV、USV、移动/操作机器人、固定式边缘感知、多无人系统和边云协同。六摄像头无人平台是工程 Case，不是总体范围中心。

## 3. 能力框架原则

### 3.1 不自创跨域线性等级
不得把项目自定义 L1–L5 当作行业能力等级。跨域优先采用多维描述。

### 3.2 功能栈采用行业常用术语
优先按 Sensing、State Estimation/Localization、Mapping/World Modeling、Perception、Prediction/Tracking、Planning/Decision、Control/Execution，并扩展 Mission、HMI、Multi-Agent、Safety、Edge-Cloud。

具体领域可按 PX4、Nav2、Autoware、ROS 2/Isaac ROS 等公开架构调整。

### 3.3 自主性采用多维画像
跨域优先参考 NIST ALFUS：Mission Complexity、Environmental Complexity、Human Independence/HRI。领域标准只用于适用领域，如 SAE J3016、IMO MASS。

## 4. 应用研究方法

任何应用先明确：
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

不得用“需要 XX TOPS”替代工作负载分析。

## 6. Benchmark 证据规则

第一版公共基线：
- W1：EuRoC / TUM-VI / nuScenes sensor profiles
- W2：ORB-SLAM3 + EuRoC / TUM-VI
- W3：MLPerf Inference Edge YOLOv11
- W4：MLPerf PointPainting + BEVFormer / nuScenes
- W5：Waymo Open Motion Dataset
- W6：Nav2 MPPI
- W7：OpenVLA + LIBERO / LIBERO-Plus
- W8：MRTA/Multi-Robot 参数化 scaling experiment

必须区分公开 benchmark 条件、行业需求门槛、本项目工程压力测试档位。数据集频率与论文参数不能自动成为产品要求。

## 7. 计算平台评价

TOPS 只是一个指标。必须同时关注 CPU、GPU、NPU/AI ASIC、精度、内存/带宽、ISP/VPU/Camera、I/O、软件生态、实时性/隔离、SWaP-C、可靠性、温度、供货、国产化和实际 Benchmark。

必须区分：
> 理论峰值算力、模型吞吐、端到端延迟、多任务并发、持续热稳态性能。

### 7.1 平台适配判断必须有证据
任何“平台适合某 workload”的结论必须至少绑定以下证据之一：
- CASE：命名产品/量产/实际系统
- BENCH：条件明确的 benchmark
- REF：官方 reference design
- SPEC：官方规格/SDK
- PAPER：论文实测

如果只有架构推导，必须标记 **INFER**；没有足够资料标记 **GAP**。

禁止：
- 因为“TOPS 足够”就判定 W2/W4/W6/W9 适配；
- 用完整系统案例推断所有功能都运行在同一芯片；
- 忽略 benchmark 的 host、软件版本、精度、输入和功耗条件；
- 把独立 M.2/PCIe accelerator 与完整 SoC/SoM 当成同一种系统资源。

当前证据索引：
- references/webpages/platform-workload-evidence-2026.md
- research/products/workload-platform-fit-matrix.md

## 8. 技术路线

长期跟踪：
- MCU/实时控制 + Companion Computer
- 高集成异构 SoC
- GPU 边缘计算
- NPU / AI ASIC
- PCIe / M.2 / MXM AI accelerator
- 车规/机器人专用 SoC
- Edge Server / Compute Box
- Edge-Cloud
- Multi-Robot / Swarm

不得混淆芯片、SOM、开发板、加速卡、整机。

## 9. 未来趋势

趋势必须有论文、官方路线或真实产品依据：多传感器融合/BEV/Occupancy、Transformer、E2E、World Models、Foundation Models、VLM/VLA、端侧 Generative AI、多机器人协作、Edge-Cloud、学习系统与确定性安全系统融合。

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

标记：已确认事实、厂商宣称、第三方资料、工程推断、待验证。未知写“未确认”。

## 12. 资料落盘

建议：
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
- Benchmark 条件与结果
- 来源/证据等级

不得按 TOPS 单指标排名。

## 14. Benchmark

目标：
> **资料调研 → 工作负载模型 → 可量化 Benchmark → 可复现实验 → 工程结论**

优先 W1–W8、DDR/PCIe/network、power/thermal/stability。Benchmark 至少记录 software/model/version、precision、input、latency/P95/P99、throughput、CPU/GPU/NPU、memory/DDR、power/temp、throttling。

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
- 禁止把未来趋势表述为当前成熟能力；
- 禁止无案例/文献/规格证据时凭空给出平台适配结论。

## 17. 当前进展与优先研究

已完成第一版：
- 跨域应用事实库；
- 场景—功能栈—自主性—工作负载矩阵；
- W1–W9 taxonomy；
- W1–W8 定量 workload profile；
- 公共 benchmark 基线；
- sensor payload / model memory calculation data；
- 代表平台事实底座；
- **证据驱动 workload → resource → platform 适配矩阵 v0.1**；
- **平台 workload 证据索引（Jetson/Qualcomm/RK3588/Journey6/A2000/Metis/Hailo/LQ50）**；
- 六摄像头 workload model。

下一阶段：
1. 将平台参数与 benchmark 结构化到 data/product-specs 与 data/benchmarks；
2. 补 RK3588、IQ-9075、LQ50 的 W2/W3 可量化证据；
3. 六摄像头 Case 冻结 W1 参数并完成第一轮推导；
4. 分别建立一体 SoC 与 Host+Accelerator Benchmark；
5. 用实测逐步替换 INFER/GAP；
6. 分析 E2E/VLM/VLA/World Model 的增量资源需求；
7. 形成需求驱动的平台选型方法。
