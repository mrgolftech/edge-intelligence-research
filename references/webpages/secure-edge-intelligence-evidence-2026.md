# 安全可信无人装备端侧智能计算：证据索引（2026-09）

> 用途：为最终报告“安全可信计算”章节和产品 Security Gate 提供可追溯事实底稿。  
> 规则：CASE / SPEC / STANDARD / PAPER / VENDOR 与 INFER / GAP 分离。

## 1. 标准与通用可信计算

### NIST SP 800-193 — Platform Firmware Resiliency Guidelines
- 类型：STANDARD
- 机构：NIST
- 日期：2018
- URL：https://csrc.nist.gov/pubs/sp/800/193/final
- 关键事实：平台固件韧性应覆盖 Protection / Detection / Recovery。
- 支撑：Secure Boot、完整性检测、恢复链设计不能只做“签名启动”。

### NIST SP 800-207 — Zero Trust Architecture
- 类型：STANDARD
- 机构：NIST
- 日期：2020
- URL：https://csrc.nist.gov/pubs/sp/800/207/final
- 关键事实：不因网络位置或资产归属隐式授予信任，设备/主体在访问资源前应认证和授权。
- 支撑：Fleet / 指控系统的 identity + posture + policy 模型。

### NIST SP 1800-36 — Trusted IoT Device Onboarding
- 类型：STANDARD / PRACTICE GUIDE
- 机构：NIST NCCoE
- 日期：2025-11 final
- URL：https://csrc.nist.gov/pubs/sp/1800/36/final
- 关键事实：在下发网络凭据前验证设备身份与 security posture，并在生命周期中持续管理。
- 支撑：attestation-gated credential / mission access 的参考模式。

### IETF RFC 9334 — RATS Architecture
- 类型：STANDARD ARCHITECTURE
- 日期：2023
- URL：https://www.rfc-editor.org/rfc/rfc9334.html
- 关键事实：Attester / Verifier / Relying Party；Evidence / Attestation Result；freshness。
- 支撑：无人装备 Remote Attestation 术语和架构。

### TCG DICE Attestation Architecture
- 类型：SPEC
- 最新：v1.2 + Errata v1.0 r1, 2026-01
- URL：https://trustedcomputinggroup.org/resource/dice-attestation-architecture/
- 关键事实：定义 DICE layering attestation、evidence、endorsement、X.509 扩展。
- 支撑：轻量嵌入式设备 identity/attestation 路线。

### TCG TPM 2.0
- 类型：SPEC
- 最新：Version 185, 2026-03
- URL：https://trustedcomputinggroup.org/resource/tpm-library-specification/
- 关键事实：TPM 支持 sealed key、PCR measurement、Quote/attestation 等可信计算原语。
- 支撑：Measured Boot / IMA / Remote Attestation。

### Arm Platform Security / PSA
- 类型：SPEC / REFERENCE
- URL：https://www.arm.com/architecture/security-features/platform-security
- 关键事实：Crypto API、Secure Storage API、Attestation API、Firmware Update API。
- 支撑：MCU/嵌入式 Trust Plane 的 API 化思路。

## 2. 安全更新

### IETF RFC 9019
- 类型：STANDARD ARCHITECTURE
- URL：https://www.rfc-editor.org/rfc/rfc9019.html
- 关键事实：更新决策涉及 signer trust、image integrity、device applicability、sequence/rollback 等。
- 支撑：无人智算 firmware/model signed manifest。

### IETF RFC 9124
- 类型：STANDARD
- URL：https://www.rfc-editor.org/rfc/rfc9124.html
- 关键事实：定义 firmware manifest information model。
- 支撑：model package / update metadata 的可借鉴结构。

### Uptane 2.0
- 类型：INDUSTRY STANDARD
- URL：https://uptane.org/docs/2.0.0/standard/uptane-standard
- 关键事实：车辆软件更新的多角色 signed metadata、inventory、attack resilience。
- 支撑：无人系统安全 OTA 的参考，而非直接宣称 UAV 已采用。

## 3. 无人系统工程安全

