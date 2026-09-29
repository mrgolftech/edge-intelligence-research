# W3 DNN Perception Workload Profile

- 状态：v0.1
- 日期：2026-09-30

## 第一版统一基准：MLPerf Inference Edge YOLOv11

截至 2026-09，MLCommons 的 MLPerf Inference v6.1 将 YOLO v11 列为 Edge benchmark：
- reference: PyTorch / ONNX
- dataset: COCO safe subset
- Offline / SingleStream / MultiStream

采用 MLPerf 的目的，是避免“各厂商各测一个 YOLO FPS”导致不可比。

## 两层测试

### A. MLPerf-compatible
记录：
- precision
- scenario
- throughput
- latency
- accuracy
- power
- software stack

### B. 无人系统真实流式 Pipeline
```text
camera/decode → preprocess → inference → NMS → optional tracking
```

记录：
- end-to-end frame age
- effective FPS
- dropped frames
- CPU/GPU/NPU
- DDR
- power

## 多路扩展

单路、2路、4路、6路分别测试：

```text
Efficiency(N) = Throughput(N) / (N × Throughput(1))
```

## 不能用 TOPS 推 FPS 的原因

- graph / precision
- compiler
- unsupported-op fallback
- pre/post processing
- memory traffic
- scheduling
- batch/scenario
- thermal state

## References
- https://github.com/mlcommons/inference
- https://docs.mlcommons.org/inference/benchmarks/object_detection/yolo/
