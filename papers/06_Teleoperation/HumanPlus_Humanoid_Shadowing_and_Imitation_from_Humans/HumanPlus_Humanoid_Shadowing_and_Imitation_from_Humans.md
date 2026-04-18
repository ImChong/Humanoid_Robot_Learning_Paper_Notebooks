---
layout: paper
title: "HumanPlus: Humanoid Shadowing and Imitation from Humans"
category: "遥操作 Teleoperation"
zhname: "HumanPlus：人形机器人影子跟随与人类模仿"
---

# HumanPlus: Humanoid Shadowing and Imitation from Humans
**HumanPlus：人形机器人影子跟随与人类模仿**

> 📅 阅读日期: 待读
> 🏷️ 板块: 06_Teleoperation 首篇骨架
> 🚧 本笔记为骨架，基本信息待人工核对。

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **arXiv** | 🚧 待核对（候选：2406.10454） |
| **PDF** | 🚧 |
| **作者** | 🚧 待核对（Stanford 团队） |
| **机构** | 🚧 待核对（Stanford） |
| **发布时间** | 2024（🚧 待核对月份，候选：2024-06） |
| **项目主页** | 🚧 |
| **代码** | 🚧 开源（awesome 列表标 🌟） |

---

## 🎯 一句话总结

> 🚧 待补。推测方向：把人类动作（RGB / mocap）实时映射到人形机器人上（shadowing），再通过模仿学习把这些遥操数据蒸馏成自主策略。一套人形"人类 → 机器人"的数据生成 + 策略学习框架。

---

## 📌 英文缩写速查

| 缩写 | 全称 | 简单解释 |
|------|------|----------|
| **Shadowing** | 影子跟随 | 机器人实时复制人类动作，用作遥操/数据采集 |
| 🚧 | | |

---

## ❓ HumanPlus 要解决什么问题？

> 🚧 待补。可能方向：
> - 人形遥操系统门槛高（动捕衣、外骨骼）→ 能否仅凭 RGB？
> - 得到遥操数据后如何扩展到自主策略？
> - 人类身形 vs 机器人身形差异如何重映射（retargeting）？

---

## 🔧 方法详解

> 🚧 待补：预期包含 ① 人体姿态估计；② retargeting 到机器人关节；③ 全身 RL/控制；④ 模仿学习头。

---

## 🚶 具体实例

> 🚧 待补（典型场景：系鞋带、打球、抓取、坐下等）。

---

## 🤖 工程价值

> 🚧 待补。意义：06_Teleoperation 分类首篇骨架；代表"单目视频 → 实时人形遥操"低成本路线。

---

## 📁 源码对照

> 🚧 开源代码 repo 待核对。

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
| 03_Loco-Manipulation_and_WBC | 提供全身控制器下层 |
| 13_Human_Motion | 共用人类姿态估计模块 |
| 05_Manipulation | 上肢策略可能共用 |

### B. 参考来源

- 🚧 待核对 arXiv / 主页 / 代码
- 建议交叉验证来源：[awesome-humanoid-robot-learning](https://github.com/YanjieZe/awesome-humanoid-robot-learning) Teleoperation section
