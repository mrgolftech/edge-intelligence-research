# TPM/TCM + Linux IMA + Remote Attestation + ROS2/DDS + AI Model Integrity 参考资料链

> 日期：2026-09-30
> 目的：为安全可信型无人装备端侧智能计算平台建立可追溯的标准、官方实现、论文和开源工程证据链。

## 1. 核心结论

现有公开资料已经能够支撑以下完整技术链：

~~~text
Device/TCM Identity
→ Secure/Measured Boot
→ Linux IMA Runtime Measurement
→ PCR
→ TPM/TCM Quote + Nonce
→ Verifier / Reference Values / Policy
→ Attestation Result
→ ROS2/DDS / Mission / Model-Key Admission
~~~

AI 模型也可以进入该链：Linux IMA 的 FILE_CHECK + MAY_READ 能对普通读取文件进行度量，因此 model.rknn / model.engine / model.bin / manifest / config 都存在明确的测量入口。

当前主要 GAP 不在架构依据，而在：
- 国产 TCM 与 RK3588/国产 AI SoC BSP 的实机适配；
- SM2/SM3 Quote、IMA PCR 的国密软件栈闭环；
- model artifact 已度量到 NPU 实际执行内容之间的绑定；
- Security workload 对六摄 C2 P95/P99 Frame Age / power 的影响。

## 2. IETF RATS：远程证明顶层架构

### RFC 9334 — Remote ATtestation procedureS Architecture

- URL：https://www.rfc-editor.org/rfc/rfc9334.html
- 定义 Attester / Verifier / Relying Party / Evidence / Reference Values / Attestation Result。
- 明确 freshness、nonce、appraisal policy。

无人装备映射：

~~~text
UAV Edge Compute = Attester
Fleet/GCS Verifier = Verifier
Mission Controller = Relying Party
~~~

## 3. 国产可信密码模块标准

### GM/T 0012-2020《可信计算 可信密码模块接口规范》

- 国家密码管理局公告：
  https://www.oscca.gov.cn/sca/xwdt/2020-12/30/content_1060794.shtml
- 标准页面：
  https://www.oscca.gov.cn/sca/xxgk/2017-05/04/content_1012596.shtml

相关：
- GM/T 0079-2020 可信计算平台直接匿名证明规范；
- GM/T 0082-2020 可信密码模块保护轮廓。

说明国产可信计算已经存在 TCM + 证明 + 保护轮廓标准体系，而不仅是 SM2/SM3/SM4 算法。

## 4. Linux IMA：AI 模型运行时度量入口

IMA policy 支持：

~~~text
measure func=BPRM_CHECK
measure func=FILE_MMAP mask=MAY_EXEC
measure func=FILE_CHECK mask=MAY_READ
measure func=MODULE_CHECK
measure func=FIRMWARE_CHECK
~~~

参考：
- https://github.com/linux-integrity/ima-doc/blob/main/policy-syntax.rst
- https://github.com/torvalds/linux/blob/master/Documentation/ABI/testing/ima_policy

AI 权重和 accelerator compiled model 往往不是 executable，因此 FILE_CHECK/MAY_READ 非常重要。

可研究纳入：
- model.rknn / .engine / .onnx / .bin；
- model manifest；
- preprocessing/postprocessing config；
- planner config。

边界：IMA 证明文件访问时的内容 hash，不自动证明 NPU 最终执行微码与该 artifact 一一对应。

## 5. TPM Quote / PCR 工具链

### tpm2_quote
https://github.com/tpm2-software/tpm2-tools/blob/master/man/tpm2_quote.1.md

支持 PCR bank/index、Attestation Key signature、nonce/qualification。

### tpm2_checkquote
https://github.com/tpm2-software/tpm2-tools/blob/master/man/tpm2_checkquote.1.md

验证 Quote signature、PCR values、nonce。

### PCR Policy / sealed key
https://github.com/tpm2-software/tpm2-tools/blob/master/man/tpm2_policypcr.1.md

