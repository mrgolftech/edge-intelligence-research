# Benchmark Reference：OpenVLA / LIBERO / LIBERO-Plus

- 获取日期：2026-09-30
- 用途：W7 VLM/VLA

## OpenVLA
- 7B parameters
- 970k robot episodes
- open-source
- official code recommends control/data frequency around 5–10Hz
- no action chunking in original model

来源：
https://openvla.github.io/
https://github.com/openvla/openvla

## LIBERO
- 130 tasks
- standardized manipulation suites
- public demonstrations/evaluation

来源：
https://github.com/Lifelong-Robot-Learning/LIBERO

## LIBERO-Plus
CVPR 2026：
- 7 perturbation dimensions
- 10 SOTA VLA models
- reported drop from >95% to <30% under modest perturbations

来源：
https://openaccess.thecvf.com/content/CVPR2026/html/Fei_LIBERO-Plus_A_Progressive_Robustness_Benchmark_for_Visual-Language-Action_Models_CVPR_2026_paper.html

## 裸权重估算
OpenVLA 7B：
- FP16: 14.0GB
- INT8: 7.0GB
- INT4: 3.5GB

仅为 raw weight lower bound。
