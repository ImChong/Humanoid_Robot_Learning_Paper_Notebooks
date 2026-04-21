---
layout: paper
paper_order: 11
title: "Universal Humanoid Motion Representations for Physics-Based Control (PULSE)"
category: "基础强化学习"
zhname: "PULSE：物理可行的通用潜在技能提取"
---

# PULSE: Universal Humanoid Motion Representations for Physics-Based Control
**PULSE：物理可行的通用潜在技能提取**

> 📅 阅读日期: 2026-04-21
> 🏷️ 板块: 技能组合主线 · ASE → CALM → **PULSE**
> 🚧 本笔记已填充基本信息，深度技术细节待细化。

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **arXiv** | [2310.04582](https://arxiv.org/abs/2310.04582) (ICLR 2024 Spotlight) |
| **PDF** | [Download](https://arxiv.org/pdf/2310.04582.pdf) |
| **作者** | Zhengyi Luo, Jinkun Cao, Alexander Winkler, Jessica Hodgins, Weipeng Xu, Kris Kitani |
| **机构** | CMU / Meta Reality Labs |
| **发布时间** | 2023-10 (arXiv), 2024-05 (ICLR) |
| **项目主页** | [PULSE Project Page](https://zhengyiluo.github.io/projects/pulse/) |
| **代码** | [GitHub - ZhengyiLuo/PULSE](https://github.com/ZhengyiLuo/PULSE) |

---

## 🎯 一句话总结

> PULSE 通过 Variational Information Bottleneck (VIB) 将大规模 AMASS 动作集压缩进一个 32 维的通用物理潜空间，使下游任务能以即插即用的方式调用多样化的人形技能。

---

## 📌 英文缩写速查

| 缩写 | 全称 | 简单解释 |
|------|------|----------|
| PULSE | Physics-based Universal motion Latent SpacE | 物理通用的运动潜空间 |
| VIB | Variational Information Bottleneck | 变分信息瓶颈，用于压缩和提取核心特征 |
| AMASS | Archive of Motion Capture as Surface Shapes | 大规模人体动作捕捉数据集 |

---

## ❓ PULSE 要解决什么问题？

PULSE 旨在构建人形控制的"基础模型"：
- **覆盖率不足**：之前的 ASE/CALM 虽然有 latent skill，但通常针对特定任务或较小数据集，难以覆盖人类全谱系动作。
- **通用性挑战**：如何将 AMASS 这种数万个动作片段的规模（覆盖人类 99.8% 的动作）压进一个统一且可控的潜空间？
- **下游适配**：如何让 high-level 策略在无需重新训练底层控制器的前提下，直接利用这个潜空间完成新任务？

---

## 🔧 方法详解

PULSE 采用两阶段学习框架：
1. **第一阶段：大规模模仿 (Large-scale Imitation)**
   - 训练一个高保真运动模仿器，学习跟踪 AMASS 数据集中极其多样且无结构的动作。
2. **第二阶段：技能蒸馏与潜空间构建 (Distillation via VIB)**
   - 使用变分信息瓶颈将模仿器的技能蒸馏到一个概率潜空间。
   - 引入 **Proprioceptive Prior**（本体感受先验）：学习一个以当前状态（姿态、速度）为条件的先验分布，确保生成的动作在长时间序列下依然物理可行且稳定。
3. **下游任务适配**
   - High-level 策略只需在 32 维潜空间中进行采样/优化，即可驱动机器人执行地形导航、击打物体等任务。

---

## 🚶 具体实例

通过 PULSE，用户可以：
- 从 latent space 中随机采样，机器人会自发产生连贯的人类动作（如转圈、挥手、小跑）。
- 给定一个简单的奖励函数（如"击打目标"），策略能快速学会在 latent 中寻找合适的动作序列。

---

## 🤖 工程价值

- **学术地位**：ICLR 2024 Spotlight，是人形机器人运动表示领域的重要里程碑。
- **扩展性**：其潜空间设计思想影响了后续如 OmniH2O 等多项全身控制与遥操作工作。
- **效率**：显著提升了复杂任务的训练速度，因为智能体不再从零开始学习"怎么动"，而是学习"何时用什么技能"。

---

## 📁 MimicKit 源码对照

> 🚧 待确认。ASE 和 CALM 在 MimicKit 中有体现，PULSE 的官方实现独立于 GitHub。

---

## 🎤 面试高频问题 & 参考回答

1. **PULSE 与 ASE/CALM 的核心区别？**
   - ASE 是无方向的随机探索，CALM 增加了方向性条件，而 PULSE 追求的是覆盖全量数据的通用表示（Universal coverage）并引入了本体感受先验。
2. **为什么 PULSE 需要 VIB？**
   - VIB 能有效平衡潜空间的表达能力与压缩度，防止过拟合到特定动作片段，增强泛化性。

---

## 📎 附录

### A. 与路线图其他论文的关联

| 论文 | 关系 |
|------|------|
| ASE | 提供对抗技能潜空间基础 |
| CALM | 引入条件引导，使潜空间可导向 |
| **PULSE** | 实现全量数据覆盖，构建通用的运动表示"基础" |

### B. 参考来源

- [arXiv:2310.04582](https://arxiv.org/abs/2310.04582)
- [Zhengyi Luo Project Page](https://zhengyiluo.github.io/projects/pulse/)
