---
layout: paper
paper_order: 1
title: "Understanding Domain Randomization for Sim-to-real Transfer"
category: "仿真到现实"
---

# Understanding Domain Randomization for Sim-to-real Transfer
**理解域随机化在仿真到现实迁移中的作用**

> 📅 阅读日期: 待读  
> 🏷️ 板块: Sim-to-Real / Theory

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **arXiv** | [2110.03239](https://arxiv.org/abs/2110.03239) |
| **PDF** | [下载](https://arxiv.org/pdf/2110.03239) |
| **作者** | Xiaoyu Chen 等 |
| **机构** | Princeton（主要）|
| **发布时间** | 2021年10月（v1）, 2022年3月（v2） |
| **类型** | 理论分析 / 综述 |

---

## 🎯 一句话总结

Domain Randomization（DR）是 sim-to-real 领域最常用的方法之一，但这篇论文提供了**理论框架**来解释为什么 DR 能在不需要任何现实数据的情况下成功迁移，并证明了**使用记忆（历史依赖策略）对 DR 的成功至关重要**。

---

## 📌 英文缩写速查

| 缩写 | 全称 | 简单解释 |
|------|------|----------|
| **DR** | Domain Randomization | 域随机化 |
| **sim-to-real** | Simulation to Real World | 仿真到现实迁移 |
| **MDP** | Markov Decision Process | 马尔可夫决策过程 |
| **RL** | Reinforcement Learning | 强化学习 |

---

## ❓ 这篇论文要解决什么问题？

DR 在实践里效果很好（机器人操纵、足式 locomotion 等），但**没有理论解释**——为什么简单的随机化仿真参数就能迁移到现实？需要多少随机化样本？什么时候会失败？

---

## 🔑 核心理论框架

### 仿真器建模为 MDP 集合

真实世界的物理参数（摩擦力、质量、延迟等）是**未知的**，DR 把仿真器建模为一组带有**可调参数**的 MDP 集合：

$$\mathcal{M} = \{ M_\theta : \theta \in \Theta \}$$

每个 $\theta$ 代表一套物理参数配置。

### Sim-to-Real Gap 的界限

论文给出了 DR 返回的策略价值与真实世界最优策略价值之间的**理论上界**：

$$\text{gap} \leq f(\text{随机化分布}, \text{样本复杂度})$$

关键发现：在** mild conditions** 下，这个 gap 可以足够小——意味着 DR 可以**无需任何现实样本**实现成功迁移。

### Memory (历史依赖策略) 的重要性

论文理论分析的一个核心结论：**DR 需要使用历史依赖策略（memory-based policy）**，而非只依赖当前状态的 Markov 策略。

直觉：只有利用历史信息，策略才能隐式地识别当前所在的 domain，从而在仿真随机化中学到跨不同物理参数都有效的能力。

---

## ✅ 主要贡献

1. 提出第一个 DR 的**严格理论框架**
2. 证明 DR 成功的**充分条件**（mild conditions）
3. 从理论角度揭示 **memory-based policy** 的必要性
4. 将 sim-to-real gap _bound 转化为无限时域 MDP 的学习复杂度问题（新理论工具）

---

## 💡 个人理解

这篇论文的价值在于把 DR 从"玄学调参"拉到了"有据可依"的层面。

之前大家用 DR 都是"试试这个范围、不行再调"，现在有了理论指导：随机化分布怎么选、需要多少样本、为什么 history 重要。

对于人形机器人学习来说，理解 DR 的理论边界能帮助我们更聪明地设计随机化策略——不是盲目随机，而是**有目标地覆盖真实世界的不确定性空间**。

---

## 📚 相关参考

- Domain Randomization 原始应用（RoboLearn, OpenAI 等）
- 后续工作：ADR (Automatic Domain Randomization)

---

## 🏷️ 标签

`#Sim-to-Real` `#Theory` `#DomainRandomization` `#PolicyGradient`
