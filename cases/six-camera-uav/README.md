# 六摄像头无人平台视觉系统 Case Study

- 状态：Baseline v0.3
- 日期：2026-09-30

## 研究目的

将六摄像头无人平台作为本仓库的核心工程案例，用真实系统需求逐级推导端侧计算资源，而不是从芯片参数反向定义需求。

## 当前能力演进路径

```text
六路摄像头采集与同步
        ↓
视频采集与图像处理
        ↓
目标检测与跟踪
        ↓
图像拼接 / 多摄像头融合
        ↓
深度估计 / 障碍物检测
        ↓
自主避障
        ↓
VIO / SLAM
        ↓
自主导航
        ↓
VLM / 多模态场景理解
```

## 当前已确认

- 系统以六路摄像头为主要视觉输入；
- 既往单路媒体链路已观测到 **1072×1280、NV12** downstream output；当前尚不能确认六路全部为同一 mode/FPS；
- 需要研究多路同步采集；
- 需要完成视频采集和处理；
- 后续目标包括检测、融合、障碍检测和避障；
- VIO / SLAM / 自主导航作为进一步能力演进方向；
- VLM / 多模态理解属于更高层能力，不视为当前基础能力的必选项。

## 尚未冻结的关键输入

以下参数在进行定量算力推导前必须明确：

| 参数 | 当前状态 |
|---|---|
| 每路分辨率 | 单路已观测 1072×1280；六路一致性待确认 |
| 每路帧率 | 待确认 |
| 像素格式 | 单路 downstream 已观测 NV12；Sensor RAW 待确认 |
| 是否同时编码录像 | 待确认 |
| 六路同步误差指标 | 待确认 |
| 检测模型及输入尺寸 | 待确认 |
| 跟踪算法 | 待确认 |
| 拼接/融合方式 | 待确认 |
| 深度估计方案 | 待确认 |
| 避障最大允许延迟 | **改为由速度/探测距离/车辆响应反推；当前待冻结任务参数** |
| VIO/SLAM 输入相机数量 | 待确认 |
| 目标功耗预算 | 待确认 |
| 尺寸/重量约束 | 待确认 |

禁止在这些输入没有明确前直接得出“需要 XX TOPS”的结论。

## 公开参考负载档位

在实际 Camera mode 未冻结前，使用公开系统/数据集做参考量级，不把其当成项目指标：

| 参考 | Camera/图像配置 | 六路等效 Pixel Rate | 用途 |
|---|---|---:|---|
| EuRoC MAV | 752×480 @20Hz | 43.315 MP/s | MAV/VIO 低分辨率参考 |
| TUM VI | 1024×1024 @20Hz | 125.829 MP/s | VIO 高分辨率参考 |
| nuScenes | 6×1600×900 @12Hz | 103.680 MP/s | 原生六 Camera 感知参考 |
| NVIDIA Hawk | 1920×1200 @30Hz | 414.720 MP/s | 高分辨率机器人参考 |
| NVIDIA Hawk | 1920×1200 @60Hz | 829.440 MP/s | 高帧率压力档 |

详见 `research/workloads/six-camera-reference-load-profiles.md`。

注意：Hawk 是双目模块，一个模块含两个同步 imager；表中的“六路等效”按 **六个 image streams** 算术缩放，不是六个 Hawk 模块。

## 后续工作负载模型

将按以下方式建立计算链路：

### Stage A：采集与预处理

需要量化：

- 六路原始输入带宽
- ISP负载
- 图像格式转换
- 内存读写带宽
- 编码/录像吞吐
- CPU占用

### Stage B：实时环境感知

加入：

- 检测
- 跟踪
- 分割/深度（按实际需求）
- 多摄像头融合

需要量化：

- 单模型延迟
- 六路并发方式
- 批处理是否适用
- NPU/GPU占用
- 前后处理时间
- 内存带宽
- 端到端延迟

### Stage C：定位与自主导航

加入：

- VIO / SLAM
- 障碍地图
- 路径规划
- 避障

重点量化：

- CPU / GPU负载
- IMU/Camera同步
- ROS2节点并发
- 地图内存
- 端到端闭环延迟
- 与视觉模型并发时的性能退化

### Stage D：高级认知

按明确任务价值决定是否加入：

- VLM
- 场景理解
- 自然语言任务
- Agent/任务规划

重点不是继续叠加 TOPS，而是测试：

- 模型可装载容量
- TTFT
- Token吞吐
- 多模态输入延迟
- 与实时感知任务共存情况

