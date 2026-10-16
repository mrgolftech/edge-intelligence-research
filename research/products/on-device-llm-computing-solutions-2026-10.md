# 国内可用端侧大模型计算方案与产品调研（2026-10）

- 研究日期：2026-10-16
- 范围：国内原厂芯片/板卡、国内整机厂商，以及在国内可获得的国际端侧 AI 计算平台。
- 主要问题：实际可部署哪些参数规模/类型的 LLM、VLM？端到端推理速度和系统功耗有何证据？怎样用于无人装备？
- 状态：公开证据版 v0.1；**不含本项目实机验证**。
- 配套结构化性能数据：`data/benchmarks/on-device-llm-public-performance-2026-10.csv`。
- 关联：`research/products/evidence-gap-backlog.md`、`research/workloads/profiles/w7-vla.md`、`cases/six-camera-uav/phase-2-validation-plan.md`。

## 一、执行摘要

1. **Xiaomi AI Cube**（2026-08）为三芯协同工程原型，不是可按量产工业模组采购的产品；发布会展示 O3+O100+D100、80 GB 统一内存、120B+3B 双模型和 150 W 持续散热释放。120B 具体模型、量化精度、tokens/s、SDK、可用性、稳定功耗 **未确认**。O3+O100 另一移动端原型的 295 tokens/s 是 *不同终端/较小 MiMo 模型* 的演示，不得套用至 AI Cube 120B。
2. **DGX Spark** 为 128 GB/273 GB/s 的 GB10 桌面计算机。NVIDIA 官宣单机最高支持 200B 参数推理，并公开了可复核测试条件的实例：GPT-OSS-120B（MXFP4、llama.cpp、ISL=2048、OSL=128、batch=1）输出 **55.37 tokens/s**；Qwen3-14B **22.71 tokens/s**，Qwen2.5-VL-7B **41.71 tokens/s**。这些模型/后端不一致，不作芯片横排。
3. **后摩 M50/LQ50** 是独立加速器路线：M50 官方称芯片最高 160 INT8 TOPS、最大 48 GB、153.6 GB/s、芯片典型 10 W；LQ50-24GB M.2 板卡的板载内存 **24 GB**、典型 **13 W**、PCIe Gen4 x4，官方称 7B/8B 模型超过 25 tokens/s。联想 **P7 整机**公布最高 80 GB 系统内存、122B 模型、最高 50 tokens/s、最大 30W 整机功耗，但 50 tokens/s 对应的模型/上下文/精度未公开，**不能**写成“122B 实测 50 tokens/s”。
4. **Jetson AGX Thor T5000** 128 GB/273 GB/s、模块功耗 40–130 W。NVIDIA 官方 JetPack 7.0+vLLM 单并发（ISL/OSL=2048/128）：Qwen3-30B-A3B **61**、Qwen3-32B **13.19**、Llama 3.3-70B **4.7**、Qwen2.5-VL-7B **45 tokens/s**，是机器人/无人平台值得重点跟踪的参考。
5. **低功耗端侧** 的公开性能不能以 70B 或 120B 宣传为导向。RK3588 官方 W8A8 Benchmark（输入128/输出64）给出 Qwen2.5-1.5B **16.69**、ChatGLM3-6B **4.98**、Qwen3-VL-2B **14.98 tokens/s**。VLM 的 **图像编码** 另有秒级阶段开销：Qwen3-VL-2B，448×448 输入，RK3588 官方报告 2.08s 图像编码；这说明文本 decode tokens/s 不能代理视觉闭环延迟。
6. **SOPHGO BM1688** 官方 LLM-TPU_Lite 提供约 7B 及以下 INT4 LLM/VLM 部署，SE7-32 官方 Llama2-7B INT4 示例 10.25 tokens/s（序列 512）；产品、SDK 和芯片版本需要逐条绑定。
7. **Qualcomm IQ-9075** 官方页标称 Llama2-7B 至多 22 tokens/s（条件未给齐），具备工业视觉与机器人接口，但没有据此认定多相机/VIO/VLM 并发可用。
8. **国产整机+非国产计算芯片**：GMKtec EVO-X2 采用 AMD Ryzen AI Max+ 395、64/128 GB 内存，官方给出本地 GPT-OSS-120B 19.25、Qwen3-235B 11 tokens/s 的厂家测试表；精度、上下文、可重现日志、端到端功耗缺失，列为 VENDOR 而非独立 BENCH。
9. 高参数**不等于更高推理速度、更好视觉实时性**。GPT-OSS-120B 总 117B，单 token 约 5.1B 活跃参数（MoE），但全模型权重仍需存储；评估需同时记录 total/active parameters、量化、KV cache、context、prefill、decode 和并发。

