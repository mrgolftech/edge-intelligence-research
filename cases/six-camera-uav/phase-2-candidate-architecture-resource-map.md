# 六摄像头 UAV：Candidate Architecture Resource Map

- 状态：v0.1
- 日期：2026-09-30
- 基础 Composition：C2 Visual Autonomy
- 目的：把候选平台从“规格/算力对比”推进为“工作负载职责 + 数据路径 + 共享资源 + 架构边界”比较
- 关联：
  - `phase-2-requirement-card.md`
  - `phase-2-requirement-to-gate-traceability.md`
  - `phase-2-architecture-gate-matrix.md`
  - `research/products/workload-platform-fit-matrix.md`
  - `research/architecture/host-accelerator-edge-architecture.md`
  - `data/calculations/six-camera-candidate-architecture-resource-map.csv`

## 1. 比较原则

本文件不比较“谁最好”，只回答：

1. W1/W2/W3/W4/W6/W9 分别由谁承担；
2. 图像、tensor、map、结果跨越哪些 memory / interconnect；
3. 哪些 workload 竞争同一 CPU/GPU/NPU/DDR；
4. 哪些模块必须依赖 Host；
5. 哪些已由 SPEC/REF/BENCH/PAPER 证明；
6. 哪些仍是 GAP；
7. 因此应该怎样设计后续验证。

---

# 2. Route A — RK3588 Integrated SoC + External FCU

## 2.1 第一版职责分配

```text
6 Camera
  ↓
MIPI CSI / ISP / DMA
  ↓
Host DDR
  ├─ W2 VIO/SLAM → CPU/GPU
  ├─ W3 Detection → RKNN NPU
  ├─ W4 Local Map → CPU/GPU
  ├─ W6 Planner → CPU (algorithm-dependent)
  └─ Codec/Record → VPU
  ↓
FCU / W9
```

### Evidence

- W1：RK3588 官方 Camera/ISP/VPU 规格基础；
- W2/W4：公开 RK3588 SLAM system PAPER；
- W3：Rockchip RKNN Model Zoo BENCH + multi-context/core API；
- W6：当前主要为架构推断，缺六摄项目同构 BENCH；
- W9：本项目架构原则采用 external FCU。

## 2.2 Memory / Data Path

主要是单 Host memory domain：

```text
Camera
→ ISP/DMA
→ LPDDR
→ CPU/GPU/NPU/VPU consumers
```

潜在优点：
- 不需要把完整 image/tensor 经 PCIe 外发；
- Camera、VIO、DNN、Map 可在单平台编排。

结构性风险：
- ISP/VPU、CPU/GPU/NPU 同时竞争 DDR；
- W2/W6 对 CPU tail latency 敏感；
- NPU 单模型性能不能预测 W1+W2+W3 并发 Frame Age；
- thermal throttling 可能同时影响多个 workload。

## 2.3 当前主要 Bottleneck Hypothesis

这是待验证假设，不是事实结论：

1. shared DDR / memory copy；
2. CPU latency-sensitive W2/W6；
3. multi-camera ingest + NPU + map 并发；
4. thermal steady-state；
5. Camera lane/sync 实际板级实现。

---

# 3. Route B — Jetson Orin SoM + External FCU

## 3.1 第一版职责分配

```text
6 Camera / SerDes
  ↓
Jetson Camera / multimedia path
  ↓
Shared LPDDR
  ├─ W2 VIO / Visual Odometry → CPU/GPU/Isaac ROS implementation
  ├─ W3 Detection / Stereo Depth → GPU/DLA implementation-dependent
  ├─ W4 Nvblox / Local Map → GPU/CPU
  ├─ W6 Planner → CPU/GPU implementation-dependent
  └─ Codec / ROS graph
  ↓
FCU / W9
```

注意：
- 不把所有 Isaac ROS workload 都强行指定到某一种 engine；
- engine placement 必须以具体 graph / implementation 为准。

### Evidence

现有证据是四条路线中最接近 C2 组合的一类：

- 物理多 Camera Nova/Perceptor；
- Multicam VSLAM；
- DNN stereo/depth；
- Nvblox；
- Isaac ROS 5.0 graph/component latency；
- 真实 UAV/robotics CASE。

