# Radxa ROCK 5B/5B+ 官方工程文档原文快照

- 获取日期：2026-10-08。
- 原始仓库：[`radxa-docs/docs`](https://github.com/radxa-docs/docs)
- 固定版本：[`9155dd01cc4010f51d29067002735d88c013975c`](https://github.com/radxa-docs/docs/tree/9155dd01cc4010f51d29067002735d88c013975c)
- 原始许可：[Radxa Docs CC BY 4.0](https://docs.radxa.com/en/license)。
- 所有快照均保留上游原文，未修改，原始网站关联的图片和依赖没有全部单独归档；部分 Markdown 中的相对图片路径在本地不一定可显示。

| 原始资料 | GitHub 原始文档 | 仓库原文快照 | 上游 Blob SHA |
|---|---|---|---|
| ROCK5B MIPI CSI 操作指南 | [固定版本](https://github.com/radxa-docs/docs/blob/9155dd01cc4010f51d29067002735d88c013975c/i18n/en/docusaurus-plugin-content-docs/current/rock5/rock5b/getting-started/interface-usage/mipi-csi.md) | [mipi-csi.md](radxa-rock5b-mipi-csi.md) | `d557cf9337f555a388803f97d7936aed3168de3b` |
| Camera 使用共用模板 | [固定版本](https://github.com/radxa-docs/docs/blob/9155dd01cc4010f51d29067002735d88c013975c/i18n/en/docusaurus-plugin-content-docs/current/common/accessories/_camera-usage.mdx) | [camera-usage.mdx](radxa-camera-usage.mdx) | `e9a88526e3c9288f0e875fe419705e9896a5dee7` |
| ROCK5B 硬件接口和引脚 | [固定版本](https://github.com/radxa-docs/docs/blob/9155dd01cc4010f51d29067002735d88c013975c/i18n/en/docusaurus-plugin-content-docs/current/rock5/rock5b/hardware-design/hardware-interface.md) | [hardware-interface.md](radxa-rock5b-hardware-interface.md) | `7d61cc2a9310e9891266249e37970afd379e528f` |
| ROCK5B 产品介绍 | [固定版本](https://github.com/radxa-docs/docs/blob/9155dd01cc4010f51d29067002735d88c013975c/i18n/en/docusaurus-plugin-content-docs/current/rock5/rock5b/getting-started/introduction.md) | [introduction.md](radxa-rock5b-introduction.md) | `1aa29e7963f97bc27197cb94a70ae1e896d14967` |

价值：
1. **W1 传感器通路**：区分 SoC 摄像头能力与实体载板 MIPI 接口数；不把单个 4-lane 接口误写成多路物理摄像头。
2. **W1/W3 视频推理并发**：上游文档中的 GStreamer/V4L2/MPP 示例可用于后续实验设计，不能冒充实际性能数据。
3. **Host+Accelerator**：PCIe、M.2、供电、Pinout 的实际板级约束可以与 Firefly/Qualcomm 对比。

本目录文件为官方开发文档**源文件**，不是 PDF；归档理由是作者给予明确 CC BY 4.0 许可且源文件比重排的 PDF 更接近原始技术资料。
