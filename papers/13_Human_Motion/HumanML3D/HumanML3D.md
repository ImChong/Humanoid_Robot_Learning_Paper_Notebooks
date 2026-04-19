---
layout: paper
title: "HumanML3D: 3D Human Motion-Language Dataset"
category: "人体运动 Human Motion"
zhname: "HumanML3D：3D 人体运动 - 语言数据集"
---

# HumanML3D: 3D Human Motion-Language Dataset
**HumanML3D：3D 人体运动 - 语言数据集**

> 📅 阅读日期: 待读
> 🏷️ 板块: 13_Human_Motion 首篇骨架
> 🚧 本笔记为骨架，基本信息待人工核对。

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **arXiv** | 🚧 待核对（候选：2204.09419） |
| **PDF** | 🚧 |
| **作者** | 🚧 待核对（Chuan Guo 等） |
| **机构** | 🚧 待核对（University of Alberta 等） |
| **发布时间** | 2022（CVPR 2022） |
| **会议** | CVPR 2022（🚧 待核对） |
| **项目主页** | 🚧 |
| **代码 / 数据** | 🚧 |

---

## 🎯 一句话总结

> 🚧 待补。推测方向（以论文为准）：把 AMASS 等 mocap 数据 + 重新众包的**自然语言描述**配对，得到第一个大规模 3D 人体动作 - 语言数据集（约 14k 动作、44k 描述），为后续 text-to-motion 工作（MotionDiffuse / MDM / T2M-GPT）打底。

---

## 📌 英文缩写速查

| 缩写 | 全称 | 简单解释 |
|------|------|----------|
| **AMASS** | Archive of Motion Capture as Surface Shapes | 一个统一表示的大型 mocap 集合 |
| **SMPL** | Skinned Multi-Person Linear model | 标准化的人体参数化模型 |
| **T2M** | Text-to-Motion | 文本生成动作任务 |
| 🚧 | | |

---

## ❓ HumanML3D 要解决什么问题？

> 🚧 待补。可能方向：
> - **数据匮乏**：text-to-motion 任务此前缺少高质量、规模够大、语言描述自然的数据。
> - **统一表示**：把多个 mocap 子集（CMU / KIT / HumanAct12 等）统一到 SMPL 参数下。
> - **评测基准**：提供标准 train/val/test 划分及评价指标（FID-motion、R-precision）。

---

## 🔧 数据组成

> 🚧 待补：读完论文/项目页后填充。
>
> 预期章节：
> 1. **来源**：从 AMASS / HumanAct12 选取动作。
> 2. **标注流程**：每段动作由 Amazon MTurk 工人写 3 条自然语言描述。
> 3. **统一处理**：mirror augmentation、20 fps 重采样、SMPL 表示。
> 4. **划分**：~14k motion / ~44k text / 标准 split。

---

## 🚶 典型用途

> 🚧 待补（典型下游：MotionDiffuse、MDM、T2M-GPT 等 text-to-motion 模型）。

---

## 🤖 工程价值

> 🚧 待补。意义：13_Human_Motion 分类首篇骨架；几乎所有近年 text-to-motion 论文都拿 HumanML3D 当主基准，理解它有助于读 motion generation 方向论文。

---

## 📁 数据 / 代码

> 🚧 待核对：
> - 数据下载链接：🚧
> - 评估脚本：🚧
> - SMPL 模型授权：🚧（需注册 SMPL 官网）

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
| 12_Physics-Based_Animation | 上游 mocap 数据可被两边共用 |
| Diffusion Policy / MDM | text-to-motion 模型的标准训练集 |
| ExBody / OmniH2O | 把 mocap 动作转成人形机器人参考动作的上游来源之一 |

### B. 参考来源

- 🚧 待核对 arXiv / 主页 / 数据下载
- 交叉验证：[awesome-humanoid-robot-learning](https://github.com/YanjieZe/awesome-humanoid-robot-learning) Human Motion section
