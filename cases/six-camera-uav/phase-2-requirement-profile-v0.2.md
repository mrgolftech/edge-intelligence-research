# 六摄像头 UAV：Project Nominal Requirement Profile v0.2

- 日期：2026-09-30
- 状态：v0.2
- 基础 Composition：C2 Visual Autonomy
- 性质：项目需求状态 + 公开参考锚点 + Benchmark/Stress 设计
- 公开锚点：`references/webpages/six-camera-requirement-reference-anchors-2026.md`
- 机器可读：`data/calculations/six-camera-requirement-profile-v02.csv`

## 1. 分类

严格分：
- PROJECT_CONFIRMED
- REFERENCE_ANCHOR
- BENCHMARK_BASELINE
- STRESS_ANCHOR

只有 PROJECT_CONFIRMED 是产品需求。

## 2. P0/P1 参数参考状态

| ID | Parameter | Project | Reference Anchor | Benchmark / Stress |
|---|---|---|---|---|
| R04 | actual Camera FPS | PENDING | 12 Hz nuScenes；20 Hz EuRoC/TUM；30 Hz Hawk | 20/30 sensitivity；60 stress |
| R25 | perception topology | PENDING | PER_VIEW 与 FUSED_MULTI_VIEW 都有现实路线 | 两种 topology 都保留 |
| R07 | perception views/streams | PENDING | six-view fused perception 已有公开路线 | PER_VIEW 2/4/6；FUSED 记录 views/call |
| R08 | model/input/precision | PENDING | 640×640 INT8 YOLO-family 多平台有证据 | 横比必须 exact same model/input/precision |
| R09 | perception update/call rate | PENDING | 10/12/20/30 Hz 出现在不同 context | 10/20/30 test grid |
| R10 | VIO topology | PENDING | EuRoC/TUM stereo；Nova multi-camera VSLAM | stereo 2-view baseline |
| R11 | depth topology | PENDING | Hawk stereo；Nova multi-stereo depth | 1 stereo pair first |
| R12 | local map | PENDING | EGO 5–5.5 m 配置锚点 | 只做参考 |
| R13 | planner | PENDING | planner compute 与 schedule/sensor rate需分开 | 按 closed-loop deadline 定 |
| R15 | flight speed | PENDING | 3.56 / 4.0 / 4.5 m/s | 7.8 m/s stress |
| R16 | usable obstacle range | PENDING | EGO 5 m 仅为算法配置 | 必须项目验证 |
| R17 | keep-out | PENDING | 无可迁移固定值 | 项目定义 |
| R18 | vehicle response | PENDING_MEASURE | PX4 0.1–0.5 s | flight-log measurement |
| R19 | compute power | PENDING_PRODUCT | 无可迁移行业值 | 产品冻结 |
| R20 | mass/volume/cooling | PENDING_PRODUCT | 无可迁移行业值 | 产品冻结 |
| R21 | mission energy | PENDING_PRODUCT | 无可迁移行业值 | mission+measured W |
| R23 | VLM | optional | 现实路线但非 C2 必需 | baseline OFF |

## 3. W3 公式修正

### PER_VIEW

```text
InferenceRate_total =
Σ(N_view × PerViewHz)
```

### FUSED_MULTI_VIEW

```text
ModelCallRate =
PerceptionUpdateHz

InputViewRate =
N_views_per_call × PerceptionUpdateHz
```

例：
6 views/call × 20 Hz = 20 model calls/s，但输入 view-image rate = 120 images/s。

不能写成 120 次 model inference/s。

### MIXED
按 branch 分别预算。

因此新增 R25 perception_topology。

## 4. Reference Operating Points

### RP-A
6×1072×1280 NV12 @20 Hz sensitivity：
- 164.659 MP/s；
- image-plane ≈246.99 MB/s。

### RP-B
6×1072×1280 NV12 @30 Hz sensitivity：
- 246.989 MP/s；
- image-plane ≈370.48 MB/s。

### SP-C
6×1072×1280 NV12 @60 Hz stress：
- 493.978 MP/s；
- image-plane ≈740.97 MB/s。

全部不是 Project Nominal。

## 5. W3 Benchmark 设计

先冻结：
```text
PerceptionTopology
Model
Input
Precision
N_views
UpdateHz
Preprocess
Postprocess
```

公开资料说明 640×640 INT8 是现实的 benchmark 起点，但现有 model variant 不一致。

规则：
1. 优先 exact same model；
2. input 先考虑 640×640；
3. precision 先考虑 INT8；
4. 同时测 single call、PER_VIEW 2/4/6；
5. fused multi-view 仅在目标算法采用时测试；
6. exact model 不统一时不做定量横排。

## 6. W2/W3/W4 不必使用相同 Camera 集合

```text
N_capture = 6

W2:
selected VIO views

W3:
PER_VIEW selected views
or FUSED multi-view

W4:
selected depth/map source
```

公开事实支持：
- EuRoC/TUM：stereo VIO；
- Nova：multi-camera VSLAM + stereo depth；
- BEVFormer：multi-view fused perception。

后续 architecture diagram 必须显式画 camera-to-workload routing。

## 7. Flight Speed 使用方式

公开真实 UAV 锚点：
- EGO-Planner 3.56 m/s；
- PX4 4 m/s；
- FOAM 4.5 m/s；
- FASTER 7.8 m/s。

本项目分析可写：
```text
REFERENCE CLUSTER ~3.5–4.5 m/s
HIGH-DYNAMIC STRESS 7.8 m/s
```

这是对公开事实的工程汇总，不是行业等级。

## 8. Range / Keep-out

EGO 的 5 m depth filter、5.5 m local update range 仅为实现配置，不能把 R16 写成 5 m。

PX4 CP_DIST 是 vehicle-specific。

因此 R16/R17 继续保留为 Project GAP。

## 9. SWaP 方向不能反过来

正确方向：
```text
Aircraft / Mission
→ allowed power / mass / volume
→ candidate architecture
```

禁止：
```text
candidate platform spec
→ redefine product requirement
```

R19/R20/R21 继续 PENDING_PRODUCT。

## 10. 当前 Benchmark Profiles

### BP1 W1
- 6×observed geometry；
- 20/30 Hz；
- 60 Hz stress；
- sync/drop/frame-age。

### BP2 PER_VIEW W3
```text
views = 2 / 4 / 6
update = 10 / 20 / 30 Hz
```
仅为 test grid。

### BP3 VIO
- stereo 2-view first；
- hardware timestamp/sync；
- 20 Hz reference；
- 再按实际 architecture 扩 multi-camera。

### BP4 Full C2
必须等 project speed/range/keep-out/vehicle response 冻结后，反解 deadline 再生成。

## 11. 仍需产品侧冻结

Product/Mission：
- nominal/max avoidance speed；
- allowed compute power；
- compute mass/size；
- mission duration。

Camera/Mechanical：
- six-stream actual mode/FPS；
- geometry；
- valid stereo pairs；
- sync tolerance。

Algorithm：
- PER_VIEW / FUSED / MIXED；
- detection baseline；
- VIO camera set；
- depth method；
- map/planner。

完成这些后，才能构造真正的 Project Nominal C2 Resource Envelope。