但仍缺：
- 本项目 6×1072×1280 actual mode；
- target detection model；
- W2+W3+W4+W6 exact concurrent P99；
- 本项目 power/weight/cooling。

## 3.2 Memory / Data Path

主要为 shared-memory integrated path：

```text
Camera
→ shared memory
→ CUDA / TensorRT / Isaac ROS consumers
→ map/planner
```

主要风险不是 PCIe accelerator round-trip，而是：

- GPU/CPU/memory concurrency；
- graph queue / Frame Age；
- power mode；
- thermal；
- carrier/camera adaptation。

---

# 4. Route C — Qualcomm IQ-9075 + External FCU / RT Subsystem

## 4.1 第一版职责分配

```text
CSI / GMSL Camera
  ↓
qrb_ros_camera
  ↓
DMA-BUF / shared LPDDR
  ├─ W2 SLAM / localization → ROS/CPU/GPU path, exact allocation TBD
  ├─ W3 NN → QNN / Hexagon Tensor path
  ├─ W4 mapping/depth → implementation-dependent
  ├─ W6 Nav2 / planning → CPU path
  └─ RT subsystem → optional W9 supporting role
  ↓
External FCU retained in baseline
```

### Evidence

- up to 16 concurrent Camera capability；
- Camera/CSI/GMSL；
- DMA-BUF transport；
- QNN / NN inference reference；
- ROS SLAM / Nav2 reference；
- partner multi-stream video+DNN benchmark；
- 4-core RT subsystem。

### 重要边界

Partner multi-stream benchmark 表明：
- 即使 AI engine 有较高峰值算力；
- 多流系统仍可能由 CPU/decode/scheduling 先成为约束。

所以 IQ-9075 的 C2 判断重点不是 100 TOPS，而是：

```text
physical camera
+ DMABUF
+ W2
+ W3
+ W4
+ W6
+ tail latency
```

## 4.2 当前主要 GAP

- physical 6-camera hardware synchronization；
- Camera→QNN P95/P99；
- visual VIO/SLAM quantitative latency；
- W2+W3+W4+W6 concurrency；
- project-specific SWaP；
- RT subsystem 与 external FCU 的最终职责边界。

---

# 5. Route D — RK3588 Host + PCIe/M.2 AI Accelerator + External FCU

## 5.1 第一版职责分配

```text
6 Camera
  ↓
RK3588 MIPI / ISP / VPU
  ↓
Host DDR
  ├─ W2 VIO/SLAM → RK3588 CPU/GPU
  ├─ W4 Local Map → RK3588 CPU/GPU
  ├─ W6 Planner → RK3588 CPU
  │
  └─ W3 preprocessing
        ↓
       PCIe
        ↓
     Accelerator
     M50 / Metis / Hailo
        ↓
     inference result
        ↓
       PCIe
        ↓
     Host fusion/planning
        ↓
       FCU
```

W7 如后续正式进入，可考虑放入 accelerator，但不是当前 C2 baseline。

## 5.2 这里的关键不是“额外 TOPS”

外挂 accelerator 主要可能卸载：

```text
W3
(+ optional W7)
```

它**不会自动改善**：

- Camera input；
- ISP/VPU；
- W2 VIO；
- W4 Map；
- W6 Planner；
- W9 Flight Control。

因此评价 Route D 必须回答：

> W3 offload 后，RK3588 Host 对 W1/W2/W4/W6 的余量是否足够？

## 5.3 两个 Memory Domain

抽象数据路径：

```text
Host Camera/ISP
→ Host DDR
→ preprocessing
→ H2D / PCIe
→ accelerator runtime / device memory domain
→ D2H / result
→ Host DDR / CPU
→ planner
```

这里不能假设 M50、Metis、Hailo 内部 memory architecture 完全相同。

因此通用 Resource Map 只记录：
- Host DDR；
- PCIe/interconnect；
- accelerator runtime/device memory domain；
- H2D/D2H；
- queue。

具体 SKU 再单独记录。

## 5.4 子路线证据边界

### D1 — RK3588 + M50/LQ50

已确认：
- RK3588+M50 组合产品路线存在；
- M50-compatible xh2 有 YOLO 模型级 benchmark；
- LQ50 M.2 有板级规格。

