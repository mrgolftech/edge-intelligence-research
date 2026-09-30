# C2 Visual Autonomy：资源与闭环时延证据锚点（2026）

- 日期：2026-09-30
- 用途：为 C2 Visual Autonomy 的资源预算与六摄像头 Case 提供可追溯事实锚点
- 规则：只记录公开事实；项目计算和需求阈值另行标记为 CALC / PROJECT / STRESS

## 1. PX4 Collision Prevention：闭环延迟必须包含传感器与飞行器响应

来源：
https://docs.px4.io/main/en/computer_vision/collision_prevention

已确认事实：

- PX4 使用 `CP_DELAY` 对碰撞预防链中的延迟进行保守估计；
- 文档明确要求同时考虑：
  - sensor delay；
  - vehicle velocity setpoint tracking delay；
- 对外部视觉系统，sensor delay **may be as high as 0.2 s**；
- vehicle tracking delay 典型范围约 **0.1–0.5 s**，并要求从实际飞行日志测量；
- companion/external vision 的初始测试点使用：
  - vehicle speed = **4 m/s**；
  - `OBSTACLE_DISTANCE` = **10 Hz**。

支撑结论：

1. 避障不能只看 DNN inference latency；
2. `sensor → compute → planner → FCU → vehicle response` 才是有效闭环；
3. update rate 与 delay 必须和飞行速度、最小障碍距离一起预算；
4. 4 m/s + 10 Hz 只能作为公开参考工况，不能直接当项目需求。

### 工程算术锚点（CALC，不是 PX4 原文结论）

如果只把：
- external-vision sensor delay = 0.2 s；
- tracking delay = 0.1–0.5 s

相加，则 delay anchor 为 **0.3–0.7 s**。

在 4 m/s 下对应飞行距离：

`D = v × T = 1.2–2.8 m`

如果为了敏感性分析，再额外保守加入一个 10 Hz update period（0.1 s），则为：

- 0.4–0.8 s；
- 1.6–3.2 m。

注意：该“额外 0.1 s”可能与 sensor delay 定义发生部分重叠，因此只做上界敏感性，不作为项目 deadline。

---

## 2. NVIDIA Hawk：高分辨率实时双目输入锚点

来源：
https://nvidia-isaac-ros.github.io/getting_started/sensors/hawk_setup.html

当前 Isaac ROS 文档确认：

- Hawk 为 stereo camera；
- ROS 2 发布：
  - `/left/image_raw`
  - `/right/image_raw`
- 当前 setup 页面给出的发布模式为：
  - **1920×1200 @ 30 fps**。

用途：

- 用于高分辨率机器人视觉 W1 的公开事实锚点；
- 可对“单 image stream”做六路等效算术缩放；
- **不能**写成“六个 Hawk”或“NVIDIA 已验证六路本项目摄像头”。

---

## 3. Isaac ROS 5.0：AGX Orin W3/W4 组件性能锚点

固定版本来源：

https://nvidia-isaac-ros.github.io/v/release-5.0/performance/index.html

AGX Orin 当前公开例子：

- Stereo Disparity Graph，1080p：
  - 117 fps；
  - **9.3 ms @ 30 Hz**；
- DetectNet Object Detection Graph，544p：
  - 73.5 fps；
  - **15 ms @ 30 Hz**；
- RT-DETR SyntheticaDETR Graph，720p：
  - 87.3 fps；
  - **13 ms @ 30 Hz**。

Nvblox 固定版本来源：

https://nvidia-isaac-ros.github.io/v/release-5.0/repositories_and_packages/isaac_ros_nvblox/index.html

Replica / voxel 0.05 m / AGX Orin 的 core component timing：

- TSDF：0.8 ms；
- Color：1.1 ms；
- Meshing：2.3 ms；
- ESDF：1.7 ms。

证据边界：

这些是固定软件版本下的**组件/Graph BENCH**，可以作为 W3/W4 service-time 数量级锚点，但不能：

- 直接相加成完整端到端闭环；
- 外推为六摄像头并发 P99；
- 外推到其他模型、输入、功耗模式或平台；
- 替代 VIO / planning / FCU / vehicle response。

---

## 4. Qualcomm Dragonwing IQ-9075：C2 架构 Gate 的 I/O/RT 事实锚点

官方页面：
https://www.qualcomm.com/internet-of-things/products/iq9-series/iq-9075

官方 Product Brief：
https://docs.qualcomm.com/doc/87-83840-1/87-83840-1_REV_E_Qualcomm_Dragonwing_IQ9_Series_Platform_Product_Brief.pdf

当前确认：

- up to **16 concurrent camera inputs**；
- Camera：**4×4-lane CSI-2**；
- up to **36 GB LPDDR5 with inline ECC**；
- dedicated real-time subsystem：
  - 4 real-time cores；
- SoC-only power range：
  - **3.8–20 W**；
- Ubuntu / Qualcomm Linux；
- 2× PCIe Gen4；
- 2×2.5GbE with TSN。

支撑结论：

这些数据可进入：
- Gate A Sensor/I/O；
- Gate B Real-Time Partition；
- Gate C Memory；
- Gate F Power；
- Gate G Software。

但它们仍然**不能证明**六摄像头 C2 workload 的 W2+W3+W4+W6 并发 P99。

---

## 5. Reference 与 Project Requirement 的边界

本文件只提供事实锚点。

必须继续区分：

- **REF/BENCH**：公开系统与官方 Benchmark；
- **CALC**：本项目从事实参数做的算术；
- **PROJECT**：六摄像头产品真实需求；
- **STRESS**：为了未来测试人为设定的压力点。

禁止把：
- PX4 4 m/s；
- nuScenes 12 Hz；
- TUM VI 20 Hz；
- Hawk 30 fps；
- IQ-9075 16 Camera

自动写成六摄像头项目的产品需求。
