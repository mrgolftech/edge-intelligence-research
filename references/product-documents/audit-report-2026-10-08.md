# 2026-10-08 厂商产品原始资料获取与归档审计

> 研究对象：端侧 SoC / GPU SoM / M.2 AI Accelerator / Robotics Computer / Host+Accelerator。
>
> 此文档是 **原版 PDF 下载有效性审计**，不是用摘要替换原始资料。保存实际经过下载、解析和 SHA-256 检查后的文件记录；详细数据见 [fetch-results.csv](fetch-results.csv)。

## 一、实测结果

- 官方 PDF 来源条目：13。
- GitHub Actions 实际取得、经 PDF 校验的原始文档：11。
- 已永久保存在本公开仓库的厂商产品原始 PDF：3（原文许可确认且不做任何改动）。
- 其余8份：已下载和校验，其中7份需进一步确认再发布许可、1份虽属于 Raspberry Pi 产品简报但原件未检出可核实的许可声明，故均仅保留官方原始链接、页数、文件大小和 SHA-256，不向公开 Git 仓库复制。
- 官方下载失败/下载入口返回 HTML：2（研华 MIC-733 与 Hailo-10H），已保留官方下载入口便于人工获取。

## 二、仓库已保存的真正产品原版 PDF

| 产品 | 原版 PDF | 主要参考用途 |
|---|---|---|
| Raspberry Pi Compute Module 5 | [CM5 Datasheet](originals/P008_cm5-datasheet.pdf) | Host SoM、Camera/PCIe/DDR、模块级接口 |
| Raspberry Pi Compute Module 5 IO Board | [CM5 IO Board Datasheet](originals/P009_cm5io-datasheet.pdf) | SoM + 载板接口、M.2 PCIe 和 Camera 原始设计 |
| Raspberry Pi Compute Module 4 | [CM4 Datasheet](originals/P011_cm4-datasheet.pdf) | SoM 跨代比较、嵌入式模块规格 |

以上资料采用文件标示的 CC BY-ND 4.0 许可，原样存档、保留版权页和厂商名称。**这是 Host + Accelerator 架构产品形态参考，不代表可直接用于本项目六摄或安全关键飞控。**

## 三、已实际获取并校验的厂商原版 PDF（保留原始官方入口）

