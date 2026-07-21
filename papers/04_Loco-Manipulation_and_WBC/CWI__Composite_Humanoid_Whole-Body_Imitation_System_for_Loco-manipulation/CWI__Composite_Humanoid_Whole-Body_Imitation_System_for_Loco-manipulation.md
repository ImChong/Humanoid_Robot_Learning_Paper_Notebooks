---
layout: paper
paper_order: 1
title: "CWI: Composite Humanoid Whole-Body Imitation System for Loco-manipulation"
zhname: "CWI：面向移动操作的人形复合式全身模仿系统"
category: "Loco-Manipulation and WBC"
---

# CWI: Composite Humanoid Whole-Body Imitation System for Loco-manipulation
**CWI：按「目标」而非「架构」拆分——上半身用完整 AMASS 做跟踪、下半身用双判别器 AMP 学步态风格，再以多 critic + 师生蒸馏压成只需「双手位姿 + 速度指令」即可部署的单一全身控制器**

> 📅 阅读日期: 2026-07-21
>
> 🏷️ 板块: 04 Loco-Manipulation / WBC · 移动操作 · 全身模仿 · 对抗动作先验(AMP) · 多 critic · 师生蒸馏
>
> 🔁 推进轨: 模块轮转（14_Human_Motion → **04_Loco-Manipulation_and_WBC**）

---

## 📋 基本信息

