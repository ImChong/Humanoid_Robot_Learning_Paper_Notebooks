---
layout: paper
paper_order: 1
title: "RMA: Rapid Motor Adaptation for Legged Robots"
category: "仿真到真实"
zhname: "RMA：足式机器人的快速电机自适应"
---

# RMA: Rapid Motor Adaptation for Legged Robots
**RMA：足式机器人的快速电机自适应**

> 📅 阅读日期: 2026-04-21
> 🏷️ 板块: 09 Sim-to-Real · 分类起步样例
> 🚧 本笔记已填充基本信息，深度技术细节待细化。

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **arXiv** | [2107.04034](https://arxiv.org/abs/2107.04034) (RSS 2021) |
| **PDF** | [Download](https://arxiv.org/pdf/2107.04034.pdf) |
| **作者** | Ashish Kumar, Zipeng Fu, Deepak Pathak, Jitendra Malik |
| **机构** | UC Berkeley / Facebook AI Research / CMU |
| **发布时间** | 2021-07 |
| **项目主页** | [ashish-kmr.github.io/rma-legged-robots/](https://ashish-kmr.github.io/rma-legged-robots/) |
| **代码** | 🚧 |

---

## 🎯 一句话总结

> RMA 提出了一个两阶段学习框架，让机器人通过自身的运动历史来实时"感应"并适应未知的环境外因（如摩擦力、负载、坡度），实现了无需任何现实微调的零样本（Zero-shot）环境迁移。

---

## 📌 英文缩写速查

| 缩写 | 全称 | 简单解释 |
|------|------|----------|
| RMA | Rapid Motor Adaptation | 快速电机自适应 |
| Privileged Info | 特权信息 | 仅在仿真中可知的环境参数（如精确地面摩擦力） |
| Proprioception | 本体感受 | 机器人自身的关节位置、速度等内部传感器信息 |

---

## ❓ 论文要解决什么问题？

- **Sim-to-Real Gap**：仿真环境无法穷举现实世界的每一种地形和物理参数。
- **环境感知的实时性**：当机器人从地毯走到油滑表面，或被放上重物时，如何不依赖视觉、在零点几秒内完成步态调整？
- **传统建模局限**：传统的控制方法依赖精确的动力学模型，难以处理复杂的非线性地面交互。

---

## 🔧 方法详解

1. **第一阶段：特权信息下的策略学习 (Base Policy Training)**：
   - 在仿真中，智能体可以访问"特权信息"（摩擦力、质量、重心、坡度等）。
   - 训练一个 **Environment Encoder** 将这些信息压缩为 **Extrinsics** 向量。
   - Base Policy 以当前状态和 Extrinsics 为输入，学习最优动作。
2. **第二阶段：自适应模块训练 (Adaptation Module)**：
   - 移除特权信息。
   - 训练一个 **Adaptation Module**（通常为 TCN 或 LSTM），仅根据机器人最近的**本体感受历史**来预测 Extrinsics 向量。
   - 核心逻辑：如果机器人的腿打滑了，那它就能推断出地面摩擦力很小，从而调整 Extrinsics 引导策略。
3. **部署**：
   - 在现实世界中，仅运行 Adaptation Module 和 Base Policy，实现实时的"感知 - 适应 - 执行"闭环。

---

## 🚶 具体实例

- **多地形挑战**：四足机器人 Unitree A1 可以在沙地、草地、海绵垫、台阶上无缝切换。
- **动态干扰**：在机器人背上突然增加 8kg 负载，它能在几步之内稳定住身形。
- **极端条件**：在涂油的塑料板上行走也能保持平衡。

---

## 🤖 工程价值

- **方法论突破**：彻底改变了 Sim-to-Real 的思路，从"努力做更真实的仿真"转变为"训练机器人具备实时适应能力"。
- **可扩展性**：该框架已被后续广泛应用在双足机器人 (A-RMA) 和灵巧手操作中。
- **端到端效率**：不需要人工设计的步态，纯通过强化学习涌现出鲁棒的行走能力。

---

## 🎤 面试高频问题 & 参考回答

1. **RMA 为什么不需要视觉传感器也能适应地形？**
   - 因为地形的物理属性会直接反映在机器人的关节动力学反馈中（打滑、沉降、碰撞），Adaptation Module 能够从时序反馈中逆向推断出环境属性。
2. **"特权信息"在训练后被丢弃了吗？**
   - 是的。部署时机器人并不直接知道这些参数，而是通过 Adaptation Module "猜"出来的。

---

## 📎 附录

### A. 参考来源
- [arXiv:2107.04034](https://arxiv.org/abs/2107.04034)
- [Project Website](https://ashish-kmr.github.io/rma-legged-robots/)
