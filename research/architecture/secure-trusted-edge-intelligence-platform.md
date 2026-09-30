# 安全可信型无人装备端侧智能计算平台：需求、技术架构与证据基线

> 状态：Phase 3 扩展研究 / v0.1  
> 日期：2026-09-30  
> 证据标记：FACT=已有可靠资料；VENDOR=厂商宣称；PAPER=论文/研究；INFER=工程推断；GAP=公开证据不足

## 1. 研究问题

本研究不是在现有 AI Box 上简单增加“密码芯片”，而是回答：

> 面向 UAV / UGV / AMR / USV / 机器人等无人装备，如何把端侧 AI 计算、实时控制链、设备身份、密码能力、软件/模型完整性、数据保护、通信安全、远程可信证明、失陷处置和生命周期管理整合为一套可产品化的安全可信智能计算平台？

研究主线由原有：

```text
Mission → Workload → Resource → Architecture → Platform
```

扩展为：

```text
Mission + Threat Model
→ AI/RT Workload + Trust/Security Requirement
→ Compute Resource + Security Resource
→ Compute Architecture + Trust Architecture
→ Platform + Crypto/Root-of-Trust
→ Verification / Lifecycle / Fleet Policy
```

安全可信能力不是新的 W10 workload，也不是新的自主等级，而是横跨 W1–W9 与 C1–C5 的系统属性。

---

## 2. 当前可确认的行业事实

### 2.1 无人系统存在真实的身份、命令完整性和数据保护问题

**FACT**：PX4 当前生产安全文档明确指出，默认 MAVLink 接口面向开发是开放的，生产部署需要额外安全加固；MAVLink 2 Signing 提供消息来源认证/完整性，但不加密 payload。PX4 还提供 Secure Boot、Log Encryption、Read-Only Parameters 等能力入口。

工程含义：

- 仅有消息签名不能解决任务数据/视频保密；
- 共享密钥若以普通文件方式保存，物理捕获后仍可能暴露；
- 飞控、伴随计算机、地面站、任务载荷之间需要显式信任边界。

### 2.2 ROS 2 / DDS 已具备认证、授权、加密机制，但“节点身份可信”仍可继续强化

**FACT**：ROS 2 的 DDS-Security 集成支持 PKI 身份认证、DDS access control 和 AES-GCM/GMAC 加密/认证；SROS 2 policy 支持按 topic/service/action 对身份授予权限，并强调 deny-by-default、最小权限和权限隔离。

**PAPER**：2024 ARES 的 DDS Security+ 研究把 TPM Remote Attestation 集成到 DDS 安全握手，并将建立的安全通道与被证明的软件栈绑定。这证明“只有运行批准软件栈的 DDS/ROS 节点才进入可信通信域”具有工程可行性。

### 2.3 无人机产品已把可信计算机制引入整机安全

**VENDOR/CASE**：

- DJI Drone Security White Paper v3.1：公开描述 TEE、RPMB Secure Storage、Secure Boot、Secure Update、系统加固、日志/媒体数据安全与通信安全；BootROM→bootloader→OS/flight firmware 构成签名/加密启动链。
- Skydio：公开描述 Secure/Trusted Boot、签名软件/固件更新、AES-256 数据保护、FIPS 140-3 validated encryption；Dock 使用 TPM 保存密钥；部分证据数据在采集点进行 SHA-256 哈希，用于后续完整性验证。
- AuterionOS / Skynode：近期发行记录显示正在 rollout full encryption 与 Secure Boot，并强化 bootloader、关闭 production image 的默认 debug console。

这些案例说明安全可信能力已进入无人装备产品，而不是纯理论要求。

### 2.4 端侧 AI/机器人 SoC 已出现可复用的安全硬件基础

**FACT/VENDOR**：

