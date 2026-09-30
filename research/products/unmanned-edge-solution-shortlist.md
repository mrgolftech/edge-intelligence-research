# 无人装备端侧计算：现成产品/解决方案的架构映射

- 日期：2026-09-30
- 状态：v0.1
- 输入：需求/Workload/Gate 方法 + 2026 产品 Landscape
- 目的：把产品放回系统架构，不做产品排行榜

## 1. 适用于本报告的产品层分类

### A — Integrated Companion Compute

代表产品：
- Jetson Orin NX/AGX 产品体系；
- Qualcomm IQ-9075 EVK / SECO IQ9 / Innodisk EXMP-Q911；
- Firefly RK3588 industrial computers；
- Huawei Atlas 200I A2；
- Firefly BM1688 Core/AIO。

特点：
- CPU + AI engine + video/memory/I/O 高度集成；
- 更适合 W1+W2+W3+W4+W6 在同一主平台编排；
- 主要风险是 shared DDR、软件调度、thermal、Camera/carrier 适配。

### B — Host + Accelerator

代表：
- Firefly AIBOX PRO + Houmo LQ50；
- RK3588 + Axelera Metis；
- Arm/x86 Host + Hailo-10H；
- Cambricon MLU220 M.2。

特点：
- W3/W7 扩展明显；
- Host 继续承担 W1/W2/W4/W6；
- 必须分析 H2D/D2H、Host preprocess、总功耗和散热。

### C — Rugged Robotics / Industrial Computer

代表：
- Seeed reComputer Robotics / Rugged；
- Advantech MIC-733。

特点：
- GMSL/CAN/宽压/工业结构成熟；
- 更接近 UGV/USV/机器人量产形态；
- 重量/尺寸常常不适合小型 UAV。

### D — Adaptive / Deterministic Compute

代表：
- AMD Kria K26/KR260。

特点：
- programmable logic；
- deterministic I/O；
- sensor/industrial protocol acceleration；
- 不以 TOPS 优势取胜。

### E — High-End Physical AI

代表：
- Jetson Thor；
- Intel Core Ultra + Robotics AI Suite；
- 高端 IQ9 / future high-performance modules。

特点：
- C3/C4；
- VLM/VLA/多模型；
- 对小型 UAV 首先检查 SWaP。

---

## 2. 六摄像头 C2 Case 的产品层 Gate

### Camera Gate

最有直接公开 W1 产品证据的候选：

- **Firefly BM1688 Core/AIO**：官方明确 6-channel sensor input；
- **IQ-9075**：SoC up to 16 concurrent Camera；产品模组接口仍需 carrier 级核对；
- **Jetson Orin**：module/platform multi-CSI；第三方 carrier 决定实际物理 Camera；
- **RK3588**：SoC/板卡具备多 Camera 能力，但项目六路 lane/sync 未确认；
- **Atlas 200I A2**：集成 ISP/MIPI，官方明确 UAV/robot applications，但本项目 Camera 组合仍需验证。

因此：
> 产品“能接 Camera”与“满足六路同步”仍是两件事。

### W2/W6 Gate

优先看：
- Jetson + Isaac ROS；
- Qualcomm QRB ROS；
- RK3588 Linux/ROS + 自研；
- Atlas/CANN + ROS integration；
- SOPHGO/BM1688 的机器人软件成熟度。

独立 accelerator 不直接解决。

### W3 Gate

现成选择非常丰富：
- RK3588 NPU；
- Orin GPU/DLA；
- IQ-9075 HTP/QNN；
- Atlas Ascend；
- BM1688 TPU；
- LQ50；
- Metis；
- Hailo；
- MLU220。

这也是为什么“只看 W3”会错误地得出大量平台都可替代的结论。

### W4/FUSED Gate

目前证据明显更集中在：
- Jetson Orin；
- Qualcomm AI Hub/IQ9 路线（仍有 exact support GAP）；
- 车规/高性能 GPU 类平台。

RK3588/BM1688/独立 accelerator 不能仅凭 generic Transformer support 判定。

---

## 3. 面向产品研发的典型组合

### 组合 S — 小型低成本 Integrated

```text
RK3588 / BM1688 Core
+ custom carrier
+ external FCU
```

目标：
- C1 / C2-PER_VIEW；
- 小尺寸；
- 国产化；
- camera/ISP integration。

验证重点：
- 六路实际 Camera；
- sync；
- VIO + DNN concurrency；
- thermal。

### 组合 M — 国产 Host + Accelerator

```text
RK3588 Host
+ LQ50 / other M.2
+ FCU
```

市场已有 Firefly AIBOX PRO 作为 architecture proof。

适合：
- W3 较重；
- optional W7；
- Host 已能承担 VIO/planning。

验证重点：
- Host headroom；
- PCIe；
- H2D/D2H；
- full-system power。

### 组合 R — Robotics Integrated

```text
Orin NX / IQ-9075
+ GMSL/CSI carrier
+ CAN/FCU
```

适合：
- C2/C3；
- ROS2；
- 多 sensor；
- mapping。

代价：
- 成本；
- SWaP；
- 非国产软件/供应链（按项目约束考虑）。

### 组合 D — Domestic Integrated Edge Module

```text
Atlas 200I A2
or BM1688 Core/AIO
+ custom carrier
+ FCU
```

意义：
- 国产化 integrated route；
- ISP/video/AI 同平台。

关键不是峰值 TOPS，而是：
- ROS/VIO/SLAM；
- operator；
- Camera sync；
- developer tooling；
- full-C2 benchmark。

---

## 4. 产品调研结束条件

当前已经覆盖：
- GPU SoM；
- Robotics SoC；
- RK3588 AIoT SoC；
- 国产 integrated module；
- M.2 accelerator；
- FPGA/adaptive SOM；
- industrial/rugged computer；
- Host+Accelerator complete box；
- C4 Physical-AI upper bound。

因此对最终报告第 6 章“主流芯片与产品”和第 7 章“典型配置方案”，产品事实底座已经够用。

后续只在以下情况补产品：
1. 报告具体结论缺少代表产品；
2. 用户/领导指定某型号；
3. 某产品可能改变六摄 Architecture Gate；
4. 出现新的高可信同构 Benchmark。

否则停止继续扩大 SKU 清单，转入最终报告编写。
