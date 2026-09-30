# Dragonwing IQ-9075：实时控制与机器人证据

- 日期：2026-09-30
- 状态：verified-public-evidence

## 1. 官方平台事实

来源：
- https://www.qualcomm.com/internet-of-things/products/iq9-series/iq-9075
- https://www.qualcomm.com/developer/hardware/qualcomm-iq-9075-evaluation-kit-evk

已确认：
- 50 / 100 dense INT8 TOPS SKU
- 8-core Kryo CPU
- Adreno 663 GPU
- dual Hexagon Tensor Processor
- 4-core real-time MCU subsystem
- up to 36GB LPDDR5 with ECC
- up to 16 concurrent cameras
- 2.5GbE TSN / CAN-FD / PCIe
- Ubuntu / Qualcomm Linux
- Llama 2 7B up to 22 tokens/s（厂商规格页）
- application positioning includes robotics / AMR / drones

这些属于 SPEC / VENDOR_BENCH，不等于 VIO/SLAM benchmark。

## 2. acontis EtherCAT partner benchmark

来源：
https://www.qualcomm.com/support/partner/blog/acontis-iq9

日期：2026-06-22

测试条件：
- Dragonwing IQ-9075
- EC-Master
- Linux CLOCK_MONOTONIC real-time scheduling
- target cycle: 1 ms
- full send/receive/application workload
- 7 EtherCAT slaves
- 512-byte process data

公开结果：
- continuous stable round-trip ≈100 μs
- jitter: single-digit μs，文章标题称 under 8 μs

### 工程含义
这是 W9/real-time control support 的量化证据，说明 IQ-9075 不能只当“100 TOPS NPU”来看，它还具备经过实际测试的实时工业控制路径。

### 限制
- 来源属于 Qualcomm Partner Network 上的合作伙伴实测；
- EtherCAT timing ≠ 飞控控制环 WCET；
- 不等于 ISO 26262 / DO-178C 等安全认证；
- 没有给出 AI perception + planning + EtherCAT 全满载并发情况下的资源占用。

因此矩阵升级为 PARTNER_BENCH，而不是“安全控制已完全验证”。
