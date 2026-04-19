---
layout: paper
title: "ANYmal Parkour: Robust Perceptive Locomotion"
category: "行走 Locomotion"
zhname: "ANYmal 跑酷：鲁棒的感知型移动"
---

# ANYmal Parkour: Robust Perceptive Locomotion
**ANYmal 跑酷：鲁棒的感知型移动**

> 📅 阅读日期: 待读
> 🏷️ 板块: 04_Locomotion 扩展骨架
> 🚧 本笔记为骨架，基本信息待人工核对。

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **arXiv** | 🚧 待核对（候选：2312.08647，Science Robotics 2024 版本） |
| **PDF** | 🚧 |
| **作者** | 🚧 待核对（Takahiro Miki 等，ETH RSL） |
| **机构** | 🚧 待核对（ETH Zurich / Intel） |
| **发布时间** | 2023–2024（🚧 待核对具体月份） |
| **期刊** | 🚧（Science Robotics 候选） |
| **项目主页** | 🚧 |
| **代码** | 🚧 |

---

## 🎯 一句话总结

> 🚧 待补。推测方向：ETH RSL 系列沿 Hutter 组主线，将**感知型运动（Perceptive Locomotion）**从平地扩展到跑酷级别，强调对传感噪声和相机掉帧的鲁棒性。

---

## 📌 英文缩写速查

| 缩写 | 全称 | 简单解释 |
|------|------|----------|
| **Perceptive Locomotion** | 感知型运动 | 融合本体 + 视觉 / 高度图的运动控制 |
| **Elevation map** | 高程图 | 机器人周围地形高度栅格 |
| **RMA-style** | RMA 风格两阶段训练 | Teacher-Student + privileged |
| 🚧 | | |

---

## ❓ ANYmal Parkour 要解决什么问题？

> 🚧 待补。可能方向：
> - 复杂地形需要视觉 → 但相机容易掉帧 / 被遮挡。
> - 要求能同时"看得准"和"失明时不摔"。
> - 与 CMU Extreme Parkour 的对比：不同硬件（ANYmal vs A1）与不同感知（elevation map vs ego depth）。

---

## 🔧 方法详解

> 🚧 待补：读完论文后填充。
>
> 预期主线：
> 1. 高程图 + 本体感觉作为学生输入。
> 2. Teacher 用 privileged 地形。
> 3. Noise / dropout 训练使学生对感知退化鲁棒。

---

## 🚶 具体实例

> 🚧 待补。

---

## 🤖 工程价值

> 🚧 待补。意义：ETH 系列跑酷工作与 CMU 系列并列，理解两家方法论有助于把握感知型运动的两条主线。

---

## 📁 源码对照

> 🚧 开源代码待核对。

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
| Extreme Parkour (CMU) | 同期跑酷工作，对比项 |
| RMA | 两阶段训练思路的源头 |
| 09_Sim-to-Real | 视觉退化鲁棒性是典型 sim-to-real 挑战 |

### B. 参考来源

- 🚧 待核对 arXiv / 主页 / 代码
