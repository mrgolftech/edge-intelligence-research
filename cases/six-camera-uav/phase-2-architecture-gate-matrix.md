# 六摄像头 UAV：候选架构 Gate Matrix v0.1

- 日期：2026-09-30
- 基础 workload：C2 Visual Autonomy
- 目的：用需求与证据判断架构状态，不做综合评分或平台排名
- 状态词：
  - **Candidate**：已有与该 Gate 直接相关的公开证据，可进入下一轮验证；
  - **Unverified**：有部分能力证据，但缺本项目关键条件；
  - **Requirement-missing**：平台可能有能力，但项目门槛尚未冻结；
  - **Constraint**：已知会引入明确架构约束；
  - **N/A**：不适用。

## 1. 候选路线

A. RK3588 Integrated SoC + FCU  
B. Jetson Orin Integrated SoM + FCU  
C. Qualcomm IQ-9075 Integrated SoC + FCU  
D. RK3588 Host + M.2/PCIe AI Accelerator + FCU

D 的 Accelerator 可进一步分：
- M50/LQ50
- Metis
- Hailo

当前不在 D 内部做排名。

---

## 2. Gate Matrix

| Gate | RK3588 | Jetson Orin | IQ-9075 | RK3588 + Accelerator |
|---|---|---|---|---|
| A Sensor / I/O | **Unverified** | **Candidate** | **Candidate** | **Unverified**（取决于Host） |
| B Real-Time Partition | **Candidate + external FCU** | **Candidate + external FCU** | **Candidate + external FCU / RT subsystem** | **Candidate + external FCU** |
| C Memory Capacity | **Requirement-missing** | **Requirement-missing** | **Requirement-missing** | **Requirement-missing** |
| C DDR / Data Movement | **Unverified** | **Candidate/Unverified** | **Candidate/Unverified** | **Constraint + Unverified** |
| D W2/VIO | **Candidate** | **Candidate** | **Candidate/Unverified** | **Candidate on RK3588 Host** |
| D W3/DNN | **Candidate** | **Candidate** | **Candidate** | **Candidate** |
| D W4/Mapping | **Candidate/Unverified** | **Candidate** | **Candidate/Unverified** | **Host-dependent / Unverified** |
| D W6/Planning | **Candidate/Unverified** | **Candidate/Unverified** | **Candidate** (Nav2 REF) | **Host-dependent / Unverified** |
| E Concurrent P99 | **Unverified** | **Unverified** | **Unverified** | **Unverified** |
| F Power/Thermal | **Requirement-missing** | **Requirement-missing** | **Requirement-missing** | **Constraint + Requirement-missing** |
| G Software | **Candidate** | **Candidate** | **Candidate** | **Candidate / higher integration complexity** |

这张表不是“好坏比较”，而是当前证据成熟度与架构风险地图。

---

## 3. Gate A — Sensor / I/O

### RK3588

公开规格确认：
- multiple MIPI CSI inputs；
- dual ISP；
- video codec。

但当前仍未用高等级证据确认：
- 本项目 6×Camera 同时 ingest；
- actual lane mapping；
- six-camera sync；
- 1072×1280×actual FPS 六路 steady state。

因此：**Unverified**。

### Jetson Orin

公开证据：
- AGX Orin up to 6 physical / 16 virtual CSI cameras；
- Nova Carter 物理 multi-camera system；
- hardware synchronization / timestamp 证据。

所以 Gate A 可进入 **Candidate**。

但实际 GMSL/MIPI carrier、camera electrical adaptation 仍需工程设计。

### IQ-9075

公开：
- up to 16 cameras；
- CSI/GMSL；
- QRB ROS Camera；
- per-frame timestamp propagation；
- DMA-BUF path。

所以 Gate A 为 **Candidate**。

但本项目真正需要的 multi-camera hardware trigger/sync 仍未确认，因此不是 Confirmed-fit。

### RK3588 + Accelerator

Camera 仍先进入 RK3588 Host。

因此外挂 M50/Metis/Hailo **不会改善 Camera input Gate**。

状态继承 RK3588 Host：**Unverified**。

这是 Host+Accelerator 架构非常重要的一条判断。

---

## 4. Gate B — Real-Time Partition

当前六摄像头 UAV 应把：
- flight control；
- actuator loop；
- failsafe

与 Linux AI workload 分开建模。

因此四条候选路线第一版都采用：

```text
Compute platform
↕
FCU / real-time controller
```

