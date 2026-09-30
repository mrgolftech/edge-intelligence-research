# 六摄像头 UAV：Phase 2 Validation Plan

- 状态：v0.1
- 日期：2026-09-30
- 目的：把 Architecture Gate 的 GAP 转成可执行、可复现的验证项
- 当前约束：暂时无实机测试条件；因此本文件同时区分“公开证据可关闭”和“必须后续实测”的项
- 配套：`data/benchmarks/six-camera-validation-matrix.csv`

## 1. 验证原则

统一按以下层级递增：

```text
L0 Requirement freeze
L1 W1 ingest
L2 W3 baseline
L3 W1+W3
L4 W1+W2+W3
L5 W1+W2+W3+W4+W6
L6 closed-loop + FCU/vehicle
L7 thermal / endurance
L8 degraded / fallback
```

不能从 L2 单模型 benchmark 跳过 L3-L7 直接宣布平台满足 C2。

---

## 2. 当前阶段：无实机时先关闭什么

### 可以继续用公开资料关闭/缩小

- 平台 Camera / PCIe / memory / codec 规格；
- SDK/ROS/operator support；
- model-level BENCH；
- official reference graph；
- known product/robotics CASE；
- benchmark harness / profiling method；
- product power range / form factor。

### 公开资料很难真正关闭

以下必须保持 GAP，直到有同构第三方 BENCH 或实测：

- 6×项目 Camera actual ingest；
- project sync tolerance；
- W1+W2+W3 concurrent Frame Age；
- W2+W3+W4+W6 P99；
- Host↔Accelerator H2D/D2H absolute latency；
- full-system DDR contention；
- 30/60/120 min thermal steady state；
- FCU command→vehicle response；
- exact mission power / endurance。

---

# 3. V01 — Requirement Freeze

### 输入

R04 / R07-R17 / R19-R24。

### 输出

Project Nominal：

```text
Camera mode
N_detection / Hz / model
N_vio
N_depth
map/planner
speed/range/keep-out
power/mass/cooling
FCU boundary
```

### Gate

A/C/D/E/F/G。

这是所有硬件测试之前的 prerequisite。

---

# 4. V02 — W1 Multi-Camera Ingest / Sync

### 测试

```text
1 / 2 / 4 / 6 Camera
→ capture
→ timestamp
→ optional ISP
→ memory
```

### 指标

- effective FPS/channel；
- drop；
- timestamp jitter；
- inter-camera skew；
- Frame Age at W1 output；
- CPU；
- DDR；
- ISP utilization；
- power。

### Route 特殊项

- RK3588：lane / ISP / buffer / six-stream；
- Jetson：carrier / SerDes / hardware sync；
- IQ-9075：physical CSI/GMSL + DMABUF；
- Host+Accelerator：**W1 只测 Host**，外挂卡不能算通过 Gate A。

---

# 5. V03 — W3 Baseline

先固定：

- same model；
- same input；
- same precision；
- batch/stream policy；
- SDK/runtime version；
- power mode。

记录：

- single-inference latency；
- P50/P95/P99；
- aggregate inf/s；
- host preprocess/postprocess；
- accelerator utilization；
- power。

作用：
- 绑定 R08/R09；
- 建立 ServiceTime；
- 用于后续 `Demand_engine` 计算。

---

# 6. V04 — W1 + W3

```text
Camera ingest
→ preprocess
→ inference
→ result
```

核心不是模型 FPS，而是：

- Camera→result Frame Age P50/P95/P99；
- drop；
- queue depth；
- CPU/DDR；
- NPU/GPU/accelerator；
- per-camera effective inference Hz。

### Host+Accelerator 额外插桩

必须拆：

```text
T_preprocess
T_H2D
T_accel_queue
T_inference
T_D2H
T_postprocess
```

禁止用 accelerator-only latency 代替 V04。

---

# 7. V05 — W1 + W2 + W3

加入：

- Camera/IMU；
- VIO/SLAM；
- DNN detection。

测：

