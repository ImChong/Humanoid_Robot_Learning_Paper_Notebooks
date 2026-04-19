---
layout: paper
title: "Extreme Parkour with Legged Robots"
category: "行走 Locomotion"
zhname: "腿式机器人的极限跑酷"
---

# Extreme Parkour with Legged Robots
**腿式机器人的极限跑酷**

> 📅 阅读日期: 待读
> 🏷️ 板块: 04_Locomotion 扩展骨架
> 🚧 本笔记为骨架，基本信息待人工核对。

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **arXiv** | 🚧 待核对（候选：2309.14341） |
| **PDF** | 🚧 |
| **作者** | 🚧 待核对（Xuxin Cheng, Kexin Shi 等） |
| **机构** | 🚧 待核对（CMU） |
| **发布时间** | 2023（🚧 待核对月份） |
| **会议** | 🚧（ICRA 2024 候选） |
| **项目主页** | 🚧 |
| **代码** | 🚧 |

---

## 🎯 一句话总结

> 🚧 待补。推测方向：让四足机器人凭**单个前视深度相机**完成跳高、跳远、攀爬栏杆、过窄缝等极限跑酷动作，teacher-student 蒸馏 + 地形 curriculum。

---

## 📌 英文缩写速查

| 缩写 | 全称 | 简单解释 |
|------|------|----------|
| **Parkour** | 跑酷 | 连续跨越障碍的高动态运动 |
| **Teacher-Student** | 教师 - 学生 | 特权教师训练后蒸馏给只看 onboard 传感的学生策略 |
| 🚧 | | |

---

## ❓ Extreme Parkour 要解决什么问题？

> 🚧 待补。可能方向：
> - 商用机器人"走平路"远远不够，城市环境充满台阶、窄缝、栏杆。
> - 依赖外部感知（Mocap、地图）不可部署，要靠 onboard depth。
> - 复杂地形下 RL 的 reward shaping 与 curriculum 难度。

---

## 🔧 方法详解

> 🚧 待补：读完论文后填充。
>
> 预期主线：
> 1. 仿真地形生成：跳跃、攀爬、窄缝等地形 prototypes。
> 2. Privileged teacher：可看地形真值 + 机器人状态。
> 3. Student：前视 depth + proprioception → action。
> 4. 高度驱动的 reward shaping。

---

## 🚶 具体实例

> 🚧 待补（典型：0.8m 跳高、2m 跳远、过 0.3m 窄缝、爬 0.5m 高栏杆）。

---

## 🤖 工程价值

> 🚧 待补。意义：把腿式机器人运动从平地推到"极限"的代表作，后续双足/人形跑酷论文多以其为范式参考。

---

## 📁 源码对照

> 🚧 开源代码待核对（legged_gym 变体）。

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
| Learning_to_Walk_in_Minutes | 同用 Isaac Gym 大规模并行仿真 |
| ANYmal Parkour | 同期四足跑酷工作，策略侧重不同 |
| 09_Sim-to-Real | depth-only student 是 sim-to-real 典型案例 |

### B. 参考来源

- 🚧 待核对 arXiv / 主页 / 代码
