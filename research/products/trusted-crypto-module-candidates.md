# 安全可信无人智算：可信密码模块/安全芯片候选事实底座

> 状态：v0.1  
> 日期：2026-09-30  
> 目的：寻找能把“商密 + 设备身份 + 平台度量 + 远程证明”合并到单一安全器件的现实方案。  
> 注意：本文件不是选型结论，只是公开事实与工程适配问题清单。

## 1. 为什么这一类器件重要

前一阶段 Trust Plane 架构发现：

- 普通 Secure Element / 商密芯片擅长 SM2/SM3/SM4、密钥保护与设备身份；
- TPM/TCM 擅长 PCR、度量、sealed key、Quote/Remote Attestation；
- 若分别使用两颗芯片，会增加 BOM、板面积、驱动、中间件、provisioning 和证书体系复杂度。

因此优先寻找：

> **TCM/TPM + SM2/SM3/SM4 + 设备身份 + PCR/Quote + Arm/Linux/嵌入式适配**

的国产器件。

---

## 2. 国民技术 NS350

### 已确认事实

国民技术官方资料显示，NS350 v32/v33：

- TCM 2.0 可信密码模块安全芯片；
- 符合 GM/T 0012-2020；
- 同时兼容 TPM 2.0（官方标注 Spec 1.59）；
- 支持 SM2 / SM3 / SM4；
- 支持完全个性化 EK（Endorsement Key）证书；
- 24 个 SM3 PCR；
- 支持多路设备主动度量（杂凑和签名验证）；
- 支持 SPI / I2C；
- 1.8 V / 3.3 V；
- QFN32 / QFN16；
- 支持安全固件升级；
- 可用于通用 Arm 平台和嵌入式系统；
- 兼容 Windows / Linux / BSD UNIX 及多种国产 OS；
- 官方当前资料显示已通过国内安全芯片和可信密码模块“双商密二级”认证，并获得 CC EAL4+ 认证。

### 为什么它值得进入我们的重点候选

NS350 同时覆盖：

```text
SM crypto
+ Device / EK identity
+ PCR
+ TCM/TPM command model
+ measurement
+ embedded Arm
+ SPI/I2C
```

这意味着它具备把此前：

```text
Option B: SoC + SM Secure Element
+
Option C: SoC + TPM/TCM
```

合并成一颗器件的潜力。

### 当前仍需确认

公开材料还不足以直接下产品结论，至少需要厂商/开发板验证：

1. Linux kernel driver 使用标准 TPM2 TIS SPI/I2C 还是厂商驱动；
2. TCM 2.0 与 TPM 2.0 firmware mode 的切换/兼容方式；
3. TCM 模式下 Quote / sealed key / PCR extend 的具体 API；
4. SM2 EK/AK certificate provisioning 流程；
5. tpm2-tools / tpm2-tss 的实际兼容边界；
6. 国密 TSS / SDK 是否开放；
7. Linux IMA 与 SM3 PCR 的适配；
8. RK3588 / A1000 / Atlas 等 Arm64 BSP 的实机适配；
9. boot measurement 如何从 SoC BootROM/bootloader 延伸到 NS350；
10. 功耗、启动时序、SPI/I2C 带宽；
11. 高低温/振动/无人机环境；
12. 量产密钥/证书注入方案。

### 官方来源

- https://www.nationstech.com/product/securityic/trustedcomputing/ns350/
- https://www.nationstech.com/about/news/product/3387.html
- https://www.nationstech.com/about/news/product/3390.html
- https://www.nationstech.com/about/news/product/6223.html

---

## 3. 国民技术 Z32H330TC

### 已确认事实

官方产品页明确：

- 中国密码算法 + 国际密码算法双算法可信计算产品；
- SPI 接口；
- 硬件隔离密码算法服务；
- 平台完整性保护；
- **平台远程身份证明**；
- 支持 Intel / AMD / Qualcomm 及多个国产计算平台；
- 支持嵌入式系统 / IoT；
- 支持 SM2 / SM3 / SM4 以及 AES/RSA/ECC/SHA；
- 官方资料说明支持 TPM 2.0 / TCM 2.0 应用；
- EAL4+ 安全认证。

### 工程意义

Z32H330TC 的官方资料直接使用“平台远程身份证明”表述，因此它是本项目当前公开证据中非常直接的 Remote Attestation 器件案例。

但相较于 NS350：
- 产品代际较早；
- 新产品接口/认证/供货/成本优势需重新确认。

所以当前定位：