| 产品 | 官方原始 PDF/产品技术文档 | 对本项目价值 |
|---|---|---|
| NVIDIA Jetson AGX Orin | [Technical Brief v1.2（21页）](https://www.nvidia.com/content/dam/en-zz/Solutions/gtcf21/jetson-orin/nvidia-jetson-agx-orin-technical-brief.pdf) | SoM CPU/GPU/DDR 与机器人工作负载 |
| Qualcomm IQ-9075 | [IQ9 Series Platform Product Brief（2页）](https://docs.qualcomm.com/doc/87-83840-1/87-83840-1_REV_E_Qualcomm_Dragonwing_IQ9_Series_Platform_Product_Brief.pdf) | 50/100 TOPS、多摄与独立实时子系统 |
| Firefly BM1688 AIO | [AIO-1688JD4 Specification（25页）](https://download.t-firefly.com/Spec/Mainboards/AIO-1688JD4_Specification_EN.pdf) | 六路 Camera 接入与板卡接口 |
| Firefly BM1688 Core | [Core-1688JD4 Specification（23页）](https://download.t-firefly.com/Spec/CoreBorads/Core-1688JD4_Specification_EN.pdf) | SoM Pinout、ISP、内存、视频、供电 |
| Firefly RK3588J | [ROC-RK3588J-RT Specification（14页）](https://download.t-firefly.com/Spec/Mainboards/ROC-RK3588-RT_ROC-RK3588J-RT_Specification_EN.pdf) | 既有嵌入式平台对照 |
| Axelera Metis Embedded 113m | [Datasheet Issue 2（15页）](https://docs.axelera.ai/assets/files/axelera-ai-metis-m.2-max-ai-accelerator-card-datasheet-34f232e6c6512e54f0ac2341818724ea.pdf) | M.2 外形、电源峰值、PCIe、尺寸、产品 SKU |
| Axelera Embedded 113m | [Thermal Design Guide（23页）](https://docs.axelera.ai/assets/files/axelera-metis-m.2-max-ai-accelerator-card-thermal-design-guidelines-4b54f28be524f982a63fec069454b66d.pdf) | 主动散热、空间占用、热设计 |
| Raspberry Pi AI HAT+ | [Product Brief（6页）](https://datasheets.raspberrypi.com/ai-hat-plus/raspberry-pi-ai-hat-plus-product-brief.pdf) | Hailo Host+Accelerator 成品化案例；原文转载许可需单独核实 |

## 四、已确认存在官方原件，但自动抓取失败

- [Advantech MIC-733-AO 最新 Datasheet（2026-04）](https://www.advantech.com/en-us/products/965e4edb-fb98-429e-89ed-9a0a8435a7be/mic-733/mod_09861425-4950-46ab-ad39-1b5522881218)：网页的 Datasheet 下载按钮可在浏览器访问到 2026-04-21 版本，但 GitHub Actions 对该 CDN 链接收到 HTTP 404；可能存在防盗链/动态跳转，不能标记“已归档原文”。
- [Hailo-10H M.2 Extended Temperature Product Brief](https://hailo.ai/files/hailo-10h-m-2-et-product-brief-en/)：网页阅读器能展示 PDF（2页），但 Python 请求返回 HTML 包装页；不能把 HTML 当成 PDF。

## 五、需要持续纳入的产品原始技术文档

这些产品已有官方原始文档，但缺少稳定的公开 PDF 下载源，**不能因为网站主要提供 HTML 就写成“没有手册”**。

| 厂商/产品 | 官方原始文档入口 | 应优先获取的内容 |
|---|---|---|
| NVIDIA Jetson Orin 系列 | [Jetson Download Center](https://developer.nvidia.com/embedded/downloads) | Data Sheet 1.81、设计指南 1.81、Camera Hardware Guide 1.8 |
| Qualcomm QCS9075 | [QCS9075 Data Sheet Rev AL](https://docs.qualcomm.com/bundle/publicresource/topics/80-73417-1) | 引脚、电气、ISP、MCU/RTSS、供电 |
| 后摩 LQ50 | [LQ50 M.2 用户指南](https://developer.houmoai.com/hmdoc/m50/hardware-manuals/latest/product-manuals/lq50-m.2/LQ50_M.2_guidelines/intro/index.html) | M.2 Pinout、PCIe、功耗、DDR、散热、软件 |
| 华为 Atlas 200I A2 | [Atlas 产品与技术资料](https://www.hiascend.com/zh/hardware/accelerator-module-A2) | SoC/Module、ISP、PCIe、功耗及 SDK |
| AMD Kria K26 | [DS987 Rev 1.6](https://docs.amd.com/r/en-US/ds987-k26-som) | PS/PL、引脚、Camera I/O、实时/FPGA |
| Intel Robotics AI Suite | [官方开发文档](https://developer.robotics.intel.com/development-stack/ai-suite-robotics/index.html) | ROS2、CPU/GPU/NPU、软件/工具链 |
| Firefly AIBOX PRO | [AIBOX PRO 产品资料](https://www.t-firefly.com/products/aibox-pro-edge-computing-computer) | Host+M.2 系统功耗、I/O、散热 |
| Seeed reComputer Robotics | [官方 Getting Started](https://wiki.seeedstudio.com/recomputer_robotics_j401_getting_started/) | GMSL、CAN、结构、载板与 BSP |
| 黑芝麻 A2000 | [产品公开资料](https://www.blacksesame.com/zh/list_11/958.html) | 具体 SKU/SoC/PPA/软件接口 |
| 地平线 Journey 6 | [地平线官网](https://www.horizon.auto/) | Journey 6 模组/开发方案与实测数据 |

## 六、文献归档规则

- **原始 PDF 不是报告摘要**。每条校验记录提供官方 URL、PDF 页数、SHA-256、文件大小、权限和具体归档路径。
- 由于本仓库是公开仓库，不把受限厂商原件随意复制到 Git 历史。用户可从清单直接访问原始 PDF。
- 发布许可明确的 PDF 可以原样提交；新技术文档应优先使用官方版本化 URL。
- 重新测试命令：`python -m pip install pypdf && python scripts/fetch_official_product_pdfs.py`。
- 审计结果由 GitHub Actions 自动更新，并非从厂商宣传内容主观填表。

## 七、后续最有价值的补强方向

优先应覆盖官方完整 Datasheet 和硬件设计/散热指南，而非只收集 1～2 页的 Product Brief，尤其是 **六摄输入、VIO/SLAM Host 计算、M.2 卡峰值供电、持续功耗和可信启动**等硬件工程问题。
