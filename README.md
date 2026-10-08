# Edge Intelligence Research

面向无人装备、机器人与边缘智能系统的端侧计算研究仓库。

本仓库不以“收集算力卡参数”或“按 TOPS 排名”为目标，而是建立一套可复用的工程方法：

> **应用/任务场景 → 功能栈 → 自主性画像 → 数据与算法工作负载 → 计算/系统资源 → 部署架构 → 芯片/模组/产品 → Benchmark 验证**

## 研究对象

研究范围不局限于六摄像头项目，覆盖：

- UAV / UAS：巡检、测绘、搜救、监视、物流、GNSS拒止导航、协同无人机等
- UGV / 自动驾驶：道路车辆、特种无人车、园区车辆、AMR/AGV
- USV / 无人船：测绘、巡检、监视、海洋作业、自主航行与避碰
- 移动/操作机器人：仓储、工业、服务、巡检、具身智能
- 固定式边缘智能：多摄像头感知、视频分析、工业视觉、边缘推理节点
- 多无人系统：多机协同、任务分配、共享感知、边云协同

六摄像头无人平台仅作为本项目的一个工程 Case Study，用于验证方法和 Benchmark。

## 研究框架

### 1. 任务与应用场景
先回答“系统在什么环境中完成什么任务”，包括任务复杂度、环境复杂度、传感器配置、人机关系和安全约束。

### 2. 通用自主系统功能栈
参考 PX4、Nav2、Autoware 以及近年无人系统/机器人综述，采用业内常见功能划分：

**Sensing / Data Acquisition → State Estimation & Localization → Perception & World Modeling → Prediction / Tracking → Planning & Decision → Control & Execution**

在此基础上扩展 Mission/Task Management、HMI/Remote Operation、Multi-Agent/Fleet、Edge-Cloud、Safety/Security/Health Monitoring。

### 3. 自主性画像
跨无人系统不使用项目自创的 L1–L5。通用分析优先参考 NIST ALFUS 的 Mission Complexity、Environmental Complexity、Human Independence；道路车辆另参考 SAE J3016，海上自主船参考 IMO MASS。

详见：[无人系统端侧智能应用、功能栈与自主性框架](research/scenarios/unmanned-intelligence-scenarios.md)

## 算力研究原则

平台评估至少同时分析：
- CPU / GPU / NPU / DSP / MCU
- INT4 / INT8 / FP16 / BF16 / FP32
- 内存容量、带宽、Cache
- ISP、视频编解码、Camera/SerDes
- PCIe、Ethernet、CAN、USB、MIPI
- ROS2、Linux、PyTorch、ONNX、厂商 SDK、算子覆盖
- 实时性、任务并发、数据搬运
- SWaP-C
- 热稳定性、可靠性、供货与国产化
- 实际模型性能与系统级持续性能

始终区分：

> **理论峰值算力 ≠ 单模型 Benchmark ≠ 多任务系统性能 ≠ 可产品化能力**

## 当前事实底座

### 标准/框架
- [NIST ALFUS](references/standards/nist-alfus.md)
- [SAE J3016](references/standards/sae-j3016.md)
- [IMO MASS](references/standards/imo-mass.md)

### 工程架构
- [PX4 Computer Vision](references/webpages/px4-computer-vision.md)
- [PX4 Collision Prevention 时延事实](references/webpages/px4-collision-prevention-timing.md)
- [Nav2](references/webpages/nav2-navigation.md)
- [Autoware Architecture](references/webpages/autoware-architecture.md)
- [NVIDIA Isaac ROS](references/webpages/nvidia-isaac-ros.md)

### 综述/趋势
- [UAV 自主系统综述索引](references/papers/uav-autonomy-surveys.md)
- [UAV 局部规划计算时延证据](references/papers/uav-planning-latency-evidence.md)
- [UAV GNSS拒止导航综述 2025](references/papers/uav-gnss-denied-navigation-2025.md)
- [仓储与物流机器人综述 2026](references/papers/amr-logistics-2026.md)
- [多机器人导航综述 2025](references/papers/multi-robot-navigation-2025.md)
- [USV 方法与应用综述 2025](references/papers/usv-overview-2025.md)
- [Edge Robotics 综述 2025](references/papers/edge-robotics-2025.md)
- [VLA 端侧效率问题综述 2025](references/papers/vla-efficiency-2025.md)
- [Foundation Models / VLM / VLA / Edge Robotics](references/papers/foundation-models-robotics.md)
- [BEVFormer](references/papers/bevformer.md)

