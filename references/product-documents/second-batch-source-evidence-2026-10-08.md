# 端侧算力产品原始资料增补——第二批取证记录

- 记录日期：2026-10-08
- 项目：edge-intelligence-research
- 取证方式：官方固定 PDF 下载源 → GitHub Actions 下载 → 文件头、页数、关键词 → SHA-256 → 许可审查
- 机器可读总清单：[27→30 项官方原始资料源](official-product-pdf-sources.csv)
- 实际下载审计：[fetch-results.csv](fetch-results.csv)
- **注意**：`FETCHED_ORIGINAL_LINK_ONLY` 表示已实际取得并校验过原件，**不表示**文件已永久存储在本公开仓库。

## 新增来源范围：P014–P030

| ID | 厂商 | 产品/资料类型 | 官方原始资料 |
|---|---|---|---|
| P014 | Qualcomm | IQ-9075 Module Product Brief Rev C | [原版 PDF](https://docs.qualcomm.com/doc/87-97354-1/87-97354-1_REV_C_Qualcomm_Dragonwing_IQ-9075_Module_Product_Brief.pdf) |
| P015 | Qualcomm | IQ-9075 EVK Product Brief Rev G | [原版 PDF](https://docs.qualcomm.com/doc/87-87713-1/87-87713-1_REV_G_Qualcomm_Dragonwing_IQ-9075_EVK_Product_brief.pdf) |
| P016 | Firefly | RK3576/RK3588 AIBOX 产品规格 | [原版 PDF](https://download.t-firefly.com/Spec/Computers/AIBOX-3576_AIBOX-3588_AIBOX-3588S_Specification_EN.pdf) |
| P017 | Firefly | BM1688 AIBOX 规格 | [原版 PDF](https://download.t-firefly.com/Spec/Computers/AIBOX-1688_AIBOX-186_Specification_EN.pdf) |
| P018 | Firefly | AIO-3576C 工业主板规格 | [原版 PDF](https://download.t-firefly.com/Spec/Mainboards/AIO-3576C_Specification_EN.pdf) |
| P019 | Firefly | iCore-3576Q/JQ 核心板规格与引脚 | [原版 PDF](https://download.t-firefly.com/Spec/CoreBorads/iCore-3576Q_iCore-3576JQ_Specification_EN.pdf) |
| P020 | Firefly | ROC-RK3576-PC 板卡规格 | [原版 PDF](https://download.t-firefly.com/Spec/Mainboards/ROC-RK3576-PC_Specification_EN.pdf) |
| P021 | Radxa | RK3588 ROCK 5B+ Product Brief | [原版 PDF](https://dl.radxa.com/rock5/5b%2B/docs/radxa_rock5bp_product_brief.pdf) |
| P022 | Radxa | ROCK 5B+ 实际板卡原理图 | [原版 PDF](https://dl.radxa.com/rock5/5b%2B/docs/hw/radxa_rock5bp_v1.2_schematic.pdf) |
| P023 | Radxa | AX-M1 M.2 Accelerator Product Brief | [原版 PDF](https://dl.radxa.com/aicore/ax_m1/radxa_aicore_ax_m1_product_brief_en.pdf) |
| P024 | Radxa | ROCK 5B Product Brief | [原版 PDF](https://dl.radxa.com/rock5/5b/docs/hw/radxa_rock5b_product_brief_Revision_1.2.pdf) |
| P025 | Radxa | ROCK 5B v1.450 板级原理图 | [原版 PDF](https://dl.radxa.com/rock5/5b/docs/hw/radxa_rock_5b_v1450_schematic.pdf) |
| P026 | Firefly | BM1684X AI Box 整机规格 | [原版 PDF](https://download.t-firefly.com/Spec/Computers/AIBOX-1684X_AIBOX-1684_Specification_EN.pdf) |
| P027 | Firefly | EC-R3576PC 工业计算机规格 | [原版 PDF](https://download.t-firefly.com/Spec/Computers/EC-R3576PC%20FD_Specification_EN.pdf) |
| P028 | Raspberry Pi | Camera Module 3 Product Brief | [原版 PDF](https://datasheets.raspberrypi.com/camera/camera-module-3-product-brief.pdf) |
| P029 | Raspberry Pi | IMX500 AI Camera Product Brief | [原版 PDF](https://datasheets.raspberrypi.com/camera/ai-camera-product-brief.pdf) |
| P030 | Raspberry Pi | AI Kit Product Brief | [原版 PDF](https://datasheets.raspberrypi.com/ai-kit/raspberry-pi-ai-kit-product-brief.pdf) |

这批资料的技术重点不是增加 TOPS 数字，而是补齐：

1. SoC 与 SoM、载板实际物理 I/O 的差别；
2. 核心板 Pinout/电源/Camera/ISP；
3. 多摄项目的物理 MIPI/CSI/FPC 接口；
4. M.2 加速卡的 Host/PCIe、散热与实际外形；
5. AI Box 与开发板形态下的整机功耗与外设接口；
6. Camera Module、智能传感器与 NPU 的边界。

## 额外归档：有明确 CC BY 4.0 的官方**原始源码文档**

已将 Radxa Docs 固定 Git 版本下的以下四份**原始 Markdown/MDX 源文件**保存到仓库（不是二次摘要）：

- [ROCK 5B/5B+ MIPI CSI Interface](open-docs/radxa-rock5b-mipi-csi.md)
- [共享 Camera 使用教程源码](open-docs/radxa-camera-usage.mdx)
- [ROCK 5B/5B+ Hardware Interface / Pinout](open-docs/radxa-rock5b-hardware-interface.md)
- [ROCK 5B/5B+ Product Introduction](open-docs/radxa-rock5b-introduction.md)

来源版本和许可证明：[Radxa 官方原始资料源码快照](open-docs/README.md)。

CC BY 4.0 许可入口：https://docs.radxa.com/en/license 。

## 可用于产品技术论证的两个关键事实

**事实 1：SoC/模组/开发板不可混淆。** IQ-9075 SoC 宣称最多 16 Camera，但 EVK 官方产品简报只给出 4 个 MIPI CSI 摄像头 FPC 连接器；因此不能据 SoC 最大能力断言任意 EVK 无桥接实现六摄。EVK 官方 PDF 见 P015；SoC 官方规格以现有 P002 为准。

**事实 2：同一 RK3588 SoC，在不同载板上可用摄像头接口数不同。** Radxa 官方 ROCK 5B/5B+ 文档分别给出 1 个和 2 个摄像头物理接口的板卡配置。其 Camera 接口也可能支持 lane 拆分，但并不自动代表六路图像同步输入能力。见 P021/P024 以及上面的官方原始 Hardware Interface/CSI 文档。

## 未解决项

- Hailo-10H 官方 Product Brief 页面返回 HTML 预览，原 PDF 直链尚未确认；
- Advantech MIC-733 数据手册 CDN 返回 HTTP 404；
- 后摩 LQ50、昇腾 Atlas 200I A2 官方文档部分以 HTML/SDK 门户提供，尚未取得可可靠下载并具有可复制授权的 PDF；
- NVIDIA 2026 Orin 最新 Data Sheet/Design Guide/Camera Guide 仍需按具体受控下载入口及许可另行处理；
- **未获得再分发授权的厂商原版 PDF，不上传到公开仓库**。官方文件链接、校验元数据与获取失败原因仍可在 CSV 完整审计中追溯。

最新结果以 [fetch-results.csv](fetch-results.csv) 为准；不要把该文档中的来源登记视为“已经完成永久原文归档”。
