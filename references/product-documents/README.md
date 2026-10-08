# 现有端侧计算产品原始文件资料库

更新日期：2026-10-08。

**本目录以厂商原始规格书、数据手册、技术简报与设计指南为主，区别于研究者整理的产品参数表和二次摘要。**

- [官方产品 PDF 下载源清单](official-product-pdf-sources.csv)：字段包括厂商、产品、产品形态、文档类型、官方原始 URL、版本/标题、许可策略、报告引用和优先级。
- [PDF 下载与校验脚本](../../scripts/fetch_official_product_pdfs.py)：读取 CSV；校验 PDF magic、页数、内容、来源、计算 SHA256；拒绝 HTML 假 PDF；生成逐项状态记录。
- [GitHub Actions 自动取证任务](../../.github/workflows/collect-product-reference-pdfs.yml)：跑一次下载和校验，生成可下载的完整原件包。部分文件因版权不直接提交到公开仓库。
- [持续归档目录](originals/)：仅纳入可明确原样再分发的官方 PDF，保留原文许可。

## 为什么与 papers/ 下原版 PDF 的策略不同？

这是**公开仓库**。厂商官网给出下载地址，不代表授予 GitHub 二次分发许可。NVIDIA、Qualcomm、Firefly、Hailo、研华等文档需要区分**公开下载**和**原文再发布**。对尚未取得再发布授权的文档，仓库保留官方下载入口、版本、校验元数据，下载的完整 PDF 作为 GitHub Actions 工作产物供研究使用（不作为永久公开源码分发）。

Raspberry Pi Compute Module/AI HAT+ 官方 PDF 明确标明 **CC BY-ND 4.0**；只在确认实际 PDF 中的许可并保持**原样无修改**后才纳入 `originals/`，不得抽取页面重新包装、删掉署名或修改版面。

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
