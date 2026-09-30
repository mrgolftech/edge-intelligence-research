# 2026-09 现成端侧计算产品/解决方案证据索引

- 获取日期：2026-09-30
- 用途：支撑 `research/products/commercial-product-landscape-2026.md`
- 原则：优先官方产品页/官方文档；冲突不自行消解

## NVIDIA

### Jetson Developer Kits / Orin Nano Super
- https://developer.nvidia.com/embedded/jetson-developer-kits
- https://www.nvidia.com/en-eu/autonomous-machines/embedded-systems/jetson-orin/nano-super-developer-kit/
确认：
- Orin Nano Super 67 TOPS、8GB、102GB/s、7–25W；
- AGX Orin Developer Kit；
- Thor Developer Kit。

### Jetson lifecycle
- https://developer.nvidia.com/embedded/lifecycle
确认：
- AGX Orin / Orin NX / Orin Nano commercial modules through 2032-01；
- AGX Orin Industrial through 2033-07。

### Thor
- https://developer.nvidia.com/blog/introducing-nvidia-jetson-thor-the-ultimate-platform-for-physical-ai/
确认：
- 40–130W；
- 128GB / physical-AI route；
- dev-kit mechanical/interface facts。

## Seeed

### reComputer Robotics
- https://wiki.seeedstudio.com/recomputer_robotics_j401_getting_started/
确认：
- Orin NX/Nano；
- optional 4-in-1 GMSL2；
- CAN；
- 19–54V；
- 115×115×38mm；
- 1100g；
- JetPack 6 preinstalled / 7.2 supported。

### reComputer Rugged J4012
- https://wiki.seeedstudio.com/ai_robotics_recomputer_rugged_j40_getting_started/
确认：
- Orin NX 16GB；
- rugged M12；
- 4×PoE GbE + GbE；
- dual isolated CAN-FD；
- 19–48V。

## Advantech

### MIC-733-AO
- https://www.advantech.com/en-us/products/965e4edb-fb98-429e-89ed-9a0a8435a7be/mic-733/mod_09861425-4950-46ab-ad39-1b5522881218
- 2026 datasheet
确认：
- AGX Orin；
- optional GMSL；
- 9–36V；
- 192×230×87mm；
- 4.5kg；
- fanless。

## Qualcomm / IQ-9075

### IQ-9075
- https://www.qualcomm.com/internet-of-things/products/iq9-series/iq-9075
确认：
- Active；
- 50/100 dense TOPS；
- 36GB LPDDR5 ECC；
- up to 16 cameras；
- 4-core RT subsystem；
- 10+ year longevity；
- IQ-9075 Module / EVK。

### SECO IQ9 COM Express
- https://edge.seco.com/en/som-come-ct6-dragonwing-iq9.html
确认：
- COM Express Type 6；
- 50/100 TOPS；
- up to 36GB LPDDR5 ECC；
- 页面显示 in stock。

### Innodisk EXMP-Q911
- https://www.innodisk.com/en/products/computing/qualcomm-solution/exmp-q911
确认：
- COM-HPC Mini；
- IQ-9075；
- 36GB LPDDR5X；
- dual 2.5GbE；
- dual 4-lane CSI-2；
- -40～85°C；
- longevity through 2038（厂商声明）。

## Firefly / RK3588

### EC-A3588JQ
- https://community.t-firefly.com/en/docs/products/computers/EC-A3588JQ/started
确认：
- RK3588J；
- up to 32GB；
- industrial computer；
- -40～85°C。

### AIBOX PRO
- https://www.t-firefly.com/products/aibox-pro-edge-computing-computer
确认：
- RK3588/RK3576 Host；
- dual M.2 accelerator；
- supports RK1828 / Houmo LQ50 / DeepX DX-M1；
- CAN-FD/RS485/DI/DO；
- 9–36V；
- 160×111×61mm；
- RK3588 + 1×LQ50 page values: normal 8.4W, max 45.6W。

冲突：
- Firefly 页面称 LQ50 48GB；
- Houmo current LQ50-24GB guide = 24GB。
结论：exact Firefly card SKU/memory 未确认。

## Houmo

