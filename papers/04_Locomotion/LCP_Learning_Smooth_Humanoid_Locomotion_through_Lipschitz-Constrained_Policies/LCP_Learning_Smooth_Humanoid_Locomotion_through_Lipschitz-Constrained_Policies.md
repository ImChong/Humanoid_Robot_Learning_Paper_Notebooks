---
layout: paper
paper_order: 1
title: "Learning Smooth Humanoid Locomotion through Lipschitz-Constrained Policies (LCP)"
category: "行走运动"
---

# Learning Smooth Humanoid Locomotion through Lipschitz-Constrained Policies (LCP)
**通过 Lipschitz 约束策略学习平滑人形机器人运动**

> 📅 阅读日期: 待读  
> 🏷️ 板块: Locomotion / Smooth Policy

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **arXiv** | [2410.11825](https://arxiv.org/abs/2410.11825) |
| **PDF** | [下载](https://arxiv.org/abs/2410.11825) |
| **作者** | Zixuan Chen*, Xialin He*, Yen-Jen Wang*, Qiayuan Liao, Yanjie Ze, Zhongyu Li, S. Shankar Sastry, Jiajun Wu, Koushil Sreenath, Saurabh Gupta, Xue Bin Peng |
| **机构** | SFU, UIUC, UC Berkeley, Stanford, NVIDIA |
| **会议** | IROS 2025 |
| **代码** | [MimicKit](https://github.com/xbpeng/MimicKit) / [GitHub](https://github.com/zixuan417/smooth-humanoid-locomotion) |

---

## 🎯 一句话总结

LCP 通过对策略网络施加 **Lipschitz 约束**（以梯度罚项形式），替代了传统的手动调参平滑技术（低通滤波器、平滑奖励），让人形机器人能够自动学到平滑、鲁棒的运动控制器。

---

## 📌 英文缩写速查

| 缩写 | 全称 | 简单解释 |
|------|------|----------|
| **LCP** | Lipschitz-Constrained Policies | Lipschitz 约束策略 |
| **RL** | Reinforcement Learning | 强化学习 |
| **sim-to-real** | Simulation to Real World | 仿真到现实迁移 |
| **Lipschitz** | — | 连续性度量：函数输出变化有上界 |

---

## ❓ 这篇论文要解决什么问题？

人形机器人要真正部署到现实世界，运动控制器必须产生**平滑的动作输出**——不能有抖动的关节指令，否则会损坏硬件或失去平衡。

传统做法：
- **低通滤波器**：对输出的动作信号做滤波，硬件层面平滑
- **平滑奖励**：在奖励函数里加平滑项，需要大量手动调参

这些方法**不可微**，需要针对每个机器人平台单独调参，迁移成本高。

**LCP 的核心思想**：把"平滑"编码进策略网络的结构约束里，用一个**可微的 Lipschitz 约束**替代不可微的平滑技术。

---

## 🔑 核心方法

### Lipschitz 约束

一个函数 $f$ 是 Lipschitz 连续的，当：

$$\| f(x_1) - f(x_2) \| \leq L \| x_1 - x_2 \|$$

其中 $L$ 是 Lipschitz 常数。直观理解：**输入的小变化 → 输出的变化也有上界**，这直接保证了输出的平滑性。

### 梯度罚项实现

LCP 将 Lipschitz 约束转化为一个**可微的梯度罚项**加入策略损失：

$$L_{\text{LCP}} = \mathbb{E} \left[ \max(0, \| \nabla_\theta \pi_\theta(a|s) \| - L)^2 \right]$$

这可以直接融入标准 PPO/强化学习框架，**无需手动调参**，自动学习到平滑策略。

---

## ✅ 主要贡献

1. 提出 **LCP**：一个通用、可微的平滑策略方法
2. 证明 Lipschitz 约束可以无缝替代低通滤波器和手动平滑奖励
3. 在**多种人形机器人平台**上验证（物理形态差异大）
4. sim-to-real 零样本迁移效果鲁棒

---

## 🔬 实验洞察

- LCP 在训练阶段自动产生平滑行为，无需后期滤波
- 适用于不同构型的人形机器人（从低维度到高维度）
- 相比传统低通滤波，LCP 在真实硬件上表现出更好的**高频扰动鲁棒性**

---

## 💡 个人理解

这篇工作的价值在于：**把一个工程调参问题，变成了一个可学习的结构约束问题**。

之前做平滑要手动调滤波器参数或反复设计平滑奖励，现在直接约束网络的 Lipschitz 常数，框架自动学出平滑动作。

属于那种"简单但深刻"的想法——问题还是老问题，但解法从"手动工程"变成了"端到端学习"。

---

## 📚 相关参考

- 低通滤波 vs LCP 的对比分析
- MimicKit 套件中已集成 LCP
- PPO 作为基础 RL 算法

---

## 🏷️ 标签

`#Locomotion` `#SmoothPolicy` `#Sim-to-Real` `#Humanoid` `#LipschitzConstraint` `#IROS2025`
