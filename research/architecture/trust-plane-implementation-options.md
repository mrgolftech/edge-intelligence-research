# Trust Plane 实现方案：TEE、TPM/TCM、商密安全芯片与 SoC 安全原语如何组合

> 状态：v0.1  
> 日期：2026-09-30  
> 目标：避免把 Secure Boot、TEE、TPM/TCM、SE/密码芯片混为一谈，并给出安全可信无人智算平台的可实施组合。

## 1. 核心结论

“安全芯片”不能替代完整 Trust Plane。

一个可工作的 Trust Plane 至少涉及四类不同问题：

1. **Boot Trust**：上电后为什么相信正在运行的软件；
2. **Secret / Identity**：密钥和设备身份放在哪里；
3. **Runtime Isolation**：高权限 Linux/AI 应用失陷后，敏感服务如何隔离；
4. **Measurement / Attestation**：远端如何知道设备当前到底运行什么。

不同技术解决的问题不同：

| 技术 | 最擅长解决 | 不应自动假设 |
|---|---|---|
| SoC BootROM/eFuse/Secure Boot | 启动链完整性 | 不自动提供运行时证明 |
| TrustZone + TEE | Secure/Normal World 隔离、可信应用 | 不自动保护 GPU/NPU/整个 DDR |
| TPM/TCM | 度量、PCR、sealed key、quote/attestation | 不适合承担所有高吞吐业务加解密 |
| SE / 商密安全芯片 | 不可导出密钥、SM2/SM3/SM4/TRNG、设备身份 | 不自动具备 PCR/IMA/remote attestation |
| Linux IMA / dm-verity / fs-verity | OS/app/file integrity measurement/verification | 需要可信根保存/签署最终状态 |
| Disk/Data Encryption | 设备丢失后的数据保密 | 设备运行且已解锁时不能阻止已授权进程读数据 |

---

## 2. SoC Secure Boot：Trust Chain 的起点

推荐抽象：

```text
BootROM / immutable code
→ eFuse / OTP root public-key hash
→ FSBL / bootloader
→ firmware / kernel / DTB
→ rootfs / critical application
```

Secure Boot 解决：

> “未经授权的软件能不能启动？”

它不解决：

> “远端能否知道当前设备运行了什么？”

因此 P1 产品必须继续增加 Measured Boot / Attestation。

### 对无人平台的意义

FCU 和 Edge AI Compute 都应有各自的启动信任链；不能因为 companion secure boot，就认为 external FCU 自动可信。

---

## 3. TEE：运行时隔离，而不是万能保险箱

Arm TrustZone 把系统资源划分为 Secure / Normal World；OP-TEE 是常见开源 TEE 实现之一。

适合放入 TEE 的服务：

- device key wrapper；
- model key unwrap；
- certificate/private-key operation；
- secure policy decision；
- security state；
- attestation agent 的敏感部分；
- critical audit signing。

不建议把完整 YOLO/VIO/VLM 直接塞入 TEE：
- TEE 设计目标不是大规模 AI runtime；
- Secure World 资源有限；
- GPU/NPU driver/accelerator 通常在 Normal World；
- 会放大 TCB。

### Secure Storage 的工程边界

OP-TEE 官方文档说明：
- secure storage 可以基于普通 REE filesystem 加密完整性保护；
- 也可以使用 eMMC RPMB；
- 真正安全依赖平台提供 Hardware Unique Key / Chip ID；
- 如果平台没有正确实现 HUK，secure storage 可能失去设备绑定意义。

因此平台验证必须检查：

```text
TEE exists?
≠
Secure Storage is actually device-bound
```

必须进一步验证：
- HUK 来源；
- RPMB；
- rollback protection；
- production key provisioning。

官方：
- https://optee.readthedocs.io/en/latest/
- https://optee.readthedocs.io/en/4.3.0/architecture/secure_storage.html

---

## 4. TPM / TCM：最适合做“状态证明”

TPM/TCM 类模块的核心价值不是“再做一次 AES”，而是：

```text
measurement
→ PCR/state register
→ key sealing
→ quote/sign
→ remote verification
```

因此它特别适合：

### Measured Boot

```text
hash(Bootloader)
hash(Kernel)
hash(RootFS)
hash(App)
hash(Model)
      ↓
 PCR / measurement state
```

### Sealed Key

只有当 PCR / platform state 满足策略时：
- 解封 model key；
- 解封 mission key；
- 解封 network credential。

### Remote Attestation

```text
Verifier nonce
→ TPM/TCM Quote
→ PCR + event log
→ Verifier appraisal
```

这是“身份”升级为“身份 + 当前状态”的关键。

### 国产可信密码模块标准