## 二、技术形态与实际硬件边界

| 路线 | 代表产品 | 算法/数据位置 | 优势 | 关键约束 |
|---|---|---|---|---|
| 异构多芯协同/近存计算原型 | Xiaomi AI Cube | O3 CPU/GPU/NPU + O100 近存计算 + D100 大内存/AI | 示范 120B+3B 快慢模型 | 原型，SKU、软件栈、各芯片统一内存的细节未确认；O100 1.22 TB/s 是近存带宽，不能当整机 DDR 带宽 |
| 桌面 Blackwell SoC/GPU | DGX Spark GB10 | 128 GB 统一内存、273 GB/s，CUDA/TRT-LLM/vLLM/llama.cpp | 200B 声明、丰富模型运行工具与已公布推理表 | GB10 TDP 140W、240W 电源；非无人机低 SWaP 节点 |
| 插卡加速器 + Host | 后摩 LQ50、LQ50 Duo、LM5050/LM5070、联想 P7 | 相机/OS/CPU/DDR 在 Host，M50 外挂 NPU/设备内存 | 宿主可选、可以增量 AI 加速 | 必须记录 Host CPU/DDR、PCIe H2D/D2H、模型权重放置、总功耗、驱动软件和资源争用 |
| 机器人嵌入式 GPU/SoM | Jetson Thor T5000 | 128 GB 一致共享系统内存、摄像头/视觉工具链 | VLM/LLM 与 robotics stack 一体开发 | 模组 40–130W，需与真实 W1–W6 并发而非只跑 LLM |
| CPU+iGPU 大内存 mini PC | GMKtec EVO-X2 (AMD) | 64/128 GB LPDDR5X，LM Studio/本地推理 | 方便部署 32B/70B 与 MoE 大参数模型 | 约 120W 持续 SoC 功率设计；非国产主芯片；易被厂商跨模型宣传混淆 |
| 低功耗 NPU SoC | RK3588、BM1688 | Host CPU/DDR + NPU、定制 LLM runtime | 1B–7B 小型模型、轻量 VLM | 算子/编译、图像编码、P99、VIO/视觉共用资源 |

不要混淆 M50 芯片级 10W、LQ50 M.2 板卡典型 13W、P7 整机最大 30W，也不要把 AI Cube 150W **持续性能释放设计**误作同工况实测平均功耗。

## 三、实测数据与来源属性

结构化数据见 CSV。代表性对照：

| 系统 | 模型 | Decode tokens/s | 类型/条件 | 属性 |
|---|---|---:|---|---|
| DGX Spark | GPT-OSS-120B | 55.37 | MXFP4/llama.cpp/ISL 2048/OSL 128/BS1 | NVIDIA 官方技术 Benchmark |
| DGX Spark | Qwen3-14B | 22.71 | NVFP4/TRT-LLM/同上 | NVIDIA 官方技术 Benchmark |
| DGX Spark | Qwen2.5-VL-7B | 41.71 | NVFP4/TRT-LLM/同上；文本输出而非 Camera→semantic E2E | NVIDIA 官方技术 Benchmark |
| Jetson Thor | Qwen3-30B-A3B | 61.0 | vLLM/JetPack7.0/ISL 2048/OSL128/单并发 | NVIDIA 官方 Benchmark |
| Jetson Thor | Qwen3-32B | 13.19 | 同上 | NVIDIA 官方 Benchmark |
| Jetson Thor | Llama3.3-70B | 4.7 | 同上 | NVIDIA 官方 Benchmark |
| Jetson Thor | Qwen2.5-VL-7B | 45.0 | 同上；不含多 Camera 闭环 | NVIDIA 官方 Benchmark |
| RK3588 | Qwen2.5-1.5B | 16.69 | RKLLM W8A8/ISL128/OSL64 | Rockchip 官方 Benchmark |
| RK3588 | ChatGLM3-6B | 4.98 | RKLLM W8A8/ISL128/OSL64 | Rockchip 官方 Benchmark |
| RK3588 | Qwen3-VL-2B | 14.98 | RKLLM W8A8/ISL128/OSL64 | Rockchip 官方 Benchmark |
| SE7-32 | Llama2-7B | 10.25 | INT4/seq512，官方 demo | SOPHGO 官方示例 |
| IQ-9075 | Llama2-7B | up to 22 | quant/context/并发未确认 | 高通官网宣称 |
| Houmo LQ50 M.2 | 7B/8B 未指明具体模型 | >25 | quant/context/host 未确认 | 后摩官网宣称 |
| Lenovo P7 | 未公布与速率绑定的具体模型 | up to 50 | 本地整机，最大 122B 支持与速率是两个声明 | 联想厂商宣称 |
| GMKtec EVO-X2 128 GB | GPT-OSS-120B | 19.25 | quant/context/后端未给出，厂家表 | 厂商宣称 |
| GMKtec EVO-X2 128 GB | Qwen3-235B | 11.0 | total 235B MoE；quant/context 未给出 | 厂商宣称 |

