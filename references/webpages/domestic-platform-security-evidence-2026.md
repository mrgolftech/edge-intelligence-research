# 国产候选平台 Security Gate 证据补充（2026-09）

> 目的：对当前无人装备候选平台的安全可信能力做 SKU 级证据审计。  
> 原则：功能安全 != 网络安全/可信计算；同厂商不同 SKU 不继承能力；只有公开官方材料能确认的功能才标 Confirmed。

## 1. RK3588 / RK3588J

### 已确认

**SPEC/VENDOR**
- Rockchip 官方资料明确列出 RK3588 系列通过 PSA Certified Level 1。
- RK3588 系列安全子系统包含：
  - Arm TrustZone 隔离；
  - 硬件密码加速器；
  - Secure OTP；
  - Secure Boot。
- Rockchip 2025 工业方案资料继续明确 RK3588 / RK3576 / RK3568 平台提供全链路 Secure Boot、TrustZone、加解密引擎。
- Rockchip 工业安全方案还公开描述磁盘加密、固件加密、防回滚、OP-TEE、安全 OTP、AES/RSA/SM4 等能力，但该条属于 Rockchip 工业平台能力描述，不应自动推导所有第三方 RK3588 BSP 默认启用这些能力。

### Gate 更新

| Gate | 状态 | 判断 |
|---|---|---|
| SG-A Root of Trust | Candidate/Confirmed primitive | Secure OTP + TrustZone 可作为 RoT 构件 |
| SG-B Boot Integrity | Confirmed | 官方明确 Secure Boot |
| SG-C Key & Identity | Candidate | Secure OTP 已确认；设备 PKI/provisioning 方案需产品实现 |
| SG-D Runtime Isolation | Confirmed primitive | TrustZone；OP-TEE 是否在目标 BSP/SKU 完整可用需板级确认 |
| SG-E Attestation | GAP | 未找到 RK3588 官方通用 remote attestation 方案 |
| SG-F AI Artifact | GAP/Product work | 可做签名/加密，但 NPU model execution trust 未公开证明 |
| SG-G Communication | Host software | 可由 Linux/ROS2/网络栈实现 |
| SG-H Physical Capture | Candidate | Secure Boot/OTP/磁盘加密路线存在；debug lock/量产配置需验证 |
| SG-I Lifecycle | Partial | 官方公开防回滚能力，但量产 update/recovery 流程需产品化 |
| SG-J Domestic Crypto | Partial/Confirmed primitive | 官方资料列出 SM4 硬件支持；SM2/SM3/密码模块认证需单独确认 |

### 工程判断

RK3588 已不能继续写为“安全能力未知”。它具备构建 P0 安全智算节点所需的一部分基础原语，但 **Remote Attestation、AI model runtime trust、设备证书/密钥生命周期** 仍需自研或外接 SE/TPM/密码芯片。

官方来源：
- https://www.rock-chips.com/a/cn/news/rockchip/2022/0818/1687.html
- https://www.rock-chips.com/a/cn/news/rockchip/2025/0321/2057.html

---

## 2. Black Sesame 华山 A1000 / A1000 Pro

### 已确认

**SPEC/VENDOR**
A1000 官方产品页明确公开：
- CPU TrustZone；
- 独立功能安全/信息安全岛；
- Secure Boot；
- 片内 OTP，用于密钥存储和生命周期管理；
- 双核锁步安全处理器、ECC/Parity 等安全机制。

A1000 官方软件材料还公开：
- SDK 提供 ATF（Arm Trusted Firmware）；
- 提供 Open-TEE 组件。

A1000 Pro 官方页同样公开：
- Arm CPU TrustZone；
- ASIL-D safety island；
- 但产品页对 secure boot / OTP 的描述不如 A1000 页面完整，因此不要自动把所有 A1000 条目复制到 A1000 Pro。

### Gate 更新（A1000）

| Gate | 状态 | 判断 |
|---|---|---|
| SG-A Root of Trust | Candidate/Confirmed primitive | OTP + TrustZone + security island |
| SG-B Boot Integrity | Confirmed | Secure Boot |
| SG-C Key & Identity | Partial | OTP 明确用于 key storage/lifecycle；PKI provisioning 未公开 |
| SG-D Runtime Isolation | Confirmed primitive | TrustZone + ATF + Open-TEE |
| SG-E Attestation | GAP | 未找到 remote attestation 公开方案 |
| SG-F AI Artifact | GAP | 未找到 NN model signing/measurement/execution attestation |
| SG-G Communication | Product software | 需上层实现 |
| SG-H Physical Capture | Partial | OTP/secure boot 有帮助；debug/storage encryption 需补证 |
| SG-I Lifecycle | GAP/Partial | secure boot 有证据，secure update/anti-rollback 需补证 |
| SG-J Domestic Crypto | GAP | 未找到产品页对 SM2/SM3/SM4 与认证的明确 SKU 级说明 |

### 工程判断

A1000 是目前国产候选中公开材料里 **“计算 SoC + TrustZone + TEE + Secure Boot + OTP”链条较完整** 的案例之一，值得作为“高算力 SoC 内建安全岛”的参考架构。但它是车规 ADAS 芯片，生态、Camera、OS 和无人机产品化适配必须与安全能力分开评价。

官方来源：
- https://www.blacksesame.com.cn/zh/huashan-a1000/
- https://www.blacksesame.com/zh/list_11/829.html
- https://www.blacksesame.com.cn/zh/huashan-a1000pro/

---

## 3. Horizon Journey 6

### 已确认

