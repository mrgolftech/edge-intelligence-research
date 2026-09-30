# 最终调研报告 Evidence Map

- 状态：v0.2
- 日期：2026-09-30
- 对应报告：`reports/drafts/secure-trusted-edge-intelligence-report-v0.2.md`
- 目的：把最终报告中的主要结论与仓库既有事实、数据、Benchmark、工程推断和证据缺口建立一一对应关系。
- 原则：最终报告不以厂商宣传作为独立结论；所有关键工程判断应能追溯到 FACT / CASE / BENCH / PAPER / SPEC / INFER / GAP 中至少一种证据状态。

## 1. 报告主线

```text
应用场景 / Mission
→ 功能栈 / Function
→ 工作负载 / Workload
→ 系统资源 / Resource
→ 计算架构 / Architecture
→ 产品形态 / Platform
→ 安全可信 / Trust
→ 六摄像头 Case / Validation
→ 产品研发建议
```

安全可信采用横向主线：

```text
Mission + Threat Model
→ AI/RT Workload + Trust Requirement
→ Compute Resource + Security Resource
→ Compute Architecture + Trust Architecture
→ Platform + Root of Trust / Crypto
→ Verification + Lifecycle
```

---

## 2. 章节—证据资产映射

| 报告章节 | 核心问题 | 主要证据资产 | 当前状态 |
|---|---|---|---|
| 执行摘要 | 为什么不能按 TOPS 选型；为什么建议形成安全可信无人智算平台 | README.md；AGENTS.md；requirements-to-architecture-selection.md；secure-trusted-edge-intelligence-platform.md | 可写 |
| 第1章 调研背景与方法 | 如何从任务推导平台，而不是从芯片反推应用 | README.md；AGENTS.md；requirements-to-architecture-selection.md | 可写 |
| 第2章 应用与任务 | UAV/UGV/USV/AMR/机器人/固定边缘当前真实应用与功能栈 | unmanned-intelligence-scenarios.md；application-workload-matrix.md；uav.md；ugv-amr.md；usv.md；robotics-fixed-edge.md | 可写 |
| 第3章 工作负载 | W1–W9 如何覆盖感知、定位、建图、规划、Foundation Model、多机与安全监督 | workload-taxonomy.md；workload-composition-library.md；quantitative-workload-baselines.md | 可写 |
| 第4章 资源需求 | Camera/DDR/CPU/GPU/NPU/实时性如何从 workload 量化推导 | system-resource-budget-model.md；avoidance-latency-budget.md；c2-visual-autonomy-resource-envelope.md；six-camera-perception-topology-envelope.md | 可写，项目实参数仍有 GAP |
| 第5章 技术路线 | Integrated SoC / Host+Accelerator / FCU+Companion / Edge-Cloud 如何选 | requirements-to-architecture-selection.md；host-accelerator-edge-architecture.md；closed-loop-latency-platform-mapping.md | 可写 |
| 第6章 主流产品 | 当前产品形态、代表平台、软件生态、SWaP与证据边界 | commercial-product-landscape-2026.md；representative-edge-compute-platforms.md；platform-facts.csv；public-platform-benchmarks.csv | 可写 |
| 第7章 安全可信 | Threat Model、Trust Plane、Root of Trust、TEE/TPM/TCM/SE、模型可信与远程证明 | secure-trusted-edge-intelligence-platform.md；trust-plane-implementation-options.md；security-trust-capability-matrix-2026.csv；secure-edge-intelligence-evidence-2026.md | 可写 |
| 第8章 典型配置 | 场景如何映射到 composition、架构和候选产品形态 | workload-composition-resource-envelope.md；workload-platform-fit-matrix.md；unmanned-edge-solution-shortlist.md | 可写 |
| 第9章 六摄 Case | 方法如何落到真实项目；哪些参数已确认、哪些未冻结 | six-camera-uav/*；six-camera-workload-model.md；six-camera-reference-load-profiles.md；six-camera-topology-platform-evidence.csv | 可写，保留 GAP |
| 第10章 技术趋势 | BEV/Occupancy、E2E、VLM/VLA、World Model、多机、边云协同 | unmanned-intelligence-scenarios.md；foundation-models-robotics.md；vla-efficiency-2025.md；edge-robotics-2025.md；bevformer.md | 可写 |
| 第11章 产品研发建议 | 如何形成“智能计算 + 实时协同 + 密码安全 + 平台可信”差异化产品 | 全部章节综合；尤其 secure-trusted-edge-intelligence-platform.md 与 six-camera-uav/security-threat-model-and-trust-flow.md | 可写，属于工程建议 |

---

## 3. 关键结论—证据状态

### K1：不能用 TOPS 直接定义无人装备算力需求

- 状态：**FACT + INFER**
- 依据：
  - 无人系统任务同时包含 W1 Sensor/Video、W2 Localization、W3 DNN、W4 Mapping、W6 Planning、W9 Safety/Control 等异构负载；
  - NPU TOPS 无法描述 CPU、DDR、ISP/VPU、Camera I/O、同步和闭环时延。
- 主要资产：
  - `research/workloads/workload-taxonomy.md`
  - `research/architecture/requirements-to-architecture-selection.md`

### K2：无人系统应采用“任务场景 + 功能栈 + 自主性画像 + 工作负载画像”描述，而不是项目自创统一 L1–L5

- 状态：**FACT**
- 依据：NIST ALFUS、SAE J3016、IMO MASS 的适用边界与无人系统工程框架。
- 主要资产：
  - `research/scenarios/unmanned-intelligence-scenarios.md`
  - `references/standards/`

### K3：多摄像头系统必须先定义 Camera Routing 与 Perception Topology

- 状态：**INFER，受公开系统证据支持**
- 关键变量：
  - C = physical capture cameras
  - V = VIO/SLAM subset
  - P = PER_VIEW perception subset
  - F = FUSED_MULTI_VIEW subset
  - D = depth/stereo subset
  - R = recording subset
- 主要资产：
  - `research/workloads/six-camera-perception-topology-envelope.md`
  - `cases/six-camera-uav/phase-2-camera-workload-routing.md`

### K4：避障实时性必须从闭环和平台动力学反推，而不是只比较模型 FPS

- 状态：**FACT + INFER**
- 核心关系：
  ```text
  T_reaction =
  T_sample + T_sensor/ISP + T_queue + T_perception
  + T_fusion/map + T_planner + T_command + T_vehicle

  D_reaction = speed × T_reaction
  ```
- 主要资产：
  - `research/workloads/avoidance-latency-budget.md`
  - `research/architecture/closed-loop-latency-platform-mapping.md`

### K5：Host + Accelerator 已是现实产品路线，但 Accelerator 不能替代 Host 的完整系统职责

- 状态：**FACT + CASE**
- 已有现成例证：Firefly AIBOX PRO 等 Host+M.2 accelerator 产品。
- 工程边界：W1/W2/W4/W6、Camera/ISP、DDR、PCIe、预后处理与实时编排仍由 Host/系统承担。
- 主要资产：
  - `research/architecture/host-accelerator-edge-architecture.md`
  - `research/products/commercial-product-landscape-2026.md`

### K6：面向无人装备，安全可信能力应成为横向 Trust Plane，而不是“在 AI Box 上增加一颗密码芯片”

- 状态：**FACT + CASE + INFER**
- 已有行业证据：PX4、ROS 2/DDS Security、Jetson、Qualcomm、DJI、Skydio、Kria/NXP 等公开安全机制。
- 建议能力：RoT、设备身份、Secure/Measured Boot、Attestation、Secure Storage、Runtime Isolation、AI Artifact Trust、Secure Update、Physical Capture、Fleet Trust。
- 主要资产：
  - `research/architecture/secure-trusted-edge-intelligence-platform.md`
  - `research/architecture/trust-plane-implementation-options.md`

### K7：公司产品方向宜从“通用算力盒”升级为“安全可信无人智能计算平台”

- 状态：**INFER / 产品策略建议**
- 依据：
  - 通用 SoC、加速卡和工业 AI Box 市场已有大量成熟方案；
  - 公司可形成差异化的方向在于密码能力、设备身份、模型可信、通信安全、远程证明和失陷处置与无人智能计算的深度结合。
- 需要后续验证：
  - 客户需求与市场规模；
  - 国产芯片/商密器件可用性；
  - 产品 SWaP-C；
  - Trust Plane 软件栈实现成本。

---

## 4. 六摄像头 Case 的已确认与 GAP

### 已确认

- N_capture = 6；
- 单路 downstream 已观测 1072×1280 NV12；
- 需要研究/实现多 Camera 同步；
- 后续能力包括检测/跟踪、融合/深度、避障、VIO/SLAM、自主导航；
- 六摄 Case 基础 composition 为 C2 Visual Autonomy。

### 仍未冻结

- actual FPS；
- 六路是否同 mode；
- Sensor RAW format；
- N_detection；
- N_tracking；
- N_depth；
- N_vio；
- N_record；
- 飞行速度；
- usable detection range / keep-out；
- vehicle response；
- 计算功耗、尺寸、重量目标。

### 报告处理规则

这些 GAP 不用虚构数字补齐。正文采用：

- **Reference Profile**：公开数据集/论文/产品案例；
- **Project Nominal**：本项目已冻结值；
- **Stress Profile**：Benchmark 压力档；
- **GAP**：尚未冻结或缺公开证据。

---

## 5. 最终报告需要重点生成的图表

1. 无人系统功能栈图；
2. Application → Workload → Resource → Architecture → Platform 方法论图；
3. W1–W9 工作负载—计算资源映射图；
4. 四类端侧计算架构图；
5. Compute Plane + Real-Time Plane + Trust Plane 总体架构图；
6. 六摄像头 Camera Routing / Data Flow / Workload Mapping 图；
7. Workload Composition → Architecture Gate → Product Form 映射表；
8. 安全可信能力向量 S1–S12 / SG-A–SG-J 对照图；
9. 六摄项目闭环时延与 reaction distance 图；
10. 产品研发路线图。

图中涉及定量数据时必须保留原始 CSV / calculation script。

---

## 6. 当前写作优先级

### P0 — 立即形成正文
- 执行摘要；
- 第1章；
- 第2章；
- 第3章；
- 第4章；
- 第7章安全可信；
- 第11章产品建议。

### P1 — 用现有资产收束
- 第5章架构路线；
- 第6章产品 Landscape；
- 第8章典型配置；
- 第9章六摄 Case。

### P2 — 末轮补充
- 第10章趋势；
- 图表；
- References 统一格式；
- 全文术语和证据标签审校。

---

## 7. 报告写作禁区

- 不按 TOPS 排名；
- 不按厂商逐家写成产品手册；
- 不把 Dev Kit、SoM、M.2 accelerator、工业整机混为一类；
- 不把数据集频率直接当项目需求；
- 不把单模型 Benchmark 当整机性能；
- 不把 Secure Boot 等同 Measured Boot / Remote Attestation；
- 不把 TEE 等同 GPU/NPU confidential execution；
- 不把商密安全芯片等同完整 TPM/TCM；
- 不把未来 VLM/VLA 趋势写成所有无人装备当前必需能力；
- 不补齐未知参数，不跨 SKU 继承安全能力。


## 8. 报告可读性与术语规则

最终报告面向领导、系统工程师、硬件工程师、算法工程师等跨专业读者，不能写成只有领域专家才能快速理解的技术速记。

写作要求：
1. 专业术语首次出现采用“中文名称（英文全称，缩写）”形式，并用一到两句话解释其作用；
2. 不能只罗列算法/接口/器件名称，关键段落应回答“是什么、为什么重要、在无人装备中怎么使用、对系统资源有什么影响”；
3. 公式前后必须用自然语言说明物理意义和工程含义；
4. 产品章节除了规格，还应解释产品形态差异和适用边界；
5. 安全章节必须解释 Secure Boot、Measured Boot、TEE、TPM/TCM、SE、Attestation 等概念之间的差异；
6. 报告设置独立“专业术语与缩略语说明”章节，正文仍保留首次出现解释，不能只要求读者查术语表；
7. 首选中文叙述，确需保留英文术语时提供中文对照，避免连续堆叠英文缩写。
