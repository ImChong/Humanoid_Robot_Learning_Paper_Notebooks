---
layout: paper
paper_order: 1
title: "Learning to Walk in Minutes Using Massively Parallel Deep Reinforcement Learning"
category: "行走运动"
zhname: "几分钟学会走路：大规模并行深度强化学习"
---

# Learning to Walk in Minutes Using Massively Parallel Deep Reinforcement Learning
**几分钟学会走路：大规模并行深度强化学习**

> 📅 阅读日期: 待读
> 🏷️ 板块: 04 Locomotion · 分类起步样例
> 🚧 本笔记为骨架，待逐节补完。作为 `04_Locomotion` 分类的首篇样例。

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **arXiv** | 🚧 待核对（Rudin et al., CoRL 2021） |
| **PDF** | 🚧 |
| **作者** | Nikita Rudin 等 |
| **机构** | ETH Zurich / RSL |
| **发布时间** | 2021 |
| **项目主页** | 🚧 |
| **代码** | [legged_gym](https://github.com/leggedrobotics/legged_gym)（🚧 待核对） |

---

## 🎯 一句话总结

> 🚧 用 Isaac Gym 的大规模 GPU 并行仿真（数千环境同时），把四足 / 人形走路训练从小时级压到分钟级，成为 legged RL 社区的事实基线。

---

## 📌 英文缩写速查

| 缩写 | 全称 | 简单解释 |
|------|------|----------|
| 🚧 | | |

---

## ❓ 论文要解决什么问题？

> 🚧 待补。关键切入点：
> - 传统 CPU 仿真（MuJoCo / PyBullet）并行度受限，训练 legged 策略需要数小时甚至数天
> - Isaac Gym 提供 GPU 并行物理仿真，能否把训练时长缩短一个数量级？
> - 如何设计奖励 / 课程 / DR 来匹配大规模采样？

---

## 🔧 方法详解

> 🚧 待补。建议展开：
> 1. Isaac Gym 环境设置（4096 + 并行）
> 2. 奖励设计（base velocity, orientation, joint limits, action rate, energy）
> 3. Domain randomization 配置
> 4. 课程学习 / terrain randomization

---

## 🚶 具体实例

> 🚧 待补。

---

## 🤖 工程价值

> 🚧 待补。这篇是后续所有 legged RL 工作（ExBody、HIMLoco、OmniH2O 等）的训练基础设施起点。

---

## 🎤 面试高频问题 & 参考回答

> 🚧

---

## 💬 讨论记录

> 🚧

---

## 📎 附录

### A. 参考来源
- 🚧 原论文 / 代码 / 教程