- NVIDIA Jetson：Secure Boot、OP-TEE、Secure Storage、Firmware TPM、Rollback Protection、LUKS disk encryption；新版本支持 fTPM provisioning，需要每设备唯一身份与 EK certificate 才能建立可信 attestation identity。
- Qualcomm QRB5165 / Robotics RB5：官方列出 Secure Processing Unit、hardware root of trust、TEE、Secure Boot、camera security，并在 RB5 发布资料中列出 secure token 用于 remote attestation / secure device provisioning。
- AMD Kria K26 SOM：官方 2026 datasheet 列出片上安全硬件 + 板载 TPM，可支持 tamper monitoring、secure boot、measured boot 和硬件密码加速。
- NXP i.MX 95：EdgeLock Secure Enclave（Advanced Profile），官方列出 hardware root of trust、secure boot/debug/update、认证/加密能力，并开始支持 PQC 相关机制。

**GAP**：对于 IQ-9075、RK3588、BM1688、后摩 LQ50、Hailo、Metis 等具体 SKU，不能因为同厂商其他产品存在安全机制而跨 SKU 推断；需要逐 SKU 建立证据。

---

## 3. 威胁模型：安全可信平台需要保护什么

采用 ROS 2 Threat Model、PX4 security guidance、CISA UAS guidance、无人机安全产品案例，并结合无人装备工程特点，可建立以下第一版威胁面。

### T1 — 非法设备 / 节点接入

攻击者伪装成合法无人机、飞控、伴随计算节点、ROS 2 node、地面站或载荷设备。

需要：设备级硬件身份、证书/密钥、双向认证、最小权限。

### T2 — 固件 / OS / 应用被替换

攻击者修改 bootloader、kernel、runtime、ROS node、飞控固件或 mission software。

需要：Secure Boot + Measured Boot + runtime integrity + anti-rollback。

### T3 — AI 模型 / 参数被替换

攻击者替换检测、VIO、VLM/VLA 模型，修改权重、配置、阈值或 planner 参数。

需要：模型包签名、hash/manifest、版本/授权绑定、加载前验证；运行态证明仍需单独设计。

### T4 — 敏感数据泄露

包括图像/视频、地图、任务航线、模型、日志、目标信息、密钥等。

需要：at-rest encryption、secure storage、in-transit encryption、数据流策略。

### T5 — 控制命令注入 / Topic 越权

恶意节点发布控制 topic、MAVLink command、参数修改、mission upload 等。

需要：身份认证、topic/service/action ACL、命令授权、链路认证加密。

### T6 — 物理捕获 / 拆卸

无人装备丢失或被获取后读取 eMMC/NVMe、调试口、存储器、密钥、模型与任务数据。

需要：debug lock、secure key storage、全盘/分区加密、tamper event、失陷后密钥撤销/策略降级。

### T7 — 恶意或失陷应用横向移动

ROS/DDS 安全只控制 middleware 通信并不足以覆盖 raw socket、shared memory、file、pipe 等旁路。

**PAPER**：Privaros (ACM CCS 2020) 用 ROS + OS mandatory access control 同时执行信息流策略，说明中间件安全需要和 Linux/OS 级强制访问控制组合。

### T8 — 不可信软件仍持有合法证书

证书证明“它是谁”，不等于证明“它正在运行什么”。

需要：Measured Boot / IMA / TPM Quote / TEE Attestation，把身份与软件状态绑定。

### T9 — 恶意/回滚更新

需要：signed manifest、版本/序列控制、anti-rollback、A/B recovery；可参考 NIST SP 800-193、IETF SUIT、Uptane 的保护/验证/恢复思路。

### T10 — 编队 / Fleet 中的失陷节点

多机协同时，一个合法但已失陷节点可能继续进入共享感知、任务分配和协同决策。

需要：持续 device posture / attestation、证书撤销、任务级授权、隔离与降级。

---

## 4. 安全可信能力向量（不是等级）

建议后续产品和平台评估使用以下 Capability Vector，而不是“安全 L1–L5”。

