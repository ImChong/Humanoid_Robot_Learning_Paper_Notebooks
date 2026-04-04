---
layout: paper
title: "Expressive Whole-Body Control for Humanoid Robots"
category: "High Impact Selection"
subcategory: "Whole-Body Control Core"
---

# Expressive Whole-Body Control for Humanoid Robots
**人形机器人的表达性全身控制**

> 📅 阅读日期: -  
> 🏷️ 板块: Whole-Body Control / Humanoid

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **arXiv** | [2402.16796](https://arxiv.org/abs/2402.16796) |
| **PDF** | [下载](https://arxiv.org/pdf/2402.16796) |
| **作者** | Xuxin Cheng, Yandong Ji, Junming Chen, Ruihan Yang, Ge Yang, Xiaolong Wang |
| **机构** | UC San Diego |
| **发布时间** | 2024年（RSS 2024） |
| **项目主页** | [expressive-humanoid.github.io](https://expressive-humanoid.github.io/) |
| **代码** | [GitHub 🌟](https://github.com/chengxuxin/expressive-humanoid) |

---

## 🎯 一句话总结

让人形机器人在**保持行走稳定性**的同时，用上半身做出**丰富的表达性动作**（挥手、舞蹈等）——全身控制的开山之作，开源，工程参考价值极高。

---
## 📌 英文缩写速查

| 缩写 | 全称 | 简单解释 |
|------|------|----------|
| **DoF** | Degrees of Freedom | 自由度：机器人可独立运动的轴数 |
| **RL** | Reinforcement Learning | 强化学习：通过奖惩反馈训练策略 |
| **MoCap** | Motion Capture | 动作捕捉：记录人体运动数据的技术 |
| **Sim-to-Real** | Simulation to Reality | 仿真到真实迁移：仿真训练迁移到真实机器人 |
| **RSS** | Robotics Science and Systems | 机器人学顶级会议，本论文发表场所 |


## 🔍 核心问题与动机

**问题：** 如何让人形机器人在完成运动任务（走路）的同时，还能控制上半身做出有意义的姿态和动作？

**挑战：**
- 上下半身动作会相互干扰（上半身摆动影响行走平衡）
- 人类动作捕捉数据与机器人运动学不匹配（自由度不同）
- 实现 sim-to-real 迁移

**动机：** 实用的人形机器人不只需要"走路"，还需要与人交互——挥手、指引、舞蹈、搬运等，这要求全身协调控制。

---

## 🛠️ 方法详解

### 整体框架

**两级控制结构：**
1. **上层：** 接收参考动作（来自人类动作捕捉），生成全身目标姿态
2. **下层（RL策略）：** 在物理约束下执行目标姿态，同时保持行走平衡

### 关键技术

**1. 运动重定向（Motion Retargeting）**
- 将人类 mocap 数据映射到机器人关节空间
- 处理自由度不匹配问题（人类 ~73 DOF → 机器人 ~19 DOF）

**2. 分层 RL 训练**
- 下半身策略：专注行走稳定
- 上半身策略：跟踪参考动作
- 联合训练实现全身协调

**3. Sim-to-Real**
- 域随机化（Domain Randomization）
- 在 Isaac Gym 中训练，部署到真实机器人

---

## 📐 关键公式

**奖励函数（全身控制）：**

$$r = r_{\text{tracking}} + r_{\text{locomotion}} + r_{\text{regularization}}$$

- $r_{\text{tracking}}$：上半身关节角度跟踪误差
- $r_{\text{locomotion}}$：行走速度、姿态稳定性
- $r_{\text{regularization}}$：动作平滑、能量消耗惩罚

---

## 🔧 工程复现要点

- **训练框架：** Isaac Gym（GPU 并行仿真）
- **机器人：** Unitree H1
- **开源代码：** 完整训练和部署代码公开
- **关键超参：** 上下半身奖励权重需要仔细调节

---

## 💡 核心贡献

1. **首次**在真实人形机器人上实现行走 + 丰富上半身表达的联合控制
2. **开源**完整训练流程，社区影响力大
3. 提出运动重定向方法，将人类 mocap 迁移到机器人

---

## 🤔 局限性

- 上半身动作受机器人自由度限制，表达能力有上限
- 复杂地形下全身协调性下降
- mocap 数据质量直接影响效果

---

## ❓ 面试高频问题

**Q: ExBody 和纯行走控制有什么区别？**
A: 纯行走只优化下半身稳定性，ExBody 同时追踪上半身参考动作，奖励函数包含跟踪误差项，需要协调上下半身不相互干扰。

**Q: 运动重定向怎么处理自由度不匹配？**
A: 通过优化问题将人类姿态投影到机器人可达关节空间，最小化关节角度差异，同时满足运动学约束。

**Q: 为什么这篇论文影响力大？**
A: 开源 + 真机验证 + 首次做到表达性全身控制，后续 ExBody2、HOVER 等都以此为基础。

---

## 📝 讨论记录

（暂无）
