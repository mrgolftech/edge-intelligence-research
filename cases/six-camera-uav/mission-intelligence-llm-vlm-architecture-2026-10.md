# 六摄像头无人平台：从视觉避障升级至端侧任务智能的 LLM/VLM 架构研究

- 日期：2026-10-16
- 状态：Architecture Hypothesis / 方案预研，**不是产品确认、实测或飞行验证**
- 相关已有研究：
  - `cases/six-camera-uav/phase-2-requirement-profile-v0.2.md`
  - `cases/six-camera-uav/phase-2-validation-plan.md`
  - `cases/six-camera-uav/security-threat-model-and-trust-flow.md`
  - `research/products/on-device-llm-computing-solutions-2026-10.md`
  - `research/workloads/profiles/w7-vla.md`

## 1. 研究问题

在六摄像头 C2 Visual Autonomy 视觉避障、导航与外部 FCU 基础上，是否需要通过一张端侧 AI 加速卡叠加本地任务级智能？哪些功能必须由大模型完成，哪些功能应保留在确定性控制链？如何量化 W7 的增量资源、实时性、安全与可产品化门槛？

**结论假设**：只有需要开放语义理解、自然语言目标、复杂任务分解/重新规划时才值得引入 LLM；如果直接理解六摄图像的语义，则首先应考虑 VLM（含视觉编码器）而不是仅文本 LLM；路径规划、碰撞规避、FCU 实时控制继续使用确定性算法。端侧 C2 + C4 为正交叠加，C4 不是更高自主等级，也不一定比规则式 Mission Manager 更优。

## 2. “指挥控制与决策”功能边界

| 层 | 典型问题 | 优先方案 | 时效语义 |
|---|---|---|---|
| 实时安全/飞控 | 稳定姿态、执行基础保护 | 外部 FCU / W9；安全仲裁 | 硬实时、独立于 LLM |
| 局部运动与导航 | 障碍/深度、航迹/轨迹、状态估计 | W1/W2/W3/W4/W6 + 控制器 | Frame Age、P99、deadline |
| 行为管理 | 改变巡检路线、复查异常、恢复中断任务 | FSM/Behavior Tree/任务管理器 | 事件触发，状态可验证 |
| 任务级意图/决策 | 自然语言巡检目标、场景语义、任务分解/更新 | 小型 VLM + 可选 LLM/Agent，工具调用 | 低频、异步、可超时 |
| 上级指控与机群 | 权限、任务授权、跨机协同、资源调度 | 地面/边缘指控 + 策略与安全服务，端侧执行代理 | 网络/权限/一致性；不以单机 LLM 代替整体 C2 系统 |

示例（民用巡检）：任务“巡检指定区域、发现设备异常拍照记录、必要时选择替代安全路线、按任务条件返回”。端侧 VLM 将关键帧与结构化感知状态转为语义事件；LLM/Agent 只建议 `reinspect`/`goto_inspection_point`/`request_human_review` 等白名单高层行为；确定性任务管理器执行 geofence、能源余量、避障地图、权限与冲突校验，进而交给 W6/FCU。**禁止自由文本直接驱动姿态/电机控制**。

## 3. 建议数据与控制架构

```text
6 physical cameras + IMU --> Host W1/W2/W3/W4 --> obstacle map, pose, tracked objects, selected timestamped keyframes
                                      |                         |
                                      +--> W6 local planner --> FCU / W9 --> vehicle
                                                               ^
Mission / GCS --> authenticated command / policy ---> Mission Manager / BT / Safety Arbiter
                                                               ^
                         VLM (event-triggered selected frames) -> semantic event
                         LLM (optional) -> structured proposed high-level tasks
```

执行防线：
- LLM/VLM 没有直接访问 FCU 姿态、电机、参数更改 API 的权限；模型只输出 schema-validated proposed action 与证据引用。
- Safety Arbiter 验证地理限制、航迹安全、剩余电量、任务授权、可信状态与时效；冲突、超时、不确定性高则拒绝、延迟或交由人处理。
- 处理含多个摄像头的输入时，明确 Camera Routing：`N_capture=6` 不等于 `N_VLM=6`；建议以 **按事件抽取关键帧/ROI/空间状态** 做 POC，而不是把 6 路 30fps 连续发送到 VLM。
- 任务级大模型异步执行；其排队、视觉编码、prefill、decode 不得阻断 W1–W6 的采集、感知和避障。
- 单机端侧 Mission Manager 不等于完整的“指挥控制系统”；多机/远程指控还需要授权链、通信、态势共享和地面协调。

