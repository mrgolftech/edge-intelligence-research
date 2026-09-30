# 最终调研报告 Evidence Map v0.3

- 日期：2026-09-30
- 对应报告：`reports/drafts/secure-trusted-edge-intelligence-report-v0.3.md`
- 参考文献索引：`references/final-report-reference-index-v0.3.md`
- 状态：证据强化版

## 1. v0.3 的主要变化

1. W1–W9 不再直接作为既定分类出现，而是先列 PX4 / Nav2 / Autoware / Waymo / 论文综述等行业依据，再说明本项目如何抽象；
2. 明确 W1–W9 和 C1–C5 是本项目研究 taxonomy / composition ID，不是行业标准或自主等级；
3. 关键结论在正文中使用可点击 `[Rxx]` 引用；
4. 建立独立参考文献索引，记录来源类型、官方链接、支撑结论和仓库摘要；
5. 新增四张 Mermaid 核心图及可复用源文件；
6. 新增产品形态总表及机器可读 CSV；
7. 新增六摄像头“需求 → Workload → 资源 → Gate → 候选架构”总表及 CSV。

## 2. 关键概念与来源

| 概念/判断 | 外部依据 | 本项目处理 |
|---|---|---|
| 自主性不宜跨域统一 L1–L5 | NIST ALFUS、SAE J3016、IMO MASS | 采用任务场景 + 功能栈 + 自主性画像 + workload |
| W1 Sensor/Video | PX4 / Autoware Sensing / Isaac ROS | 抽象为数据入口与视频流水线 |
| W2 Localization | PX4 VIO / Nav2 State Estimation / Autoware Localization / UAV review | 抽象为定位、融合、VIO/SLAM 相关资源 |
| W3 DNN Perception | Autoware Perception / Waymo / MLPerf | 抽象为 NPU/GPU 张量感知 |
| W4 Map/World Model | Nav2 costmap / Autoware occupancy / BEVFormer | 抽象为持续空间状态与地图资源 |
| W5 Prediction | Waymo / BEV temporal / multi-robot | 抽象为 tracking/prediction/situation |
| W6 Planning | Nav2 / Autoware / Waymo / USV review | 抽象为搜索、优化和决策 |
| W7 Foundation Model | PaLM-E / RT-2 / OpenVLA / VLA review | 抽象为大内存、多模态和生成式 workload |
| W8 Multi-Agent | Multi-robot survey / MiR Fleet | 抽象为网络、协同、分布式状态 |
| W9 Safety/Control | PX4 / Nav2 / Autoware / MASS / MiR safety | 抽象为确定性、监督和控制接口 |
| Trust Plane | ROS/PX4 Security、RFC 9334、NIST SP800-193、Jetson security | 抽象为 RoT/身份/启动/证明/模型/OTA/失陷处置 |

## 3. 核心新增资产

### 报告
- `reports/drafts/secure-trusted-edge-intelligence-report-v0.3.md`

### 参考文献
- `references/final-report-reference-index-v0.3.md`

### 图源
- `assets/diagrams/final-report-methodology-evidence-chain-v03.mmd`
- `assets/diagrams/final-report-workload-map-v03.mmd`
- `assets/diagrams/secure-trusted-three-plane-v03.mmd`
- `assets/diagrams/six-camera-requirement-resource-architecture-v03.mmd`

### 数据表
- `data/product-specs/final-report-product-form-comparison-v03.csv`
- `data/calculations/six-camera-requirement-workload-resource-architecture-v03.csv`

## 4. 报告证据写作规则

- 先给外部来源，再提出本项目抽象；
- 本项目自定义编号必须明确标注为 research taxonomy / composition ID；
- 事实、厂商宣称、Benchmark、工程推断和 GAP 分开；
- 产品形态对比不做 TOPS 总排名；
- 图表中的数值必须能追溯到 CSV / Benchmark / Requirement Card；
- 报告中的外部资料尽量直接可点击；
- 关键判断应优先由标准、官方文档、论文或公开 Benchmark 支撑。

## 5. 仍需后续补强

- 国产可信计算/商密 GM/T 标准正式编号引用；
- 第七章代表产品规格附表的逐字段 reference ID；
- Mermaid → SVG/Draw.io 矢量图；
- 六摄实际 FPS、速度、探测距离、SWaP 冻结后更新定量结论。
