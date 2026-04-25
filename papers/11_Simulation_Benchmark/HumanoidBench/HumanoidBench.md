---
layout: paper
paper_order: 1
title: "HumanoidBench: Simulated Humanoid Benchmark for Whole-Body Locomotion and Manipulation"
category: "仿真环境"
zhname: "HumanoidBench：全身运动与操作的人形机器人仿真基准"
---

# HumanoidBench: Simulated Humanoid Benchmark for Whole-Body Locomotion and Manipulation
**HumanoidBench：全身运动与操作的人形机器人仿真基准**

> 📅 阅读日期: 2026-04-21
> 🏷️ 板块: 10 Simulation Benchmark · 分类起步样例
> 🚧 本笔记已填充基本信息，深度技术细节待细化。

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **arXiv** | [2403.10506](https://arxiv.org/abs/2403.10506) (RSS 2024) |
| **PDF** | [Download](https://arxiv.org/pdf/2403.10506.pdf) |
| **作者** | Carlos Ferrazza 等 |
| **机构** | UCL / CMU / Oxford / Berkeley 等 |
| **发布时间** | 2024-03 |
| **项目主页** | [humanoid-bench.github.io](https://humanoid-bench.github.io) |
| **代码** | [GitHub - carlosferrazza/humanoid-bench](https://github.com/carlosferrazza/humanoid-bench) |

---

## 🎯 一句话总结

> HumanoidBench 是一个基于 MuJoCo 的大规模人形机器人学习基准，包含 27 个涉及全身操作和运动的任务，旨在解决高维动作空间下的协调与长时序规划问题。

---

## 📌 英文缩写速查

| 缩写 | 全称 | 简单解释 |
|------|------|----------|
| H1 | Unitree H1 | 本基准主要采用的国产全尺寸人形机器人模型 |
| Shadow Hand | Shadow Dexterous Hand | 一种高度仿人的灵巧手模型（24 自由度） |
| HRL | Hierarchical Reinforcement Learning | 分层强化学习，本基准证明其在复杂任务中的必要性 |

---

## ❓ 论文要解决什么问题？

- **缺乏统一基准**：人形机器人领域缺乏一个涵盖面广、任务复杂度高且可重复的仿真测试集。
- **高维控制挑战**：现代人形机器人（如 H1 + Shadow Hand）拥有超过 60 个执行器，传统的"扁平"强化学习算法难以在高维空间中有效协调全身。
- **操作与运动的结合**：如何在一个基准中同时评估机器人的移动能力（Locomotion）和精细操作能力（Manipulation）？

---

## 🔧 方法详解

1. **丰富的任务库 (Task Suite)**：
   - **15 个全身操作任务**：如货架整理、窗户擦拭、甚至篮球投篮。
   - **12 个运动任务**：如迷宫导航、障碍跳跃、上下楼梯。
2. **硬件配置**：
   - 默认使用 **Unitree H1** 搭载两只 **Shadow Hand**（共 61 个执行器）。
   - 同时也支持 Digit、G1 等其他主流机器人模型。
3. **算法评测**：
   - 对比了 PPO、SAC、TD-MPC2、DreamerV3 等主流算法。
   - 结果发现：纯端到端算法在长时序任务上表现极差。
4. **分层强化学习优势**：
   - 论文提出了一种基于预训练技能（Pre-trained skills）的分层方案，证明了将复杂任务分解为"底层技能 + 高层调度"是解决高维人形控制的关键。

---

## 🚶 具体实例

- **包裹卸载任务**：机器人需要走到货车旁，识别包裹，用灵巧手将其抓起并搬运到指定地点。这要求极其精准的全身协调（足部稳定 + 手臂伸展 + 灵巧手抓取）。
- **篮球投篮**：展示了机器人在动态平衡中完成爆发性、精确动作的能力。

---

## 🤖 工程价值

- **研究加速器**：为全球开发者提供了一个快速、安全且无需昂贵硬件即可进行人形算法迭代的平台。
- **技能库建设**：开源了大量预训练的底层技能权重，方便后续研究直接进行高层算法开发。
- **算法分水岭**：揭示了现有 RL 算法在处理 60+ 自由度机器人时的局限性，指明了分层学习的研究方向。

---

## 🎤 面试高频问题 & 参考回答

1. **HumanoidBench 与传统的 Gym 环境有什么区别？**
   - 任务维度更高（61 DOF vs 10-20 DOF），且包含长时序、跨类别的复合任务（运动 + 操作）。
2. **为什么 hierarchical RL 在这里表现更好？**
   - 扁平 RL 在高维动作空间中探索效率极低；分层架构通过复用已经学会的稳定动作（如走路、抓取），极大地缩小了高层策略的搜索空间。

---

## 📎 附录

### A. 参考来源
- [arXiv:2403.10506](https://arxiv.org/abs/2403.10506)
- [Project Website](https://humanoid-bench.github.io)