国家密码管理局已发布：
- GM/T 0011 可信计算可信密码支撑平台功能与接口规范；
- GM/T 0012-2020 可信计算可信密码模块接口规范；
- GM/T 0013 可信密码模块符合性检测规范（历史体系）；
- GM/T 0082-2020 可信密码模块保护轮廓；
- GM/T 0079-2020 可信计算平台直接匿名证明规范。

因此国内体系并不是只有“SM2/SM4 安全芯片”，已有可信计算/可信密码模块标准基础。

官方：
- https://www.oscca.gov.cn/sca/xwdt/2020-12/30/content_1060794.shtml
- https://www.oscca.gov.cn/sca/xxgk/2017-05/04/content_1012596.shtml

---

## 5. 商密安全芯片 / Secure Element：最适合做设备密码身份与密钥服务

对我们的产品，离散商密安全芯片的价值很明确：

- SM2 device private key；
- SM2 certificate identity；
- SM3 hash/HMAC；
- SM4 data/model key wrapping；
- TRNG；
- key lifecycle；
- non-exportable private key；
- certificate signing / mutual auth。

国家密码管理局的商用密码产品认证体系明确引用：
- SM2 / SM3 / SM4；
- GM/T 0028 密码模块安全技术要求；
- GM/T 0005/0062 随机性要求等。

官方：
- https://www.oscca.gov.cn/sca/xxgk/2017-05/04/content_1012612.shtml
- https://www.oscca.gov.cn/sca/xwdt/2025-03/27/content_1061246.shtml

### 但一个普通商密芯片不能自动替代 TPM/TCM

除非目标芯片明确实现：
- platform measurement registers；
- quote；
- sealed storage；
- attestation key；
- trusted boot measurement API；

否则：

```text
Security Chip
= identity + crypto + key protection

not automatically

= Trusted Platform Module
```

这是产品选型时必须问厂商的关键问题。

---

## 6. PSA 的启示：Trust Plane 应做成“安全服务”，而不只是芯片

Arm PSA 把底层 Root of Trust 抽象成：
- Crypto API；
- Secure Storage API；
- Attestation API；
- Firmware Update API。

这是很值得我们借鉴的产品思想。

对于无人智算平台，可以定义自己的：

```text
Trust Service API

/device/identity
/crypto/sign
/crypto/encrypt
/key/unseal
/model/verify
/platform/measure
/platform/attest
/update/verify
/security/event
```

上层 ROS2 / mission / AI runtime 不直接知道底层究竟是：
- eFuse；
- TEE；
- 商密 SE；
- TPM/TCM。

由 Trust Service 统一抽象。

这样未来更换 SoC 或安全芯片，不需要重写全部业务软件。

Arm 官方：
https://www.arm.com/architecture/security-features/platform-security

---

## 7. 四种实施组合

## Option A — SoC-only

```text
SoC
├─ eFuse / OTP
├─ Secure Boot
├─ TrustZone / OP-TEE
├─ HW Crypto
└─ encrypted storage
```

### 优点
- BOM 低；
- 面积小；
- 性能路径短。

### 风险
- 国产密码/认证能力可能不足；
- device identity/provisioning 依赖 SoC vendor；
- attestation 能力不一定存在；
- SoC 被替换时产品安全软件耦合大。

适用：
低成本 P0 产品。

---

## Option B — SoC + 商密安全芯片（推荐 P0 基线）

```text
SoC:
Secure Boot + TrustZone + Linux

Discrete Crypto/SE:
SM2/SM3/SM4/TRNG
Device Identity
Private Key
Model/Mission Key wrapping
```

### 优点
- 很符合现有密码技术积累；
- 设备身份与 AI SoC 解耦；
- 可做商密认证；
- AI SoC 替换后 identity/PKI 体系可保持稳定。

### 能实现
- Secure Boot；
- Hardware-backed device identity；
- SM crypto；
- model signature verification；
- encrypted storage key protection；
- mutual authentication。

### 缺口
如果 SE 没有 TCM/TPM 类 measurement/quote：
- remote attestation 要自己设计；
- 无法仅靠 SE 自动证明 kernel/model 状态。

适用：
**安全可信无人智算产品第一版最现实路线。**

---

## Option C — SoC + TPM/TCM

```text
SoC Secure Boot
      +
TPM/TCM
├─ PCR / Measurement
├─ Sealed Key
├─ Attestation
└─ Device Identity
```

### 优点
- Measured Boot / Attestation 清晰；
- Linux IMA 生态成熟；
- 适合 Fleet Zero-Trust / device posture。

### 风险
- 如果 TPM 不支持目标商密体系，又需要独立密码芯片；
- 可能形成双安全器件；
- BSP、TSS、provisioning、CA/Verifier 软件增加复杂度。

适用：
P1 高安全/可信准入产品。

---

