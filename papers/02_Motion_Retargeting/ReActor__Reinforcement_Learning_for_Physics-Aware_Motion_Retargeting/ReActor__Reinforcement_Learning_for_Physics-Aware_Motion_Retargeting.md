---
layout: paper
title: "ReActor: Reinforcement Learning for Physics-Aware Motion Retargeting"
zhname: "ReActor：面向物理可行动作重定向的强化学习"
category: "Motion Retargeting"
paper_order: 3
---

# ReActor: Reinforcement Learning for Physics-Aware Motion Retargeting
**双层优化：上层调「跨本体映射参数」，下层用 RL 在物理仿真里把参考轨迹「跑成」可跟踪的样子**

> 📅 阅读日期: 2026-05-13
> 🏷️ 板块: Motion Retargeting
> ℹ️ 笔记已对照 [arXiv HTML 2605.06593v1](https://arxiv.org/html/2605.06593v1) 与 arXiv 元数据（SIGGRAPH 2026 / TOG）整理；实现与定理细节以原文为准。

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **arXiv** | [2605.06593v1](https://arxiv.org/abs/2605.06593) |
| **HTML 全文** | [2605.06593v1 (HTML)](https://arxiv.org/html/2605.06593v1) |
| **PDF** | [arXiv PDF](https://arxiv.org/pdf/2605.06593v1.pdf) |
| **会议 / 期刊** | **SIGGRAPH 2026**（arXiv `comment` 标注）；ACM TOG 正式出版信息见论文页 |
| **发布时间** | 2026 年 5 月（arXiv） |

**作者**: David Müller, Agon Serifi, Sammy Christen, Ruben Grandia, Espen Knoop, Moritz Bächer

**一行定位**：把「生成可模仿参考」与「学会跟踪它」放进 **同一个物理仿真回路**：**上层**优化少量、可解释的重定向参数 \(\mathbf{p}\)，**下层**用 RL 学 \(\pi_\phi(a|o,g)\) 跟踪由 \(\mathbf{p}\) 诱导的参考 \(\mathbf{g}_t\)；用 **TTSA 式双时间尺度更新** 与 **对上层梯度的结构化近似**，避免在每个内层 RL 收敛后再求隐式 Hessian 那种不现实开销。

---

## 🎯 一句话总结

针对传统几何重定向需要 **手工接触模板 / 大量调参**、且仍产生 **脚滑、自碰、动力学不可行** 等问题，ReActor 提出 **物理感知、RL 内嵌的双层框架**：用户只给 **稀疏语义刚体对应** 与名义姿态对齐，系统自动搜索一组 **有界偏移参数** 把源运动 \(\mathbf{m}_t\) 映到参数化参考 \(\mathbf{g}_t(\mathbf{p})\)；下层策略在仿真里跟踪 \(\mathbf{g}_t\)，上层最小化 \(\mathbf{g}\) 与仿真 rollout 状态 \(\mathbf{s}_t\) 的误差。论文在 **两台人形 + 四足** 上展示跨大差异本体的重定向，并分析近似梯度与泛化行为。

---

## 📌 英文缩写速查

| 缩写 | 含义 | 备注 |
|------|------|------|
| **TTSA** | Two-Timescale Stochastic Approximation | 上层慢、下层快（相对）联合更新 |
| **RFC** | Residual Force Control | 根上施辅助力矩帮助跨数据集泛化；论文对 wrench 施惩罚与死区 |
| **RSI** | Reference State Initialization | 经典 motion imitation 技巧；本文因本体不同需改初始化 |
| **AMASS** | 大规模人体动作库 | 实验数据来源之一 |

---

## ❓ 和「DeepMimic 式模仿」差在哪？

- **DeepMimic**：给定一条（多半已手工修好）参考，RL 学跟踪。
- **ReActor**：参考本身 **尚未** 与目标机器人对齐；**同时**学「怎么改参考」与「怎么跟改完的参考」。  
换言之，它补的是 **embodiment gap 的上游**，而不是只优化下游 tracking 增益。

---

## 🧭 双层优化结构（mermaid）

<div class="mermaid">
flowchart TB
    subgraph UPPER["上层：重定向参数 p"]
        P0["用户：稀疏刚体语义对应 + 名义姿态"] --> P1["全局尺度 s + nominal 变换<br/>（自动从输入抽取）"]
        P1 --> P2["有界可学习偏移<br/>p_pos, p_ori, p_z"]
        P2 --> G["参数化参考轨迹 g_t(p)"]
    end

    subgraph LOWER["下层：RL 跟踪"]
        G --> RL["策略 pi_phi(a|o,g_t)"]
        RL --> SIM["物理仿真 + 接触动力学"]
        SIM --> S["状态 rollout s_t"]
    end

    S --> L["上层损失 L = E[l(g_t - s_t)]"]
    L -->|"TTSA + 简化梯度 d_p L"| P2

    subgraph OUT["输出"]
        S --> O1["artifact 较少的参考运动"]
        O1 --> O2["可直接用于下游模仿 / tracking 训练"]
    end

    style UPPER fill:#e8f4fd,stroke:#1f78b4
    style LOWER fill:#fdebd0,stroke:#e67e22
    style OUT fill:#e8f8e8,stroke:#27ae60
</div>

---

## 🔧 方法详解

### 1. 双层问题写法（Sec. 3）

外层：\(\min_{\mathbf{p}\in\mathcal{P}} \mathcal{L}(\mathbf{p}, \phi^\*(\mathbf{p}))\)，约束 \(\phi^\*(\mathbf{p}) = \arg\max_\phi \mathcal{R}(\mathbf{p},\phi)\)。  
内层：标准 **最大化回报** 的 RL；外层把 **仿真轨迹与参考的失配** 当监督。直觉上，\(\mathbf{p}\) 把「人」那边的帧 **抬到** 机器人能跟上的流形附近，\(\phi\) 负责在 **非光滑接触** 下真的跑起来。

### 2. 上层梯度为何能「算得动」（Sec. 4）

完全等内层收敛再对 \(\mathbf{p}\) 求导会爆炸慢。作者采用 **单循环 bilevel**，并在总导数

\[
\mathrm{d}_{\mathbf{p}} \ell(\mathbf{g}_t - \mathbf{s}^\*_t)
  = \partial_{\mathbf{g}_t}\ell\,\mathrm{d}_{\mathbf{p}}\mathbf{g}_t
  + \partial_{\mathbf{s}^\*_t}\ell\,\mathrm{d}_{\mathbf{p}}\mathbf{s}^\*_t
\]

里，利用 **对称损失** \(\partial_{\mathbf{s}}\ell = -\partial_{\mathbf{g}}\ell\) 与 **「最优轨迹对参考的响应可标量近似」** \(\mathrm{d}_{\mathbf{p}}\mathbf{s}^\* \approx \alpha \,\mathrm{d}_{\mathbf{p}}\mathbf{g}\) 的假设，把敏感项收成 **\((1-\alpha)\,\partial_{\mathbf{g}}\ell\,\mathrm{d}_{\mathbf{p}}\mathbf{g}\)** 的实用估计，再用当前策略 rollout 的样本做蒙特卡洛近似。读者可把 \(\alpha\) 理解成 **「机器人有多听话地跟着 g 走」** 的黑盒灵敏度旋钮。

### 3. 参数化 \(\mathbf{g}_t\)（Sec. 5）

- 从名义 T-pose 对齐开始：**根高度比** 给出全局尺度 \(s = h_{\text{target}}/h_{\text{source}}\)。
- 对每个用户指定的刚体对，在源局部坐标里存 **常数 nominal 偏移** \(\mathbf{x}^b_{\text{nom}}, \mathbf{R}^b_{\text{nom}}\)，把缩放后的源骨架与目标帧对齐。
- 优化变量：**小范数约束下的** \(\mathbf{p}^b_{\text{pos}}, \mathbf{p}^b_{\text{ori}}\) 以及 **每条运动的可学习竖直平移** \(p_z\)（处理 AMASS 类数据里残余的穿地 / 漂浮）。
- 位置、线速度、角速度项用 **平方误差**；旋转用 **测地线 Log 映射范数**；对欠驱动关节可只惩罚 swing/twist 子分量。

### 4. 下层 RL（Sec. 6 摘要）

- **动作**：关节 PD 目标 + **根残差力矩（RFC）**，并对 wrench 做 **惩罚 + 连续死区**，鼓励在不需要时预测精确零外力。
- **观测**：根高度、投影重力、根线角速度、关节状态、动作历史，外加 **retargeting phase 变量** \(\psi_t\)：用于在 episode 开头先把机器人 **摆到可跟踪姿态**，再逐步打开跟踪奖励（避免一上来就巨大误差）。
- **初始化**：因本体不同，不能 RSI 到同构关节；改为 **源根状态 + 名义关节附近高斯扰动**，让策略自己学会对齐。

---

## 📊 实验阅读抓手

1. **与几何 / 学习基线比**：脚滑、自碰、关节突变等 **artifact 指标** 是否稳定下降。  
2. **下游 tracking**：用 ReActor 清洗后的参考训练控制器，样本效率与最终误差。  
3. **跨形态**：四足等 **与人差异极大** 的本体，验证「稀疏对应 + 自动寻参」是否仍 work。  
4. **消融**：去掉 bilevel 或近似梯度假设后，外层是否不稳定或陷入差解。

---

## 🤔 自测问答

**Q1：RFC 会不会「作弊」把物理问题糊过去？**  
A：论文明确区分 **retargeting vs motion imitation**：此处允许根辅助力是为了 **在形态差异极大时仍能跨 AMASS 学到通用跟踪器**，并通过 **强惩罚 + 死区** 逼策略在可行时关掉外力；下游若追求完全物理真实，可把 RFC 逐步收紧或换硬跟踪设定做第二阶段。

**Q2：我要提供多少人工？**  
A：**语义刚体对 + 根对 + 名义姿态**；不需要手写整条接触时间表——这与许多 IK 管线「先猜接触再优化」形成对比。

**Q3：主要风险点？**  
A：**假设 \(\mathrm{d}_{\mathbf{p}}\mathbf{s}^\* \approx \alpha \mathrm{d}_{\mathbf{p}}\mathbf{g}\)** 是实用近似而非严格定理；在强多模态接触任务上，外层可能仍需调 \(\eta\) 与损失权重 \(w_x, w_R, \ldots\) 的相对比例。

---

## 🔗 相关笔记与外链

- 几何强基线（同板块）：`Retargeting_Matters__...`（GMR）
- 神经分布映射视角：`Make_Tracking_Easy__...`（NMR，arXiv 2603.22201）
- 本文 HTML：[2605.06593v1](https://arxiv.org/html/2605.06593v1)

---

## 📚 引用（BibTeX 备忘）

```bibtex
@article{muller2026reactor,
  title={ReActor: Reinforcement Learning for Physics-Aware Motion Retargeting},
  author={M{\"u}ller, David and Serifi, Agon and Christen, Sammy and Grandia, Ruben and Knoop, Espen and B{\"a}cher, Moritz},
  journal={arXiv preprint arXiv:2605.06593},
  year={2026}
}
```
