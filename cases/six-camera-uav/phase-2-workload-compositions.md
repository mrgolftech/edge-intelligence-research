# 六摄像头 UAV：Phase 2 Workload Composition 与运行工况

- 状态：v0.2
- 日期：2026-09-30
- 基础 Composition：**C2 Visual Autonomy**
- 可选扩展：C4（VLM）/ C5（协同）
- 原则：当前只冻结 workload 结构，不虚构尚未确认的 FPS、模型、功耗和时延数字

## 1. 为什么归入 C2 Visual Autonomy

当前六摄像头项目目标链包括：
- multi-camera capture；
- detection/tracking；
- depth/obstacle；
- VIO/SLAM；
- local planning/avoidance；
- FCU/vehicle control interface。

对应：
```text
W1 + W2 + W3 + W4 + W6 + W9
```

Tracking 若进入正式方案，则增加 W5。

因此它不是单纯 C1 Multi-Camera Analytics。

---

## 2. 三种运行工况

### S1 — Nominal Autonomy

定义：
> 日常自主飞行/导航时长期持续的基础闭环。

结构：
```text
W1:
N_capture = 6
camera ingest / timestamp / sync

W2:
N_vio = TBD
VIO / localization

W3:
N_detection = TBD
obstacle / target perception

W4:
local map if required

W6:
local planning / avoidance

W9:
FCU / safety supervision

W7:
OFF
```

需要冻结：
- actual FPS；
- N_detection；
- N_vio；
- N_depth；
- planner update；
- closed-loop deadline。

### S2 — Peak Mission

定义：
> 感知、导航、记录等任务同时打开时的资源压力工况。

结构可能包括：
```text
S1
+ N_record > 0
+ tracking
+ depth/map
+ higher perception coverage
+ network/storage activity
```

注意：
- 这里不假定 N_record=6；
- 不假定六路全部 detection；
- 不假定六路全部 depth；
- Peak workload 必须由产品任务冻结。

测试目标：
- DDR；
- CPU；
- GPU/NPU；
- Frame Age P99；
- thermal；
- power；
- drop。

### S3 — Degraded / Safety Fallback

定义：
> 资源不足、过温、模型故障、链路故障时仍需保持的最小安全闭环。

建议结构原则：
```text
keep:
W1 minimum sensing
W2 localization as required
W6 local safe action
W9 control/safety

shed first:
W7
noncritical recording
noncritical analytics
mission-level perception not required for immediate safety
```

最终降级顺序必须由系统安全分析确定，当前不固定。

### S4 — Optional Semantic Mission

仅在具体任务证明有价值后启用：

```text
S1 or S2
+ W7 VLM / multimodal understanding
```

此工况必须测试：
- W7 对 W2/W3/W6 P99 的干扰；
- memory residency；
- DDR；
- power/thermal；
- priority/isolation。

---

## 3. 不能把 Nominal 与 Peak 混在一起

平台需求应至少输出：

| Dimension | Nominal | Peak | Fallback |
|---|---|---|---|
| Camera ingest | 必须持续 | 必须持续 | 最小安全集 |
| VIO | 按任务 | 按任务 | 视安全依赖保留 |
| Detection | 按 coverage | 最大任务 coverage | 仅安全必要 |
| Depth/map | 按路线 | 可能开启 | 视安全依赖 |
| Recording | 按需求 | 可能最大 | 优先关闭 |
| VLM | OFF | optional | OFF |
| Deadline | 必须满足 | 必须满足或定义降级 | 必须满足 |
| Thermal | steady | worst case | safe mode |

这样才能回答：
- 平台平时够不够；
- 峰值时会不会排队；
- 资源不足时如何降级。

---

## 4. 第一版资源变量

### W1

```text
PixelRate =
6 × 1072 × 1280 × FPS
```

这里只能把 FPS 保持为变量。

Downstream NV12 image-plane：

```text
Payload =
PixelRate × 1.5 byte/pixel
```

不能把它当 Sensor RAW/MIPI rate 或 DDR 总带宽。

### W3

```text
InferenceRate =
N_detection × detection_hz
```

后续选择 baseline model 后，再映射到公开 benchmark。

### W2

必须冻结：
- N_vio；
- mono/stereo/multi-camera；
- IMU；
- update rate；
- target accuracy；
- synchronization。

### W4/W6

必须由避障架构决定：
- depth source；
- map representation；
- map update rate；
- planner；
- deadline。

---

## 5. Phase 2 当前最小需求冻结集

为了让架构 Gate 开始真正“Pass/Fail”，当前至少还需要冻结：

1. actual FPS；
2. N_detection；
3. detection baseline；
4. N_vio；
5. N_depth；
6. N_record；
7. flight speed；
8. usable obstacle range；
9. keep-out / maneuver requirement；
10. compute power / mass / envelope。

在这些输入未冻结前，平台状态最多只能是 Candidate / Unverified，不能是 Confirmed-fit。


---

## 6. Resource Envelope Bridge

C2 的 workload 结构现在进一步连接到：

- `research/workloads/c2-visual-autonomy-resource-envelope.md`
- `data/calculations/c2-visual-autonomy-reference-envelope.csv`
- `scripts/calc_c2_visual_autonomy_reference_envelope.py`

新增的定量入口：

1. Camera pixel rate；
2. image-plane rate；
3. frame queue memory；
4. W3 invocation/service demand；
5. W2/W4/W6 独立资源；
6. Frame Age；
7. vehicle response；
8. Architecture Gate。

当前项目 1072×1280 NV12 六路只冻结了 geometry/representation，actual FPS 仍为 GAP。因此 20/30/60 Hz 只作为 sensitivity/stress，不作为 Project Nominal。

Project Nominal 仍必须由 Requirement Card 冻结。
