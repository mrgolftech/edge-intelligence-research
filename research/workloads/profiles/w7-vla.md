# W7 Foundation Model / VLM / VLA Workload Profile

- 状态：v0.1
- 日期：2026-09-30

## 开放基线：OpenVLA

已确认：
- 7B parameters
- open-source VLA
- pretrained on 970k robot episodes

OpenVLA官方代码建议：
- control/data frequency around 5–10Hz
- model is not trained with action chunking
- high-frequency controller may need action downsampling

这说明 VLA policy frequency 与低层 servo frequency 必须分层。

## 裸权重下限

| Precision | Raw weights |
|---|---:|
| FP16 | ~14.0 GB |
| INT8 | ~7.0 GB |
| INT4 | ~3.5 GB |

实际内存还包括：
- vision encoder
- activations
- runtime
- quantization metadata
- allocator/cache
- optional language KV cache

## Benchmark

### LIBERO
- 130 tasks
- standardized manipulation task suites

### LIBERO-Plus (CVPR 2026)
- 7 类 perturbation
- 10 个 SOTA VLA
- paper reports success can fall from >95% to <30% under modest perturbations

因此要同时测：
- task success
- action latency/rate
- memory
- bandwidth
- power
- robustness
- 与 perception/SLAM 并发退化

Gemini Robotics On-Device 作为产业趋势证据，不作为第一版开放硬件 benchmark。

## References
- https://openvla.github.io/
- https://github.com/openvla/openvla
- https://github.com/Lifelong-Robot-Learning/LIBERO
- https://openaccess.thecvf.com/content/CVPR2026/html/Fei_LIBERO-Plus_A_Progressive_Robustness_Benchmark_for_Visual-Language-Action_Models_CVPR_2026_paper.html
- https://deepmind.google/blog/gemini-robotics-on-device-brings-ai-to-local-robotic-devices/
