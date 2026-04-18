---
layout: paper
paper_order: 11
title: "PULSE: Physically Plausible Universal Latent Skill Extraction"
category: "基础强化学习"
zhname: "PULSE：物理可行的通用潜在技能提取"
---

# PULSE: Physically Plausible Universal Latent Skill Extraction
**PULSE：物理可行的通用潜在技能提取**

> 📅 阅读日期: 待读
> 🏷️ 板块: 技能组合主线 · ASE → CALM → **PULSE**
> 🚧 本笔记为骨架，待逐节补完。

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **arXiv** | 🚧 待核对（Zhengyi Luo et al., ICLR 2024） |
| **PDF** | 🚧 |
| **作者** | 🚧 Zhengyi Luo 等 |
| **机构** | 🚧 CMU / Meta Reality Labs |
| **发布时间** | 🚧 2023–2024 |
| **项目主页** | 🚧 |
| **代码** | 🚧 |

---

## 🎯 一句话总结

> 🚧 待补：一句大白话概括 PULSE 的核心贡献（预期方向：把"全动作库"压缩成通用运动 latent space，供下游任务即插即用）。

---

## 📌 英文缩写速查

| 缩写 | 全称 | 简单解释 |
|------|------|----------|
| 🚧 | | |

---

## ❓ PULSE 要解决什么问题？

> 🚧 待补。参考路线图定位：在 ASE（2022）提供 latent skill、CALM（2023）加方向性的基础上，PULSE 进一步要解决什么？猜想方向：
> - 如何把 AMASS 规模的人类动作数据全部压进一个 latent space？
> - 如何让下游 high-level controller 在这个 latent 上直接 plug-and-play？

---

## 🔧 方法详解

> 🚧 待补。读论文后按以下结构展开：
> 1. 数据准备
> 2. Encoder / Prior / Policy 结构
> 3. 训练目标 & loss
> 4. 与 ASE / CALM 的差异

---

## 🚶 具体实例

> 🚧 待补。建议用一个"从 AMASS 片段到 latent 再到仿真动作"的前向流程走通。

---

## 🤖 工程价值

> 🚧 待补。关注点：
> - PULSE 的 latent space 是否被后续工作（H2O、OmniH2O 等）作为基础？
> - 在真机上跑过吗？
> - 对人形机器人学习流水线的影响（数据规模 / 泛化）？

---

## 📁 MimicKit 源码对照

> 🚧 读完论文后确认 MimicKit 是否覆盖；若暂无，标 ❌。

---

## 🎤 面试高频问题 & 参考回答

> 🚧 5–8 题待补。

---

## 💬 讨论记录

> 🚧

---

## 📎 附录

### A. 与路线图其他论文的关联

| 论文 | 关系 |
|------|------|
| ASE | 提供 adversarial skill latent，但无方向性 |
| CALM | 在 ASE 上加条件，让 latent 可导向 |
| **PULSE** | 🚧 下一步——扩大规模并统一 latent 空间 |

### B. 参考来源

- 🚧 论文链接
- 🚧 项目主页 / 视频
- 🚧 开源仓库