## 4. 公开证据与限制

| 编号 | 证据 | 说明 | 不可外推 |
|---|---|---|---|
| E01 | PX4 Offboard 官方文档：允许 Companion 经 MAVLink/ROS 2 输出 position/velocity 等设定值，要求控制链保活并设置 failsafe | 支持 Companion/FCU 分工 | Offboard 模式存在 ≠ LLM 可安全直接控制 |
| E02 | VLFly (2025) 用 LLM 指令编码 + VLM goal retrieval + waypoint planner 的分层方法；有仿真与室内外现实导航案例 | 分层 VLM/LLM→planner 有科研依据 | 论文成功 ≠ 工程级安全保证 |
| E03 | GRaD-Nav++ (2025) 声明 fully onboard VLA 并给出真机成功率：训练任务 67%、未见任务 50% | 轻量语言引导动作模型可上机，但鲁棒性仍是问题 | 未知环境下远非 100%，不能直接作安全闭环 |
| E04 | Rockchip `rknn-llm/benchmark.md`：RK3588 Qwen3-VL-2B W8A8 TTFT 383.62ms、decode 14.98 tok/s（文本段，128/64）；448×448 图像编码 2.08s、prefill 649ms、decode 14.91 tok/s（单独 multimodal 表） | 必须分拆视觉编码、prefill、decode；原设备仍需做六摄并发 | 14.98 tok/s ≠ 图像理解 14.98fps |
| E05 | Houmo LQ50 M.2 官方指南：24GB、153.6GB/s、典型 13W、PCIe Gen4 x4 | 模型权重/卡内内存/供电初筛 | 不含 Host、散热、FCU、六路 Camera |
| E06 | Houmo `postmo-modelzoo` release_xh2_v1.3.0：提供 qwen3、qwen3-30b-a3b、qwen2.5-vl、qwen3-vl、detection 例程；警告大模型只能在非 VPU 固件上运行 | 说明软件移植路径存在；**同卡 VPU 视频 + 大模型同时跑存在明确固件兼容疑问** | Model Zoo 示例 ≠ exact LQ50 SKU 全模型/全流程并发 BENCH |
| E07 | NVIDIA Jetson Thor 官方单并发 Qwen2.5-VL 7B 45 tok/s、Qwen3-32B 13.19 tok/s，JetPack7.0、2048/128 | 高性能机器人模型端侧参考 | 文本 decode ≠ 六摄+VIO+避障+VLM 全系统 P99；Thor 不是小型 UAV SWaP 基线 |

## 5. 参数与内存初步边界

裸权重 4-bit 理论下限：
- 2B → 1.0GB；3B → 1.5GB；7B → 3.5GB；14B → 7GB；32B → 16GB；均不含视觉编码器、量化元数据、运行时、KV、图像缓存及其他 C2 常驻任务。
- 实际可运行模型取决于确切 VLM 编码器与 LLM 后端、精度/算子、可用内存、Host DRAM 与 LQ50 板卡内存隔离、PCIe 数据移动，不是看 160TOPS 或 24GB 独立决定。
- 对 25 tok/s 的纯 decode，30 output tokens 的**理想生成时长 1.2s**；未含视觉编码、prefill、排队及调用开销，且 25tok/s 的厂商口径与具体 VLM 尚未绑定。
- 双模型（实时检测 + 语义模型）如分置 RK3588 NPU 和 LQ50 Accelerator，**只是一条可验证架构假设**。需量化 RK3588 的 Camera/ISP/W2/W4/W6 与模型预处理 CPU/DDR 峰值，LQ50 固件、PCIe/SDK、功率、电源峰值与系统热条件。

## 6. POC 路线与候选架构

### P0 — 不加大模型的任务决策基线（必要的对照）
- 在现有六摄 C2 之上新增 FSM/Behavior Tree 的巡检任务（航点进度、异常复查、绕行、任务恢复与超时）。
- 建立任务成功率、事件→决策时延、闭环 Frame Age 和功耗基线。
- 目标：先证明“指挥/行为决策”不等于必须上 LLM。

### P1 — 引入低频 VLM/LLM 的任务智能（优先）
- 2B/3B 左右 VLM（或更小）理解触发式关键帧/裁剪图 + 结构化对象/位置信息；LLM 可选。
- 先在非机载开发环境复现任务识别准确率/幻觉/延迟；再移植到机载 Host 或外挂卡。
- 上层输出：结构化建议动作、区域引用、置信度/不确定度；任务管理器审查后才能执行。
- 当前较可执行的板卡实验假设：`RK3588 + LQ50-24GB`，但必须先向厂商核实非 VPU 固件下的大模型与 RK3588 Host 六路视频方案可以同时工作，且 LQ50 输出进入任务管理的路径能够完成数据拷贝与调用。