### PX4 Security
- 类型：OFFICIAL
- URL：https://docs.px4.io/main/en/security/
- 关键事实：生产系统需要 integrator 主动加固；提供 MAVLink hardening、message signing、secure boot、log encryption 等入口。

### PX4 MAVLink Security Hardening
- 类型：OFFICIAL
- URL：https://docs.px4.io/main/en/mavlink/security_hardening
- 关键事实：默认 MAVLink 未认证未加密；生产部署可结合底层加密链路与 MAVLink signing。

### PX4 MAVLink Message Signing
- 类型：OFFICIAL
- URL：https://docs.px4.io/main/en/mavlink/message_signing
- 关键事实：Signing 做 authentication/integrity，不加密 payload；当前 PX4 指南描述 signing key 存在 SD card。
- 支撑：密码密钥应移出普通 removable storage 的产品机会。

### ROS 2 DDS-Security Integration
- 类型：OFFICIAL DESIGN
- URL：https://design.ros2.org/articles/ros2_dds_security.html
- 关键事实：PKI participant authentication、access control、AES-GCM/GMAC crypto；SROS2 用 per-enclave security artifacts。

### ROS 2 Access Control Policies
- 类型：OFFICIAL DESIGN
- URL：https://design.ros2.org/articles/ros2_access_control_policies.html
- 关键事实：deny by default、least privilege、privilege separation；按 topic/service/action 定义权限。

### ROS 2 Threat Model
- 类型：OFFICIAL DESIGN / DRAFT
- URL：https://design.ros2.org/articles/ros2_threat_model.html
- 关键事实：sensor privacy、actuator command integrity、robot behavior/data integrity、compute/sensor availability 均是机器人威胁面；文档建议 credentials 存入 secure enclave/RoT，并使用 sandbox。

## 4. 无人机产品案例

### DJI Drone Security White Paper v3.1
- 类型：VENDOR / CASE
- URL：https://www.dji.com/trust-center/resource/white-paper
- 关键能力：TEE、FIPS-certified crypto engine、RPMB secure storage、secure boot、secure update、system hardening、log/media security、communication security。
- 注意：厂商材料，具体 SKU/认证范围需按产品确认。

### Skydio Security Trust Center
- 类型：VENDOR / CASE
- URL：https://www.skydio.com/security-trust-center
- 关键能力：FIPS 140-3 validated encryption、signed updates、AES data protection、Dock TPM、capture evidence SHA-256 hashing、cloud identity/access controls。
- 支撑：设备+Dock+Cloud 的端到端安全产品化案例。

### Auterion Skynode / AuterionOS
- 类型：VENDOR / CASE
- URL：https://docs.auterion.com/
- 关键事实：AOS 近期 release notes 记录 full encryption rollout、secure boot rollout、bootloader hardening、production debug console disabled 等。
- 支撑：mission computer/flight platform 的安全演进。

### CISA UAS Security Guidance
- 类型：GOV GUIDANCE
- URL：https://www.cisa.gov/resources-tools/resources/secure-your-drone-privacy-and-data-protection-guidance
- 关键事实：UAS 数据在传输和存储中都应受保护；身份/数据管理/物理安全均属于 UAS 风险。
- 注意：操作侧 guidance，不是产品技术规范。

## 5. AI/Robot Platform Security

### NVIDIA Jetson Security
- 类型：SPEC / OFFICIAL DOC
- URL：https://docs.nvidia.com/jetson/archives/r38.4/DeveloperGuide/SD/Security.html
- 能力：Secure Boot、OP-TEE、Secure Storage、Firmware TPM、Rollback Protection、Disk Encryption。
- 关键补充：fTPM provisioning 文档明确 per-device unique ID + EK certificate 是可信 TPM identity / attestation 的基础。

### Qualcomm QRB5165 / Robotics RB5
- 类型：SPEC / VENDOR
- URL：https://www.qualcomm.com/internet-of-things/products/q5-series/qrb5165
- 能力：SPU、hardware root of trust、TEE、Secure Boot、camera security。
- RB5 launch：还明确提到 secure token 支持 remote attestation / secure device provisioning。
- 注意：不能外推到 IQ-9075。

