# 平台适配证据缺口 Backlog

- 状态：active
- 日期：2026-09-30
- 原则：目标不是把所有 GAP 变成“支持”，而是找到足够证据决定它到底是支持、受限还是不适用。

## P0：六摄像头 Case 直接相关

### G01 — RK3588: W1 + W2 + W3 并发
当前：
- W1 有官方规格基础；
- W3 已有 Rockchip 官方 RKNN Model Zoo 单核 NPU benchmark：YOLOv8n INT8 640×640 为 73.5 FPS，YOLO11n 为 60.0 FPS；
- W2/W4 已有 2026 Sensors 论文在 RK3588 上运行多传感器 SLAM 的系统证据；
- Rockchip 官方 API 已确认 `rknn_dup_context` 与三核 `core_mask` 调度路径，官方 `rknn_benchmark` 可指定 1/2/3 核；
- 已审计社区 `dongyuzhen/rk3588-yolo` 的单路 1080p60 RGA/RKNN/MPP pipeline：分阶段 P99 有工程参考价值，但其 README 中“E2E 16.6ms/P99 22.3ms”小于同表 NPU avg 25.5ms，且另一处又写 E2E <200ms，口径冲突；**不升级为主 Benchmark**；
- **仍缺** 可复现的 VIO/SLAM + 多路视频 + detection 并发 Frame Age 数据，且不得按核心数线性外推吞吐。

可接受证据：
1. 官方/论文/开源项目，明确板卡、算法、输入、FPS、软件版本；
2. 若公开资料不足，执行本项目自测。

必须记录：
- camera count/resolution/fps
- ORB-SLAM3/VIO版本
- detection model/input/precision
- CPU/GPU/NPU/DDR
- dropped frame / latency
- board power / temperature
- RKNN Toolkit / librknnrt / RKNPU driver / model-zoo revision / core_mask

注意：Rockchip 官方 Model Zoo 明确说明旧 RKNPU SDK 可能导致性能或结果错误，因此 SDK/driver version 必须冻结。社区多线程 issue 仅作为风险信号，不作为当前缺陷结论。

### G02 — LQ50: W3 视觉推理与 Host 开销
当前：
- W7 大模型证据明确；
- BX50 已证明 RK3588 host + M50 可作为多路视频分析系统；
- 后摩官方 Model Zoo 已给出 M50-compatible xh2 的 YOLOv5s/YOLO11m accuracy、inference latency、end-to-end latency 与 throughput；
- 官方 `resnet50_multistreams` 还提供单设备/多设备、多线程、多 stream runtime 示例（默认 1 device / 4 threads，每线程 1 stream），证明并发软件路径存在；
- 官方 `tools/bandwidth_perf` 已审计：它通过芯片上 load/store/transpose 模型测 AI Core 实际读写带宽，XH2 示例约 123.43/127.14 GiB/s；**它不是 PCIe Host↔Device 带宽，不能填 T_H2D/T_D2H**；
- **剩余 GAP 已从“有没有视觉性能/并发路径”进一步收敛为“LQ50 板卡 + host + Camera/video/PCIe 的多流端到端性能、功耗和热稳态”。**

可接受证据：
- 同一 YOLO 模型的 input/precision/FPS；
- host CPU；
- PCIe generation/lanes；
- pre/post-processing位置；
- accelerator-only 与 system power。

否则继续保持 GAP。

### G03 — Jetson Orin: 多 workload 并发
当前：
- Isaac ROS 5.0 已补固定版本 AGX Orin graph latency：DetectNet 15ms、RT-DETR 13ms、DNN Stereo Full 17ms；Nvblox TSDF/ESDF 有 core timing；
- 单节点和系统案例证据丰富；
- Nova Carter / Isaac ROS release-3.2 已给出物理多相机 Live Graph：4×1200p VSLAM 30.1 FPS，3×1200p Perceptor 中 VO 30 FPS / ESDF 9.45 FPS；
- 这已经证明 W1+W2+W3(depth)+W4 的整图系统路径；
- **仍缺** 与本项目六摄像头 + YOLO detection + VIO/SLAM 完全同构的并发、功耗和热数据。

实验目标：
- 6-camera W1 only
- W1+YOLO W3
- W1+W2+W3
- W1+W2+W3+W6
- 30/60/120 min thermal steady state

重点从“Orin能不能跑多任务”转为“在本项目 workload 下边界在哪里”。

## P1：新一代候选平台

