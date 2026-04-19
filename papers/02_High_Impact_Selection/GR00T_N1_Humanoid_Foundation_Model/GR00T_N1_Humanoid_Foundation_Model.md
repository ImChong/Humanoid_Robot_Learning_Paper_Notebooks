---
layout: paper
title: "GR00T N1: An Open Foundation Model for Generalist Humanoid Robots"
category: "高影响力精选 High Impact Selection"
subcategory: "Sim-to-Real & Foundation Model"
zhname: "GR00T N1：通用人形机器人开源基座模型"
---

# GR00T N1: An Open Foundation Model for Generalist Humanoid Robots
**GR00T N1：通用人形机器人开源基座模型**

> 📅 阅读日期: 待读
> 🏷️ 板块: 02_High_Impact_Selection / Sim-to-Real & Foundation Model 骨架
> 🚧 本笔记为骨架，基本信息待人工核对。

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **arXiv** | 🚧 待核对（候选：2503.14734） |
| **PDF** | 🚧 |
| **作者** | 🚧 待核对（NVIDIA GEAR Team） |
| **机构** | 🚧 待核对（NVIDIA） |
| **发布时间** | 2025（🚧 待核对月份） |
| **项目主页** | 🚧（NVIDIA developer） |
| **代码 / 权重** | 🚧 开源 |

---

## 🎯 一句话总结

> 🚧 待补。推测方向：NVIDIA 推出的**开源**人形机器人基座模型，采用 **System 1 / System 2 双系统**（快策略 + 慢 VLA），在大规模 egocentric 视频 + 仿真数据上预训练，支持多个硬件平台。

---

## 📌 英文缩写速查

| 缩写 | 全称 | 简单解释 |
|------|------|----------|
| **GR00T** | Generalist Robot 00T（NVIDIA 品牌） | NVIDIA 的人形基座模型系列 |
| **VLA** | Vision-Language-Action | 视觉 + 语言 → 动作 |
| **System 1/2** | Kahneman 快慢双系统 | 快推理（低延迟控制） + 慢推理（高层 reasoning） |
| 🚧 | | |

---

## ❓ GR00T N1 要解决什么问题？

> 🚧 待补。可能方向：
> - 人形机器人缺少**通用基座模型**，每个工作都要从零训。
> - 数据来源如何统一：视频 + 仿真 + 真机。
> - 如何在**一个模型**里同时支持多硬件（H1、G1、Optimus 等）。

---

## 🔧 方法详解

> 🚧 待补：读完论文后填充。
>
> 预期主线：
> 1. **数据金字塔**：互联网人类视频（最宽） / 合成数据（中间） / 真机遥操数据（最窄）。
> 2. **双系统**：System 2（VLA，慢）读入视觉 + 指令 → 潜动作 token；System 1（快）把 token 解码成 action。
> 3. **多硬件 embodiment token** 让同一模型跑在不同机器人上。
> 4. **微调**：在目标任务上少样本微调。

---

## 🚶 具体实例

> 🚧 待补（典型任务：桌面操作、双臂协作、家居整理）。

---

## 🤖 工程价值

> 🚧 待补。意义：当前人形机器人**基座模型**的代表作，开源权重让研究者可以直接微调，是跨越 02 / 03 / 05 三条主线的超级节点。

---

## 📁 源码对照

> 🚧 权重与代码仓库待核对：
> - 📦 HuggingFace：🚧
> - 📦 GitHub：🚧

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
| HumanPlus / OmniH2O | 都依赖 mocap / 遥操数据，GR00T 把它们吸收进基座模型 |
| Diffusion Policy | System 1 可能使用扩散策略作为动作头 |
| Isaac Lab | 合成数据来源 |

### B. 参考来源

- 🚧 待核对 arXiv / 主页 / 代码