| ID | 能力 | 最小实现 |
|---|---|---|
| S1 | Hardware Root of Trust | OTP/eFuse/HUK/TPM/SE/secure enclave 中至少一种不可软件替换的根 |
| S2 | Device Identity & Key | 每设备唯一身份、私钥不可明文导出、生命周期 provisioning |
| S3 | Secure Boot & Anti-Rollback | 逐级签名验证、生产密钥、版本回滚控制 |
| S4 | Measured Boot / Runtime Integrity | 启动/关键运行组件度量，形成可验证 evidence |
| S5 | Remote Attestation | Attester–Verifier–Relying Party 模型，带 freshness 和 policy appraisal |
| S6 | Secure Storage / Data Protection | 密钥安全存储、数据/日志/模型 at-rest encryption |
| S7 | Trusted Runtime / Isolation | TEE / process sandbox / container / SELinux/AppArmor / enclave policy |
| S8 | Secure Communication & Access Control | ROS 2/DDS、FCU、GCS、Fleet 链路身份认证、加密和最小权限 |
| S9 | Secure Update & Recovery | signed manifest、anti-rollback、A/B 或恢复路径、撤销机制 |
| S10 | AI Artifact Trust | 模型/配置/算法包签名、hash、版本、授权与 provenance |
| S11 | Physical Capture Resistance | debug lock、tamper detect、storage encryption、失陷密钥策略 |
| S12 | Fleet Trust Management | CA/KMS/Verifier/policy/revocation/设备状态准入 |

S1–S12 是可组合能力，不表示高低顺序。

---

## 5. 建议的系统技术架构

### 5.1 Trust Plane 与 Compute Plane 分离

```text
                 Fleet / Ground Trust Services
       ┌────────────────────────────────────────┐
       │ CA / KMS / Attestation Verifier       │
       │ Device Inventory / Policy / Revocation │
       │ Signed Update / Model Repository       │
       └────────────────┬───────────────────────┘
                        │ identity / evidence / policy
                        ▼
┌────────────────────────────────────────────────────────────┐
│           Secure / Trusted Edge Intelligence Node          │
│                                                            │
│  Trust Plane                                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ SE / TPM / fTPM / TEE / Secure Enclave             │  │
│  │ HUK / TRNG / Key / Device ID / Attestation Key      │  │
│  └──────────────────────────────────────────────────────┘  │
│        │                    │                   │            │
│        ▼                    ▼                   ▼            │
│  Secure Boot         Secure Storage       Attestation       │
│  Measured Boot       Crypto Service       Model Verify      │
│                                                            │
│  Compute Plane                                             │
│  ┌────────┬────────┬────────┬──────────┬────────────────┐  │
│  │ CPU    │ GPU    │ NPU    │ ISP/VPU  │ MCU/RT domain  │  │
│  └────────┴────────┴────────┴──────────┴────────────────┘  │
│        │ ROS2 / containers / AI runtime / VIO / planner     │
│        │ + MAC / least privilege / integrity enforcement    │
└────────┬───────────────────────────────┬────────────────────┘
         │                               │
       FCU / MCU                    Sensor / Payload
  signed/auth channel           camera/lidar/IMU/etc.
         │                               │
         └──────────────┬────────────────┘
                        ▼
                  Vehicle / Mission
```

### 5.2 Trust Plane 的关键工程边界

1. **密码模块不能等同于 TEE/TPM**  
   密码模块负责密钥和密码运算；TEE 提供隔离执行；TPM 更擅长度量、sealed key、quote/attestation。三者可重叠但不能概念替换。

2. **Secure Boot 不能等同于 Remote Attestation**  
   Secure Boot 是本地准入；Measured Boot/Attestation 用于远端判断“当前运行状态”。

3. **TEE 不能自动保护完整 AI data path**  
   GPU/NPU/ISP/DDR/DMA 是否处于可信/加密/隔离域必须逐 SoC 验证。TEE 能安全保存密钥，不代表模型解密到普通 DDR 后仍受保护。

4. **ROS 2 security 不能替代 OS-level sandbox/MAC**  
   Privaros 已证明应用可绕过 ROS API 通过 OS primitives 交换信息，因此需组合 DDS policy + Linux MAC/container/namespace 等机制。

5. **MAVLink Signing 不能替代保密链路**  
   Signing 只做认证/完整性；敏感数据仍应通过 link-layer security / VPN / IPsec / 安全数传等机制保护。

---

## 6. Remote Attestation 建议方案

采用 IETF RATS 术语：

