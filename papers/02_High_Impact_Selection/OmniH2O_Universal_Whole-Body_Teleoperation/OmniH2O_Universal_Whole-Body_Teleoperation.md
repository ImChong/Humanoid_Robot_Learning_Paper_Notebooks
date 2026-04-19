---
layout: paper
title: "OmniH2O: Universal and Dexterous Human-to-Humanoid Whole-Body Teleoperation and Learning"
category: "高影响力精选 High Impact Selection"
zhname: "OmniH2O：通用灵巧的人 - 人形整体遥操与学习"
---

# OmniH2O: Universal and Dexterous Human-to-Humanoid Whole-Body Teleoperation and Learning
**OmniH2O：通用灵巧的人 - 人形整体遥操与学习**

> 📅 阅读日期: 待读
> 🏷️ 板块: 02_High_Impact_Selection 扩展骨架
> 🚧 本笔记为骨架，基本信息待人工核对。

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **arXiv** | 🚧 待核对（候选：2406.08858） |
| **PDF** | 🚧 |
| **作者** | 🚧 待核对（Tairan He, Zhengyi Luo 等） |
| **机构** | 🚧 待核对（CMU / NVIDIA / UC San Diego） |
| **发布时间** | 2024（🚧 待核对月份） |
| **项目主页** | 🚧 |
| **代码** | 🚧 |

---

## 🎯 一句话总结

> 🚧 待补。推测方向：把 H2O 扩展到**全身 + 灵巧手**，用 sim-to-real 单策略覆盖上半身表达性动作 + 下半身行走 + 手指操作，支持 VR 头显 + 体感外设实时遥操人形机器人。

---

## 📌 英文缩写速查

| 缩写 | 全称 | 简单解释 |
|------|------|----------|
| **OmniH2O** | Omnidirectional Human-to-Humanoid | 本文方法名 |
| **WBC** | Whole-Body Control | 整体控制 |
| 🚧 | | |

---

## ❓ OmniH2O 要解决什么问题？

> 🚧 待补。可能方向：
> - **上下肢分策略**的拼接痕迹明显 → 要一个统一的全身策略。
> - **灵巧手被割裂**：WBC 工作大多不关心手指 → OmniH2O 把手包进来。
> - **遥操延迟 / 重瞄**：输入 modality 多，如何兼容 VR、RGB、Mocap。

---

## 🔧 方法详解

> 🚧 待补：读完论文后填充。
>
> 预期主线：
> 1. **Motion retargeting**：人类动作 → 机器人参考轨迹。
> 2. **Sim-to-real 策略**：privileged teacher + student distillation（类 RMA / H2O）。
> 3. **多模态接口**：VR 头显、RGB-based pose estimation、Mocap 三套输入统一到同一参考。

---

## 🚶 具体实例

> 🚧 待补。

---

## 🤖 工程价值

> 🚧 待补。意义：当前人形通用遥操 + 学习框架的代表作，跨 06_Teleoperation、03_Loco-Manipulation_and_WBC 两条线。

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
| H2O (Tairan He 2024 前作) | OmniH2O 的直接前身 |
| ExBody / ExBody2 | 同类 WBC 方案，强调表达性 |
| HumanPlus | 相近问题域但策略结构不同 |

### B. 参考来源

- 🚧 待核对 arXiv / 主页 / 代码
