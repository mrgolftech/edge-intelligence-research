# 端侧智能计算调研——参考资料原文归档

## 原始 PDF 正式归档（2026-10-08）

以下文件是**论文/技术报告的原始 PDF 二进制全文**，并非自写摘要。仓库自动任务已校验文件头、内容与页数，计算并保存 SHA-256。

| 引用编号 | 原始全文 | 本地 PDF |
|---|---|---|
| R01 | NIST ALFUS Volume II（73页） | [打开 PDF](pdfs/NIST_ALFUS_SP1011_II_1_0.pdf) |
| R14 | Edge Robotics Survey（27页） | [打开 PDF](pdfs/Edge_Computing_Robotics_Survey_JSAN2025.pdf) |
| R18 | PaLM-E（20页） | [打开 PDF](pdfs/PaLM-E_ICML2023.pdf) |
| R20 | OpenVLA（37页） | [打开 PDF](pdfs/OpenVLA_2024_arxiv2406.09246v3.pdf) |
| R30 | IETF RFC 9334（46页） | [打开 PDF](pdfs/IETF_RFC9334_RATS_Architecture.pdf) |
| R31 | NIST SP 800-193（45页） | [打开 PDF](pdfs/NIST_SP_800-193_Firmware_Resiliency.pdf) |

- [PDF 校验、源网址、许可与 SHA-256 清单](pdfs/MANIFEST.csv)
- [下载/校验的 GitHub Actions](../../.github/workflows/archive-licensed-reference-pdfs.yml)

**许可：** PaLM-E、OpenVLA、Edge Robotics 为 CC BY 4.0；RFC 9334 按 IETF Trust 许可完整、未经修改地转载；NIST 公开报告保留完整原文及署名。GB/T、GM/T、SAE 等标准全文以及授权不明确的厂商手册暂不复制。

当前为原版 PDF 6 份；另有官方工程文档和开源项目 README 快照 6 份、对应许可证 4 份。


**归档日期：2026-10-08；当前批次：首批 6 份许可明确的原始资料快照。**

本目录与 `references/papers/`、`references/standards/`、`references/benchmarks/`、`references/webpages/` 相互补充：原目录以本项目编写的摘要、研究笔记、证据说明和 URL 为主；本目录保存**获得明确再分发许可的上游源文档原文**。原始文档与研究者撰写的分析文件必须区分。

## 1. 现有资料统计和位置

- 报告主引用：[R01–R62 编号索引](../final-report-reference-index-v0.5.md)。
- [R01–R62 每条的来源与当前落盘状态 CSV](reference-inventory-2026-10-08.csv)。
- [原始快照固定版本与许可清单 CSV](source-manifest-2026-10-08.csv)。
- 已归档 6 份原始源文档/README，另保存 4 份上游许可证。
- **目前没有把任何受限制的标准、厂商 PDF 或论文 PDF 宣称为“已完整归档”。**

## 2. 第一批原文快照