```text
Attester (无人装备/智算节点)
     │ Evidence
     ▼
Verifier (可信验证服务)
     │ Attestation Result
     ▼
Relying Party (任务系统/地面站/Fleet Controller)
```

Evidence 第一版可考虑绑定：

- device identity / EK / cert；
- boot firmware measurement；
- kernel / initramfs；
- rootfs / container image digest；
- ROS 2 mission application；
- AI runtime version；
- model package hash + model ID + config hash；
- debug state；
- security policy version；
- nonce / freshness。

**INFER**：对于“任务开始前准入”，可以把 mission key / model decryption key / fleet credential 的释放绑定到 attestation result；这与 2025 NIST SP 1800-36 的“验证设备身份与 posture 后再下发网络凭据”模式一致，但在无人装备上的具体实现需自研验证。

### Linux 实现候选

- TPM/fTPM：PCR + Quote；
- Linux IMA：运行文件/配置度量；
- dm-verity / fs-verity：只读/文件完整性；
- OP-TEE TA：设备密钥、证明代理、策略关键逻辑；
- Security chip/SE：商密密钥和不可导出设备身份；
- 后台 Verifier：reference values + appraisal policy。

---

## 7. AI 模型可信：应如何定义，哪些还不能声称

### 7.1 当前可以工程定义的能力

**INFER，可直接进入产品需求：**

```text
Model Package
= model binary/weights
+ preprocessing config
+ postprocessing config
+ runtime constraints
+ version
+ target accelerator
+ hash
+ signature
+ authorization metadata
```

加载流程：

```text
Signed Manifest
→ Verify Signer
→ Verify Model Hash
→ Verify Version / Target / Policy
→ Optional decrypt
→ Runtime load
→ Record measurement
→ Produce attestation evidence
```

这可以复用 Secure Software Update / signed manifest 的成熟思想。

### 7.2 当前仍是 GAP 的问题

- NPU 是否支持模型密文直接加载或执行；
- 模型解密后的权重是否长期存在普通 DDR；
- GPU/NPU DMA 能否读取其他安全域；
- model measurement 能否可靠绑定到“实际执行的 accelerator binary”；
- 编译器/量化器生成的离线模型是否需纳入供应链证明；
- VLM/LLM KV cache、prompt、视觉 embedding 的运行态保护。

这些必须逐平台测试，不能用“有 TEE”推断解决。

---

## 8. 安全通信与任务级访问控制

### 8.1 ROS 2 / DDS

推荐基线：

- per-device / per-enclave identity；
- identity CA + permissions CA；
- strict enforcement；
- deny by default；
- topic/service/action least privilege；
- sensitive topic encryption；
- identity key 放在 SE/TPM/TEE，而不是普通文件系统；
- 高安全版本研究 DDS Security+ 式 attestation-bound handshake。

### 8.2 FCU / MAVLink

推荐基线：

- MAVLink Signing 用于来源认证/完整性；
- 敏感链路增加底层加密；
- mission upload / parameter change / shell / file operation 需单独授权策略；
- signing key / link key 不落普通可移除介质；
- Companion Computer 与 FCU 的信任关系应纳入设备 provisioning。

### 8.3 Fleet / Multi-Agent

**INFER**：

```text
Identity
+ Device Posture
+ Mission Role
+ Time/Lifetime
→ Authorization
```

例如：一台无人机只有在证书有效、attestation 通过、mission role 匹配时，才能发布共享目标、接受编队任务或获取敏感模型。

---

## 9. Secure Update / Recovery

### 9.1 标准依据

- NIST SP 800-193：Protection / Detection / Recovery；
- IETF RFC 9019：firmware update architecture；
- RFC 9124：firmware manifest information model；
- Uptane：车辆软件更新中的 signed metadata、role separation、rollback/freeze/mix-and-match 等攻击防护思路。

### 9.2 产品化建议

至少定义：

- Root / signing key hierarchy；
- bootloader/OS/app/model 分级签名；
- version/sequence；
- device class / SKU compatibility；
- anti-rollback；
- A/B partition 或等价恢复策略；
- revoked key / revoked version；
- 更新日志可审计；
- 离线任务场景的可控更新。