### G04 — Qualcomm IQ-9075: Robotics workload benchmark
当前：
- 100 dense TOPS、16 camera、36GB ECC、real-time subsystem、LLM 数据已有官方证据；
- Qualcomm 官方 QRB ROS Camera：CSI/GMSL、多 stream、DMA-BUF zero-copy；
- Qualcomm 官方 AMR Service：2D LiDAR SLAM、mapping/localization、Nav2；
- Innodisk iQ-Studio：YOLOv10n INT8 + 1080p30 H.264 的 1/4/9/16 stream 可复现 benchmark，9 streams 28.41 E2E FPS/channel，16 streams 15.90；
- acontis EtherCAT：1 ms target cycle、约100 μs round-trip、<8 μs jitter；
- 当前缺口转为 **物理多 camera 同步、VIO/视觉 SLAM 定量数据、SLAM+AI+planning 全并发性能**。

新增事实：
- Qualcomm 官方 `qrb_ros_benchmark` 明确支持 IQ-9075 EVK，可 Benchmark QRB Image/IMU/PointCloud/TensorList 与 DMA-BUF Image/PointCloud；
- 官方 `qrb_ros_nn_inference` 支持 IQ-9075，并封装 QNN / AI Engine Direct；
- 当前 `qrb_ros_benchmark/results` 公开数字仅发现 QCM6490 IMU JSON，**没有 IQ-9075 Camera/NN 结果**。

目标：
- 不再重复搜索“有没有官方 benchmark 方法”——方法已经确认；
- 下一步寻找公开 IQ-9075 result，或未来按官方 harness 复测 physical Camera→DMABUF→QNN；
- 没有 IQ-9075 numeric result 前继续标 REF+GAP，不升级为 BENCH。

### G05 — Black Sesame A2000: 从汽车案例到可量化 workload
当前：
- 2026 官方公开家族 200–1000 TOPS、VLA/world-model支持、ISP和8TB/s片上缓存；
- 有 Qwen VLM 端侧实时交互演示；
- 缺公开标准化 latency/FPS/power benchmark。

规则：
- 量产/展会演示证明产品路线存在；
- 不从“1000 TOPS”反推 UAV/robot workload 适配。

### G09 — IQ-9075 physical multi-camera / VIO

已有多 stream benchmark 主要由 H.264 文件流构成，InnoPPE 只有 1 路 live UVC camera。

已确认可复现入口：
- `qrb_ros_camera → qrb_ros_transport/DMABUF → preprocess → qrb_ros_nn_inference → qrb_ros_benchmark monitor`；
- 官方 benchmark calculator 可产生 latency/jitter/missed-frame/CPU 一类指标，但当前公开 IQ-9075 Camera/NN 数字仍缺。

仍需公开证据：
- 6+ physical CSI/GMSL cameras；
- per-frame timestamp propagation 已由 Qualcomm 官方源码确认；仍需 multi-camera hardware synchronization / trigger；
- drop/jitter；
- camera → zero-copy → QNN inference；
- VIO/visual SLAM 与多 camera detection 并发；
- DDR/CPU/NPU/power。

在这些证据出现前，16-stream video benchmark 不得写成“16-camera autonomous perception benchmark”。

## P1.5：Perception Topology

### G10 — FUSED Multi-View / BEV 平台证据

当前：
- Jetson Orin：NVIDIA-AI-IOT CUDA-BEVFusion 已有 Orin TensorRT 18/25 FPS 的 fused-BEV 类 BENCH，但包含 LiDAR、输入/软件条件与本项目不同，因此是 BENCH(class)+GAP(exact)；
- IQ-9075：Qualcomm AI Hub BEVFormer 页给出 6×3×480×800、27M、120MB，并把 IQ-9075 EVK/chipset 列入 supported list，但同页又显示 Not supported，当前记 REF/GAP + metadata conflict；
- RK3588：官方 RKNN software 有 transformer/operator support 演进，但未找到 official exact BEVFormer/BEVFusion benchmark，记 SPEC/INFER+GAP；
- RK3588+M50/Metis/Hailo：本轮官方域定向检索未获得条件完整的 BEVFormer/BEVFusion benchmark，继续 GAP。

详细：
`references/benchmarks/fused-multiview-platform-evidence-2026.md`

规则：
- PER_VIEW YOLO evidence 不升级 FUSED；
- generic Transformer/LLM support 不升级 BEV；
- fused model 必须记录 exact model / views / resolution / precision / operator placement / memory / latency / software / power。

