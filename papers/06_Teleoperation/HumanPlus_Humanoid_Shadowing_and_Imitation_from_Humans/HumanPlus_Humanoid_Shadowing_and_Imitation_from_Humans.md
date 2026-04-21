---
layout: paper
paper_order: 1
title: "HumanPlus: Humanoid Shadowing and Imitation from Humans"
category: "遥操作与模仿"
zhname: "HumanPlus：人形机器人对人类的影子跟随与模仿"
---

# HumanPlus: Humanoid Shadowing and Imitation from Humans
**HumanPlus：人形机器人对人类的影子跟随与模仿**

> 📅 阅读日期: 2026-04-21
> 🏷️ 板块: 06 Teleoperation · 分类起步样例
> 🚧 本笔记已填充基本信息，深度技术细节待细化。

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **arXiv** | [2406.10454](https://arxiv.org/abs/2406.10454) |
| **PDF** | [Download](https://arxiv.org/pdf/2406.10454.pdf) |
| **作者** | Zipeng Fu, Zhuo Xu, Shuran Song |
| **机构** | Stanford University |
| **发布时间** | 2024-06 |
| **项目主页** | [humanoid-ai.github.io](https://humanoid-ai.github.io/) |
| **代码** | [GitHub - MarkFzp/humanplus](https://github.com/MarkFzp/humanplus) |

---

## 🎯 一句话总结

> HumanPlus 实现了仅需单个 RGB 摄像头即可让 1.8 米高的人形机器人实时"影子跟随"人类动作，并能通过模仿学习在 40 次左右的演示后学会穿鞋、折衣服等复杂技能。

---

## 📌 英文缩写速查

| 缩写 | 全称 | 简单解释 |
|------|------|----------|
| HST | Humanoid Shadowing Transformer | 低层控制策略，负责将人类姿态映射为机器人关节指令 |
| HIT | Humanoid Imitation Transformer | 高层技能策略，负责从视觉和状态中学习自主行为 |
| AMASS | Archive of Motion Capture as Surface Shapes | 大规模人类动捕数据集，用于 HST 的预训练 |

---

## ❓ 论文要解决什么问题？

- **遥操作门槛高**：传统的全身遥操作通常需要昂贵的动捕设备（如 Xsens）或复杂的视觉方案。
- **具身 Gap 挑战**：人类与人形机器人（如 Unitree H1）在高度、自由度、质量分布上存在差异。
- **技能获取效率**：如何从简单的"影子跟随"数据中快速蒸馏出自主执行的技能？

---

## 🔧 方法详解

1. **两阶段架构**：
   - **阶段一：影子跟随 (Shadowing)**：使用单摄像头追踪人，HST 策略将姿态实时转换为 H1 机器人的动作。
   - **阶段二：自主学习 (Imitation)**：在影子跟随过程中，机器人通过头部的 binocular 相机收集第一视角数据，由 HIT 策略进行模仿学习。
2. **HST 预训练**：
   - 在仿真中使用 40 小时的 AMASS 动捕数据进行强化学习，学习如何平衡 and 移动，实现了零样本（Zero-shot）的 Sim-to-Real 迁移。
3. **HIT 模仿学习**：
   - 采用 Transformer 架构处理时序视觉输入。
   - 只需约 40 个演示（约 2 小时数据）即可掌握一个新技能。

---

## 🚶 具体实例

- **穿鞋并行走**：机器人能够先坐下，用手拎起鞋子套在脚上，然后站起来行走。
- **仓库卸货**：通过影子跟随演示，机器人学会了将箱子从货架上搬运到传送带上。
- **社交互动**：学会了与人打招呼、击掌。

---

## 🤖 工程价值

- **极低成本遥操作**：只需要一个摄像头，极大降低了全身控制研究的设备门槛。
- **全栈开源**：不仅开源了算法代码，还提供了 Unitree H1 的硬件改装方案。
- **复杂任务突破**：在全尺寸人形机器人上展示了折衣服、穿鞋等极高难度的精细化操作。

---

## 🎤 面试高频问题 & 参考回答

1. **单摄像头如何保证深度和 3D 姿态的准确性？**
   - 并非追求绝对坐标精度，而是通过 HST 学习从 2D/3D 关键点序列到平衡动作的映射。
2. **HST 和 HIT 的关系？**
   - HST 是"小脑"（负责平衡与关节控制），HIT 是"大脑"（负责决策与视觉引导）。

---

## 📎 附录

### A. 参考来源
- [arXiv:2406.10454](https://arxiv.org/abs/2406.10454)
- [Project Website](https://humanoid-ai.github.io/)