| 引用 | 上游资料 | 本地原文快照 | 上游固定版本 | 原始许可 |
|---|---|---|---|---|
| R04 | PX4 Computer Vision | [源文件](primary/px4-computer-vision.md) | [PX4 Git Commit](https://github.com/PX4/PX4-user_guide/blob/2fa62338099f18fc3092197e856615eca94d2975/en/advanced/computer_vision.md) | CC BY 4.0 |
| R05 | PX4 Visual Inertial Odometry | [源文件](primary/px4-visual-inertial-odometry.md) | [PX4 Git Commit](https://github.com/PX4/PX4-user_guide/blob/2fa62338099f18fc3092197e856615eca94d2975/en/computer_vision/visual_inertial_odometry.md) | CC BY 4.0 |
| R06 | PX4 Collision Prevention | [源文件](primary/px4-collision-prevention.md) | [PX4 Git Commit](https://github.com/PX4/PX4-user_guide/blob/2fa62338099f18fc3092197e856615eca94d2975/en/computer_vision/collision_prevention.md) | CC BY 4.0 |
| R28 | ROS 2 Security | [源文件](primary/ros2-security.rst) | [ROS 2 Git Commit](https://github.com/ros2/ros2_documentation/blob/a2f0aa76f61144a4ac3bcda0401e9d4e9a840f22/source/Developer-Tools/Introspection-and-analysis/Security/About-Security.rst) | CC BY 4.0 |
| R17 | BEVFormer 官方实现 README | [源文件](primary/bevformer-implementation.md) | [BEVFormer Git Commit](https://github.com/fundamentalvision/BEVFormer/blob/66b65f3a1f58caf0507cb2a971b9c0e7f842376c/README.md) | Apache-2.0 |
| R20 | OpenVLA 官方实现 README | [源文件](primary/openvla-implementation.md) | [OpenVLA Git Commit](https://github.com/openvla/openvla/blob/c8f03f48af692657d3060c19588038c7220e9af9/README.md) | MIT |

> 注意：R17 和 R20 保存的是**论文作者发布的实现仓库 README**，不等于已经保存 BEVFormer 或 OpenVLA **论文全文**；技术报告引用论文中的具体实验结果仍应查看论文原文。

### 许可证文本

- [PX4 CC BY 4.0](licenses/px4-CC-BY-4.0.txt)
- [ROS 2 CC BY 4.0](licenses/ros2-CC-BY-4.0.txt)
- [BEVFormer Apache-2.0](licenses/bevformer-Apache-2.0.txt)
- [OpenVLA MIT](licenses/openvla-MIT.txt)

快照内容保持上游原样，未在正文增加本项目水印或注释。上表提供出处、署名来源和许可证；如复制到其他产品或衍生文档，须继续履行相应许可条款。

## 3. 高价值资料优先级

### A — 无人系统功能与工作负载基础

- **R01 NIST ALFUS**：跨无人系统自主性维度；主要支撑任务/环境/人机参与分析。
- **R04–R06 PX4**：视觉、VIO、避障闭环，是 W1/W2/W9 和 C2 的直接工程依据（本批已归档官方文本）。
- **R07 Nav2**、**R08/R09 Autoware**、**R10 Waymo**：定位、地图、感知、预测、规划、控制，支撑 W1–W9 的功能事实底座。
- **R11 UAV GNSS 拒止综述**、**R12 多机器人综述**、**R13 USV 综述**：支撑 UAV/USV/协同应用任务实际存在。

### B — 算法与未来负载

- **R17 BEVFormer (ECCV 2022)**：多摄像头时空 BEV，是 W4/W5 与多摄融合的关键论文（本批仅归档实现 README）。
- **R18 PaLM-E (ICML 2023)**、**R19 RT-2**、**R20 OpenVLA**、**R21 VLA 效率综述**：支撑 W7、C4 的场景和资源特征。
- **R14 Edge Robotics Survey (2025)**：端云协同、计算卸载、网络时延和边缘机器人系统方法。期刊页面确认 **CC BY 4.0**；论文 PDF 尚未归档。

### C — Benchmark/实验依据

- **R23/R24 Isaac ROS 性能/多相机图**：公开机器人系统 Benchmark，必须保留软件版本；
- **R25 MLPerf、R26 EuRoC、R27 TUM-VI**：模型推理与 VIO 数据集基础；
- 报告中的资料推导值和实际 Benchmark 不得混为一谈。

### D — 安全可信与国产化标准

- **R28 ROS 2 Security**、**R29 PX4 Security**、**R30 RFC 9334**、**R31 NIST SP 800-193**：可信证明、固件韧性及通信安全；
- **R48–R62**：GB/T 38638、GB/T 29829、GM/T 0011、GM/T 0012、GM/T 0028、SM2/3/4 等国产可信/商密标准（留存官方索引和版本，不擅自转载标准全文）。

### E — 代表产品官方资料

- **R35–R46**：NVIDIA、Qualcomm、Firefly、后摩、Axelera、Hailo、华为、SOPHGO、Seeed、Advantech、AMD、Intel 等产品/生态；
- 以固定型号和官方 Datasheet/Manual 为准，不同 SKU 与板卡不能混用，也不能将厂商宣传结果冒充第三方性能实测。

## 4. 全文 PDF 归档范围与限制

1. 可以归档：权利人以 CC BY、Apache-2.0、MIT 等明确允许再分发的文献/文档，保留完整署名、原始 URL、版本、许可和获取日期。
2. 审慎处理：论文虽然提供免费 PDF，但未确认再分发授权时，不自动提交全文。
3. 不擅自归档：GB/T、GM/T、SAE 等可能受版权/获取限制的标准全文、带访问控制的厂商资料、未授权扫描件。
4. 目前已经确认 [PaLM-E 论文](https://proceedings.mlr.press/v202/driess23a.html) 与 [Edge Computing and Its Application in Robotics](https://www.mdpi.com/2224-2708/14/4/65) 存在 **CC BY 4.0** 公开授权，但本轮二进制 PDF 下载通路失败，尚未上传其 PDF；后续可通过可复现下载脚本或受许可的正规获取渠道补齐。
5. 本次没有归档模型权重、数据集、上游 README 中嵌入的第三方图片和视频。

## 5. 归档要求

后续新增文件应记录：

```text
引用编号 | 标题 | 作者/机构 | 发布/版本日期 | 官方入口
许可 | 获取日期 | 固定版本/校验哈希 | 本地路径
关联 W/C 分类/报告结论 | 事实/厂商宣称/推断/待验证
```

如下载文件，补充 SHA256/文件大小及可验证性；如只能保存来源入口，状态标记 `INDEX_OR_SUMMARY_ONLY`，不得宣称全文已保存。