### Benchmark
- [EuRoC / TUM-VI](references/benchmarks/euroc-tumvi.md)
- [MLPerf Edge](references/benchmarks/mlperf-edge.md)
- [nuScenes / Waymo](references/benchmarks/nuscenes-waymo.md)
- [Nav2 MPPI](references/benchmarks/nav2-mppi.md)
- [OpenVLA / LIBERO](references/benchmarks/vla-libero.md)
- [公开平台 Benchmark 结构化基线](references/benchmarks/platform-public-benchmarks-2026.md)
- [IQ-9075 ROS2 自主栈与多流视觉证据](references/benchmarks/iq9075-multistream-robotics-2026.md)
- [RK3588 官方 DNN Benchmark 与 SLAM 论文证据](references/benchmarks/rk3588-public-evidence-2026.md)
- [IQ-9075 实时控制证据](references/benchmarks/iq9075-realtime-control-2026.md)
- [Jetson/Nova 物理多相机 Perceptor Benchmark](references/benchmarks/jetson-nova-multicamera-perceptor-2026.md)
- [ARM Host + Accelerator 公开基线](references/benchmarks/arm-host-accelerator-evidence-2026.md)
- [Isaac ROS 5.0 / Orin 时延锚点](references/benchmarks/isaac-ros-5.0-latency-anchors.md)
- [时延证据缺口审计 2026](references/benchmarks/latency-gap-audit-2026.md)
- [FUSED Multi-View / BEV 平台证据审计](references/benchmarks/fused-multiview-platform-evidence-2026.md)

### 平台与适配
- [安全可信型无人装备端侧智能计算平台](research/architecture/secure-trusted-edge-intelligence-platform.md)
- [Trust Plane 实现方案：TEE / TPM-TCM / 商密安全芯片](research/architecture/trust-plane-implementation-options.md)
- [可信密码模块/安全芯片候选事实底座](research/products/trusted-crypto-module-candidates.md)
- [国产候选平台 Security Gate 证据](references/webpages/domestic-platform-security-evidence-2026.md)
- [安全可信无人智算证据索引 2026](references/webpages/secure-edge-intelligence-evidence-2026.md)
- [Security/Trust capability matrix](data/product-specs/security-trust-capability-matrix-2026.csv)
- [Host + Accelerator 架构分析](research/architecture/host-accelerator-edge-architecture.md)
- [闭环时延 → 平台架构映射](research/architecture/closed-loop-latency-platform-mapping.md)
- [时延复现实验入口](research/architecture/latency-reproduction-methods.md)
- [需求驱动架构选型方法](research/architecture/requirements-to-architecture-selection.md)
- [系统资源预算模型](research/workloads/system-resource-budget-model.md)
- [Workload Composition Library](research/workloads/workload-composition-library.md)
- [Workload Composition 资源包络](research/workloads/workload-composition-resource-envelope.md)
- [C2 Visual Autonomy 可量化资源包络](research/workloads/c2-visual-autonomy-resource-envelope.md)
- [六摄像头 PER_VIEW vs FUSED perception envelope](research/workloads/six-camera-perception-topology-envelope.md)
- [代表性端侧计算平台事实底座](research/products/representative-edge-compute-platforms.md)
- [2026 现成端侧计算产品/解决方案 Landscape](research/products/commercial-product-landscape-2026.md)
- [无人装备现成产品架构映射](research/products/unmanned-edge-solution-shortlist.md)
- [Workload → Compute Resource → Platform 适配矩阵](research/products/workload-platform-fit-matrix.md)
- [平台—工作负载适配证据索引](references/webpages/platform-workload-evidence-2026.md)
- [机器可读适配矩阵](data/product-specs/workload-platform-evidence.csv)
- [六摄 topology→platform evidence](data/product-specs/six-camera-topology-platform-evidence.csv)
- [Commercial product/solution landscape 2026](data/product-specs/commercial-product-landscape-2026.csv)

