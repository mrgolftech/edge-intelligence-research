# 最终调研报告 Evidence Map v0.5

- 对应报告：`reports/drafts/secure-trusted-edge-intelligence-report-v0.5.md`
- 日期：2026-10-08
- 参考文献：`references/final-report-reference-index-v0.5.md`

## 1. v0.5 结构调整

v0.5 从“研究说明/技术笔记式”行文调整为正式技术报告体例：

```text
摘要
→ 调研概述
→ 应用与功能需求
→ W1–W9 工作负载
→ C1–C5 组合
→ 资源需求
→ 技术路线
→ 现有产品调研
→ 安全可信架构
→ 六摄 Case
→ Benchmark
→ 趋势
→ 产品研发建议
→ 结论
```

## 2. 新增产品调研主章节

代表产品：
- NVIDIA Jetson AGX Orin
- Qualcomm Dragonwing IQ-9075
- Rockchip RK3588
- Huawei Atlas 200I A2
- SOPHGO BM1688 / Firefly AIO
- Houmo LQ50
- Axelera Metis
- Hailo-10H
- Firefly AIBOX PRO
- Seeed reComputer Robotics/Industrial
- Advantech MIC-733-AO
- Horizon Journey 6
- Black Sesame A2000

产品按形态而非 TOPS 排名：
- Integrated SoC/SoM
- GPU Robotics
- Independent Accelerator
- Host+Accelerator
- Industrial/Robotics Computer
- Automotive/Physical AI

机器可读数据：
- `data/product-specs/final-report-representative-products-v05.csv`

时效复核：
- `references/webpages/product-refresh-2026-10-08.md`

## 3. 图表资产

v0.5 正文包含至少 8 类图/表：
- 方法论图；
- 通用功能链；
- W1–W9 图；
- C1–C5 图；
- 产品 Landscape 图；
- 三平面 Trust 架构；
- 六摄需求→架构图；
- Architecture Gate 流程图；
- 多张工作负载、产品和六摄对比表。

## 4. 写作规则

- 技术报告采用连续技术论述，不采用问答/讲义式标题；
- 概念提出前给出处和定义边界；
- 关键结论使用可点击 [Rxx]；
- 产品章节必须写“参数 + 形态 + 适用场景 + GAP + 工程判断”；
- 图表必须服务于技术理解，而不是装饰。
