# W1–W9 工作负载分类的定义依据与划分原则

- 日期：2026-09-30
- 状态：v1
- 目的：回答“W1–W9 为什么这样定义”，避免把本项目工作负载分类误认为行业标准或主观拍脑袋。
- 结论：W1–W9 是本项目的 **resource-oriented workload taxonomy（面向资源分析的工作负载分类）**，不是自主等级。

## 1. 外部事实底座

本项目首先比较不同领域已经成熟的功能栈：

- PX4：Optical Flow、VIO、Collision Prevention、Companion Computer；
- Nav2：State Estimation、Environmental Representation、Planning、Control、Behavior；
- Autoware：Sensing、Map、Localization、Perception、Planning、Control、Vehicle Interface；
- Waymo：Where am I / What’s around me / What will happen next / What should I do；
- UAV GNSS-denied 综述：INS、Vision、LiDAR、SLAM、VO、VIO、Kalman Filter、Sensor Fusion；
- Multi-Robot survey：Perception、Planning、Collaboration；
- PaLM-E / RT-2 / OpenVLA：Foundation Model / VLM / VLA；
- PX4/Nav2/Autoware/工业 AMR：Safety/Control/Failsafe/Vehicle Interface。

这些体系的“模块名称”并不完全相同，但存在高度稳定的功能簇。

## 2. 为什么不是照抄某一个功能栈

报告目标不是做软件架构介绍，而是推导硬件资源。

例如 Autoware 的 Perception 可能同时包含 DNN Detection、Occupancy、tracking；从软件功能角度可以都放在 Perception，但从硬件资源角度：
- DNN 主要压 NPU/GPU；
- Occupancy/BEV 主要压 GPU/DDR/temporal state；
- Tracking/Prediction 更依赖历史状态、CPU/GPU。

因此需要对行业功能栈做“资源特征重分组”。

## 3. 九类划分的五条原则

### P1 — 主导资源不同

如果两类任务主要消耗的硬件引擎显著不同，应尽量分开。
例如：
- W1：ISP/VPU/Camera/DDR；
- W2：CPU/GPU + 同步；
- W3：NPU/GPU tensor compute；
- W6：CPU/优化器。

### P2 — 时延语义不同

同样 30 FPS：
- Detection 可以接受一定 pipeline；
- Flight Control 必须强调确定性；
- LLM 更关注 TTFT/tokens/s。

因此 W7、W9 与传统 CV 必须分开。

### P3 — 状态生命周期不同

- W3 Detection 常以 frame 为输入；
- W4 Map/World Representation 长期维护空间状态；
- W5 Prediction 维护时序历史；
- W7 KV Cache 随上下文增长。

这些状态特征直接改变内存预算。

### P4 — 部署与验证方式不同

如果需要完全不同的 Benchmark/验证方法，应独立。
例如：
- W2 用 EuRoC/TUM-VI；
- W3 用统一 DNN benchmark；
- W8 要测网络、协同和 distributed state；
- W9 要测 deadline/failsafe。

### P5 — 能形成独立架构 Gate

分类应能够对平台选择产生实际影响。若拆分后不改变 CPU/GPU/NPU/DDR/I/O/实时性判断，则没有必要新增分类。

## 4. W1–W9 逐项定义理由

| ID | 中文名称 | 为什么单独定义 |
|---|---|---|
| W1 | 传感器输入与视频流水线 | 入口数据吞吐、ISP/VPU、Camera、DMA/DDR 可能先于 AI 成为瓶颈 |
| W2 | 状态估计与定位 | VIO/SLAM/融合具有 CPU/GPU、同步和低延迟特征，不能被 NPU TOPS 替代 |
| W3 | 深度神经网络感知 | 最典型的 tensor/NPU workload，需要模型/精度/编译器口径 |
| W4 | 地图与世界表示 | 长期维护空间状态，Map/BEV/Occupancy 强依赖 memory/DDR |
| W5 | 跟踪、预测与态势理解 | 需要历史时序状态，从“看见”过渡到“理解下一步” |
| W6 | 规划、优化与决策 | 搜索/优化算法关注 worst-case latency，通常 CPU/GPU 主导 |
| W7 | 基础模型/VLM/LLM/VLA | 大模型资源由 model footprint、KV Cache、TTFT、token/action latency 主导 |
| W8 | 多机协同/Fleet | 新增通信、distributed state、task allocation 与可信身份 |
| W9 | 安全监督与控制 | 算力不一定大，但 deadline、确定性、故障隔离和 failsafe 是独立约束 |

## 5. 为什么恰好是九类，而不是七类或十二类

九类不是“自然界唯一正确答案”。

它是当前研究阶段在以下两个目标之间的折中：
1. 足够细，能区分对平台选型真正有影响的资源结构；
2. 足够粗，能够跨 UAV/UGV/USV/AMR/固定边缘复用。

未来如果出现稳定的新资源模式（例如独立 Neuromorphic/Event Camera Pipeline）并且会改变平台架构 Gate，可以扩展 taxonomy；否则不为了“完整”随意增加 W10/W11。

## 6. 与自主等级的区别

W1–W9 没有高低顺序。
- W9 不比 W1“高级”；
- W7 不代表系统自主程度最高；
- 一个固定多摄像头设备可以有很重的 W1/W3/W5，但没有 W2/W6/W9；
- 一个小型飞控系统 W9 很关键，但 AI TOPS 很低。

因此禁止把 W1→W9 画成能力升级阶梯。