### AMD Kria K26 SOM
- 类型：SPEC
- URL：https://docs.amd.com/r/en-US/ds987-k26-som/Security-Features
- 日期：datasheet rev 1.6, 2026-03
- 能力：MPSoC security + onboard TPM；secure boot、measured boot、tamper monitoring、crypto acceleration。

### NXP i.MX 95
- 类型：SPEC
- URL：https://www.nxp.com/products/i.MX95
- 2026 资料：EdgeLock Secure Enclave Advanced Profile；RoT、secure boot/debug/update、authentication/encryption，PQC 相关能力。
- 用途：安全架构参考；算力/Camera/AI workload 适配仍需独立评估。

## 6. 论文

### DDS Security+: TPM-based Remote Attestation
- 类型：PAPER
- 作者：Paul-Georg Wagner, Pascal Birnstill, Jürgen Beyerer
- 会议：ARES 2024
- DOI：10.1145/3664476.3670442
- 资料：https://publica.fraunhofer.de/entities/publication/2acdae72-58de-4469-9979-47a0e4ef6da2
- 结论：将 TPM remote attestation 透明集成到 DDS secure-channel handshake，并把 channel 绑定到 attested software stack。
- 支撑：ROS/DDS 节点“身份 + 软件状态”准入。

### Privaros
- 类型：PAPER / PROTOTYPE
- 作者：Rakesh Rajan Beck, Abhishek Vijeev, Vinod Ganapathy
- 会议：ACM CCS 2020
- DOI：10.1145/3372297.3417858
- 资料：https://www.csa.iisc.ac.in/~vg/papers/ccs2020/
- 结论：SROS alone 不能覆盖 raw socket/shared memory/file 等旁路；结合 ROS policy + Linux/OS MAC 可执行无人机数据流策略。实现于 Jetson TX2 + ROS2。
- 支撑：安全中间件必须和 OS isolation 组合。

### UAV + TEE Survey
- 类型：PAPER / SURVEY
- 作者：Wenyu Dong et al.
- 期刊：ACM Computing Surveys 58(3)
- 出版：2026
- DOI：10.1145/3763788
- 资料：https://researchers.mq.edu.au/en/publications/escorting-the-confidentiality-and-integrity-of-uavs-what-exactly-/
- 结论：系统综述 TEE 在 UAV confidentiality/integrity、secure storage、attestation、isolated execution 等方向的作用与限制。
- 支撑：TEE 是 UAV 安全的重要技术，但不是全系统安全的充分条件。

## 7. 国内密码规范

### 国家密码管理局标准查询
- URL：https://www.oscca.gov.cn/app-zxfw/zxfw/bzgfcx.jsp
- 相关：SM2/SM3/SM4、GM/T 0028、GM/T 0005 等。

### GM/T 0028
- 类型：STANDARD
- 名称：密码模块安全技术要求
- URL：https://www.oscca.gov.cn/sca/xxgk/2017-05/04/content_1012612.shtml
- 支撑：产品中的密码模块应按密码模块安全要求单独设计/评估。

### 商用密码产品认证目录（第二/第三批）
- URL：https://www.oscca.gov.cn/sca/xwdt/2022-07/14/content_1060931.shtml
- URL：https://www.oscca.gov.cn/sca/xwdt/2025-03/27/content_1061246.shtml
- 关键事实：认证目录引用 GM/T 0012 可信密码模块接口、GM/T 0028，以及 SM2/SM3/SM4、随机数检测等要求。

## 8. 当前明确 GAP

1. IQ-9075 的具体 RoT/TEE/attestation 能力公开证据仍需逐文档核。
2. RK3588 / BM1688 / Houmo LQ50 等国产候选产品的 secure boot / TEE / key storage / attestation 能力不能凭同厂或 Arm 架构推断。
3. 独立 AI accelerator 的 firmware authenticity、model confidentiality、PCIe DMA/IOMMU trust boundary 证据不足。
4. “有 TEE”不代表 NPU/GPU execution confidential。
5. AI model attestation 尚无跨平台统一工程标准，需采用 signed artifact + measurement + platform attestation 的组合方案验证。
6. 商密算法如何进入 ROS2/DDS、MAVLink/安全数传、TPM-like attestation，需要做协议/产品适配研究。