AI model 应视作需要签名、版本、适配约束和授权的“关键软件资产”，而不是普通数据文件。

---

## 10. 物理失陷模型

无人装备与普通 edge server 的显著区别是：设备丢失、拆卸或被直接接触是现实工况。

建议最低能力：

- production debug interface disabled/locked；
- eMMC/NVMe encryption；
- device-unique key；
- key unwrap only after trusted boot；
- security state / tamper event；
- fleet revocation；
- lost-device credential revoke；
- 可选 tamper input / enclosure continuity；
- 敏感 mission/model key 短生命周期。

**CASE**：DJI 产品公开资料明确列出 production debug channel 关闭；Skydio Dock 使用 TPM 保护密钥；这些都是“physical capture must be considered”的产品证据。

---

## 11. 国产密码与产品特色

对于面向国内行业/专用场景的“安全智算单元”，可在通用 trusted-computing 架构之上增加国产密码适配层。

国家密码管理局当前认证/标准体系可确认：

- SM2：公钥密码/签名/密钥交换；
- SM3：杂凑；
- SM4：分组密码；
- GM/T 0028：密码模块安全技术要求；
- GM/T 0012 / 0013：可信密码模块接口与符合性测试相关规范；
- GM/T 0005-2021：随机性检测规范。

建议产品层把“密码算法”与“可信计算状态”分开定义：

```text
Crypto Service:
SM2/SM3/SM4/TRNG / certificate / key lifecycle

Trust Service:
device identity / boot measurement / runtime measurement / attestation /
policy / update / recovery
```

后续重点研究：如何用国产密码安全芯片或可信密码模块承载 device identity、attestation key、model key、mission key，并和 Linux/ROS 2/FCU 可信链对接。

---

## 12. 代表性案例映射

| 案例 | 已确认能力 | 说明 |
|---|---|---|
| DJI enterprise drone security | TEE、secure storage、secure boot/update、data/communication security | 完整无人机产品安全体系案例 |
| Skydio X10/Dock/Cloud | secure/trusted boot、signed update、FIPS crypto、TPM、evidence hashing | 无人机 + dock + cloud 端到端产品案例 |
| Auterion Skynode/AOS | encryption、secure boot、bootloader hardening | 飞控+mission computer 一体化安全演进 |
| PX4 | MAVLink signing、secure boot、log encryption、parameter hardening | 开源飞控工程安全基线 |
| ROS 2/SROS2 | PKI auth、ACL、encryption | 机器人/伴随计算 middleware 基线 |
| Privaros | ROS + OS mandatory access control、TEE attestation assumption | 学术系统：跨层信息流策略 |
| DDS Security+ | DDS security + TPM remote attestation | 学术系统：身份与软件状态绑定 |

---

## 13. 对“安全可信型无人装备端侧智能计算平台”的第一版产品定义

产品不应定义为：

> XX TOPS AI Box + 一颗安全芯片

而应定义为：

> 以异构端侧 AI 计算为基础、以硬件根信任和国产密码能力为信任锚点，向上形成设备身份、可信启动、模型/数据保护、可信运行、通信访问控制、远程证明、安全更新和无人装备失陷处置能力，并可接入 Fleet/指控系统进行可信准入和生命周期管理的无人装备可信智能计算平台。

### 最小可产品化能力包 P0

- Secure Boot；
- device unique identity；
- hardware-backed key；
- SM2/SM3/SM4/TRNG crypto service；
- encrypted storage；
- model package signature verification；
- production debug lock；
- ROS 2/DDS security integration；
- FCU link authentication；
- signed update + anti-rollback；
- security event/audit log。

### 增强能力包 P1

- Measured Boot；
- TPM/fTPM/TEE based remote attestation；
- model/config measurement；
- attestation-gated mission/model key release；
- ROS/DDS attestation-bound trust；
- fleet certificate/revocation；
- tamper input；
- lost-device policy。

### 高安全研究能力 P2（需验证，不作为当前成熟承诺）

- accelerator execution attestation；
- encrypted/isolated NPU model execution；
- sensor→ISP→DDR→NPU full data-path confidentiality；
- continuous runtime attestation；
- multi-agent posture-aware trust；
- confidential VLM/LLM runtime。

