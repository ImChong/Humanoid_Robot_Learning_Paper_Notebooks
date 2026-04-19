---
layout: paper
title: "RMA: Rapid Motor Adaptation for Legged Robots"
category: "仿真到真实 Sim-to-Real"
zhname: "RMA：腿式机器人的快速运动自适应"
---

# RMA: Rapid Motor Adaptation for Legged Robots
**RMA：腿式机器人的快速运动自适应**

> 📅 阅读日期: 待读
> 🏷️ 板块: 09_Sim-to-Real 首篇骨架
> 🚧 本笔记为骨架，基本信息待人工核对。

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **arXiv** | 🚧 待核对（候选：2107.04034） |
| **PDF** | 🚧 |
| **作者** | 🚧 待核对（Ashish Kumar 等） |
| **机构** | 🚧 待核对（UC Berkeley / CMU / Facebook AI Research） |
| **发布时间** | 2021（🚧 待核对月份） |
| **会议** | RSS 2021（🚧 待核对） |
| **项目主页** | 🚧 |
| **代码** | 🚧 |

---

## 🎯 一句话总结

> 🚧 待补。推测方向（以论文为准）：训练时给策略 privileged 环境参数，部署时用 adaptation module 从最近的状态-动作历史在线**1 秒内**估出环境隐变量，让四足/腿式机器人快速适应未见地形与负载。

---

## 📌 英文缩写速查

| 缩写 | 全称 | 简单解释 |
|------|------|----------|
| **RMA** | Rapid Motor Adaptation | 本文的方法名 |
| **Privileged learning** | 特权学习 | 训练阶段给策略额外信息（地形、摩擦系数），部署时学一个去估这些信息的模块 |
| **Adaptation module** | 适应模块 | 部署时根据历史 obs/act 在线估隐变量 z 的小网络 |
| 🚧 | | |

---

## ❓ RMA 要解决什么问题？

> 🚧 待补。可能方向：
> - **Sim-to-real gap**：仿真训练的策略遇到真实地形/负载会失效。
> - **慢适应**：传统 system identification 需要离线辨识，RMA 想做到 1 秒内自适应。
> - **不依赖真机微调**：完全 sim 训练，零样本迁移。

---

## 🔧 方法详解

> 🚧 待补：读完论文后填充。
>
> 预期主线：
> 1. **Phase 1** 在仿真中用 PPO 训 base policy + privileged encoder（输入地形 / 摩擦 / 负载等真值）。
> 2. **Phase 2** 训 adaptation module：用最近 N 步 obs-action 历史回归出 phase 1 的 z。
> 3. **部署** 用 adaptation module 替换 privileged encoder，base policy 不变。

---

## 🚶 具体实例

> 🚧 待补（典型评测：A1 / Anymal 在沙地、楼梯、负载下的表现）。

---

## 🤖 工程价值

> 🚧 待补。意义：09_Sim-to-Real 分类首篇骨架；privileged learning + adaptation module 是后续诸多人形 sim-to-real 工作（如 ExBody、HumanPlus）的基础范式。

---

## 📁 源码对照

> 🚧 官方实现在 IsaacGym / legged_gym 系列代码库中有复现。

---

## 🎤 面试高频问题 & 参考回答

> 🚧

---

## 💬 讨论记录

> 🚧

---

## 📎 附录

### A. 与其他方向的关联

| 方向 | 关系 |
|------|------|
| Domain Randomization | RMA 也用 DR，但靠 adaptation module 把 DR 变量"估出来"而不是平均掉 |
| ExBody / HumanPlus | 沿用 privileged-learning + adaptation 的两阶段范式 |
| 04_Locomotion | 基础运动控制的 sim-to-real 范本 |

### B. 参考来源

- 🚧 待核对 arXiv / 主页 / 代码
- 交叉验证：[awesome-humanoid-robot-learning](https://github.com/YanjieZe/awesome-humanoid-robot-learning) Sim-to-Real section
