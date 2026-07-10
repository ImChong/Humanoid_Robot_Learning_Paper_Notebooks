---
layout: paper
paper_order: 1
title: "Athena-WBC: Capability-Aligned Policy Experts for Long-Tail Humanoid Whole-Body Control"
zhname: "Athena-WBC：用「能力对齐」的动态/平衡专家攻克人形全身控制的长尾动作"
category: "Loco-Manipulation and WBC"
---

# Athena-WBC: Capability-Aligned Policy Experts for Long-Tail Humanoid Whole-Body Control
**Athena-WBC：先诊断出「训练集内长尾」动作失败源自能力瓶颈（而非样本不足），再用「动态专家 + 平衡专家」两类能力对齐的专家分而治之，最后蒸馏 + PPO 精修成单一可部署控制器**

> 📅 阅读日期: 2026-07-10
>
> 🏷️ 板块: 04 Loco-Manipulation / WBC · 全身运动跟踪 · 长尾动作 · 教师-学生 · 专家蒸馏 · 平衡课程
>
> 🔁 推进轨: 模块轮转（14_Human_Motion → **04_Loco-Manipulation_and_WBC**）

---

## 📋 基本信息

| 项目 | 链接 |
|---|---|
| 时间 | 2026 年 7 月 |
| arXiv | [2607.04837](https://arxiv.org/abs/2607.04837) · [PDF](https://arxiv.org/pdf/2607.04837) · [HTML](https://arxiv.org/html/2607.04837v2) |
| 发布时间 | 2026-07-06 (v1) / 2026-07-07 (v2) |
| 代码 | 论文未公开代码 / 项目页（截至 2026-07-10） |
| 作者 | Yuan Jiang、Ningyuan Zhang、Xicun Yang、Yuzhi Jiang、Jie Chen |
| 实验平台 | 全尺寸 **XPENG（小鹏）人形机器人**，80 kg，行星滚柱丝杠驱动 + 闭链机构 |
| 主题 | cs.RO · 人形全身控制 / 运动跟踪 / 专家蒸馏 |

---

## 🎯 一句话总结

> 人形全身运动跟踪里有一类容易被忽视的失败：**动作明明就在训练集中、物理上也可行，却始终跟不好**——集中在**高动态过渡**（急转向、剧烈接触切换）与**平衡临界**（低支撑姿态、缓慢恢复）两类动作上。Athena-WBC 指出这不是「样本不够」，而是**能力瓶颈**：保守的奖励正则压制了「激进但可行」的动作，名义重力下训练又让平衡临界片段在早期拿不到有效学习信号。对策是训练两类**能力对齐的专家**——**动态专家**（去掉力矩/时序控制惩罚、改用 Grad-CAPS 平滑约束换取「大而有序」的动作）与**平衡专家**（重力续延课程，从 α·g₀ 逐步升到名义重力提升早期存活率）——再把「通用教师 + 两类专家」按动作路由后**蒸馏进单一学生**并用 PPO 精修，得到一个可直接部署、又能补齐长尾的控制器。

---

## 📌 英文缩写速查

| 缩写 | 含义 |
|---|---|
| WBC | Whole-Body Control，全身控制 |
| DAgger | Dataset Aggregation，交互式模仿学习/蒸馏算法 |
| Grad-CAPS | 对 actor 均值做「二阶差分平滑」的辅助损失（CAPS 平滑正则的梯度版），抑制高频抖动 |
| MPJPE | Mean Per-Joint Position Error，逐关节平均位置误差（跟踪精度指标） |
| MPJPE-W | 世界系下的逐关节位置误差 |
| IID / OOD | 独立同分布 / 分布外（评测集划分） |
| 长尾（Long-Tail） | 分布尾部的少数难样本，此处特指「训练集内仍学不会」的动作 |

---

## ❓ 论文要解决什么问题？

大规模人形运动跟踪常报告很高的整体成功率，但作者聚焦一个更棘手的现象——**训练集内的长尾失败（training-set long-tail）**：某些片段**已经出现在训练数据里、物理上也可行**，模型却依旧跟不好。它们高度集中在两类：

- **高动态过渡**：急转向、快速方向变化、剧烈接触切换；
- **平衡临界**：低支撑面姿态、缓慢恢复等对稳定性要求苛刻的动作。

作者把根因归结为 **「能力瓶颈（capability bottleneck）」**，而不是曝光不足：

1. **保守的奖励正则**（力矩惩罚、时序控制平滑等）会**压制激进但物理可行**的动作，使高动态片段无法被真正学会；
2. **名义重力下训练**，平衡临界片段在早期 rollout 里几乎立刻摔倒，**拿不到有用的学习信号**。

因此，单纯加数据或延长训练无济于事，需要**针对性地重塑「能力」**。

---

## 🔧 方法详解

### 1. 挖掘长尾：先训通用教师，再筛残差失败集
先在完整动作集 𝒟train 上训练一个**通用教师**；随后**挖掘残差失败**（成功率 < 0.8 的片段）组成难例集 ℛgen，作为两类专家的专项训练对象。

### 2. 动态专家（Dynamic Experts）
- **去掉力矩/时序控制惩罚**，仅保留跟踪奖励与物理硬约束，把「激进但可行」的动作解放出来；
- 用 **Grad-CAPS 辅助损失**（对 actor 均值施加二阶差分平滑）在**奖励层之外**约束平滑性——从而允许**幅度大但结构化**的动作变化，同时不牺牲部署所需的平稳度（消融中把高频抖动从 0.063 压到 0.007）。

### 3. 平衡专家（Balance Experts）
- 采用 **重力续延课程（gravity continuation curriculum）**：训练时重力从 αmin·g₀ 逐步升高到名义 g₀，先提升早期 rollout 的**存活率**再恢复完整动力学，让平衡临界片段能拿到有效梯度。

### 4. 路由 + 蒸馏 + 精修：压成单一可部署控制器
1. 冻结「通用教师 + 动态专家 + 平衡专家」三方；
2. 基于 rollout 表现，为每个动作**路由到表现最好的教师**；
3. 用 **DAgger** 以「可部署观测」把被路由的教师**蒸馏进单一学生**；
4. 学生再经 **critic 预热 + PPO 精修**收尾。

### 5. 数据与结果
- **训练语料（合计 55,482 段 / 175.88 h）**：AMASS 7,333 段/25.11 h、Bones-Seed 46,341 段/95.66 h、BEAT 1,574 段/43.47 h、精选动捕 234 段/11.64 h；
- **评测**：AMASS-eval（10 h，IID）与 Omni-eval（227 段，含操作相关行为的困难 OOD）；
- **held-out 提升**：AMASS-eval 成功率 98.18% → **99.26%**，Omni-eval 91.81% → **94.89%**；MPJPE 68.26±18.42 mm → **63.63±18.91 mm**；动作率保持在可部署的 1.03（对照 0.54）；
- **长尾恢复**：平衡专项 MPJPE-W 101.99±73.06 mm → **90.22±55.64 mm**，多教师学生在平衡子集达 **94.73%** 成功率；
- **平台**：全尺寸 XPENG 人形（80 kg，行星滚柱丝杠 + 闭链），与 SONIC 所用 Unitree G1 形成对照。

---

### 🧭 整体流程（mermaid）

<div class="mermaid">
flowchart TD
    D["📚 完整动作集 𝒟train<br/>(AMASS+Bones-Seed+BEAT+精选, 5.5万段/176h)"] --> T0["🧑‍🏫 通用教师<br/>general teacher"]
    T0 --> MINE["🔎 挖掘残差失败<br/>成功率<0.8 → 难例集 ℛgen"]

    MINE --> DYN["⚡ 动态专家<br/>去力矩/时序惩罚<br/>+ Grad-CAPS 平滑<br/>(大而有序的动作)"]
    MINE --> BAL["⚖️ 平衡专家<br/>重力续延课程<br/>α·g₀ → g₀<br/>(提升早期存活)"]

    T0 --> ROUTE["🧭 按动作路由<br/>选表现最好的教师"]
    DYN --> ROUTE
    BAL --> ROUTE

    ROUTE --> DISTILL["🎓 DAgger 蒸馏<br/>可部署观测 → 单一学生"]
    DISTILL --> PPO["🔧 critic 预热 + PPO 精修"]
    PPO --> OUT["🤖 单一可部署控制器<br/>AMASS 99.26% · Omni 94.89%<br/>平衡子集 94.73% · 全尺寸 XPENG 80kg"]

    style D fill:#e8f4fd,stroke:#1f78b4,color:#0b3954
    style T0 fill:#fff4e6,stroke:#e67e22,color:#7d3c08
    style DYN fill:#f7e8fd,stroke:#9b59b6,color:#4a1c5d
    style BAL fill:#eef7ee,stroke:#27ae60,color:#0f3d1e
    style DISTILL fill:#fde8e8,stroke:#c0392b,color:#641e16
    style OUT fill:#fde8e8,stroke:#c0392b,color:#641e16
</div>

---

## 💡 核心贡献

1. **问题诊断**：把「训练集内长尾失败」明确归因为**能力瓶颈**——保守奖励正则压制激进可行动作、名义重力下平衡片段拿不到早期信号，而非样本曝光不足；
2. **能力对齐的两类专家**：**动态专家**（去惩罚 + Grad-CAPS 换「大而有序」的动作）与**平衡专家**（重力续延课程提升早期存活），分别对症两类长尾；
3. **路由—蒸馏—精修配方**：多教师按动作路由 + DAgger 蒸馏进单一学生 + critic 预热 PPO 精修，**兼顾长尾补齐与单一可部署性**；
4. **全尺寸实测**：在 80 kg XPENG 人形上把 AMASS/Omni 成功率与平衡子集精度同时抬升，抖动可控（0.007）、动作率可部署。

---

## 🤖 对人形机器人学习的启发

- **「先诊断能力、再对症训练」是一条有价值的方法论**：当整体成功率已很高时，值得把注意力从「加数据」转向「找出被奖励正则/训练设定压制的可行动作」；
- **奖励层平滑 ≠ 网络层平滑**：把平滑性从奖励里拿出来、改用 Grad-CAPS 这类结构化辅助损失，能在**不牺牲部署平稳度**的前提下释放高动态能力，是可迁移的技巧；
- **重力课程是攻克平衡临界的低成本手段**：先降重力保早期存活、再续延回名义值，为「一开始就摔」的片段提供有效梯度，可推广到其他稳定性受限任务；
- **多专家 → 单一学生** 的蒸馏范式，与 SONIC / Embodiment-Aware 通专蒸馏一脉相承，兼顾专长覆盖与推理期简洁，工程落地友好。

---

## 📁 资源对照

| 资源 | 内容 |
|---|---|
| [arXiv 2607.04837](https://arxiv.org/abs/2607.04837) | 论文正文（含方法、消融与数值结果） |
| [PDF](https://arxiv.org/pdf/2607.04837) · [HTML](https://arxiv.org/html/2607.04837v2) | 在线阅读 |
| 代码 / 项目页 | 论文未公开（截至 2026-07-10） |

> ℹ️ 备注：本环境网络出口对 arXiv 有限制，本笔记依据可获取的 Abstract 与 HTML 正文整理，方法机制与实验数值均取自官方描述；若后续释出代码/项目页可再补链接。

---

## 🔗 相关阅读

- **多教师/通专蒸馏 · 同模块**：[Embodiment-Aware Generalist Specialist Distillation](../Embodiment-Aware_Generalist_Specialist_Distillation_for_Unified_Humanoid_Whole-B/Embodiment-Aware_Generalist_Specialist_Distillation_for_Unified_Humanoid_Whole-B.md) · [General Humanoid WBC via Pretraining and Fast Adaptation](../General_Humanoid_Whole-Body_Control_via_Pretraining_and_Fast_Adaptation/General_Humanoid_Whole-Body_Control_via_Pretraining_and_Fast_Adaptation.md)；
- **大规模运动跟踪**：[SONIC: Supersizing Motion Tracking](../../03_High_Impact_Selection/SONIC_Supersizing_Motion_Tracking_for_Natural_Humanoid_Control/SONIC_Supersizing_Motion_Tracking_for_Natural_Humanoid_Control.md) · [EGM：高效通用运动跟踪](../EGM__Efficiently_Learning_General_Motion_Tracking_for_High_Dynamic_Humanoid_WBC/EGM__Efficiently_Learning_General_Motion_Tracking_for_High_Dynamic_Humanoid_WBC.md)；
- **鲁棒/泛化跟踪**：[Robust and Generalized Humanoid Motion Tracking](../Robust_and_Generalized_Humanoid_Motion_Tracking/Robust_and_Generalized_Humanoid_Motion_Tracking.md)。
