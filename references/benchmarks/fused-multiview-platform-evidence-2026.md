# FUSED Multi-View / BEV 平台公开证据审计（2026-09）

- 日期：2026-09-30
- 状态：v0.1
- 目的：为六摄像头 Case 的 `FUSED_MULTI_VIEW` topology 建立平台证据边界
- 规则：PER_VIEW YOLO Benchmark 不得自动外推为 fused multi-view / BEV 性能
- 配套：`data/product-specs/six-camera-topology-platform-evidence.csv`

## 1. Reference Model：BEVFormer

BEVFormer 官方实现证明：

- camera-only；
- multi-camera；
- spatial cross-attention across camera views；
- temporal self-attention；
- unified BEV representation；
- 3D object detection / semantic map segmentation。

官方仓库：
https://github.com/fundamentalvision/BEVFormer

本项目使用它的目的不是指定项目必须采用 BEVFormer，而是证明：

> FUSED_MULTI_VIEW 是一种真实且与 PER_VIEW 明显不同的 workload topology。

它横跨：
- W3 Perception；
- W4 World Representation / temporal state。

---

## 2. NVIDIA Orin：已有官方 fused-BEV 类 TensorRT Benchmark

NVIDIA-AI-IOT 官方：
https://github.com/NVIDIA-AI-IOT/Lidar_AI_Solution/tree/master/CUDA-BEVFusion

公开事实：

- CUDA-BEVFusion 使用 CUDA + TensorRT；
- 数据样例包含 **6 directions Camera images** + LiDAR；
- camera resolution：256×704；
- ResNet50 / TensorRT / FP16：
  - **18 FPS on ORIN**；
- ResNet50-PTQ / TensorRT / FP16+INT8：
  - **25 FPS on ORIN**；
- 仓库注明该性能表使用：
  - TensorRT 8.6；
  - CUDA 11.4；
  - cuDNN 8.6。

### Evidence Status

**BENCH(class) + GAP(exact project)**

它证明：
- Orin 上存在 multi-camera BEV / fused world-representation 的真实 TensorRT 路线和定量性能；

但不能写成：
- 本项目六 Camera BEVFormer = 25 FPS；
- camera-only BEVFormer = 25 FPS；
- 当前 JetPack/Isaac ROS 5.0 下仍为同一结果。

原因：
- BEVFusion 同时包含 LiDAR；
- 输入分辨率不同；
- 模型不是 BEVFormer；
- 软件版本是固定历史栈。

---

## 3. Qualcomm IQ-9075：BEVFormer 已进入 AI Hub 模型目录，但当前元数据存在冲突

Qualcomm AI Hub：
https://aihub.qualcomm.com/models/bevformer

页面当前公开：

- model：BEVFormer；
- technical input：
  - **6 × 3 × 480 × 800**；
- checkpoint：
  - `bevformer_tiny_deformable_optimized_exp_86_epoch_24.pth`；
- model size：120 MB；
- parameters：27M；
- Supported Devices 列表包含：
  - **Dragonwing IQ-9075 EVK**；
- Supported Chipsets 列表包含：
  - **Dragonwing IQ-9075**。

Qualcomm 官方 AI Hub Models：
https://github.com/qualcomm/ai-hub-models

目录同时列出：
- BEVDet；
- BEVFormer；
- BEVFusion；
- CVT 等 Driver Assistance 模型。

### 重要冲突

当前 AI Hub 页面同时显示：

> Not supported / This model is currently not supported on any All Models chipset.

但同一页面又列出 IQ-9075 EVK / IQ-9075。

因此本项目不能把这一页面解释成：
> “BEVFormer 已在 IQ-9075 完成可复现 Benchmark”。

### Evidence Status

**REF/GAP + metadata conflict**

可以确认：
- Qualcomm 官方模型资产已经覆盖 BEVFormer；
- 页面元数据把 IQ-9075 列入 supported device/chipset list；

仍不能确认：
- IQ-9075 的实际 BEVFormer latency/FPS；
- 当前下载 artifact 是否已对 IQ-9075 可用；
- 6-view BEVFormer + physical Camera + W2/W6 concurrency。

后续优先寻找：
- AI Hub 具体 IQ-9075 profile；
- downloadable artifact target；
- QNN operator placement；
- IQ-9075 latency/memory；
- physical Camera→BEV graph。

---

## 4. RK3588：Transformer 软件能力增强，但 exact fused-BEV Benchmark 仍是 GAP

