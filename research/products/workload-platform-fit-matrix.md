# Workload → Compute Resource → Platform 适配矩阵

- 状态：v0.7
- 日期：2026-09-30
- 目标：建立基于公开案例、论文、官方 benchmark 和硬件事实的端侧平台适配分析
- 证据索引：[`platform-workload-evidence-2026.md`](../../references/webpages/platform-workload-evidence-2026.md)
- 工作负载定义：[`workload-taxonomy.md`](../workloads/workload-taxonomy.md)

## 1. 规则

本矩阵不做“最好/最差”排名，也不按 TOPS 排序。

每个判断必须满足以下之一：
- 有命名系统/量产案例（CASE）；
- 有条件明确的 benchmark（BENCH）；
- 有官方 reference design（REF）；
- 有官方规格/SDK 支持（SPEC）；
- 有公开演示但条件不足以复现（DEMO）；
- 只有架构推导时明确标记 INFER；
- 证据不足标记 GAP。

**“CASE”只证明该系统组合存在，不自动证明全部 workload 都由目标芯片单独执行。**

## 2. Workload 对计算资源的第一版映射

| Workload | 主要计算资源 | 关键系统资源 | 典型瓶颈 |
|---|---|---|---|
| W1 Sensor/Video | ISP/VPU + CPU/DMA | CSI/SerDes、DDR、时间戳、编码器 | pixel rate、DDR copy、同步、视频通道 |
| W2 Localization/VIO/SLAM | CPU + GPU（按算法） | IMU/Camera同步、低延迟内存 | feature/front-end、BA/optimization、jitter |
| W3 DNN Perception | NPU/GPU | ISP、DDR、runtime/compiler | 模型算子、前后处理、多流并发 |
| W4 3D/BEV/Mapping | GPU + CPU + NPU（按算法） | 大内存/高带宽、point cloud | temporal state、3D tensor、map growth |
| W5 Prediction/Tracking | CPU/GPU/NPU | world state、历史窗口 | temporal model、目标数、并发 |
| W6 Planning/Optimization | CPU 为主；部分 GPU/NPU | 实时调度、地图/约束数据 | worst-case latency、优化收敛 |
| W7 LLM/VLM/VLA | GPU/NPU + 大容量内存 | 高带宽、量化、runtime | model fit、TTFT、tokens/s、action rate |
| W8 Multi-Agent/Fleet | CPU/Network/Edge server | Wi-Fi/5G/Ethernet、message bus | 通信时延、全局优化、扩展性 |
| W9 Safety Control | MCU/RT CPU | CAN/UART/PWM/Watchdog/RTOS | WCET、jitter、failover |

## 3. 证据驱动平台矩阵

标签含义：CASE / BENCH / REF / SPEC / PAPER / DEMO / INFER / GAP，详细来源见证据索引 E01–E38。

