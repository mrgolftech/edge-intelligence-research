# 六摄像头 UAV：Security Threat Model 与 Trust/Data Flow

- 状态：v0.1
- 日期：2026-09-30
- 基础 Composition：C2 Visual Autonomy
- 目的：把安全可信要求加入六摄像头工程 Case，与原 W1/W2/W3/W4/W6/W9 资源模型并行验证
- 原则：Security 不是 W10；安全机制不得破坏飞行安全闭环

## 1. 当前系统抽象

```text
C0..C5 Cameras
     │ image + timestamp
     ▼
┌─────────────────────────────────────────────┐
│ Secure Edge AI Compute                      │
│                                             │
│ W1 Capture / ISP / VPU                      │
│ W2 VIO / SLAM                               │
│ W3 Detection / Depth / Perception           │
│ W4 Local Map                                │
│ W6 Planner                                  │
│                                             │
│ Trust Plane:                                │
│ RoT / Device ID / Key / Boot / Attestation  │
│ Model Trust / Storage / Audit / Update      │
└───────────────┬─────────────────────────────┘
                │ command/state
                ▼
              FCU / W9
                │
          actuators / vehicle

External:
GCS / Mission System / Fleet / Maintenance / Update Service
```

当前 external FCU 保持独立实时控制基线。

---

## 2. 关键资产

| Asset | 为什么重要 |
|---|---|
| A1 Device Identity / private key | 决定设备是否可被可信识别 |
| A2 Boot keys / root hash | 决定可信启动链 |
| A3 Flight firmware / parameters | 被篡改可直接影响飞行安全 |
| A4 AI OS / kernel / drivers | 高权限执行环境 |
| A5 ROS2 nodes / planner | 可影响感知和决策 |
| A6 AI model / compiled binary | 被替换可改变识别/避障行为 |
| A7 Model config / thresholds | 轻微篡改也可能改变系统行为 |
| A8 Camera / IMU data | 任务信息、隐私、感知输入 |
| A9 Map / mission / target data | 高价值任务数据 |
| A10 Logs / evidence | 调试、审计、取证依据 |
| A11 FCU command channel | 可直接控制无人机 |
| A12 OTA/update package | 可形成持久化攻击入口 |

---

## 3. Trust Boundaries

### TB1 — Sensor → Compute

风险：
- 假 Camera / 恶意 sensor；
- 数据注入；
- timestamp/sync 欺骗；
- 物理总线窥探/篡改。

当前判断：
- MIPI CSI 通常不是安全协议；
- 不能默认 Sensor 已认证。

要求：
- Camera topology/serial inventory；
- sensor config integrity；
- timestamp consistency check；
- 重要型号可研究 sensor identity / secure SerDes；
- 对异常 frame/timestamp 建立健康检测。

### TB2 — Normal World → Trust Plane

风险：
- Linux root 被突破后窃取密钥；
- 普通应用调用敏感 crypto service；
- TEE API 权限过宽。

要求：
- private key non-exportable；
- Trust Plane 最小 API；
- per-service authorization；
- secrets 不落普通文件系统。

### TB3 — CPU/DDR → NPU/GPU/Accelerator

风险：
- 模型权重明文驻留；
- DMA 越界；
- accelerator firmware 被替换；
- Host+Accelerator PCIe 跨域。

要求：
- 明确 IOMMU / memory isolation；
- model package verify before load；
- accelerator firmware provenance；
- 后续验证运行时权重/中间 tensor 暴露面。

当前状态：GAP，不能声称 full confidential AI execution。

### TB4 — Compute → FCU

风险：
- 命令注入；
- 参数修改；
- 非法 shell/file/mission 操作；
- companion computer 被攻陷后控制 FCU。

PX4 官方已明确：未保护的 MAVLink 链路可能允许命令、shell、文件、参数、mission、arming、flight termination 等操作。

要求：
- MAVLink signing 或等价 command authentication；
- 敏感链路另加 authenticated encryption；
- key 不存普通 removable media；
- mission/parameter command 做权限分级；
- 保留 FCU 独立 failsafe 和安全降级逻辑。

### TB5 — Compute → GCS/Fleet

风险：
- 假地面站；
- 数据窃听；
- 设备冒充；
- 合法设备运行恶意软件。

要求：
- 双向身份认证；
- 链路加密；
- Device Identity + Attestation；
- role-based mission access；
- credential revocation。

