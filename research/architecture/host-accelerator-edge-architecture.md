# 低功耗 ARM Host + AI Accelerator：公开证据与工程边界

- 日期：2026-09-30
- 状态：v0.2
- 目的：回答独立 M.2/PCIe AI accelerator 在无人装备中“Host 到底承担什么”，并记录 Metis、Hailo、M50 的公开 ARM Host 路径。

## 1. 核心架构

典型数据链：

Sensor / Camera
→ Host CSI/USB/SerDes
→ ISP / VPU / Decode
→ Host memory / DMA
→ Resize / Color Convert / Pre-process
→ PCIe / shared transport
→ AI Accelerator
→ Inference result
→ Host Post-process / Tracking / Fusion
→ VIO/SLAM / Mapping / Planning
→ Control / MCU

因此独立 AI Accelerator 的 TOPS 只覆盖其中一部分。

## 2. Host 的一等资源职责

对无人装备，Host 通常仍需要承担：
- W1：Camera、ISP/VPU、codec、timestamp、sync、DMA；
- W2：VIO/SLAM / state estimation；
- W5/W6：tracking、fusion、planning / optimization；
- W9 的上层 supervision / communication（硬实时控制通常仍需 MCU/RT CPU）；
- OS、ROS2、网络、存储和设备管理。

Accelerator 更适合承担：
- W3：DNN perception；
- W7：LLM/VLM/VLA 中适合其 runtime 的神经网络部分。

这解释了为什么“160 TOPS / 214 TOPS 加速卡”不能替代完整主控。

## 3. Axelera Metis：ARM Host 已从推断变成官方验证事实

Axelera 官方 ARM Host 页面列出已验证平台：

Edge 130p：
- Firefly ITX-3588J — RK3588；
- Advantech AOM-5521 — NXP i.MX95；
- Renesas RZ/V2H EVK。

Embedded 110m：
- Orange Pi 5 Plus — RK3588；
- Raspberry Pi 5 — BCM2712；
- NanoPC-T6 — RK3588；
- Jetson Orin Nano/NX。

来源：
https://axelera.ai/systems/arm-host

Voyager SDK v1.8 Release Notes 进一步确认：
- runtime 支持 Arm64 host；
- Linux kernel 支持 5.4–6.17；
- 支持 Yocto embedded targets；
- benchmark 工具可输出 latency distribution、device-vs-host split、throughput、host CPU 和 peak memory。

来源：
https://github.com/axelera-ai-hub/voyager-sdk/blob/latest/RELEASE_NOTES.md

### NanoPC-T6 厂商团队数据

Axelera Team 在官方 Community 2025-12-17 发布 NanoPC-T6 + Metis / Voyager SDK 1.5.2 数据：
- YOLOv8n：约 450 FPS (host)，61 ms latency (OpenCL)；
- YOLOv8s：约 360 FPS (host)，77 ms latency (OpenCL)；
- MobileNetV2：约 3100 FPS (host)；
- ResNet50：约 1600 FPS (host)；
- LPRNet：6084 FPS raw，611 FPS end-to-end。

同时明确指出 RK3588 默认 device tree 的 PCIe non-prefetchable memory window 需要调整。

来源：
https://community.axelera.ai/the-axelera-forum-52/nanopc-t6-now-working-with-metis-setup-guide-available-1178

**证据等级：VENDOR_BENCH / vendor-team community。**

限制：
- 页面没有完整公开 Metis SKU、模型输入尺寸、量化、功耗；
- “host FPS”和“OpenCL latency”的具体统计口径需回到 SDK benchmark 工具复现；
- 不能与 i9 官方 benchmark 或 Jetson live graph 直接数值排序。

## 4. Hailo：Raspberry Pi 5 低功耗 Host 路径

