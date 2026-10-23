# v0.6 章节证据地图与未关闭问题

- 日期：2026-10-23
- 对应版本：[报告 v0.6](secure-trusted-edge-intelligence-report-v0.6.md)
- 状态：正式报告初稿；公开证据，非工程实测

## 主要论证链

| 报告环节 | 重要已知依据 | 结论级别 | 仍待关闭的关键缺口 |
|---|---|---|---|
| 第1～2章 端边云与 UAV/UGV应用 | PX4 Companion/Collision Prevention [P01/P07]、ModalAI VOXL 2 [P02/P03]、Autoware [P08]、Waymo [P09]、Skydio [P04] | FACT/VENDOR + INFER | 同机型同传感器配置的端边分工、业务场景级需求 |
| 第3～5章 W1–W9/C1–C5/资源 | 仓库 workload taxonomy、composition、六摄 mode sensitivity、延迟模型 | FACT/METHOD/INFER | 实际六摄 FPS、视场/同步、算法模型与尾延迟 |
| 第6～7章 产品路线 | VOXL 2、Skynode X [P12]、DJI Manifold 3 [P05]、Firefly/RK3588/独立卡等 | SPEC/VENDOR | 板卡接口并发、热稳态、SDK/加速卡联调 |
| 第8章 安全可信 | `references/standards/china-trusted-computing-crypto-standards-2026.md`，既有 Trust Plane 系统研究 | FACT/INFER | 标准适用性、平台安全根/SDK与整机认证 |
| 第9.7章 吊舱 ATR | DJI Payload SDK [P06]；独立 RK3588 ATR 单元为当前用户系统设计背景 | CASE-HYPOTHESIS | 模型精度、样本集、云台/EOIR 数据流、是否在伴飞板重复推理 |
| 第9.8章 双目避障 | OpenCV 立体几何 [P11]、ModalAI [P03]、PX4 [P07] | FACT + INFER | 相机配对/基线/同步、远距精度、闭环 deadline 与故障降级 |
| 第9.9章 LLM/任务与机群 | PX4 [P01]、Nav2 BT [P10]、Rockchip RKLLM [P13]、既有端侧 LLM 专项 | FACT/BENCH + INFER | 真实开放语义任务增益，VLM 额外能耗/对避障 P99 的影响 |
| 第10～12章 验证与产品建议 | `cases/six-camera-uav/phase-2-validation-plan.md` 与已有安全可信研究 | INFER/PLAN | 统一工况复现实测、受控外部算法引入、用户/市场验证 |

## 必须严格区分的四组概念

1. **端侧 / 边侧**：相对无人机本体的位置，不等于“微型/大型算力芯片”。
2. **ATR / 双目深度 / VIO**：识别对象、计算几何、计算运动状态，不能彼此代用。
3. **失联自主 / LLM**：前者是系统可靠性需求，后者只是可能采用的一类算法。
4. **芯片 TOPS / 单模型 Benchmark / 多任务 P99**：三个不同证据层级，不能互相替代。

## 项目侧待冻结输入（不以推测填补）

- 是否保留独立吊舱 ATR RK3588：当前为历史讨论中已有分工，需要项目立项版本确认。
- 六路具体 Camera Routing：C/V/P/F/D/R，每路分辨率、FPS、同步偏差和是否有有效双目基线。
- 双目有效最大探测距离、速度包络、机体响应及 FCU 控制权限。
- 安装 SWaP、供电轨/峰值/散热/M.2 插槽与 PCIe lane 竞争。
- 多机任务定义、网络条件与可用边侧指控系统。
- LLM/VLM 的增量任务指标与可回退性；必要时设无模型对照组。

## 固定来源与追溯

新增外部一手来源编号 [P01]–[P13] 在报告附录 B.1 给出完整链接；旧版产品/标准来源 [Rxx] 仍按 `references/final-report-reference-index-v0.5.md` 管理。所有更迭时必须核验来源时间和 SKU，不继承旧版样机的未经证实性能。
