---
layout: paper
paper_order: 9
title: "Genie Sim 3.0: A High-Fidelity Comprehensive Simulation Platform for Humanoid Robot"
zhname: "Genie Sim 3.0：面向人形机器人的高保真一体化仿真平台"
category: "Simulation Benchmark"
---

# Genie Sim 3.0: A High-Fidelity Comprehensive Simulation Platform for Humanoid Robot

**人形机器人「数据贵、场景搭得慢、评测靠人盯」一直是规模化训练的瓶颈。Genie Sim 3.0（智元 AgiBot）把「造场景 → 造数据 → 评策略」三件事整进一个闭环平台：① 用 LLM 把一句自然语言指令翻译成高保真仿真场景（意图解析 → 资产检索 → DSL 代码生成 → 场景组装四步流水线）；② 用「遥操作（PICO VR）+ 自动化（cuRobo GPU 运动规划）」双模式大批量造演示数据；③ 首次把 LLM/VLM 用作自动评测器，从语义理解、空间推理、操作执行三个维度自动判分。配套开源 5140 个仿真就绪资产、1 万+ 小时合成数据、10 万+ 评测场景，并在智元 G1/G2 人形上验证了强 sim-to-real 相关性（R²=0.924）。**

> 📅 阅读日期: 2026-06-17
>
> 🏷️ 板块: 11 Simulation Benchmark · 人形仿真平台 / LLM 场景生成 / 批量数据生成 / VLM 自动评测
>
> 🔁 推进轨: 模块轮转（10_Sim-to-Real → **11_Simulation_Benchmark**）

---

## 📋 基本信息

