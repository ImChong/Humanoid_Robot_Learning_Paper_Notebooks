---
layout: paper
paper_order: 9
title: "OMG: Omni-Modal Motion Generation for Generalist Humanoid Control"
zhname: "OMG：通用人形控制的多模态运动生成"
category: "物理动画"
---

# OMG: Omni-Modal Motion Generation for Generalist Humanoid Control
**像生物运动系统那样分层：一个会「读多模态指令」的大脑（动作生成）骑在一个「反应式」小脑（物理动作跟踪）之上**

> 📅 阅读日期: 2026-06-19
>
> 🏷️ 板块: 13 Physics-Based Animation · 多模态动作生成 / 扩散 Transformer / 物理动作跟踪 / 人形通用控制
>
> 🔁 推进轨: 模块轮转（12_Hardware_Design → **13_Physics-Based_Animation**）

---

## 📋 基本信息

| 项目 | 链接 |
|---|---|
| arXiv | [2606.10340](https://arxiv.org/abs/2606.10340) |
| HTML | [在线阅读](https://arxiv.org/html/2606.10340) |
| PDF | [下载](https://arxiv.org/pdf/2606.10340) |
| 项目主页 | [tsinghua-mars-lab.github.io/OMG](https://tsinghua-mars-lab.github.io/OMG/) |
| 源码 | [Tsinghua-MARS-Lab/OMG](https://github.com/Tsinghua-MARS-Lab/OMG) |
| **发布时间** | 2026-06-09（arXiv） |
| 机构 | 清华大学 MARS Lab / IIIS |

**作者**：Siqiao Huang, Kun-Ying Lee, Dongming Qiao, Guanqi He, Zhenyu Wang, Yitang Li, Shaoting Zhu, Hang Zhao。

**定位**：一个面向人形机器人的**全模态（omni-modal）动作生成框架**——把语言、音频、人体参考动作等异构条件统一喂给一个**扩散 Transformer「大脑」**，生成全身轨迹，再交给一个预训练的**物理动作跟踪「小脑」**在机器人上执行，朝「人形基础模型」迈出具体一步。

---

## 🎯 一句话总结

人形控制要么「会跟踪但不会自己想动作」（纯 tracking），要么「会生成动作但落不了地」（纯运动学生成）。OMG 仿照「大脑—小脑」分工，把这两件事解耦：上游 **OMG-DiT（扩散 Transformer，大脑）** 把语言/音频/人体动作等多模态指令翻译成未来的全身运动轨迹，下游 **HoloMotion 跟踪器（小脑）** 负责把轨迹在物理里稳稳执行；配上一条 **1174 小时、统一到 Unitree G1 本体**的多模态数据流水线，做到 SOTA、可随模型规模涨点、且能用极少数据高效适配新模态。

---

## 📌 英文缩写速查

| 缩写 / 术语 | 全称 / 含义 | 解释 |
|---|---|---|
| OMG-DiT | OMG Diffusion Transformer | 上游「大脑」，扩散 Transformer，直接在动作空间生成全身轨迹 |
| DiT | Diffusion Transformer | 用 Transformer 做骨干的扩散模型 |
| FiLM | Feature-wise Linear Modulation | 逐特征线性调制，用于注入帧对齐的音频/参考动作条件 |
| CFG | Classifier-Free Guidance | 无分类器引导，靠训练时随机丢弃条件实现可调强度的条件生成 |
| GMR | General Motion Retargeting | 通用动作重定向，把不同拓扑的人体动作统一到 G1 本体 |
| HoloMotion | —— | 预训练的物理动作跟踪器，充当「小脑」执行生成的轨迹 |
| MPJPE | Mean Per-Joint Position Error | 各关节平均位置误差，越小越好 |

---

## ❓ 这篇论文要解决什么问题？

人形机器人要成为「通用智能体」，需要同时具备两种能力，但它们长期割裂：

- **会「想」**：根据语言、音乐、看到的人体动作等高层意图，生成合理的全身运动；
- **会「做」**：把这套运动在真实/仿真物理里稳定执行而不摔。

现有方案常常二选一：纯 tracking 控制器（如 motion imitation）执行力强但**不会自己生成动作**；纯运动学动作生成模型**生成的动作物理上不可执行**；而且不同模态（文本 / 音频 / 动作）往往各训各的、难以统一。OMG 的问题是：**能不能用一个统一的生成大脑吃下所有模态、再借一个现成的物理小脑落地，做成可扩展的人形基础模型雏形？**

---

## 🧱 方法的关键设计

### 1. 「大脑—小脑」分层（generator–tracker hierarchy）

- **大脑（OMG-DiT）**：把高层条件翻译成未来的全身运动轨迹（运动学层面）；
- **小脑（HoloMotion 跟踪器）**：一个**预训练且固定**的物理跟踪控制器，把生成轨迹转成机器人可执行动作。
- 好处：生成和执行解耦，大脑可以专注「想得对」，小脑保证「做得稳」，且小脑可复用、不必随大脑重训。

### 2. OMG-DiT：直接在动作空间生成的扩散 Transformer

- **目标**：扩散 Transformer，采用 **x-prediction**，**直接在动作空间生成**，不依赖额外学习的编码器/隐空间；
- **动作表示**：125 维、以根节点为中心的状态向量（规范化的根位置/朝向、关节角、身体连杆位置）；
- **多模态条件注入**：
  - **语言**：冻结的 T5 编码器，经 **cross-attention** 注入；
  - **音频**：帧对齐特征，经 **FiLM** 调制注入；
  - **人体参考动作**：同样走 FiLM 注入——**把「动作生成」本身当作一种隐式重定向**；
  - **新模态**：用**零初始化的 FiLM 适配器**，少量数据即可高效微调接入；
- **训练**：条件扩散 + **随机模态 dropout**，从而支持 **CFG** 与多模态零样本组合。

### 3. OMG-Data：物理在环（physics-in-the-loop）的数据流水线

把 **AMASS、AIST++、BEAT2、Motion-X、FineDance** 等公开数据汇聚成 **1174.66 小时**、统一到 Unitree G1 本体的多模态语料：

1. **聚合**多源数据；
2. **重定向**：用 GMR 统一到 G1 拓扑；
3. **标注**：用 Seed-1.8 视觉模型对渲染动作生成文本标签；
4. **切分**：按语言边界或滑窗切片；
5. **过滤**：用 **MuJoCo 物理在环**校验，按摔倒启发式（根高 < 0.20 m 或根倾斜 > 85° 判为摔倒帧）剔除物理上跑不动的片段。

> 数据构成：文本标注约 1166.6h、人体参考动作约 958.77h、音频条件约 191.6h。

---

## 🔄 方法 / 系统结构流程图

<div class="mermaid">
flowchart TD
    subgraph IN["多模态条件 (意图)"]
      L["语言<br/>(T5 冻结编码器)"]
      A["音频<br/>(帧对齐特征)"]
      M["人体参考动作"]
      X["新模态<br/>(如 Pico 关键点遥操作)"]
    end
    L -->|cross-attention| B
    A -->|FiLM| B
    M -->|FiLM| B
    X -->|零初始化 FiLM 适配器, 少样本微调| B
    B["🧠 大脑 OMG-DiT<br/>扩散 Transformer · x-prediction<br/>直接在动作空间生成"]
    B --> TRAJ["未来全身轨迹<br/>(125 维根中心状态)"]
    TRAJ --> C["🌐 小脑 HoloMotion 跟踪器<br/>(预训练 · 物理执行)"]
    C --> R["Unitree G1 实时执行<br/>(MuJoCo 仿真 / 真机)"]
    DATA["OMG-Data 1174h<br/>聚合→GMR重定向→视觉标注→切分→MuJoCo物理过滤"] -.训练.-> B
</div>

---

## 📊 实验与结果

- **文本→动作**（对比 GENMO / HYMotion / Kimodo）：OMG-XL 取得 **FID 6.03**（Kimodo-G1-SEED 为 50.22）、**R@3 86.91%**（对比 41.11%），摔倒率 0.78%（对比 1.56%），关节限位违例极少。
- **音频→动作**（对比 GENMO / LODGE / Bailando）：BeatAlign 0.51、FIDk 40.46、**零摔倒**，对齐指标全面领先。
- **人体参考动作**（对比 GMR / NMR / PHC / OmniRetarget）：**MPJPE 18.84 cm**（OmniRetarget 56.90 cm）——说明「用生成做隐式重定向」很有效。
- **少样本微调**：仅用 1% 目标数据微调，即可超过用全量数据从零训练。
- **规模化**：FID、R-Precision 等指标随模型增大（L → XL）单调改善。
- **零样本组合 / 新模态**：可同时条件于语言 + 音频而无需专门训练；接入 Pico 关键点遥操作只需轻量编码器微调即有不错表现；并演示文本/音频/动作在连续运行中实时切换。

---

## 💡 启发与点评

- **「大脑—小脑」解耦是务实范式**：让生成模型专注「想得对」，把「做得稳」交给一个现成、固定的物理跟踪器，工程上可复用、可叠加，与本模块 PhysMoDPO「先物理化再评分」的思路异曲同工——都在强调生成必须对齐物理执行。
- **统一多模态到单一生成器**：用 cross-attention（语言）+ FiLM（帧对齐的音频/动作）+ 零初始化适配器（新模态）把异构条件收进一个 DiT，配合模态 dropout 实现零样本组合，是把「人形基础模型」做大的合理路径。
- **数据是隐形主角**：1174 小时、物理在环过滤、统一本体——再次印证「会动」的人形模型，瓶颈往往在高质量、统一本体的数据流水线。
- **把生成当隐式重定向**：人体参考动作直接进生成器、MPJPE 远小于专门的重定向方法，这个视角值得借鉴。
- **局限**：训练数据以**平地动作**为主，扩展到不平整地形仍困难；当前是**模块化、只优化生成**，生成器与跟踪器的**联合优化**留待未来；**没有执行反馈闭环**（小脑执行结果不回灌大脑）。

---

## 🎤 面试参考

**Q：OMG 的「大脑—小脑」分别指什么？为什么要分层？**
A：大脑是 OMG-DiT（扩散 Transformer），负责把语言/音频/人体动作等多模态指令生成未来的全身运动轨迹；小脑是预训练的 HoloMotion 物理跟踪器，负责把轨迹在机器人上稳定执行。分层让「想动作」和「执行动作」解耦，生成专注合理性、跟踪保证物理稳定，且小脑可复用不必随大脑重训。

**Q：不同模态是怎么统一注入一个生成器的？**
A：语言用冻结 T5 经 cross-attention 注入；帧对齐的音频和人体参考动作用 FiLM 调制注入；新模态用零初始化 FiLM 适配器少样本微调接入。训练时随机丢弃条件（模态 dropout），从而支持 CFG 与多模态零样本组合。

**Q：为什么强调「物理在环」的数据过滤？**
A：运动学上看着合理的动作，物理上可能根本跑不动。OMG 在 MuJoCo 里跑一遍并用摔倒启发式（根高 / 根倾斜阈值）剔除不可执行片段，保证喂给生成器的数据本身就「落得了地」。

**Q：它和 PhysMoDPO 有什么异同？**
A：都强调「生成要对齐物理执行」。PhysMoDPO 是用固定 WBC 当物理裁判、靠 DPO 把已有生成器后训练成「生成即可执行」；OMG 则是从架构上做「生成大脑 + 物理小脑」的分层，并把多模态统一进一个可扩展的扩散 Transformer，更偏「人形基础模型」的路线。

---

## 🔗 相关阅读 / 类似方向

- [PhysMoDPO: Physically-Plausible Humanoid Motion with Preference Optimization](https://arxiv.org/abs/2603.13228)：本模块，用 DPO 把生成动作对齐物理可执行
- [Kimodo: Scaling Controllable Human Motion Generation](https://research.nvidia.com/labs/sil/projects/kimodo/)：可控人体动作生成，本文对比基线之一
- [PHC: Perpetual Humanoid Control for Real-time Simulated Avatars](https://arxiv.org/abs/2305.06456)：物理动作跟踪器范式，人体参考对照基线
- [DeepMimic: Example-Guided Deep RL of Physics-Based Character Skills (SIGGRAPH 2018)](https://arxiv.org/abs/1804.02717)：物理动作跟踪/模仿的奠基工作

---

> 备注：本笔记基于 arXiv 元信息（2606.10340）、项目主页与论文 HTML 公开内容整理；部分数值（指标、超参、数据时长）以论文公开陈述为准，若后续正式版/源码释出更详尽内容可补全对应字段。
