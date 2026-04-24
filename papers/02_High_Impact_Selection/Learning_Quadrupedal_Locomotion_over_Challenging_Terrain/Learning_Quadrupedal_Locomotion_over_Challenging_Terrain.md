---
layout: paper
title: "Learning Quadrupedal Locomotion over Challenging Terrain"
category: "高影响力精选 High Impact Selection"
subcategory: "Locomotion Classics"
zhname: "挑战地形下的四足运动学习（ANYmal 里程碑）"
---

# Learning Quadrupedal Locomotion over Challenging Terrain
**挑战地形下的四足运动学习（ANYmal 里程碑）**

> 📅 阅读日期: 2026-04-24
> 🏷️ 板块: 02_High_Impact_Selection / Locomotion Classics
> 🧭 状态: 快速扩充版，已替换原骨架；后续可继续补实验图表和 reward 细节。

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **论文** | Science Robotics 5(47): eabc5986 |
| **DOI** | [10.1126/scirobotics.abc5986](https://doi.org/10.1126/scirobotics.abc5986) |
| **项目页** | [Vladlen Koltun publication page](https://vladlen.info/publications/learning-quadrupedal-locomotion-challenging-terrain/) |
| **作者** | Joonho Lee, Jemin Hwangbo, Lorenz Wellhausen, Vladlen Koltun, Marco Hutter |
| **机构** | ETH Zurich / KAIST / Intel |
| **发布时间** | 2020-10-21 |
| **关键词** | Quadrupedal locomotion, proprioception, reinforcement learning, sim-to-real, challenging terrain |

---

## 🎯 一句话总结

这篇 Science Robotics 论文证明了一个重要事实：只依赖本体感知、在相对简单的仿真域中训练的 RL 控制器，也可以零样本迁移到泥地、雪地、碎石、植被和流水等真实复杂地形上的 ANYmal 四足机器人。

---

## 📌 英文缩写速查

| 缩写 | 全称 | 简单解释 |
|------|------|----------|
| **RL** | Reinforcement Learning | 用奖励函数训练控制策略 |
| **PPO** | Proximal Policy Optimization | 常用 on-policy 强化学习算法 |
| **TCN** | Temporal Convolutional Network | 从历史本体感知中估计隐含地形/状态 |
| **Privileged information** | 特权信息 | 训练时可用、部署时不可用的仿真真值 |
| **Proprioception** | 本体感知 | IMU、关节角、关节速度等内部传感 |
| **Zero-shot** | 零样本迁移 | 不在真实目标地形上再训练，直接部署 |

---

## ❓ 这篇论文为什么是 Classic？

在这篇论文之前，四足机器人越野通常依赖精心设计的状态机、步态规划、地形感知和人工调参。本文的影响力在于，它把"复杂自然地形"这个问题推进到学习控制范式中，而且结果足够直观：ANYmal 能在从未训练过的泥地、雪地、碎石、灌木和流水中保持鲁棒运动。

它对后续工作的影响主要有三点：

1. **本体感知路线成立**：不依赖相机或 LiDAR，机器人也能通过身体反馈适应地形。
2. **特权训练范式成熟**：训练时让策略接触仿真真值，部署时只保留可观测输入。
3. **sim-to-real 信心增强**：只要随机化和训练任务设计合理，仿真策略能跨越很大真实域差异。

---

## 🔧 方法详解

### 1. 问题设定

目标是在没有外部地形传感器的情况下，让 ANYmal 在复杂自然地形上稳定前进。控制器输入主要来自本体感知，例如 IMU、关节状态、历史动作和期望速度命令。输出是底层关节控制目标。

这个设定刻意不使用视觉地形图。优点是系统简单、延迟低、鲁棒；缺点是机器人必须通过接触后的反馈来适应地形，无法提前规划远处障碍。

### 2. 仿真训练

策略在仿真中通过强化学习训练。环境包含不同高度场、摩擦、坡度、接触条件和扰动。训练目标不是记住某个地形，而是在大量变化中学到稳定的身体反馈控制。

典型 reward 会包含：

- 跟踪目标速度；
- 保持身体姿态稳定；
- 限制能耗和关节动作抖动；
- 避免跌倒；
- 鼓励合适的足端接触模式。

### 3. 本体感知历史编码

由于部署时没有显式地形真值，策略需要从过去一段时间的本体感知中推断当前接触环境。例如，脚突然下陷、身体俯仰变化、关节负载变化，都能暗示地面软硬或高度变化。论文使用历史编码思想，让策略从时间序列中提取隐含环境信息。

这条思路后来在 RMA 等工作中进一步系统化：学生网络用历史观测估计 latent adaptation vector，再交给控制策略。

### 4. 随机化与真实部署

成功迁移的关键不是把仿真做得完全真实，而是覆盖足够宽的随机域。本文强调控制器在训练中没有见过真实的泥地、雪地、植被和流水，但这些场景仍落在策略学到的反馈调节能力范围内。

### 5. 为什么不依赖视觉？

视觉可以提前感知障碍，但会引入感知失败、标定误差、延迟和数据分布问题。本文展示的是另一种极简路线：只用身体反馈也能实现很强的鲁棒性。后续 ANYmal Parkour、Extreme Parkour 等工作再把视觉和更复杂动作接回来。

---

## 🚶 具体实例

论文和项目页展示的典型真实环境包括：

- 泥地：接触软、足端可能下陷；
- 雪地：摩擦和支撑都不稳定；
- 碎石/瓦砾：足端接触点动态变化；
- 厚植被：脚部运动被阻挡，接触模型与训练差异很大；
- 流水/湿滑表面：摩擦和扰动不可控。

这些场景共同考验的是策略能否在无法提前知道地形的情况下，通过反馈快速恢复。

---

## 🤖 工程价值

1. **越野不是必须先上视觉**：本体感知策略可以作为稳定基础层。
2. **训练域设计比模型精度更重要**：仿真不必完全真实，但随机化必须覆盖部署误差。
3. **历史观测是隐式状态估计器**：很多后续 legged robot 工作都沿用"从历史估计环境 latent"的思想。
4. **适合作为人形学习先修论文**：人形 WBC 中的 teacher-student、domain randomization、sim-to-real 都能在这篇看到早期成熟形态。

---

## 📁 源码对照

该论文年代早于现在常见的 legged_gym / rsl_rl 生态，但读代码时可以按下面映射理解：

- terrain curriculum 对应地形随机化；
- observation history 对应历史编码或 adaptation module；
- reward tracking 对应速度、姿态、能耗、平滑性；
- deployment wrapper 对应真实机器人低层接口和传感滤波。

如果用 Isaac Lab 或 legged_gym 复现，优先实现 blind proprioceptive locomotion，再逐步加入地形感知。

---

## 🎤 面试高频问题 & 参考回答

**Q1: 这篇为什么不用视觉也能走复杂地形？**

A: 因为它依赖本体感知闭环适应，而不是提前规划。地形变化会通过身体姿态、关节状态和接触反馈反映出来，策略从历史观测中学习如何调节动作。

**Q2: 它和 RMA 的关系是什么？**

A: 两者都利用训练时特权信息和部署时有限观测的思想。RMA 后来把 adaptation module 和 latent 表达做得更显式，成为更清晰的框架。

**Q3: 这篇对人形机器人有什么启发？**

A: 人形机器人同样需要在有限传感输入下适应接触和模型误差。本文证明的不是四足专属技巧，而是 sim-to-real 训练范式和本体感知反馈控制的价值。

---

## 💬 讨论记录

- 这篇适合和 RMA、ANYmal Parkour、Extreme Parkour 连读：从 blind locomotion 到 adaptation，再到视觉和动态动作。
- 对人形研究者来说，重点不是照搬四足结构，而是理解"训练域、历史观测、部署观测约束"之间的关系。

---

## 📎 附录

### A. 与其他方向的关联

| 方向 | 关系 |
|------|------|
| RMA | 后续把隐式适应做成更明确的模块 |
| ANYmal Parkour | 在鲁棒 locomotion 基础上加入感知和跑酷动作 |
| Extreme Parkour | 进一步扩展到跳跃、攀爬等高动态技能 |
| Humanoid locomotion | teacher-student 和 sim-to-real 范式被迁移到人形 |

### B. 参考来源

- DOI: <https://doi.org/10.1126/scirobotics.abc5986>
- Project/publication page: <https://vladlen.info/publications/learning-quadrupedal-locomotion-challenging-terrain/>
- KAIST publication page: <https://pure.kaist.ac.kr/en/publications/learning-quadrupedal-locomotion-over-challenging-terrain>
