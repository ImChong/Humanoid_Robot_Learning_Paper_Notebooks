---
layout: paper
paper_order: 8
title: "PhysMoDPO: Physically-Plausible Humanoid Motion with Preference Optimization"
zhname: "PhysMoDPO：用偏好优化把文本生成的动作「磨」成物理可执行的人形动作"
category: "物理动画"
---

# PhysMoDPO: Physically-Plausible Humanoid Motion with Preference Optimization
**让扩散模型生成的动作不只是「看起来对」，而是放进物理控制器后还能稳稳跑出来**

> 📅 阅读日期: 2026-06-17
>
> 🏷️ 板块: 13 Physics-Based Animation · 物理可行动作生成 / 扩散模型 / 偏好优化(DPO) / 全身控制器
>
> 🔁 推进轨: 模块轮转（12_Hardware_Design → **13_Physics-Based_Animation**）

---

## 📋 基本信息

| 项目 | 链接 |
|---|---|
| arXiv | [2603.13228](https://arxiv.org/abs/2603.13228) |
| HTML | [在线阅读](https://arxiv.org/html/2603.13228) |
| PDF | [下载](https://arxiv.org/pdf/2603.13228) |
| 项目主页 | [mael-zys.github.io/PhysMoDPO](https://mael-zys.github.io/PhysMoDPO/) |
| 源码 | [Mael-zys/PhysMoDPO](https://github.com/Mael-zys/PhysMoDPO) |
| **发布时间** | 2026-03-13（arXiv，2026-03-16 修订） |
| 机构 | MBZUAI · LIGM/École des Ponts/IP Paris/CNRS · EPFL |

**作者**：Yangsong Zhang, Anujith Muraleedharan, Rikhat Akizhanov, Abdul Ahad Butt, Gül Varol, Pascal Fua, Fabio Pizzati, Ivan Laptev。

**定位**：一种**面向部署的文本→动作生成后训练框架**——不在「运动学空间」里评好坏，而是把扩散模型生成的动作先送进**全身控制器（WBC）**跑一遍，看它在物理里到底能不能执行，再用**直接偏好优化（DPO）**把生成器往「物理可执行」的方向微调。

---

## 🎯 一句话总结

文本驱动的扩散模型能生成「姿态空间里看着合理」的人体动作，但一旦交给真实/仿真机器人执行，物理控制器为了满足动力学和接触约束会做大量修正，导致**执行出来的动作和生成的动作严重跑偏**。PhysMoDPO 的思路是：**先用一个固定的 WBC 把候选动作「物理化」，在跟踪后的真实动作上算奖励（跟踪保真、不滑步、文本对齐、空间控制），再用 DPO 把生成器微调到「生成即可执行」**——无需重训控制器，且能零样本迁移到 Unitree G1 / H1 真机。

---

## 📌 英文缩写速查

| 缩写 / 术语 | 全称 / 含义 | 解释 |
|---|---|---|
| WBC | Whole-Body Controller | 全身控制器，这里用固定的 DeepMimic 跟踪器把运动学动作转成物理可行轨迹 |
| DPO | Direct Preference Optimization | 直接偏好优化，用「胜/负」样本对微调生成模型，无需显式奖励模型 |
| SFT | Supervised Fine-Tuning | 监督微调，作为 DPO 的正则项防止偏离原分布 |
| Tracking Distortion (Δ) | 跟踪畸变 | 衡量「生成动作」与「WBC 跟踪后真实动作」之间偏差的指标 |
| M2T / TMR | Motion-to-Text / Text-Motion Retrieval | 用检索编码器度量动作与文本语义是否一致 |
| SMPL | Skinned Multi-Person Linear model | 参数化人体模型，动作用 SMPL 表示避免昂贵的逆运动学 |

---

## ❓ 这篇论文要解决什么问题？

文本→动作的扩散模型（如 MotionStreamer、OmniControl）在**运动学空间**里能生成看似合理的动作，但放到物理系统上往往「翻车」：

- 控制器为了满足**动力学和接触可行性**，会对生成动作做大量修正；
- 修正越大，**执行出来的动作离原生成动作越远**——也就是论文强调的「跟踪畸变 Δ」很大；
- 关键洞见：**在运动学空间里评出来的「好样本」，落到物理执行上可能很差**。质量必须在「跟踪之后」评，才和真正的部署效果对齐。

所以问题是：**怎么把一个已经训好的运动学生成器，后训练成「生成的动作本身就物理可执行」？**

---

## 🧱 方法的关键设计

### 1. 三件套流水线：扩散生成 → WBC 物理化 → DPO 微调

- **扩散生成器**：基于预训练模型（MotionStreamer / OmniControl），从文本或空间约束生成候选动作；
- **物理算子（固定 WBC）**：一个固定的 DeepMimic 跟踪器，把运动学动作转成满足动力学/接触的可执行轨迹——**不训练它，只用它当「物理裁判」**；
- **DPO 偏好优化**：在跟踪后的真实动作上构造偏好对，微调生成器，并用 SFT 正则防止漂移。

### 2. 在「跟踪后」算奖励，而不是在生成空间算

奖励是多目标的，且**全部在 WBC 跟踪后的动作上计算**：

- **跟踪奖励**：原动作 vs 跟踪后动作的差异要小（Δ 小）；
- **滑步奖励**：接触发生时惩罚脚部漂移；
- **文本-动作对齐（M2T）**：用 TMR 编码器保住语义一致；
- **空间控制奖励**：满足给定的空间约束。

### 3. 支配式（dominance-based）偏好选择

不靠手调各奖励的权重，而是用**支配规则**：一个样本只有在**所有奖励维度都不劣、且至少有提升**时才算「胜」。这样避免了多目标加权融合里恼人的调参问题。

### 4. 迭代式后训练

多轮精炼：每轮用上一轮改进后的模型重新采样、重建偏好对，让监督信号逐步贴近真实的「部署失败模式」（论文中 3 轮最优）。

---

## 🔄 方法 / 系统结构流程图

<div class="mermaid">
flowchart TD
    T["文本 / 空间约束"] --> G["扩散生成器<br/>(MotionStreamer / OmniControl)"]
    G --> K["K 个候选动作<br/>(运动学空间, SMPL)"]
    K --> W["固定 WBC (DeepMimic 跟踪器)<br/>施加动力学 + 接触约束"]
    W --> R["在跟踪后动作上算多目标奖励<br/>跟踪Δ / 不滑步 / 文本对齐 / 空间控制"]
    R --> P["支配式规则构造偏好对<br/>(全维度不劣才算胜)"]
    P --> D["DPO 微调生成器<br/>+ SFT 正则"]
    D -. 迭代 3 轮: 用新模型重采样 .-> G
    D --> O["生成即可执行的动作<br/>零样本部署 G1 / H1 真机"]
</div>

---

## 📊 实验与结果

- **仿真（SMPL 角色）**：
  - 文本→动作：R@3 从 0.831 → 0.852，Jerk（抖动）46.75 → 43.60；
  - 空间控制：可控性误差 0.094 → 0.092，FID / Jerk 同步改善；
  - 优于 MaskedMimic（物理可行但文本保真差）和普通监督微调基线。
- **零样本迁移真机**：Unitree G1 在文本一致性、可控性、平滑度上一致提升，无需额外训练；H1 跨本体迁移仍保持较强空间可控性；真机 G1 成功执行生成动作。
- **泛化**：在分布外的人-物交互数据集 OMOMO 上验证泛化能力。
- **用户研究**：20 名受试者对 40 组视频对在「文本贴合 / 平滑 / 稳定」三项上打分，PhysMoDPO 全面优于 OmniControl 与 MaskedMimic。
- **消融**：迭代 3 轮最优；各奖励分量都不可或缺；支配式选择优于加权融合；λ_SFT=2、β=20 较优。

---

## 💡 启发与点评

- **「质量要在执行后评」是核心洞见**：运动学空间里的好坏与物理部署效果不对齐，先跑物理再评分，让优化目标直接对准「能不能跑出来」，这点对所有「生成→部署」的机器人任务都有借鉴价值。
- **把固定 WBC 当「物理裁判」**：不重训控制器，只用它生成偏好信号，工程上轻量、可叠加到现有生成器上，是一种实用的后训练范式。
- **支配式偏好绕开多目标调参**：多奖励加权常常难调，用「全维度不劣才算胜」的支配规则构造偏好对，省心且稳健。
- **DPO 进入物理动作生成**：把 LLM 对齐里成熟的 DPO 搬到「物理可行性对齐」上，是一个有意思的跨界迁移。
- **局限**：依赖一个能用的固定 WBC（DeepMimic 跟踪器）作为物理算子，其能力上限会限制可达动作范围；偏好信号质量也受奖励设计影响；真机以零样本演示为主，长时程/高动态任务的稳健性仍待进一步验证。

---

## 🎤 面试参考

**Q：为什么文本生成的动作直接给机器人执行会「跑偏」？**
A：扩散模型只保证运动学（姿态）上看着合理，但不保证动力学/接触可行；物理控制器执行时会为满足约束做大量修正，导致执行出来的动作和生成的动作偏差很大（即跟踪畸变 Δ 很大）。

**Q：PhysMoDPO 怎么解决？核心思路是什么？**
A：先用一个固定的 WBC 把候选动作「物理化」跑一遍，在跟踪后的真实动作上算多目标奖励（跟踪保真、不滑步、文本对齐、空间控制），再用 DPO 把生成器微调到「生成即可执行」的方向，并迭代多轮。

**Q：为什么用支配式偏好而不是加权奖励？**
A：多目标加权需要手调权重、容易顾此失彼；支配规则只在「所有维度都不劣且有提升」时判一个样本胜出，避免调参、构造的偏好对更可靠。

**Q：相比 MaskedMimic 这类物理方法的优势？**
A：MaskedMimic 物理可行但文本保真差；PhysMoDPO 在保物理可行的同时显著改善文本一致性与可控性，且能零样本迁移到 G1/H1 真机。

---

## 🔗 相关阅读 / 类似方向

- [MaskedMimic: Unified Physics-Based Character Control Through Masked Motion Inpainting (SIGGRAPH Asia 2024)](https://research.nvidia.com/labs/par/maskedmimic/)：物理可行但文本保真弱，本文重要对照
- [OmniControl: Control Any Joint at Any Time for Human Motion Generation (ICLR 2024)](https://arxiv.org/abs/2310.08580)：空间可控的运动生成基座之一
- [PhysHMR: Learning Humanoid Control Policies from Vision for Physically Plausible Human Motion Reconstruction](https://arxiv.org/abs/2602.21599)：本模块，物理可行的人体动作重建
- [DeepMimic: Example-Guided Deep RL of Physics-Based Character Skills (SIGGRAPH 2018)](https://arxiv.org/abs/1804.02717)：本文物理算子(WBC)所依赖的跟踪器范式来源

---

> 备注：本笔记基于 arXiv 元信息（2603.13228）、项目主页与论文 HTML 公开内容整理；部分数值（指标、超参）以论文公开陈述为准，若后续正式版/源码释出更详尽内容可补全对应字段。