### TB6 — Maintenance / Update

风险：
- 恶意 firmware/model；
- rollback；
- 开发调试接口遗留；
- service key 泄露。

要求：
- signed image/model manifest；
- anti-rollback；
- recovery image；
- production debug lock；
- update audit。

### TB7 — Physical Capture

风险：
- 拆机读取 eMMC/NVMe；
- JTAG/UART；
- 提取模型/任务数据/密钥；
- 继续用合法证书伪装在线。

要求：
- disk/data encryption；
- hardware-backed key；
- debug lock；
- lost-device revoke；
- 可选 tamper input；
- 高价值 mission key 短生命周期。

---

## 4. 威胁 → 控制矩阵

| Threat | Example | Primary controls |
|---|---|---|
| T01 Device spoofing | 假 Companion/GCS 接入 | Device ID, PKI, mutual auth |
| T02 Firmware tamper | 修改 boot/kernel | Secure Boot, anti-rollback |
| T03 Valid identity + malicious software | 盗取证书后跑恶意镜像 | Measured Boot, Attestation |
| T04 Model replacement | 替换 detector/VIO model | signed model manifest, hash |
| T05 Config tamper | 修改 threshold/planner config | signed config, measurement |
| T06 Data exfiltration | 任务视频/地图被拷走 | encryption at rest/in transit |
| T07 Command injection | MAVLink/ROS control injection | signing, ACL, auth encryption |
| T08 Node lateral movement | 被攻陷 node 读其它凭据 | sandbox/MAC/TEE isolation |
| T09 Update attack | 恶意/旧版本 OTA | signed update, rollback control |
| T10 Physical capture | 丢机提取模型与密钥 | secure storage, disk crypto, revoke |
| T11 Replay | replay command/attestation | timestamp/nonce/freshness |
| T12 Sensor spoof/data poisoning | 假图像/时间戳 | sensor health, sync checks, plausibility |
| T13 DoS / overload | 恶意流量拖垮 W2/W6 | RT isolation, resource quotas |
| T14 Security mechanism harms control | encryption/attestation占用CPU | workload isolation + P99 validation |

---

## 5. Security Requirement Vector

关键原则：

```text
Compute Requirement Vector
+
Security Requirement Vector
→ Candidate Architecture
```

### SR01 Device Root of Trust
端侧计算节点应具有 hardware-backed root/key storage，具体实现可为 secure OTP、SE、TPM/fTPM、TEE secure storage 或组合。

### SR02 Unique Device Identity
每台计算节点应可分配唯一设备身份；私钥不得以明文文件形式导出。

### SR03 Secure Boot
Bootloader/kernel/关键固件需建立签名启动链。

### SR04 Anti-Rollback
量产固件需要版本防回滚策略。

### SR05 Model Package Trust
AI model + preprocessing + postprocessing + config + runtime constraints 形成签名 artifact manifest。

### SR06 Model/Config Measurement
任务关键模型和配置 hash 应进入可信状态记录；P1 目标进入 attestation evidence。

### SR07 Data-at-Rest
任务数据、日志、模型与凭据按敏感级别加密存储。

### SR08 FCU Channel Authentication
Companion ↔ FCU 需认证；若使用 MAVLink，Signing 仅作为完整性/认证层，敏感链路另设计保密保护。

### SR09 ROS2 Access Control
如系统采用 ROS2，应使用 DDS Security/SROS2 或等价机制执行 participant authentication + least privilege。

### SR10 OS Isolation
关键 node 之间需使用 MAC/sandbox/container/namespace 等避免单 node 横向访问。

### SR11 Remote Attestation
P1 产品目标：任务开始/接入 Fleet 前证明 boot/runtime/model 状态。

### SR12 Attestation-gated Credential
P1 研究：attestation 通过后才释放 mission/model/network credential。

### SR13 Secure Update
Firmware/app/model 更新必须签名验证。

### SR14 Recovery
更新失败/完整性失败后需存在安全恢复路径。

### SR15 Production Debug Lock
生产版本关闭或强认证 JTAG/UART/shell/debug service。

### SR16 Lost-device Revocation
设备丢失后可撤销证书/任务凭据。

### SR17 Tamper State
可选产品特色：外壳拆卸/安全状态进入日志或 Trust Plane。

### SR18 Security Audit Log
关键安全事件需可审计并防止简单篡改。