### P2 — 扩展 7B/8B 与更复杂 Agent
- 只在小模型任务质量不足，且大模型收益明确时升级。
- 比较同模型、同任务、同量化的 RK3588（若能部署）、RK3588+LQ50、Jetson/机器人 SoM 参考平台。
- 32B/70B/120B 不作为小型 UAV 的默认规格；需要真实任务价值、Host/DDR/系统 SWaP 和 P99 证据。
- VLA 直接 Action 输出属于另一路科研方向，不默认绕过现有安全规划/飞控链。

## 7. 新增验证项目 V13–V18（不改写已有 V01–V12）

| ID | 测试 | 必须记录 | Gate |
|---|---|---|---|
| V13 | Mission Task Manager without LLM | success/recovery, scenario logs, decision latency, action veto | functional baseline |
| V14 | VLM triggered keyframe/ROI | exact model/vision size/image count, image encoder, prefill, decode, first useful result P50/P95/P99, power | W7 capability |
| V15 | LLM structured task proposal | schema compliance, hallucinated entities, invalid action rejection, mission success, human-review rate | safety/policy |
| V16 | W1+W2+W3+W4+W6 **with W7** | C2 Frame Age and deadline misses before/after W7, W2 ATE/RPE, NPU/DDR/PCIe/thermal | real-time noninterference |
| V17 | 30/60/120 min mission co-run | host+board/system power, peak current, throttling, sustained VLM latency, W1–W6 drop | SWaP/thermal |
| V18 | Degraded/security | LLM timeout/crash/incorrect output, bad mission command, accelerator loss, signed-model corruption, compromised node isolation | safe fallback and Trust Plane |

Evidence state at writing: all V13–V18 are **not measured**; any chosen targets will be **PROJECT_TARGET**, not borrowed from product ads.

## 8. 待冻结的需求变量

- 任务属于纯自动巡检、自然语言任务理解，还是要求更复杂的自主重新规划/多机协同？
- 任务层输入：结构化事件/告警，还是必须靠原始视觉语义（VLM）？
- 任务可接受的 VLM 决策延迟、更新频次、最大模型内存与离线任务模式；
- 六路 Camera 实际FPS与同步；N_detection/N_vio/N_depth；FCU 边界；
- 机载允许加算力卡的 **整机功耗、尺寸、重量、散热、航时**；
- RT 安全仲裁、通信/密码模块、权限与失效处理。

## 9. 工程结论

“六目避障 + 算力卡”可作为 C2 Visual Autonomy + C4 Foundation-Model Augmented Robotics 的**候选架构**，但验证顺序必须从 Mission Manager 对照组开始，再证明 VLM 是否提高真实任务完成率，再证明其共运行不破坏 C2 P99，最后才做算力卡 SKU 选型。将 LLM 生成 Token 速度直接当无人机指挥控制能力没有依据。

## References

- [R01] PX4 Offboard Mode，官方：https://docs.px4.io/main/en/flight_modes_fw/offboard
- [R02] PX4 Collision Prevention，官方：https://docs.px4.io/main/en/computer_vision/collision_prevention
- [R03] Zhang et al., *Grounded Vision-Language Navigation for UAVs with Open-Vocabulary Goal Understanding* (VLFly), 2025-06：https://arxiv.org/abs/2506.10756
- [R04] Chen et al., *GRaD-Nav++: Vision-Language Model Enabled Visual Drone Navigation*, 2025-06：https://arxiv.org/abs/2506.14009
- [R05] Sun et al., *AutoFly: Vision-Language-Action Model for UAV Autonomous Navigation in the Wild*, 2026-02：https://arxiv.org/abs/2602.09657
- [R06] Rockchip 官方 RKLLM Benchmark：https://github.com/airockchip/rknn-llm/blob/main/benchmark.md
- [R07] Houmo LQ50 M.2 官方产品说明：https://developer.houmoai.com/hmdoc/m50/hardware-manuals/latest/product-manuals/lq50-m.2/LQ50_M.2_guidelines/intro/index.html
- [R08] 后摩 Model Zoo 固定 release_XH2_v1.3.0：https://github.com/houmo-ai/postmo-modelzoo/blob/release_xh2_v1.3.0/README.md
- [R09] NVIDIA Jetson Benchmarks（Thor JetPack 7.0）：https://developer.nvidia.com/embedded/jetson-benchmarks/
