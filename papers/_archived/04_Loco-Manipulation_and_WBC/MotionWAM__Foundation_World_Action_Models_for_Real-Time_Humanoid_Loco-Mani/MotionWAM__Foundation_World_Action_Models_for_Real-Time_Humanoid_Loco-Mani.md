---
layout: paper
paper_order: 1
title: "MotionWAM: Towards Foundation World Action Models for Real-Time Humanoid Loco-Manipulation"
zhname: "MotionWAM：面向实时人形移动操作的基础世界动作模型"
category: "Loco-Manipulation and WBC"
---

# MotionWAM: Towards Foundation World Action Models for Real-Time Humanoid Loco-Manipulation
**把视频世界模型的"中间去噪特征"直接喂给动作策略——一次前向、无需迭代去噪，从单目第一视角相机实时驱动人形全身移动操作**

> 📅 阅读日期: 2026-06-17
>
> 🏷️ 板块: 04 Loco-Manipulation / WBC · 世界动作模型(WAM) · 视频扩散世界模型 · 统一全身动作 token · 实时推理
>
> 🔁 推进轨: 模块轮转（14_Human_Motion → **04_Loco-Manipulation_and_WBC**）

---

## 📋 基本信息

| 项目 | 链接 |
|---|---|
| arXiv | [2606.09215](https://arxiv.org/abs/2606.09215) |
| HTML | [arXiv HTML](https://arxiv.org/html/2606.09215v1) |
| PDF | [arXiv PDF](https://arxiv.org/pdf/2606.09215) |
| **发布时间** | 2026-06-08 (arXiv) |
| 源码 | 截至当前未见公开代码/项目主页（待官方释出） |
| 作者 | Jia Zheng, Teli Ma, Yudong Fan, Zifan Wang, Shuo Yang, Junwei Liang |
| 机构 | Mondo Robotics · 香港科技大学(广州) HKUST(GZ) · 香港科技大学 HKUST |
| 评测平台 | Unitree G1（双 ALOHA2 夹爪 + 头戴 RealSense D435i） |

---

## 🎯 一句话总结

> MotionWAM 想解决"世界动作模型(WAM)虽然能给策略注入强动力学先验，但要对高维视频-动作 latent 反复迭代去噪、太慢、跑不动实时人形控制"的问题：核心做法是**不再把视频完全去噪成清晰画面，而是在去噪早期（接近纯噪声）用 forward hook 截取 Video DiT 的中间隐藏特征**，让策略以"一次前向、一次想象"的方式拿到"未来会怎样"的先验，从而**实时（A100 上 4.9Hz）**地从单目第一视角相机驱动**统一的全身动作**（行走、躯干、身高调节、脚部交互、双手操作一起出），把桌面操作扩展到协调、像人一样的人形全身移动操作。

---

## 📌 英文缩写速查

| 缩写 | 全称 | 简单解释 |
|---|---|---|
| WAM | World Action Model | 世界动作模型：把"预测未来视觉动态"和"生成动作"耦合在一起的策略 |
| VLA | Vision-Language-Action | 视觉-语言-动作模型，直接从观测映射到动作 |
| DiT | Diffusion Transformer | 扩散 Transformer，本文 Video DiT + Motion DiT 双分支 |
| Flow Matching | — | 流匹配，预测从噪声态到干净态的速度场 |
| FSQ | Finite Scalar Quantization | 有限标量量化，把全身意图压成离散 token |
| Loco-Manipulation | — | 移动操作：行走与操作协同 |

---

## ❓ 论文要解决什么问题？

人形机器人要做"既走又操作"的日常任务（开抽屉拿东西、踢球、装购物车、倒垃圾、擦白板……），难点是这些动作**腿和躯干必须主动参与**，不只是站着保持平衡。两类已有思路各有短板：

1. **VLA（直接观测→动作）**：缺少对"接下来世界会怎么变"的动力学先验，时序连贯性和物理合理性弱；
2. **WAM（世界动作模型）**：把视觉动态预测和动作生成耦合，能注入强动力学先验，但要对高维"视频-动作 latent"**反复迭代去噪**，计算开销大，慢到无法实时人形控制（同类 Cosmos Policy 仅约 0.7Hz）。

此外，传统人形控制常把上半身（关节目标）和下半身（底盘速度/身高/朝向指令）**拆开**，导致"踩踏板、踢球"这类需要腿主动参与任务目标的脚部行为做不出来。

---

## 🔧 方法详解

### 1) 核心思路：条件于"中间去噪特征"而非原始 latent

- 传统 WAM 要把视频-动作 latent 完整迭代去噪 → 慢；
- MotionWAM 在 Video DiT 上装一个 **forward hook**，在**固定的早期去噪步（接近纯噪声，flow step ≈ 1.0）截取中间激活**；
- 这种"**一次想象（one-shot imagination）**"：模型一次前向就生成"编码了合理第一视角未来"的特征，**不必把画面真的去噪干净**，消除迭代开销，实现实时。

### 2) 双 DiT 架构

- **Video DiT**：从 Cosmos-Predict2.5-2B 初始化（因果时空 VAE + 流匹配扩散 Transformer），把第一视角画面压成 latent，在固定 flow step 输出中间隐藏态；
- **Motion DiT**（DiT-B）：吃 Video DiT 的隐藏态 + 本体感知状态 + 带噪动作-latent token，用交错的 self/cross-attention，输出速度场，积分得到动作 latent；多具身训练时用**逐具身的输入/输出投影器**包住共享主干。
- 两个分支都用**流匹配**目标训练（从带噪中间态预测到干净目标的速度场）。

### 3) 统一全身动作 token（不再拆上下半身）

- 动作 latent 分解为 *m_t* = (*m_t^cont*, *k_t*)：连续通道管灵巧末端执行器；一个 **64 维离散 token（FSQ 量化）**总结"全身意图"；
- 一套 token 同时覆盖**行走 / 躯干运动 / 身高调节 / 脚部交互 / 双手操作**；
- 正因统一，才能做出上下半身解耦策略做不到的**任务驱动脚部行为**（踩踏板、踢球）。

### 4) 三阶段学习

- **阶段一·第一视角视频预训练**：仅训 Video DiT，用约 **2136 小时**第一视角人类+人形视频（无动作标签），把世界模型从通用迁到第一视角动态；
- **阶段二·跨具身动作后训练**：接上 Motion DiT，两分支在异构 Unitree G1 数据上联合训练，用逐具身投影器对齐不同末端/动作格式；
- **阶段三·全身微调**：在目标具身的遥操作演示上端到端微调（每任务 200 条），保留联合损失以守住先验。

### 🧭 整体流程

<div class="mermaid">
flowchart TB
    subgraph PRE["阶段一 · 第一视角视频预训练"]
        VID["~2136h 第一视角<br/>人类+人形视频(无动作标签)"]
        VDIT["Video DiT<br/>(从 Cosmos-Predict2.5-2B 初始化)"]
        VID --> VDIT
    end

    subgraph RUNTIME["运行时 · 一次想象(实时)"]
        CAM["单目第一视角相机<br/>RealSense D435i"]
        HOOK["forward hook<br/>截取早期去噪中间特征<br/>(flow step ≈ 1.0, 不完整去噪)"]
        MDIT["Motion DiT (DiT-B)<br/>+ 本体感知状态"]
        TOK["统一全身动作 token<br/>m=(连续末端, 64维FSQ全身意图)"]
        WB["全身动作: 行走/躯干/身高<br/>/脚部交互/双手操作"]
        CAM --> VDIT
        VDIT --> HOOK --> MDIT --> TOK --> WB
    end

    subgraph TRAIN["阶段二/三 · 动作训练"]
        XEMB["跨具身后训练<br/>(逐具身投影器)"]
        FT["全身微调<br/>每任务200条遥操作演示"]
        XEMB --> FT
    end

    VDIT --> XEMB
    FT --> MDIT

    WB --> ROBOT["Unitree G1 真机<br/>9 个全身移动操作任务"]

    style PRE fill:#fdebd0,stroke:#e67e22
    style RUNTIME fill:#e8f4fd,stroke:#1f78b4
    style TRAIN fill:#e8f8e8,stroke:#27ae60
    style ROBOT fill:#fceae8,stroke:#c0392b
</div>

---

## 💡 核心贡献

| 创新 | 描述 |
|---|---|
| **中间去噪特征条件化** | 不完整去噪、一次前向就拿"未来想象"特征喂策略，把 WAM 从 0.7Hz 拉到 4.9Hz(A100)，让世界动作模型首次实时驱动人形 |
| **统一全身动作 token** | 连续末端 + 64 维 FSQ 全身意图，一套 token 同管行走/躯干/身高/脚部/双手，做出上下半身解耦做不到的任务驱动脚部行为 |
| **三阶段课程** | 第一视角视频预训练 → 跨具身动作后训练 → 全身微调，把视频世界模型逐步适配到第一视角与目标具身 |
| **真机验证** | Unitree G1 上 9 个需要腿/躯干主动参与的全身移动操作任务，平均成功率显著超越 VLA 基线 |

---

## 📊 实验亮点

- **平台**：Unitree G1 + 双 ALOHA2 夹爪 + 头戴 Intel RealSense D435i RGB 相机；
- **任务（9 个真实世界）**：拿瓶子摆放、踢足球、从抽屉取物、装购物车、倒垃圾、抬篮子、上货架、擦白板、洗衣——每个都需要腿/躯干主动参与，超出"仅维持平衡"；
- **基线**：Diffusion Policy、ACT、π₀.₅、GR00T-N1.7、Qwen3DiT（VLM 消融）；
- **结果**：平均成功率 **76.1%**，最强基线 GR00T-N1.7 为 43.9%，**绝对提升 >32%**；在需要全身协调的任务上提升最大（+40~45%）；
- **实时性**：A100 上 **4.9Hz** 推理，对照同类 Cosmos Policy 仅 0.7Hz。

---

## ⚠️ 局限

- 阶段三仅在 Unitree G1 上验证，向其他人形平台的迁移性未验证；
- 未做受控的"新物体泛化"研究，训练/测试物体视觉相似；
- 主要失败模式来自**单目第一视角相机**：被操作物体离开视野、或头部相机视角漂移出训练分布时，会丢失视觉锚定而卡住。

---

## 🤖 对人形机器人领域的意义

| 影响方向 | 说明 |
|---|---|
| **世界模型提速** | "条件于中间去噪特征而非完整去噪结果"为把重型视频扩散世界模型用于实时机器人控制提供了一条通用提速思路 |
| **全身一体化表征** | 用统一 token 替代上下半身解耦，给"任务目标如何驱动腿/脚行为"提供了可借鉴的动作表征 |
| **视频先验复用** | 大规模第一视角视频预训练 → 跨具身/全身微调，展示了如何把通用视频生成先验迁到具体人形具身 |

---

## 🎤 面试参考

**Q：MotionWAM 为什么能比传统 WAM 快这么多？**
A：传统 WAM 要把高维视频-动作 latent 反复迭代去噪成清晰未来帧，再反推动作，迭代步数多、计算重。MotionWAM 用 forward hook 在去噪早期（接近纯噪声）就截取 Video DiT 的中间隐藏特征，这些特征已经编码了"合理的第一视角未来"，足够作为策略的动力学先验——一次前向就够，不必把画面真的去噪干净，所以从约 0.7Hz 提到 4.9Hz，能实时控制。

**Q：为什么要用统一全身动作 token，而不是沿用上下半身解耦？**
A：解耦下，下半身只接收速度/身高/朝向这类与任务目标无关的底盘指令，腿无法"为了完成任务"主动动作，像踩踏板、踢球这种需要脚参与任务的行为就做不出来。统一 token（连续末端 + 64 维 FSQ 全身意图）让一套表征同时安排行走、躯干、身高、脚部交互和双手操作，腿脚能被任务目标直接驱动。

**Q：它最大的失败来源是什么？**
A：单目第一视角相机。当被操作物体移出视野，或头部相机视角漂移到训练分布之外时，模型失去视觉锚定就会卡住。这也指向下一步：多视角/外部相机或更鲁棒的视觉锚定。

---

## 💬 讨论记录

> 此部分在阅读讨论后更新