## Option D — SoC + TCM/商密可信模块 + TEE（优先研究的一体化路线）

理想状态：

```text
SoC
├─ Secure Boot
├─ TrustZone / TEE
├─ IOMMU / OS isolation
└─ AI Compute

Trusted Crypto Module
├─ SM2/SM3/SM4/TRNG
├─ Device Identity
├─ Measurement / PCR-like state
├─ Sealed Key
└─ Attestation
```

如果国产可信密码模块能够同时满足：
- 商密；
- TCM measurement；
- quote/attestation；
- sealed key；

则有机会把 Option B + C 合并，避免“SE + TPM 两颗芯片”。

这是下一轮安全器件调研重点。

---

## 8. 推荐软件分层

```text
Application
├─ ROS2
├─ Perception
├─ VIO/SLAM
├─ Planner
└─ Fleet Agent

Security Middleware
├─ Identity Service
├─ Model Trust Service
├─ Attestation Agent
├─ Key Service
├─ Audit Service
└─ Update Verification

Linux Normal World
├─ IMA / dm-verity / fs-verity
├─ SELinux/AppArmor
├─ Container
└─ Device drivers

TEE / Secure World
├─ Key wrapper
├─ Attestation signer
├─ Sensitive policy
└─ Secure storage

Hardware
├─ SoC Secure Boot / eFuse
└─ SE / TPM / TCM
```

---

## 9. 推荐第一版 Trust Flow

### Manufacturing / Provisioning

```text
Generate Device Key
→ inject into Security Module
→ issue Device Certificate
→ bind Board SN / SoC ID / Module ID
→ register Fleet inventory
→ provision boot trust
```

### Boot

```text
SoC Secure Boot
→ Linux
→ IMA / application measurement
→ Trust Agent
→ verify Model Manifest
```

### Mission

P0：
```text
Device Certificate
→ mutual authentication
→ mission authorization
```

P1：
```text
Device Certificate
+ Attestation Evidence
→ Verifier
→ policy pass
→ release Mission/Model Credential
```

---

## 10. 对六摄像头产品的建议

### P0 原型

优先采用：

```text
Integrated SoC
+ Secure Boot
+ TrustZone/TEE
+ Discrete SM Crypto/SE
+ Device Certificate
+ Signed Model Manifest
+ Data Encryption
+ ROS2/DDS Security
+ FCU Authentication
```

原因：
- 工程边界可控；
- 不依赖立刻解决完整 attestation；
- 能形成明显区别于普通 AI Box 的产品能力；
- 可直接利用现有密码技术资产。

### P1 原型

增加：

```text
Linux IMA
+ TPM/TCM measurement
+ Remote Attestation
+ Attestation-gated Model/Mission Key
+ Fleet Verifier
```

### P2

研究：
- NPU execution measurement；
- NPU/DDR model confidentiality；
- secure sensor path；
- continuous attestation。

---

## 11. 下一步器件调研问题清单

对每一颗国产密码/可信芯片必须询问：

1. 是否支持 SM2 / SM3 / SM4 / TRNG；
2. 私钥是否不可导出；
3. 是否有 device unique key / certificate provisioning；
4. 是否支持 TCM/TPM 类 PCR；
5. 是否支持 Quote / Attestation；
6. 是否支持 sealed key；
7. 是否支持 monotonic counter / anti-rollback；
8. host interface：SPI/I2C/USB/PCIe；
9. Linux driver / TSS / PKCS#11；
10. ROS2 / OpenSSL / GmSSL integration；
11. 量产烧录与证书注入；
12. 密码产品认证状态；
13. 温度/功耗/封装；
14. 防物理攻击等级；
15. 供货周期。

只有回答清楚 4–7，才能判断它是：
- 普通安全芯片；
- 密码模块；
- 还是可以承担 Remote Attestation 的可信密码模块。


## 12. 已发现的现实一体化候选：NS350 / Z32H330TC

进一步公开资料检索已经确认，国产可信计算芯片中存在能够同时覆盖 **TCM/TPM + SM2/SM3/SM4 + PCR/度量 + 嵌入式 Arm** 的产品。

重点参考：
- 国民技术 NS350：TCM 2.0 / TPM 2.0 兼容、SM2/SM3/SM4、24 个 SM3 PCR、EK 证书、SPI/I2C、Arm/Linux/嵌入式；
- Z32H330TC：官方明确给出平台完整性保护和平台远程身份证明。

详见：
- `research/products/trusted-crypto-module-candidates.md`
- `data/product-specs/trusted-crypto-module-candidates.csv`

这证明 Option D 不是纯概念路线。但是否能在 RK3588 / A1000 等目标 BSP 上实现 Linux IMA + TCM/TPM Quote + model measurement，仍需开发板/SDK 实测后才能升级为 Confirmed-fit。
