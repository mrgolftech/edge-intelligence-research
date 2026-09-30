# SmartSens SC132GS：公开器件事实与项目使用边界

- 获取日期：2026-09-30
- 状态：device-facts-verified / project-mode-partially-confirmed

## 1. SmartSens 官方公开事实

官方 GS Series 产品页：
https://www.smartsens.com/en/gs_products

SC132GS：
- Series：SmartGS-1
- Resolution：1.3MP
- Pixel Array：1080H × 1280V
- Pixel Size：2.7 μm
- Optical Format：1/4"
- Shutter：Global Shutter
- HDR：Yes
- Max Frame Rate：120 fps
- Interface：MIPI / LVDS
- package：RW / Fan-out / PLCC

这些是**器件能力上限/规格**，不等于本项目工作模式。

## 2. 项目已有观测

项目既往调试记录确认过：
- 单路媒体链路输出：**1072 × 1280**
- userspace/media format：**NV12**

当前仍未在仓库证据中确认：
- 六路是否全部采用 SC132GS；
- 六路是否全部运行相同 crop/mode；
- 实际 FPS；
- sensor wire RAW bit-depth；
- 六路实际 lane 配置/每 lane rate；
- 六路硬件同步误差。

因此严禁把“SC132GS 最高 120fps”写成本项目实际 120fps。

## 3. RAW Sensor 与 NV12 必须分开

SC132GS 是 image sensor；其 MIPI/LVDS 传输属于 sensor output domain。

项目观测到的 NV12 属于 downstream media/ISP pipeline representation。

所以必须分别记录：

`Sensor RAW/MIPI payload → ISP/CIF → NV12 memory frame → AI/encoder`

不能用 NV12 1.5 byte/pixel 去反推 Sensor MIPI wire rate，也不能用 Sensor max 120fps 去反推当前 NV12 frame rate。

## 4. 对 W1 的处理

在 FPS 未冻结前：
- 1072×1280 NV12 可作为**已观测 frame shape/format**
- FPS 继续做 10/20/30/60/120 Hz sensitivity
- 120 Hz 仅作为器件能力 stress point，不是目标要求

计算结果见：
`data/calculations/six-camera-observed-mode-sensitivity.csv`
