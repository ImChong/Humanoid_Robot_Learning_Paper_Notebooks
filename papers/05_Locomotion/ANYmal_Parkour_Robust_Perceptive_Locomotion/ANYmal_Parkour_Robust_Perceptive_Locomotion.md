---
layout: paper
paper_order: 3
title: "ANYmal Parkour: Learning Agile Navigation for Quadrupedal Robots"
category: "行走运动"
zhname: "ANYmal 跑酷：足式机器人的敏捷导航学习"
---

# ANYmal Parkour: Learning Agile Navigation for Quadrupedal Robots
**ANYmal 跑酷：足式机器人的敏捷导航学习**

> 📅 阅读日期: 2026-04-21
> 🏷️ 板块: 04 Locomotion · 敏捷导航
> 🚧 本笔记已填充基本信息，深度技术细节待细化。

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **arXiv** | [2306.14874](https://arxiv.org/abs/2306.14874) (Science Robotics) |
| **PDF** | [Download](https://arxiv.org/pdf/2306.14874.pdf) |
| **作者** | David Hoeller, Nikita Rudin, Christopher Sako, Marco Hutter |
| **机构** | ETH Zurich / NVIDIA |
| **发布时间** | 2023-06 |
| **项目主页** | [ETH RSL ANYmal Parkour Website](https://rsl.ethz.ch/research/anymal-parkour.html) |
| **代码** | 🚧 宇树 Go1 版有部分复现，官方代码部分开源 |

---

## 🎯 一句话总结

> 宇树（ETH Zurich）团队通过分层分层的强化学习，让 ANYmal 机器人不仅掌握了攀爬、跳跃、钻洞等多种单一跑酷技能，还能根据地形环境感知自主选择最优的技能路径。

---

## 📌 英文缩写速查

| 缩写 | 全称 | 简单解释 |
|------|------|----------|
| HRL | Hierarchical Reinforcement Learning | 分层强化学习 |
| MLP | Multi-Layer Perceptron | 多层感知机 |
| Perceptive Locomotion | 感知感知运动 | 利用视觉/深度信息引导的机器人行走 |

---

## ❓ 论文要解决什么问题？

- **技能组合难题**：机器人已经学过走路、跳跃，但在面对连续障碍（如先钻洞再上台阶）时，如何实现技能间的平滑过渡？
- **环境感知的局限**：如何让机器人在复杂的工业或灾难现场中，识别哪些地形是可以过的，哪些需要特定动作（如侧身）？
- **鲁棒性挑战**：在高动态动作中保持板载传感器数据的准确性并进行实时决策。

---

## 🔧 方法详解（技术路径）

1. **分层分层控制架构 (Hierarchical Architecture)**：
   - **高层策略 (High-level Navigator)**：负责感知周围地形（Depth map），并根据目标点规划出一条路径。它会输出给低层一个"期望技能"的信号。
   - **低层技能库 (Low-level Skills)**：由一系列专门训练的专家策略组成（例如：爬台阶专家、深沟跳跃专家、狭窄空间钻爬专家）。
2. **技能感知导航 (Skill-Aware Navigation)**：
   - 高层导航策略在训练过程中被告知了每个底层专家技能的物理极限（比如能跳多远、能爬多高）。
   - 这使得机器人不会规划出物理上无法实现的路径，而是会主动选择它"能力范围内"的最佳越障方式。
3. **Isaac Gym 大规模预训练**：
   - 利用 GPU 并行仿真技术，模拟了极其复杂的各种跑酷迷宫关卡，极大地提升了泛化能力。

---

## 🚶 具体实例

- **迷宫越障**：机器人面对一个狭窄缝隙，高层策略识别到高度限制，自动切换到"低伏前行"模式，钻过去后再迅速站起恢复正常行走。
- **动态规划**：在有多个路径可选时，它能根据当前剩余能量和安全性，选择跳过浅坑而不是绕远路。

---

## 🤖 工程价值

- **工业应用前景**：这种敏捷性是人形或四足机器人进入建筑工地、矿井等复杂环境进行巡检的基础。
- **分层范式的标杆**：相比于纯端到端，ANYmal Parkour 证明了模块化分层设计在处理多任务、长程规划时的优越性。
- **软硬件深度结合**：展示了 ETH Zurich 在 ANYmal 硬件潜力挖掘上的深厚功底。

---

## 🎤 面试高频问题 & 参考回答

1. **ANYmal Parkour 与 CMU 的 Extreme Parkour 有何主要区别？**
   - ANYmal 侧重于**分层分层**（Navigation + Specialist Skills），擅长长程规划和技能切换；Extreme Parkour 侧重于**端到端**视觉控制，追求极限爆发力和最小延迟。
2. **分层架构的缺点是什么？**
   - 依赖于技能库的完整性；如果遇到一个库中没有定义的障碍类型，机器人可能会卡住。

---

## 📎 附录

### A. 参考来源
- [Science Robotics 2023 Paper](https://www.science.org/doi/10.1126/scirobotics.adh5409)
- [ETH RSL Lab](https://rsl.ethz.ch/)
