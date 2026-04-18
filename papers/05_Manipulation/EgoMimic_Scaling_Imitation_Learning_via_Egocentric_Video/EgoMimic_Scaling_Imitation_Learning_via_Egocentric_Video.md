---
layout: paper
title: "EgoMimic: Scaling Imitation Learning via Egocentric Video"
category: "操作 Manipulation"
zhname: "EgoMimic：用第一人称视频规模化模仿学习"
---

# EgoMimic: Scaling Imitation Learning via Egocentric Video
**EgoMimic：用第一人称视频规模化模仿学习**

> 📅 阅读日期: 待读
> 🏷️ 板块: 05_Manipulation 首篇骨架
> 🚧 本笔记为骨架，基本信息待人工核对。以下字段除分类定位外均待原论文确认。

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **arXiv** | 🚧 待核对（候选：2410.24221） |
| **PDF** | 🚧 |
| **作者** | 🚧 待核对（主要作者来自 Georgia Tech） |
| **机构** | 🚧 待核对 |
| **发布时间** | 2024（🚧 待核对月份） |
| **项目主页** | 🚧 |
| **代码** | 🚧 开源（见 awesome-humanoid-robot-learning 列表标 🌟） |

---

## 🎯 一句话总结

> 🚧 待补。推测方向（以论文为准）：利用大规模人类**第一人称（egocentric）视频**作为模仿学习的数据源，配合少量机器人遥操数据，在人形/双臂操作上获得可泛化的视觉 - 动作策略。

---

## 📌 英文缩写速查

| 缩写 | 全称 | 简单解释 |
|------|------|----------|
| **Egocentric video** | 第一人称视频 | 相机戴在人头上/胸前拍到的视角，与机器人相机视角几何对齐容易 |
| 🚧 | | |

---

## ❓ EgoMimic 要解决什么问题？

> 🚧 待补。可能方向：
> - 遥操数据昂贵 → 能否用便宜的人类第一人称视频替代或补充？
> - 人类手与机械臂形态不同 → 如何处理 embodiment gap？
> - 视频只有 observation，没有 action 标签 → 如何从视频中学到可执行的动作？

---

## 🔧 方法详解

> 🚧 待补：读完论文后填充（预期包含视觉 backbone、手部/末端执行器对齐、共同训练策略、策略头设计等）。

---

## 🚶 具体实例

> 🚧 待补（典型任务：双臂拿取/放置、长时序操作）。

---

## 🤖 工程价值

> 🚧 待补。意义：05_Manipulation 分类首篇骨架；是"人类视频 → 机器人操作"数据引擎思路的代表之作。

---

## 📁 源码对照

> 🚧 开源代码待实测对照（repo 暂记："EgoMimic"）。

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
| 06_Teleoperation | 遥操数据 vs 视频数据的互补关系 |
| 13_Human_Motion | 都以人类视频为起点，但目标任务层级不同 |
| Diffusion Policy | 可能作为底层策略类 |

### B. 参考来源

- 🚧 待核对 arXiv / 主页 / 代码
- 建议交叉验证来源：[awesome-humanoid-robot-learning](https://github.com/YanjieZe/awesome-humanoid-robot-learning) Manipulation section