P0/P1/P2 是产品研发阶段建议，不是行业等级。

---

## 14. 对计算平台选型增加的 Security Gates

原七类 Architecture Gate 之外，建议增加横向 Security Gates：

| Gate | 问题 |
|---|---|
| SG-A Root of Trust | 是否有可用 RoT / HUK / SE / TPM / TEE |
| SG-B Boot Integrity | Secure/Measured Boot、anti-rollback 是否可产品化 |
| SG-C Key & Identity | 每设备 provisioning、key isolation、PKCS#11/crypto API |
| SG-D Runtime Isolation | TEE、IOMMU、MAC、container 等隔离边界 |
| SG-E Attestation | 能否产生可验证 evidence，支持 EK/AK/cert lifecycle |
| SG-F AI Artifact | model/package verify、secure storage、runtime measurement |
| SG-G Communication | ROS2/DDS、FCU、network security integration |
| SG-H Physical Capture | debug lock、storage encryption、tamper/lost-device |
| SG-I Lifecycle | signed update、recovery、revocation、fleet policy |
| SG-J Domestic Crypto | SM2/SM3/SM4/TRNG/密码模块适配能力 |

禁止把 SG-A~SG-J 做简单加权总分；输出 Confirmed / Candidate / GAP / Constraint。

---

## 15. Benchmark / 验证计划

安全功能也必须可测试，不能只看 datasheet。

### V-S1 Secure Boot
- 未签名 image；
- 错误签名；
- rollback image；
- boot failure recovery。

### V-S2 Device Identity / Key
- 每设备 ID 唯一性；
- private key 不可导出；
- key provisioning；
- revoke / re-provision。

### V-S3 Attestation
- 正常 software state；
- kernel/app/model 被修改；
- replay old evidence；
- debug mode；
- verifier policy change。

记录：attestation latency、CPU、网络、启动时间、失败模式。

### V-S4 Model Trust
- model hash mismatch；
- signature mismatch；
- version rollback；
- unauthorized model；
- config tamper。

### V-S5 ROS 2 Security
- unauthorized participant；
- unauthorized topic publish；
- stolen credential；
- changed software but valid credential（用于验证 attestation 增量价值）。

### V-S6 FCU/MAVLink
- unsigned / wrong signing key；
- replay；
- sensitive command authorization；
- encrypted vs non-encrypted link。

### V-S7 Physical Capture
- remove storage；
- offline disk read；
- debug port；
- lost-device certificate revoke；
- enclosure/tamper event。

### V-S8 Security–Performance Co-Run
与 C2 Visual Autonomy workload 同时运行：
- P95/P99 Frame Age；
- DDR/CPU overhead；
- ROS2 encryption overhead；
- attestation/update background task；
- thermal/power；
- 是否影响控制 deadline。

---

## 16. 当前关键工程判断

1. **FACT**：安全启动、TEE、磁盘加密等能力在主流平台/无人机中已存在，单项功能不构成足够差异化。
2. **FACT/PAPER**：身份认证可继续扩展为“身份 + 软件状态证明”，DDS + TPM remote attestation 已有研究实现。
3. **CASE**：无人机厂商正在把安全能力覆盖到 device/app/data/link/cloud，而不是只保护一颗芯片。
4. **INFER**：本项目最有差异化潜力的是把密码能力、可信身份、AI 模型保护、无人协议安全、失陷处置和 Fleet trust 做成一体化产品。
5. **GAP**：目前公开资料对“AI accelerator 实际执行状态如何证明”“模型解密后 DDR/NPU data path 如何保密”仍缺统一成熟方案，应列为中长期研发问题。
6. **INFER**：安全可信能力必须与现有 workload/resource 方法并列进入平台 Gate，而不是报告最后的附加章节。

---

## 17. 后续待研究

