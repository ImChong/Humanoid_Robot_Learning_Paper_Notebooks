---
layout: paper
title: "Character Controllers Using Motion VAEs"
category: "基于物理的角色动画 Physics-Based Animation"
zhname: "用 Motion VAE 做角色控制器"
---

# Character Controllers Using Motion VAEs
**用 Motion VAE 做角色控制器**

> 📅 阅读日期: 待读
> 🏷️ 板块: 12_Physics-Based_Animation 首篇骨架
> 🚧 本笔记为骨架，基本信息待人工核对。

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **arXiv** | 🚧 待核对（候选：2103.14274） |
| **PDF** | 🚧 |
| **作者** | 🚧 待核对（Hung Yu Ling, Fabio Zinno, George Cheng, Michiel van de Panne 等） |
| **机构** | 🚧 待核对（UBC / EA SEED） |
| **发布时间** | 2020（🚧 待核对：SIGGRAPH 2020） |
| **会议** | SIGGRAPH 2020 |
| **项目主页** | 🚧 |
| **代码** | 🚧 |

---

## 🎯 一句话总结

> 🚧 待补。推测方向（以论文为准）：用条件 VAE 把高维角色动作的**下一帧分布**学下来，用低维 latent 当"动作字典"，再训一个上层策略采样这些 latent 实现可控制的角色动画。

---

## 📌 英文缩写速查

| 缩写 | 全称 | 简单解释 |
|------|------|----------|
| **VAE** | Variational Autoencoder | 变分自编码器，能从数据学到一个连续 latent 空间并采样 |
| **MVAE** | Motion VAE | 本文方法名 |
| **Autoregressive** | 自回归 | 下一帧条件于前几帧，逐帧滚动生成 |
| 🚧 | | |

---

## ❓ MVAE 要解决什么问题？

> 🚧 待补。可能方向：
> - **kinematic 动画的可控性**：传统 motion graph / motion matching 难以扩展。
> - **动作分布建模**：如何用一个紧凑模型表达一个角色"所有合理的下一帧"。
> - **上层任务策略**：得到 latent 之后，目标驱动的高层策略只在 latent 空间训练就够了。

---

## 🔧 方法详解

> 🚧 待补：读完论文后填充。
>
> 预期主线：
> 1. **下层** Conditional VAE：encoder(过去 K 帧, 下一帧) → latent z；decoder(过去 K 帧, z) → 下一帧。
> 2. **训练** kinematic motion 数据集（如 LaFAN1 / Locomotion Mocap）的下一帧重建 + KL。
> 3. **上层** 一个 RL 策略 / 控制器在 z 空间 sample，用奖励驱动达到目标（朝向、位置）。

---

## 🚶 具体实例

> 🚧 待补（典型任务：行走方向跟踪、跳跃到目标点、避障）。

---

## 🤖 工程价值

> 🚧 待补。意义：12_Physics-Based_Animation 分类首篇骨架；MVAE 是 latent skill 范式（后续 ASE / CALM / PULSE）在 kinematic 动画上的早期代表，理解它有助于看清 ASE 的物理化路径。

---

## 📁 源码对照

> 🚧 官方 PyTorch 实现待核对链接。

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
| ASE / CALM / PULSE | latent skill 思路同源，差异在物理仿真 vs kinematic |
| Diffusion Policy | 同样是把动作分布学下来再采样，但用 diffusion 替代 VAE |
| 13_Human_Motion | 上游 mocap 数据来源相同 |

### B. 参考来源

- 🚧 待核对 arXiv / 主页 / 代码
- 交叉验证：[awesome-humanoid-robot-learning](https://github.com/YanjieZe/awesome-humanoid-robot-learning) Physics-Based Animation section
