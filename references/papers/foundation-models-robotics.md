# Foundation Models / VLM / VLA / Edge Robotics 参考索引

- 获取日期：2026-09-29
- 目的：分析未来无人端侧负载，不把趋势当作当前默认需求

## PaLM-E

ICML 2023，Embodied Multimodal Language Model。

将视觉、连续状态和文本输入纳入语言模型，用于机器人任务、规划、VQA 等。

来源：
https://proceedings.mlr.press/v202/driess23a.html

## RT-2

Google DeepMind，2023。

Vision-Language-Action 模型，将视觉/语言输入转换为机器人动作 token，展示 VLM → VLA 的路线。

来源：
https://deepmind.google/blog/rt-2-new-model-translates-vision-and-language-into-action/

## OpenVLA

2024，开源 7B Vision-Language-Action model。

来源：
https://arxiv.org/abs/2406.09246
https://openvla.github.io/

## NVIDIA GR00T

2025–2026 持续迭代的 humanoid robot foundation model。

N1 使用 VLM reasoning + diffusion action generation；N1.5/N1.6 继续增强语言跟随、泛化与动作策略。

来源：
https://research.nvidia.com/labs/lpr/publication/gr00tn1_2025/
https://research.nvidia.com/labs/gear/gr00t-n1_5/
https://research.nvidia.com/labs/gear/gr00t-n1_6/

## Gemini Robotics / On-Device

Google DeepMind 当前公开 Gemini Robotics VLA/embodied reasoning 产品线，并提供专门针对本地运行、网络约束的 On-Device 模型路线。

来源：
https://deepmind.google/models/gemini-robotics/
https://deepmind.google/models/gemini-robotics/on-device/

## Edge Robotics Survey

2025 综述指出机器人采用 edge computing 的主要动机包括：
- low latency
- mobility
- location awareness
- time-sensitive local processing

同时 cloud robotics 受网络延迟/连接约束，现实系统会采用 device/edge/cloud 分层。

来源：
https://doi.org/10.3390/jsan14040065

## World Models for Autonomous Driving

2025 survey 将 world model 研究覆盖：
- future physical world generation
- behavior planning
- prediction-planning interaction

说明未来自主系统计算负载会从感知进一步进入时空预测、生成和策略。

来源：
https://arxiv.org/abs/2501.11260

## 工程结论

Foundation Model / VLA 是明确的技术趋势，但本项目必须区分：

- 论文研究能力
- 可下载/可运行模型
- 厂商端侧产品支持
- 真实量产使用
- 安全关键闭环适用性

不能因为 VLA 发展快，就默认所有无人机/无人船都需要 LLM。
