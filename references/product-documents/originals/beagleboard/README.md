# 已永久归档的开放硬件产品原版 PDF（2026-10-08）

以下 **15 份为原始 PDF 二进制文件**，已由 GitHub Actions 真实下载和写入 `main`，不是技术摘要、链接清单或重新排版的文档。

- [批量原始 PDF 来源与固定提交版本](../../open-hardware-pdf-sources.csv)
- [15 份原件的页数、尺寸、SHA-256 和提交路径](../../open-hardware-pdf-manifest.csv)
- [可复现抓取与 PDF 校验脚本](../../../../scripts/archive_open_hardware_pdfs.py)
- [成功执行的 Actions 任务](https://github.com/mrgolftech/edge-intelligence-research/actions/runs/37743646456)

## 原版文件

| ID | 产品 / SoC | PDF 原件 | 用途 |
|---|---|---|---|
| BH001 | BeagleBone AI-64 / TI TDA4VM | [Rev B1 完整硬件原理图（32页）](BH001_BeagleBone_AI-64_Rev_B1_SCH_220602.pdf) | W1/ W2 /RT /Power |
| BH002 | BeagleY-AI / TI AM67A | [完整硬件原理图](BH002_BeagleY-AI_SCH.pdf) | Sensors + Heterogeneous SoC |
| BH003 | BeagleY-AI | [I²C 总线树](BH003_BeagleY_AI_Rev_A_IIC_TREE_240426.pdf) | I/O Integration |
| BH004 | BeagleY-AI | [电源流向图](BH004_BeagleY_AI_Rev_A_POWER_FLOW_DIAGRAM_240426.pdf) | Power Tree |
| BH005 | BeagleY-AI | [器件位号参考图](BH005_BeagleY_AI_V1.0_Part_Reference_240109.pdf) | Layout |
| BH006 | BeagleY-AI | [系统框图](BH006_BeagleY-AI_Rev_A_BLOCK_DIAGRAM_240426.pdf) | Architecture |
| BH007 | BeagleY-AI | [机械尺寸图](BH007_BeagleY-AI_mechanical_drawing.pdf) | SWaP |
| BH008 | BeagleV-Fire / PolarFire | [原版原理图](BH008_BeagleV-Fire_sch.pdf) | FPGA + RISC-V |
| BH009 | BeagleV-Fire | [器件布局图](BH009_319015079_BeaglV-Fire_Rev-A_Placement.pdf) | Board Layout |
| BH010 | BeagleV-Fire | [丝印图](BH010_319015079_BeaglV-Fire_Rev-A_silkscreen.pdf) | PCB Assembly |
| BH011 | BeaglePlay / TI AM62x | [完整原理图](BH011_BeaglePlay_sch.pdf) | RT /SoC /I/O |
| BH012 | BeaglePlay | [机械尺寸图](BH012_BeaglePlay_mech.pdf) | Mechanical |
| BH013 | BeagleBone AI / AM5729 | [Rev A2 原理图](BH013_BeagleBone-AI_RevA2_sch.pdf) | Legacy Architecture |
| BH014 | BeagleBone AI | [Rev A2 PCB 图](BH014_BeagleBone-AI_RevA2_brd.pdf) | PCB |
| BH015 | BeagleV-Ahead / RISC-V | [原版原理图](BH015_BeagleV-Ahead_SCH.pdf) | RISC-V SoC |

## 权利人、许可证和出处

这些文件来自 BeagleBoard.org Foundation 和相关贡献方的**官方公开硬件仓库**。六个上游源仓库均声明 **Creative Commons Attribution 4.0（CC BY 4.0）**。各文件为原样保存，未重新渲染、翻译或删改其内容。

- [beagleboard/beaglebone-ai-64 — 固定版本源仓库](https://github.com/beagleboard/beaglebone-ai-64/tree/7313ca3cca8a7035bd077dc51d4a9b3a40e4c1a3)；[原始 LICENSE](https://github.com/beagleboard/beaglebone-ai-64/blob/7313ca3cca8a7035bd077dc51d4a9b3a40e4c1a3/LICENSE)。
- [beagleboard/beagley-ai — 固定版本源仓库](https://github.com/beagleboard/beagley-ai/tree/d1c9f8b76c17c0b629341b79bd4286dbeebb1e3e)；[原始 LICENSE](https://github.com/beagleboard/beagley-ai/blob/d1c9f8b76c17c0b629341b79bd4286dbeebb1e3e/LICENSE)。
- [beagleboard/beaglev-fire — 固定版本源仓库](https://github.com/beagleboard/beaglev-fire/tree/cdbd4b6892cebc5eab2d73c5a098b73aa0c2612c)；[原始 LICENSE](https://github.com/beagleboard/beaglev-fire/blob/cdbd4b6892cebc5eab2d73c5a098b73aa0c2612c/LICENSE)。
- [beagleboard/beagleplay — 固定版本源仓库](https://github.com/beagleboard/beagleplay/tree/7a59a98ae27dc4fd9e2bd8975ff90cdb44a366ea)；[原始 LICENSE](https://github.com/beagleboard/beagleplay/blob/7a59a98ae27dc4fd9e2bd8975ff90cdb44a366ea/LICENSE)。
- [beagleboard/beaglebone-ai — 固定版本源仓库](https://github.com/beagleboard/beaglebone-ai/tree/819b6268c33ed85f1030205eea24a68261d30681)；[原始 LICENSE](https://github.com/beagleboard/beaglebone-ai/blob/819b6268c33ed85f1030205eea24a68261d30681/LICENSE)。
- [beagleboard/beaglev-ahead — 固定版本源仓库](https://github.com/beagleboard/beaglev-ahead/tree/6b56e2d69485c375c5912eaa2791f79f1d089c07)；[原始 LICENSE](https://github.com/beagleboard/beaglev-ahead/blob/6b56e2d69485c375c5912eaa2791f79f1d089c07/LICENSE)。

原始权利人、技术版本与来源以该文件本身和上游对应版本的 `LICENSE` 为准。本项目仅开展技术引用和备份，不声称拥有上游文档的著作权。

**注意：** 这些是嵌入式/异构计算设备的硬件原理图、连接拓扑、供电与结构资料。它们为六摄、多接口和产品设计提供可分析的工程案例，但**不能直接证明六路摄像头闭环性能或可信执行能力**。同时并非 Jetson/Qualcomm/Firefly 等其他厂商受限 Datasheet 的替代品。
