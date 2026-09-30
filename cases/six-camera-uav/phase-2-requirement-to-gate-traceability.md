# 六摄像头 UAV：Requirement → Architecture Gate Traceability Matrix

- 状态：v0.2
- 日期：2026-09-30
- 基础 Composition：C2 Visual Autonomy
- 目的：把每个架构 Gate 的 Candidate / Unverified / Requirement-missing 追溯到具体需求变量、事实锚点与未来验证项
- 关联：
  - `phase-2-requirement-card.md`
  - `phase-2-workload-compositions.md`
  - `phase-2-architecture-gate-matrix.md`
  - `research/workloads/c2-visual-autonomy-resource-envelope.md`
  - `data/calculations/six-camera-requirement-gate-traceability.csv`

## 1. 为什么需要 Traceability

当前平台判断最大的风险不是候选平台太少，而是：

> Requirement 未冻结时，平台能力与项目需求无法一一对照。

因此每个变量必须回答五件事：

1. 当前值是什么；
2. 这是 PROJECT / REF / CALC / GAP 中哪一种；
3. 影响哪个 Architecture Gate；
4. 如果不冻结，会阻塞哪类判断；
5. 后续通过设计输入、资料或 Benchmark 如何关闭。

---

## 2. 第一版矩阵

| ID | Requirement | 当前状态 | Gate | 为什么阻塞 |
|---|---|---|---|---|
| R01 | N_capture | 6，Confirmed | A/C/E | 已有基本输入规模，但仍需 FPS/mode 才能形成吞吐 |
| R02 | downstream geometry | 1072×1280，单路观测 | A/C/D | 可做 buffer/payload 算术，不能证明六路一致 |
| R03 | downstream format | NV12，单路观测 | C | 可计算 image-plane，但不能反推 Sensor RAW |
| R04 | actual FPS | **Requirement-missing** | A/C/D/E | 不冻结就无法得到 PixelRate、FramePeriod、W1 deadline |
| R05 | 六路 mode 是否一致 | GAP | A/C/E | 可能存在异构流，不能直接乘 6 |
| R06 | sync / timestamp tolerance | Requirement-missing | A/E | VIO/depth/融合的输入质量与 Frame Age 无法验收 |
| R07 | N_detection | Requirement-missing | D/E | 直接决定 aggregate inference/s |
| R08 | detection model/input/precision | Requirement-missing | C/D/E/G | 无法绑定任何公开 benchmark |
| R09 | detection update rate | Requirement-missing | D/E | 无法计算 W3 service demand |
| R10 | N_vio + mono/stereo topology | Requirement-missing | A/C/D/E | W2 CPU/GPU、sync 和 camera set 均未知 |
| R11 | N_depth + depth method | Requirement-missing | C/D/E | stereo / DNN depth / geometry 路线资源差异很大 |
| R12 | local map representation/range/update | Requirement-missing | C/D/E | W4 memory/DDR/GPU 无法预算 |
| R13 | planner + update rate/horizon | Requirement-missing | D/E | W6 service demand 与 deadline 未定义 |
| R14 | N_record + codec | Requirement-missing | A/C/F | 录像会额外占 VPU、DDR、storage、power |
| R15 | max/nominal flight speed | Requirement-missing | E | 不能把 latency 转换为 reaction distance |
| R16 | usable obstacle detection range | Requirement-missing | E | 无法求允许的最大 pipeline delay |
| R17 | keep-out / safety distance | Requirement-missing | E | 无法形成停止/避障空间余量 |
| R18 | vehicle tracking/response delay | GAP / must measure | B/E | 完整闭环不能只计算 companion compute |
| R19 | steady/peak compute power limit | Requirement-missing | F | 无法把 SoC/SoM/Accelerator功耗映射到产品 |
| R20 | compute mass/volume/cooling limit | Requirement-missing | F | 无法判断外挂卡/风扇/散热器的结构代价 |
| R21 | mission duration / energy budget | Requirement-missing | F | 无法把 W 转换为 Wh/mission |
| R22 | FCU responsibilities / interface deadline | Partial | B/E/G | 已确定原则上独立 FCU，但接口与 deadline 未冻结 |
| R23 | VLM 是否是正式任务 | Decision-pending | C/D/E/F/G | 不能提前为 W7 预留刚性资源 |
| R24 | target OS/ROS/model operator constraints | Partial | D/G | 决定 SDK/算子/集成风险，需随算法冻结 |
| R25 | perception topology: PER_VIEW / FUSED_MULTI_VIEW / MIXED | **Requirement-missing** | C/D/E/G | 决定 model call rate、input view rate、preprocess 与 memory/tensor 结构 |

---

## 3. 当前真正的阻塞链

### Gate A — Sensor / I/O

当前最关键：

```text
R04 actual FPS
R05 six-camera mode
R06 sync tolerance
R14 recording
```

仅知道“6 Camera”不足以判定 Gate A。

---

### Gate B — Real-Time Partition

