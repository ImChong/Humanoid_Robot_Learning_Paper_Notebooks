---
layout: paper
paper_order: 34
title: "Perceptive Humanoid Parkour: Chaining Dynamic Human Skills via Motion Matching"
zhname: "Perceptive Humanoid Parkour：通过动作匹配串联动态人类技能"
category: "Loco-Manipulation and WBC"
---

# Perceptive Humanoid Parkour: Chaining Dynamic Human Skills via Motion Matching
**PHP：让人形机器人用“动作匹配 + 感知决策”跨越复杂障碍的长程跑酷框架**

> 📅 阅读日期: 2026-04-28  
> 🏷️ 板块: Loco-Manipulation and Whole-Body-Control · 高动态跑酷

---

## 📋 基本信息

| 项目 | 链接 |
|---|---|
| arXiv | [2602.15827](https://arxiv.org/abs/2602.15827) |
| HTML | [在线阅读](https://arxiv.org/html/2602.15827) |
| PDF | [下载](https://arxiv.org/pdf/2602.15827) |
| DOI | [10.48550/arXiv.2602.15827](https://doi.org/10.48550/arXiv.2602.15827) |
| 代码 | 暂未公开（截至 2026-04-28） |
| 实验平台 | Unitree G1 |
| 提交日期 | 2026-02-17 |

**作者**：Zhen Wu, Xiaoyu Huang, Lujie Yang, Yuanhang Zhang, Koushil Sreenath, Xi Chen, Pieter Abbeel, Rocky Duan, Angjoo Kanazawa, Carmelo Sferrazza, Guanya Shi, C. Karen Liu

---

## 🎯 一句话总结

这篇论文提出 **Perceptive Humanoid Parkour (PHP)**：先用动作匹配（motion matching）把重定向后的人类原子技能拼成长时程运动轨迹，再训练 tracking expert 并蒸馏成一个基于深度视觉的多技能学生策略，让 Unitree G1 只靠机载深度与速度命令，就能在不同障碍之间自动决策“跨、爬、撑越、滚下”等动作链。

---

## ❓要解决的问题

传统人形跑酷方案常见瓶颈：
- 技能孤岛：单技能强，但很难长程组合；
- 轨迹僵硬：动作过渡不自然，难以保持“人类风格”动态性；
- 感知闭环不足：面对实时变化障碍时，难以在线改动作。

PHP 的目标是把这三点同时解决：
1. **长程技能组合**（skill chaining）；
2. **动态动作表达**（human-like agility）；
3. **感知驱动决策**（perception-based adaptation）。

---

## 🔧 方法拆解

### 1) Motion Matching 负责“拼动作”
将人类动态动作库中的原子技能映射到特征空间，用近邻检索方式拼接成连续 kinematic 目标轨迹。  
关键收益：
- 动作过渡更自然；
- 能针对障碍几何快速换技能段；
- 不必每种组合都重新手工设计状态机。

### 2) Motion-Tracking RL Experts 负责“学跟踪”
对组合轨迹训练多个 tracking expert，使机器人在动力学约束下稳定复现目标动作。

### 3) DAgger + RL 蒸馏成单一学生策略
将专家行为蒸馏到一个统一的多技能 student policy，输入为：
- 机载深度感知；
- 离散二维速度命令。  
输出为全身控制动作，实现端到端执行。

### 4) 感知与技能链联合决策
在闭环执行时，策略会根据前方障碍的高度/形状与相对位置，切换“迈过、爬上、撑越、滚下”等动作路径，而不是固定脚本。

---

## 🧪 论文结果要点（按原文摘要）

- 在 Unitree G1 上完成多种高动态跑酷行为；
- 报告可攀爬至 **1.25m** 高障碍（约机器人身高 **96%**）；
- 可执行长程多障碍穿越，并对实时障碍扰动进行闭环适应。  

这些结果说明：PHP 更像“动作组合系统 + 感知控制策略”的统一框架，而非单一 trick。

---

## 💡 阅读备注（后续复现关注点）

1. 若后续代码公开，最值得先复现的是 motion matching 特征设计（决定拼接质量上限）。
2. 多 expert 到单 student 的蒸馏调度（DAgger 采样比例、在线纠偏频率）会直接影响真实机器人稳定性。
3. 障碍课程的分布设计（高度、间距、组合顺序）是长时程泛化的关键。

---

## 🔗 参考

```bibtex
@article{wu2026perceptive,
  title={Perceptive Humanoid Parkour: Chaining Dynamic Human Skills via Motion Matching},
  author={Wu, Zhen and Huang, Xiaoyu and Yang, Lujie and Zhang, Yuanhang and Sreenath, Koushil and Chen, Xi and Abbeel, Pieter and Duan, Rocky and Kanazawa, Angjoo and Sferrazza, Carmelo and Shi, Guanya and Liu, C. Karen},
  journal={arXiv preprint arXiv:2602.15827},
  year={2026}
}
```