## 避障闭环时延预算

已新增：
- `research/workloads/avoidance-latency-budget.md`
- `data/calculations/avoidance-timing-fact-anchors.csv`
- `scripts/calc_avoidance_latency_budget.py`

核心判断：
- 不预设“30 FPS”或“100 ms”就是合格；
- 先冻结 flight speed、usable detection range、keep-out distance、vehicle response、acceleration/jerk；
- 再反推 sensor update rate 与 Frame Age P95/P99 deadline；
- planner/DNN 的单模块 latency 只占闭环预算的一部分。

PX4 当前 Collision Prevention 公开资料可作为事实锚点：`CP_DELAY` 明确包含 sensor delay 和 vehicle tracking delay，速度限制还考虑 sensor range、acceleration 和 jerk。

## 第一版 Benchmark 建议

后续至少形成以下可复现实验：

1. 六路视频采集稳定性；
2. 六路视频同时编码；
3. 1/2/4/6 路目标检测扩展曲线；
4. 检测 + 跟踪并发；
5. 检测 + 深度估计并发；
6. VIO/SLAM 独立运行；
7. VIO/SLAM + 多路检测并发；
8. 内存带宽压力测试；
9. 持续功耗与温度测试；
10. 长时间运行稳定性测试。

## 目标

最终得到的不是“某芯片有多少 TOPS”，而是一张类似以下形式的能力映射表：

| 能力阶段 | 工作负载 | CPU | GPU/NPU | 内存/带宽 | I/O | 功耗 | 可选平台 |
|---|---|---|---|---|---|---|---|
| Stage A | 六路采集/处理 | 待测 | 待测 | 待测 | 待测 | 待测 | 待研究 |
| Stage B | 感知 | 待测 | 待测 | 待测 | 待测 | 待测 | 待研究 |
| Stage C | 导航 | 待测 | 待测 | 待测 | 待测 | 待测 | 待研究 |
| Stage D | 高级认知 | 待测 | 待测 | 待测 | 待测 | 待测 | 待研究 |

该表将随着真实测试逐步替换“待测/待研究”。


## Phase 2 Requirement Card

本 Case 已进入“需求→资源→架构”阶段。

当前需求状态与候选架构见：
- `phase-2-requirement-card.md`
- `../../data/calculations/six-camera-requirement-status.csv`

后续不再以“继续搜更多平台”为主线，优先冻结：
`N_detection / N_vio / N_depth / N_record / FPS / flight speed / detection range / SWaP`。


## Phase 2 Composition / Gate Matrix

当前基础 workload composition：
**C2 Visual Autonomy = W1 + W2 + W3 + W4 + W6 + W9**

已增加：
- `phase-2-workload-compositions.md`：Nominal / Peak / Fallback / Optional VLM 工况；
- `phase-2-architecture-gate-matrix.md`：RK3588、Jetson Orin、IQ-9075、RK3588+Accelerator 的证据状态；
- `../../data/calculations/six-camera-architecture-gates.csv`：机器可读 Gate 数据。

当前四条路线均保留为候选/待验证，不做平台排名。


---

## Phase 2 Camera → Workload Routing

新增：

- `phase-2-camera-workload-routing.md`
- `../../research/workloads/six-camera-perception-topology-envelope.md`
- `../../data/calculations/six-camera-camera-workload-routing.csv`
- `../../data/calculations/six-camera-perception-topology-envelope.csv`
- `../../scripts/calc_six_camera_perception_topology_envelope.py`

核心变化：

```text
N_capture = 6
≠
N_vio
≠
N_depth
≠
N_perception
```

W3 继续区分：
- PER_VIEW；
- FUSED_MULTI_VIEW；
- MIXED。

后续平台分析至少保留 P20/P30 与 F20/F30 两类 topology envelope，不能用“六路检测”一个条目覆盖。


## Security / Trust 扩展

六摄像头 Case 已增加安全可信横向需求，不改变 C2 workload 定义：

- [Security Threat Model 与 Trust/Data Flow](security-threat-model-and-trust-flow.md)
- [Security Requirements](../../data/calculations/six-camera-security-requirements.csv)
- [Trust Plane 实现方案](../../research/architecture/trust-plane-implementation-options.md)

规则：
- Security 不是 W10；
- 安全能力与 W1/W2/W3/W4/W6/W9 并发验证；
- 安全机制不得破坏 FCU/W9 实时与 failsafe；
- Integrated SoC 与 Host+Accelerator 均需独立检查 Trust Boundary。
