---
layout: paper
title: "Learning Quadrupedal Locomotion over Challenging Terrain"
category: "高影响力精选 High Impact Selection"
subcategory: "Locomotion Classics"
zhname: "挑战地形下的四足运动学习（ANYmal 里程碑）"
---

# Learning Quadrupedal Locomotion over Challenging Terrain
**挑战地形下的四足运动学习（ANYmal 里程碑）**

> 📅 阅读日期: 待读
> 🏷️ 板块: 02_High_Impact_Selection / Locomotion Classics 骨架
> 🚧 本笔记为骨架，基本信息待人工核对。

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **期刊/arXiv** | 🚧 待核对（Science Robotics 2020） |
| **PDF** | 🚧 |
| **作者** | 🚧 待核对（Joonho Lee, Jemin Hwangbo, Lorenz Wellhausen, Vladlen Koltun, Marco Hutter） |
| **机构** | 🚧 待核对（ETH Zurich / Intel） |
| **发布时间** | 2020-10（🚧 待核对月份） |
| **项目主页** | 🚧 |
| **代码** | 🚧 |

---

## 🎯 一句话总结

> 🚧 待补。推测方向（以论文为准）：首次在 ANYmal 真机上演示用**完全仿真训练**的 RL 策略跨越复杂地形（台阶、泥地、雪地），用 Teacher-Student + privileged 的范式成为后续跑酷 / 人形工作的基础模板。

---

## 📌 英文缩写速查

| 缩写 | 全称 | 简单解释 |
|------|------|----------|
| **TCN** | Temporal Convolutional Network | 学生网络用来编码历史的 |
| **Privileged info** | 特权信息 | 教师看得到但学生看不到的真值（地形接触、摩擦系数等） |
| **Noisy TCN** | | 学生网络在有噪声 proprioception 下稳定运行 |
| 🚧 | | |

---

## ❓ 这篇论文为什么是"Classic"？

> 🚧 待补。可能方向：
> - 把 legged locomotion 的门槛从"平地 / 实验室"推到"真实户外环境"。
> - Teacher-Student + privileged learning 的**正式奠基**（RMA 及后续都在其基础上）。
> - Science Robotics 登刊让 sim-to-real RL 进入主流视野。

---

## 🔧 方法详解

> 🚧 待补：读完论文后填充。
>
> 预期主线：
> 1. **Phase 1** Privileged teacher（全状态 + 地形真值 → action）PPO 训练。
> 2. **Phase 2** Student（proprioception 历史 TCN → action）监督学习。
> 3. 仿真地形随机化：高度场、摩擦、接触 configurations。
> 4. 真机部署：部署噪声下的鲁棒性测试。

---

## 🚶 具体实例

> 🚧 待补（典型：泥地、雪地、台阶、湿滑表面）。

---

## 🤖 工程价值

> 🚧 待补。意义：RMA、ExBody、HumanPlus、OmniH2O 这些方法的 Teacher-Student 骨架都源于它；理解它有助于看清整个 sim-to-real 流水线的祖师爷。

---

## 📁 源码对照

> 🚧 开源代码待核对（RSL 组后续开源的 legged_gym / rsl_rl）。

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
| RMA (2021) | 直接继承两阶段 privileged → student 思路 |
| Extreme Parkour / ANYmal Parkour | 在本文地形基础上升级到跳跃 / 攀爬 |
| 03_Loco-Manipulation_and_WBC | 训练范式被人形 WBC 复用 |

### B. 参考来源

- 🚧 待核对 Science Robotics / arXiv / 代码
