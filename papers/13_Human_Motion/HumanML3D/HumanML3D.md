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
> 🧭 状态: 快速扩充版；按 CVPR 2022 论文、项目页和官方实现整理。

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **arXiv** | [2204.09419](https://arxiv.org/abs/2204.09419) (CVPR 2022) |
| **PDF** | [Download](https://arxiv.org/pdf/2204.09419.pdf) |
| **作者** | Chuan Guo, Shihao Zou, Xinxin Zuo, Sen Wang, Wei Ji, Xingyuan Li, Li Cheng |
| **机构** | University of Alberta / Simon Fraser University |
| **发布时间** | 2022-04 |
| **项目主页** | [Text-to-Motion Project](https://ericguo5513.github.io/text-to-motion/) |
| **代码** | [EricGuo5513/text-to-motion](https://github.com/EricGuo5513/text-to-motion) |

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

## 🔧 方法详解

### 1. 为什么需要 HumanML3D

在 HumanML3D 之前，文本到动作生成主要受限于数据规模和标注粒度。KIT Motion-Language 规模较小，动作以 locomotion 为主，文本形式也比较简单。HumanML3D 的目标是构建一个更大、更自然、覆盖动作更广的 3D human motion-language 数据集，让模型能从自然语言生成多样、长度可变且语义匹配的动作。

### 2. 数据来源与清洗

HumanML3D 整合 AMASS 和 HumanAct12 等动捕来源，覆盖日常动作、运动、杂技和舞蹈等类别。论文将动作统一到默认人体骨架模板，调整朝向，统一采样率到 20 FPS，并把过长动作裁剪到 10 秒以内。

这个处理对机器人很重要：如果未来要把 HumanML3D 作为 motion prior 或 retargeting 数据源，统一骨架、朝向、采样率和长度是后续训练稳定性的基础。

### 3. 文本标注

论文通过 Amazon Mechanical Turk 采集英文描述，每段 motion clip 通常有多条文本描述。标注要求不是简单动作标签，而是自然语言句子，能描述方向、速度、动作顺序和风格。例如"先站起来，逆时针绕圈走，然后躺下"这类长句比单词标签更接近真实指令。

最终数据集包含 14,616 段动作、44,970 条文本描述、5,371 个不同词，总运动时长约 28.59 小时。

### 4. Text2Length + Text2Motion

论文方法分两阶段：

1. **Text2Length**：根据文本条件采样动作长度。这样同一句文本可以生成不同持续时间的合理动作，而不是固定长度输出。
2. **Text2Motion**：使用 temporal VAE 生成动作。模型不是直接在原始 pose 序列上建模，而是引入 motion snippet code，捕捉局部时间片段中的语义运动上下文。

这个设计回应了 text-to-motion 的三个难点：长度可变、一句多解、文本复杂度高。

### 5. 评测指标

HumanML3D 后续成为主流 benchmark，很大原因是它提供了稳定评测口径：

- **R-Precision**：文本和生成动作在检索空间里是否匹配；
- **FID**：生成动作分布与真实动作分布距离；
- **Diversity**：生成结果是否有足够多样性；
- **Multimodality**：同一文本下是否能生成多种合理动作；
- **MultiModal Distance**：文本动作语义对齐距离。

这些指标后来被 MDM、T2M-GPT、MotionDiffuse、MoMask 等大量工作沿用。

---

## 🧠 技术亮点

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

## 📁 源码对照

官方 `text-to-motion` 仓库可以按三块阅读：

| 模块 | 关注点 |
|------|--------|
| dataset / data preparation | HumanML3D 和 KIT-ML 的加载、文本 token、motion 表示 |
| model | text encoder、length estimator、temporal VAE / motion generator |
| evaluation | R-Precision、FID、Diversity、Multimodality 等指标 |

如果把 HumanML3D 用在人形机器人上，还需要额外做 retargeting：SMPL/人体骨架动作不能直接作为 H1、G1 或 Digit 的关节目标，需要转换到机器人骨架，并处理接触、足滑、关节限位和动力学可行性。

---

## 💬 讨论记录

- HumanML3D 对机器人不是"可直接执行的数据集"，而是语言到人体动作先验的来源。
- 机器人使用时最关键的中间层是 retargeting 和 physics filtering。没有这层，文本生成的动作可能视觉上合理但动力学不可行。
- 后续 text-to-humanoid 工作往往会把 HumanML3D 与 AMASS、BABEL、Motion-X 等数据一起使用，训练更大的 motion prior。

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
- [CVPR OpenAccess PDF](https://openaccess.thecvf.com/content/CVPR2022/papers/Guo_Generating_Diverse_and_Natural_3D_Human_Motions_From_Text_CVPR_2022_paper.pdf)
- [Project Page](https://ericguo5513.github.io/text-to-motion/)
- [GitHub: text-to-motion](https://github.com/EricGuo5513/text-to-motion)