### SR19 Security/RT Partition
认证、加密、日志、attestation、OTA 等不得阻塞 W9/FCU 实时控制。

### SR20 Security Performance Budget
必须测量安全机制开启前后：
- Frame Age P95/P99；
- CPU/DDR；
- network throughput；
- power/temperature；
- boot time；
- update time。

---

## 6. 推荐 Trust Flow

### 6.1 上电

```text
Hardware RoT
→ verify boot stage
→ verify kernel/rootfs
→ start Trust Service
→ verify mission software
→ verify AI model/config
→ release local operational keys
```

### 6.2 任务准入（P1）

```text
GCS/Fleet nonce
→ device collects measurements
→ TPM/TEE/SE signs evidence
→ Verifier compares Reference Values
→ Attestation Result
→ mission authorization
→ optional model/mission key release
```

### 6.3 运行

```text
Camera/VIO/Perception/Planner
        │
        ├─ health/status
        ├─ security event
        └─ model/config identity
                ↓
          audit / fleet state
```

安全状态变化不应直接执行未经 safety analysis 的激进行为；例如飞行中发现 attestation 异常，优先通知 FCU/mission manager 进入定义好的安全降级，而不是任意切断电源。

---

## 7. Security 与 Safety 的边界

这是六摄 Case 必须新增的设计原则：

```text
Security mechanism failure
≠
直接破坏 flight safety
```

例如：
- certificate expiry；
- verifier unavailable；
- encryption service restart；
- OTA failure；
- security log full。

均应有明确 fail-safe/fail-operational 规则。

外部 FCU 在当前 baseline 中继续承担：
- 姿态控制；
- 基础飞控；
- failsafe；
- lost link / return / landing 等核心安全动作。

安全智算盒可以影响高层 mission/autonomy，但不能让普通 Linux/AI 故障直接摧毁 W9 安全闭环。

---

## 8. 平台选型新增检查

六摄候选 Route A~D 除原 Architecture Gate 外，增加 Security Gate：

### Route A RK3588
已找到 Secure Boot / TrustZone / secure OTP 等原语；Attestation、model runtime trust 仍 GAP。

### Route B Jetson Orin
Secure Boot / OP-TEE / fTPM / disk encryption 等原语丰富，是 P1 attestation prototype 的重要参考平台。

### Route C IQ-9075
当前 SKU 级公开 security evidence 仍不足，不能继承 QRB5165。

### Route D RK3588 + Accelerator
需要双重验证：
1. Host Trust；
2. Accelerator firmware/model/PCIe trust。

不能因为 RK3588 Secure Boot 就认为 LQ50/Metis/Hailo 也进入同一 secure boot chain。

---

## 9. Validation Plan 增量

### VS01 Boot Tamper
错误签名/修改 kernel/rollback image。

### VS02 Model Tamper
修改 model/config/manifest。

### VS03 Device Identity
复制文件系统到另一设备，验证私钥/身份不可简单克隆。

### VS04 FCU Injection
无签名/错误签名 command、parameter、mission write。

### VS05 ROS2 ACL
非法 node publish/subscribe/service。

### VS06 Credential Theft
Normal-world root 后尝试读取 device key。

### VS07 Attestation
正常、kernel modified、model modified、replay evidence。

### VS08 Physical Storage
拆下 eMMC/NVMe 后离线读取。

### VS09 Debug
量产状态 JTAG/UART/debug shell。

### VS10 Security + C2 Co-run
打开 encryption / ROS security / audit 后运行：
W1 + W2 + W3 + W4 + W6，记录 P95/P99 Frame Age 与功耗。

### VS11 Lost-device
证书吊销后验证设备无法重新获取敏感 mission credential。

### VS12 Update/Recovery
断电、错误签名、旧版本、损坏 image 与恢复。

---

## 10. 当前项目结论

1. 六摄 Camera 本身只是 W1 数据入口；真正高价值安全对象是 compute identity、model、mission data 和 FCU control path。
2. 当前优先应建立 P0：Secure Boot + Device Identity + Model Signature + Data Encryption + FCU Auth + ROS ACL + Debug Lock + Signed Update。
3. P1 差异化重点是 Measured Boot / Remote Attestation / Attestation-gated key。
4. “安全芯片”应成为 Trust Plane 的根，不应只是一个 SM2/SM4 API 外设。
5. Security benchmark 必须和 C2 并发 workload 一起测，否则可能牺牲 Frame Age / deadline。
