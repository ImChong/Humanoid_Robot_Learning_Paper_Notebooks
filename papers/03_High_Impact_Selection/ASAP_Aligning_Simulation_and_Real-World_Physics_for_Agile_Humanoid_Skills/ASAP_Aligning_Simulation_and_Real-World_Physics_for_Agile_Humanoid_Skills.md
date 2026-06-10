---
layout: paper
title: "ASAP: Aligning Simulation and Real-World Physics for Learning Agile Humanoid Whole-Body Skills"
category: "高影响力精选 High Impact Selection"
subcategory: "Sim-to-Real & Foundation Model"
zhname: "ASAP：用残差动作模型对齐仿真与真机动力学的人形敏捷全身技能"
---

# ASAP: Aligning Simulation and Real-World Physics for Learning Agile Humanoid Whole-Body Skills
**ASAP：用残差动作模型对齐仿真与真机动力学的人形敏捷全身技能**

> 📅 阅读日期: 2026-05-24
>
> 🏷️ 板块: 03_High_Impact_Selection / Sim-to-Real & Foundation Model
>
> 🧭 状态: 首版基础摘要（含 mermaid 流程图）；与 H17 ANYmal 致动器网络、域随机化等基线对照阅读更佳。

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **arXiv** | [2502.01143](https://arxiv.org/abs/2502.01143) |
| **HTML** | [arxiv.org/html/2502.01143v3](https://arxiv.org/html/2502.01143v3) |
| **PDF（arXiv）** | [arxiv.org/pdf/2502.01143](https://arxiv.org/pdf/2502.01143) |
| **PDF（项目镜像）** | [agile.human2humanoid.com/static/asap.pdf](https://agile.human2humanoid.com/static/asap.pdf) |
| **项目主页** | [agile.human2humanoid.com](https://agile.human2humanoid.com/) |
| **发布时间** | 2025-02-03 (arXiv), Robotics: Science and Systems (RSS) 2025 |
| **源码** | [LeCAR-Lab/ASAP](https://github.com/LeCAR-Lab/ASAP) |
| **会议** | Robotics: Science and Systems (RSS) 2025 |
| **作者** | Tairan He, Jiawei Gao, Wenli Xiao, Yuanhang Zhang, Zi Wang, Jiashun Wang, Zhengyi Luo, Guanqi He, Nikhil Sobanbabu, Chaoyi Pan, Zeji Yi, Guannan Qu, Kris Kitani, Jessica Hodgins, Linxi "Jim" Fan, Yuke Zhu, Changliu Liu, Guanya Shi |
| **机构** | CMU 等（LeCAR Lab 等合作单位） |
| **硬件** | Unitree G1 人形（实机部署段落）；仿真侧覆盖 IsaacGym、IsaacSim、Genesis 等组合 |

---

## 🎯 一句话总结

先用人类视频重定向后的参考动作在仿真里预训练**运动跟踪策略**，再在真机 rollout 收集状态轨迹，用**残差（delta）动作模型**显式补偿仿真与真机的动力学差；把该模型**冻结后嵌入仿真器**做「物理对齐」式的策略微调，最后在真机**去掉 delta 模型**直接部署——在侧跳、前跳、踢球、球星庆祝动作等全身敏捷技能上显著降低跟踪误差，并优于纯 SysID、纯域随机化、以及仅学习 delta 动力学但不回灌仿真的基线。

---

## 📌 英文缩写速查

| 缩写 | 含义 |
|------|------|
| **ASAP** | Aligning Simulation and Real Physics |
| **SysID** | System Identification，系统辨识 |
| **DR** | Domain Randomization，域随机化 |
| **delta / residual** | 在名义仿真动作上叠加的残差控制量，用于对齐真机接触与执行器效应 |

---

## ❓ 论文要解决什么问题？

人形做高动态全身动作时，**仿真里能跟踪的参考动作**往往在真机上因接触、摩擦、柔性、执行器延迟等**动力学失配**而崩掉。传统路子要么：

1. **SysID / 手工调参**：劳动密集，且难以覆盖所有敏捷工况；  
2. **强域随机化**：容易训出**过于保守**的策略，牺牲爆发力与协调性；  
3. **只学 delta 动力学但不在闭环里对齐训练**：补偿难以与原有策略稳定耦合。

ASAP 的核心诉求是：**用可学习、可回灌仿真的残差通道，把「真机 rollout 暴露的误差结构」压缩进训练闭环**，从而在**不牺牲敏捷性**的前提下完成 sim-to-real。

---

## 📌 流程概览（mermaid）

<div class="mermaid">
flowchart TD
  subgraph stage1["阶段一：仿真预训练"]
    M["人类动作重定向 → 参考轨迹库"]
    P0["在 IsaacGym 等环境中预训练运动跟踪策略 π₀"]
    M --> P0
  end
  subgraph stage2["阶段二：真机数据与 delta 模型"]
    R["真机部署 π₀ 采集 rollout（状态/动作轨迹）"]
    D["训练 delta 动作模型：对齐 s_sim 与 s_real 的差异"]
    P0 --> R
    R --> D
  end
  subgraph stage3["阶段三：对齐式微调"]
    I["将冻结的 delta 模型嵌入仿真器（对齐管线）"]
    F["在「对齐后」仿真中微调 π → π*"]
    D --> I
    I --> F
  end
  subgraph stage4["阶段四：实机部署"]
    X["去掉 delta，仅部署 π*"]
    F --> X
  end
  stage1 --> stage2 --> stage3 --> stage4
</div>

---

## 🔧 方法详解

### 1. 运动跟踪预训练与真机轨迹采集

- 从人类视频中重定向得到人形参考动作，在仿真中训练多条**运动跟踪（motion tracking）**策略，使其在理想动力学下尽可能贴合参考。  
- 将这些策略直接部署到真机（如 Unitree G1），得到**带失配噪声**的真实状态—动作序列，为后续 delta 学习提供监督信号。

### 2. 基于真机数据的 delta 动作模型

- 学习一个 **delta（残差）动作模型**：在每一步上，根据当前策略输出与真实响应，预测应叠加的控制修正，使**仿真状态轨迹逼近真机状态**（论文在摘要与方法中强调最小化仿真状态 \(s_t\) 与真机状态 \(s^r_t\) 的偏差）。  
- 直观理解：delta 模型把「仿真里缺的摩擦/接触/延迟」用数据驱动方式**显式参数化**，而不是仅靠随机化去碰运气。

### 3. 将 delta 嵌入仿真并做策略微调

- **冻结** delta 模型，把它接到仿真闭环里，使训练时策略所见的下一状态分布**更接近真机 rollout 的动力学流形**。  
- 在该「对齐后的仿真」中对预训练策略做**二次微调**，让策略学会在「已补偿」的动力学下仍完成敏捷跟踪。

### 4. 真机部署（无 delta）

- 微调完成后，**真机侧不再运行 delta 模型**，直接部署微调后的策略。  
- 论文动机是：delta 主要承担**训练期对齐**角色，把可迁移的鲁棒性「蒸馏」进最终策略；部署链路保持简洁。

### 5. 跨仿真器与跨实机的验证设定

- 论文在三种迁移场景报告结果：**IsaacGym → IsaacSim**、**IsaacGym → Genesis**、以及 **IsaacGym → 真实 G1**。  
- 用于说明 ASAP 不仅修复「仿真 vs 真机」，也能缓解**不同仿真器之间**的物理参数与接触实现差异（对 toolchain 迁移有工程参考价值）。

---

## 🧪 实验与现象（定性）

- 展示类技能包括：**侧跳（约 1.3 m）**、**前跳（0.85 m / 1.5 m）**、踢球、球星风格庆祝动作、APT 舞蹈、深蹲与躯干前倾组合等，强调**全身协调与爆发力**。  
- 项目页提供 **Before / After ASAP fine-tuning** 视频对比，可直观看到跟踪误差与动作「发僵」程度的改善。  
- 与 SysID、DR、以及「仅 delta 动力学学习但不用于闭环对齐」等基线相比，论文主张 ASAP 在**敏捷性—鲁棒性**折中上更优；具体数值与消融以论文图表为准。

---

## 🔗 与仓库内其它笔记的关系

- **H17 Learning Agile and Dynamic Motor Skills for Legged Robots（ANYmal）**：经典「致动器网络 + 快速仿真」路线，侧重**执行器黑盒化**；ASAP 侧重**跨仿真/真机的残差对齐与二阶段微调**，二者可对照理解 sim-to-real 工具箱。  
- **H13 Humanoid Locomotion as Next Token Prediction**：自回归轨迹范式；ASAP 仍是**强化学习 + 物理仿真**主线的 sim-to-real 工程补强。

---

## 📚 延伸阅读

- OpenReview / 引用格式见项目页 BibTeX（`arXiv:2502.01143`）。  
- 若需复现管线，优先阅读 [LeCAR-Lab/ASAP](https://github.com/LeCAR-Lab/ASAP) 的 README 与训练脚本入口，并对照论文附录中的环境与超参表。

---

## 🔁 修订记录

| 日期 | 说明 |
|------|------|
| 2026-05-24 | 首版：摘要、方法四阶段、mermaid、PDF/HTML/代码链接 |
