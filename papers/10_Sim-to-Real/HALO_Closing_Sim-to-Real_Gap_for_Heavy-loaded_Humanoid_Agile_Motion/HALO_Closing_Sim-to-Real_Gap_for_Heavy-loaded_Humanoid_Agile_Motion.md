---
layout: paper
paper_order: 7
title: "HALO: Closing Sim-to-Real Gap for Heavy-loaded Humanoid Agile Motion Skills via Differentiable Simulation"
zhname: "HALO：用可微仿真做两阶段系统辨识——先把名义机器人模型标准，再辨识未知负载的质量分布，让 RL 策略在负重条件下零样本迁移到真机"
category: "Sim-to-Real"
---

# HALO: Closing Sim-to-Real Gap for Heavy-loaded Humanoid Agile Motion Skills via Differentiable Simulation

**人形机器人干活时常要背/抱不知质量的负载，这会让"仿真里练好的策略"到真机上动作变形。HALO 把可微仿真（MuJoCo XLA）当作系统辨识引擎：第一阶段标准本体动力学，第二阶段在线辨识未知负载的质量分布，把结构化的模型偏差在训练前就消掉，从而让 RL 策略在负重条件下零样本迁移、敏捷动作更稳更准。**

> 📅 阅读日期: 2026-06-10
>
> 🏷️ 板块: Sim-to-Real · 可微仿真 · 系统辨识 · 负载自适应 · 零样本迁移
>
> 🔁 推进轨: 模块轮转（09_State_Estimation → **10_Sim-to-Real**）

---

## 📋 基本信息