**特别注意：** NVIDIA 2025-10-24 DGX Spark 博客同时给出 *训练* tokens/s 和 *推理生成* tokens/s，两类数值不应混用。这里只记录推理生成表中的数值。

## 四、参数规模与内存下限（工程计算，非产品实测）

计算 `Weight_GB ≈ P_B × Bits/8`，按十进制 GB，尚未包含量化 scale/metadata、计算工作区、KV cache、视觉编码器、显存碎片和 OS。

| 模型总参数 | 4-bit 理想权重 | INT8 理想权重 | FP16/BF16 理想权重 |
|---|---:|---:|---:|
| 3B | 1.5 GB | 3 GB | 6 GB |
| 7B | 3.5 GB | 7 GB | 14 GB |
| 14B | 7 GB | 14 GB | 28 GB |
| 32B | 16 GB | 32 GB | 64 GB |
| 70B | 35 GB | 70 GB | 140 GB |
| 120B | 60 GB | 120 GB | 240 GB |
| 200B | 100 GB | 200 GB | 400 GB |

MoE total 参数决定模型权重存储占用，active 参数更接近每 token 计算量，两者必须并列记录。GPT-OSS-120B 官方 checkpoint 约 60.8 GiB，模型为 116.8B 总参数/5.1B 活跃参数；`60 GB` 为理想 4-bit 数量级而非其真实权重文件大小。设备有 80GB 内存不意味着 120B 模型支持 128K 全上下文与多并发：需核算 KV cache、推理框架、OS、其他任务。

## 五、从端侧大模型部署能力映射到无人装备

1. **低功耗无人机/小型机器人：**优先验证 0.5B–3B 任务辅助模型，定位于低频语义解释/交互，不代替 VIO、目标跟踪、避障、FCU。RK3588 的 Qwen3-VL 2B 图像编码 2.08 秒证据尤其说明“生成 15 tokens/s”不足以论证实时避障。
2. **高性能机器人/地面无人装备：** 7B–32B VLM/LLM 可能承担图像理解、任务分解、语义检索、复杂意图到计划的桥接；Jetson Thor、带高内存 Host 的后摩、AMD APU 等有工程研究价值。
3. **桌面/车载/边缘智能中心：**70B–200B 模型适合非强实时复杂推理、开发原型、任务级规划、视频离线摘要或边缘协同；DGX Spark、AI Cube 原型和 P7 等不能直接作为小型 UAV 机载节点。
4. **安全可信差异化产品：**围绕本地模型包完整性、设备身份、非导出密钥、可信启动、模型/配置签名、网络链路安全、更新与吊销，形成 Trust Plane；评估开启安全服务前后推理 TTFT、P99、功耗增量。不能把“本地离线”直接宣称为“数据绝对安全”。
5. **双模型策略：**小模型高频预处理/快速交互，大模型低频复杂语义决策；但 O3/O100/D100 三芯以及 3B/120B 运行分工仍需官方软件级证据，不能自创断言哪个芯片具体跑哪个模型。

## 六、建议 Benchmark / 验证记录

- 条件：真实 SKU/模组/Host、DRAM 容量与带宽、PCIe、可用 GPU/NPU 内存、整机供电、环境温度、风扇策略、SDK/runtime/driver 版本。
- 模型：名字+具体 checkpoint SHA、总参数/活跃参数、dense/MoE、量化（INT4/MXFP4/NVFP4/W8A8 等）、模型权重文件 GiB、上下文、KV cache、编译策略。
- 推理：单用户 `ISL=512/2048/8192` 和 `OSL=128/512`；TTFT P50/P95/P99、prefill tokens/s、decode tokens/s、总请求 wall-clock、内存峰值、质量退化。增测多并发下 aggregate 和 per-session 指标。
- VLM：固定图像分辨率/数量/帧源、image encoding 时间、prefill、decode、`sensor exposure/timestamp→semantic result` 的 Frame Age/P99。
- 共运行：将 W7 与 W1 多路 Camera、W2 VIO、W3 目标检测、W4 Map、W6 Planning 组合，记录抢占、DDR、P99、deadline miss；先确保 W1–W6 保持资源隔离/优先级。
- 稳态：30/60/120 分钟持续吞吐、温度、功率、电源限制、掉帧、故障恢复；外挂卡必须含 Host+PCIe H2D/D2H。
- 安全：签名模型加载与篡改拒绝、链路认证、可信启动、日志与模型保密的系统开销。

