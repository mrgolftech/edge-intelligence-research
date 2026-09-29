# Benchmark Reference：MLPerf Inference Edge

- 机构：MLCommons
- 获取日期：2026-09-30
- 用途：W3 DNN Perception、W4 3D Perception

## MLPerf Inference v6.1

当前 repository 将 YOLO v11 列入 Edge：
- COCO safe subset
- PyTorch / ONNX reference
- Offline / SingleStream / MultiStream

来源：
https://github.com/mlcommons/inference
https://docs.mlcommons.org/inference/benchmarks/object_detection/yolo/

## PointPainting

MLPerf文档：
- dataset: Waymo
- Edge
- SingleStream
- 44M parameters
- 3T FLOPs
- FP32 reference mAP 54.25%

来源：
https://docs.mlcommons.org/inference/benchmarks/automotive/3d_object_detection/pointpainting/
https://docs.mlcommons.org/inference/

## 使用规则

MLPerf reference implementation 不一定是最快实现。

本项目：
1. 保存 MLPerf-compatible 测试；
2. 另测真实 camera pipeline；
3. 非正式提交不得称为“MLPerf 官方成绩”。