| 项目 | 链接 |
|---|---|
| arXiv | [2603.15084](https://arxiv.org/abs/2603.15084) |
| HTML | [在线阅读](https://arxiv.org/html/2603.15084) |
| PDF | [下载](https://arxiv.org/pdf/2603.15084) |
| 项目主页 | [mwondering.github.io/halo-humanoid](https://mwondering.github.io/halo-humanoid/) |
| **发布时间** | 2026-03-16 (arXiv) |
| 源码 | 暂未见公开代码仓库（以项目主页与论文为准） |

**作者**：Xingyi Wang, Chenyun Zhang, Weiji Xie, Chao Yu, Wei Song, Chenjia Bai, Shiqiang Zhu
**主题**：负重条件下的人形敏捷运动 sim-to-real——把可微仿真系统辨识嵌入 RL 控制流水线

---

## 🎯 一句话总结

主流 sim-to-real 用**域随机化（DR）**把摩擦、惯性、增益等未知量"盖住"，但当机器人**背负未知负载**时，质量、质心、惯量发生大幅偏移，DR 的覆盖范围要么不够、要么过宽导致策略保守。HALO 换一条路：**与其随机化，不如辨识**。它把参数辨识写成**可微物理仿真里的轨迹级优化问题**——用 MuJoCo XLA 的解析梯度，直接从真机交互数据里梯度下降地拟合物理参数。分两阶段：① 标准**名义机器人模型**消除本体固有的 sim-real 差距；② 进一步辨识**未知负载的质量分布**。把结构化的模型偏差在策略训练**之前**就显式减小，于是 RL 策略可在负重条件下**零样本**迁移到硬件，敏捷动作的跟踪精度与鲁棒性都优于已有基线。

---

## 📌 英文缩写速查

| 缩写 | 全称 | 解释 |
|---|---|---|
| Sim-to-Real | - | 仿真训练、真实部署 |
| DR | Domain Randomization | 域随机化：随机化物理参数以求鲁棒 |
| SysID | System Identification | 系统辨识：从数据反推物理参数 |
| RL | Reinforcement Learning | 强化学习 |
| MJX | MuJoCo XLA | MuJoCo 的可微 / GPU 并行版本，支持解析梯度 |
| CoM | Center of Mass | 质心 |

---

## ❓ 论文要解决什么问题？

**问题陈述**：人形机器人在真实场景里经常需要**搬运、背负、抱持未知质量的负载**。负载会改变整机的质量、质心与惯量分布，引入显著的 sim-real mismatch：

- 仿真里"练好"的敏捷动作（跳跃、转身、快速踏步等）一旦上真机负重，**动作变形、跟踪误差变大、甚至失稳**；
- 纯靠**域随机化**硬扛：负载范围一旦放大，策略被迫学得保守、牺牲敏捷性；范围放小又覆盖不到真实负载。

**核心问题**：

> 能否在策略训练**之前**就把"本体 + 未知负载"的动力学**辨识准**，从而无需依赖宽泛域随机化，让负重条件下的敏捷策略**零样本**迁移到真机？

---

## 🔧 方法拆解：可微仿真驱动的两阶段系统辨识

### 核心思想：把辨识写成可微仿真里的优化问题

HALO 在**可微物理仿真器 MuJoCo XLA** 里运行机器人模型，把"仿真轨迹 vs 真机轨迹"的差异当作损失，利用**跨多步仿真的解析梯度**，直接对物理参数做**梯度下降**。相比无梯度方法（如进化策略），可微仿真能高效地从真机交互数据里拟合参数。

### 第一阶段：标准名义机器人模型

用真机数据校准**本体自身**的动力学参数，减少机器人固有（无负载时就存在）的 sim-real 差距。这一步把"基准模型"对齐到真机，是后续负载辨识的前提。

### 第二阶段：辨识未知负载的质量分布

在标准好的本体模型之上，进一步辨识**未知负载的质量分布**（质量、质心位置等）。负载参数同样通过可微仿真的轨迹级优化求解。

### 关键效果：训练前消除结构化偏差

两阶段辨识把**结构化的模型偏差**（本体 + 负载）在策略训练**之前**显式减小，使仿真本身就贴近真机。于是 RL 策略训练完即可**零样本**部署到负重硬件，而不必依赖宽泛域随机化来"覆盖"未知负载。

---

## 🧭 整体流程（mermaid）

<div class="mermaid">
flowchart TB
    REAL["🤖 真机负重交互数据<br/>(本体 + 未知负载)"]

    subgraph SYSID["🔬 可微仿真系统辨识 (MuJoCo XLA)"]
        OPT["轨迹级优化<br/>min ‖sim 轨迹 − real 轨迹‖<br/>用解析梯度做梯度下降"]
        S1["① 标准名义机器人模型<br/>消除本体固有 sim-real 差距"]
        S2["② 辨识未知负载质量分布<br/>(质量 / 质心 / 惯量)"]
        OPT --> S1 --> S2
    end

    REAL --> OPT
    PARAM["📦 标准后的动力学参数<br/>(本体 + 负载)"]
    S2 --> PARAM

    subgraph TRAIN["🎮 RL 训练 (训练前已减小结构化偏差)"]
        SIM["高保真仿真<br/>(用辨识参数, 弱化对宽域随机化的依赖)"]
        POL["🦿 敏捷运动策略 π"]
        PARAM --> SIM --> POL
    end

    subgraph DEPLOY["🚀 零样本部署"]
        HW["负重硬件上直接运行<br/>敏捷动作: 跳跃 / 转身 / 快速踏步"]
        RES["✅ 跟踪精度↑  ✅ 敏捷性与鲁棒性↑<br/>优于已有基线"]
        HW --> RES
    end

    POL -. 零样本 .-> HW

    style SYSID fill:#e8f4fd,stroke:#1f78b4
    style TRAIN fill:#f3e8ff,stroke:#8e44ad
    style DEPLOY fill:#e8f8e8,stroke:#27ae60
</div>

---

## 💡 核心贡献

1. **范式贡献**：提出"**辨识 > 随机化**"在**负重人形**上的落地——把"用 DR 覆盖未知负载"替换为"用可微仿真辨识负载"，在训练前消除结构化偏差；
2. **方法贡献**：一个**两阶段可微仿真系统辨识**框架（先标准本体、再辨识负载质量分布），把辨识写成 MuJoCo XLA 里的**轨迹级梯度优化**，直接吃真机交互数据；
3. **迁移贡献**：使 RL 策略在**负重条件下零样本迁移**到真机，敏捷动作的跟踪精度、敏捷性与鲁棒性均优于已有基线；
4. **工程价值**：揭示"负载不确定性"是人形 sim-to-real 的关键瓶颈，并给出可微仿真这一系统化的对齐工具。

---

## 📊 关键设定与结果

| 维度 | 值 |
|---|---|
| 任务 | 负重条件下的人形敏捷运动技能 |
| 辨识工具 | 可微仿真 MuJoCo XLA（解析梯度） |
| 辨识结构 | 两阶段：① 名义机器人模型 ② 未知负载质量分布 |
| 优化形式 | 轨迹级参数优化（梯度下降） |
| 迁移方式 | 零样本（训练前已减小结构化偏差） |
| 关键结果 | 参数辨识更精确、运动跟踪更准、敏捷性与鲁棒性显著提升，优于基线 |

> 📌 各任务具体辨识误差、跟踪精度数值、基线对比与消融请以论文 PDF 实验章节为准。

---

## 🤖 对 Sim-to-Real 领域的意义

| 方向 | 含义 |
|---|---|
| **聚焦"负载不确定性"** | 多数 sim-to-real 关注摩擦/增益/延迟，HALO 把**未知负载**这一被忽视却高频的现实约束当成主攻点 |
| **可微仿真做 SysID** | 与 [PACE](../PACE_Systematic_Sim-to-Real_Transfer_for_Diverse_Legged_Robots/PACE_Systematic_Sim-to-Real_Transfer_for_Diverse_Legged_Robots.md)（CMA-ES 无梯度辨识）路线互补——HALO 用解析梯度，样本效率更高 |
| **"辨识 vs 随机化"的再平衡** | 与 DR 主流路线（如 [PolySim](../PolySim__Bridging_the_Sim-to-Real_Gap_for_Humanoid_Control_via_Multi-Simulato/PolySim__Bridging_the_Sim-to-Real_Gap_for_Humanoid_Control_via_Multi-Simulato.md)）对照：DR 盖住 gap，HALO 量准 gap |
| **敏捷动作友好** | 训练前对齐动力学，避免 DR 带来的保守化，对负重敏捷技能尤其重要 |

---

## 🎤 面试参考

**Q：背个未知负载，为什么不直接把负载范围塞进域随机化里练？**
A：可以，但有代价。负载会大幅改变质量/质心/惯量，要"覆盖"这些变化，DR 范围必须放得很宽，策略就被迫学得保守、牺牲敏捷性；范围放窄又覆盖不到真实负载。HALO 的思路是：既然能从真机数据里把负载**辨识准**，就不需要让策略去硬扛一大片未知范围——把不确定性变成已知量。

**Q：为什么用可微仿真而不是 CMA-ES 这类无梯度辨识？**
A：可微仿真器（MuJoCo XLA）能提供**跨多步仿真的解析梯度**，把参数辨识当成可微优化直接梯度下降，样本效率通常高于无梯度进化策略。代价是需要一个可微的仿真管线，工程门槛更高，但换来更快、更精的参数拟合。

**Q：为什么要分两阶段，而不是一次把本体和负载一起辨识？**
A：解耦能减少歧义。本体动力学（关节摩擦、传动等）和负载（质量分布）是两类不同来源的偏差，如果混在一起优化，参数容易"互相补偿"导致辨识不准。先把无负载时的本体模型标准，再在此基准上辨识负载，能让每一步的优化目标更干净、结果更可靠。

**Q：这和 ASAP 那种"残差动力学对齐"是什么关系？**
A：目标相近（都想让仿真贴近真机），手段不同。ASAP 学一个**残差动作/动力学**来补偿差距，HALO 直接**辨识物理参数**（尤其是负载质量分布）。HALO 的参数是物理可解释的，且专门处理"负载变化"这一结构化偏差；两者可以叠加：先用 HALO 辨识物理参数，再用残差项补偿剩余的非结构化误差。

---

## 🔗 相关阅读

- [Towards Bridging the Gap: Systematic Sim-to-Real Transfer for Diverse Legged Robots (PACE, 2509.06342)](../PACE_Systematic_Sim-to-Real_Transfer_for_Diverse_Legged_Robots/PACE_Systematic_Sim-to-Real_Transfer_for_Diverse_Legged_Robots.md)：同属"辨识替代随机化"，但用 CMA-ES 无梯度辨识，本仓库已有笔记
- [PolySim: Multi-Simulator Domain Randomization (2510.01708)](../PolySim__Bridging_the_Sim-to-Real_Gap_for_Humanoid_Control_via_Multi-Simulato/PolySim__Bridging_the_Sim-to-Real_Gap_for_Humanoid_Control_via_Multi-Simulato.md)：仿真侧随机化路线，与 HALO 思路对照，本仓库已有笔记
- [RMA: Rapid Motor Adaptation for Legged Robots (2107.04034)](../RMA_Rapid_Motor_Adaptation/RMA_Rapid_Motor_Adaptation.md)：在线动力学适应路线，本仓库已有笔记
- [ASAP: Aligning Simulation and Real-World Physics for Agile Humanoid Skills (2502.01143)](../../03_High_Impact_Selection/ASAP_Aligning_Simulation_and_Real-World_Physics_for_Agile_Humanoid_Skills/ASAP_Aligning_Simulation_and_Real-World_Physics_for_Agile_Humanoid_Skills.md)：残差动力学对齐，与 HALO 互补，本仓库已有笔记

---

> 备注：本笔记基于 arXiv 摘要、项目主页（[mwondering.github.io/halo-humanoid](https://mwondering.github.io/halo-humanoid/)）整理；网络受限期间论文全文 HTML/PDF 未完整抓取，**具体机器人平台、各任务辨识误差/跟踪精度数值、基线与消融对比**请以论文 PDF 为准。
</content>
</invoke>
