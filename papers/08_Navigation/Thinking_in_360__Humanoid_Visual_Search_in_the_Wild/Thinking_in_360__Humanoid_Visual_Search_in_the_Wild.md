---
layout: paper
paper_order: 5
title: "Thinking in 360°: Humanoid Visual Search in the Wild"
zhname: "在 360° 里思考：把人形视觉搜索做成「转头看路 + 转头找物」的两类显式任务"
category: "Navigation"
---

# Thinking in 360°: Humanoid Visual Search in the Wild
**在 360° 里思考：把人形视觉搜索做成「转头看路 + 转头找物」的两类显式任务**

> 📅 阅读日期: 2026-05-26
>
> 🏷️ 板块: Navigation · 视觉搜索 · 360° 全景 · 头部主动转向 · VLM + RL
>
> 🔁 推进轨: 模块轮转（07_Teleoperation → **08_Navigation**）

---

## 📋 基本信息

| 项目 | 链接 |
|---|---|
| arXiv | [2511.20351](https://arxiv.org/abs/2511.20351) |
| HTML | [在线阅读](https://arxiv.org/html/2511.20351v1) |
| PDF | [下载](https://arxiv.org/pdf/2511.20351) |
| 项目主页 | [humanoid-vstar.github.io](https://humanoid-vstar.github.io/) |
| **发布时间** | 2025-11-25 (arXiv) |
| 源码（官方）| [THUSI-Lab/hstar](https://github.com/THUSI-Lab/hstar) · [humanoid-vstar/hstar](https://github.com/humanoid-vstar/hstar) |
| 模型权重 | HuggingFace HVS-3B（Qwen2.5-VL-3B-Instruct 微调，详见仓库 README） |
| 出版 | CVPR 2026 |
| 提交日期 | 2025-11 |

**机构 / 作者**：清华大学（THUSI-Lab）联合 NYU · NVIDIA · Stanford · UC Berkeley · TU Darmstadt。作者：Heyang Yu, Yinan Han, Xiangyu Zhang, Saining Xie, Yiming Li 等。

**任务定位**：把"视觉搜索"从**静态单图里圈框**升级为**人形机器人在 360° 沉浸世界里主动转头**——同时支持「找物体」与「找可行路径」两种行为前置感知任务。

---

## 🎯 一句话总结

H\* 把人形视觉搜索拆成两个**为下游行为而生**的子任务——**HOS**（找物体、视线对齐）和 **HPS**（找路径、身体朝向对齐）——以 360° 全景图为世界模型，让 VLM 像人一样**转头扫视**做空间推理；通过 **冷启动 SFT + 掩码 GRPO** 把 Qwen2.5-VL-3B-Instruct 调成 **HVS-3B**，在自建的 **H\*Bench**（车站 / 商场 / 街道 / 公共场所等"野外"场景）上把物体搜索成功率从 14.83% 拉到 47.38%、路径搜索从 6.44% 拉到 24.94%，三倍以上提升。

---

## 📌 英文缩写速查

| 缩写 | 全称 | 解释 |
|---|---|---|
| HOS | Humanoid Object Search | 人形物体搜索：把目标物体推到视线中心（foveate），为后续抓取做准备 |
| HPS | Humanoid Path Search | 人形路径搜索：识别可行路径并把身体朝向对齐，为后续行走做准备 |
| HVS-3B | Humanoid Visual Search 3B | 本文训练的 3B 量级视觉搜索 VLM |
| H\*Bench | 论文提出的视觉搜索 benchmark | 覆盖交通枢纽 / 大型零售 / 城市街景 / 公共机构等野外场景 |
| GRPO | Group Relative Policy Optimization | DeepSeek-Math 提出的相对优势 RL，不需要 critic |
| SFT | Supervised Fine-Tuning | 监督微调 |
| VLM | Vision-Language Model | 视觉语言模型 |
| Foveate | 把目标推到视野中央 | 来自人眼"中央凹"的概念 |
| Cephalomotor / Oculomotor | 头部 / 眼部运动控制 | 人类视觉搜索的两条神经通路 |

---

## ❓ 论文要解决什么问题？

**视觉搜索（Visual Search）**在视觉领域被研究了很久，但已有 setup 几乎都是「**给定一张静态图，问目标在哪 / 框是什么**」。对**人形机器人**来说，这件事有三个本质 gap：

1. **没有"看哪里"的物理动作**：人形不是相机，它要**主动转头**去看四周才能完成搜索；
2. **没有连接到下游行为**：找到物体之后要**抓**，找到路之后要**走**——视觉搜索的输出必须**对齐"下一步要做什么"**；
3. **场景太家庭化**：现有 benchmark 多在客厅 / 厨房里转，跟真实部署里那些**车站、商场、街道、机场**等大空间、强语义、强空间约束的场景脱节。

H\* 给出的回答：

- 把世界表示成**等距 360° 全景图**（equirectangular panorama），机器人 agent 通过**改变视线方向**在这张图上"看"局部矩形视窗，本质上模拟了人形的**头部 + 眼部联合主动观察**；
- 把任务**显式分两类**：HOS（为抓取做准备：定位 + 对齐视线）、HPS（为行走做准备：找路径 + 对齐身体朝向），输出的动作就是下游控制器要消费的接口；
- 自建 **H\*Bench**：每张全景都配上具身任务问句 + ground-truth 动作（HOS 是**头部朝向**，HPS 是**地面单位方向向量**），强行把场景拉到 in-the-wild。

---

## 🔧 方法拆解

### 1. 世界模型：等距 360° 全景 + 主动视窗

- 每个场景给一张**等距全景**（equirectangular），覆盖完整 4π 立体角；
- VLM agent 不能一次看全景，而是**给定一个视线方向 (yaw, pitch)**，从全景里**剪出一块透视视窗**作为当前帧；
- 多轮交互里，模型每一步**选下一个视线方向**，等价于"我要把头转到哪里去看"。
- 这种 setup 的好处：把"主动观察"压成 VLM 能理解的**一串动作 token**，且天然支持**多步推理**（先看大概，再去看细节）。

### 2. 两类任务的动作语义

| 任务 | 动作含义 | 终止条件 |
|---|---|---|
| **HOS**（找物体） | 选下一个**头部朝向 (yaw, pitch)**，目标是把待找物体**推到视线中央**（foveate） | 物体被对齐到视野中心 + 置信度满足 |
| **HPS**（找路径） | 选下一个**视线方向**，最终输出**地面单位方向向量**作为"应该往哪走" | 给出与可行路径对齐的身体朝向 |

> 关键观察：HOS 的输出**直接被抓取控制器消费**（已经把物体推到视线中），HPS 的输出**直接被行走控制器消费**（机器人转向 → 直走）。这与 NaVILA / EgoActor 那种"先 VLM 推理一段话再去落地"的范式不同，**H\* 输出的是物理动作向量**。

### 3. 训练：冷启动 SFT → 掩码 GRPO 的两段式

1. **冷启动 SFT**（基于 LLaMA-Factory）
   - 数据：`hos_sft` / `hps_sft`，每个样本是一条多轮"看-思-动"轨迹，包含**自由思考（free think）**段和最终动作；
   - 目的：先让 Qwen2.5-VL-3B-Instruct 学会**"输出动作 + 思维链格式"**和**360° 视窗坐标系**，避免直接 RL 训练发散；
2. **强化学习：掩码 GRPO**（基于 VAGEN / verl）
   - 数据：`hvs_rl`，奖励主要看**是否成功完成 HOS / HPS**（物体是否落在视线中心、路径方向是否与 GT 对齐）；
   - **GRPO**：组内多次 rollout 用相对奖励算优势，无需 critic；
   - **掩码**：只在**模型自己生成的"动作 token"**位置上回传 RL 梯度，避免污染思维链或观察 token——这是把 GRPO 用在多模态多轮 agent 上时常见的稳定化技巧；
   - 推理用 vLLM 部署成 OpenAI 兼容服务，方便和 benchmark 解耦。

### 4. H\*Bench：野外 360° 视觉搜索基准

- 场景域：**交通枢纽 / 大型零售空间 / 城市街道 / 公共机构**等，强调**空间大、语义重、视野遮挡多**；
- 每张等距全景都密集标注**具身任务问句 + GT 动作**：
  - HOS GT = 把目标对齐到视线中心所需的**最佳头部朝向**；
  - HPS GT = 地面平面上的**单位方向向量**；
- 数据集格式：`hstar_bench`（高分辨率 PNG + parquet 标注），仓库提供切割版与全量版两种评测脚本。

### 5. 关键数字

| 指标 | Qwen2.5-VL-3B-Instruct（base） | HVS-3B（本文） |
|---|---|---|
| HOS 成功率 | 14.83% | **47.38%**（× 3.2） |
| HPS 成功率 | 6.44% | **24.94%**（× 3.9） |

> 提升的核心来源是 **HPS**——找路径需要**对地面几何 + 可通过性的理解**，是 VLM 默认能力的薄弱区，加 RL 后的相对涨幅最大。

---

## 🧭 整体流程（mermaid）

<div class="mermaid">
flowchart TB
    subgraph WORLD["🌍 世界模型: 等距 360° 全景"]
        PANO["🖼️ Equirectangular Panorama<br/>(整个场景一张图)"]
        VIEW["🔭 透视视窗<br/>(yaw, pitch) 决定看哪里"]
    end

    subgraph TASK["🎯 两类视觉搜索任务"]
        HOS["🍎 HOS · 物体搜索<br/>动作 = 头部朝向<br/>目标: 把物体推到视野中心"]
        HPS["🛣️ HPS · 路径搜索<br/>动作 = 地面单位方向向量<br/>目标: 对齐身体朝向到可行路径"]
    end

    subgraph AGENT["🧠 HVS-3B Agent (Qwen2.5-VL-3B-Instruct 微调)"]
        FT["💭 Free-Think<br/>(空间推理 / 多步规划)"]
        ACT["🎯 动作 token<br/>(下一帧朝向 / 终止)"]
    end

    subgraph TRAIN["🏋️ 两段式训练"]
        SFT["📚 冷启动 SFT<br/>(hos_sft / hps_sft)<br/>学格式 + 坐标系"]
        RL["♻️ 掩码 GRPO<br/>(hvs_rl)<br/>动作 token 上回传"]
    end

    subgraph BENCH["📊 H*Bench: 野外 360° benchmark"]
        SC1["🚉 交通枢纽"]
        SC2["🏬 大型零售"]
        SC3["🏙️ 城市街道"]
        SC4["🏛️ 公共机构"]
        METRIC["✅ HOS 14.83% → 47.38%<br/>HPS 6.44% → 24.94%"]
    end

    PANO --> VIEW
    VIEW --> FT
    FT --> ACT
    ACT -- "更新 (yaw, pitch)" --> VIEW

    HOS -. "任务条件" .-> FT
    HPS -. "任务条件" .-> FT

    SFT --> RL
    RL --> AGENT

    AGENT --> BENCH
    SC1 & SC2 & SC3 & SC4 --> METRIC

    ACT -- "HOS 输出" --> GRASP["🦾 下游抓取控制器"]
    ACT -- "HPS 输出" --> WALK["🦶 下游行走控制器"]

    style WORLD fill:#e8f4fd,stroke:#1f78b4
    style TASK fill:#fff7e0,stroke:#d4a017
    style AGENT fill:#f3e8ff,stroke:#8e44ad
    style TRAIN fill:#fde8e8,stroke:#c0392b
    style BENCH fill:#e8fff0,stroke:#2ca02c
</div>

---

## 💡 核心贡献

1. **任务范式**：第一次把"视觉搜索"明确为**为下游行为做前置感知**的两类任务（HOS / HPS），把动作语义直接对齐到抓取 / 行走控制器接口。
2. **世界表示**：用**等距 360° 全景 + 主动视窗**模拟人形头部 / 眼部联合观察，把"转头"这件物理动作压成 VLM 能消费的 token 序列。
3. **训练范式**：在 Qwen2.5-VL-3B 这一**3B 量级**模型上，用**冷启动 SFT + 掩码 GRPO** 把成功率拉高 3 倍以上，证明小模型 + 好任务设计 + RL 是足够的。
4. **基准建设**：H\*Bench 把视觉搜索从家庭场景推到**车站 / 商场 / 街道 / 机场**等真实部署域，并提供高分辨率全景 + 密集动作标注。
5. **完整开源**：模型权重（HVS-3B）+ 训练管线（VAGEN + LLaMA-Factory + verl）+ benchmark 数据全部 Apache 2.0。

---

## 📊 关键发现

| 维度 | 结论 |
|---|---|
| 任务粒度 | "找物体 → 抓"和"找路 → 走"分开训练比统一一个 generic visual search 更稳，**动作语义对齐下游控制器**是关键 |
| 数据形式 | 360° 全景 + 视窗交互天然支持**多步主动观察**，比单图 box prediction 更接近真实人形需求 |
| 训练管线 | 冷启动 SFT 不可省——直接对 3B VLM 跑 GRPO 容易发散；先 SFT 学格式 / 坐标系再 RL 拉性能是稳定路径 |
| 掩码 GRPO | 只对动作 token 回传梯度避免污染思维链，是多模态多轮 agent 用 GRPO 时的工程关键 |
| HPS 难度 > HOS | 路径搜索涉及**地面几何 + 可通过性 + 朝向对齐**，VLM 默认能力最弱，因此提升空间也最大 |

---

## 🤖 对人形 / 具身领域的意义

| 方向 | 含义 |
|---|---|
| **视觉搜索从静态到主动** | 把视觉搜索从"图像问答"重新定义为"机器人主动观察"，给具身 VLM 提供了一个干净的中间任务 |
| **下游控制器的标准接口** | HOS 输出"看哪里"= 抓取的 pre-grasp 视线；HPS 输出"往哪走"= 行走的目标朝向，**直接可消费** |
| **小模型 + 好任务** | 3B 量级 VLM + 掩码 GRPO 就能在野外场景把成功率拉 3×，说明 robot reasoning 不一定要 70B+ 大模型 |
| **与 NaVILA / EgoActor / FocusNav 的位置** | 这三者负责"语义层 / VLA 规划 / 局部注意力"；H\* 负责的是**"我应该把头转去哪里"**这个更底层的感知决策，是它们的**前置或中间层** |

---

## 🎤 面试参考

**Q：为什么不直接训练一个端到端的人形 VLA 模型，非要把"视觉搜索"单独拎出来？**
A：因为视觉搜索是**所有具身行为的前置感知步**。如果把"看哪里"和"做什么"全压在一个端到端模型里，模型很难解释 / 调试，数据也难标。把视觉搜索单独定义、对齐到"头部朝向 / 路径方向"这种**可标注、可评估**的动作空间，相当于把"感知 → 决策"中间最难的一段做成一个独立 module，下游的抓取 / 行走可以单独训练并对接。

**Q：HOS 和 HPS 有什么本质区别？**
A：HOS 的动作语义是**"对齐视线"**——找到 + 把目标推到视野中央，输出是 `(yaw, pitch)`；HPS 的动作语义是**"对齐身体朝向"**——找到一条可行路径，输出是**地面上的单位方向向量**。一个服务抓取，一个服务行走，**评测指标和 ground-truth 标注完全不同**，所以论文要分开做。

**Q：等距 360° 全景作为世界模型有什么好处和坏处？**
A：好处是**一张图覆盖完整 4π 立体角**，agent 通过 (yaw, pitch) 选视窗就能模拟"主动转头"，且全景数据获取便宜（相机绕一圈或拼接）；坏处是**没有深度、没有动态、没有自身运动**——它只能模拟"原地转头看"，不能模拟"边走边看"。所以 H\* 是定位为**行为前置的感知**，不是完整 navigation 解决方案，下游还得接 navigation policy。

**Q：掩码 GRPO 里"掩码"到底掩什么？**
A：掩 reward / 梯度流。VLM 多轮 rollout 里包含三类 token：**观察 token**（视窗图）/ **思维链 token**（free-think）/ **动作 token**（朝向 / 方向）。GRPO 的相对奖励只能与**最终动作**对齐，如果让奖励信号穿过所有 token，模型很容易把奖励"投射"到思维链字面上，导致**胡思乱想能拿高分**。掩码后只在动作 token 处回传 RL 梯度，思维链由 SFT 阶段塑形稳定，RL 只动决策位。

**Q：和 NaVILA / EgoActor / FocusNav 这些导航工作相比，H\* 在哪一层？**
A：可以理解为**主动观察层**：
- **EgoActor / NaVILA**：高层语义 + 任务规划（"去打开冰箱"）；
- **FocusNav / STATE-NAV**：局部导航 + 可通过性（"在这片地形上稳着走"）；
- **H\***：再往前一层，**"我现在该把头转去哪里看"**——是"主动感知"的决策，给上面两层提供它们需要的视觉证据。

---

## 🔗 相关阅读

- [NaVILA (2412.04453)](https://arxiv.org/abs/2412.04453)：人形 VLA 导航，H\* 给它提供"看哪里"的前置感知
- [EgoActor (2602.04515)](https://arxiv.org/abs/2602.04515)：VLM 任务规划，与 H\* 形成"看 → 想 → 做"的接力
- [FocusNav (2601.12790)](https://arxiv.org/abs/2601.12790)：路径点引导注意力，与 HPS 思路有相似处但层级更低
- [STATE-NAV (2506.01046)](https://arxiv.org/abs/2506.01046)：双足稳定性感知可通过性，H\* 的 HPS 输出可作其上游目标
- [GRPO (DeepSeek-Math, 2402.03300)](https://arxiv.org/abs/2402.03300)：本文 RL 阶段沿用的相对优势策略优化
- [Qwen2.5-VL](https://github.com/QwenLM/Qwen2.5-VL)：HVS-3B 的 base 模型
