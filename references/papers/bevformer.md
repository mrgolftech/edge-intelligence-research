# BEVFormer 论文摘要

- 论文：BEVFormer: Learning Bird’s-Eye-View Representation from Multi-Camera Images via Spatiotemporal Transformers
- 会议：ECCV 2022
- 获取日期：2026-09-30
- 用途：W4 multi-camera BEV/Transformer baseline

## 核心事实

BEVFormer：
- camera-only autonomous-driving perception
- unified BEV representation
- spatial cross-attention across cameras
- temporal self-attention
- 3D detection / map segmentation
- nuScenes evaluation
- paper reports 56.9 NDS on test set

## 对项目意义

该 workload 同时包含 multi-camera、cross-view attention 和 temporal state，平台评估需要关注 memory / bandwidth / temporal cache，不能只比较单帧 INT8 TOPS。

## 来源
- https://www.ecva.net/papers/eccv_2022/papers_ECCV/html/694_ECCV_2022_paper.php
- https://github.com/fundamentalvision/BEVFormer
