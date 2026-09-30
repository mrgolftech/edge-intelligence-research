# Workload → Compute Resource → Platform 适配矩阵

- 状态：v0.2
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

标签含义：CASE / BENCH / REF / SPEC / PAPER / DEMO / INFER / GAP，详细来源见证据索引 E01–E22。

| 平台 | W1 | W2 | W3 | W4 | W5 | W6 | W7 | W8 | W9 | 当前工程边界 |
|---|---|---|---|---|---|---|---|---|---|---|
| NVIDIA Jetson Orin | SPEC+BENCH E01/E02 | CASE+PAPER E03/E04/E05 | CASE+BENCH E02/E03 | CASE+PAPER E03/E05 | CASE E03 | CASE(system) E03 | PAPER E06 | GAP | GAP | 公开证据最完整的是多传感器机器人计算；安全飞控/硬实时控制不应默认放在 Orin 上 |
| Qualcomm Flight RB5 | REF E07 | REF E07 | REF E07 | REF(深度/SLAM) E07 | REF E07 | REF E07 | GAP | REF E07 | GAP | 典型 UAV companion/reference platform；飞控 W9 边界需单独设计 |
| Qualcomm IQ-9075 | SPEC E08 | INFER | SPEC E08 | INFER | INFER | INFER | SPEC+BENCH(vendor) E08 | INFER | SPEC E08 | 新一代工业/机器人 SoC，异构资源完整；LLM 有官方量级数据，但 W2/W4/W6 仍需真实机器人 benchmark |
| Rockchip RK3588 | SPEC E20 | INFER | SPEC E20 | INFER | INFER | INFER | GAP | GAP | INFER | 低成本一体 SoC；W2/W4/W6 需以真实算法和并发测试验证，不能由 6 TOPS 外推 |
| Horizon Journey 6M | CASE(system) E10 | CASE(system) E10 | CASE+SPEC E09/E10 | CASE+SPEC E09/E10 | CASE(system) E10 | CASE+SPEC E09/E10 | GAP | GAP | SPEC(系统安全架构) E09 | 量产车端证据强，但与 UAV 的 SWaP、接口、软件生态不可直接等同 |
| Black Sesame A2000 | SPEC E11/E21 | INFER | SPEC E11/E21 | SPEC E11/E21 | INFER | SPEC E11/E21 | SPEC+DEMO E11/E21 | GAP | SPEC E11/E21 | 2026 官方已披露 200–1000 TOPS 家族、VLA/world-model 与 Qwen VLM 演示；仍缺公开可复现 benchmark |
| Axelera Metis M.2 | HOST依赖 E14 | GAP | CASE+BENCH E12/E13 | GAP | CASE E13 | GAP | SPEC(实验性 LLM) E14 | GAP | GAP | 强项证据集中在视觉推理；W1 解码/预处理及 W2/W6/W9 依赖 host |
| Hailo-8 / Hailo-10H | HOST依赖 | CASE(系统) E15/E16 | CASE+BENCH(vendor) E15/E16/E22 | GAP | INFER | GAP | SPEC+BENCH(vendor) E17/E22 | GAP | GAP | Hailo-8 有真实视觉案例，Hailo-10H 有视觉/GenAI 厂商量级数据；都不能替代主控/飞控 |
| Houmo M50 / LQ50 M.2 | HOST依赖 E18 | GAP | GAP/待公开benchmark | GAP | GAP | GAP | SPEC+vendor benchmark E18/E19 | GAP | GAP | 当前公开证据最强的是 W7；160 TOPS 不能直接外推无人机 W2/W3/W6 |

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

1. **RK3588**：需要公开或自测 ORB-SLAM3/VIO + multi-camera + YOLO 并发数据。
2. **Houmo LQ50**：需要 W3 视觉模型公开 benchmark、实际 host 条件和端到端 pipeline 数据。
3. **Black Sesame A2000**：需要公开 benchmark 或量产 workload 的可量化数据。
4. **Qualcomm IQ-9075**：需要 ROS2/VIO/SLAM/多路视觉实测，而不只是产品规格。
5. **Hailo/Metis**：需要换用低功耗 ARM host 后重复端到端性能与功耗测试。
6. **所有平台**：需要在 30/60/120 min 稳态下测温度、降频和性能漂移。

## 7. 下一步

优先把矩阵从“证据存在性”推进到“可量化适配”：

1. 为 Jetson Orin、RK3588、IQ-9075、Metis、Hailo、LQ50 建立统一 product facts；
2. 将公开 benchmark 按 model/input/precision/host/software/power 条件结构化；
3. 针对六摄像头 Case 冻结 W1 输入参数；
4. 选定一个 W3 detection baseline 和一个 W2 VIO/SLAM baseline；
5. 生成两套可复现实验：一体 SoC 与 Host+Accelerator。
