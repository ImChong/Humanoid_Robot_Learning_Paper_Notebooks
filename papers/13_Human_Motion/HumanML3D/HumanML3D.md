---
layout: paper
paper_order: 1
title: "Generating Diverse and Natural 3D Human Motions from Textual Descriptions (HumanML3D)"
category: "人类运动数据"
zhname: "从文本描述生成多样化且自然的 3D 人体运动"
---

# Generating Diverse and Natural 3D Human Motions from Textual Descriptions
**从文本描述生成多样化且自然的 3D 人体运动**

> 📅 阅读日期: 2026-04-21
> 🏷️ 板块: 13 Human Motion · 分类起步样例
> 🚧 本笔记已填充基本信息，深度技术细节待细化。

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **arXiv** | [2204.09419](https://arxiv.org/abs/2204.09419) (CVPR 2022) |
| **PDF** | [Download](https://arxiv.org/pdf/2204.09419.pdf) |
| **作者** | Chuan Guo, Shihao Zou, Xinxin Zuo, Sen Wang, Wei Ji, Xingyuan Li, Li Cheng |
| **机构** | University of Alberta / Simon Fraser University |
| **发布时间** | 2022-04 |
| **项目主页** | [HumanML3D GitHub](https://github.com/EricGuo5513/HumanML3D) |
| **代码** | [GitHub - EricGuo5513/HumanML3D](https://github.com/EricGuo5513/HumanML3D) |

---

## 🎯 一句话总结

> HumanML3D 是目前最主流的 3D 人体运动 - 文本数据集之一，提供了近 1.5 万个动作剪辑和 4.5 万条对应的自然语言描述，是研究文本生成动作（Text-to-Motion）的基石。

---

## 📌 核心数据集参数

| 维度 | 参数 | 备注 |
|------|------|------|
| **动作剪辑数** | 14,616 | 覆盖日常、运动、艺术等多种类别 |
| **文本描述数** | 44,970 | 每个视频平均 3 条文本描述 |
| **总时长** | 约 28.59 小时 | 规模领先 |
| **骨骼格式** | SMPL (22 关节点) | 工业标准 |
| **采样率** | 20 fps | 兼顾平滑度与计算效率 |
| **数据源** | AMASS + HumanAct12 | 整合了多源动捕数据 |

---

## ❓ HumanML3D 解决了什么行业痛点？

- **数据匮乏**：之前的 3D 运动数据集要么只有标签（如"走路"），要么缺乏高质量的自然语言对应。
- **标注粒度粗**：传统的动作分类（Action Recognition）无法描述"一个人慢慢地走并挥手"这种复杂的长句。
- **评测标准不统一**：HumanML3D 提供了一套完整的 Benchmark 和评测指标（如 R-Precision, FID, Diversity），统一了该领域的研究范式。

---

## 🔧 技术亮点

1. **多模态对齐**：通过人工标注和精心设计的过滤机制，确保了文本描述与动作细节的高度匹配。
2. **时序建模**：支持从 2 秒到 10 秒不等长度的动作生成，能够处理连续、流畅的动态过程。
3. **广泛的应用适配**：该数据集直接催生了后来的 MDM (Motion Diffusion Model) 等一系列基于扩散模型的生成算法。

---

## 🚶 典型任务

- **Text-to-Motion**：输入"A person steps forward and bows"，模型生成对应的 3D 骨骼轨迹。
- **Motion-to-Description**：输入一段 3D 动作，模型自动生成对应的自然语言描述。

---

## 🤖 工程价值

- **人形机器人示教**：通过文本直接生成参考轨迹，作为人形机器人模仿学习的输入源。
- **动作先验预训练**：在训练机器人底层控制器时，可以利用 HumanML3D 的大规模数据学习人类运动的先验分布。
- **游戏与影视**：自动化生成海量、多样的背景角色动作，显著降低动画制作成本。

---

## 🎤 面试高频问题 & 参考回答

1. **HumanML3D 的数据是如何生成的？**
   - 它通过对 AMASS 这种大规模纯动作数据进行精细的人工文本标注，并与已有的动作分类数据集（HumanAct12）进行清洗整合。
2. **为什么 SMPL 格式在 HumanML3D 中很重要？**
   - 因为 SMPL 是目前的标准人体模型，能够方便地重映射（Retargeting）到各种不同身形的人形机器人或虚拟角色上。

---

## 📎 附录

### A. 参考来源
- [arXiv:2204.09419](https://arxiv.org/abs/2204.09419)
- [GitHub: HumanML3D](https://github.com/EricGuo5513/HumanML3D)