Rockchip 官方 RKNN Toolkit2 / RKNPU2：
https://github.com/airockchip/rknn-toolkit2

当前官方软件栈能够确认：
- RK3588 support；
- ONNX deployment；
- custom operators；
- LayerNorm / Softmax / GELU / MatMul 等相关支持持续优化；
- changelog 明确出现 transformer support optimization。

这说明：
> 不能因为 RK3588 常见 Benchmark 主要是 YOLO，就断言它“不支持 Transformer 类模型”。

但截至本轮定向检索，**未找到 Rockchip 官方 BEVFormer / BEVFusion on RK3588 的条件明确 Benchmark**。

### Evidence Status

**SPEC/INFER + GAP**

必须验证：
- exact model conversion；
- deformable attention / custom op；
- CPU/GPU fallback；
- memory footprint；
- NPU/GPU split；
- latency；
- six-view input data movement。

不能从“支持 Transformer”推出“BEVFormer 可实时运行”。

---

## 5. RK3588 + M50 / Metis / Hailo：PER_VIEW 证据明显强于 fused-BEV

当前已有证据主要集中于：
- YOLO / detection；
- multi-stream；
- LLM/VLM（部分 accelerator）；
- ARM Host integration。

截至 2026-09-30 本轮对官方域/官方 GitHub 的定向检索，未获得：

- Metis BEVFormer / BEVFusion 条件明确 Benchmark；
- Hailo BEVFormer / BEVFusion 条件明确 Benchmark；
- M50/LQ50 BEVFormer / BEVFusion 条件明确 Benchmark。

这不是证明“不能运行”，而是：

> **目前没有足够公开证据把 Route D 的 FUSED topology 提升为 Candidate-fit。**

### Evidence Status

**GAP**

如果未来目标算法选 FUSED：
- 先验证 model conversion/operator coverage；
- 再验证是否整模型放 accelerator；
- 如果只 offload backbone/head，而 cross-view/temporal 在 Host/GPU，必须重新画 data path；
- 不能沿用 PER_VIEW 的 H2D/D2H 模型。

---

## 6. Topology-specific Evidence Matrix

| Route | PER_VIEW 当前证据 | FUSED 当前证据 | 当前工程边界 |
|---|---|---|---|
| RK3588 Integrated | Official YOLO BENCH | SPEC/INFER + GAP | transformer support ≠ exact BEV benchmark |
| Jetson Orin | BENCH/CASE | BENCH(class) + GAP(exact) | BEVFusion on Orin exists; exact six-camera UAV graph still unknown |
| IQ-9075 | PARTNER_BENCH + REF | REF/GAP + metadata conflict | AI Hub lists BEVFormer/IQ-9075 but no clean IQ-9075 numeric result |
| RK3588 + Accelerator | VENDOR_BENCH/CASE/REF | GAP | current public accelerator evidence is much stronger for PER_VIEW |

这张表**不是平台排名**。

它只说明：
> topology 一变，平台证据成熟度也会变化。

---

## 7. 对六摄像头 Case 的新判断

### 如果项目选择 PER_VIEW

当前公开证据链较成熟：
- RK3588；
- Jetson；
- IQ-9075；
- M50/Metis/Hailo

都能找到与 detection/streaming 直接相关的事实或 Benchmark。

因此 PER_VIEW 更容易在短期内做统一 Benchmark。

### 如果项目选择 FUSED_MULTI_VIEW

平台研究重点会转向：
- Transformer/operator coverage；
- cross-view attention；
- temporal state；
- memory capacity/bandwidth；
- GPU/NPU split；
- whole graph deployment；
- model conversion；
- fused output 与 W4 map/planner 的边界。

此时“YOLO FPS”价值会显著下降。

---

## 8. 证据升级条件

### RK3588
GAP → REF/BENCH：
- official/credible exact BEV model deploy；
- model/input/precision/software/device；
- latency/memory/power。

### Jetson
BENCH(class) → exact Candidate evidence：
- camera-only target fused model；
- exact 6-view input；
- current software；
- Frame Age/P95/P99；
- W2/W6 concurrency。

### IQ-9075
REF/GAP → BENCH：
- resolve AI Hub support metadata；
- IQ-9075 exact profile/result；
- physical Camera/QNN path；
- latency/memory/power。

### Host+Accelerator
GAP → Candidate：
- exact fused model supported；
- operator split documented；
- H2D/D2H graph documented；
- end-to-end latency/power measured。