可实现：

~~~text
Trusted PCR State
→ unseal Model Key / Mission Key
~~~

## 6. Keylime：最接近本项目目标的开源参考实现

- 项目：https://github.com/keylime/keylime
- CNCF：https://www.cncf.io/projects/keylime/

Keylime 提供：
- Remote Boot Attestation；
- Linux IMA Runtime Integrity Monitoring；
- Hardware-rooted identity；
- Secure payload provisioning；
- Revocation；
- Verifier / Registrar / Agent。

典型链路：

~~~text
Linux IMA
→ Measurement List
→ PCR 10
→ TPM Quote
→ Keylime Verifier
→ Runtime Policy
→ Pass / Failed
~~~

Runtime IMA：
https://github.com/keylime/keylime-docs/blob/master/docs/user_guide/runtime_ima.rst

Keylime demo IMA policy 已包含：

~~~text
measure func=FILE_CHECK mask=MAY_READ uid=0
~~~

资料：
https://github.com/keylime/keylime/blob/master/demo/ima-policies/ima-policy-default

Verifier API 可处理 nonce、Quote、AK/EK、PCR policy、IMA runtime policy、IMA measurement list 和 measured boot log：
https://keylime.readthedocs.io/en/latest/rest_apis/2_4/verifier.html

2026 年 Keylime 仍持续维护，并已支持 push attestation / one-shot evidence verification。产品化时应固定已修复版本并做安全审计，因为项目历史上存在认证/nonce 相关安全公告。

## 7. Keylime 原始论文

### Bootstrapping and Maintaining Trust in the Cloud

- ACSAC 2016
- MIT Lincoln Laboratory
- URL：https://www.ll.mit.edu/r-d/publications/bootstrapping-and-maintaining-trust-cloud

证明了 hardware-rooted identity、periodic attestation、trusted key provisioning、大规模 verifier 的可行性。

历史实验报告约 2 s bootstrapping、最快约 110 ms 完整性违规检测、可扩展到数千节点。

注意：云场景历史数字不能直接成为 UAV 指标，只作为架构可行性证据。

## 8. ROS2/DDS 最直接参考：DDS Security+

### DDS Security+: Enhancing the Data Distribution Service with TPM-based Remote Attestation

- ARES 2024
- DOI：10.1145/3664476.3670442
- URL：https://publica.fraunhofer.de/entities/publication/2acdae72-58de-4469-9979-47a0e4ef6da2

实现：
- DDS Security handshake + TPM Remote Attestation；
- 验证 remote participant code integrity；
- 通信通道与 attested software stack 密码绑定；
- Tamarin 形式化验证；
- 基于 eProsima Fast DDS 实现和性能评估。

它直接支撑：

~~~text
ROS2/DDS Participant Identity
+ TPM Attestation
→ Trusted DDS Participant
→ Allow Topic / Service / Mission Interaction
~~~

## 9. fs-verity / dm-verity：模型和系统本地完整性

### fs-verity
https://www.kernel.org/doc/html/latest/filesystems/fsverity.html

特性：
- 单文件 Merkle Tree；
- 文件只读；
- read/mmap 时验证；
- 被篡改数据读取失败；
- 可结合 signature。

适合 model.rknn / .engine / .bin 等大文件。

推荐组合：

~~~text
Signed Model Manifest
+ fs-verity
+ IMA Measurement
+ Remote Attestation
~~~

### dm-verity
https://www.kernel.org/doc/html/latest/admin-guide/device-mapper/verity.html

适合 rootfs / system partition 完整性。

可形成：

~~~text
Secure Boot
→ dm-verity RootFS
→ IMA Runtime Measurement
→ fs-verity Model
→ TPM/TCM Quote
~~~

## 10. Artifact Supply Chain：Sigstore 辅助参考

https://docs.sigstore.dev/

Sigstore 回答：
“artifact 是谁发布的、发布后是否被修改？”