仍缺：
- live Camera→Host→PCIe→M50→Host Frame Age；
- T_H2D / T_D2H；
- total system power / thermal；
- 与 W2/W4/W6 同时运行。

### D2 — RK3588 + Metis

已确认：
- Axelera 官方 ARM Host 列表包含多款 RK3588；
- NanoPC-T6 有厂商团队 benchmark；
- Voyager 支持 profiler；
- double buffering 能 overlap transfer/compute，但会增加 result frame delay。

因此：
> throughput optimization 不能自动当成 UAV low-latency optimization。

### D3 — RK3588 + Hailo

已确认：
- Hailo 已有 ARM Host / camera / multisource 路线；
- HailoRT 可测 hw-only latency / FPS / power；
- 真实机器人/UAV视觉案例存在。

仍缺：
- RK3588 exact host path；
- live multi-camera E2E P99；
- W2/W3 conflict；
- total power。

---

# 6. 四条路线的“资源责任”对比

| Workload / Resource | RK3588 | Jetson Orin | IQ-9075 | RK3588 + Accelerator |
|---|---|---|---|---|
| W1 Camera/ISP | RK3588 | Jetson | IQ-9075 | **RK3588 Host** |
| W2 VIO/SLAM | RK3588 CPU/GPU | Jetson CPU/GPU | IQ-9075 host compute | **RK3588 Host** |
| W3 Detection | RK NPU | GPU/DLA path | QNN/HTP path | **Accelerator** |
| W4 Map | RK CPU/GPU | Jetson GPU/CPU | implementation dependent | **RK3588 Host** |
| W6 Planning | RK CPU | CPU/GPU by implementation | CPU/Nav2 | **RK3588 Host** |
| W9 Flight control | External FCU | External FCU | External FCU baseline / RT subsystem optional | External FCU |
| Primary image memory | Host LPDDR | Shared LPDDR | Shared LPDDR / DMABUF | **Host LPDDR first** |
| Extra PCIe inference crossing | No | No | No for integrated NN | **Yes** |
| Main system-level unknown | concurrent Frame Age | exact project P99/SWaP | physical camera+VIO P99 | H2D/D2H + Host headroom |
| Software integration boundary | single main stack | single main stack | single main stack + QRB ROS/QNN | **host stack + accelerator SDK** |

---

# 7. 现在可以得出的工程判断

## 7.1 Integrated 路线

三个 Integrated 候选的共同问题是：

> 不同 workload 竞争 shared CPU/GPU/NPU/DDR 后，P99 是否仍满足 deadline？

所以统一 Benchmark 应重点测：

```text
W1
→ W1+W3
→ W1+W2+W3
→ W1+W2+W3+W4+W6
```

而不是单独跑 YOLO。

## 7.2 Host + Accelerator 路线

Route D 的额外问题是：

```text
T_H2D
+ T_accel_queue
+ T_infer
+ T_D2H
```

以及：
- W3 offload 后 Host 是否真正释放；
- Host preprocess 是否反而成为瓶颈；
- PCIe data movement 是否增加 Frame Age；
- 总功耗/板面积/散热是否仍满足 UAV。

## 7.3 当前不能做的结论

现在仍不能说：
- Integrated 一定低延迟；
- Host+Accelerator 一定高延迟；
- Jetson 一定比 RK3588 适合；
- IQ-9075 100 TOPS 一定比 RK3588 6 TOPS 强；
- M50 160 TOPS 一定能让 RK3588 系统满足 C2。

因为 Project Nominal 和 concurrent P99 尚未冻结/验证。

---

# 8. 下一步：从 Resource Map 进入 Validation Matrix

下一层不再继续画架构图，而是对每条路线定义统一验证：

1. W1 ingest/sync；
2. W3 model baseline；
3. W1+W3；
4. W1+W2+W3；
5. W1+W2+W3+W4+W6；
6. Frame Age P50/P95/P99；
7. drop/deadline miss；
8. CPU/GPU/NPU/DDR；
9. power/temperature；
10. Host+Accelerator 单独测 H2D/D2H；
11. FCU interface + vehicle response；
12. 30/60/120 min thermal steady state。

配套见：
`cases/six-camera-uav/phase-2-validation-plan.md`