Raspberry Pi 官方资料：
- AI HAT+：Hailo-8L 13 TOPS INT8 / Hailo-8 26 TOPS INT8；
- AI HAT+ 2：Hailo-10H 40 TOPS INT4 + 8GB onboard memory；
- Raspberry Pi 5 camera framework 可直接将支持的视觉 workload offload 到 Hailo NPU；
- AI HAT+ 2 支持 LLM/VLM；
- 重负载/benchmark 场景官方建议使用主动散热/随板 heatsink，避免过热降速。

来源：
https://www.raspberrypi.com/documentation/accessories/ai-hat-plus.html
https://www.raspberrypi.com/documentation/computers/ai.html

Hailo 官方 `hailo-apps` 的 multisource pipeline：
- USB / RTSP / file 多源；
- 多路 stream 并行 decode + scale；
- frame-by-frame 送入 Hailo device；
- HailoRoundRobin + HailoStreamRouter；
- 对 Raspberry Pi，文档建议“up to three sources are optimal”；
- 推荐 15 FPS，默认 640×640。

来源：
https://github.com/hailo-ai/hailo-apps/tree/main/hailo_apps/python/pipeline_apps/multisource

**证据等级：REF。**

上述“3 sources / 15 FPS”是官方应用指导，不是标准化 Benchmark，不能写成 Hailo-8/10H 的固定性能上限。

## 5. Houmo M50：RK3588 Host 已有产品化组合

已有证据：
- BX50 = RK3588 host + M50；
- 厂商称支持 32 路视频分析；
- M50/xh2 有官方 YOLO 模型级 benchmark；
- xh2 runtime 有多线程、多 stream 示例。

但仍未公开：
- 32 路每路 resolution/FPS/codec；
- model / precision；
- RK3588 decode/pre-process 占用；
- PCIe traffic；
- Host + LQ50 total power。

所以 M50 与 Metis/Hailo 一样，评估必须把 Host 一并作为产品变量。

## 6. 统一 Benchmark 应测什么

### 数据路径
1. sensor ingest / decode FPS；
2. ISP/VPU utilization；
3. host→accelerator copy bytes/frame；
4. PCIe effective GB/s 与 queue depth；
5. resize/color conversion latency；
6. inference latency；
7. D2H/result latency；
8. post-process / tracking；
9. total Frame Age。

### 资源
- Host CPU utilization / per-core load；
- Host GPU/VPU；
- Host DDR bandwidth；
- Accelerator utilization / memory；
- PCIe utilization；
- host memory + accelerator memory；
- total system power，而非 accelerator-only power；
- temperature / throttling。

### 并发
至少测试：
- W1 only；
- W1+W3；
- W1+W2+W3；
- W1+W2+W3+W6；
- 30/60/120 min thermal steady state。

## 7. 工程判断

截至当前公开证据：

1. **Host 不是“配套板”，而是 Host+Accelerator 系统的一半。**
2. **ARM Host 可行性已经不是假设。** Metis 已官方验证 RK3588/RPi5/Orin；Hailo 已被 Raspberry Pi 5 官方集成；M50 已有 RK3588+M50 产品组合。
3. **ARM Host 可用 ≠ ARM Host 性能足够。** 仍需统一模型、视频输入、功耗和并发条件下复测。
4. 对六摄像头无人平台，若采用独立 accelerator，真正需要比较的是：
   **Host 视频/SLAM能力 + 数据搬运 + Accelerator DNN性能 + 总功耗/热**。


## 7. Host+Accelerator 对闭环时延预算的新增项

闭环模型见：
`research/architecture/closed-loop-latency-platform-mapping.md`

对独立 accelerator，需要在传统 `T_perception` 内继续拆：

```text
T_perception =
T_host_preprocess
+ T_H2D
+ T_accel_queue
+ T_inference
+ T_D2H
+ T_host_postprocess
```

所以单模型 inference/P99 只覆盖其中一部分。

当前公开证据：
- M50/xh2 已有模型 E2E P99；
- Metis+RK3588 有厂商团队 OpenCL latency；
- Hailo/RPi5 有多源 Reference，但缺统一 P99。

下一步真正有判别力的是：
**same Host + same Camera input + same model + same Frame Age instrumentation**。