IMA/TPM 回答：
“设备当前实际读取/运行了什么？”

两者组合：

~~~text
Artifact Signature / Provenance
+
Runtime Measurement / Attestation
~~~

涉密/离线环境不必照搬公共 transparency log，可借鉴 artifact signing / provenance 思路。

## 11. 国产现实器件：NS350

国民技术：
https://www.nationstech.com/about/news/product/3387.html

Product Family PDF：
https://www.nationstech.com/uploads/NationsNS350ProductFamilyv2.pdf

公开能力：
- TCM 2.0；
- TPM 2.0 compatible；
- GM/T 0012-2020；
- SM2/SM3/SM4；
- 24 个 SM3 PCR；
- personalized EK certificate；
- active measurement；
- SPI/I2C；
- Arm / embedded；
- Linux / 国产 OS；
- secure firmware update。

2026 年官方进一步把 NS350 定位为 AI 服务器和算力平台的可信根：
https://www.nationstech.com/about/news/product/7111.html

这说明“可信密码模块 + AI 算力平台”已有现实产业路径。

## 12. 第一版 P1 Reference Architecture

~~~text
Domestic AI SoC / RK3588
│
├─ Secure Boot / eFuse
├─ dm-verity RootFS
├─ Linux IMA
│    ├─ ROS2 Application
│    ├─ Planner / Config
│    ├─ AI Runtime
│    ├─ Model Manifest
│    └─ Model File
│
├─ fs-verity Model Protection
│
└─ NS350 / TCM
     ├─ Device EK / Identity
     ├─ SM2/SM3/SM4
     ├─ PCR
     ├─ Quote
     └─ Sealed Mission/Model Key

        │ Evidence
        ▼

Fleet / GCS Verifier
├─ Device Certificate
├─ Reference Values
├─ IMA Runtime Policy
├─ Model Hash / Version
└─ Mission Policy

        │ Attestation Result
        ▼

Allow:
- ROS2/FastDDS Trust
- Mission Access
- Model Key
- Fleet Credential

or Reject / Limited Mode
~~~

## 13. 当前主要 GAP

### G1 NS350 ↔ Linux TPM/TCM Stack
需验证 kernel SPI/I2C driver、tpm2-tss/tpm2-tools、TCM 模式 SM2/SM3 PCR、Quote、EK/AK、sealed object、IMA extend。

### G2 AI SoC Boot Measurement Chain
Secure Boot 不等于 Measured Boot。BootROM/TF-A/U-Boot 的 measurement 是否能 extend 到外部 TCM PCR 需要 BSP/bootloader 实测或改造。

### G3 AI Model Measurement
需确认 RKNN / TensorRT / QNN / accelerator runtime 如何读取 compiled model，以设计 IMA FILE_CHECK policy。

### G4 Artifact → Execution Gap
模型 artifact hash 正确不等于证明 NPU firmware/runtime/compiler 没被替换，也不等于证明 NPU 最终执行内容与 artifact 完全一致。

第一阶段应使用：
AI Model Artifact Integrity / Trusted Loading

不要直接声称：
NPU Trusted Execution / Confidential AI Execution。

### G5 实时性能
需测试 IMA overhead、TCM Quote latency、attestation frequency、ROS/DDS Security overhead、Full C2 P95/P99 Frame Age、power、thermal。

## 14. 报告优先引用

### 正文必引
1. RFC 9334 RATS Architecture
2. GM/T 0012-2020
3. Linux IMA Policy
4. Keylime Runtime IMA / Verifier
5. DDS Security+ ARES 2024
6. NS350 官方资料
7. Linux fs-verity / dm-verity

### 工程实现
8. tpm2-tools Quote / CheckQuote / PolicyPCR
9. Keylime source / runtime policy
10. eProsima Fast DDS + DDS Security+ 原型

### 背景补充
11. Keylime ACSAC 2016
12. Sigstore Artifact Signing
