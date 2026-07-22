---
layout: paper
paper_order: 1
title: "HumoSlope: Physics-Guided Biomechanical Gait Adaptation for Humanoid Locomotion on Extreme Sloped Terrains"
zhname: "HumoSlope：极端坡地上的人形物理引导生物力学步态自适应"
category: "Locomotion"
---

# HumoSlope: Physics-Guided Biomechanical Gait Adaptation for Humanoid Locomotion on Extreme Sloped Terrains
**HumoSlope：两阶段物理引导框架——先用「贴合局部斜面的 ZMP 正则」立住斜坡平衡先验，再用「生物力学坡地步态适配器（BSGA）」按坡角调制质心高度与髋/膝分工（上坡髋主导推进、下坡膝主导制动），让 Unitree G1 仅凭本体感知盲走 32.1°（62.7% 坡度）的野外草坡**

> 📅 阅读日期: 2026-07-22
>
> 🏷️ 板块: 05 Locomotion · 坡地行走 · ZMP 正则 · 生物力学步态 · 本体感知 · 两阶段 PPO
>
> 🔁 推进轨: 模块轮转（04_Loco-Manipulation_and_WBC → **05_Locomotion**）

---

## 📋 基本信息

| 项目 | 链接 |
|---|---|
| 时间 | 2026 年 7 月（arXiv v1：2026-07-08） |
| arXiv | [2607.07830](https://arxiv.org/abs/2607.07830) · [PDF](https://arxiv.org/pdf/2607.07830) · [HTML](https://arxiv.org/html/2607.07830) |
| 作者 | Xuanyu Chen、Mohan Liu、Dengchen Mei、Zhihao Gu、Haitian Zhang、Kaimin Mao、Haiyue Zhu、Shijun Yan、Lin Wang |
| 机构 | 南洋理工大学（NTU）· 新加坡科技研究局（A*STAR） |
| 实验平台 | Unitree G1 人形（仿真 Isaac Lab + 真机野外草坡） |
| 主题 | cs.RO · 人形坡地行走 / 物理引导 RL / 本体感知 sim-to-real |

---

## 🎯 一句话总结

> 人形上下陡坡最容易「越走越蹲」（Groucho gait，长期低质心屈膝），既费力又易失稳。HumoSlope 不靠外部视觉，只用**本体感知**，把问题拆成两阶段攻：**阶段 I** 把 ZMP（零力矩点）平衡评估从「世界水平面」改到**局部斜面**上算，给出与地形一致的平衡先验；**阶段 II** 用一个**生物力学坡地步态适配器（BSGA）**，靠训练期的坡度描述子去**门控软奖励先验**——按坡角调**质心高度**、并让**上坡髋主导推进、下坡膝主导制动**、摆动腿髋 pitch 参考随坡角标定。整套用 **PPO** 两阶段训练（阶段 II 热启动 actor、重置 critic 以纳入特权观测），靠域随机化零样本上真机，Unitree G1 盲走 **32.1°（62.7% 坡度）** 草坡，并泛化到湿滑、波浪、平地。

---

## 📌 英文缩写速查

| 缩写 | 含义 |
|---|---|
| ZMP | Zero Moment Point，零力矩点（步态平衡稳定性的经典判据） |
| BSGA | Biomechanical Slope Gait Adapter，生物力学坡地步态适配器 |
| CoM | Center of Mass，质心 |
| PCA | Principal Component Analysis，主成分分析（此处用于压缩坡地地形描述子） |
| PPO | Proximal Policy Optimization，近端策略优化 |
| Groucho gait | 「格劳乔步态」：持续低质心屈膝行走的退化姿态 |

---

## ❓ 论文要解决什么问题？

人形在**陡坡**上行走面临两个叠加难点：

1. **平衡基准错位**：传统 RL 奖励以「世界水平面」为参考评估姿态与平衡，一旦上到斜面，机身相对重力方向本就该倾斜，硬拉回水平反而不稳。
2. **姿态退化（Groucho gait）**：为了稳，策略容易学成「一直蹲着屈膝走」，质心过低、膝关节峰值力矩畸高，既耗能又限制坡度上限；且上坡与下坡的合理下肢分工本不相同，单一策略难以自适应。

作者主张：**不必上外部视觉**，而是把「斜面几何」以**物理引导 + 生物力学先验**的方式注入奖励，让本体感知策略学会与坡度匹配的平衡与步态。

---

## 🔧 方法详解

### 阶段 I：贴合斜面的 ZMP 正则（Slope-Adaptive ZMP Regularization）
把 ZMP 的偏差评估放到**局部支撑斜面**上，而非世界水平参考：

- 以接触力加权的**支撑锚点**为基准，将「表观比力射线」与**估计的局部支撑平面**求交，得到斜面上的 ZMP 偏差 `d_zmp`；
- 奖励取 `r_zmp = exp(-d_zmp / σ_zmp)`，鼓励 ZMP 落在斜面支撑区内，从而建立**与地形一致的平衡先验**。

### 阶段 II：生物力学坡地步态适配器（BSGA）
用一个**仅训练期可见**的 5 维坡地描述子（含坡度 `θ_slope`、侧倾 `θ_bank`、坡度绝对值、以及上/下坡指示）去**门控三类软奖励**：

- **质心高度调制**：坡度相关的高度目标 `h_tgt = h_nom·cos(|θ_slope|) + ρ_slope·(b_up·𝟙_up + b_down·𝟙_down)`，缓解「越走越蹲」；
- **生物力学非对称分工**：**上坡髋主导推进、下坡膝主导制动**，贴合人类坡地运动学；
- **摆动腿引导**：按坡角标定的髋 pitch 参考，帮助抬腿越坡。

三项加权组成 `r_BSGA = w_com·r_com + w_bio·r_bio + w_swing·r_swing`，再叠加标准行走奖励与上身稳定/可行性正则。

### 训练与部署
- **算法**：PPO；**actor 只吃本体感知**（基座角速度、投影重力、速度指令、关节状态与动作历史），**部署零外感**；
- **特权 critic（仅训练）**：真实基座线速度 + 压缩的 49 点高程扫描 `ℋ_49` + 5 维 PCA 坡地描述子；
- **动作空间**：关节位置残差目标，交由底层 PD 跟踪；
- **两阶段衔接**：阶段 I 在混合地形训平衡先验；阶段 II 在坡道轨道地形上训练，**热启动 actor、重置 critic**以纳入特权观测；
- **仿真**：Isaac Lab（RTX 5090）数千并行环境 + 域随机化，零样本 sim-to-real。

### 关键结果
- **仿真（复合坡道基准）**：0°/10°/20° 成功率 100%，30° 仍达 **77.1%**，最大可达 **36°（73%）**；对照基线 URL、FastTD3、Gallant（含深度感知）在 30° 均为 **0%**；
- **真机**：Unitree G1 盲走野外草坡至 **32.1°（62.7% 坡度）**，并泛化到沥青、波浪、湿滑地形；
- **消融（20°）**：完整模型 98.2%；去掉 ZMP 正则骤降至 **55.6%**；去掉 BSGA **直接 0%**——两模块缺一不可，且 BSGA 明显抬高平均质心、缓解 Groucho gait。

---

### 🧭 整体流程（mermaid）

<div class="mermaid">
flowchart TD
    subgraph OBS["👁️ 观测（部署仅本体感知）"]
      PROP["🦿 本体感知<br/>角速度·投影重力·指令·关节·动作历史"]
      PRIV["🔒 特权观测（仅训练）<br/>真实线速度·49点高程 ℋ₄₉·5维PCA坡描述子"]
    end

    subgraph S1["① 贴合斜面的 ZMP 正则"]
      PLANE["📐 估计局部支撑斜面<br/>比力射线 ∩ 支撑平面"] --> ZMP["r_zmp = exp(-d_zmp/σ)<br/>斜面上评估平衡"]
    end

    subgraph S2["② 生物力学坡地步态适配器 BSGA"]
      DESC["🧭 坡度描述子门控"] --> COM["📏 质心高度调制<br/>h_tgt=h·cos|θ|+坡度偏置"]
      DESC --> BIO["🦵 上坡髋推进 / 下坡膝制动"]
      DESC --> SWING["🦿 摆动腿髋pitch参考(随坡角)"]
    end

    PROP --> ACTOR["🧠 PPO Actor<br/>关节位置残差目标"]
    PRIV -.-> CRITIC["📈 特权 Critic"]
    ZMP --> ACTOR
    COM --> ACTOR
    BIO --> ACTOR
    SWING --> ACTOR
    CRITIC --> ACTOR

    ACTOR --> DR["🎲 域随机化 · Isaac Lab"]
    DR --> REAL["🤖 零样本上真机<br/>Unitree G1 盲走 32.1° 草坡 · 泛化湿滑/波浪/平地"]

    style S1 fill:#e8f4fd,stroke:#1f78b4,color:#0b3954
    style S2 fill:#f7e8fd,stroke:#9b59b6,color:#4a1c5d
    style ACTOR fill:#fff4e6,stroke:#e67e22,color:#7d3c08
    style REAL fill:#fde8e8,stroke:#c0392b,color:#641e16
</div>

---

## 💡 核心贡献

1. **斜面一致的平衡先验**：把 ZMP 评估从世界水平面搬到**局部斜面**，用物理正则直接给出与地形匹配的平衡，避免「硬拉回水平」的失稳；
2. **生物力学步态自适应（BSGA）**：以坡度描述子门控软奖励，按坡角调质心高度、并区分**上坡髋推进 / 下坡膝制动**，系统性缓解 Groucho gait；
3. **纯本体感知 + 两阶段 PPO**：部署零外感、域随机化零样本上真机，Unitree G1 盲走陡坡并跨地形泛化，消融证明两模块缺一不可。

---

## 🤖 对人形机器人学习的启发

- **把「参考系」选对，比堆奖励更关键**：在斜面上以局部支撑面而非世界水平面评估平衡，是一处「物理引导」胜过「纯数据拟合」的典型；
- **生物力学先验可作为软门控**：用坡度描述子去调制（而非硬约束）髋/膝分工与质心高度，既保留 RL 的探索自由，又注入了人类运动学的合理结构；
- **本体感知也能上陡坡**：在明确的物理/生物力学奖励结构下，不依赖外部视觉也能盲走 32° 草坡，为低成本部署提供了参考；
- **两阶段（先平衡先验、后步态风格）** 再次印证「先立骨架、再塑风格」的课程式训练在复杂地形上的有效性。

---

## 📁 资源对照

| 资源 | 内容 |
|---|---|
| [arXiv 2607.07830](https://arxiv.org/abs/2607.07830) | 论文正文（两阶段方法、消融与数值结果） |
| [PDF](https://arxiv.org/pdf/2607.07830) · [HTML](https://arxiv.org/html/2607.07830) | 在线阅读 |
| 代码 / 项目页 | 论文未见公开代码或项目页（基于 Unitree RL Lab / Isaac Lab 生态实现）；若后续释出可再补链接 |

> ℹ️ 备注：本环境网络出口对 arXiv 有限制，本笔记依据可获取的 Abstract 与 HTML 正文整理，方法机制与实验数值均取自官方描述。

---

## 🔗 相关阅读

- **感知 / 复杂地形 · 同模块**：[RPL：挑战地形上的鲁棒感知行走](../RPL__Learning_Robust_Humanoid_Perceptive_Locomotion_on_Challenging_Terrains/RPL__Learning_Robust_Humanoid_Perceptive_Locomotion_on_Challenging_Terrains.md) · [CMR：非结构地形收缩映射嵌入](../CMR__Contractive_Mapping_Embeddings_for_Robust_Humanoid_Locomotion/CMR__Contractive_Mapping_Embeddings_for_Robust_Humanoid_Locomotion.md)；
- **台阶 / 落脚 / 高平台**：[FastStair：学习跑上楼梯](../FastStair__Learning_to_Run_Up_Stairs_with_Humanoid_Robots/FastStair__Learning_to_Run_Up_Stairs_with_Humanoid_Robots.md) · [APEX：自适应高平台穿越](../APEX_Learning_Adaptive_High-Platform_Traversal_for_Humanoid_Robots/APEX_Learning_Adaptive_High-Platform_Traversal_for_Humanoid_Robots.md) · [Walk the PLANC：受限落脚点的敏捷行走](../Walk_the_PLANC__Physics-Guided_RL_for_Agile_Humanoid_Locomotion_on_Constrained_Footholds/Walk_the_PLANC__Physics-Guided_RL_for_Agile_Humanoid_Locomotion_on_Constrained_Footholds.md)；
- **负载鲁棒 / 地形可供性**：[TACT-ful：多通道地形可供性 + 负载柔顺](../TACT-ful__Multi-Channel_Terrain_Affordance_and_Compliance_for_Payload-Robust_Locomotion/TACT-ful__Multi-Channel_Terrain_Affordance_and_Compliance_for_Payload-Robust_Locomotion.md)。
