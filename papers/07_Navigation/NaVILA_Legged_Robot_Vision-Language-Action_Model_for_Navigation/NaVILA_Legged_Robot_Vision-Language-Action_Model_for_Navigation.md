---
layout: paper
title: "NaVILA: Legged Robot Vision-Language-Action Model for Navigation"
category: "导航 Navigation"
zhname: "NaVILA：面向腿式机器人导航的视觉 - 语言 - 动作模型"
---

# NaVILA: Legged Robot Vision-Language-Action Model for Navigation
**NaVILA：面向腿式机器人导航的视觉 - 语言 - 动作模型**

> 📅 阅读日期: 待读
> 🏷️ 板块: 07_Navigation 首篇骨架
> 🚧 本笔记为骨架，基本信息待人工核对。

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **arXiv** | 🚧 待核对（候选：2412.04453） |
| **PDF** | 🚧 |
| **作者** | 🚧 待核对（UCSD / NVIDIA 相关团队） |
| **机构** | 🚧 待核对 |
| **发布时间** | 2024（🚧 待核对月份，候选：2024-12） |
| **项目主页** | 🚧 |
| **代码** | 🚧 |

---

## 🎯 一句话总结

> 🚧 待补。推测方向：把 VILA / VLA 范式引入腿式机器人导航——视觉 + 语言指令 → 腿式机器人低层步态命令，形成"端到端视觉语言导航（VLN）"范式。

---

## 📌 英文缩写速查

| 缩写 | 全称 | 简单解释 |
|------|------|----------|
| **VLA** | Vision-Language-Action | 输入视觉 + 语言，输出机器人动作的大模型范式 |
| **VLN** | Vision-and-Language Navigation | 给自然语言指令，机器人按语言指令导航 |
| 🚧 | | |

---

## ❓ NaVILA 要解决什么问题？

> 🚧 待补。可能方向：
> - VLA 大模型主要落在固定底盘机械臂，能否上腿式机器人？
> - 腿式运动的频率（~50Hz）vs VLM 推理（~1Hz）如何解耦？
> - 视觉语言指令到步态动作的层级控制？

---

## 🔧 方法详解

> 🚧 待补：预期双层结构 ① 高层 VLM 输出 waypoint/语义指令；② 低层 locomotion policy。

---

## 🚶 具体实例

> 🚧 待补（典型任务："到沙发前坐下"、"去厨房"、"绕过障碍物到目标区域"）。

---

## 🤖 工程价值

> 🚧 待补。意义：07_Navigation 分类首篇骨架；将大语言模型范式落到腿式/人形导航的代表工作。

---

## 📁 源码对照

> 🚧 代码状态待核对。

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
| 04_Locomotion | 提供低层步态策略 |
| 05_Manipulation | 共享 VLA 基座 |
| 10_Simulation_Benchmark | HumanoidBench 等可作评测场 |

### B. 参考来源

- 🚧 待核对 arXiv / 主页 / 代码
- 建议交叉验证来源：[awesome-humanoid-robot-learning](https://github.com/YanjieZe/awesome-humanoid-robot-learning) Navigation section
