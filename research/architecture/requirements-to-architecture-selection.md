# 从任务需求到端侧计算架构：需求驱动选型方法

- 状态：v0.1
- 日期：2026-09-30
- 阶段：Phase 2 — Requirement & Architecture Synthesis
- 目的：把 Phase 1 已建立的场景、工作负载、Benchmark 和平台证据转化为可复用的系统架构决策方法
- 原则：不做 TOPS 排名，不在证据不足时给平台打分

## 1. 阶段切换理由

Phase 1 已经建立：
- 跨 UAV / UGV / USV / Robot / Fixed Edge 的应用事实矩阵；
- W1–W9 工作负载分类；
- W1–W8 定量公共基线；
- 平台事实表与公开 Benchmark 表；
- 平台—工作负载证据矩阵；
- Host+Accelerator 与一体 SoC 的证据边界；
- 六摄像头 Case 的数据入口模型与闭环时延模型；
- 关键 GAP 的负证据审计。

当前继续公开资料搜索的边际收益下降，尤其缺少：
- 多 workload 并发 P95/P99；
- physical multi-camera → perception → planning Frame Age；
- Host↔Accelerator H2D/D2H；
- 长时间功耗/热稳态。

这些数据通常需要厂商内部资料或实机测量。因当前无法实测，Phase 2 的目标改为：

> **用已经确认的事实建立需求参数、资源预算和架构门槛；把未确认项保留为变量，而不是继续用低可信度资料填空。**

---

## 2. 需求向量

任何目标系统先形成一个 Requirement Vector：

```text
R = {
  Mission,
  Sensors,
  DataRate,
  Synchronization,
  WorkloadSet,
  Concurrency,
  UpdateRate,
  Deadline,
  Memory,
  I/O,
  SWaP-C,
  Safety,
  Software,
  Productization
}
```

### 2.1 Mission

至少明确：
- 平台：UAV / UGV / USV / Robot / Fixed Edge；
- 任务：巡检、导航、避障、测绘、操作、协同等；
- 环境：室内/室外、GNSS可用性、动态障碍、光照/天气；
- 人类参与：遥控、监督、自主执行；
- 失效后果与降级策略。

### 2.2 Sensors

必须用真实输入描述：
- Camera 数量、分辨率、FPS、format；
- IMU / LiDAR / Radar / GNSS；
- hardware trigger / timestamp；
- SerDes / MIPI / Ethernet；
- 是否需要录像/编码。

### 2.3 WorkloadSet

使用本仓库 W1–W9，而不是一个“总 AI 算力”：
- W1 Sensor / Video
- W2 Localization / SLAM
- W3 DNN Perception
- W4 Mapping / World Model
- W5 Prediction / Tracking
- W6 Planning / Optimization
- W7 VLM / LLM / VLA
- W8 Multi-Agent / Fleet
- W9 Safety / Control Supervision

必须记录实际并发关系，例如：

```text
W1(always)
+ W2(always)
+ W3(4 cameras @ 15Hz)
+ W4(10Hz)
+ W6(20Hz)
+ W7(on-demand)
```

而不是“系统支持 W1–W7”。

---

## 3. 先算数据，再算 AI

### 3.1 W1 Camera 数据率

```text
PixelRate = Σ(N_i × W_i × H_i × FPS_i)

Payload = Σ(PixelRate_i × bytes_per_pixel_i)
```

必须继续区分：
- Sensor effective payload；
- MIPI/SerDes physical link；
- ISP output；
- DDR image-plane traffic；
- codec traffic；
- AI tensor traffic。

### 3.2 DDR 预算

```text
BW_DDR,working ≈
Σ(image/tensor bytes × effective read/write passes)
+ SLAM/map traffic
+ codec
+ OS/runtime
```

不能用 LPDDR 理论峰值直接判定“够”。

推荐输出：
- steady-state GB/s；
- burst；
- copy count；
- zero-copy coverage；
- margin。

### 3.3 W3 推理调用率

```text
InferenceRate_total =
Σ(N_model_stream × inference_hz)
```

然后再绑定：
- model；
- input；
- precision；
- per-inference latency；
- throughput；
- pre/post processing；
- accelerator utilization。

TOPS 只作为最后的硬件规格解释之一。

### 3.4 W2/W4/W6

传统算法/优化负载必须单独预算：
- CPU thread/core time；
- GPU compute；
- map memory；
- update rate；
- WCET / tail latency；
- synchronization dependency。

NPU TOPS 不能替代这些资源。

### 3.5 W7

至少预算：
- model weights；
- activation/workspace；
- KV cache；
- visual encoder；
- TTFT；
- token/s；
- 与实时 W2/W3/W6 的资源隔离。

---

## 4. Deadline 不是模型延迟

实时闭环使用：

```text
T_total =
T_sample
+ T_sensor/ISP
+ T_queue
+ T_preprocess
+ T_W2/W3/W4
+ T_W6
+ T_command
+ T_vehicle
```

对于避障：

```text
T_pipeline,max =
(D_detect - D_keepout - D_maneuver)/v
- 1/f_sensor
- T_vehicle
```

平台比较必须问：
- P95/P99 Frame Age 是否小于 `T_pipeline,max`；
- deadline miss 是否可接受；
- 并发后是否仍满足；
- 热稳态下是否仍满足。

单模型 FPS 不直接回答以上问题。

---

## 5. 七个架构决策门槛

### Gate A — Sensor / I/O Fit

先淘汰：
- Camera lane/CSI/SerDes 不足；
- ISP/VPU 不匹配；
- PCIe/以太网/CAN 不够；
- hardware synchronization 无法实现。

这是硬门槛，不能靠 TOPS 弥补。