## 应用—工作负载基线

- [无人装备端侧智能应用—工作负载需求矩阵](research/scenarios/application-workload-matrix.md)
- [UAV / UAS](research/scenarios/uav.md)
- [UGV / 自动驾驶 / AMR](research/scenarios/ugv-amr.md)
- [USV / 无人船](research/scenarios/usv.md)
- [机器人、VLA 与固定边缘智能](research/scenarios/robotics-fixed-edge.md)
- [工作负载分类 W1–W9](research/workloads/workload-taxonomy.md)
- [定量工作负载基线](research/workloads/quantitative-workload-baselines.md)
- [W1 Sensor/Video](research/workloads/profiles/w1-sensor-video.md)
- [W2 VIO/SLAM](research/workloads/profiles/w2-localization-slam.md)
- [W3 DNN Perception](research/workloads/profiles/w3-dnn-perception.md)
- [W4 3D/BEV/Mapping](research/workloads/profiles/w4-3d-bev-mapping.md)
- [W5 Prediction](research/workloads/profiles/w5-prediction.md)
- [W6 Planning](research/workloads/profiles/w6-planning.md)
- [W7 VLM/VLA](research/workloads/profiles/w7-vla.md)
- [W8 Multi-Agent](research/workloads/profiles/w8-multi-agent.md)
- [当前真实自主系统/产品证据](references/webpages/deployed-autonomous-systems.md)

### 可复用计算数据
- [Sensor payload baselines](data/calculations/sensor-payload-baselines.csv)
- [Model memory baselines](data/calculations/model-memory-baselines.csv)
- [Six-camera reference profiles](data/calculations/six-camera-reference-profiles.csv)
- [Avoidance timing fact anchors](data/calculations/avoidance-timing-fact-anchors.csv)
- [Observed 1072×1280 NV12 sensitivity](data/calculations/six-camera-observed-mode-sensitivity.csv)
- [Pipeline latency evidence](data/benchmarks/pipeline-latency-evidence.csv)
- [Latency gap audit](data/benchmarks/latency-gap-audit.csv)
- [Workload composition resource envelope](data/calculations/workload-composition-resource-envelope.csv)
- [C2 Visual Autonomy reference/sensitivity envelope](data/calculations/c2-visual-autonomy-reference-envelope.csv)
- [Six-camera Requirement → Gate traceability](data/calculations/six-camera-requirement-gate-traceability.csv)
- [Six-camera Requirement Profile v0.2](data/calculations/six-camera-requirement-profile-v02.csv)
- [Six-camera perception topology envelope](data/calculations/six-camera-perception-topology-envelope.csv)
- [Six-camera Camera→Workload routing](data/calculations/six-camera-camera-workload-routing.csv)
- [Six-camera candidate architecture resource map](data/calculations/six-camera-candidate-architecture-resource-map.csv)
- [Six-camera validation matrix](data/benchmarks/six-camera-validation-matrix.csv)

## 工程 Case
- [六摄像头无人平台](cases/six-camera-uav/README.md)
- [六摄像头工作负载模型](research/workloads/six-camera-workload-model.md)
- [六摄像头参考工作负载档位](research/workloads/six-camera-reference-load-profiles.md)
- [六摄像头避障闭环时延预算](research/workloads/avoidance-latency-budget.md)
- [六摄像头 Phase 2 Requirement Card](cases/six-camera-uav/phase-2-requirement-card.md)
- [六摄像头 Project Nominal Requirement Profile v0.2](cases/six-camera-uav/phase-2-requirement-profile-v0.2.md)
- [六摄像头 Camera → Workload Routing](cases/six-camera-uav/phase-2-camera-workload-routing.md)
- [六摄像头需求状态表](data/calculations/six-camera-requirement-status.csv)
- [六摄像头 Phase 2 Workload Composition](cases/six-camera-uav/phase-2-workload-compositions.md)
- [六摄像头 Architecture Gate Matrix](cases/six-camera-uav/phase-2-architecture-gate-matrix.md)
- [六摄像头 Requirement → Gate Traceability](cases/six-camera-uav/phase-2-requirement-to-gate-traceability.md)
- [六摄像头 Candidate Architecture Resource Map](cases/six-camera-uav/phase-2-candidate-architecture-resource-map.md)
- [六摄像头 Phase 2 Validation Plan](cases/six-camera-uav/phase-2-validation-plan.md)
- [六摄像头 Architecture Gates 数据表](data/calculations/six-camera-architecture-gates.csv)

