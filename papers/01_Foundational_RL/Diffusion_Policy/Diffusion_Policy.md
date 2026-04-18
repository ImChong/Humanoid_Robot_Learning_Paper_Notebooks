---
layout: paper
paper_order: 12
title: "Diffusion Policy: Visuomotor Policy Learning via Action Diffusion"
category: "基础强化学习"
zhname: "Diffusion Policy：基于动作扩散的视觉运动策略学习"
---

# Diffusion Policy: Visuomotor Policy Learning via Action Diffusion
**Diffusion Policy：基于动作扩散的视觉运动策略学习**

> 📅 阅读日期: 待读
> 🏷️ 板块: 扩散+控制终点主线起点
> 🚧 本笔记为骨架，待逐节补完。

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **arXiv** | [2303.04137](https://arxiv.org/abs/2303.04137) 🚧 待核对 |
| **PDF** | 🚧 |
| **作者** | Cheng Chi 等（🚧 待核对） |
| **机构** | Columbia / Toyota Research Institute（🚧 待核对） |
| **发布时间** | RSS 2023 |
| **项目主页** | 🚧 |
| **代码** | 🚧 |

---

## 🎯 一句话总结

> 🚧 待补：用扩散模型生成动作序列，把操作策略从"单步回归"升级为"多步轨迹生成"，显著改善多模态行为的表达。

---

## 📌 英文缩写速查

| 缩写 | 全称 | 简单解释 |
|------|------|----------|
| DDPM | Denoising Diffusion Probabilistic Model | 去噪扩散概率模型 |
| DDIM | Denoising Diffusion Implicit Model | 非马尔可夫采样的加速版本 |
| 🚧 | | |

---

## ❓ Diffusion Policy 要解决什么问题？

> 🚧 待补。关键切入点：
> - 传统 BC 策略（MLP / MDN）在**多模态动作分布**下表现差——人类演示里"同一个状态两种走法"会被平均成怪异动作；
> - GMM、VAE 等方案表达力仍有限；
> - 扩散模型在图像生成上显示出"对多模态极强的建模能力"，是否能搬到动作空间？

---

## 🔧 方法详解

> 🚧 待补。参考展开：
> 1. Action chunking：一次生成 H 步动作
> 2. Conditional denoising：以观测为条件去噪
> 3. 网络结构（U-Net / Transformer 两种常见实现）
> 4. 训练目标（预测噪声 ε）
> 5. 推理（DDIM 加速）

---

## 🚶 具体实例

> 🚧 待补。建议：拿一个"推方块到目标位置"的小例子，把一次前向的 "观测 → 采样 → 去噪 → 输出动作序列" 走一遍。

---

## 🤖 工程价值

> 🚧 待补。关注点：
> - 为什么它成为后续大量模仿学习工作的默认骨干？
> - 对延迟 / 实时性的影响（扩散步数）？
> - 与 ACT、RT-2 等范式的对比？
> - 在人形机器人 loco-manipulation 中的应用（连接到 BeyondMimic 等）

---

## 📁 MimicKit 源码对照

> 🚧 MimicKit 目前聚焦于运动模仿，未必覆盖 Diffusion Policy；若无，本节标 ❌。

---

## 🎤 面试高频问题 & 参考回答

> 🚧 5–8 题待补。候选：
> 1. 为什么扩散模型擅长多模态？
> 2. action chunking 为什么重要？
> 3. 训练目标是预测噪声还是预测动作？
> 4. 扩散步数对推理延迟的影响？
> 5. Diffusion Policy vs RT-2 / ACT 差异？

---

## 💬 讨论记录

> 🚧

---

## 📎 附录

### A. 与路线图的关系

| 论文 | 关系 |
|------|------|
| **Diffusion Policy (2023)** | 扩散 + 控制主线的**起点** |
| BeyondMimic (2025) | 扩散控制在人形机器人上的延伸（🚧 待核对） |

### B. 参考来源

- 🚧 原论文 & 项目主页
- 🚧 作者后续工作（Diffusion Policy v2 / 3D 变种）
