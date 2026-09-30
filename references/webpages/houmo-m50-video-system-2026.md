# 后摩 M50 / LQ50：视觉系统证据边界

- 日期：2026-09-30
- 状态：verified-public-evidence

## 1. LQ50 直接证据

官方用户指南：
https://developer.houmoai.com/hmdoc/m50/hardware-manuals/latest/product-manuals/lq50-m.2/LQ50_M.2_guidelines/intro/index.html

已确认：
- M50 ×1 / 2 IPU cores
- 160 TOPS
- 100 TFLOPS@bFP16
- 24GB LPDDR5/LPDDR5X（该用户指南型号）
- 153.6GB/s
- PCIe Gen4 x4
- 22×80mm
- typical 13W

该资料主要面向端边大模型推理。

## 2. BX50 证明 M50 可以进入视频分析系统

官方发布资料：
https://www.houmoai.com/1/35/NewsDetails.html

BX50 产品页：
https://www.houmoai.com/58/10/Product.html

已确认/厂商宣称：
- BX50 host CPU：RK3588
- GPU：Mali-G610 MC4
- NPU：1× M50
- Ubuntu 20.04
- system typical power ≤25W
- 厂商发布资料称支持 32 路视频分析与本地大模型

## 3. 为什么不能把它写成“LQ50 支持 32 路”

BX50 是完整整机：
- RK3588 提供 CPU/GPU/video/host 资源
- M50 提供 AI acceleration
- 整机还有独立内存、I/O、散热和软件栈

因此“32 路视频分析”只能证明：
> **M50 可以作为 Host + Accelerator 视频系统的一部分。**

不能证明：
- LQ50 M.2 在任意 host 上都能跑 32 路；
- 每路分辨率/FPS；
- 具体 detection model；
- W3 FPS/latency；
- PCIe 与 host preprocessing 的实际占用。

所以当前矩阵应写：
- M50 W3：SPEC(system via BX50)
- LQ50 direct W3 benchmark：GAP