## 当前研究判断

1. 不存在一个可直接横跨 UAV、道路车辆、USV、AMR、操作机器人的统一“L1–L5 算力等级”。
2. 感知、定位/建图、规划、控制是当前自主系统反复出现的核心功能链。
3. AI/ML 正从单点感知扩展到预测、规划、端到端策略、世界模型和 VLM/VLA，但经典/确定性模块仍大量存在。
4. 大模型进入机器人端侧已有真实产品和研究依据，但不能作为所有无人装备的默认需求。
5. 端侧与边缘/云协同将长期并存。
6. 公开 workload 已可用 EuRoC/TUM-VI、MLPerf、nuScenes/Waymo、Nav2 MPPI、OpenVLA/LIBERO 建立第一版跨平台基准。
7. 第一版证据驱动的平台适配矩阵已经建立；当前最重要的新结论是：**高集成 SoC/SoM 与 M.2/PCIe AI accelerator 必须分两类评估，后者的 TOPS 不能替代 host 的 W1/W2/W6/W9 能力。**
8. IQ-9075 已从“规格候选”进入“官方 ROS2 Reference + 可复现多流 Partner Benchmark”阶段：YOLOv10n INT8 的 1/4/9/16 路 1080p30 视频实测已公开，但这些主要是文件流，不能冒充物理多 Camera 同步测试。
9. M50 已有官方 xh2 YOLOv5s/YOLO11m 模型级 latency/accuracy/throughput 数据；LQ50 板卡 + Host 的多流视频、PCIe 和总功耗仍需单独证据。
10. Nova Carter 已有物理多相机 Live Graph Benchmark，可把 Jetson 的证据从“单节点/整机案例”推进到 W1+W2+W3(depth)+W4 组合 workload；但仍不能等同六摄像头+YOLO。
11. Metis/Hailo/M50 均已证明 ARM Host 路线真实存在；因此独立 Accelerator 评估必须把 Host CPU/VPU/DDR、PCIe、预处理和总系统功耗作为一等指标。
12. 六摄像头 W1 已建立证据锚定的参考档位：六路等效公开参考约 43–829 MP/s，说明 Camera 数量相同也可能相差近一个数量级以上；分辨率/FPS/数据路径必须先于 TOPS 冻结。
13. 避障实时性已改为参数化闭环预算：速度、有效探测距离、sensor/frame age、vehicle tracking delay、acceleration/jerk 和 keep-out distance共同决定 deadline；禁止用单模型 FPS 或 planner latency 代替端到端时延。
14. 已建立闭环时延→平台阶段映射，并开始用固定软件版本记录 graph/component latency；Isaac ROS 5.0 已成为当前 Orin 时延基线，历史 Nova 3.2 继续用于物理多相机整图证据。
15. 已建立“负证据/GAP 审计”：IQ-9075 已确认官方 benchmark 方法但尚无公开 Camera/NN 数字；Metis double buffering 明确以帧延迟换吞吐；Hailo hw-only latency 不等于 live Frame Age；M50 bandwidth_perf 内部带宽不等于 PCIe；RK3588 定义冲突的社区 E2E 数字不进入主基线。
16. 已建立五类可复用 workload composition：Multi-Camera Analytics、Visual Autonomy、Multi-Sensor Autonomy、Foundation-Model Augmented Robotics、Cooperative Autonomy；它们是 workload 组合而不是能力等级。
17. 六摄像头 Case 已归入 C2 Visual Autonomy，并建立 Nominal/Peak/Fallback 工况与第一版 Architecture Gate Matrix；当前共同最大未决项是多 workload 并发 P95/P99 / Frame Age，而不是 TOPS。
18. C2 已从“资源结构描述”推进到“可量化资源包络”：W1 用 pixel/image-plane/buffer 建模，W3 用 invocation/service demand 建模，W2/W4/W6 独立预算，并用 PX4 的 sensor+vehicle delay 事实锚点把 Frame Age 映射到闭环反应距离。
19. 已启动安全可信型无人装备端侧智能计算研究：安全能力作为横跨 W1–W9/C1–C5 的 Security/Trust Vector，不定义为新的 workload 或自主等级；平台评估增加 Root of Trust、Boot Integrity、Key/Identity、Runtime Isolation、Attestation、AI Artifact、Communication、Physical Capture、Lifecycle、Domestic Crypto 等 Security Gates。
20. 当前产品方向假设从“高算力盒子”升级为“Compute + Trust + Security”的安全可信无人智算平台；该假设必须继续通过标准、真实产品、论文与 Benchmark 验证，不能把有 TEE/Secure Boot 直接等同于模型可信执行或整机远程证明。

