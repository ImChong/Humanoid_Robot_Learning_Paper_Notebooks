---
layout: paper
paper_order: 38
title: "EgoHumanoid: Unlocking In-the-Wild Loco-Manipulation with Robot-Free Egocentric Demonstration"
zhname: "EgoHumanoid：用无机器人自我中心示范解锁野外环境中的移动操作"
category: "Loco-Manipulation and WBC"
---

# EgoHumanoid: Unlocking In-the-Wild Loco-Manipulation with Robot-Free Egocentric Demonstration
**EgoHumanoid：以人类自我视角示范+双对齐管线，让人形机器人用极少机器人数据完成野外移动操作**

> 📅 阅读日期: 2026-04-30  
> 🏷️ 板块: Loco-Manipulation and Whole-Body-Control · 自我中心示范学习

---

## 📋 基本信息

| 项目 | 链接 |
|---|---|
| arXiv | [2602.10106](https://arxiv.org/abs/2602.10106) |
| HTML | [在线阅读](https://arxiv.org/html/2602.10106v1) |
| PDF | [下载](https://arxiv.org/pdf/2602.10106) |
| 项目主页 | [opendrivelab.com/EgoHumanoid](https://opendrivelab.com/EgoHumanoid/) |
| 源码 | [OpenDriveLab/EgoHumanoid](https://github.com/OpenDriveLab/EgoHumanoid) |
| 提交日期 | 2026-02-10 |

**作者**：Modi Shi, Shijia Peng, Jin Chen 等（OpenDriveLab）

---

## 🎯 一句话总结

EgoHumanoid 是首个利用"无机器人"自我中心人类示范来训练全身移动操作策略的框架——通过**视角对齐（View Alignment）+ 动作对齐（Action Alignment）**，将大量廉价人类 egocentric 数据与少量机器人遥操作数据共同训练 VLA 策略，在未见过的环境中比纯机器人数据基线提升 **+51%**。

---

## 📌 英文缩写速查

| 缩写 | 全称 | 简单解释 |
|---|---|---|
| VLA | Vision-Language-Action | 视觉-语言-动作模型 |
| Loco-Manipulation | Locomotion + Manipulation | 移动+操作，边走边抓 |
| Egocentric Demo | Egocentric Demonstration | 人类佩戴头戴设备录制的第一人称示范 |
| View Alignment | - | 减小人类与机器人相机视角差异的对齐方法 |
| Action Alignment | - | 将人类动作映射到机器人运动学可行空间的方法 |
| OpenPI | Open Physical Intelligence | Physical Intelligence 开源的 VLA 基础模型 |

---

## ❓ 论文要解决什么问题？

移动操作（Loco-Manipulation）需要同时控制行走和双臂——数据采集成本极高：遥操作系统昂贵、训练人员需要熟练操作，且采集环境单一，泛化到"野外"（室外、不同地面、陌生房间）效果差。

人类有大量廉价的自我视角视频（戴 VR 头显就能录），但有**两个鸿沟**：
1. **视角鸿沟**：人站立时相机高约 1.7m，机器人头部约 1.3m，且俯仰角不同。
2. **动作鸿沟**：人手臂/腿部比例与机器人不同，人的运动不能直接映射为机器人关节指令。

EgoHumanoid 的核心问题是：**如何让廉价的人类 egocentric 示范真正有效地迁移到人形机器人？**

---

## 🔧 方法拆解

### 整体框架

```
人类戴 PICO VR 头显录制示范（室内室外各种任务）
         ↓
  ① 视角对齐（View Alignment）
     - 用相机内外参将人类视角图像重投影到机器人头部视角
     - 消除高度差和俯仰角差异
         ↓
  ② 动作对齐（Action Alignment）
     - PICO 全身追踪 → 提取关键点轨迹
     - 运动学可行性约束 → 映射为 G1 机器人关节角度
     - 统一 action space（不依赖人类/机器人差异）
         ↓
  混合数据集 = 人类 egocentric demo + 少量机器人遥操作数据
         ↓
  共同训练 OpenPI VLA 策略（视觉+语言→动作）
         ↓
  Unitree G1 实机部署（4 项室内外任务）
```

### 视角对齐（View Alignment）

- 人类 ZED 相机录制的图像通过**几何重投影**，变换到与 G1 头部相机近似等效的视角。
- 关键是校准人类采集时的相机标定参数，使重投影后的像素分布匹配机器人实际观测。

### 动作对齐（Action Alignment）

- PICO SDK 提供全身关节追踪（头、双手、双脚）。
- 以机器人根节点为参考，将人类肢体端点轨迹转化为末端执行器目标，再通过逆运动学求解 G1 关节指令。
- 对非运动学可行的姿态做截断过滤，保证训练数据质量。

### 与 OpenPI 联合训练

- 基础策略采用 Physical Intelligence 开源的 OpenPI VLA 模型。
- 训练时混合：大量人类 egocentric demo（低成本，覆盖多样环境）+ 少量机器人遥操作 demo（保证精度）。
- 语言条件指令用于指定任务类型。

---

## 📊 主要实验结果

| 方法 | 成功率（4 任务平均）| 未见环境 |
|---|---|---|
| 纯机器人遥操作数据 | 基线 | 低 |
| **EgoHumanoid（人类 + 机器人）** | **基线 +51%** | 显著提升 |

- **任务**：4 项室内外 loco-manipulation，含室内取物、户外开门等。
- **机器人**：Unitree G1 人形机器人。
- **关键发现**：人类 egocentric 数据对**未见环境泛化**帮助最大，而不只是提升训练环境性能。

---

## 🏷️ 关键词

`Egocentric Demonstration` · `Loco-Manipulation` · `Vision-Language-Action` · `View Alignment` · `Action Alignment` · `Unitree G1` · `OpenDriveLab` · `Robot-Free Data Collection`