> **Reference / fallback candidate，不直接作为首选。**

官方来源：
- https://www.nationstech.com/product/securityic/trustedcomputing/z32h330tc/
- https://www.nationstech.com/about/news/product/3367.html

---

## 4. 与普通商密安全芯片的区别

普通商密 SE 典型能力：

```text
SM2 private key
SM3
SM4
TRNG
certificate
key wrapping
```

NS350 / Z32H330TC 这一类 TCM/TPM 器件额外引入：

```text
PCR
measurement
EK
platform state
sealed object/key
attestation / platform proof
```

因此它更适合本项目提出的：

> Device Identity + Platform State + Model State + Mission Admission

而不是只有“密码接口”。

---

## 5. 对安全智算平台的候选组合

### Combination T1 — RK3588 + NS350

```text
RK3588
├─ Secure Boot
├─ TrustZone
├─ AI / ISP / VPU
└─ Linux / ROS2

NS350
├─ SM2/SM3/SM4
├─ Device / EK identity
├─ PCR / measurement
├─ sealed key
└─ attestation
```

潜在优势：
- 国产化程度高；
- RK3588 已有 Secure Boot / OTP / TrustZone；
- NS350 补足 TCM/attestation 与商密可信根；
- 可形成低功耗、小型化安全智算盒。

最大工程问题：
- Boot measurement chain 如何连接；
- RK3588 BSP + IMA + TCM/TPM stack 的集成成熟度；
- 六摄 C2 full workload + security overhead。

### Combination T2 — A1000 + NS350

A1000 已有：
- Secure Boot；
- TrustZone / Open-TEE；
- OTP；
- Security Island。

NS350 可补：
- 标准 TCM/TPM measurement；
- fleet attestation；
- SM EK/PCR。

风险：
- A1000 本身安全能力可能与 NS350 部分重复；
- 车规平台开发资料/供应链/无人机生态成本更高。

### Combination T3 — Atlas 200I A2 + NS350

Atlas 已有较明确硬件 Secure Boot chain；
NS350 可作为外部设备身份与 attestation root。

需验证：
- Arm Linux TPM/TCM driver；
- NPU firmware/model measurement；
- 产品功耗/Camera interface 是否满足无人平台。

---

## 6. 推荐的 P1 Attestation Prototype

优先做一个不依赖“完整 NPU confidential compute”的可落地原型：

```text
RK3588 Secure Boot
     ↓
U-Boot / Kernel measurements
     ↓
Linux IMA
     ├─ ROS2 binary hash
     ├─ planner binary/config
     ├─ model manifest
     └─ model hash
     ↓
NS350 PCR
     ↓
Quote / Attestation Evidence
     ↓
Verifier
     ↓
Policy
     ├─ allow mission
     ├─ release model key
     └─ reject / limited mode
```

这条路线的优点是：
- 不要求证明 NPU 内部 transistor-level execution；
- 先解决真正工程可做的“系统软件 + 模型 artifact 身份”；
- 能形成清晰 Demo 和 Benchmark；
- 与 Fleet / 指控系统容易结合。

---

## 7. 原型必须验证的关键问题

### Functional
- PCR extend；
- Quote；
- SM2 AK/EK；
- sealed model key；
- boot event log；
- IMA measurement；
- model hash change；
- nonce/replay protection。

### Performance
- boot 增量时间；
- IMA 启动开销；
- Quote latency；
- SM2 sign latency；
- SPI/I2C transaction；
- full C2 workload 下 CPU/P99 Frame Age；
- attestation background task 对功耗的影响。

### Security
- clone eMMC 到另一板；
- model tamper；
- rootfs tamper；
- stolen filesystem credential；
- replay old Quote；
- revoke device cert。

---

## 8. 当前工程判断

1. “国产商密 + TCM/TPM + Remote Attestation”已经有现实芯片基础，不是只能依赖国外 TPM。
2. NS350 是目前公开资料下非常值得做开发验证的器件，因为它同时覆盖 TCM2.0/TPM2.0、SM2/3/4、PCR、EK、Arm/嵌入式和 SPI/I2C。
3. 但“支持 TCM/TPM”不等于已和 RK3588/ROS2/IMA 打通，下一阶段需要 SDK/开发板验证。
4. 如果 NS350 可承担所需 TCM + 商密能力，安全智算盒可以避免普通 SE + TPM 双芯片重复设计。
5. 第一版 Attestation 不必追求证明 NPU 微架构执行；先证明 boot/kernel/app/model artifact，是更现实的工程路线。
