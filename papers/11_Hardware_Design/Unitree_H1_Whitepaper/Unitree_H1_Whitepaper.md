---
layout: paper
title: "Unitree H1 Humanoid Whitepaper"
category: "硬件设计 Hardware Design"
zhname: "宇树 H1 人形机器人白皮书"
---

# Unitree H1 Humanoid Whitepaper
**宇树 H1 人形机器人白皮书**

> 📅 阅读日期: 待读
> 🏷️ 板块: 11_Hardware_Design 首篇骨架
> 🚧 本笔记为骨架，基本信息待人工核对（白皮书无 arXiv 编号，需以官网/技术页为准）。

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **类型** | 商业白皮书 / Spec sheet（非 arXiv 论文） |
| **厂商** | Unitree Robotics（宇树科技） |
| **机型** | H1（H1-2 / G1 为后续型号，单独建条目） |
| **发布时间** | 2023（🚧 待核对具体月份） |
| **官网** | 🚧 待核对（unitree.com/h1/） |
| **技术规格** | 🚧 待核对（身高 / 体重 / 自由度 / 关节扭矩 / 电池续航） |

---

## 🎯 一句话总结

> 🚧 待补。推测方向：H1 是宇树第一代量产人形机器人，主打**全尺寸**、**高扭矩关节**、**开放算法接口**，把通用人形从研究原型推到批量出货。

---

## 📌 关键参数速查（待核对）

| 项目 | 数值 | 备注 |
|------|------|------|
| 身高 | ~180 cm | 🚧 |
| 体重 | ~47 kg | 🚧 |
| 自由度 | 19+ | 🚧（含手腕/夹爪可选） |
| 关节峰值扭矩 | 360 N·m（髋部） | 🚧 |
| 行走速度 | > 1.5 m/s | 🚧 |
| 电池续航 | ~2 h | 🚧 |
| 运算 | Intel / Jetson 双系统 | 🚧 |

---

## ❓ H1 这台机器解决了什么问题？

> 🚧 待补。可能方向：
> - **成本下探**：把全尺寸双足从百万级科研机降到中小研究组可买的价位。
> - **开放生态**：提供 Python/C++ SDK、ROS2 接口，研究者无需从零做底层。
> - **关节性能**：自研高扭矩力控关节，支持 RL 端到端控制。

---

## 🔧 系统组成

> 🚧 待补：核对官网技术规格后填充。
>
> 预期章节：
> 1. **机械**：腿/手/躯干自由度分布；关节模组规格（扭矩、转速、力矩传感）。
> 2. **感知**：IMU、深度相机、激光雷达（可选）的型号与位置。
> 3. **计算**：板载主控芯片、上下层通信架构。
> 4. **能源**：电池容量、热管理。
> 5. **SDK**：API 层级、与 Isaac Lab / MuJoCo 的对接方式。

---

## 🚶 典型应用场景

> 🚧 待补（参考 awesome-humanoid-robot-learning 中以 H1 为底座的论文：ExBody2、HumanPlus、OmniH2O 等）。

---

## 🤖 工程价值

> 🚧 待补。意义：11_Hardware_Design 分类首篇骨架；H1 是当前最常被学界引用的人形硬件平台，了解它的硬件约束有助于读对应控制论文。

---

## 📁 配套软件 / 复现链接

> 🚧
> - Unitree SDK：🚧
> - Isaac Lab 集成：🚧
> - MuJoCo MJCF：🚧

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
| 04_Locomotion | 多数 H1 行走论文以这台机为目标硬件 |
| 03_Loco-Manipulation_and_WBC | ExBody / OmniH2O 等也跑在 H1 上 |
| 09_Sim-to-Real | H1 的 MJCF / URDF 是 sim-to-real 流水线起点 |

### B. 参考来源

- 🚧 待核对 Unitree 官网产品页
- 交叉验证：[awesome-humanoid-robot-learning](https://github.com/YanjieZe/awesome-humanoid-robot-learning) Hardware section
