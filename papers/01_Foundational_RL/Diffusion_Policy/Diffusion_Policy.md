---
layout: paper
paper_order: 10
title: "Diffusion Policy: Visuomotor Policy Learning via Action Diffusion"
category: "基础强化学习"
zhname: "Diffusion Policy：基于动作扩散的视觉运动策略学习"
---

# Diffusion Policy: Visuomotor Policy Learning via Action Diffusion
**Diffusion Policy：基于动作扩散的视觉运动策略学习**

> 📅 阅读日期: 2026-04-21
> 🏷️ 板块: 扩散+控制主线起点
> 🚧 本笔记已填充基本信息，深度技术细节待细化。

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **arXiv** | [2303.04137](https://arxiv.org/abs/2303.04137) |
| **PDF** | [Download](https://arxiv.org/pdf/2303.04137.pdf) |
| **作者** | Cheng Chi, Siyuan Feng, Yilun Du, Zhenjia Xu, Eric Cousineau, Benjamin Burchfiel, Shuran Song |
| **机构** | Columbia / MIT / Toyota Research Institute |
| **发布时间** | 2023-03 (arXiv), RSS 2023 |
| **项目主页** | [Diffusion Policy Website](https://diffusion-policy.cs.columbia.edu/) |
| **代码** | [GitHub - columbia-ai-robotics/diffusion_policy](https://github.com/columbia-ai-robotics/diffusion_policy) |

---

## 🎯 一句话总结

> Diffusion Policy 将机器人策略表示为条件去噪扩散过程，将动作生成从"单步回归"升级为"多步轨迹生成"，从而完美处理模仿学习中的多模态分布挑战。

---

## 📌 英文缩写速查

| 缩写 | 全称 | 简单解释 |
|------|------|----------|
| DDPM | Denoising Diffusion Probabilistic Model | 去噪扩散概率模型 |
| DDIM | Denoising Diffusion Implicit Model | 非马尔可夫采样的加速版本，大幅减少推理步数 |
| FiLM | Feature-wise Linear Modulation | 用于视觉特征与扩散噪声融合的调制机制 |
| RHC | Receding Horizon Control | 后退水平控制：预测序列，仅执行前段，滚动规划 |

---

## ❓ Diffusion Policy 要解决什么问题？

- **多模态挑战 (Multimodality)**：传统 BC（Behavior Cloning）使用 MLP 直接回归动作，在遇到人类演示中有多种解法时（例如从左绕开或从右绕开障碍），会因均方误差（MSE）损失而产生"平均动作"，导致机器人撞上障碍。
- **高维连续空间建模**：传统方案如 GMM 或 VAE 在高维复杂动作序列上的表现力不足。
- **训练稳定性**：相比于 GAN 或 EBM（能量模型），扩散模型的训练过程更加稳定且可扩展。

---

## 🔧 方法详解

1. **Action Chunking**：不再预测单步动作，而是预测一个长度为 $H$ 的动作序列。
2. **Conditional Denoising**：
   - 输入：当前视觉观测 $O$（ResNet/ViT 提取）和包含高斯噪声的动作序列 $A_k$。
   - 目标：通过网络 $f_\theta$ 预测噪声 $\epsilon$，逐步剔除噪声还原真实动作。
3. **网络结构**：
   - **CNN-based**：使用 1D 时序卷积，推理延迟低。
   - **Transformer-based**：擅长处理长序列，能建模更复杂的交互。
4. **推理优化**：通过 DDIM 采样，将训练时的数百步扩散压缩至推理时的 10-20 步。

---

## 🚶 具体实例

在一个"抓取方块"的任务中：
- **观测**：双目摄像头画面 + 机械臂关节角。
- **去噪**：模型从随机轨迹开始，经过 10 步迭代，逐渐形成一条平滑的抓取路径。
- **执行**：预测未来 16 步，实际执行前 8 步，随后接收新观测再次预测。

---

## 🤖 工程价值

- **行业标准**：已成为现代端到端模仿学习（Imitation Learning）的事实标准。
- **鲁棒性**：在 15 个复杂操作任务中，成功率平均提升 46.9%。
- **通用性**：支持多种传感器输入（RGB、Depth、Proprioception），并能轻松扩展到双臂甚至全身控制。

---

## 📁 MimicKit 源码对照

> ❌ MimicKit 目前主要面向 RL 和运动模仿，尚未集成标准的视觉扩散策略。

---

## 🎤 面试高频问题 & 参考回答

1. **为什么扩散模型擅长处理多模态？**
   - 因为它不直接预测均值，而是学习梯度的得分函数（Score function），能收敛到分布的多个局部极大值。
2. **预测噪声还是预测动作？**
   - 实践中预测噪声 $\epsilon$ 通常更稳定。
3. **Diffusion Policy vs ACT (Action Chunking Transformer)？**
   - ACT 侧重于 CVAE 框架，而 Diffusion Policy 利用扩散过程提供了更强的表达能力和训练稳定性。

---

## 📎 附录

### A. 与路线图的关系

| 论文 | 关系 |
|------|------|
| **Diffusion Policy (2023)** | 扩散 + 控制主线的**起点** |
| BeyondMimic (2025) | 扩散控制在人形机器人全身动态运动上的突破性应用 |

### B. 参考来源

- [arXiv:2303.04137](https://arxiv.org/abs/2303.04137)
- [Project Website](https://diffusion-policy.cs.columbia.edu/)