## P2：Host + Accelerator 路线

### G06 — Metis on low-power ARM Host
当前：
- i9-13900K 官方 YOLO benchmark 已有；
- Axelera 官方 ARM Host 页面已验证 Firefly ITX-3588J / Orange Pi 5 Plus / NanoPC-T6（RK3588）、RPi5、Jetson Orin Nano/NX；
- Axelera Team 已发布 NanoPC-T6 + Metis / SDK1.5.2 的 YOLOv8n/v8s 性能量级；
- RK3588 Host 需要关注 PCIe non-prefetchable memory window / device-tree 配置；
- Voyager 官方 double buffering 文档确认可把 data transfer 与 compute overlap，典型 transfer-heavy workload 可提高吞吐，但代价是 **2×N frame result delay**；官方明确不建议用于 latency-critical workload；
- Voyager v1.8 `axzoo benchmark` 可输出 P50/P95/P99/P99.9、jitter、per-frame device-vs-host split、CPU/内存，为后续复测提供官方方法。

剩余需要：
- exact Metis SKU
- same model/input/precision
- PCIe Gen3 x4 effective traffic
- end-to-end FPS / P95/P99
- host CPU/DDR usage
- accelerator-only + total system power
- multi-camera decode/preprocess

ARM Host “能运行”已确认，下一步是测系统代价。

### G07 — Hailo on robotics Host
当前：
- Raspberry Pi 5 + Hailo-8L/8/10H 已有官方产品与 camera-stack integration；
- Hailo Apps multisource 支持 USB/RTSP/file 多源并行 pipeline；
- 官方对 RPi 给出 up to 3 sources optimal、15 FPS、640×640 的应用指导；
- 这些属于 REF，不是标准化性能 Benchmark；
- Hailo Model Zoo 官方 `hailortcli benchmark` 可测 HEF 的 hw-only FPS、hardware latency 和 power；**这些属于 T_inference(hw)，不能替代 live Camera Frame Age**；
- Hailo Apps 中的 `pipeline_latency` 配置值不得当作实测结果。

仍需：
- exact Hailo SKU
- same model/input/precision
- live camera count
- E2E latency/FPS
- host CPU/DDR
- system power
- 与 SLAM/VIO 同时运行的资源冲突

### G08 — Accelerator 与 Host 数据搬运
闭环时延映射已经明确 Host+Accelerator 需要单独记录 H2D/accelerator queue/D2H。

已完成证据审计：
- Metis：官方确认 transfer/compute overlap 与 double-buffer latency trade-off，但没有统一 RK3588 Host absolute H2D/D2H；
- Hailo：官方可以测 hw-only inference latency/power，但 live Camera→result P95/P99 仍缺；
- M50/LQ50：官方 bandwidth_perf 是 AI Core/model memory bandwidth，**不是 PCIe H2D/D2H**。

Metis/Hailo/LQ50统一测试：
- host decode
- resize/color conversion
- H2D/D2H copy
- inference
- post-process
- end-to-end / Frame Age P50/P95/P99
- deadline miss
- zero-copy feasibility

## 证据升级规则

- GAP → SPEC：官方文档明确硬件/SDK能力
- SPEC → REF：官方给出完整 reference design/application flow
- SPEC/REF → BENCH：测试条件足够复现
- PARTNER_BENCH：合作伙伴公开实测，条件明确但需保留来源独立性限制
- 任意 → CASE：出现命名真实产品/量产部署
- DEMO 不自动升级为 BENCH
- CASE 不自动升级为 BENCH

同一平台可以同时拥有多种证据，结论只使用与对应 workload 直接相关的那部分。


---

## 与 Phase 2 Validation Matrix 的映射

本 Backlog 继续保留“证据搜索/负证据”职责；六摄像头 Case 的统一验证入口已转到：

- `cases/six-camera-uav/phase-2-validation-plan.md`
- `data/benchmarks/six-camera-validation-matrix.csv`

对应关系：

- G01 RK3588 W1+W2+W3 → V04/V05/V06/V08/V09
- G02/G08 M50/LQ50 Host+Accelerator → V04/V08/V09
- G03 Jetson concurrency → V05/V06/V09
- G04/G09 IQ-9075 physical Camera/VIO → V02/V05/V06
- G06 Metis → V04/V08/V09
- G07 Hailo → V04/V08/V09

这样避免“证据继续搜索”和“未来工程实测”两套任务重复维护。
