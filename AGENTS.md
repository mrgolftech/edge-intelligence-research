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

### 5.1 避障时延必须由任务动力学反推

对 UAV/UGV/机器人避障，禁止直接规定“模型 ≥XX FPS”或“推理 ≤XX ms”后宣称系统满足实时性。

至少建立：

```text
T_reaction =
T_sample_wait
+ T_sensor/ISP
+ T_queue
+ T_perception
+ T_fusion/map
+ T_planner
+ T_command
+ T_vehicle_response

D_reaction = speed × T_reaction
```

并结合：
- usable sensor/detection range；
- keep-out distance；
- acceleration / jerk / turning capability；
- measured braking/vehicle tracking response；
- P50/P95/P99/max Frame Age；
- drop/deadline miss。

必须区分 **update rate、单模块 compute latency、Frame Age、closed-loop response**。

### 5.2 Camera Routing Set 规则

多 Camera 系统先定义：

```text
C = physical capture cameras
V = VIO/SLAM camera subset
P = PER_VIEW perception subset
F = FUSED_MULTI_VIEW camera subset
D = depth/stereo subset
R = recording subset
```

这些集合可以重叠。禁止把 `N_capture` 自动等同 `N_detection/N_vio/N_depth/N_record`。

对 fan-out 的 source-frame MB/s 估算若采用“一次完整 frame read / consumer”，必须标记为 **analysis equivalent**，不得写成实测 DDR/PCIe bandwidth。

### 5.3 Multi-Camera Perception Topology 规则

多 Camera W3 必须先区分 `PER_VIEW / FUSED_MULTI_VIEW / MIXED`。

- PER_VIEW：可使用 `N_view × Hz` 计算 model calls/s；
- FUSED_MULTI_VIEW：一次 model call 可消费多个 views，必须分别记录 `views/call`、`model calls/s` 与 `input view rate`；
- MIXED：按 branch 分别预算。

禁止把“6 Camera 输入”自动解释为“每个周期 6 次独立 inference”。

### 5.4 Service Demand 规则

对 C2 等多 workload 并发系统，优先按 compute engine 分别建立：

```text
Demand_engine = Σ(InvocationRate_i × measured ServiceTime_i)
```

该值只用于可行性初筛。Demand < 1 不等于 P99 满足；必须继续验证 batching、pipeline overlap、DDR、queue、thermal 与 runtime scheduling。禁止把不同平台/模型/输入条件的 latency 混合计算。

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

如果只有架构推导，必须标记 **INFER**；没有足够资料标记 **GAP**。公开演示但无法复现的结果标记 **DEMO**，不得冒充 BENCH。

禁止：
- 因为“TOPS 足够”就判定 W2/W4/W6/W9 适配；
- 用完整系统案例推断所有功能都运行在同一芯片；
- 忽略 benchmark 的 host、软件版本、精度、输入和功耗条件；
- 把独立 M.2/PCIe accelerator 与完整 SoC/SoM 当成同一种系统资源。

### 7.2 Benchmark 横向比较门槛
只有 model、input、precision、batch/stream mode、host、software version、power condition 等关键条件足够一致时，才允许做定量横向比较。条件不一致时只能并列记录，不得形成快慢排序。

厂商 Benchmark 必须标明来源属性；缺 host/context/quantization 等关键条件时，即使有 FPS 或 tokens/s，也只作为量级锚点。

### 7.3 Benchmark 必须固定版本化 URL

对于会随软件 release 更新的官方性能页：
- 优先保存 `/v/release-X.Y/` URL；
- 记录 software version / release date / access date；
- 禁止把从旧页面摘出的固定数字长期绑定到 `latest` URL；
- 新 release 与旧 release 的数字不得拼成一次端到端 pipeline。

### 7.4 GAP 与负证据也必须落盘

如果经过官方文档/GitHub/论文检索后：
- 找到了官方 Benchmark 方法，但未找到目标平台 numeric result；
- 找到了相邻指标，但其统计边界不属于目标阶段；
- 找到社区结果，但定义自相矛盾或无法追溯；

必须记录：
- access date；
- 搜索/来源入口；
- 当前能确认什么；
- 为什么不能升级证据；
- 下一步复现实验。

