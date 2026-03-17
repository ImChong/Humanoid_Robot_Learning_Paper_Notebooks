---
layout: paper
title: "VIGOR: Visual Goal-In-Context Inference for Unified Humanoid Fall Safety"
category: "Loco-Manipulation and WBC"
---

# VIGOR: Visual Goal-In-Context Inference for Unified Humanoid Fall Safety

> 📅 阅读日期: 待定
> 🏷️ 板块: Loco-Manipulation and Whole-Body-Control

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **arXiv** | [2602.16511](https://arxiv.org/abs/2602.16511) |
| **PDF** | [下载](https://arxiv.org/pdf/2602.16511) |
| **项目主页** | [vigor2026.github.io](https://vigor2026.github.io/) |
| **发布时间** | 2026年2月18日 |
| **实验平台** | Unitree G1 人形机器人 |

---

## 🎯 一句话总结

VIGOR 把人形机器人的跌倒安全（避免跌倒 + 缓冲冲击 + 站起恢复）统一成一个策略：用稀疏人类示范在平地和仿真复杂地形上训练特权 Teacher，再蒸馏为只用第一人称深度和本体感知的 Student，实现零样本跨地形泛化。

---

## 💬 讨论记录

> 此部分在阅读讨论后更新

---

## 📖 英文缩写速查

| 缩写 | 全称 | 简单解释 | 生活类比 |
|------|------|----------|----------|
| **VIGOR** | Visual Goal-In-Context Inference for Unified Humanoid Fall Safety | 本文系统名称缩写 | — |
| **RL** | Reinforcement Learning | 强化学习：通过奖惩反馈训练策略 | 训狗：做对了给零食，做错了没有 |
| **IL** | Imitation Learning | 模仿学习：从人类示范中直接学习行为 | 跟着老师临摹字帖，而不是自己试错摸索 |
| **Teacher-Student** | Teacher-Student Distillation | 知识蒸馏：用信息丰富的 Teacher 指导简化版 Student | 老师知道所有答案（用特权信息），学生只能靠考卷（真实传感器）学——Teacher 教会 Student 如何用有限信息做对题 |
| **Proprioception** | Proprioception | 本体感知：机器人自身的关节角度、速度、力矩等内部状态 | 闭上眼睛，你仍然知道自己的手臂在哪里——那就是本体感知 |
| **Egocentric** | Egocentric (Depth/Perception) | 以机器人自身视角为中心的感知（第一人称视角） | 戴着 VR 头盔看世界，视角随头转动 |
| **Zero-shot** | Zero-shot Generalization | 零样本泛化：在完全没见过的场景中直接工作，不需要微调 | 没在雪地开过车，但驾驶技术扎实，上去就能开 |
| **Sim-to-Real** | Simulation to Reality | 仿真训练迁移到真实机器人 | 游戏里练了一千小时，然后上真实赛场 |
| **DoF / DOF** | Degrees of Freedom | 自由度：可独立运动的轴数 | 人手腕有 3 个自由度：弯曲、侧偏、旋转 |
| **G1** | Unitree G1 | 宇树科技人形机器人平台 | — |
| **MoCap** | Motion Capture | 动作捕捉：用传感器记录人体运动 | 演员身上贴满反光球，摄像机记录轨迹，合成精确运动数据 |

---
