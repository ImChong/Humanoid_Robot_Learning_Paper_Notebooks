---
layout: paper
title: "ASE: Adversarial Skill Embeddings for Large-Scale Motion Control"
category: "Foundational RL"
---

# ASE: Adversarial Skill Embeddings for Large-Scale Motion Control
**大规模可复用对抗技能嵌入：物理仿真角色**

> 📅 阅读日期: -  
> 🏷️ 板块: Reinforcement Learning / Motion Imitation / Skill Embedding

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **arXiv** | [2205.01906](https://arxiv.org/abs/2205.01906) |
| **PDF** | [下载](https://arxiv.org/pdf/2205.01906) |
| **作者** | Xue Bin Peng, Yunrong Guo, Lina Halper, Sergey Levine, Sanja Fidler |
| **机构** | UC Berkeley, NVIDIA |
| **发布时间** | 2022年（SIGGRAPH 2022, ACM Transactions on Graphics） |
| **项目主页** | [xbpeng.github.io/projects/ASE](https://xbpeng.github.io/projects/ASE/) |
| **GitHub** | [nv-tlabs/ASE](https://github.com/nv-tlabs/ASE)<br>[xbpeng/MimicKit](https://github.com/xbpeng/MimicKit) |

---

## 🎯 一句话总结

ASE 在 AMP 的基础上引入**潜在技能空间（latent skill space）**，将大量动捕数据编码为一个连续的、可复用的技能嵌入——预训练一次，就能通过高层策略选择不同的潜变量 $z$ 来完成多种下游任务，而不需要为每个任务重新训练底层运动控制器。

---

## ❓ 这篇论文要解决什么问题？

> 待补充

---

## 🔧 ASE 是怎么做的？

> 待补充

---

## 🚶 具体实例

> 待补充

---

## 🤖 ASE 对人形机器人领域的意义

> 待补充

---

## 🎤 面试高频问题 & 参考回答

> 待补充

---

## 💬 讨论记录

> 待补充

---

## 📎 附录

### A. 与路线图其他论文的关联

| 关系 | 说明 |
|------|------|
| **AMP → ASE** | ASE 在 AMP 的对抗框架上引入潜在技能空间 |
| **ASE → CALM** | CALM 在 ASE 基础上引入条件生成（可控技能选择） |
| **DeepMimic → ASE** | DeepMimic 的单技能模仿 → ASE 的多技能嵌入 |