禁止：
- “工具存在”写成“性能已验证”；
- 芯片内部 memory bandwidth 写成 PCIe H2D/D2H；
- throughput/双缓冲增益写成更低 Frame Age；
- hw-only inference latency 写成 Camera→result E2E；
- 自相矛盾的社区 E2E 数字进入主 Benchmark。

机器可读审计：`data/benchmarks/latency-gap-audit.csv`。

### 7.5 证据搜索停止条件

当满足以下条件时，单个问题应从“继续搜索”转为“记录 GAP 并进入架构分析”：
- 已查官方产品页/文档；
- 已查官方 GitHub/SDK；
- 已查论文或可靠 Partner Benchmark；
- 只剩社区口径冲突或无法复现的数字；
- 已确认厂商只公开方法、未公开目标 numeric result。

停止搜索不是把 GAP 当作已解决，而是：
> 保留变量、记录阻塞影响、给出未来复现路径。

Phase 2 中只有当 GAP 会改变某个 architecture gate 的结论时才重新触发深挖。

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

六摄像头 Case 必须分别记录 `N_capture / N_detection / N_vio / N_depth / N_record`，禁止默认“六路全部进入同一个 DNN/VIO/Depth workload”。

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

对于 M.2/PCIe 独立加速器，**Host 是一等平台变量**：必须记录 Host SoC/CPU/GPU/VPU、PCIe、预处理、DDR、总功耗和热状态；不得只记录加速卡 TOPS/FPS。

### 13.1 产品化层规则

产品调研必须区分：
- Dev Kit / EVK；
- Production SoM/Core；
- Carrier/Development Board；
- M.2/PCIe/MXM Accelerator；
- Robotics/Industrial Computer；
- Heterogeneous Edge Box；
- Edge Server；
- Solution Ecosystem。

同一 base chip 的不同产品不能合并。

系统厂商与芯片原厂参数冲突时：
- 记录冲突；
- 不猜测；
- 原厂数据用于具体原厂 SKU；
- 系统厂商数据只能用于其系统配置。

产品 Landscape 已完成第一版：
- `research/products/commercial-product-landscape-2026.md`
- `data/product-specs/commercial-product-landscape-2026.csv`
- `research/products/unmanned-edge-solution-shortlist.md`

当产品覆盖已足以支撑最终报告，不再为了“收全型号”继续扩 SKU。

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
- **证据驱动 workload → resource → platform 适配矩阵 v0.9**；
- **平台 workload 证据索引（Jetson/Qualcomm/RK3588/Journey6/A2000/Metis/Hailo/LQ50）**；
- 六摄像头 workload model；
- **结构化平台事实表 data/product-specs/platform-facts.csv**；
- **结构化公开 Benchmark 表 data/benchmarks/public-platform-benchmarks.csv**；
- **平台证据缺口 Backlog 与自动校验脚本**；
- **Nova Carter 物理多相机 W1+W2+W3(depth)+W4 Live Graph Benchmark**；
- **Metis/Hailo/M50 的 ARM Host + Accelerator 证据链与架构分析**；
- **六摄像头公开参考负载档位（EuRoC/TUM-VI/nuScenes/Nova），含可复现计算 CSV/脚本**；
- **PX4/EGO/FASTER 证据锚定的避障闭环时延预算与计算脚本**；
- **项目单路 1072×1280 NV12 观测模式的 FPS 敏感性数据，明确与 Sensor RAW/六路实际模式区分**；
- **C2 Visual Autonomy 可量化资源包络：pixel/image-plane/buffer、W3 service demand、W2/W4/W6 独立预算、Frame Age→reaction distance**；
- **六摄 Camera→Workload Routing + PER_VIEW/FUSED topology envelope：显式区分 model-call rate、input-view rate 与 image fan-out**；
- **六摄像头 Requirement → Gate Traceability：R01–R24 需求变量绑定 Gate、证据状态、阻塞项与关闭方法**；
- **Candidate Architecture Resource Map：四条候选路线的 workload placement、memory domain、data path、shared resource 与 bottleneck hypothesis**；
- **V01–V12 Validation Matrix：从 Requirement Freeze、W1/W3 到 full C2、FCU闭环、DDR/PCIe、热稳态与降级验证**；
- **闭环时延→平台阶段映射与 pipeline latency evidence 表**；
- **Isaac ROS 5.0 / Jetson Orin 固定版本时延锚点**；
- **时延 GAP 审计：记录“方法存在但数字缺失”、指标边界与下一步复现路径**；
- **现成产品/解决方案 Landscape：Dev Kit、SoM/Core、加速卡、工业/机器人整机、Host+Accelerator Box 已覆盖，含国内外代表路线**。