- 国产 AI SoC / accelerator 逐 SKU Security Gate 证据；
- 国产可信密码模块 / 安全芯片与 Linux TPM/PKCS#11/TEE 的组合方式；
- SM2/SM3/SM4 下的 ROS 2/DDS、TLS/TLCP 或安全数传适配；
- IMA + TPM/TEE + model manifest 的无人智算 attestation prototype；
- AI accelerator / IOMMU / secure memory path；
- 安全机制对 C1–C5 workload 的 CPU/DDR/latency/power 增量；
- 无人装备丢失后的 key revoke / zeroize / limited-function mode；
- fleet / swarm 中 posture-aware authorization；
- 安全与功能安全（safety）边界：安全功能故障不得破坏飞行安全闭环。

---

## References

### 标准 / 官方架构
- NIST SP 800-193, Platform Firmware Resiliency Guidelines: https://csrc.nist.gov/pubs/sp/800/193/final
- NIST SP 800-207, Zero Trust Architecture: https://csrc.nist.gov/pubs/sp/800/207/final
- NIST SP 1800-36, Trusted IoT Device Network-Layer Onboarding and Lifecycle Management: https://csrc.nist.gov/pubs/sp/1800/36/final
- IETF RFC 9334, RATS Architecture: https://www.rfc-editor.org/rfc/rfc9334.html
- IETF RFC 9019, Firmware Update Architecture for IoT: https://www.rfc-editor.org/rfc/rfc9019.html
- IETF RFC 9124, Firmware Manifest Information Model: https://www.rfc-editor.org/rfc/rfc9124.html
- TCG DICE Attestation Architecture: https://trustedcomputinggroup.org/resource/dice-attestation-architecture/
- TCG TPM 2.0 Library: https://trustedcomputinggroup.org/resource/tpm-library-specification/
- Arm Platform Security: https://www.arm.com/architecture/security-features/platform-security
- Uptane: https://uptane.org/docs/2.0.0/standard/uptane-standard

### 无人系统 / Middleware
- PX4 Security: https://docs.px4.io/main/en/security/
- PX4 MAVLink Security Hardening: https://docs.px4.io/main/en/mavlink/security_hardening
- PX4 MAVLink Message Signing: https://docs.px4.io/main/en/mavlink/message_signing
- ROS 2 DDS-Security Integration: https://design.ros2.org/articles/ros2_dds_security.html
- ROS 2 Access Control Policies: https://design.ros2.org/articles/ros2_access_control_policies.html
- ROS 2 Threat Model: https://design.ros2.org/articles/ros2_threat_model.html

### 产品 / 平台
- NVIDIA Jetson Security: https://docs.nvidia.com/jetson/archives/r38.4/DeveloperGuide/SD/Security.html
- NVIDIA Jetson fTPM Provisioning: https://docs.nvidia.com/jetson/archives/r39.2/DeveloperGuide/SD/Security/FirmwareTPM/Provisioning.html
- Qualcomm QRB5165: https://www.qualcomm.com/internet-of-things/products/q5-series/qrb5165
- AMD Kria K26 Security Features: https://docs.amd.com/r/en-US/ds987-k26-som/Security-Features
- NXP i.MX 95: https://www.nxp.com/products/i.MX95
- DJI Drone Security White Paper: https://www.dji.com/trust-center/resource/white-paper
- Skydio Security Trust Center: https://www.skydio.com/security-trust-center
- AuterionOS release/security notes: https://docs.auterion.com/

### 论文
- Wagner et al., “DDS Security+: Enhancing the Data Distribution Service with TPM-based Remote Attestation,” ARES 2024, DOI 10.1145/3664476.3670442.
- Beck et al., “Privaros: A Framework for Privacy-Compliant Delivery Drones,” ACM CCS 2020, DOI 10.1145/3372297.3417858.
- Dong et al., “Escorting the Confidentiality and Integrity of UAVs: What Exactly Can Trusted Execution Environment Offer?”, ACM Computing Surveys 58(3), 2026, DOI 10.1145/3763788.

### 国内密码规范
- 国家密码管理局标准规范查询：https://www.oscca.gov.cn/app-zxfw/zxfw/bzgfcx.jsp
- GM/T 0028 密码模块安全技术要求：https://www.oscca.gov.cn/sca/xxgk/2017-05/04/content_1012612.shtml
