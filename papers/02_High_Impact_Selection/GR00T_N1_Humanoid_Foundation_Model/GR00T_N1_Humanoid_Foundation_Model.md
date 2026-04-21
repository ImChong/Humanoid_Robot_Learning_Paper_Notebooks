---
layout: paper
paper_order: 1
title: "GR00T N1: An Open Foundation Model for Generalist Humanoid Robots"
category: "高影响力工作"
zhname: "GR00T N1：面向通用人形机器人的开放基础模型"
---

# GR00T N1: An Open Foundation Model for Generalist Humanoid Robots
**GR00T N1：面向通用人形机器人的开放基础模型**

> 📅 阅读日期: 2026-04-21
> 🏷️ 板块: 02 High Impact · 基础模型
> 🚧 本笔记已填充基本信息，深度技术细节待细化。

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **arXiv** | [2503.14734](https://arxiv.org/abs/2503.14734) |
| **PDF** | [Download](https://arxiv.org/pdf/2503.14734.pdf) |
| **作者** | NVIDIA Project GR00T Team (Linxi Fan, Yuke Zhu 等) |
| **机构** | NVIDIA |
| **发布时间** | 2025-03 |
| **项目主页** | [NVIDIA GR00T Website](https://www.nvidia.com/en-us/geforce/news/project-gr00t-humanoid-robots/) |
| **代码 / 模型** | [Hugging Face - GR00T-N1](https://huggingface.co/nvidia/GR00T-N1-2B) |

---

## 🎯 一句话总结

> GR00T N1 是 NVIDIA 发布的业界领先的开放权重人形机器人基础模型，采用双系统 VLA 架构（慢速推理 + 快速执行），支持跨多种硬件平台的通用任务执行。

---

## 📌 英文缩写速查

| 缩写 | 全称 | 简单解释 |
|------|------|----------|
| VLA | Vision-Language-Action | 视觉 - 语言 - 动作模型，端到端学习从图像到行为的映射 |
| DiT | Diffusion Transformer | 扩散 Transformer，GR00T 用于生成高频动作的核心模块 |
| TOPS | Tera Operations Per Second | 每秒万亿次运算，衡量 AI 算力的指标 |

---

## ❓ GR00T N1 要解决什么问题？

- **泛化性缺失**：传统的机器人模型多为"一机一用"或"一任务一用"，难以适应多样化的现实场景和不同的机器人形态。
- **高频感知与低频决策的矛盾**：复杂的逻辑推理（System 2）需要时间，而物理平衡控制（System 1）必须实时（>100Hz）。如何将两者有机结合？
- **数据孤岛**：如何利用异构的数据源（人类视频、不同机器人的轨迹、仿真数据）训练出一个统一的通用模型？

---

## 🔧 方法详解（架构设计）

1. **双系统 VLA 架构 (Dual-System)**：
   - **System 2 (慢速推理层)**：基于 **NVIDIA Eagle-2** 的视觉语言模型，运行在 **10Hz**。负责理解语言指令、分析视觉场景并输出高层语义表征。
   - **System 1 (快速执行层)**：基于 **Diffusion Transformer (DiT)**，运行在 **120Hz**。接收 System 2 的潜变量输入，通过流匹配（Flow-matching）快速生成精细的关节动作指令。
2. **数据金字塔 (Data Pyramid)**：
   - 融合了人类第一视角视频、真实的机器人遥操作轨迹（如 Open X-Embodiment）以及在 Isaac Lab 中生成的大规模合成数据。
3. **跨具身训练 (Cross-Embodiment)**：
   - 模型设计之初就考虑了对不同自由度、不同高度的人形机器人的兼容性（如 Fourier GR-1, 1X 等）。

---

## 🚶 具体实例

- **多任务执行**：在不进行任务特定微调的情况下，机器人可以根据指令"去厨房拿一个苹果并递给我"，自动完成导航、识别、精准抓取和交付。
- **跨平台适配**：GR00T N1 的同一个权重可以部署在两台完全不同型号的人形机器人上，并表现出一致的任务理解能力。

---

## 🤖 工程价值

- **开源生态里程碑**：NVIDIA 开放 2B 规模的模型权重，极大地降低了全球研究者进入人形基础模型领域的门槛。
- **算力示范**：展示了 NVIDIA GPU (如 Jetson Orin) 在板载运行复杂 VLA 模型方面的强大实力。
- **物理 AI 标杆**：将生成式 AI（DiT）与经典控制论深度结合，指明了具身智能的演进方向。

---

## 🎤 面试高频问题 & 参考回答

1. **GR00T N1 的 System 1 和 System 2 分别负责什么？**
   - System 2 负责"想"（感知和逻辑推理），System 1 负责"做"（高频且平滑的动作生成）。
2. **为什么在 System 1 中使用 Diffusion Transformer？**
   - 相比于 MLP 或简单的 Transformer，DiT 能够建模更复杂的多模态动作分布，生成的轨迹更自然且鲁棒。

---

## 📎 附录

### A. 参考来源
- [arXiv:2503.14734](https://arxiv.org/abs/2503.14734)
- [NVIDIA Blog on Project GR00T](https://blogs.nvidia.com/blog/gr00t-humanoid-robot-ai/)
