# NIST ALFUS 参考摘要

- 名称：Autonomy Levels for Unmanned Systems (ALFUS)
- 机构：NIST / ALFUS Working Group
- 主要资料：NIST SP 1011 系列，2003–2008
- 用途：跨无人系统自主性描述的基础参考

## 核心事实

ALFUS 的目标是为不同 unmanned systems 提供通用的自主能力描述/度量框架。

其 Contextual Autonomous Capability 模型以多个方面描述自主性，经典三个方面为：

- Mission Complexity (MC)
- Environmental Complexity (EC)
- Human Independence (HI)

NIST资料强调无人系统能力必须结合任务、环境和人机交互上下文，而不是把所有系统简单放到一个单轴等级中。

早期 ALFUS 还讨论 subsystem / system / system-of-systems 等层次。

## 对本项目的意义

- 不再自创跨 UAV/UGV/USV/robot 的 L1–L5。
- 自主性与计算量分开：自主性高不必然意味着 TOPS 高，固定视频分析算力很高也不等于高自主。
- 用 MC/EC/HI 做“自主性画像”，再独立建立工作负载和硬件需求。

## 原始来源

- https://www.nist.gov/publications/framework-autonomy-levels-unmanned-systems-alfus-0
- https://www.nist.gov/publications/autonomy-levels-unmanned-systems-alfus-frameworkvolume-ii-framework-models-initial
- https://www.nist.gov/publications/autonomy-measures-robots