**SPEC/VENDOR**
- Journey 6 官方公开强功能安全能力：ASIL-B(D) Compute、ASIL-D MCU、AEC-Q100 Grade 2。
- 2026 年 Journey 6 算法工具链运行时通过 ASIL-B、开发工具通过 ASIL-D 功能安全认证。
- Horizon 有产品安全漏洞响应/披露机制，Journey 6 在其公开产品安全范围内。

### 不能混淆

上述资料主要证明 **Functional Safety / Product Security Process**，并不能自动证明：
- Secure Boot；
- hardware RoT；
- TEE；
- key storage；
- remote attestation；
- AI model signing；
- storage encryption。

开发者社区关于 Journey 6 的“安全机制”公开回答主要仍是 lockstep、CRC、ECC、PVT、watchdog、FCHM 等功能安全机制。

### Gate 更新

SG-A~SG-J 中除“安全开发/功能安全体系”外，具体可信计算 Gate 暂时保持 **GAP**。

### 工程判断

Journey 6 是一个很好的反例：报告中必须单独区分：

```text
Safety:
故障、失效、随机硬件错误 → ISO 26262 / ASIL

Security / Trust:
恶意修改、身份冒充、密钥窃取、软件替换 → Secure Boot / RoT / TEE / Attestation
```

官方来源：
- https://www.horizon.auto/solutions/horizon-journey/horizon-journey6
- https://www.horizon.auto/news/press/455
- https://www.horizon.auto/en/legal/security

---

## 4. Huawei Atlas 200I A2

### 已确认

**OFFICIAL DOC**
Atlas 200I A2 当前官方驱动开发文档明确描述安全启动：
- BSBC（BootROM Secure Boot Code）为根；
- eFuse 保存根公钥 Hash；
- hboot1-a → hboot1-b → 后续固件逐级 RSA/CMS 验证；
- 构建关键固件安全可信链。

软件包发布流程还要求下载并验证 OpenPGP 数字签名，以确认软件包传输/存储未被篡改。

### Gate 更新

| Gate | 状态 | 判断 |
|---|---|---|
| SG-A Root of Trust | Confirmed | BSBC + eFuse public-key hash |
| SG-B Boot Integrity | Confirmed | 明确多级 secure boot chain |
| SG-C Key & Identity | Partial/GAP | eFuse 证明 boot root；设备身份/客户 key lifecycle 未确认 |
| SG-D Runtime Isolation | GAP | 本轮未找到 SKU 级 TEE 资料 |
| SG-E Attestation | GAP | 未找到 remote attestation |
| SG-F AI Artifact | GAP | 固件可信不等于模型可信 |
| SG-G Communication | Host/software | 需独立设计 |
| SG-H Physical Capture | Partial | eFuse/secure boot；storage/debug 仍需补证 |
| SG-I Lifecycle | Partial | 包签名与升级工具存在；anti-rollback/recovery 需补证 |
| SG-J Domestic Crypto | GAP | 本轮未找到 SKU 级商密可信服务公开证据 |

官方来源：
- https://www.hiascend.com/document/detail/zh/Atlas%20200I%20A2/2550/RC/driverdevelopmentguide/atlasdg_11_0136.html
- https://www.hiascend.com/document/detail/zh/Atlas%20200I%20A2/24.1.RC2/RC/driverdevelopmentguide/atlasdg_11_0003.html

---

## 5. SOPHGO BM1688

### 已确认

BM1688 官方 SOPHONSDK 文档可确认：
- BootROM → bootloader → Linux 的启动软件结构；
- boot 分区 / recovery 分区 / read-only root 分区；
- SDK 支持 SD 卡整盘重刷、USB 烧录、bootloader/kernel 替换；
- OEM/SN/MAC 等产品信息存储方式。

### 当前缺口

本轮没有在 BM1688 官方公开文档中找到足以升级以下 Gate 的明确证据：
- Secure Boot；
- TrustZone/TEE；
- secure OTP / HUK；
- remote attestation；
- anti-rollback；
- model artifact trust。

因此继续保持 GAP，不能从 Cortex-A 或其他 Sophgo 产品推断。

官方来源：
- https://doc.sophgo.com/bm1688_sdk-docs/v2.1/docs_latest_release/
- https://doc.sophgo.com/bm1688_sdk-docs/v1.8/docs_latest_release/docs/athena2-img/4_system_software_composition.html

---

## 6. Houmo LQ50 / 独立 AI Accelerator

截至本轮公开检索，未找到 LQ50 SKU 级：
- secure firmware chain；
- accelerator RoT；
- device identity；
- model encryption/measurement；
- PCIe endpoint attestation；
- secure update；
- anti-rollback。

继续标记 GAP。

### 特别注意

对于独立加速卡，安全边界比 Integrated SoC 更复杂：

```text
Host RoT / Secure Boot
→ Host driver
→ PCIe
→ Accelerator firmware
→ Device memory / model
```

因此“Host 安全”不能自动证明“Accelerator 安全”。

后续需要厂商补充：
- firmware signature；
- PCIe DMA/IOMMU；
- device firmware update；
- model memory boundary；
- device unique identity；
- host-device authentication。

---

## 7. 本轮结论

1. RK3588、A1000、Atlas 200I A2 已找到明确可信计算技术原语，不应继续统一标为 unknown。
2. Journey 6 的公开安全证据当前主要属于功能安全，不能冒充 cybersecurity/trusted-computing 证据。
3. BM1688 当前可以确认启动/恢复结构，但安全启动等关键可信能力仍是 GAP。
4. 独立 AI accelerator 的“Host + Card 双信任域”是后续安全调研的重要新增问题。
5. 国产平台下一步真正需要补的不是更多 TOPS，而是：
   - device identity/provisioning；
   - measured boot；
   - attestation；
   - AI artifact trust；
   - secure update/rollback；
   - NPU/GPU/PCIe data-path trust；
   - 商密服务集成。
