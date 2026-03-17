---
layout: paper
title: "Learning Humanoid End-Effector Control for Open-Vocabulary Visual Loco-Manipulation (HERO)"
category: "Loco-Manipulation and WBC"
---

# Learning Humanoid End-Effector Control for Open-Vocabulary Visual Loco-Manipulation (HERO)
**学习人形机器人末端执行器控制：面向开放词汇的视觉移动操作**

> 📅 阅读日期: 待定
> 🏷️ 板块: Loco-Manipulation and Whole-Body-Control

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **arXiv** | [2602.16705](https://arxiv.org/abs/2602.16705) |
| **PDF** | [下载](https://arxiv.org/pdf/2602.16705) |
| **项目主页** | [hero-humanoid.github.io](https://hero-humanoid.github.io/) |
| **发布时间** | 2026年2月18日 |

---

## 🎯 一句话总结

HERO 用残差感知末端执行器跟踪策略（IK + 神经正运动学 + 重规划）将末端跟踪误差降低 3.2 倍，再结合开放词汇大视觉模型，让人形机器人在真实咖啡馆、办公室等场景中能操作各种日常物品。

---

## 💬 讨论记录

> 此部分在阅读讨论后更新

---

## 📖 英文缩写速查

| 缩写 | 全称 | 简单解释 | 生活类比 |
|------|------|----------|----------|
| **HERO** | Humanoid End-effector control for Open-vocabulary loco-manipulation | 本文系统名称缩写 | — |
| **EE** | End-Effector | 末端执行器：机器人手臂的末端（手掌/夹爪） | 机器人的"手" |
| **IK** | Inverse Kinematics | 逆运动学：给定末端目标位置，反推各关节角度 | 知道手要放哪里，反推肩肘腕怎么弯 |
| **FK** | Forward Kinematics | 正运动学：给定关节角度，计算末端位置 | 知道每节手指弯了多少度，算出指尖在哪 |
| **RGB-D** | Red, Green, Blue + Depth | 带深度信息的彩色图像 | 普通照片 + 每个像素到相机的距离——让机器人"看到"3D 空间 |
| **RL** | Reinforcement Learning | 强化学习 | 训狗：做对了给零食，做错了没有 |
| **OOD** | Out-of-Distribution | 分布外：遇到训练中没见过的场景 | 在中国学车，突然到英国靠左行驶 |
| **Sim-to-Real** | Simulation to Reality | 仿真训练迁移到真实机器人 | 游戏里练了一千小时，然后上真实赛场 |
| **VLM** | Vision-Language Model | 视觉语言模型：同时理解图像和文字的大模型 | 能看图说话的 AI，你说"帮我拿那个红色的杯子"它看一眼就知道是哪个 |
| **DoF / DOF** | Degrees of Freedom | 自由度：机器人可独立运动的轴数 | 人手腕有 3 个自由度：弯曲、侧偏、旋转 |
| **G1** | Unitree G1 | 宇树科技人形机器人平台 | — |

---
