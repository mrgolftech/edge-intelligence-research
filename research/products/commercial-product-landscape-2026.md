# 现成端侧智能计算产品与解决方案 Landscape（2026-09）

- 日期：2026-09-30
- 状态：v0.1
- 目标：从“芯片/平台能力”进入“可采购、可集成、可产品化”的产品层调研
- 机器可读数据：`data/product-specs/commercial-product-landscape-2026.csv`
- 证据索引：`references/webpages/commercial-products-solutions-2026.md`
- 原则：不按 TOPS 排名；必须区分开发套件、量产模块、加速卡、工业整机与参考方案

## 1. 产品层为什么必须单独研究

芯片能力不能直接等于产品可用性。

真正工程选型需要继续回答：

```text
Chip / SoC
→ SoM / Core Board
→ Carrier / Dev Kit
→ Industrial / Robotics Computer
→ Complete Solution
```

同一芯片在不同产品上的 Camera、PCIe、供电、散热、尺寸、温度、软件版本和生命周期都可能不同。

因此本轮不再问“哪颗芯片 TOPS 高”，而是问：
- 是否有真实可采购产品；
- 是评估板还是量产形态；
- Sensor/Camera 如何接入；
- Host 是否完整；
- 是否需要外置 Accelerator；
- 整机功耗、尺寸、重量；
- ROS/SDK/模型生态；
- 生命周期/供货；
- 与 C1–C4 workload composition 的结构对应关系。

---

## 2. 高集成 SoM / 模块 / 开发平台

### NVIDIA Jetson Orin 系列

#### Jetson Orin Nano Super Developer Kit

当前官方：
- 67 INT8 TOPS；
- 8GB LPDDR5；
- 102 GB/s；
- 7–25W；
- JetPack / CUDA / TensorRT；
- 定位是开发套件，不是最终工业产品。

工程定位：
- 低门槛原型；
- W3、轻量 W2/W4、VLM 原型；
- Camera/I/O 产品化需要自研/第三方 carrier。

#### Jetson AGX Orin

当前官方产品线仍为成熟生产路线：
- AGX Orin 64GB module 生命周期到 2032-01；
- AGX Orin Industrial 到 2033-07；
- Isaac ROS / TensorRT / CUDA 生态最完整。

它的价值不只是 275 TOPS，而是：
- GPU + DLA + CPU + shared memory；
- 多 Camera；
- robotics software；
- 已有 Nova/Perceptor 与真实无人机案例。

#### Jetson AGX Thor

当前已进入开发套件阶段：
- 128GB；
- 40–130W；
- 面向 Physical AI / VLA / Generative Robotics。

工程判断：
- 是 C4 高端 Physical AI 的上界参考；
- 对小型 UAV 通常首先受 SWaP 限制；
- 不应与十几瓦 M.2 卡按算力直接横排。

---

## 3. Jetson 的产品化整机

### Seeed reComputer Robotics J4012

产品形态：
- Jetson Orin NX 16GB robotics computer；
- JetPack 6 预装，已支持 JetPack 7.2；
- 可选 4-in-1 GMSL2；
- 多 CAN、UART/I2C；
- 19–54V；
- 115×115×38mm；
- 约 1100g。

意义：
- 比 NVIDIA Developer Kit 更接近机器人整机集成；
- GMSL/CAN 已直接面向移动机器人/车辆。

边界：
- 1100g 对小型 UAV 明显偏重；
- 当前公开 carrier 并不是“六路直连 Camera 已确认”的本项目同构硬件。

### Seeed reComputer Rugged J4012

特点：
- Orin NX 16GB；
- 多 GbE/PoE；
- 双隔离 CAN-FD；
- 19–48V；
- M12 防水接口；
- 面向 harsh-environment robotics。

工程意义：
- 更适合 UGV/USV/工业机器人；
- 作为无人机端计算单元通常受重量/结构约束。

### Advantech MIC-733-AO

工业整机：
- Jetson AGX Orin 32/64GB；
- 最高 275 TOPS；
- 4×GbE，可选 PoE；
- 可选 2-ch GMSL；
- 9–36V；
- 192×230×87mm；
- 约 4.5kg；
- fanless。

工程意义：
- 是“芯片 → 工业产品”的典型例子；
- 适合固定边缘、UGV/工业机器人；
- 不属于小型 UAV SWaP 范围。

---

## 4. Qualcomm Dragonwing IQ-9075 产品化链