## 当前阶段：Phase 3 — Product Landscape Complete / Final Report Preparation

Phase 1/2 已完成场景、workload、资源、架构 Gate 与代表产品事实底座。产品层已有足够代表性覆盖，项目现在转入最终报告组织：

> **事实底稿 → 章节证据映射 → 产品/方案对照 → 六摄 Case → 工程建议 → 最终调研报告**

公开资料检索不停止，但由“主线任务”改为“阻塞项按需补证”。

当前优先：

1. 继续扩展 Requirement Vector，但以五类 workload composition 为复用模板，不按厂商/芯片组织需求；
2. 对每类 composition 建立 Reference / Project Nominal / Stress 三种 profile；
3. 用 Sensor I/O、实时隔离、Memory/DDR、Compute、Concurrency、SWaP、Software 七个 Gate 做架构筛查；
4. 六摄像头 Case 优先冻结 N_capture / N_detection / N_vio / N_depth / N_record、FPS、速度、探测距离和功耗边界；
5. 分别形成 Integrated SoC/SoM 与 Host+Accelerator 两条候选架构，不做 TOPS 排名；
6. 只有当某个 GAP 阻塞具体架构判断时，继续联网补证；
7. 后续有硬件条件时，再按统一 Benchmark 用实测替换 INFER/GAP。

研究和提交规范以 [AGENTS.md](AGENTS.md) 为准。


## 最终报告

Phase 3 已进入正式报告编制阶段：

- [面向无人装备的安全可信端侧智能计算平台技术调研报告 v0.5（当前版：技术报告体例 + 产品调研）](reports/drafts/secure-trusted-edge-intelligence-report-v0.5.md)
- [v0.4 分类依据与国产可信标准强化版](reports/drafts/secure-trusted-edge-intelligence-report-v0.4.md)
- [v0.3 证据强化版](reports/drafts/secure-trusted-edge-intelligence-report-v0.3.md)
- [v0.2 可读性增强版](reports/drafts/secure-trusted-edge-intelligence-report-v0.2.md)
- [v0.1 初稿](reports/drafts/secure-trusted-edge-intelligence-report-v0.1.md)
- [最终调研报告 Evidence Map v0.3](reports/drafts/final-report-evidence-map-v0.3.md)
- [最终调研报告参考文献索引 v0.3](references/final-report-reference-index-v0.3.md)

报告主线：

> **应用场景 → 功能栈 → Workload → 系统资源 → 计算架构 → 产品形态 → 安全可信 → 六摄 Case → 产品研发建议**

后续正文迭代优先围绕现有证据收敛，不再泛化扩充产品 SKU；发现会影响架构判断的证据缺口时再定向补证。


### v0.3 新增报告资产

