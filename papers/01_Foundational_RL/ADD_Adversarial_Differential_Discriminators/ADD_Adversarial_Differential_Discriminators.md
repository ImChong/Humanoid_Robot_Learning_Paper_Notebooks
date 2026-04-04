---
layout: paper
paper_order: 7
title: "ADD: Adversarial Disentanglement and Distillation"
category: "Foundational RL"
---

# ADD: Adversarial Disentanglement and Distillation
**对抗差分鉴别器：基于物理的运动模仿**

> 📅 阅读日期: -  
> 🏷️ 板块: Reinforcement Learning / Motion Imitation / Adversarial Learning

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **arXiv** | [2505.04961](https://arxiv.org/abs/2505.04961) |
| **PDF** | [下载](https://arxiv.org/pdf/2505.04961) |
| **作者** | Ziyu Zhang, Sergey Bashkirov, Dun Yang, Yi Shi, Michael Taylor, Xue Bin Peng |
| **机构** | Simon Fraser University, NVIDIA |
| **发布时间** | 2025年 |
| **项目主页** | [ziyuz.github.io/ADD](https://ziyuz.github.io/ADD/) |
| **GitHub** | [xbpeng/MimicKit](https://github.com/xbpeng/MimicKit) |

---

## 🎯 一句话总结

ADD 提出**对抗差分鉴别器**——一种新型多目标优化技术，让物理仿真角色能精确复制参考运动（包括杂技和敏捷动作），达到与手工调参的 motion tracking 方法相当的质量，但**不需要手工设计奖励函数**。它将 AMP 的"分布匹配"目标改为"精确跟踪"，鉴别器只需要单个正样本即可工作。

---
## 📌 英文缩写速查

| 缩写 | 全称 | 简单解释 |
|------|------|----------|
| **ADD** | Adversarial Disentanglement and Distillation | 对抗解耦与蒸馏：将对抗学习用于精确运动跟踪 |
| **AMP** | Adversarial Motion Priors | 对抗运动先验：用判别器正则化动作自然性 |
| **RL** | Reinforcement Learning | 强化学习：通过奖惩反馈训练策略 |
| **GAN** | Generative Adversarial Network | 生成对抗网络：生成器与判别器对抗训练 |
| **PHC** | Perpetual Humanoid Control | 永续人形控制：大规模动作模仿的 RL 框架 |


## ❓ 这篇论文要解决什么问题？

> 待补充

---

## 🔧 ADD 是怎么做的？

> 待补充

---

## 🚶 具体实例

> 待补充

---

## 🤖 ADD 对人形机器人领域的意义

> 待补充

---

## 🎤 面试高频问题 & 参考回答

> 待补充

---

## 💬 讨论记录

> 待补充

---

## 📎 附录

### A. 与路线图其他论文的关联

| 关系 | 说明 |
|------|------|
| **AMP → ADD** | ADD 将 AMP 的分布匹配改为精确轨迹跟踪 |
| **DeepMimic → ADD** | DeepMimic 用手工奖励精确跟踪，ADD 用对抗学习自动实现精确跟踪 |
| **ADD vs PHC** | 都做精确运动跟踪，但 ADD 不需要手工设计模仿奖励 |