这一条产业链已经不只存在 EVK。

### IQ-9075 EVK

官方 Active：
- 50/100 dense INT8 TOPS；
- up to 36GB LPDDR5 ECC；
- up to 16 concurrent Camera；
- CPU/GPU/NPU/4-core RT subsystem；
- Ubuntu / Qualcomm Linux；
- Robotics / AMR / Drone 为官方目标场景。

用途：
- 开发验证；
- 不等于最终量产尺寸/接口。

### SECO SOM-COMe-CT6-Dragonwing-IQ9

量产 SoM：
- COM Express Type 6；
- 50/100 TOPS SKU；
- up to 36GB LPDDR5-3200 ECC；
- 页面显示 In stock。

意义：
- 证明 IQ-9075 已有标准化工业 SoM 路线，不只是 Qualcomm EVK。

### Innodisk EXMP-Q911

COM-HPC Mini：
- IQ-9075；
- up to 100 dense / 200 sparse TOPS；
- 36GB LPDDR5X；
- 128GB UFS 3.1；
- dual 2.5GbE；
- dual 4-lane MIPI CSI-2；
- -40～85°C；
- 厂商称 chipset longevity 到 2038。

意义：
- 对产品化的价值高于 EVK；
- 但“up to 16 Camera”是 SoC capability，EXMP-Q911 的实际直出接口必须按模块/载板再核。

---

## 5. RK3588 现成整机与 Host+Accelerator

### Firefly EC-A3588JQ / EC-A3588Q

现成 RK3588 工业计算机：
- up to 32GB；
- 8K codec；
- industrial enclosure；
- EC-A3588JQ 使用 industrial RK3588J，公开工作温度 -40～85°C；
- 多网络/无线/存储扩展。

用途：
- 低成本 integrated host；
- C1 多 Camera Analytics；
- C2 可作为 Host 候选，但实际 Camera lane/sync 必须按板级资料核。

### Firefly AIBOX PRO

这是本轮非常重要的产品事实。

架构：
```text
RK3588 / RK3576 Host
+
2× M.2 M-Key accelerator slots
```

官方列出的 accelerator：
- RK1828；
- Houmo LQ50；
- DeepX DX-M1。

整机：
- Linux；
- dual GbE；
- CAN-FD / RS485 / DI/DO；
- 9–36V；
- 160×111×61mm。

Firefly 页面还直接提供：
- RK3588 + 1×LQ50 组合；
- normal 8.4W；
- max 45.6W。

### 关键意义

这说明：

> **“RK3588 Host + M.2 AI Accelerator”已经不是概念架构，而是市场上存在的现成异构 Edge AI Box。**

它非常适合作为本报告 Host+Accelerator 路线的代表产品。

### 关键冲突

Firefly AIBOX PRO 页面把“LQ50”写为 48GB；
但 Houmo 当前 LQ50 M.2 官方用户指南明确：
- LQ50-24GB；
- 24GB LPDDR5/LPDDR5X。

因此：
> exact Firefly accelerator SKU / memory configuration **未确认**。

不得把 Firefly 页面 48GB 直接覆盖 Houmo 官方 24GB SKU。

---

## 6. 独立 M.2 / PCIe Accelerator

### Houmo LQ50-24GB

当前官方硬件：
- M50；
- 160 TOPS；
- 100 TFLOPS@bFP16；
- 24GB LPDDR5/LPDDR5X；
- 153.6GB/s；
- M.2 2280 Key-M；
- PCIe Gen4 x4；
- 22×80×3.3mm；
- 约 9g；
- 典型 13W。

优势：
- 高 memory capacity；
- W3 + W7 潜力明显；
- 非常适合“已有 Host 增加 AI 能力”。

限制：
- W1/W2/W4/W6 仍由 Host 负责；
- 13W 不是系统功耗；
- live Camera→PCIe→M50→Host P99 仍缺。

### Axelera Embedded 113m / Metis

官方：
- Metis；
- up to 214 TOPS；
- M.2 2280 M-Key；
- PCIe Gen3 x4；
- 2/8GB LPDDR4X；
- host 需要提供 up to 11.55W average / 23.1W peak；
- -20～70°C。

Axelera 当前平台页给 Metis：
- typical application power 3.5–9W；
- up to 16GB per chip（具体卡型需按 SKU）。

意义：
- ARM Host 已有官方验证；
- 适合 W3 高吞吐扩展。

