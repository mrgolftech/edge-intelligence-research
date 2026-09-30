# 六摄像头 UAV：Camera → Workload Routing Matrix

- 状态：v0.1
- 日期：2026-09-30
- 基础 Composition：C2 Visual Autonomy
- 目的：显式描述 6 路 Camera 如何分配给 W1/W2/W3/W4，而不是默认“六路都跑同一算法”
- 配套：
  - `data/calculations/six-camera-camera-workload-routing.csv`
  - `research/workloads/six-camera-perception-topology-envelope.md`

## 1. 用集合表示 Camera 路由

定义物理 Camera 集合：

```text
C = {C0, C1, C2, C3, C4, C5}
|C| = 6
```

当前**不假定** C0–C5 的物理朝向，也不假定哪两路能够形成有效 stereo pair。

为不同 workload 定义子集：

```text
V ⊆ C   # VIO / SLAM cameras
P ⊆ C   # per-view perception cameras
F ⊆ C   # fused multi-view perception cameras
D ⊆ C   # depth / stereo cameras
R ⊆ C   # record / encode cameras
```

这些集合允许重叠。

例如同一 Camera 可以同时进入：
- W2 VIO；
- W3 detection；
- W4 depth。

这意味着“物理 Camera 数 = 6”与“算法消费 view 数”是两个不同变量。

---

## 2. Workload Routing Matrix

| Workload | 输入 | 当前 Project | Benchmark Baseline | 证据/依据 |
|---|---|---|---|---|
| W1 Capture | `C` | 6 路确认；FPS pending | 6× observed geometry @20/30Hz | 项目观测 + 公开参考 |
| W2 VIO/SLAM | `V ⊆ C` | pending | `|V|=2` stereo first | EuRoC/TUM stereo；Nova multi-camera VSLAM |
| W3 PER_VIEW | `P ⊆ C` | pending | `|P|=2/4/6` | 多流独立 detector 是现有常见部署形式 |
| W3 FUSED_MULTI_VIEW | `F ⊆ C` | pending | `|F|=6` analysis profile | BEVFormer 等 multi-view fused perception |
| W4 Depth | `D ⊆ C` | pending | 一个有效 stereo pair first | Hawk/Nova stereo depth |
| W4 Local Map | depth/state output | pending | 不直接指定 Camera 数 | Nvblox / local mapping 路线 |
| W6 Planning | map/state | pending | deadline-driven | EGO/PX4 类规划/闭环模型 |
| W9 Control | planner command | external FCU baseline | independent RT loop | 当前系统架构原则 |

---

## 3. 为什么 Camera Sets 必须允许重叠

假设：

```text
V = {C0, C1}
D = {C0, C1}
P = {C0, C1, C2, C3, C4, C5}
```

这不意味着 C0/C1 被物理采集三次。

真实情况更像：

```text
Camera DMA buffer
   ├─ VIO consumer
   ├─ depth consumer
   └─ perception consumer
```

因此需要区分：

1. **capture write**；
2. **consumer read / preprocessing**；
3. **zero-copy / shared buffer**；
4. **derived tensor / depth / feature traffic**。

同一源 frame 被多个 workload 使用时，系统压力主要来自 fan-out 与后续处理，而不是新增 Camera link。

---

## 4. Camera Fan-out 的分析量

为了在没有实机 profiler 时比较路由复杂度，引入：

```text
ViewConsumptionRate =
Σ(N_views_workload × workload_update_hz)
```

如果为了 sensitivity 假设每个 consumer 都完整读取一次 source NV12 frame：

```text
FullSourceReadEquivalent =
ViewConsumptionRate × SourceFrameBytes
```

再加一次 capture write：

```text
ImagePlaneOnePassEquivalent =
CaptureWrite
+ FullSourceReadEquivalent
```

**这不是 DDR 实测，也不是 DDR 下限。**

原因：
- VIO 可能读取 grayscale/缩小图；
- ISP/scaler 可能直接产生不同输出；
- zero-copy 可减少 copy；
- cache/tiling 改变实际 traffic；
- GPU/NPU tensor 和 map traffic 尚未加入；
- 同一 depth result 可能被 W4/W6 复用。

