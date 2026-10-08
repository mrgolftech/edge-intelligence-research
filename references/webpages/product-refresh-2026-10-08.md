# 代表性端侧计算产品公开资料复核（2026-10-08）

- 获取日期：2026-10-08
- 用途：支撑最终报告 v0.5 “现有产品调研”章节的时效性校核
- 原则：只记录官方页面/官方 PDF 当前可确认信息；与既有仓库数据冲突时保留冲突，不擅自合并。

## 1. NVIDIA Jetson AGX Orin

官方 Technical Brief 当前可确认：
- Jetson AGX Orin 系列最高 275 TOPS；
- 64GB/32GB LPDDR5；
- 约 204.8 GB/s memory bandwidth；
- Arm Cortex-A78AE CPU + Ampere GPU + NVDLA；
- SoM 100×87 mm；
- AGX Orin power range 15–60W（Developer Kit/Module 具体模式见官方资料）。

来源：
- https://www.nvidia.com/content/dam/en-zz/Solutions/gtcf21/jetson-orin/nvidia-jetson-agx-orin-technical-brief.pdf
- https://developer.nvidia.com/embedded/jetson-agx-orin

## 2. Qualcomm Dragonwing IQ-9075

官方页面当前状态：
- Active；
- 50 / 100 Dense INT8 TOPS；
- up to 36GB LPDDR5 with inline ECC；
- up to 16 concurrent cameras；
- 8-core Kryo CPU + Adreno GPU + Hexagon NPU；
- 4-core real-time subsystem；
- 2× 2.5GbE TSN、CAN-FD、PCIe 等；
- SoC power official brief 3.8–20W；
- Linux Yocto / Ubuntu；
- Robotics、AMR、Drones 为官方应用方向。

来源：
- https://www.qualcomm.com/internet-of-things/products/iq9-series/iq-9075
- https://docs.qualcomm.com/doc/87-83840-1/87-83840-1_REV_E_Qualcomm_Dragonwing_IQ9_Series_Platform_Product_Brief.pdf

## 3. Houmo LQ50-24GB M.2

当前官方用户指南：
- M50；
- 160 TOPS；
- 100 TFLOPS@bFP16；
- 24GB LPDDR5/LPDDR5X；
- 153.6GB/s；
- PCIe Gen4 x4；
- M.2 2280；
- 22×80×3.3mm；
- 约 9g；
- 典型功耗 13W；
- -20℃～+60℃。

来源：
- https://developer.houmoai.com/hmdoc/m50/hardware-manuals/latest/product-manuals/lq50-m.2/LQ50_M.2_guidelines/intro/index.html

## 4. Firefly BM1688 / AIO-Core-1688JD4

官方规格 PDF 当前可确认：
- BM1688；
- 16 TOPS INT8；
- 4 TFLOPS FP16/BF16；
- 16×1080p30 decode；
- 10×1080p30 encode；
- 6-channel sensor input；
- ISP 支持 HDR、3DNR、3A、去雾等。

来源：
- https://download.t-firefly.com/Spec/Mainboards/AIO-1688JD4_Specification_EN.pdf
- https://www.t-firefly.com/products/core-1688jd4-core-board

## 5. Advantech MIC-733-AO

官方产品页/数据表当前可确认：
- Jetson AGX Orin 32/64GB；
- up to 275 TOPS；
- 4×GbE（PoE optional）；
- optional 2-ch GMSL；
- 9–36VDC；
- 192×230×87mm；
- 4.5kg；
- fanless；
- optional TPM 2.0。

来源：
- https://www.advantech.com/en-us/products/965e4edb-fb98-429e-89ed-9a0a8435a7be/mic-733/mod_09861425-4950-46ab-ad39-1b5522881218
- https://advdownload.advantech.com/productfile/PIS/MIC-733/file/MIC-733-AO_DS%28030425%2920250306092757.pdf

## 6. Seeed reComputer Industrial / Robotics

官方页面当前可确认：
- reComputer Industrial J4012 使用 Jetson Orin NX 16GB；
- 100 TOPS；
- fanless；
- Ethernet、RS232/422/485、CAN；
- Robotics 系列当前在官方设备支持列表中继续维护。

来源：
- https://www.seeedstudio.com/reComputer-Industrial-J4012-p-5684.html
- https://wiki.seeedstudio.com/jetson_developtool_supported_devices/

## 7. Black Sesame A2000 family

2026 官方公开资料当前可确认：
- A2000N/L/U/X 四档；
- family range 200–1000 TOPS；
- INT4/INT8/FP8/FP16/FP32；
- vendor claims 8TB/s on-chip cache bandwidth；
- Xingmou ISP；
- 面向 physical AI、L3/L4、robotics；
- 2026 WAIC 公开 Qwen VLM 板端演示。

来源：
- https://www.blacksesame.com/zh/list_11/958.html
- https://www.blacksesame.com/zh/list_8/994.html
- https://www.blacksesame.com/zh/list_11/1010.html

## 8. 复核结论

- 2026-09 仓库主要产品事实在 2026-10-08 抽查中未发现需要整体推翻的变化；
- IQ-9075、LQ50、BM1688、Jetson Orin 等关键参数仍与既有事实表一致；
- 产品比较仍必须区分 SoC/SoM、accelerator、industrial computer、automotive/physical-AI SoC；
- Black Sesame A2000 等家族级 TOPS 不能当作具体 SKU 的统一规格；
- industrial computer 的整机重量/接口能力不能直接外推到小型 UAV；
- independent accelerator 必须连同 Host 一起评价。
