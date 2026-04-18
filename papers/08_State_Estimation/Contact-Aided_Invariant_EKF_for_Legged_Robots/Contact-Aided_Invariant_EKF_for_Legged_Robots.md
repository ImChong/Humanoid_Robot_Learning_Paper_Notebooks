---
layout: paper
title: "Contact-Aided Invariant EKF for Legged Robot State Estimation"
category: "状态估计 State Estimation"
zhname: "接触辅助不变 EKF：腿式机器人状态估计"
---

# Contact-Aided Invariant EKF for Legged Robot State Estimation
**接触辅助不变 EKF：腿式机器人状态估计**

> 📅 阅读日期: 待读
> 🏷️ 板块: 08_State_Estimation 首篇骨架
> 🚧 本笔记为骨架，基本信息待人工核对。标题为通用经典题目，具体论文版本/作者/arXiv 以原文为准。

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **arXiv** | 🚧 待核对（候选：1805.10410，Hartley et al.） |
| **PDF** | 🚧 |
| **作者** | 🚧 待核对（Hartley / Gahlani / Grizzle 等 U-Mich 团队） |
| **机构** | 🚧 待核对（University of Michigan） |
| **发布时间** | 2018（🚧 待核对会议/年份） |
| **项目主页** | 🚧 |
| **代码** | 🚧 开源实现（如 `contact-aided-invariant-ekf`，待核对） |

---

## 🎯 一句话总结

> 🚧 待补。推测方向：在腿式机器人（Cassie/人形）上，利用**接触腿的零速度约束**作为观测，配合**不变 EKF（InEKF）** 的李群误差建模，得到比普通 EKF 更稳定的全身姿态/速度估计。

---

## 📌 英文缩写速查

| 缩写 | 全称 | 简单解释 |
|------|------|----------|
| **EKF** | Extended Kalman Filter | 扩展卡尔曼滤波器 |
| **InEKF** | Invariant EKF | 不变 EKF，误差定义在李群上，避免线性化偏差 |
| **IMU** | Inertial Measurement Unit | 惯性测量单元（加速度计 + 陀螺仪） |
| **Zero-velocity update** | 零速度更新 | 脚掌接触时假设脚掌速度为 0 |
| 🚧 | | |

---

## ❓ Contact-Aided InEKF 要解决什么问题？

> 🚧 待补。可能方向：
> - 腿式机器人缺少 GPS，只能靠 IMU + 接触观测做里程计
> - 普通 EKF 在旋转大时线性化误差累积
> - 如何把"接触腿相对基座位置零速度"作为观测融合进不变 EKF？

---

## 🔧 方法详解

> 🚧 待补：预期包含 ① 状态 = 基座姿态 + 速度 + 位置 + 脚位（李群扩展）；② 预测来自 IMU；③ 观测来自 FK + 接触检测。

---

## 🚶 具体实例

> 🚧 待补（Cassie / ANYmal / humanoid 上的评测）。

---

## 🤖 工程价值

> 🚧 待补。意义：08_State_Estimation 分类首篇骨架；几乎所有腿式机器人 sim-to-real 栈的标配上游模块。

---

## 📁 源码对照

> 🚧 待核对（ROS 包 / C++ 库）。

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
| 04_Locomotion | 为 RL 策略提供稳定的基座速度观测 |
| 09_Sim-to-Real | 真机部署必备的感知栈 |
| 11_Hardware_Design | 与 IMU/编码器选型直接相关 |

### B. 参考来源

- 🚧 待核对 arXiv / 原论文
- 建议交叉验证来源：[awesome-humanoid-robot-learning](https://github.com/YanjieZe/awesome-humanoid-robot-learning) State Estimation section