它只是用于：
> 比较不同 Camera routing/topology 的“全源图像一遍式数据搬运量级”。

---

## 5. Routing Template P — PER_VIEW

```text
C: 6 Camera capture

V:
selected stereo/VIO views

P:
2 / 4 / 6 independent perception views

D:
selected stereo pair

W4 map:
consume depth/state

W6:
consume map/state
```

W3 调用率：

```text
ModelCalls/s =
|P| × PerViewHz
```

PER_VIEW 的优势/风险不能只看 model：
- 每路 pre/postprocess 独立；
- model call 数随 `|P|` 线性增加；
- 多 stream queue/scheduler 变得重要；
- Host+Accelerator 时会出现更多独立 H2D/queue transactions。

---

## 6. Routing Template F — FUSED_MULTI_VIEW

```text
C: 6 Camera capture

V:
selected VIO views

F:
multiple Camera views into one fused model call

D:
optional separate depth branch

Fused model:
cross-view / temporal fusion
→ unified representation / detection / BEV
```

调用率：

```text
ModelCalls/s = FusedUpdateHz

InputViews/s =
|F| × FusedUpdateHz
```

如果 `|F|=6`、20Hz：

```text
20 model calls/s
120 input views/s
```

因此 fused topology **降低的是 model-call count 语义，不是 Camera 输入率本身**。

---

## 7. FUSED 会改变 W3/W4 边界

BEVFormer 一类模型同时包含：
- multi-camera perception；
- cross-view fusion；
- temporal state；
- BEV/world representation。

因此它并不只是“把 6 个 YOLO 合成 1 个 YOLO”。

对资源预算来说更接近：

```text
W3 perception
+
part of W4 world representation
```

所以：

- PER_VIEW 路线可以把 W3、depth、local map 分开预算；
- FUSED/BEV 路线往往把部分 W4 compute/memory 吸收到模型内部；
- 单纯比较“calls/s”会严重误导。

---

## 8. 当前仍不能决定具体 Camera ID

需要项目侧冻结：

- 六路实际物理朝向；
- overlap/FOV；
- baseline；
- 哪些 Camera 能做 stereo；
- rolling/global shutter；
- hardware sync；
- VIO 视场需求；
- obstacle coverage。

在这些信息进入仓库之前，只使用集合表达，不写：
- C0/C1 一定是前双目；
- C2–C5 一定做环视 detection；
- 六路一定都进入 fused perception。

---

## 9. 对四条候选架构的直接影响

### RK3588 Integrated
- PER_VIEW 主要压力：NPU call rate + Host preprocess + shared DDR；
- FUSED 路线是否可部署取决于目标 fused model 的 RKNN/operator/engine 支持，当前不能假定。

### Jetson Orin
- PER_VIEW 与 fused Transformer/BEV 都有 GPU/TensorRT 类实现空间；
- 但必须用目标模型验证，不能从 GPU 理论算力推导。

### IQ-9075
- PER_VIEW 多流 DNN 已有较强公开证据；
- fused multi-view / BEV exact model 的公开定量证据需要另外建立。

### RK3588 + Accelerator
- PER_VIEW 更符合当前 M50/Metis/Hailo 公开 W3 evidence；
- fused multi-view 是否能有效卸载要看具体 accelerator operator/model 支持；
- 即使 accelerator 支持，Camera/VIO/Map/Planner Host 责任仍然存在。

---

## 10. 当前工程判断

1. 六摄系统的算力需求首先取决于 **Camera-to-workload routing**，不是 Camera 数本身。
2. `N_capture=6` 不能推出 `N_detection=6`。
3. `N_detection=6` 也不能推出每周期 6 次 inference，因为可能是 fused multi-view。
4. PER_VIEW 与 FUSED 可能拥有接近的 input-view rate，却有完全不同的 model-call granularity 与模型内部状态。
5. 因此后续平台 Benchmark 必须先固定 R25 topology，再解释 FPS/TOPS。