### LQ50 M.2
- https://developer.houmoai.com/hmdoc/m50/hardware-manuals/latest/product-manuals/lq50-m.2/LQ50_M.2_guidelines/intro/index.html
确认：
- 160 TOPS；
- 100 TFLOPS bFP16；
- 24GB；
- 153.6GB/s；
- Gen4x4；
- 22×80×3.3mm；
- 9g；
- typical 13W。

## Axelera

### Metis current product family
- https://axelera.ai/
确认：
- Metis shipping；
- 214 TOPS；
- typical app power 3.5–9W；
- up to 16GB per chip，具体 SKU 需确认。

### Embedded 113m
- https://docs.axelera.ai/docs/hardware/getting-started/start/embedded-113m/
确认：
- M.2 2280；
- PCIe Gen3 x4；
- up to 214 TOPS；
- 2/8GB LPDDR4X；
- host slot power up to 11.55W average / 23.1W peak；
- -20～70°C。

## Hailo

### Hailo-10H M.2
- https://hailo.ai/zh-hans/products/ai-accelerators/hailo-10h-m-2-generative-ai-acceleration-module/
- https://hailo.ai/zh-hans/files/hailo-10h-m-2-et-product-brief-en/
确认：
- 40 TOPS INT4；
- M.2 2242；
- PCIe Gen3x4；
- 4/8GB LPDDR4；
- ARM/x86。

冲突：
- product page typical <2.5W；
- ET product brief typical <3.5W。
不自行合并为单一精确功耗。

### Raspberry Pi AI HAT+ 2
- https://www.raspberrypi.com/products/ai-hat-plus-2/
- https://www.raspberrypi.com/documentation/accessories/ai-hat-plus.html
确认：
- Hailo-10H；
- 40 TOPS INT4；
- 8GB；
- integrated Pi camera software stack；
- production until at least 2036-01。

## Huawei Ascend

### Atlas 200I A2
- https://www.hiascend.com/zh/hardware/accelerator-module-A2
确认：
- 官方明确机器人/无人机应用；
- 20 TOPS INT8 / 10 TFLOPS FP16；
- 4-core CPU；
- 4/8/12GB LPDDR4X ECC；
- video/ISP；
- 25W typical；
- 82×60×7mm；
- PCIe/Ethernet/MIPI/SATA/USB/CAN。

## Cambricon

### MLU220-M.2
- https://www.cambricon.com/index.php?a=lists&c=index&catid=57&m=content
确认：
- 8 TOPS INT8；
- M.2 2280 B+M；
- PCIe3.0x2；
- 8.25W；
- passive cooling；
- video codec。

## SOPHGO / Firefly BM1688

### Core/AIO-1688JD4
- https://www.t-firefly.com/products/core-1688jd4-core-board
- https://download.t-firefly.com/Spec/CoreBorads/Core-1688JD4_Specification_EN.pdf
- https://wiki.t-firefly.com/en/Core-1688JD4/started.html
确认：
- BM1688；
- 16 TOPS INT8；
- 16×1080p30 decode；
- 10×1080p30 encode；
- **6-channel sensor input**；
- ISP；
- SOPHON SDK；
- AIO board has CAN/RS485/CSI/GbE。

### SOPHGO SE9
- https://sophon.ai/
确认：
- SE9 16-BP1-11；
- BM1688；
- 8GB；
- 16-channel HD Video Analysis。

## AMD

### Kria K26 / KR260
- https://www.amd.com/en/products/system-on-modules/kria/k26.html
- https://www.amd.com/en/products/system-on-modules/kria/k26/robotics.html
确认：
- production SOM；
- vision/robotics；
- commercial/industrial grade；
- native ROS2；
- KR260 robotics starter kit。

K26 brief:
- up to 1.4 TOPS；
- integrated video codec；
- up to 15 camera connectivity as platform capability。

## Intel

### Core Ultra + Robotics AI Suite
- https://builders.intel.com/intel-technologies/software/edge-ai-suites/robotics-ai-suite
确认：
- 2026.2；
- ROS2/OpenVINO；
- CPU/GPU/NPU workload consolidation；
- real-time/safety route；
- deployment-ready partner systems。

此条属于 solution ecosystem，不是单一 board SKU。

## 未确认

### “小米算力仓”
本轮 mi.com / xiaomi.com 官方检索未发现对应可核验硬件产品页。
当前状态：GAP / 暂不纳入正式产品数据库。
