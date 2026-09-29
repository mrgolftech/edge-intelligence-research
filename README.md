# Edge Intelligence Research

面向无人装备与边缘智能场景的端侧智能计算研究仓库。

本仓库不以“收集算力卡参数”或“按 TOPS 排名”为目标，而是建立一套可复用的工程分析方法：

> **应用场景 → 智能任务 → 数据/算法负载 → 算力与系统资源需求 → 计算架构 → 芯片/模组/产品 → 系统解决方案**

## 研究目标

围绕无人机、无人车、无人船、机器人、多摄像头智能设备和固定式边缘感知设备，回答以下问题：

1. 端侧到底需要完成哪些智能任务？
2. 这些任务产生怎样的数据流与算法负载？
3. CPU、GPU、NPU、内存、带宽、ISP、视频编解码和 I/O 分别需要承担什么？
4. 不同智能能力等级下，功耗、散热、尺寸、重量和软件生态有哪些约束？
5. SoC、一体化异构计算、GPU 平台和外接 AI 加速卡分别适合什么场景？
6. 哪些芯片、模组和产品能够实现这些能力？
7. 纸面参数无法判断时，应如何通过 Benchmark 和实验验证？

## 当前研究主线

### 1. 无人装备智能能力分级

当前暂采用以下项目内部分析框架：

| 等级 | 能力定位 | 典型任务 |
|---|---|---|
| L1 | 基础视觉处理 | 图像采集、ISP、编解码、预处理、轻量视觉 |
| L2 | 实时环境感知 | 检测、跟踪、分割、深度估计、多摄像头融合 |
| L3 | 定位与自主导航 | 光流、VO/VIO、SLAM、障碍地图、避障、路径规划 |
| L4 | 高级感知与多模态 | Transformer、BEV、VLM、复杂场景理解 |
| L5 | 任务级智能 | VLM/LLM/Agent/VLA、任务理解、规划与工具调用 |

> 注意：L1–L5 是本项目用于组织需求和工作负载的研究框架，不是行业标准，也不预设固定 TOPS 门槛。

详见：[无人装备端侧智能应用场景与能力分级](research/scenarios/unmanned-intelligence-scenarios.md)

### 2. 六摄像头无人平台 Case Study

当前核心工程案例为六摄像头无人平台视觉系统，按以下路径逐级研究：

**六路采集与同步 → 视频处理 → 检测/跟踪 → 多摄像头融合 → 深度/障碍检测 → 避障 → VIO/SLAM → 自主导航 → VLM/多模态理解**

详见：[六摄像头无人平台 Case](cases/six-camera-uav/README.md)

## 研究方法

平台评估不能只看 TOPS。至少同时分析：

- CPU 架构与通用计算性能
- GPU / NPU / AI ASIC 及支持的数据精度
- 内存容量、内存带宽和 Cache
- ISP、多路视频编解码和摄像头接入
- PCIe、Ethernet、CAN、USB、MIPI 等 I/O
- 功耗、散热、尺寸、重量
- Linux / ROS2 / PyTorch / ONNX / 厂商 SDK 生态
- 模型转换、算子覆盖和实际部署难度
- 供货、成本与国产化
- 实际模型性能与整机并发性能

始终区分：

> **理论算力 ≠ 单模型 Benchmark ≠ 真实系统性能**

## 仓库结构

目录按真实研究进展逐步创建，不维护空目录。

```text
AGENTS.md                         # Agent 工作基线
README.md                         # 项目导航

research/
  scenarios/                     # 应用场景与能力分级
  workloads/                     # 工作负载模型
  architecture/                  # 系统/计算架构
  chips/                         # 芯片研究
  vendors/                       # 厂商研究
  products/                      # 模组/板卡/整机
  algorithms/                    # 算法负载
  trends/                        # 技术趋势

references/
  datasheets/
  papers/
  reports/
  webpages/
  github/

data/
  product-specs/
  benchmarks/
  calculations/

cases/
  six-camera-uav/

comparisons/
reports/
assets/
scripts/
```

## 当前已落盘研究

- [AGENTS.md](AGENTS.md)：项目方法、证据规范、文件规范与 Agent 工作规则
- [无人装备端侧智能应用场景与能力分级](research/scenarios/unmanned-intelligence-scenarios.md)
- [六摄像头无人平台 Case](cases/six-camera-uav/README.md)
- [PX4 计算机视觉资料摘要](references/webpages/px4-computer-vision.md)
- [NVIDIA Isaac ROS 资料摘要](references/webpages/nvidia-isaac-ros.md)
- [Nav2 自主导航资料摘要](references/webpages/nav2-navigation.md)
- [OpenVLA 论文摘要](references/papers/openvla.md)
- [六摄像头工作负载模型](research/workloads/six-camera-workload-model.md)
- [端侧计算平台产品数据模型](data/product-specs/schema.md)

## 当前工程判断

1. 端侧算力需求必须由具体任务链路推导，不能从某个产品的 TOPS 倒推。
2. 无人系统负载通常是多传感器、多模型和传统算法并行，不是单一神经网络推理问题。
3. 从 L2 到 L3 后，CPU、传感器同步、低时延数据通路和定位导航软件栈的重要性明显提高。
4. 从 L3 到 L4/L5 后，模型参数规模、内存容量与带宽的重要性快速增加，TOPS 更不足以单独代表能力。
5. VLM/LLM/Agent 目前应优先研究其在场景理解、任务规划、人机交互和高层决策中的价值，不应未经验证直接替代安全关键的实时控制链路。
6. 六摄像头案例将作为平台需求推导和 Benchmark 设计的主要工程基线。

## 下一阶段

近期优先推进：

1. 冻结六摄像头工作负载关键输入：分辨率、帧率、像素格式、同步、目标延迟和算法基线；
2. 基于工作负载模型进行第一轮数据率、内存带宽和计算负载推导；
3. 分路线研究 RK3588、NVIDIA Jetson、后摩智能、Axelera AI、地平线、黑芝麻、昇腾等平台；
4. 按统一产品数据模型建立首批平台数据；
5. 设计第一版多路视频 + 检测 + SLAM/VIO Benchmark。

---

研究和提交规范以 [AGENTS.md](AGENTS.md) 为准。