| 项目 | 链接 |
|---|---|
| arXiv | [2601.02078](https://arxiv.org/abs/2601.02078) |
| HTML | [在线阅读](https://arxiv.org/html/2601.02078) |
| PDF | [下载](https://arxiv.org/pdf/2601.02078) |
| 源码 | [AgibotTech/genie_sim](https://github.com/AgibotTech/genie_sim) ✅ |
| **发布时间** | 2026-01-05（arXiv v1），2026-04-28（v2 修订） |
| 作者 / 机构 | Chenghao Yin、Da Huang、Di Yang、Jichao Wang、Nanshu Zhao、Chen Xu 等（智元机器人 AgiBot / Agibot Technology） |

**机器人平台**：智元 **G1 / G2 人形机器人**，支持多种末端执行器（omnipicker、omnihands、INSPIRE 灵巧手 skillhands、智行 gripper）；本作侧重「桌面级全身操作」而非全身行走。

**领域归属**：人形机器人**仿真平台 + 数据生成 + 自动评测基准**——一体化的「场景—数据—评测」闭环生态。

---

## 🎯 一句话总结

要规模化训练人形操作策略，痛点有三：**场景搭建慢**（手工建模费时）、**数据采集贵**（真机遥操作成本高）、**策略评测难**（靠人逐条看结果、且难标准化）。Genie Sim 3.0 把这三件事做成一个闭环平台：用 **LLM 从一句话生成高保真场景**、用 **遥操作 + 自动规划双模式批量造数据**、再用 **VLM 自动评测**。平台开源了 5140 个资产、1 万+ 小时合成数据与 10 万+ 评测场景，并证明**仿真表现与真机表现高度线性相关（R²=0.924、斜率≈1.045）**，说明在它上面跑出来的分数能可靠预测真机表现。

---

## 📌 英文缩写速查

| 缩写 | 全称 | 解释 |
|---|---|---|
| LLM | Large Language Model | 大语言模型，用于解析指令、生成场景代码、生成评测任务 |
| VLM | Vision-Language Model | 视觉-语言模型，用于自动评测策略执行结果 |
| DSL | Domain-Specific Language | 领域专用语言，场景生成流水线里描述场景的中间代码 |
| cuRobo | CUDA Robot Motion Generation | NVIDIA 的 GPU 加速运动规划库，自动化造数据时用 |
| 3DGS | 3D Gaussian Splatting | 三维高斯泼溅，用于真实场景重建/照片级渲染 |
| Sim-to-Real | - | 仿真到真机迁移 |
| π₀.₅ | pi-0.5 | 一个 VLA 操作策略模型，本文实验用它评估 sim-to-real |

---

## ❓ 论文要解决什么问题？

人形/操作机器人要靠学习方法规模化，离不开**海量、多样、带标注的演示数据**与**可复现的评测**。但现实里：

1. **场景搭建慢**：每个新任务/新环境都要人工建模、摆资产、调物理，扩展性差；
2. **数据采集贵**：真机遥操作既慢又费人力，难以覆盖足够多的物体/布局/任务；
3. **评测不标准**：操作任务成功与否常需人工判读，难以大规模、自动、客观地比较策略。

**核心目标**：

> 构造一个**一体化**的人形仿真平台，把「**场景生成 → 数据生成 → 策略评测**」打通成闭环，并让每个环节都尽量**自动化、可扩展、可复现**，同时保证**高保真**以缩小 sim-to-real 差距。

---

## 🔧 方法拆解：四大模块的「场景—数据—评测」闭环

### 1. Genie Sim Generator：LLM 驱动的场景生成

把一句自然语言指令变成可用的仿真场景，分四步流水线：

- **意图解析（intention interpretation）**：LLM 读懂用户想要什么任务/什么环境；
- **资产检索（asset retrieval）**：从 5140 个仿真就绪资产库（353 个类别）里挑合适的物体；
- **DSL 代码生成**：LLM 生成描述场景布局的领域专用语言代码；
- **场景组装（assembly）**：执行 DSL，把资产摆放成高保真、物理合理的可交互场景。

### 2. 数据生成：遥操作 + 自动化「双模式」

- **遥操作模式**：用 **PICO VR** 头显手柄，人远程操作虚拟机器人完成复杂任务，采高质量演示；
- **自动化模式**：用 **cuRobo（GPU 加速运动规划）** 自动生成抓取/放置类轨迹，批量、低成本扩数据。

两种模式互补：复杂、需要人类技巧的任务走遥操作，结构化、可规划的任务走自动化。

### 3. 评测基准：LLM 出题 + VLM 判分（首创亮点）

- 用 **LLM 自动生成任务指令**，覆盖大量任务变体；
- 用 **VLM 自动评测**策略执行结果，从三个维度判分：**语义理解、空间推理、操作执行**；
- 号称是**首个把 LLM 用于自动化评测**的机器人基准，免去人工逐条判读。

### 4. 环境重建：3DGS + 扩散模型

- 用 **3D 高斯泼溅（3DGS）** 做照片级真实场景重建；
- 用**扩散模型做视角外推（view extrapolation）**，补全重建里看不到的视角，提升渲染真实感、进一步缩小 sim-to-real 差距。

---

## 🧭 整体流程（mermaid）

<div class="mermaid">
flowchart TB
    NL["🗣️ 自然语言指令<br/>「让机器人把桌上不同颜色的方块分类」"]

    subgraph GEN["🌐 ① 场景生成 (LLM Generator)"]
        INT["意图解析"]
        RET["资产检索<br/>5140 资产 / 353 类"]
        DSL["DSL 代码生成"]
        ASM["场景组装<br/>高保真可交互场景"]
        INT --> RET --> DSL --> ASM
    end

    subgraph DATA["🎮 ② 数据生成 (双模式)"]
        TELE["遥操作<br/>PICO VR · 复杂任务"]
        AUTO["自动化<br/>cuRobo GPU 规划 · 批量"]
    end

    subgraph RECON["🖼️ 真实感增强"]
        GS["3D 高斯泼溅重建"]
        DIFF["扩散模型视角外推"]
        GS --> DIFF
    end

    subgraph EVAL["🧪 ③ 评测基准 (LLM 出题 + VLM 判分)"]
        TASK["LLM 自动生成任务指令"]
        VLM["VLM 自动评测<br/>语义 / 空间 / 执行"]
        TASK --> VLM
    end

    NL --> GEN
    ASM --> DATA
    RECON -. 提升真实感 .-> DATA
    DATA --> TRAIN["🤖 训练操作策略<br/>(如 π₀.₅) · 智元 G1/G2 人形"]
    TRAIN --> EVAL
    EVAL --> REAL["🦾 sim-to-real 部署<br/>R²=0.924 · 斜率≈1.045"]

    style GEN fill:#e8f4fd,stroke:#1f78b4
    style DATA fill:#fff7e6,stroke:#e67e22
    style EVAL fill:#eafaf1,stroke:#27ae60
    style RECON fill:#f5eef8,stroke:#8e44ad
</div>

---

## 💡 核心贡献

1. **一体化平台**：把「场景生成 → 数据生成 → 策略评测」打通成闭环，覆盖人形操作数据/评测全流程；
2. **LLM 场景生成**：四步流水线（意图→检索→DSL→组装）让自然语言一句话即可生成高保真可交互场景；
3. **首个 LLM/VLM 自动评测基准**：LLM 出题、VLM 从语义/空间/执行三维度自动判分，免人工、可规模化；
4. **大规模开源**：5140 个仿真资产（353 类）、1 万+ 小时合成数据、200+ 任务、10 万+ 评测场景全部开源；
5. **可信 sim-to-real**：在智元 G1/G2 + π₀.₅ 上验证**仿真分数与真机分数强线性相关（R²=0.924）**。

---

## 📊 关键设定与结果

| 维度 | 值 |
|---|---|
| 机器人平台 | 智元 G1 / G2 人形，多末端（omnipicker / omnihands / INSPIRE / 智行 gripper） |
| 资产库 | 5140 个仿真就绪物体，353 个类别 |
| 合成数据 | 10000+ 小时，200+ 任务 |
| 评测场景 | 100000+ 配置 |
| 场景生成 | LLM 四步流水线（意图→资产检索→DSL→组装） |
| 数据生成 | 遥操作（PICO VR）+ 自动化（cuRobo GPU 规划） |
| 真实感重建 | 3D 高斯泼溅（3DGS）+ 扩散模型视角外推 |
| 自动评测 | LLM 出题 + VLM 判分（语义 / 空间 / 执行） |

**sim-to-real 示例（π₀.₅，单位为成功率）**：

| 任务 | 1500 条仿真数据训练 | 500 条真机数据训练 |
|---|---|---|
| 按颜色挑选（Select Color） | 0.85 | 0.73 |
| 识别尺寸（Recognize Size） | 0.94 | 0.75 |
| 抓取目标（Grasp Targets） | 0.71 | 0.58 |
| 整理物体（Organize Objects） | 0.60 | 0.40 |

> 📌 仿真与真机表现的整体相关性 **R²=0.924、斜率≈1.045**，说明平台上的评测分数能可靠预测真机表现。更多消融与吞吐数据请以论文 PDF 为准。

---

## 🤖 对人形仿真 / 数据生态的意义

| 方向 | 含义 |
|---|---|
| **降低数据/场景成本** | LLM 一句话造场景 + 双模式批量造数据，把「搭场景、采数据」从人力密集变成可规模化 |
| **评测自动化** | 首次用 LLM/VLM 当评测器，让大规模、客观、可复现的策略评测成为可能 |
| **缩小 sim-to-real** | 3DGS + 扩散视角外推提升真实感，并用 R²=0.924 的相关性背书仿真评测的可信度 |
| **开源生态** | 资产/数据/评测场景全开放，可直接接入 VLA（如 π₀.₅）等人形操作策略训练 |

---

## 🎤 面试参考

**Q：Genie Sim 3.0 解决的核心痛点是什么？**
A：人形操作策略规模化训练的三座大山——场景搭建慢、数据采集贵、评测难标准化。它把这三件事做成一个自动化、可扩展的闭环平台。

**Q：它怎么「用一句话生成场景」？**
A：四步流水线：LLM 先做意图解析理解任务，再从 5140 个资产库里检索合适物体，然后生成描述布局的 DSL 代码，最后执行 DSL 把场景组装成高保真可交互环境。

**Q：为什么说它的评测基准是亮点？**
A：它首次把 LLM/VLM 用作自动评测器——LLM 自动出题（生成大量任务指令），VLM 从语义理解、空间推理、操作执行三个维度自动判分，免去人工逐条判读，使评测能大规模、客观、可复现地做。

**Q：怎么证明这套仿真评测「靠谱」？**
A：在智元 G1/G2 人形 + π₀.₅ 策略上，对比纯仿真数据与真机数据的训练表现，发现仿真分数与真机分数高度线性相关（R²=0.924、斜率≈1.045），即仿真里跑出来的分能可靠预测真机。

**Q：和 ComFree-Sim / Isaac Lab 这类「物理引擎/仿真器」相比定位有何不同？**
A：ComFree-Sim、Isaac Lab 卖点在底层物理/并行性能；Genie Sim 3.0 卖点在**上层一体化生态**——场景自动生成、双模式数据生成、LLM/VLM 自动评测，外加大规模开源资产与数据，更偏「数据与评测工厂」。

---

## 🔗 相关阅读

- [ComFree-Sim: A GPU-Parallelized Analytical Contact Physics Engine](../ComFree-Sim__GPU-Parallelized_Analytical_Contact_Physics_Engine/ComFree-Sim__GPU-Parallelized_Analytical_Contact_Physics_Engine.md)：同模块的 GPU 并行接触物理引擎，偏底层物理，与本作的上层生态形成互补
- [GRUtopia: Dream General Robots in a City at Scale](../GRUtopia__Dream_General_Robots_in_a_City_at_Scale/GRUtopia__Dream_General_Robots_in_a_City_at_Scale.md)：另一种大规模仿真城市/生态路线，本仓库已有笔记
- [HumanoidBench: Simulated Humanoid Benchmark](../HumanoidBench/HumanoidBench.md)：人形全身仿真基准，本仓库已有笔记
- [MolmoSpaces: A Large-Scale Open Ecosystem for Robot Navigation and Manipulation](../MolmoSpaces__A_Large-Scale_Open_Ecosystem_for_Robot_Navigation_and_Manipulation/MolmoSpaces__A_Large-Scale_Open_Ecosystem_for_Robot_Navigation_and_Manipulation.md)：大规模开放机器人导航/操作生态，本仓库已有笔记

---

> 备注：本笔记基于 arXiv 摘要、HTML 全文（[2601.02078](https://arxiv.org/html/2601.02078)）与开源仓库（[AgibotTech/genie_sim](https://github.com/AgibotTech/genie_sim)）整理；**具体吞吐、资产/任务的完整清单、各任务消融与更细的 sim-to-real 数值**请以论文 PDF 为准。
