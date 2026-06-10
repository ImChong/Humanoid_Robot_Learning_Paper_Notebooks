---
layout: paper
paper_order: 2
title: "Learned Motion Matching"
zhname: "学习式动作匹配：用三张小网络替代海量动作数据库"
category: "人体动作生成"
---

# Learned Motion Matching
**学习式动作匹配：用三张小网络替代海量动作数据库**

> 📅 阅读日期: 2026-05-17
>
> 🏷️ 板块: 14 Human Motion · 角色动画 / 运动控制器
>
> 🔁 推进轨: 模块轮转（13_Physics-Based_Animation → **14_Human_Motion**）

---

## 📋 基本信息

| 项目 | 链接 |
|---|---|
| 会议 | **ACM SIGGRAPH 2020**（ACM TOG, Vol. 39, No. 4, Article 53） |
| DOI | [10.1145/3386569.3392440](https://doi.org/10.1145/3386569.3392440) |
| ACM 页面 | [dl.acm.org/doi/10.1145/3386569.3392440](https://dl.acm.org/doi/10.1145/3386569.3392440) |
| PDF | [作者主页 PDF](https://theorangeduck.com/media/uploads/other_stuff/Learned_Motion_Matching.pdf) · [ACM PDF](https://dl.acm.org/doi/pdf/10.1145/3386569.3392440) |
| 项目主页 | [theorangeduck.com/page/learned-motion-matching](https://theorangeduck.com/page/learned-motion-matching) |
| 作者 | Daniel Holden, Oussama Kanoun, Maksym Perepichka, Tiberiu Popa |
| 机构 | **Ubisoft La Forge**（蒙特利尔）/ Concordia University |
| **发布时间** | 2022-09-29 (arXiv), **ACM SIGGRAPH 2020**（ACM TOG, Vol. 39, No. 4, Article 53） |
| 代码（作者后续开源 demo） | [orangeduck/Motion-Matching](https://github.com/orangeduck/Motion-Matching) |
| 代码（社区实现） | [pau1o-hs/Learned-Motion-Matching](https://github.com/pau1o-hs/Learned-Motion-Matching) |
| 配套动作数据 | [ubisoft/ubisoft-laforge-animation-dataset (LaFAN1)](https://github.com/ubisoft/ubisoft-laforge-animation-dataset) |

---

## 🎯 一句话总结

> **Motion Matching** 视觉效果好、流程稳定、被游戏行业广泛使用，但内存占用随动画库线性增长；本文把它拆成三个步骤，每步用一张小神经网络替代，得到了一个**视觉上几乎无差别、但内存与动画数据规模解耦**的"学习式动作匹配"系统。

---

## ❓ 论文要解决什么问题？

经典 **Motion Matching** 每帧都需要：

1. 从当前姿态构造一个"查询向量"（query feature）；
2. 在**完整动作库的特征表**里做最近邻搜索，找到最匹配的下一段动画；
3. 跳到该帧、继续播放。

它对动画师友好、可控、可预测，但有两个硬伤：

- **内存占用**与动画时长**线性增长**——库越大，运行时占用越夸张；
- **离线预处理**与特征手工挑选都依赖工程经验。

神经网络生成模型（PFNN、MANN 等）虽然能压缩动画，但牺牲了 Motion Matching 的**可控性**与**视觉稳定性**。本文目标：**保留 Motion Matching 的所有优点，把内存代价压下来**。

---

## 🔧 方法详解 —— 三张小网络

作者把 Motion Matching 流水线拆成三步，每步训练一个独立网络替代：

| 网络 | 角色 | 替代了什么 |
|---|---|---|
| **Decompressor** | 特征向量 → 完整姿态（pose） | 替代了"按索引去动画库里取完整帧"这一步；同时通过自编码器自动学到"额外特征"，省去手工选特征的工作 |
| **Stepper** | 当前特征向量 → 下一帧特征向量 | 替代了"在动画库里顺序播放下一帧"这一步，让系统**多数帧只在特征空间内走**，无须查库 |
| **Projector** | 查询向量 → 最佳匹配的特征向量 | 替代了"在动画库里做最近邻搜索"这一步 |

运行时三者协同工作：

- 多数帧由 **Stepper** 推进、由 **Decompressor** 还原 pose（**零数据库访问**）；
- 当用户输入大幅变化（如改方向 / 切动作）时，**Projector** 直接预测出新的特征向量，仍不需要查库；
- 整个动画库只在**离线训练**时使用，运行时**完全不驻留内存**。

最终效果：与原版 Motion Matching 视觉差异极小，但内存占用与动画时长**解耦**，可以扩展到原本无法装入内存的大规模动捕库。

---

### 🧭 整体流程（mermaid）

<div class="mermaid">
flowchart LR
    subgraph OFF["🛠 离线训练 Offline Training"]
        DB["📦 动画数据库<br/>(Motion DB)"]
        FT["🧮 特征提取<br/>(query/extra feats)"]
        TR1["🎓 训练 Decompressor<br/>(auto-encoder)"]
        TR2["🎓 训练 Stepper<br/>(逐帧预测)"]
        TR3["🎓 训练 Projector<br/>(query→最近邻特征)"]
        DB --> FT --> TR1
        FT --> TR2
        FT --> TR3
    end

    subgraph RT["🕹 运行时 Runtime（无数据库）"]
        Q["🎮 用户控制信号<br/>(轨迹 / 朝向 / 步速)"]
        SW{"切换条件?<br/>(用户输入剧变)"}
        STEP["🔁 Stepper<br/>特征空间逐帧推进"]
        PROJ["🎯 Projector<br/>query → 新特征"]
        DEC["🪄 Decompressor<br/>特征 → 完整 pose"]
        POSE["🚶 输出姿态<br/>(供渲染 / 物理用)"]

        Q --> SW
        SW --是--> PROJ
        SW --否--> STEP
        PROJ --> DEC
        STEP --> DEC
        DEC --> POSE
        POSE --下一帧 query--> SW
    end

    TR1 -.参数加载.-> DEC
    TR2 -.参数加载.-> STEP
    TR3 -.参数加载.-> PROJ

    style OFF fill:#e8f4fd,stroke:#1f78b4,color:#0b3954
    style RT  fill:#e8fbe8,stroke:#27ae60,color:#0f3d1e
</div>

---

## 💡 核心贡献

1. **首个把 Motion Matching 完整"网络化"的方案**：用三张职责单一的小网络替代查询、检索、解码三步，保留了 Motion Matching 的可控性；
2. **内存与数据规模解耦**：动画库只在训练时存在，运行时**几乎为零**，给"超大规模角色动画库"打开通路；
3. **特征自动学习**：用自编码器学到额外特征，省去原版"手工挑特征"环节；
4. **工业级实用性**：方法源自 Ubisoft La Forge，几乎可以无痛接入既有 Motion Matching 流水线。

---

## 📊 与相关路线的关系

| 路线 | 数据访问 | 可控性 | 内存随库扩展 | 代表方法 |
|---|---|---|---|---|
| 传统 Motion Matching | 每帧查库 | ✅ 高 | ❌ 线性增长 | Ubisoft 早期管线 |
| PFNN / MANN | 神经网络生成 | ⚠️ 中 | ✅ 与库解耦 | Holden 2017 / Zhang 2018 |
| **Learned Motion Matching（本文）** | 训练时用库，运行时无库 | ✅ 高 | ✅ 与库解耦 | — |
| 动作扩散模型（MDM 等） | 训练时用库 | ⚠️ 弱（开环） | ✅ 与库解耦 | MDM, OmniControl |

---

## 🤖 对人形机器人的启发

这是一篇典型的**角色动画**论文，但思路对人形机器人控制同样有用：

- **运动先验压缩**：人形 RL / 模仿学习常要依赖大量参考动作（AMASS、LaFAN1 等）；把"参考动作库"压成一组网络的思路，可以缓解大规模 motion prior 的存储与采样代价；
- **动作切换的连续性**：Projector / Stepper 的分工，本质上提供了"巡航 vs 切换"两种动态模式，可以启发人形 tracker 在不同行为间的**平滑过渡设计**；
- **特征空间检索**：现代 HOVER / SONIC 等 whole-body controller 中也广泛用到"motion latent + 检索"思想，可以视为 LMM 范式在物理 tracker 上的延伸。

---

## 📁 源码 / 资源对照

| 资源 | 内容 |
|---|---|
| [theorangeduck.com 项目页](https://theorangeduck.com/page/learned-motion-matching) | 原作者博客，含视频、推导与可读性极高的工程描述 |
| [orangeduck/Motion-Matching](https://github.com/orangeduck/Motion-Matching) | 作者后续开源的 Motion Matching + LMM 演示，C++ 实现 |
| [pau1o-hs/Learned-Motion-Matching](https://github.com/pau1o-hs/Learned-Motion-Matching) | 社区 Unity / Python 实现，方便阅读三网络结构 |
| [ubisoft-laforge-animation-dataset (LaFAN1)](https://github.com/ubisoft/ubisoft-laforge-animation-dataset) | Ubisoft La Forge 公开动捕数据集，常被本方法和后续 in-betweening 工作引用 |

---

## 🎤 面试参考

**Q：为什么需要三张网络，而不是一张大网络直接 query → pose？**
A：拆成三步是为了保留 Motion Matching 的**可控性与可调试性**——Projector 处理"切换"、Stepper 处理"巡航"、Decompressor 处理"还原"。一张大网络容易把所有行为揉在一起，难以单独调优、也难以与既有动画管线对接。

**Q：相比 PFNN / MANN 这类纯生成模型，LMM 有什么优势？**
A：LMM 仍然以**特征空间的最近邻匹配**为核心语义，因此动画师可以像调 Motion Matching 一样调参（轨迹权重、朝向权重等），可控性显著优于纯生成式网络。

**Q：LMM 对人形机器人 sim-to-real 直接有用吗？**
A：不直接——它解决的是**虚拟角色动画**问题，不考虑物理动力学。但作为"上游动作先验压缩 + 切换控制器"的范式，对 motion prior、tracker 设计、以及大规模 retargeting 管线有借鉴价值。

---

## 🔗 相关阅读

- **前置工作**：Motion Matching（Clavet, GDC 2016）、PFNN（Holden 2017）、MANN（Zhang 2018）
- **同期数据集**：LaFAN1（Robust Motion In-betweening，SIGGRAPH 2020）
- **后续延伸**：MDM（[arXiv 2209.14916](https://arxiv.org/abs/2209.14916)）、OmniControl（[arXiv 2310.08580](https://arxiv.org/abs/2310.08580)）等扩散式动作生成
