---
layout: paper
paper_order: 1
title: "HANDOFF: Humanoid Agentic Task-Space Whole-Body Control via Distilled Complementary Teachers"
zhname: "HANDOFF：用「互补教师蒸馏」打造任务空间人形全身控制器"
category: "Loco-Manipulation and WBC"
---

# HANDOFF: Humanoid Agentic Task-Space Whole-Body Control via Distilled Complementary Teachers
**HANDOFF：在「任务规划」与「全身控制」之间设计一个紧凑的 10 维任务空间接口（底盘速度 + 根高 + 双腕目标），把「全身动作跟踪 / 行走 / 跌倒恢复」三位互补专家通过上下文门控的多教师 KL 蒸馏融进一个 MoE 学生策略，从而既能像 SOTA 一样精准跟踪速度、又拥有最大的稳健操作工作空间，并可直接接入 VLM 规划器执行自然语言指令、无需任务专属微调**

> 📅 阅读日期: 2026-06-21
>
> 🏷️ 板块: 04 Loco-Manipulation / WBC · 任务空间接口 · 多教师蒸馏 · 混合专家(MoE) · VLM 规划 · Unitree G1
>
> 🔁 推进轨: 模块轮转（14_Human_Motion → **04_Loco-Manipulation_and_WBC**）

---

## 📋 基本信息