| 平台 | W1 | W2 | W3 | W4 | W5 | W6 | W7 | W8 | W9 | 当前工程边界 |
|---|---|---|---|---|---|---|---|---|---|---|
| NVIDIA Jetson Orin | SPEC+BENCH E01/E02/E35 | CASE+PAPER+BENCH E03/E04/E05/E35 | CASE+BENCH E02/E03/E35 | CASE+PAPER+BENCH E03/E05/E35 | CASE E03 | CASE(system) E03 | PAPER E06 | GAP | GAP | Nova Carter 已有物理3/4-camera live graph：VSLAM、DNN stereo depth、Nvblox；仍缺六摄像头+YOLO同构并发、功耗/热和硬实时飞控证据 |
| Qualcomm Flight RB5 | REF E07 | REF E07 | REF E07 | REF(深度/SLAM) E07 | REF E07 | REF E07 | GAP | REF E07 | GAP | 典型 UAV companion/reference platform；飞控 W9 边界需单独设计 |
| Qualcomm IQ-9075 | SPEC+REF+PARTNER_BENCH E08/E27/E29/E30 | REF E28/E31 | REF+PARTNER_BENCH E29/E30/E31 | REF(2D mapping/depth) E28/E31 | REF E31 | REF(Nav2) E28/E31 | SPEC+BENCH(vendor) E08 | INFER | SPEC+PARTNER_BENCH E08/E25 | W1/W3 已有多流可复现实测，W2/W4/W5/W6 有官方 ROS2 reference；仍缺物理多 camera 同步、VIO/SLAM latency 与完整自主栈全并发 benchmark |
| Rockchip RK3588 | SPEC E20 | PAPER(system) E24 | SPEC+REF+BENCH E20/E23/E33 | PAPER(system) E24 | INFER | INFER | GAP | GAP | INFER | W3 已有单模型 benchmark 与官方多 context/三核调度路径；仍无证据支持按核心数线性推算，多摄像头+SLAM+DNN 并发继续为 GAP |
| Horizon Journey 6M | CASE(system) E10 | CASE(system) E10 | CASE+SPEC E09/E10 | CASE+SPEC E09/E10 | CASE(system) E10 | CASE+SPEC E09/E10 | GAP | GAP | SPEC(系统安全架构) E09 | 量产车端证据强，但与 UAV 的 SWaP、接口、软件生态不可直接等同 |
| Black Sesame A2000 | SPEC E11/E21 | INFER | SPEC E11/E21 | SPEC E11/E21 | INFER | SPEC E11/E21 | SPEC+DEMO E11/E21 | GAP | SPEC E11/E21 | 2026 官方已披露 200–1000 TOPS 家族、VLA/world-model 与 Qwen VLM 演示；仍缺公开可复现 benchmark |
| Axelera Metis M.2 | HOST+REF E14/E36 | GAP | CASE+BENCH+VENDOR_BENCH E12/E13/E37 | GAP | CASE E13 | GAP | SPEC(实验性 LLM) E14 | GAP | GAP | ARM Host 已官方验证（含RK3588/RPi5/Orin），NanoPC-T6 有厂商团队性能锚点；W1/W2/W6/W9 与总功耗仍取决于 Host |
| Hailo-8 / Hailo-10H | HOST+REF E38 | CASE(system) E15/E16 | CASE+REF+VENDOR_BENCH E15/E16/E22/E38 | GAP | INFER | GAP | SPEC+REF+VENDOR_BENCH E17/E22/E38 | GAP | GAP | Raspberry Pi 5 已有官方 Camera/Multisource/GenAI 集成路径；多源配置指导不是标准Benchmark，SLAM/规划和总系统功耗仍由Host架构决定 |
| Houmo M50 / LQ50 M.2 | HOST依赖 E18/E26 | GAP | SPEC(system)+REF(multistream)+VENDOR_BENCH(M50) E26/E32/E34 | GAP | GAP | GAP | SPEC+VENDOR_BENCH E18/E19 | GAP | GAP | M50 已有 xh2 YOLO 模型级 benchmark 和官方多线程多-stream runtime 路径；LQ50 板卡 + host 的 Camera/PCIe/总功耗端到端性能仍是 GAP |

## 4. 按体系结构得到的工程判断

### 4.1 高集成异构 SoC / SoM

代表：Jetson Orin、Qualcomm Flight RB5/IQ-9075、RK3588、Journey 6、A2000。

**事实基础**
- 这些平台把 CPU、GPU/NPU、内存、Camera/ISP 或实时子系统的一部分集成到同一平台。
- Jetson/Qualcomm/车规 SoC 已有完整机器人、无人机或智能驾驶系统路径。

**工程判断**
对于 W1+W2+W3+W4+W6 这种“感知—定位—地图—规划”的组合，集成 SoC/SoM 更容易减少 PCIe 往返、host/accelerator 双份内存和软件编排复杂度。

这不是说其峰值 AI 算力更高，而是**系统资源更完整**。

### 4.2 Host + M.2/PCIe AI Accelerator

