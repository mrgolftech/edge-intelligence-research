# W8 Multi-Agent / Fleet / Distributed Workload Profile

- 状态：v0.1
- 日期：2026-09-30

## 证据状态

现有综述已形成稳定问题分类：
- task allocation
- path planning
- collaboration
- optimization / auction / learning / decentralized
- scalability
- uncertainty
- dynamic environment

但本轮没有找到类似 MLPerf、EuRoC 那样被 UAV/AMR/swarm 跨域共同采用的统一硬件 benchmark。

因此不制造固定机器人数量或固定算力门槛。

## 参数化模型

- N = robots
- M = pending tasks
- F_state = state update rate
- F_task = allocation/replanning rate
- S_state = bytes per robot state
- S_map = shared perception/map bytes
- RTT = network latency

```text
StateTraffic ≈ N × F_state × S_state
```

## 工程压力档位

仅用于本项目实验，不是行业标准：
- robots: 4 / 8 / 16 / 32
- tasks: N / 2N / 4N

测：
- allocation latency
- task throughput
- CPU/GPU
- memory
- network latency/bandwidth
- stale-state age
- deadlock/conflict
- failure degradation

## 部署模式

Centralized Fleet：
- edge server
- database/message bus
- stable network

Decentralized/Swarm：
- per-node compute
- peer communication
- local safety autonomy
- distributed optimization

## 结论

多机系统不能按“单机算力 × N”估算；通信拓扑、共享感知量、分配算法和失联策略会改变系统负载。

## References
- https://www.sciencedirect.com/science/article/pii/S2667379724000615
- https://www.sciencedirect.com/science/article/abs/pii/S1574013726000766
- https://www.sciencedirect.com/science/article/abs/pii/S1568494625018113
