# 当前部署/产品事实：自主系统应用模式

- 获取日期：2026-09-30
- 用途：用当前真实产品/系统验证“应用场景”不是仅来自论文假设
- 证据类型：厂商官方页面；厂商能力声明按“厂商公开事实/宣称”处理，不等于第三方 Benchmark

## 1. Skydio X10 — UAV

来源：
https://www.skydio.com/x10

官方页面当前明确展示：
- autonomous flight
- obstacle/environment understanding
- NightSense
- visible / infrared illumination supporting zero-light navigation

### 支撑结论
商用 UAV 已将视觉环境理解和避障/自主导航放在机载实时系统中。

---

## 2. Waymo Driver — Autonomous Vehicle

来源：
https://waymo.com/waymo-driver/
https://waymo.com/blog/2026/02/ro-on-6th-gen-waymo-driver/

当前官方事实：
- fully autonomous service
- camera + lidar + radar
- onboard computer
- real-time object identification and route planning
- 6th generation Driver 于 2026 年开始 fully autonomous operations
- 6th gen 继续使用多模态 sensing，并将更多 processing 推入 custom silicon

Waymo FAQ将软件问题概括为：
- Where am I?
- What’s around me?
- What will happen next?
- What should I do?

### 支撑结论
自动驾驶计算负载天然包含 localization、perception、prediction、planning，而不是只包含 detection。

---

## 3. MiR250 / MiR Fleet — AMR

来源：
https://mobile-industrial-robots.com/products/robots/mir250/specifications
https://mobile-industrial-robots.com/products/robots

MiR250官方规格：
- indoor autonomous mobile robot
- 2× SICK safety laser scanners
- 2× 3D cameras for pallet / obstacle detection
- 8× proximity sensors
- safety functions
- Wi-Fi / Ethernet

MiR产品页面同时强调：
- dynamic-environment navigation
- MiR Fleet centralized configuration / fleet management
- obstacle avoidance
- multiple pickup/delivery points

### 支撑结论
工业 AMR 是“本机安全导航 + fleet级任务/交通管理”的两层系统。

---

## 4. Saildrone Voyager — USV

来源：
https://www.saildrone.com/platform/voyager

官方页面当前说明：
- 10 m unmanned surface vehicle
- persistent coastal surveillance
- nearshore mapping
- maritime domain awareness
- endurance: 100 days between service stops
- sensor/payload examples: AIS, PTZ IR camera, radar, positioning, ocean/environment sensors
- mapping / surveillance missions

### 支撑结论
USV端侧计算必须考虑长航时、多种 maritime sensors、通信和持续可靠性，而不只是峰值 AI 算力。

---

## 5. Sea Machines SM300 / AI-ris — Maritime Autonomy

来源：
https://sea-machines.com/
https://sea-machines.com/why-sea-machines/solutions/collision-obstacle-avoidance/
https://sea-machines.com/why-sea-machines/solutions/transit-autonomy/

官方当前描述：
- transit autonomy
- remote command
- collaborative autonomy
- collision & obstacle avoidance
- AI-powered vessel vision
- radar + GPS + AIS + electronic chart + computer vision fusion
- obstacle tracking / speed or route change
- COLREG-aware responses

### 支撑结论
USV/船舶自主系统的 perception 和 planning 是多源融合、规则约束和远程协同问题。

---

## 6. NVIDIA Metropolis — Fixed Edge Vision

来源：
https://www.nvidia.com/en-us/autonomous-machines/intelligent-video-analytics-platform/

当前官方应用包括：
- video analytics AI agents
- multi-camera tracking
- automated visual inspection
- intelligent transportation
- industrial automation
- intelligent retail
- robot safety
- VLM/CV models for live/archive video

### 支撑结论
固定边缘设备可能具有很重的 AI/video workload，但没有自身 localization/planning/control，进一步证明“AI算力”和“自主程度”不能混成一个等级。
