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


## 4. 官方 Model Zoo 已补齐 M50 模型级 W3 证据

官方仓库：https://github.com/houmo-ai/postmo-modelzoo

### 4.1 xh2 与 M50
- MiniCPM-o 示例写明“部署到后摩 M50 芯片设备上”；
- 同文明确“本例只适用于 xh2”；
- Qwen3 Pipeline 把 `ndevice` 描述为 M50 device nums；
- 运行日志使用 `Xh2HalBackend`。

因此 xh2 是 M50 的官方执行 target 之一。

### 4.2 YOLOv5s
- input 640×640；COCO2017 val 5000；ncore=1；
- xh2 mAP50-95 0.355790；
- inference avg 6.668ms；
- E2E avg 9.715ms，P99 9.834ms；
- 4-thread throughput 410.350 qps。

### 4.3 YOLO11m
- input 640×640；COCO2017 val 5000；ncore=1；
- xh2 mAP50-95 0.489875；
- inference avg 17.069ms；
- E2E avg 19.917ms，P99 20.207ms；
- 4-thread throughput 199.962 qps。

## 5. 更新后的证据边界
可以写：**M50 对 W3 已有官方模型级定量 benchmark。**

仍不能写：**LQ50 在六路 camera / RK3588 host 下能达到上述吞吐。**

YOLO 页面没有给出具体 LQ50 SKU、core frequency、板卡/系统功耗、Camera/codec/PCIe/host preprocessing。throughput 也是多线程压力测试，不是六路视频端到端 FPS。


## 6. 官方多线程多-stream runtime 示例

官方路径：
https://github.com/houmo-ai/postmo-modelzoo/tree/release_xh2_v1.3.0/apis/inferences/resnet50_multistreams

`Resnet50 Multistreams Example` 明确用于展示：
- Python：多线程、多 stream；
- C++：多设备、多线程、多 stream；
- `create_weight_manager` 共享模型内存；
- 每个线程使用 1 个 stream；
- 每个设备可配置相同数量的线程。

默认参数：
- device count = 1；
- threads = 4；
- samples = 10。

示例日志显示：
- 4 个线程同时在 device 0 上加载 `resnet50_xh2_b1_1roi_1core_O2.hmm`；
- backend 为 `Xh2HalBackend`；
- C++ 示例中 10 个 samples 被 4 个线程竞争消费并完成推理。

### 工程意义

这进一步证明：
> **M50-compatible xh2 runtime 具备官方多线程、多 stream 的软件实现路径。**

但这仍属于 REF，不是 Benchmark，因为文档没有给出：
- 标准化 aggregate throughput；
- P95/P99；
- device power；
- PCIe host 负载；
- Camera/video decode；
- 多路物理传感器输入。

因此不能从日志时间戳自行算出一个“官方 FPS”，也不能用它证明 LQ50 的六路视频能力。
