# 平台适配证据缺口 Backlog

- 状态：active
- 日期：2026-09-30
- 原则：目标不是把所有 GAP 变成“支持”，而是找到足够证据决定它到底是支持、受限还是不适用。

## P0：六摄像头 Case 直接相关

### G01 — RK3588: W1 + W2 + W3 并发
当前：
- 有 W1/W3 规格基础；
- 缺少可复现的 VIO/SLAM + 多路视频 + detection 并发数据。

可接受证据：
1. 官方/论文/开源项目，明确板卡、算法、输入、FPS、软件版本；
2. 若公开资料不足，执行本项目自测。

必须记录：
- camera count/resolution/fps
- ORB-SLAM3/VIO版本
- detection model/input/precision
- CPU/GPU/NPU/DDR
- dropped frame / latency
- board power / temperature

### G02 — LQ50: W3 视觉推理与 Host 开销
当前：
- W7 大模型证据明确；
- W3 公开、条件完整的数据不足。

可接受证据：
- 同一 YOLO 模型的 input/precision/FPS；
- host CPU；
- PCIe generation/lanes；
- pre/post-processing位置；
- accelerator-only 与 system power。

否则继续保持 GAP。

### G03 — Jetson Orin: 多 workload 并发
当前：
- 单节点和系统案例证据丰富；
- 缺少与六摄像头 Case 完全同构的并发数据。

实验目标：
- W1 only
- W1+W3
- W1+W2+W3
- 30/60/120 min thermal steady state

重点不是再证明“Orin能跑AI”，而是找系统边界。

## P1：新一代候选平台

### G04 — Qualcomm IQ-9075: Robotics workload benchmark
当前：
- 100 dense TOPS、16 camera、36GB ECC、real-time subsystem、LLM 数据已有官方证据；
- 缺 ROS2/VIO/SLAM/多路 detection 的公开统一测试。

目标：
- 搜索 Qualcomm/partner robotics reference implementation；
- 如果只有产品规格，继续标 SPEC/INFER，不升级为 BENCH。

### G05 — Black Sesame A2000: 从汽车案例到可量化 workload
当前：
- 2026 官方公开家族 200–1000 TOPS、VLA/world-model支持、ISP和8TB/s片上缓存；
- 有 Qwen VLM 端侧实时交互演示；
- 缺公开标准化 latency/FPS/power benchmark。

规则：
- 量产/展会演示证明产品路线存在；
- 不从“1000 TOPS”反推 UAV/robot workload 适配。

## P2：Host + Accelerator 路线

### G06 — Metis on low-power ARM Host
当前官方 YOLO benchmark host 为 Intel Core i9-13900K。

需要：
- ARM64 host
- same model/input
- PCIe Gen3 x4
- end-to-end FPS
- host CPU usage
- system power

这是判断其是否适合无人装备的关键数据。

### G07 — Hailo on robotics Host
需要把 Bluewhite/Astrial 等案例进一步拆成：
- exact Hailo SKU
- host
- model
- input
- latency/FPS
- system power

### G08 — Accelerator 与 Host 数据搬运
Metis/Hailo/LQ50统一测试：
- host decode
- resize/color conversion
- H2D/D2H copy
- inference
- post-process
- end-to-end
- zero-copy feasibility

## 证据升级规则

- GAP → SPEC：官方文档明确硬件/SDK能力
- SPEC → REF：官方给出完整 reference design/application flow
- SPEC/REF → BENCH：测试条件足够复现
- 任意 → CASE：出现命名真实产品/量产部署
- DEMO 不自动升级为 BENCH
- CASE 不自动升级为 BENCH

同一平台可以同时拥有多种证据，结论只使用与对应 workload 直接相关的那部分。
