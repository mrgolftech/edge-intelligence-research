# 现有端侧计算产品原始文件资料库

更新日期：2026-10-08（第二批补证）。

**本目录以厂商原始规格书、数据手册、技术简报与设计指南为主，区别于研究者整理的产品参数表和二次摘要。**

- [官方产品 PDF 下载源清单](official-product-pdf-sources.csv)：字段包括厂商、产品、产品形态、文档类型、官方原始 URL、版本/标题、许可策略、报告引用和优先级。
- [PDF 下载与校验脚本](../../scripts/fetch_official_product_pdfs.py)：读取 CSV；校验 PDF magic、页数、内容、来源、计算 SHA256；拒绝 HTML 假 PDF；生成逐项状态记录。
- [GitHub Actions 自动取证任务](../../.github/workflows/collect-product-reference-pdfs.yml)：跑一次下载和校验，生成可下载的完整原件包。未获再分发授权的文件不提交到公开仓库，只保留官方原始地址、页数、大小及 SHA-256；工作流运行时校验 PDF，之后不保留受限全文。
- [持续归档目录](originals/)：仅纳入可明确原样再分发的官方 PDF，保留原文许可。

## 第二批补充状态（2026-10-08）

- 官方产品原版 PDF 地址累计 **30** 项；
- GitHub Actions 实际下载并校验原版 PDF **27** 项；
- 仅限官方原件/校验信息可查但不在本仓库存放原件：**24** 项（其中有 4 项下载成功但许可未确认，不可公开转载）；
- 已明确许可并完整保存在本公开 GitHub 的产品原版 PDF：**3** 项；
- 失败/返回非 PDF：**3** 项；
- 新增基于 CC BY 4.0 许可的 [Radxa 原始开发文档源码快照 4 份](open-docs/README.md)。
- [第二批 P014–P030 原始 PDF 来源与工程证据](second-batch-source-evidence-2026-10-08.md)。
- [全部 30 条来源的实际原件校验记录](fetch-results.csv)。

**状态含义**：`FETCHED_ORIGINAL_LINK_ONLY` 表示本轮曾下载并校验原始 PDF，但原始二进制内容并未复制到公开 GitHub 仓库；`ORIGINAL_PDF_IN_REPO` 才代表在本仓库能够打开原文；`RIGHTS_NOT_CONFIRMED_NO_REPOST` 表示已取得原始 PDF 但版权证明不足；`DOWNLOAD_FAILED` 表示校验未通过。

## 为什么与 papers/ 下原版 PDF 的策略不同？

这是**公开仓库**。厂商官网给出下载地址，不代表授予 GitHub 二次分发许可。NVIDIA、Qualcomm、Firefly、Hailo、研华等文档需要区分**公开下载**和**原文再发布**。对尚未取得再发布授权的文档，仓库保留官方下载入口、版本、校验元数据，未获再发布授权的完整 PDF **没有保存为 GitHub Actions artifact 或 Git 文件**；如需取得这些原件，应从记录的官方原始 URL 单独下载。

Raspberry Pi **Compute Module 4/5、CM5 IO Board** 已通过原始 PDF 内许可检查，按 **CC BY-ND 4.0** 原样保存；AI HAT+、Camera Module 3、AI Camera、AI Kit 的 Product Brief 虽可取得原版 PDF，但当前未在被检查页面明确检测到相同再分发许可，因此仅保留官方链接和 SHA-256，**未上传全文**。

## 阅读优先级

| 等级 | 类别 | 优先产品 | 选型时重点查什么 |
|---|---|---|---|
| P0 | GPU Robotics SoM | Jetson AGX Orin | 模块电气、内存带宽、MIPI、功耗、热设计、软件生态 |
| P0 | Robotics SoC | IQ-9075 | 传感器、实时子系统、PCIe、DDR ECC、软件、RTS |
| P0 | 国内多摄 SoC/板卡 | RK3588J、BM1688 | Camera/ISP/多路视频/实际板级路数/SoM差别 |
| P0 | AI Accelerator | Hailo-10H、后摩 LQ50 | M.2、Host、PCIe、电源峰值、DDR、本地模型支持 |
| P0 | Robotics/Industrial PC | MIC-733 | CAN/GMSL、宽压、重量、散热、可靠性 |
| P1 | Host+Accelerator 架构参照 | RPi CM5 + AI HAT+ | Host/PCIe/加速卡独立职责，以及公开载板设计 |

**注意：** RPi CM5/AI HAT+ 是低成本 Host+Accelerator 产品形态对照资料，不能直接作为六摄无人机安全关键控制平台候选。

## 尚需进一步获取的官方资料

- NVIDIA：2026-06-02 版 Jetson AGX Orin Data Sheet 1.81、Orin NX Data Sheet 1.7、Camera Module Hardware Design Guide 1.8，入口 https://developer.nvidia.com/embedded/downloads
- Qualcomm：QCS9075 Data Sheet Rev AL / IQ-9075 Module Product Brief，入口 https://docs.qualcomm.com/bundle/publicresource/topics/80-73417-1
- 后摩：LQ50 M.2 Hardware Guidelines（官方 HTML 为主，不能把其标题当成已有 PDF），入口 https://developer.houmoai.com/hmdoc/m50/hardware-manuals/latest/product-manuals/lq50-m.2/LQ50_M.2_guidelines/intro/index.html
- 华为昇腾：Atlas 200I A2 用户指南与接口/软件文档，入口 https://www.hiascend.com/zh/hardware/accelerator-module-A2
- Axelera：Metis 113m 官方硬件/软件指南，入口 https://docs.axelera.ai/docs/hardware/getting-started/start/embedded-113m/
- AMD：Kria K26 DS987 Rev 1.6，官方可浏览文档 https://docs.amd.com/r/en-US/ds987-k26-som
- Hailo：M.2 产品简报 https://hailo.ai/files/hailo-10h-m-2-et-product-brief-en/

**不以非官方转载页替代厂商源文件。** 对未找到可直接下载的 PDF，记录原始官方 HTML 文档，不伪造 PDF 全文。