代表：Axelera Metis、Hailo-8/10H、Houmo LQ50。

**事实基础**
- Metis 官方文档明确把视频 decode 与部分 pre/post-processing 放在 host。
- Hailo 与后摩产品本质上也是独立加速器形态。
- DroneStar、Astrial 等案例证明该路线可以进入无人机。

**工程判断**
这种架构适合：
- 在已有 CPU/SoC 系统上增量增加 W3 或 W7；
- 需要较高 AI 推理密度但不希望整体换主控的平台；
- Camera/ISP/VIO/SLAM/规划已经由 host 解决的系统。

主要风险：
- PCIe 数据搬运；
- host CPU/VPU 是否够用；
- 内存复制；
- SDK 算子覆盖；
- 多模型并发；
- host+accelerator 总功耗，而不是只看加速卡 10W/13W。

## 5. 对六摄像头 UAV Case 的直接启示

### 5.1 可以引用但不能照抄的现实案例

Skydio X10 是当前最有价值的锚点之一：
- 6 路 navigation cameras；
- Jetson Orin；
- 360°视觉；
- GPS-denied navigation；
- obstacle avoidance / tracking；
- onboard 2D/3D mapping。

它证明“六摄像头 + 较强异构端侧计算 + 自主导航”是真实产品路径，而不是假设。

但不能据此直接得出本项目也需要 Jetson Orin 或 275 TOPS，因为以下变量不同：
- 分辨率/帧率；
- camera pipeline；
- 是否六路都做 DNN；
- SLAM 使用几路 camera；
- 深度方案；
- 飞行速度/避障距离；
- 功耗/重量；
- 算法和软件实现。

### 5.2 第一轮平台验证应分成两种架构

**架构 A：一体化 SoC/SoM**
- RK3588 / Qualcomm / Jetson 等
- W1/W2/W3 在同一主平台内完成
- 重点测内存带宽、多任务抢占、GPU/NPU/CPU 并发

**架构 B：Host + AI Accelerator**
- RK3588/其他 host + Metis/Hailo/LQ50
- Host 负责 W1/W2/W6，accelerator 主要负责 W3/W7
- 重点测 PCIe、zero-copy、host preprocessing、端到端 latency 和总功耗

这两个架构必须分开 Benchmark，不能只比较“6 TOPS vs 160 TOPS vs 214 TOPS”。

## 6. 当前证据缺口

1. **RK3588**：W3 单模型官方 benchmark 与 W2/W4 论文系统证据已补齐；仍需要 ORB-SLAM3/VIO + multi-camera + YOLO 并发数据。
2. **Houmo LQ50**：M50 已有官方 YOLOv5s/YOLO11m xh2 模型级 benchmark；仍需要 LQ50 板卡 + host 的 PCIe/video/multi-stream 端到端数据与板级功耗。
3. **Black Sesame A2000**：需要公开 benchmark 或量产 workload 的可量化数据。
4. **Qualcomm IQ-9075**：W1/W3 已有 1/4/9/16 stream partner benchmark，W2/W6 有官方 SLAM/Nav2 reference，W9 有 EtherCAT partner benchmark；主要缺物理多 camera 同步、VIO/SLAM 定量性能和完整自主栈并发。
5. **Hailo/Metis**：需要换用低功耗 ARM host 后重复端到端性能与功耗测试。
6. **所有平台**：需要在 30/60/120 min 稳态下测温度、降频和性能漂移。

## 7. 下一步

优先把矩阵从“证据存在性”推进到“可量化适配”：

1. 为 Jetson Orin、RK3588、IQ-9075、Metis、Hailo、LQ50 建立统一 product facts；
2. 将公开 benchmark 按 model/input/precision/host/software/power 条件结构化；
3. 针对六摄像头 Case 冻结 W1 输入参数；
4. 选定一个 W3 detection baseline 和一个 W2 VIO/SLAM baseline；
5. 生成两套可复现实验：一体 SoC 与 Host+Accelerator。