限制：
- 113m 热设计尺寸超过裸 M.2 高度；
- 对 UAV 必须把散热器和 Host 纳入 SWaP。

### Hailo-10H M.2

官方产品：
- 40 TOPS INT4；
- M.2 2242 Key-M；
- PCIe Gen3 x4；
- 4/8GB onboard LPDDR4；
- x86 / Arm Host；
- LLM/VLM + CV。

功耗口径存在版本差异：
- 当前产品网页写 typical <2.5W；
- ET Product Brief 写 typical <3.5W。

因此数据库不把二者合并成一个“精确值”，而记录：
> vendor-page conflict: <2.5W / <3.5W, exact SKU/condition required.

### Raspberry Pi AI HAT+ 2

这是 Hailo-10H 的现成系统集成参考：
- Raspberry Pi 5；
- Hailo-10H 40 TOPS INT4；
- 8GB accelerator memory；
- 集成 Pi Camera software stack；
- 官方承诺生产至少到 2036-01。

意义：
- 证明 Hailo Host+Accelerator 能做到低成本系统级产品；
- 不是工业/军用 UAV 直接产品，但适合作为架构与软件参考。

---

## 7. 国产高集成边缘模块

### Huawei Atlas 200I A2

非常值得纳入无人装备调研。

华为官方明确定位：
> 集成于边端智能设备、机器人、无人机。

20 TOPS 版本：
- 20 TOPS INT8；
- 10 TFLOPS FP16；
- 4-core CPU；
- LPDDR4X 4/8/12GB ECC；
- ISP + video codec；
- 40×1080p30 decode；
- 20×1080p30 encode；
- PCIe / Ethernet / MIPI / SATA / USB / CAN；
- 82×60×7mm；
- typical 25W。

工程意义：
- 它不是纯 accelerator，而是较高集成边缘计算模块；
- 形态上接近“国产化 integrated companion compute”。

限制：
- 25W 对小型 UAV 仍需 SWaP 评估；
- CANN/MindSDK 软件迁移成本必须单独考虑。

### Firefly AIO/Core-1688JD4（SOPHGO BM1688）

这是六摄 Case 特别值得关注的国产产品。

官方 Firefly 产品资料：
- BM1688；
- 16 TOPS INT8；
- 4 TFLOPS FP16/BF16；
- 16×1080p30 video decode；
- 10×1080p30 encode；
- **支持 6 路 sensor 输入视频**；
- ISP 支持 HDR/3DNR/3A/去雾等；
- SOPHON SDK；
- AIO 板有 GbE/CAN/RS485/CSI 等。

工程意义：
> 在已调研产品中，它是少数公开规格直接出现“6 路 sensor input”的国产视觉计算板级方案。

但：
- “6 路 sensor”仍不能等于项目六路 1072×1280 exact synchronized mode；
- W2 VIO / W6 planning / ROS2 生态成熟度需要另外评估。

### SOPHGO SE9 16-BP1-11

官方现成 Micro Server：
- BM1688；
- 8GB；
- 16-channel HD Video Analysis。

定位：
- 多路视频边缘分析；
- 更接近 C1 / fixed edge；
- 不是小型 UAV companion compute 首选形态。

### Cambricon MLU220-M.2

当前官方产品目录仍保留：
- 8 TOPS INT8；
- M.2 2280 B+M；
- PCIe Gen3 x2；
- 8.25W；
- 被动散热；
- H.264/H.265/VP8/VP9 codec。

工程定位：
- 传统国产边缘 AI accelerator；
- W3 增量能力；
- 当前公开产品代际与算力密度已明显不同于 M50/Metis/Hailo-10H，适合作为国产 accelerator 路线历史/存量参考，而不是凭 TOPS 排名。

---

## 8. AMD / Intel：不同架构路线

### AMD Kria K26 SOM / KR260

K26：
- production SOM；
- Vision AI / Robotics；
- FPGA + Arm；
- up to 1.4 TOPS AI；
- integrated H.264/H.265；
- up to 15 Camera interface capability（模块/载板条件）；
- commercial/industrial grade；
- native ROS2 route。

KR260：
- robotics starter kit；
- deterministic industrial interfaces；
- ROS2/Kria Robotics Stack。

工程意义：
- 价值在 programmable I/O、deterministic pipeline、低延迟 sensor processing；
- 不应该因为 TOPS 小就被排除；
- 对纯高吞吐 Transformer/VLM 则不是主流路线。