- [方法论与证据链 Mermaid 图源](assets/diagrams/final-report-methodology-evidence-chain-v03.mmd)
- [W1–W9 Workload Mermaid 图源](assets/diagrams/final-report-workload-map-v03.mmd)
- [安全可信三平面 Mermaid 图源](assets/diagrams/secure-trusted-three-plane-v03.mmd)
- [六摄需求—资源—架构 Mermaid 图源](assets/diagrams/six-camera-requirement-resource-architecture-v03.mmd)
- [产品形态对比数据](data/product-specs/final-report-product-form-comparison-v03.csv)
- [六摄需求→Workload→资源→架构数据](data/calculations/six-camera-requirement-workload-resource-architecture-v03.csv)


### v0.4 新增研究依据

- [W1–W9 工作负载分类定义依据](research/workloads/workload-taxonomy-definition-basis-v1.md)
- [C1–C5 工作负载组合定义依据](research/workloads/workload-composition-definition-basis-v1.md)
- [国产可信计算与商用密码标准证据索引](references/standards/china-trusted-computing-crypto-standards-2026.md)
- [最终报告参考文献索引 v0.4](references/final-report-reference-index-v0.4.md)


### v0.5 新增报告资产

- [代表产品调研数据 v0.5](data/product-specs/final-report-representative-products-v05.csv)
- [C1–C5 组合关系图源](assets/diagrams/final-report-composition-map-v05.mmd)
- [产品 Landscape 图源](assets/diagrams/final-report-product-landscape-v05.mmd)
- [平台筛选流程图源](assets/diagrams/final-report-platform-selection-v05.mmd)
- [2026-10-08 产品公开资料复核](references/webpages/product-refresh-2026-10-08.md)
- [最终报告参考文献索引 v0.5](references/final-report-reference-index-v0.5.md)


## 参考文献原文与证据归档（2026-10-08）
- [原始资料快照、来源、许可、归档状态与高价值阅读索引](references/archive/README.md)
- [R01–R62 逐条引用及本地归档状态](references/archive/reference-inventory-2026-10-08.csv)
- [六份官方/开源源文档的固定版本清单](references/archive/source-manifest-2026-10-08.csv)


## 原始参考文献 PDF 已归档（2026-10-08）

- [9 份原始 PDF 全文](references/archive/pdfs/)
- [官方来源、页数与 SHA-256 校验清单](references/archive/pdfs/MANIFEST.csv)
- [参考资料归档目录说明](references/archive/README.md)


## 产品原始规格书与开发资料（2026-10-08）

- [30项官方产品原版 PDF 下载源及自动校验](references/product-documents/official-product-pdf-sources.csv)
- [厂商原版 PDF 第一批获取/校验审计](references/product-documents/audit-report-2026-10-08.md)
- [第二批增补的17份产品文献及原始 PDF](references/product-documents/second-batch-source-evidence-2026-10-08.md)
- [Radxa 原版 Camera/Pinout/接口文档源码快照（CC BY 4.0）](references/product-documents/open-docs/README.md)
- [可公开再分发的产品原版 PDF 文件](references/product-documents/originals/)
- [逐条校验结果：页数、SHA-256、许可状态](references/product-documents/fetch-results.csv)
- [原始产品资料采集脚本](scripts/fetch_official_product_pdfs.py)

## 产品原版 PDF 实际入库（2026-10-08）

- [新增15份可直接打开的 BeagleBoard AI/机器人计算板原始硬件 PDF](references/product-documents/originals/beagleboard/README.md)
- [产品 PDF 文件实存目录](references/product-documents/originals/)
- [15份新增 PDF 的 SHA-256、页数、上游 Git 版本](references/product-documents/open-hardware-pdf-manifest.csv)
- 现有产品原版 PDF：**18份**（15 份 BeagleBoard + 3 份 Raspberry Pi），均为实际入库原件；另有论文/安全规范原版 PDF 9 份。
- 其他厂商文档的下载和 SHA-256 校验结果记录于 [产品文档状态清单](references/product-documents/fetch-results.csv)，并不代表受限 PDF 已公开入库。
