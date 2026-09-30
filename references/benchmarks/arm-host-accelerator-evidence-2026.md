# ARM Host + Accelerator 公开基线

- 日期：2026-09-30
- 状态：v0.1
- 目的：记录低功耗 ARM Host 与独立 AI accelerator 的公开兼容性和性能证据，避免只引用 x86 Host 峰值数据。

## 1. Axelera Metis

### 官方 ARM Host compatibility
来源：https://axelera.ai/systems/arm-host

已验证：
- RK3588：Firefly ITX-3588J、Orange Pi 5 Plus、NanoPC-T6；
- Raspberry Pi 5；
- Jetson Orin Nano/NX；
- NXP i.MX95 等。

证据类型：SPEC / REF。

### NanoPC-T6 + Metis
来源：https://community.axelera.ai/the-axelera-forum-52/nanopc-t6-now-working-with-metis-setup-guide-available-1178

发布者：Axelera Team，2025-12-17。

Voyager SDK 1.5.2：
- YOLOv8n：~450 FPS (host)，61ms latency (OpenCL)；
- YOLOv8s：~360 FPS (host)，77ms latency (OpenCL)；
- LPRNet：6084 FPS raw / 611 FPS end-to-end。

证据类型：VENDOR_BENCH（厂商团队社区发布）。

关键限制：
- exact Metis SKU / input / quantization / system power 未完整公开；
- 必须保留页面的“host FPS”和“OpenCL latency”原始口径；
- RK3588 device tree 需要扩大 PCIe non-prefetchable memory window。

## 2. Hailo + Raspberry Pi 5

Raspberry Pi 官方资料：
https://www.raspberrypi.com/documentation/accessories/ai-hat-plus.html
https://www.raspberrypi.com/documentation/computers/ai.html

确认：
- Hailo NPU 通过 PCIe 与 RPi5 集成；
- camera framework 可运行实时视觉 AI；
- Hailo-10H AI HAT+ 2 有 8GB onboard memory，并支持 LLM/VLM；
- benchmark / intensive workload 应配置散热，避免 thermal slowdown。

Hailo Apps：
https://github.com/hailo-ai/hailo-apps

Multisource Reference：
- multiple USB/RTSP/file sources；
- parallel decode/scale；
- Hailo device round-robin；
- RPi 上 up to 3 sources optimal；
- recommendation 15 FPS / 640×640。

当前证据类型：REF，不是标准化 BENCH。

## 3. 对平台比较的要求

公开资料现在足以证明：
- Metis 和 Hailo 都可以放到低功耗 ARM Host；
- RK3588 是实际可用的 accelerator Host 路线之一。

但还不足以公平比较：
- Metis vs Hailo vs M50 的端到端 FPS；
- 同一个 RK3588 Host 下的 CPU/DDR/PCIe 占用；
- 六路 Camera + VIO/SLAM 并发；
- total system power。

因此下一步应该设计 **同 Host / 同模型 / 同视频输入 / 同功耗统计边界** 的复现实验，而不是继续收集不同厂商的峰值 FPS。