## 七、待验证 GAP

- XM-01：AI Cube 的 120B 具体模型/量化/TTFT/decode/P99；O3/O100/D100 具体内存拓扑、单芯/多芯算子调度，销售与开放 SDK 状态。
- HM-01：LQ50-24GB 的 7B/8B >25 tokens/s 具体精度、Host、上下文与热稳态；P7 的 122B 与 50 tokens/s 是否同一模型/同一测试。
- HM-02：P7 80GB 系统内存与 M50 芯片内存的具体物理布局/数据交换；其 190 TOPS 并非 M50 单芯 160 TOPS。
- NV-01：DGX Spark/Thor 在相同模型、相同量化、相同并发条件的可比数字；Thor 与 W1–W6 并发 P99。
- AMD-01：GMKtec 的 Qwen3-235B 等宣传测量条件，是否存在 CPU offload，长上下文/功耗/多并发实测。
- CN-01：国产 SoC、商密模块与 NPU 权重运行态保护/PCIe DMA/IOMMU 支持，避免误认“模型签名验证”即“运行态权重全程保密”。

## References（固定日期 2026-10-16）

- [S01] 小米集团管理层公开介绍的 AI Cube/玄戒原型机，2026-08-24，报道存证：https://www.ithome.com/0/994/002.htm；现场配置：https://www.ithome.com/0/993/546.htm 。
- [S02] NVIDIA, DGX Spark 官方规格及 200B 说明：https://www.nvidia.cn/products/workstations/dgx-spark/ 。
- [S03] NVIDIA, *How NVIDIA DGX Spark's Performance Enables Intensive AI Tasks*, 2025-10-24，表4：https://developer.nvidia.com/blog/how-nvidia-dgx-sparks-performance-enables-intensive-ai-tasks 。
- [S04] NVIDIA, Jetson AGX Thor 产品规格：https://www.nvidia.com/en-gb/autonomous-machines/embedded-systems/jetson-thor/ 。
- [S05] NVIDIA, *Jetson Benchmarks*, Thor 部分（JetPack 7.0）：https://developer.nvidia.com/embedded/jetson-benchmarks 。
- [S06] Houmo, *后摩漫界 M50 发布*, 2025-08-01：https://www.houmo.cn/1/35/NewsDetails.html 。
- [S07] Houmo, LQ50 M.2 User Guide，2026-10-16 访问：https://developer.houmoai.com/hmdoc/m50/hardware-manuals/latest/product-manuals/lq50-m.2/LQ50_M.2_guidelines/intro/index.html 。页面为 latest URL，后续需固化具体文档版本。
- [S08] 联想创投, *联想AI主机P7×后摩M50*, 2026-05-21：https://capital.lenovo.com/news/detail/id/1206/s/2.html 。
- [S09] Rockchip, *rknn-llm/benchmark.md*, 2026-10-16 访问：https://github.com/airockchip/rknn-llm/blob/main/benchmark.md 。后续需固定 Commit SHA。
- [S10] SOPHGO, *LLM-TPU_Lite*：https://github.com/sophgo/LLM-TPU_Lite 。
- [S11] SOPHGO, *sophon-demo Llama2*：https://github.com/sophgo/sophon-demo/blob/release/sample/Llama2/README.md 。
- [S12] Qualcomm, IQ-9075 产品页：https://www.qualcomm.com/internet-of-things/products/iq9-series/iq-9075 。
- [S13] GMKtec, EVO-X2 128 GB 产品/性能宣传：https://www.gmktec.com/products/amd-ryzen%E2%84%A2-ai-max-395-evo-x2-ai-mini-pc 。
- [S14] OpenAI, *Introducing gpt-oss*, 2025-08-05：https://openai.com/index/introducing-gpt-oss/ 。
- [S15] Houmo 官方 Model Zoo / llm_perf 复现入口：https://github.com/houmo-ai/postmo-modelzoo 。
- [S16] SOPHGO TPU-MLIR / LLM 编译工具：https://github.com/sophgo/tpu-mlir 。