下一阶段：
1. 继续补平台事实表中的未确认字段，禁止跨 SKU 推测；
2. 按 evidence-gap-backlog 补六摄像头同构多 workload 并发、IQ-9075 物理多 Camera/VIO，以及 RK3588+独立 Accelerator 的端到端证据；
3. 六摄像头 Case 冻结实际 FPS/六路模式、速度/探测距离/vehicle response，并由此反推 Frame Age deadline；
4. 分别建立一体 SoC 与 Host+Accelerator Benchmark；
5. 用统一测试条件和实测逐步替换 INFER/GAP；
6. 运行 scripts/validate_evidence_tables.py 检查证据字段；
7. 分析 E2E/VLM/VLA/World Model 的增量资源需求；
8. 形成需求驱动的平台选型方法。


## 18. Phase 2：需求与架构综合

当前研究已从大规模资料搜集转入 Requirement & Architecture Synthesis。

主线：
```text
Requirement Vector
→ workload composition
→ resource budget
→ latency budget
→ architecture gates
→ candidate platform
→ validation plan
```

Phase 2 必须：
- 先冻结任务参数，再谈平台；
- 用 W1–W9 分解资源，不用总 TOPS；
- 区分 Integrated SoC/SoM、Host+Accelerator、Real-Time Controller+Companion、Edge-Cloud；
- 用 Sensor I/O、Real-Time、Memory/DDR、Compute、Concurrency、SWaP、Software 七类 Gate；
- 平台输出 Confirmed-fit / Candidate / Unverified / Constraint / Not-applicable，而不是总分/排行榜；
- 对六摄像头 Case 维护独立 Requirement Card。

Phase 2 基线：
- `research/architecture/requirements-to-architecture-selection.md`
- `research/workloads/system-resource-budget-model.md`
- `cases/six-camera-uav/phase-2-requirement-card.md`
- `data/calculations/six-camera-requirement-status.csv`


### 18.1 Workload Composition 不是新等级

Phase 2 使用以下 composition ID 复用资源模型：
- C1 Multi-Camera Analytics
- C2 Visual Autonomy
- C3 Multi-Sensor Autonomy
- C4 Foundation-Model Augmented Robotics
- C5 Cooperative Autonomy

C1–C5 **不是能力等级、自主等级、性能等级或 TOPS 档位**。

每个 composition 后续只允许建立：
- Reference profile：公开事实；
- Project Nominal：项目已冻结需求；
- Stress profile：Benchmark 压力工况。

三者不得混淆。

六摄像头 UAV 当前基础 composition = C2 Visual Autonomy；VLM 或协同时分别增量叠加 C4/C5，不把它们定义成“更高等级”。

### 18.2 Architecture Gate Matrix

平台筛查使用：
- Sensor/I/O
- Real-Time Partition
- Memory/DDR
- Compute Engine
- Concurrency/Tail Latency
- SWaP/Thermal
- Software/Productization

状态只允许：
- Confirmed-fit
- Candidate
- Unverified
- Requirement-missing
- Constraint
- Not-applicable

禁止把 Gate 状态加权成平台总分或排行榜。

六摄像头当前 Gate Matrix：
`cases/six-camera-uav/phase-2-architecture-gate-matrix.md`


## 19. Phase 3：最终报告准备

产品层代表性调研已达到停止扩张条件，正式报告编制已启动。

当前已落盘：
- `reports/drafts/secure-trusted-edge-intelligence-report-v0.3.md`（当前证据强化版）
- `reports/drafts/secure-trusted-edge-intelligence-report-v0.2.md`（可读性增强版）
- `reports/drafts/secure-trusted-edge-intelligence-report-v0.1.md`（历史初稿）
- `reports/drafts/final-report-evidence-map-v0.3.md`
- `references/final-report-reference-index-v0.3.md`

报告主线：
```text
应用场景
→ 功能栈
→ Workload
→ 系统资源
→ 计算架构
→ 产品形态
→ 安全可信
→ 六摄 Case
→ 产品研发建议
```