### Intel Core Ultra + Robotics AI Suite

Intel 2026 的路线不是“小型专用 NPU 卡”，而是：
- CPU + GPU + NPU workload consolidation；
- ROS2；
- OpenVINO；
- real-time control；
- partner industrial systems。

意义：
- 更适合工业机器人/AMR/x86 软件生态；
- 对小型 UAV，尺寸/功耗依具体 OEM 系统；
- 本轮先作为 solution ecosystem，不与 M.2 卡直接对比。

---

## 9. 产品形态与适用问题

| 产品形态 | 代表 | 真正解决的问题 | 不能替代的部分 |
|---|---|---|---|
| Dev Kit / EVK | Orin Nano DK、IQ-9075 EVK、KR260 | 原型/验证 | 量产尺寸、可靠性、最终 I/O |
| Production SoM/Core | Jetson module、SECO IQ9、EXMP-Q911、Atlas 200I A2、Core-1688JD4 | 产品嵌入 | Carrier/整机热设计 |
| Integrated Robotics Computer | reComputer Robotics、EC-A3588JQ | 快速系统集成 | 小型 UAV SWaP 未必满足 |
| Rugged Industrial Computer | reComputer Rugged、MIC-733 | 工业可靠性/接口 | 重量体积 |
| M.2 Accelerator | LQ50、Metis、Hailo、MLU220 | 扩展 W3/W7 | Host 的 W1/W2/W4/W6 |
| Heterogeneous Edge Box | Firefly AIBOX PRO | Host+Accelerator 成品化 | exact Camera/VIO/P99 仍要验证 |
| Edge Micro Server | SOPHGO SE9 | 多视频分析 | 移动端 SWaP/硬实时 |

---

## 10. 对六摄像头 UAV 的产品化启示

### 路线 A：Integrated companion computer

值得继续保留：
- Jetson Orin NX/AGX 产品体系；
- IQ-9075 production modules；
- RK3588 industrial/core board；
- Atlas 200I A2；
- BM1688 Core/AIO。

这一类要先过：
- Camera Gate；
- sync；
- shared DDR；
- W2/W3/W4/W6 concurrency；
- SWaP。

### 路线 B：Host + Accelerator

已有现成产品证明产业链成立：
- Firefly AIBOX PRO + LQ50；
- RK3588 + Metis；
- ARM Host + Hailo。

这一类的关键不是 accelerator TOPS，而是：
```text
Host Camera/ISP
+ VIO
+ preprocess
+ PCIe
+ accelerator
+ postprocess
+ map/planner
```

### 路线 C：工业/机器人整机

Seeed/Advantech 等说明：
- GMSL、CAN、宽压、rugged 化已经成为成熟产品能力；
- 但这些整机重量往往偏 UGV/robotics，而非小型 UAV。

---

## 11. 国产化产品观察

当前国产路线已经覆盖三种形态：

1. **Integrated SoC / Core Board**
   - RK3588/RK3588J；
   - BM1688；
   - Atlas 200I A2。

2. **Independent Accelerator**
   - Houmo LQ50；
   - Cambricon MLU220 M.2。

3. **Host + Accelerator Complete Box**
   - Firefly AIBOX PRO + LQ50。

这说明国内端侧 AI 产品并不是只有“单颗芯片”，已经有核心板、M.2 卡和整机异构方案。

真正不足仍主要在：
- robotics/UAV 同构 Benchmark；
- ROS2 / VIO / SLAM / mapping 组合成熟度；
- multi-camera synchronization；
- concurrent P99；
- SWaP 的公开实测。

---

## 12. 未纳入/待确认项

### “小米算力仓”

本轮对 Xiaomi/mi.com 官方入口进行检索，没有找到名为“算力仓”的可核验端侧计算硬件产品页。

因此：
- 暂不纳入正式产品库；
- 不依据二手媒体/口述补参数；
- 后续若获得准确产品名/链接，再补证。

### 产品数量停止条件

本产品 Landscape 不追求穷尽市场 SKU。

满足以下条件即停止扩产品：
- 每种主要 architecture class 已有 2–4 个代表产品；
- 国内外路线均有代表；
- Dev Kit / Production Module / Accelerator / Complete Box 均覆盖；
- 足以支撑最终报告第 6/7 章。

当前已满足进入报告编写的基本条件。
