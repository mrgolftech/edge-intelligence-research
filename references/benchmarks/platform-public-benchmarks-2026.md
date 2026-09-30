# 公开平台 Benchmark 结构化基线（2026-09）

- 状态：v0.2
- 日期：2026-09-30
- 数据表：`data/benchmarks/public-platform-benchmarks.csv`
- 目的：把“厂商/论文说跑得快”拆成可比较的测试条件，防止只摘 FPS/TOPS 数字。

## 1. 纳入规则

一条 Benchmark 至少记录：

- platform
- workload
- model/node
- input
- host
- software/version（若公开）
- throughput / latency
- source
- evidence status
- limitations

缺失的字段写“未注明”，不能自行补齐。

## 2. 当前最可用的定量证据

### NVIDIA Jetson AGX Orin / Isaac ROS

当前 Isaac ROS Performance Summary 给出同一页面下的多种视觉节点与图级结果。第一版抽取：

- Stereo Disparity Node, 1080p: 124 FPS, 8.6 ms @ 30 Hz
- AprilTag Node, 720p: 189 FPS, 5.3 ms @ 30 Hz
- DetectNet Object Detection Graph, 544p: 73.5 FPS, 15 ms @ 30 Hz
- RT-DETR Object Detection Graph, 720p: 87.3 FPS, 13 ms @ 30 Hz

这些数据可以用于建立 Jetson 自身的视觉 workload 量级，但不能直接代表“六摄像头 + SLAM + detection”并发能力。

来源：
https://nvidia-isaac-ros.github.io/performance/index.html

### Axelera Metis / Voyager

官方 benchmark 页面明确披露：

- host: Intel Core i9-13900K
- YOLOv5m 640×640: 456 inference-only FPS, 452 end-to-end FPS
- YOLOv8s 640×640: 610 inference-only FPS, 617 end-to-end FPS
- 页面同时给出量化后 COCO mAP

这组数据对本项目尤其重要，因为它直接证明：**独立 accelerator 的 FPS 必须连同 host 一起记录。**

来源：
https://axelera.ai/metis-aipu-benchmarks

### Qualcomm IQ-9075 / Innodisk iQ-Studio 多流

条件：EXMP-Q911/IQ-9075、YOLOv10n INT8 640×640、1080p30 H.264、TFLite/QNN 2.32、8 cores、180s warm-up + 300s measurement。

Average E2E FPS/channel：1路 29.46；4路 29.47；9路 28.41；16路 15.90。CPU load 同时从 24.2% 上升到 99.8%。

这说明多流系统瓶颈可能在 decode/pre-post/orchestration/CPU，而不是 NPU peak TOPS。输入是文件流，因此不能当作 16 路物理 Camera benchmark。

来源：https://github.com/InnoIPA/iQ-Studio/tree/main/benchmarks/iqs-streampipe

### Houmo M50-compatible xh2 / Model Zoo

后摩官方 Model Zoo：
- YOLOv5s 640×640：Inference 6.668ms；E2E 9.715ms；P99 9.834ms；4-thread 410.350 qps。
- YOLO11m 640×640：Inference 17.069ms；E2E 19.917ms；P99 20.207ms；4-thread 199.962 qps。
- 两者均提供 COCO2017 精度和 ncore=1 配置。

官方 M50-only 示例与 Xh2HalBackend 建立 M50↔xh2 的兼容证据，因此可作为 M50 芯片级 VENDOR_BENCH；不能解释为 LQ50+host 的多流视频系统性能。

来源：https://github.com/houmo-ai/postmo-modelzoo

## 3. 当前只能作为厂商量级锚点的数据

### Qualcomm IQ-9075

官方产品页给出 Llama 2 7B up to 22 tokens/s。

但当前公开信息没有在同一条结果中完整给出：
- quantization
- context length
- TTFT
- SoC power during test
- exact reference board configuration

因此当前标记 `VENDOR_BENCH`，不能与其他平台 tokens/s 直接比较。

来源：
https://www.qualcomm.com/internet-of-things/products/iq9-series/iq-9075

### Hailo-10H

厂商公开：
- 多种 2B LLM/VLM: first-token latency < 1 s, >10 tokens/s
- YOLOv11m: real-time 4K video stream
- 产品典型功耗 2.5 W

由于缺少模型精确配置、量化/context 和准确 FPS，作为存在性和量级锚点，不进入横向性能排序。

来源：
https://hailo.ai/company-overview/newsroom/news/hailo-announces-general-availability-of-hailo-10h-edge-ai-accelerator-with-generative-ai-capabilities/

### Houmo M50 / LQ50 的 LLM 数据

7B/8B 25+ tokens/s 因模型名、量化、上下文、Host、TTFT 条件不完整，仍只作为 LLM 的 `VENDOR_BENCH` 量级锚点。注意这与上面的 YOLO Model Zoo 视觉数据是两类证据。

来源：
https://www.houmoai.com/1/35/NewsDetails.html

## 4. 不能直接横向比较的典型组合

以下比较当前都不成立：

- Jetson DetectNet 544p FPS vs Metis YOLOv8s 640×640 FPS
- Metis+i9 host vs Jetson integrated SoM
- IQ-9075 Llama2 7B tokens/s vs LQ50 未披露具体 7B/8B 模型 tokens/s
- Hailo 2B VLM >10 tok/s vs 7B/8B LLM tokens/s

原因不是“数据没价值”，而是 **模型、输入、精度、Host、软件和功耗条件不一致**。

## 5. 本项目后续统一复测策略

### W3 Detection
优先统一：
- model: 同一 YOLO variant
- input: 640×640
- precision: INT8（平台可支持时）
- batch: 1 + throughput mode
- metrics: pre-process / inference / post-process / end-to-end
- accuracy: 同一 COCO subset
- host: 明确记录
- power: host + accelerator 与 accelerator-only 分开

### W2 VIO/SLAM
统一：
- ORB-SLAM3 或同一开源实现
- EuRoC / TUM-VI
- ATE/RPE
- real-time factor / FPS
- CPU/GPU usage
- power / thermal

### W7 LLM/VLM
统一：
- exact model + revision
- quantization
- context length
- input modality
- TTFT
- decode tokens/s
- memory
- host/accelerator split
- power

只有完成统一测试条件后，才允许形成定量横向比较。