而不是用 Linux NPU SoC 替代 FCU。

IQ-9075 自带 real-time subsystem 是平台能力，但本项目是否使用它承担哪些 W9 职责仍未冻结。

所以它不能自动等于“不需要 FCU”。

---

## 5. Gate C — Memory / DDR

### Memory Capacity

当前项目尚未冻结：
- model；
- VLM；
- map；
- recording buffers；
- software runtime。

所以所有路线都是 **Requirement-missing**。

即使 Orin 64GB 或 IQ-9075 up to 36GB 已知，也不能因此判断“够”。

### DDR

公开资料对峰值带宽/架构有所描述，但本项目实际：
- image passes；
- zero-copy；
- VIO/map；
- model tensor；
- codec

都未冻结。

所以不做 Pass。

Host+Accelerator 额外引入：
- Host DDR；
- H2D；
- D2H；
- PCIe queue。

因此标记明确 **Constraint**，但 Constraint 不等于“不适合”。

---

## 6. Gate D — Compute Engine

### RK3588

证据：
- W3：official RKNN benchmark；
- W2/W4：published SLAM system；
- multi-context/core API。

因此是 Candidate。

但 W2+W3 concurrent 仍缺。

### Jetson

证据最接近 C2：
- multi-camera VSLAM；
- DNN stereo；
- Nvblox；
- current graph latency。

因此各 workload 可进入 Candidate。

但没有本项目 exact composition P99，因此仍不是 Confirmed-fit。

### IQ-9075

证据：
- W3 multi-stream partner benchmark；
- W2/W6 official ROS references；
- Camera/DMABUF；
- benchmark harness。

所以是 Candidate。

W2/W4 quantitative latency 仍弱于 Jetson 当前公开证据。

### Host + Accelerator

这里必须拆职责：

```text
RK3588 Host: W1 + W2 + W4 + W6
Accelerator: mainly W3 (+ optional W7)
```

所以它的价值取决于：
> W3 offload 后，Host 是否能稳定完成 W2/W4/W6，并且 PCIe/data movement 没有破坏 Frame Age。

当前只能 Candidate/Unverified。

---

## 7. Gate E — Concurrent Tail Latency

这是目前四条路线共同最大的 GAP。

没有一条公开资料与本项目同时满足：
- 6×1072×1280 actual FPS；
- target detection；
- target VIO；
- target depth/map；
- target planner；
- same power mode；
- P95/P99 Frame Age。

因此全部标：
**Unverified**。

这也是未来实测最有价值的一项。

---

## 8. Gate F — SWaP/Thermal

当前产品 requirement 没有冻结：
- max compute power；
- mass；
- volume；
- cooling；
- mission endurance penalty。

所以不能据平台 TDP 直接 Pass/Fail。

Host+Accelerator 的结构性 Constraint：
- additional board/module；
- PCIe；
- regulator；
- cooling；
- mass。

但是否超限必须等产品门槛。

---

## 9. Gate G — Software

### RK3588
RKNN + Linux multimedia 已有生态，但 ROS/robotics integration 更多依赖集成方/社区。

### Jetson
JetPack / CUDA / TensorRT / DeepStream / Isaac ROS 路径完整。

### IQ-9075
Qualcomm Linux/Ubuntu + QRB ROS packages + QNN 路径明确。

### Host+Accelerator
Host 软件 + Accelerator SDK 双栈：
- RK multimedia / ROS；
- Houmo / Voyager / Hailo runtime。

因此集成边界更多，标记：
**Candidate / higher integration complexity**。

这不是性能评价，而是工程工作量事实。

---

## 10. 当前架构判断

当前证据足以得出：

1. **四条路线都还有研究价值，没有证据支持现在直接淘汰其中一条。**
2. Jetson/IQ-9075 在多传感器/机器人软件 Reference 上公开证据更完整，但不等于满足本项目 SWaP。
3. RK3588 成本/集成形态有现实吸引力，但 C2 的并发 Frame Age 是核心未知。
4. RK3588+Accelerator 只解决“W3/W7 扩展”，不能替代 RK3588 对 W1/W2/W4/W6 的责任。
5. 目前真正阻止架构收敛的不是 TOPS，而是：
   - actual FPS / algorithm topology；
   - closed-loop deadline；
   - power/mass；
   - concurrent P99。

因此下一步应优先冻结 Requirement，而不是增加候选芯片。