后续默认主线：
1. 以 evidence map 驱动正文迭代，不重新按厂商组织材料；
2. 产品章节不按厂商逐家罗列，而按产品形态和 workload 适配组织；
3. 六摄 Case 单独作为 Requirement→Workload→Resource→Architecture→Validation 方法验证；
4. 工程建议必须标明 FACT / VENDOR / INFER / GAP；
5. 若报告写作发现证据缺口，只按具体结论回补资料，不重新开启泛产品搜索；
6. v0.3 已完成正式编号 References、核心 Mermaid 架构图、产品形态对比表和六摄需求→Workload→资源→架构总表；后续 v0.4 优先做引用审计、国产 GM/T 资料补强和矢量图输出；
7. 最终报告图表必须保留原始数据与可重复生成路径；
8. 最终报告必须兼顾跨专业可读性：专业术语首次出现采用“中文名称（英文全称，缩写）”，并解释其作用与工程意义；
9. 禁止用连续名词/缩写替代技术论述。关键章节应回答“是什么、为什么重要、如何在无人装备中使用、对计算/接口/实时性/安全有什么影响”；
10. 最终报告保留独立术语与缩略语章节，但正文仍需对首次出现的核心术语进行就地解释；
11. W1–W9、C1–C5、Camera Routing、Architecture Gate 等研究分类必须先给出行业/论文/官方工程依据，再明确说明它们是本项目的研究抽象，不得暗示为行业标准；
12. 最终报告关键结论尽可能在正文就地给出可点击参考编号 [Rxx]，并维护统一参考文献索引。


## 20. 安全可信无人智算扩展

最终报告和后续平台研究新增一条横向主线：

```text
Mission + Threat Model
→ AI/RT Workload + Trust/Security Requirement
→ Compute Resource + Security Resource
→ Compute Architecture + Trust Architecture
→ Platform + Crypto/Root-of-Trust
→ Verification / Lifecycle / Fleet Policy
```

安全可信能力不是 W10，也不是新的自主等级。后续所有面向无人装备的产品/平台评价，除原有七类 Architecture Gate 外，还应按证据检查：

- SG-A Root of Trust
- SG-B Boot Integrity
- SG-C Key & Identity
- SG-D Runtime Isolation
- SG-E Remote Attestation
- SG-F AI Artifact Trust
- SG-G Communication / Access Control
- SG-H Physical Capture
- SG-I Lifecycle / Secure Update / Recovery
- SG-J Domestic Crypto

状态继续使用 Confirmed / Candidate / GAP / Constraint，不得加权成总分。

特别禁止：
- 因为 SoC 支持 TrustZone 就推断产品支持完整 TEE 方案；
- 因为有 TEE 就推断 NPU/GPU 模型处于 confidential execution；
- 因为有 TPM/SE 就推断整机已实现 remote attestation；
- 跨 SKU 继承同厂商安全能力；
- 把 Secure Boot 等同 Measured Boot / Remote Attestation；
- 把 MAVLink Signing 当成 payload encryption；
- 把 ROS2/DDS Security 当成 OS-level sandbox/MAC；
- 把“AI 模型文件已加密”写成“模型运行态已保护”。

当前基线：
- `research/architecture/secure-trusted-edge-intelligence-platform.md`
- `references/webpages/secure-edge-intelligence-evidence-2026.md`
- `data/product-specs/security-trust-capability-matrix-2026.csv`

后续报告应把“安全可信”作为无人装备产品差异化方向之一，从需求、架构、产品和六摄 Case 全链路展开，而不是只在结论中附带描述。


### 20.1 Safety 与 Security 必须分开

功能安全（Functional Safety）与网络安全/可信计算（Cybersecurity / Platform Trust）不得混为一类证据。

例如：
- ISO 26262 / ASIL / lockstep / ECC / watchdog 主要证明随机故障检测、容错和功能安全；
- Secure Boot / Root of Trust / TEE / key storage / measured boot / remote attestation 解决恶意修改、身份、秘密和平台可信状态。

禁止因为某芯片通过 ASIL-B/ASIL-D 就推断其具备 Secure Boot、TEE、Remote Attestation 或模型保护能力。

对于安全器件还必须区分：
- 普通商密 SE：密码与密钥保护；
- TEE：隔离执行；
- TPM/TCM：度量、sealed key、Quote/Attestation；
- SoC Secure Boot：启动完整性。

只有公开资料明确支持时才能合并能力。