- VIO update Hz；
- ATE/RPE or project positioning metric；
- W2 P95/P99；
- W3 P95/P99；
- whole graph Frame Age；
- CPU/GPU/NPU；
- DDR；
- drop；
- jitter。

这是六摄 Case 的第一道真正 C2 Gate。

---

# 8. V06 — W1 + W2 + W3 + W4 + W6

加入：

- depth；
- local map；
- planner。

输出：

```text
sensor timestamp
→ perception/localization
→ map
→ planner output
```

核心指标：

- P50/P95/P99 Frame Age；
- planner P99；
- deadline miss；
- map age；
- queue；
- drop；
- resource utilization；
- power/temp。

这个测试才接近“端侧自主计算平台”而不是 AI accelerator benchmark。

---

# 9. V07 — FCU / Vehicle Closed Loop

```text
sensor
→ companion
→ planner command
→ FCU
→ vehicle response
```

需要测：

- command transport latency；
- FCU scheduling；
- setpoint→actual response；
- actual tracking delay；
- closed-loop reaction distance。

PX4 公开 0.1–0.5 s tracking delay 只是 REF，不能替代本机测量。

---

# 10. V08 — DDR / Data-Movement Audit

## Integrated

测：

- memory controller traffic；
- copy count；
- zero-copy path；
- W1 only / W1+W3 / full C2 的增量。

## Host+Accelerator

额外测：

- effective PCIe throughput；
- H2D；
- D2H；
- payload size sensitivity；
- batching；
- double buffering on/off；
- queue delay。

Metis double buffering 的 throughput/latency trade-off必须单独记录。

---

# 11. V09 — Power / Thermal Steady State

建议统一：

```text
30 min
60 min
120 min
```

每阶段：

- board/system power；
- SoC/accelerator temperature；
- CPU/GPU/NPU frequency；
- throttling；
- P95/P99；
- drop；
- fan/heatsink state。

输出不能只写峰值 W，需要：

```text
performance vs temperature vs power vs time
```

---

# 12. V10 — Peak Mission

在 Nominal 上逐步打开：

- recording；
- tracking；
- depth/map；
- network/storage；
- higher detection coverage。

目的：
- 找出第一个失稳资源；
- 不要求 Peak 永远无降级，但必须定义降级触发条件。

---

# 13. V11 — Degraded / Fallback

主动制造：

- over-temperature；
- accelerator unavailable；
- DNN overload；
- Camera loss；
- storage/network congestion。

观察：

- W9 是否保持；
- W2/W6 是否能保留；
- noncritical W3/recording/W7 是否优先 shedding；
- recovery 行为；
- watchdog/failsafe。

---

# 14. V12 — Software / Productization

检查：

- target model operator coverage；
- model conversion；
- ROS2 integration；
- zero-copy；
- profiling；
- logging；
- OTA/diagnostics；
- SDK version pinning；
- long-term support；
- supply/domestic sourcing。

这是 Gate G，不应在算法跑通后才补做。

---

# 15. 四条路线的验证重点不同

| Route | 最关键验证 |
|---|---|
| RK3588 Integrated | W1+W2+W3 shared DDR / CPU tail / thermal |
| Jetson Orin | exact project graph P99 / power mode / SWaP |
| IQ-9075 | physical Camera→DMABUF→QNN + visual VIO concurrency |
| RK3588 + Accelerator | Host headroom + H2D/D2H + total system power |

统一 testcase 保证横向结构一致；差异项保证不会把不同架构硬塞进一个 Benchmark。

---

# 16. 当前优先级

## P0

- V01 Requirement Freeze；
- V02 W1；
- V04 W1+W3；
- V05 W1+W2+W3；
- V07 vehicle response；
- V09 power/thermal。

## P1

- V06 full C2；
- V08 DDR/PCIe；
- V10 Peak；
- V11 Fallback。

## P2

- W7/VLM 增量验证。

在 C2 baseline 未稳定前，不让 VLM Benchmark 抢占主线。