| 项目 | 链接 |
|---|---|
| 时间 | 2026 年 6 月 4 日（arXiv v1） |
| arXiv | [2606.06493](https://arxiv.org/abs/2606.06493) · [PDF](https://arxiv.org/pdf/2606.06493) · [HTML](https://arxiv.org/html/2606.06493v1) |
| 项目页 | [lzyang2000.github.io/HANDOFF](https://lzyang2000.github.io/HANDOFF/) |
| 代码 | [github.com/lzyang2000/HANDOFF](https://github.com/lzyang2000/HANDOFF) |
| 作者 | Lizhi Yang、Junheng Li、Nehar Poddar、Yiling Hou、Gio Huh、Robert Griffin、Georgia Gkioxari、Aaron D. Ames |
| 机构 | 加州理工 AMBER Lab（Caltech）· 人机认知研究所（IHMC） |
| 实验平台 | Unitree G1 人形机器人（29 自由度） |
| 主题 | cs.RO · 人形全身控制 / 任务空间接口 / 策略蒸馏 |

---

## 🎯 一句话总结

> 人形机器人要把「高层任务规划」接到「底层全身控制」上，长期缺一个**好用的命令接口**：太密集（逐帧运动参考）规划器难产出，太稀疏（只给速度）又表达不了操作。HANDOFF 提出一个**紧凑的 10 维任务空间接口**——底盘平面速度 + 偏航角速度 + 根部高度 + 左右手腕的 3D 目标位置；并用**多教师 KL 蒸馏**把三位「各管一摊」的专家（全身动作跟踪、行走、跌倒恢复）按上下文门控融进一个 **MoE 学生策略**。结果：在 Unitree G1 上既能逼近 SOTA 的速度跟踪精度，又拿到**同类中最大的稳健操作工作空间**（0.31 m³，可行率 90.8%），还能直接挂上 VLM 规划器执行自然语言任务，**无需任务专属数据或控制器微调**。

---

## 📌 英文缩写速查

| 缩写 | 含义 |
|---|---|
| WBC | Whole-Body Control，全身控制 |
| MoE | Mixture-of-Experts，混合专家：用门控网络在多个子网络间路由/混合 |
| KL Distillation | 用 KL 散度把教师策略的动作分布蒸馏给学生 |
| PPO | Proximal Policy Optimization，近端策略优化（强化学习常用算法） |
| AMP | Adversarial Motion Prior，对抗式动作先验（用判别器鼓励动作自然） |
| VLM | Vision-Language Model，视觉语言模型 |
| DoF | Degrees of Freedom，自由度 |
| IK | Inverse Kinematics，逆运动学 |

---

## ❓ 论文要解决什么问题？

人形机器人做「任务规划 → 全身控制」对接时，**命令接口（command interface）的设计**是关键瓶颈：

- **接口太密集**：要求规划器给出逐帧的全身运动参考（kinematic reference），几何/VLM/人类规划器都很难直接产出；
- **接口太稀疏**：只给底盘速度，能走但表达不了「把手伸到某个 3D 位置去操作物体」这类操作意图；
- **单一专家难兼顾**：纯动作跟踪策略行走/速度跟踪不可靠；纯行走策略不会精细操作；都不会摔倒后爬起来。

HANDOFF 的目标：设计一个**直观、通用、模块化、且全身可表达**的紧凑接口，并训练一个能稳定吃下这个接口、同时具备「行走 + 操作 + 摔倒恢复」的统一控制器。

---

## 🔧 方法详解

### 1. 10 维任务空间接口

控制器接收的命令向量：

$$c_t = [\,v_x,\ v_y,\ \omega_z,\ z,\ p_L^P,\ p_R^P\,]$$

- $v_x, v_y$：底盘平面线速度；$\omega_z$：偏航角速度
- $z$：根部（pelvis）高度标量——支持下蹲、抬高
- $p_L^P, p_R^P$：**左右手腕在 pelvis 坐标系下的 3D 目标位置**

这个接口对「几何规划器 / VLM / 人」都友好，跨操作任务通用，并把感知—规划—控制解耦，虽紧凑却保留了全身表达力。

### 2. 三位互补教师（各自专精）

| 教师 | 训练方式 | 提供的能力 |
|---|---|---|
| **全身动作跟踪教师**（29-DoF） | 重定向人类动作片段 + 非对称 actor-critic PPO | 姿态、伸够、下蹲、双臂协调先验（但行走/纯速度跟踪不可靠） |
| **行走教师**（15-DoF 身体切片） | 平地、基于任务的速度跟踪奖励；手臂用课程混合动作样本增稳 | 可靠的速度跟踪与步态稳定 |
| **跌倒恢复教师**（29-DoF） | AMP 判别器 + 精选「摔倒-爬起」数据 + 恢复-重置课程 | 跌倒后自主恢复 |

### 3. 上下文门控的多教师 KL 蒸馏（→ MoE 学生）

学生（29-DoF）以 **MoE + 上下文路由**从三位教师学习：

- **上下文信号** $x_t = (\lVert c_t^{vel}\rVert,\ \text{recover}_t)$：指令速度大小 + 二值恢复标志
- **身体切片（腿+腰）**：在「全身跟踪教师」与「行走教师」之间按速度门控做凸混合，权重 $\alpha = \sigma\big((\lVert c^{vel}\rVert - 0.1)/0.02\big)$——低速偏跟踪、高速偏行走
- **手臂切片**：全程锚定到「全身跟踪教师」（保操作表达力）
- **恢复覆盖**：恢复标志激活时，「跌倒恢复教师」接管全部监督

学生损失 = PPO + 上下文 KL 项（身体/手臂/恢复）+ MoE 负载均衡 + 恢复路由损失。好处是**运行时无需切换策略**即可平滑地在专家间切换。

### 4. VLM 智能体规划器（接口的上游）

把自然语言指令拆成原子任务（正则 + LLM 兜底），再：VLM 检测 2D 点/框 → 投影到 RGB-D 点云得到 pelvis 系航点 → 航点跟踪器算出 $(v_x, v_y, \omega_z)$ → 技能选择器输出根高与双腕目标 → 基于运动学的腕部修正让夹爪保持水平。**整套规划无需任务专属数据或控制器微调**。

---

## 🧭 整体流程（mermaid）

<div class="mermaid">
flowchart LR
    subgraph PLAN["🧠 上游：VLM 智能体规划"]
        L["自然语言指令"]
        V["VLM 检测 2D 点/框<br/>→ RGB-D 点云航点"]
        S["技能选择器"]
        L --> V --> S
    end

    subgraph IF["🔌 10 维任务空间接口 c_t"]
        C["v_x, v_y, ω_z<br/>+ 根高 z<br/>+ 左右腕目标 p_L, p_R"]
    end

    subgraph TEACH["🎓 三位互补教师"]
        T1["全身动作跟踪教师<br/>(PPO, 29-DoF)"]
        T2["行走教师<br/>(速度跟踪, 15-DoF)"]
        T3["跌倒恢复教师<br/>(AMP, 29-DoF)"]
    end

    subgraph STU["🤖 MoE 学生策略 (29-DoF)"]
        X["上下文 x_t<br/>(速度大小, 恢复标志)"]
        G["门控/路由<br/>速度门控凸混合 + 恢复覆盖"]
        STUP["统一全身控制策略"]
        X --> G --> STUP
    end

    S --> C
    C --> STUP
    T1 -. KL 蒸馏(手臂全程/低速身体) .-> STUP
    T2 -. KL 蒸馏(高速身体) .-> STUP
    T3 -. KL 蒸馏(恢复时接管) .-> STUP
    STUP --> ROBOT["Unitree G1 实机执行"]
</div>

---

## 📊 实验与结果

- **平台**：Unitree G1（29-DoF）。
- **评测指标**：① 速度跟踪——指令与实际底盘速度的平均绝对误差（[-1, 1] m/s 扫频）；② 稳健工作空间——双腕可达性 = 凸包体积 × 可行率（前向半空间 x≥0）。
- **基线**（均加差分 IK 头以公平对比腕部目标）：FALCON、OpenHomie、AMO、SONIC。
- **主要结果**（Ours + 稳定性 + 恢复 变体）：
  - $v_x$ 误差 **0.06 m/s**（SONIC 0.03，接近 SOTA）；$v_y$ 误差 0.18 m/s；$\omega_z$ 误差 0.06 rad/s；
  - 稳健工作空间 **0.31 m³**（同类最大）；可行率 **90.8%**；
  - 可由 VLM 规划器直接驱动执行自然语言操作任务，**无需任务专属微调**。
- **消融**（逐步累加）：纯动作跟踪最弱 → +双教师（速度跟踪大涨）→ +随机指令（补横向速度）→ +拆分 KL/MoE（补 $v_x$）→ +AMP 恢复（获得跌倒生还）→ +稳定性奖励（工作空间推到 0.31 m³）。每个专家都被验证为必要。

---

## ✨ 核心创新点

| 创新 | 描述 |
|---|---|
| **10 维任务空间接口** | 速度 + 根高 + 双腕 3D 目标，紧凑却全身可表达，规划器友好 |
| **互补教师蒸馏** | 行走 / 跟踪 / 恢复三位专家各练各的，再蒸馏成一个学生 |
| **上下文门控 MoE** | 按速度大小与恢复标志路由，运行时无缝切换、无需换策略 |
| **即插 VLM 规划** | 自然语言 → 接口命令，跨任务零专属微调 |

---

## ⚠️ 局限

1. **仅腕部位置**：接口只暴露 3D 位置，不含 6D 夹爪姿态，姿态残差靠运行时运动学修正兜底；
2. **感知受限**：单个固定头部 RGB-D 相机，前向视野受限；
3. **专家覆盖非穷尽**：当前为行走/跟踪/恢复三类，地形 / 接触 / 负载等专家留待未来。

---

## 📖 相关工作速览

- **FALCON / AMO**：力自适应 / 自适应运动优化的全身控制（本文基线）。
- **SONIC**：大规模动作跟踪的自然人形控制（速度跟踪强基线）。
- **OpenHomie / HOMIE**：等距外骨骼遥操作的 loco-manipulation。
- 与本模块 **SplitAdapter（负载解耦）**、**MotionWAM（世界动作模型）** 同属「让全身控制更通用、更易被上层调用」的探索线。