### Gate B — Real-Time Partition

明确：
- flight/motion control 是否由 MCU/FCU/real-time subsystem 承担；
- Linux companion 是否允许进入硬实时控制链；
- failure/degradation path。

通常“高性能 Linux SoC + 独立实时控制器”与“单 SoC 全承担”是不同产品架构，不应只比较 AI 算力。

### Gate C — Memory Capacity & Bandwidth

要求：
- OS + model + activation + camera buffers + map + queues + margin 能装下；
- steady DDR traffic 不逼近不可持续区域；
- zero-copy 能否覆盖关键图像路径。

### Gate D — Compute Engine Fit

分别判断：
- CPU 是否承担 W2/W6；
- GPU 是否承担 VIO/depth/BEV；
- NPU 是否覆盖目标算子；
- ISP/VPU 是否卸载视频；
- accelerator 是否只解决 W3/W7。

### Gate E — Concurrency & Tail Latency

真正判定：
- W1+W2+W3；
- W2+W4+W6；
- W1+W3+W7；
- 目标组合的 P95/P99、Frame Age、drop。

没有数据时标 GAP，不按单任务 Benchmark 外推。

### Gate F — SWaP / Thermal

必须看：
- steady power；
- peak；
- heatsink/fan；
- thermal throttling；
- mass / volume；
- mission energy。

无人机尤其需要转换为：
```text
Wh/mission
```
和散热重量。

### Gate G — Software / Productization

包括：
- Linux/RTOS；
- ROS2；
- ONNX/PyTorch；
- SDK maturity；
- model conversion；
- operator coverage；
- OTA/diagnostics；
- supply；
- cost；
- temperature；
- domestic sourcing；
- lifecycle。

---

## 6. 四类常见系统架构

这些是**部署架构类型，不是能力等级**。

### A. Integrated Heterogeneous SoC / SoM

```text
Sensors
→ ISP/VPU
→ shared DDR
→ CPU/GPU/NPU
→ planning
→ FCU/MCU
```

代表研究对象：
- Jetson Orin
- IQ-9075
- RK3588

适合重点研究：
- multi-camera；
- shared-memory/zero-copy；
- W2+W3+W4+W6 concurrent；
- SWaP。

风险：
- shared DDR contention；
- Linux jitter；
- accelerator scheduling；
- thermal coupling。

### B. Host + AI Accelerator

```text
Sensors
→ Host ISP/VPU
→ Host preprocessing
→ PCIe accelerator
→ Host fusion/planning
→ FCU/MCU
```

代表研究对象：
- RK3588 + LQ50/M50
- RK3588 + Metis
- RPi5 + Hailo

适合：
- W3/W7 需要额外算力；
- Host 已能承担 W1/W2/W6；
- 产品希望计算可扩展。

关键风险：
- H2D/D2H；
- Host preprocess；
- PCIe；
- total system power；
- extra board area；
- Frame Age。

### C. Real-Time Controller + Companion Compute

```text
FCU/MCU: control / safety
        ↕
Companion: vision / VIO / mapping / planning / AI
```

UAV/robotics 中应优先作为系统安全边界研究，而不是让高性能 AI SoC 直接替代 flight controller。

### D. Edge-Cloud / Fleet Split

端侧保留：
- state estimation；
- safety perception；
- local planning；
- control。

边缘/云承担：
- global optimization；
- long-term analytics；
- map/fleet；
- heavy VLM/LLM；
- model update。

适用于 W8、部分 W7，不适合把安全闭环强依赖于不稳定链路。

---

## 7. 参考 workload composition

以下是“组合模板”，不是 L1–L5 等级。

| Composition | 现实对应场景 | Workload |
|---|---|---|
| Multi-Camera Analytics | 固定视频分析/工业视觉 | W1+W3+W5 |
| Visual Autonomy | UAV GNSS拒止、AMR视觉导航 | W1+W2+W3+W4+W6+W9 |
| Multi-Sensor Autonomy | Robotaxi/高阶UGV/USV避碰 | W1+W2+W3+W4+W5+W6+W9 |
| Foundation-Model Augmented Robotics | VLM/VLA机器人 | 基础自主栈 + W7 |
| Cooperative Autonomy | swarm/fleet | 单机自主栈 + W8 |

这样可以避免重新发明一个假的“自主等级”，同时给平台资源建模提供重复使用的 workload composition。

---

## 8. 平台判断输出格式

最终不输出单一总分。

每个平台输出：

| Dimension | Requirement | Evidence | Status | Gap |
|---|---|---|---|---|
| Sensor I/O | ... | SPEC/REF | Pass/Unknown | ... |
| W1 | ... | BENCH | ... | ... |
| W2 | ... | PAPER/BENCH | ... | ... |
| W3 | ... | BENCH | ... | ... |
| DDR | ... | SPEC/INFER | ... | ... |
| Tail latency | ... | BENCH/GAP | ... | ... |
| SWaP | ... | SPEC | ... | ... |
| Software | ... | REF/CASE | ... | ... |

Status 只能来自 Requirement 与 Evidence 的对应关系：
- Confirmed-fit
- Candidate
- Unverified
- Constraint
- Not-applicable

禁止把这些状态转换为综合排行榜。

---

## 9. Phase 2 输出物

本阶段计划形成：

1. 通用 Requirement Vector；
2. Resource Budget 模型；
3. Architecture Gate；
4. workload composition 模板；
5. 六摄像头 Case requirement card；
6. 六摄像头第一版架构候选；
7. 最终报告第 4–7 章的事实底稿。

Phase 1 的 GAP 搜索改为按需触发：
> 只有当某个 GAP 会阻塞具体架构决策时，才继续搜索或等待实测。
