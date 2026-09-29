# 端侧计算平台产品数据模型

- 状态：v0.1
- 日期：2026-09-29
- 用途：统一后续芯片、SOM、开发板、加速卡和整机平台的调研口径

## 1. 原则

产品数据库不是 TOPS 排行榜。

所有记录必须区分：

- 芯片 / SoC
- SOM / 核心板
- 开发板
- PCIe / M.2 / MXM 加速卡
- 工业计算机 / 边缘计算盒
- 边缘服务器

同一厂商的不同产品形态不得直接混为一行比较。

未知参数统一写：

`未确认`

不得根据同系列其他产品推测补齐。

---

## 2. 建议字段

### 身份信息

| 字段 | 说明 |
|---|---|
| vendor | 厂商 |
| product_name | 产品名称 |
| product_type | 芯片/SOM/开发板/加速卡/整机 |
| base_chip | 核心芯片 |
| release_date | 发布时间 |
| lifecycle | 在售/量产/开发中/EOL/未确认 |
| region | 厂商/供应链区域 |
| domestic_status | 国产化说明 |

### 计算

| 字段 | 说明 |
|---|---|
| cpu_arch | CPU架构 |
| cpu_cores | 核数/配置 |
| cpu_notes | CPU性能说明 |
| gpu_arch | GPU架构 |
| gpu_compute | GPU公开性能 |
| npu_arch | NPU/AI ASIC |
| int4 | INT4能力 |
| int8 | INT8能力 |
| fp16 | FP16能力 |
| bf16 | BF16能力 |
| fp32 | FP32能力 |
| compute_definition | 厂商计算口径说明 |
| sparsity_condition | 是否依赖稀疏等条件 |

### 内存

| 字段 | 说明 |
|---|---|
| memory_capacity | 容量 |
| memory_type | LPDDR/DDR/HBM等 |
| memory_bus | 位宽/通道 |
| memory_bandwidth | 官方带宽 |
| memory_ecc | ECC情况 |

### 视觉与视频

| 字段 | 说明 |
|---|---|
| isp | ISP能力 |
| camera_interfaces | MIPI CSI/GMSL/FPD-Link等 |
| camera_count | 官方支持路数 |
| camera_bandwidth | 摄像头接口总带宽 |
| video_decode | 解码能力 |
| video_encode | 编码能力 |
| supported_codecs | H.264/H.265/AV1等 |

### I/O

| 字段 | 说明 |
|---|---|
| pcie | PCIe版本/通道 |
| ethernet | Ethernet能力 |
| usb | USB |
| can | CAN/CAN-FD |
| uart_spi_i2c | 低速接口 |
| storage | eMMC/UFS/NVMe/SD等 |

### 软件生态

| 字段 | 说明 |
|---|---|
| os | Linux/Ubuntu/其他 |
| sdk | SDK名称/版本 |
| pytorch | 支持方式 |
| onnx | ONNX支持 |
| ros2 | ROS2支持 |
| inference_runtime | TensorRT/厂商Runtime等 |
| model_compiler | 模型转换工具 |
| operator_coverage | 算子覆盖信息 |
| container | Docker/容器支持 |
| llm_support | LLM能力 |
| vlm_support | VLM能力 |

### 工程属性

| 字段 | 说明 |
|---|---|
| power_mode | 功耗模式 |
| measured_power | 实测持续功耗 |
| dimensions | 尺寸 |
| weight | 重量 |
| cooling | 散热方案 |
| operating_temp | 工作温度 |
| availability | 供货情况 |
| price | 公开价格/询价情况 |

### Benchmark

| 字段 | 说明 |
|---|---|
| benchmark_model | 模型 |
| precision | 精度 |
| input_shape | 输入尺寸 |
| batch | Batch |
| fps | FPS |
| latency | 延迟 |
| power_during_test | 测试功耗 |
| software_version | 软件版本 |
| benchmark_source | 官方/第三方/自测 |
| reproducible | 是否可复现 |

### 证据

| 字段 | 说明 |
|---|---|
| source_url | 原始链接 |
| source_title | 文档标题 |
| source_type | datasheet/manual/blog/paper/community |
| source_version | 文档或SDK版本 |
| access_date | 获取日期 |
| evidence_status | 已确认事实/厂商宣称/工程推断/待验证 |
| notes | 限制和备注 |

---

## 3. 对比规则

跨平台比较时，至少保证：

1. 产品形态一致或明确注明差异；
2. 精度一致；
3. 模型一致；
4. 输入尺寸一致；
5. Batch一致；
6. 功耗模式明确；
7. 软件版本明确；
8. 稀疏/稠密口径明确；
9. 是否包含前后处理明确；
10. 官方结果与自测结果分开。

无法统一口径时，应写“不可直接比较”，而不是强行排序。

---

## 4. 与场景和工作负载的映射

后续每个产品除参数外，还应给出基于证据的适配分析：

- Sensor I/O / Video
- Classical Estimation / VIO / SLAM
- DNN Perception
- 3D / Mapping / BEV
- Planning / Optimization
- Learned Planning / E2E
- Foundation Model / VLM / LLM / VLA
- Multi-Agent / Collaboration
- Safety-Critical / Real-Time Control Support

并记录其适用平台形态和任务场景，例如 UAV、UGV、USV、AMR、操作机器人、固定边缘节点。

判断的是“该平台在给定任务、环境、工作负载和 SWaP-C 约束下是否具备实现条件”，不是给产品打统一能力分。

---

## 5. 下一步

后续建立正式 CSV/JSON 数据表时，以本 schema 为字段基线；如调研中发现字段不足，先更新本文件再扩展数据集。