| 项目 | 链接 |
|---|---|
| 时间 | 2026 年 6 月 |
| arXiv | [2606.27676](https://arxiv.org/abs/2606.27676) · [PDF](https://arxiv.org/pdf/2606.27676) · [HTML](https://arxiv.org/html/2606.27676v1) |
| 发布时间 | 2026-06-26 (v1) · **RAL 2026 录用** |
| 项目页 | [cwi-ral.github.io/CWI-RAL-Webpage](https://cwi-ral.github.io/CWI-RAL-Webpage)（含演示视频；截至 2026-07-21 未见开源代码仓库） |
| 作者 | Wenqi Ge、Junde Guo、Zhen Fu、Shunpeng Yang、Jiayu Chen、Hua Chen |
| 实验平台 | **LimX Oli 全尺寸人形**：1.65 m / 50 kg / 31 DoF（下肢 12 + 上肢 17 + 颈部 2） |
| 主题 | cs.RO · 人形全身控制 / 移动操作 / 模仿学习 |

---

## 🎯 一句话总结

> 人形移动操作要同时协调「走」和「操作」，可数据两头为难：**没有动捕**就只能靠稀疏奖励硬调，**用动捕**又受制于数据集不平衡（AMASS 里几乎全是站立、近零速度的片段，下肢稳定样本稀缺）。CWI 的关键思路是**按「优化目标」而非「网络架构」来解耦**：**上半身**直接吃**完整、未过滤的 AMASS**（重定向到机器人基座系，隔离手臂工作空间）做精确跟踪；**下半身**只用每类约 10 条专家级步行/下蹲片段，配**双判别器 AMP** 学「风格」而非逐帧参考。再用**多 critic** 化解「跟踪 vs 风格」的目标冲突，最后**师生蒸馏**把「拿满状态的教师」压成「只需双手关键点 + 速度/高度指令」的可部署学生——从而支持一台 VR 头显 + 手柄就能遥操作的全身移动操作，且仍保持整机（含腰部）自发协调。

---

## 📌 英文缩写速查

| 缩写 | 含义 |
|---|---|
| WBC | Whole-Body Control，全身控制 |
| AMP | Adversarial Motion Prior，对抗动作先验（用判别器把「像不像专家风格」变成奖励） |
| LSGAN | Least-Squares GAN，最小二乘 GAN 目标（此处判别器所用） |
| GAE | Generalized Advantage Estimation，广义优势估计 |
| PPO | Proximal Policy Optimization，近端策略优化 |
| DTW | Dynamic Time Warping，动态时间规整（容忍相位偏移的轨迹相似度，用作「自然度」指标） |
| AMASS | 大规模人体动捕数据集（此处作上半身动作先验） |

---

## ❓ 论文要解决什么问题？

移动操作（loco-manipulation）需要**下肢行走**与**上肢操作**协同，但现有两条路各有痛点：

- **无动捕（reward-only）方法**：靠人工奖励塑形，动作僵硬、稀疏奖励难训；
- **有动捕（MoCap-based）方法**：受**数据集不平衡**拖累——为了下肢稳定去过滤数据，会连带**丢掉大量有价值的上半身操作动作**；而 AMASS 本身又高度集中在「直立站姿（~0.85–0.90 m）+ 近零基座速度」，低身高/高速度的样本极少。

CWI 的核心主张：**不该对整份数据集统一过滤，而应按身体部位的「目标」分开取数**——上半身要「像人、覆盖广」，下半身要「稳、风格好」，二者需求根本不同。

---

## 🔧 方法详解

### 1. 目标导向的数据解耦（不是拆成两个控制器）
- **上半身**：用**完整 AMASS**（不过滤），重定向到机器人**基座系**，把手臂工作空间与行走解耦；以指数 L₂ 损失做精确跟踪。
- **下半身**：仅取每类**约 10 条专家级片段**（步行 / 下蹲），提供**风格先验**而非逐帧参考轨迹。
- 注意：策略网络仍是**单一全身策略**，解耦发生在「数据与奖励目标」层面，从而保留整机协调。

### 2. 下半身：双判别器 AMP
- 两个判别器分别管**步行**与**下蹲**风格，各对**下肢 4 帧状态转移窗口**打分，用 **LSGAN + 梯度惩罚**；
- **动态选择**：速度指令非零→走模式判别器，否则→蹲模式；
- 产出连续风格奖励 `max(0, 1 − 0.25·(D(τ)−1)²)`，鼓励「像专家」的步态，而无需逐帧对齐。

### 3. 多 critic 化解目标冲突
- 不再用单一价值函数硬扛「行走跟踪 / 上肢跟踪 / 风格」三类互相打架的目标；
- **每组目标各配一个 critic**，分组算 GAE 并在 minibatch 内归一化，防止高方差的对抗信号冲垮操作目标；
- 加权合并 `Â = Σ wᵢ·Âᵢ` 后接标准 PPO 裁剪目标。

### 4. 师生蒸馏：压成可部署单一策略
- **教师**：满状态 + 完整上半身参考（17 关节位置 + 肩/肘/腕/手的连杆位姿与关键点特征）；
- **学生（部署用）**：仅 **25 步本体感知历史** + 精简指令——**双手关键点 18D + 速度 2D + 高度 1D + 头部俯仰/偏航 2D = 23D**；
- 蒸馏损失 `L = L_RL + λ·‖μ_stu − μ_tea‖²`（λ 退火，平衡探索与模仿）。这套极简指令接口正好对齐 **VR 头显 + 手柄**遥操作。

### 5. 关键结果与消融
- **仿真对比**（LimX Oli 上复现 HOVER / FALCON / HOMIE）：成功率 ~99.9%，速度误差 **0.100 m/s**、角速度 **0.183 rad/s**、高度误差 **19.65 mm** 均为最优；末端位置误差 42.91 mm、朝向 0.171 rad 领先或持平；
- **消融**：去蒸馏→末端误差灾难性恶化 42.91→**173.2 mm**（学生无法只靠手位指令学会操作）；去多 critic→末端误差 42.91→55.49 mm；单一 AMP（合并走/蹲）→自然度 DTW 0.452→0.615；去 AMP→DTW 飙到 1.413、频繁滑步；去 AMASS 上半身先验→末端 42.91→62.32 mm 且整体跟踪退化；
- **真机**：拧瓶盖、小件装配、开门、击鼓、抓取-搬运-放置等；举箱时**腰部俯仰随手臂伸展自发调整**，展现无需显式躯干指令的整机协调。

---

### 🧭 整体流程（mermaid）

<div class="mermaid">
flowchart TD
    subgraph DATA["📚 目标导向数据解耦"]
        UP["🙆 上半身：完整 AMASS(未过滤)<br/>重定向到基座系"]
        LO["🦵 下半身：每类~10 条专家片段<br/>(步行 / 下蹲)"]
    end

    UP --> TR["🎯 上肢精确跟踪<br/>指数 L₂ 损失"]
    LO --> AMP["🎭 双判别器 AMP<br/>走/蹲动态切换<br/>LSGAN+梯度惩罚 → 风格奖励"]

    TR --> MC["🧮 多 critic<br/>行走/上肢/风格各一 critic<br/>分组 GAE + 归一化 → 加权优势"]
    AMP --> MC
    MC --> PPO["🔧 PPO 训练<br/>教师策略(满状态 + 完整上肢参考)"]

    PPO --> DIST["🎓 师生蒸馏<br/>L = L_RL + λ‖μ_stu−μ_tea‖²"]
    DIST --> STU["🤖 部署学生(23D 指令)<br/>双手关键点18D+速度2D+高度1D+头部2D<br/>+25 步本体感知历史"]
    STU --> DEP["🕹️ VR 头显+手柄遥操作<br/>LimX Oli · 拧盖/装配/开门/击鼓/搬运"]

    style DATA fill:#e8f4fd,stroke:#1f78b4,color:#0b3954
    style AMP fill:#f7e8fd,stroke:#9b59b6,color:#4a1c5d
    style MC fill:#fff4e6,stroke:#e67e22,color:#7d3c08
    style DIST fill:#eef7ee,stroke:#27ae60,color:#0f3d1e
    style DEP fill:#fde8e8,stroke:#c0392b,color:#641e16
</div>

---

## 💡 核心贡献

1. **按目标而非架构解耦**：上半身用完整 AMASS 求「广而准」，下半身用少量专家片段 + AMP 求「稳而美」，在**单一全身策略**内同时满足两类矛盾需求，规避「过滤数据丢操作样本」的困境；
2. **双判别器 AMP**：走/蹲各一判别器并动态切换，把步态「风格」变成可复用奖励，比合并判别器（自然度 DTW 0.452 vs 0.615）与无 AMP（1.413）都显著更稳；
3. **多 critic 目标解耦**：分组价值估计 + 归一化，防对抗高方差信号冲垮操作目标，末端精度与收敛均获益；
4. **极简可部署接口**：师生蒸馏把满状态教师压成「只要双手位姿 + 速度/高度」的学生，天然对齐 VR 遥操作，真机展现自发整机协调。

---

## 🤖 对人形机器人学习的启发

- **数据「分而取之」优于「统一过滤」**：当同一份动捕对上/下半身有相互冲突的取数标准时，按身体部位的目标分别配数据/奖励，比一刀切过滤更能保住信息量；
- **AMP 学「风格」而非「轨迹」**：下肢只需少量专家片段 + 判别器就能得到自然步态，省去逐帧参考与大规模下肢动捕，且走/蹲分判别器能进一步提升风格保真；
- **多 critic 是缓解多目标冲突的低成本手段**：与其手调一堆奖励权重去平衡跟踪与风格，不如分组估值 + 归一化，让对抗信号不再拖垮主任务；
- **蒸馏定义部署接口**：把「教师需要什么」与「部署能拿到什么」显式分离，用 BC 项把满状态能力搬进极简指令空间——这也是 HOVER / HANDOFF / Athena-WBC 等一脉相承的落地范式。

---

## 📁 资源对照

| 资源 | 内容 |
|---|---|
| [arXiv 2606.27676](https://arxiv.org/abs/2606.27676) | 论文正文（方法、消融、真机实验） |
| [PDF](https://arxiv.org/pdf/2606.27676) · [HTML](https://arxiv.org/html/2606.27676v1) | 在线阅读 |
| [项目页](https://cwi-ral.github.io/CWI-RAL-Webpage) | 演示视频与补充材料（截至 2026-07-21 未见开源代码仓库） |

> ℹ️ 备注：本环境网络出口对 arXiv 有限制，本笔记依据可获取的 Abstract 与 HTML 正文整理，方法机制与实验数值均取自官方描述；若后续释出代码可再补链接。

---

## 🔗 相关阅读

- **师生蒸馏 / 多教师 · 同模块**：[HANDOFF：任务空间全身控制的互补教师蒸馏](../HANDOFF__Humanoid_Agentic_Task-Space_Whole-Body_Control_via_Distilled_Teachers/HANDOFF__Humanoid_Agentic_Task-Space_Whole-Body_Control_via_Distilled_Teachers.md) · [Athena-WBC：能力对齐的动态/平衡专家](../Athena-WBC__Capability-Aligned_Policy_Experts_for_Long-Tail_Humanoid_Whole-Body_Control/Athena-WBC__Capability-Aligned_Policy_Experts_for_Long-Tail_Humanoid_Whole-Body_Control.md)；
- **上/下身解耦 · 负载自适应**：[SplitAdapter：负载感知的分解式移动操作](../SplitAdapter__Load-Aware_Humanoid_Loco-Manipulation_via_Factorized_Adaptation/SplitAdapter__Load-Aware_Humanoid_Loco-Manipulation_via_Factorized_Adaptation.md)；
- **通用全身控制器**：[General Humanoid WBC via Pretraining and Fast Adaptation](../General_Humanoid_Whole-Body_Control_via_Pretraining_and_Fast_Adaptation/General_Humanoid_Whole-Body_Control_via_Pretraining_and_Fast_Adaptation.md)。