当前原则已经比较明确：

```text
Linux companion compute
↕
FCU / real-time control
```

但仍缺：

```text
R18 vehicle response
R22 interface deadline / failure behavior
```

因此“某 SoC 有 RT core”不能自动替代 FCU。

---

### Gate C — Memory / DDR

至少受：

```text
R04 FPS
R08 model
R10 VIO
R11 depth
R12 map
R14 recording
R23 optional VLM
```

共同影响。

当前仅能确认六路 1072×1280 NV12：

- one-frame-set ≈ 12.35 MB；
- queue depth 4 ≈ 49.40 MB。

这只是图像队列下限项，不是系统 memory requirement。

---

### Gate D — Compute Engine

核心公式：

```text
Demand_engine =
Σ(InvocationRate × measured ServiceTime)
```

但现在：

- W3 缺 R07/R08/R09；
- W2 缺 R10；
- W4 缺 R11/R12；
- W6 缺 R13。

所以不能从任何一个 TOPS 数字推完整 Gate D。

---

### Gate E — Concurrent Tail Latency

这是当前最大系统级 Gate。

至少需要：

```text
R04 FPS
R06 sync
R07-R13 workload topology
R15 speed
R16 range
R17 keep-out
R18 vehicle response
R22 FCU interface
```

最终条件不是“FPS 足够”，而是：

```text
P99 Frame Age <= project deadline
AND
deadline miss <= project target
```

---

### Gate F — SWaP / Thermal

需要：

```text
R19 power
R20 mass/volume/cooling
R21 mission energy
```

在这三个产品约束未冻结前：

- 20 W SoC；
- 30 W SoM；
- SoC + M.2 accelerator

都只能描述规格，不能判断适不适合无人机。

---

### Gate G — Software / Productization

至少依赖：

```text
R08 model/operators
R22 FCU interface
R23 VLM
R24 OS/ROS/SDK
```

所以“ROS2 支持”只是入口条件，不等于项目软件适配完成。

---

## 4. 需求冻结优先级

这是**项目推进优先级**，不是行业标准。

### P0 — 不冻结就无法继续做架构收敛

- R04 actual FPS；
- R07 N_detection；
- R08 detection model/input/precision；
- R25 perception topology；
- R09 detection rate；
- R10 N_vio/topology；
- R11 N_depth/method；
- R15 flight speed；
- R16 usable range；
- R17 keep-out；
- R19 compute power limit；
- R20 mass/volume/cooling limit。

### P1 — 可以稍晚，但会阻塞系统验证

- R05 six-camera mode consistency；
- R06 sync tolerance；
- R12 map；
- R13 planner；
- R14 recording；
- R18 vehicle response；
- R21 mission energy；
- R22 FCU interface deadline；
- R24 software constraints。

### P2 — 可选能力决策

- R23 VLM/W7。

VLM 只有在具体任务价值成立后进入正式 Requirement。

---

## 5. 证据锚点如何使用

### Camera/FPS

Reference：
- nuScenes：native 6-camera，约 12 Hz；
- TUM VI：stereo 1024×1024 @20 Hz；
- NVIDIA Hawk：stereo raw streams 1920×1200 @30 fps。

这些只给量级，不定义 R04。

### Closed-loop

PX4 当前文档：
- external-vision sensor delay 可到约 0.2 s；
- tracking delay 典型约 0.1–0.5 s；
- 初始 companion 工况为 4 m/s + 10 Hz obstacle messages。

这些证明 R15/R18 必须进入模型，但不定义本项目值。

### Compute

Isaac ROS 5.0、RK3588、IQ-9075、M50/Metis/Hailo 现有 Benchmark 可用于绑定明确 workload 后的 service-time/throughput。

在 R07-R13 未冻结前，不做跨平台“谁更快”结论。

---

## 6. 当前架构矩阵为什么仍然不应收敛为单一路线

四类候选：

1. RK3588 Integrated SoC + FCU；
2. Jetson Orin SoM + FCU；
3. IQ-9075 SoC/SoM + FCU/RT subsystem；
4. RK3588 Host + Accelerator + FCU。

当前它们共同缺的是：

- Project Nominal workload；
- project deadline；
- SWaP boundary；
- concurrent P99。

因此继续增加候选产品的收益低于冻结 R04/R07-R20。

---

## 7. 下一步输出

Traceability 建好以后，下一步不再泛化讨论。

直接建立：

### A. Requirement Profile v0.2
把能够从产品设计确定的参数先冻结。

### B. Candidate Architecture Resource Map
对四条路线分别标：
- W1 放哪里；
- W2 放哪里；
- W3 放哪里；
- W4/W6 放哪里；
- DDR 路径；
- FCU 边界；
- PCIe/H2D/D2H；
- expected bottleneck；
- evidence / gap。

### C. Validation Plan
对每个 GAP 指定：
- 公开资料能不能关闭；
- 必须实测什么；
- 测什么指标；
- 怎样判 Gate。
