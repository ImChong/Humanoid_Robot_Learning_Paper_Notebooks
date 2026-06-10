---
layout: paper
title: "UH-1: Learning from Massive Human Videos for Universal Humanoid Pose Control"
category: "高影响力精选 High Impact Selection"
subcategory: "Whole-Body Control Core"
zhname: "UH-1：从海量互联网人类视频中学习通用人形姿态控制"
---

# UH-1: Learning from Massive Human Videos for Universal Humanoid Pose Control
**UH-1：从海量互联网人类视频中学习通用人形姿态控制**

> 📅 阅读日期: 2026-05-21
>
> 🏷️ 板块: 03_High_Impact_Selection / Whole-Body Control Core（H6）
>
> 🧭 状态: 首版基础摘要（含 mermaid 流程图），覆盖 Humanoid-X 数据流水线、UH-1 Transformer 与文本→动作两种控制接口；后续可在跑通官方 checkpoint 后补充消融与定量结果。

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **arXiv** | [2412.14172](https://arxiv.org/abs/2412.14172) |
| **HTML** | [arxiv.org/html/2412.14172](https://arxiv.org/html/2412.14172) |
| **PDF** | [arxiv.org/pdf/2412.14172](https://arxiv.org/pdf/2412.14172) |
| **项目主页** | [usc-gvl.github.io/UH-1](https://usc-gvl.github.io/UH-1/) |
| **发布时间** | 2024-12-18 (arXiv) |
| **源码（官方）** | [github.com/sihengz02/UH-1](https://github.com/sihengz02/UH-1) |
| **模型权重** | [huggingface.co/USC-PSI-Lab/UH-1](https://huggingface.co/USC-PSI-Lab/UH-1) |
| **数据集** | Humanoid-X（163,800 段视频 · 20M+ 帧 · 约 240 h） |
| **作者** | Jiageng Mao*、Siheng Zhao*、Siqi Song*、Tianheng Shi、Junjie Ye、Mingtong Zhang、Haoran Geng、Jitendra Malik、Vitor Guizilini、Yue Wang |
| **机构** | USC · UC Berkeley · Toyota Research Institute |
| **发表** | arXiv 2024-12-18；**Humanoids 2025 Oral** |
| **机器人** | Unitree H1（实机部署） |

---

## 🎯 一句话总结

UH-1 把「文本 → 人形动作」做成一个 GPT 风格的离散自回归问题：先用一条全自动流水线把 16 万条互联网视频清洗、打 caption、估计 SMPL 姿态、重定向到机器人、再用 PPO 蒸馏出可上机器人执行的低层动作，得到 20M+ 帧的 **Humanoid-X** 数据集；再用 VQ-VAE 把这些动作离散成 motion token，用一个 Transformer 自回归生成 token，解码后驱动 Unitree H1，使人形机器人第一次具备「直接听文本指令做姿态控制」的能力。

---

## 📌 英文缩写速查

| 缩写 | 全称 | 简单解释 |
|------|------|----------|
| **DoF** | Degree of Freedom | 关节自由度，机器人控制目标维度 |
| **SMPL** | Skinned Multi-Person Linear model | 参数化人体姿态模型，pipeline 中作为人体表示 |
| **VQ-VAE** | Vector-Quantized VAE | 把连续动作离散成 token 的 codebook 模型 |
| **PD** | Proportional-Derivative | 把目标 DoF 转换成扭矩的底层 PID 控制器 |
| **PPO** | Proximal Policy Optimization | 训练 goal-conditioned 低层策略 π 的 RL 算法 |
| **CLIP** | Contrastive Language-Image Pre-training | UH-1 中用作 text encoder |
| **FID** | Fréchet Inception Distance | 评估生成动作与真实动作分布的相似度 |
| **MM Dist** | Multi-Modal Distance | 文本-动作匹配度，越低越好 |
| **HumanoidML3D** | HumanML3D 的人形版本 | 将 HumanML3D 上的人体动作重定向到机器人形成的评测集 |

---

## ❓ 论文要解决什么问题？

人形控制的「数据瓶颈」问题：

1. **RL 路线**只能在仿真里训行走 / 跳跃等少数技能，技能种类受 reward 工程限制，不够通用；  
2. **遥操作路线**需要大量人工实采，数据规模天花板低；  
3. **机械臂用 internet video** 学到的 affordance / world model 不能直接搬到人形 —— 关节结构、DoF、动力学完全不同。

UH-1 给出的答案是：**把 internet 上海量人类视频"管线化"翻译成机器人能执行的动作样本**，再用一个 transformer 在文本条件下生成动作 token；规模放大同时享受到语言的语义泛化和动作的物理可执行性。

---

## 🔧 方法详解

### 1. Humanoid-X：自动化视频 → 机器人动作流水线（5 步）

| 步骤 | 模块 | 产物 |
|---|---|---|
| ① 视频挖掘 | 学术数据集 + 视频理解数据集 + 400+ YouTube 关键词 + 单人检测 + 运动检测 + 64 帧最短长度 | 163,800 段「单人、有动作、20 FPS」的视频片段 𝒱 |
| ② Caption | 视频字幕模型，prompt 引导只描述「动作」不描述「外观」 | 文本描述 𝒯 |
| ③ 3D 人体姿态 | 基于视频的 SMPL 估计器，附带相机参数 → 全局 root 平移 | 𝒫_human(β, θ, t_root) |
| ④ 重定向 | 12 个对齐关节（hip/knee/ankle/shoulder/elbow/wrist）；先优化 β 使 T-pose 关节长度对齐机器人；FK 取关节 → IK 取 DoF（Adam + 平滑项） | 高层关键点 𝒫_robot、低层关节角 q_robot |
| ⑤ Goal-conditioned RL | PPO + (motion reward + root 跟踪 reward + 稳定性 reward)，把"理想轨迹"补成"机器人能稳定执行的轨迹" | 实机可部署的动作序列 𝒜_robot |

最终每条样本是 5 模态元组 ⟨𝒱, 𝒯, 𝒫_human, 𝒫_robot, 𝒜_robot⟩，共 20M+ 帧 / ~240 h。

### 2. UH-1：文本 → 离散动作 Token → 机器人动作

- **动作 Tokenizer (VQ-VAE)**：把每 K 帧动作打包成一个 token，比逐帧 token 更平滑、序列长度更短；重建 loss 同时约束位置和一阶差分（关键，避免抖动）。
- **UH-1 Transformer**：以 CLIP 文本 embedding 作为条件，**自回归**解码 motion token，[End] token 控制结束。学习目标是标准的 NLL。
- **两条出口（论文 Fig. 5）**：
  - **text-to-keypoint**：先生成 𝒫_robot 再由 goal-conditioned 策略 π 闭环执行（更鲁棒）；
  - **text-to-action**：直接生成 𝒜_robot 通过 PD 开环执行（更直接，部署成本低）。

### 3. 实机部署

Unitree H1 上做了一组语言控制实验，论文给出**接近 100% 成功率**；同时在 HumanoidML3D 基准（HumanML3D 重定向到人形）上，FID / MM Dist / R-Precision 都优于 MDM、T2M-GPT 等先 generate 人 motion 再 retarget 的两阶段基线。

---

## 🧭 整体框架（mermaid）

<div class="mermaid">
flowchart TB
    subgraph PIPE["🏭 Humanoid-X 数据流水线 (5 步)"]
        V["① Internet Video<br/>163.8K clips<br/>20 FPS, 单人+动作"]
        T["② Video Caption<br/>动作中心化 prompt<br/>→ 文本 𝒯"]
        H["③ SMPL 3D Pose<br/>视频估计器<br/>→ 𝒫_human(β,θ,t_root)"]
        R["④ Retargeting<br/>12 关节对齐 + FK/IK<br/>→ 𝒫_robot, q_robot"]
        P["⑤ Goal-conditioned PPO<br/>motion + root + 稳定<br/>→ 𝒜_robot"]
        V --> T --> H --> R --> P
    end

    subgraph TRAIN["🧩 UH-1 训练"]
        TOK["VQ-VAE Tokenizer<br/>K 帧 → 1 motion token<br/>L1 + 一阶差分 loss"]
        TXT["CLIP Text Encoder<br/>𝒯 → embedding l"]
        TR["UH-1 Transformer<br/>自回归 P(z_i #124; z_{1:i-1}, l)<br/>[End] 终止"]
        TOK --> TR
        TXT --> TR
    end

    subgraph INFER["🤖 推理 / 部署"]
        MODE1["text-to-keypoint<br/>(闭环, 走 π)"]
        MODE2["text-to-action<br/>(开环, 直接 PD)"]
        PI["Goal-conditioned 策略 π"]
        PD["PD 控制器<br/>→ 电机扭矩"]
        H1["Unitree H1<br/>实机部署"]
        TR --> MODE1 --> PI --> PD --> H1
        TR --> MODE2 --> PD
    end

    PIPE -. 20M+ 帧训练样本 .-> TRAIN

    style PIPE fill:#e8f4fd,stroke:#1f78b4,color:#0b3d5c
    style TRAIN fill:#fdebd0,stroke:#e67e22,color:#7a3e00
    style INFER fill:#e8f8e8,stroke:#27ae60,color:#0b3d1a
</div>

---

## 📊 实验亮点

- **HumanoidML3D 基准**：UH-1 在 FID (0.445) / MM Dist (3.249) / R-Precision (0.761) 上同时领先 MDM、T2M-GPT；Diversity 与 T2M-GPT 持平、显著高于 oracle。
- **数据规模消融**：把训练样本量从 1k 量级一路放到 16 万级，FID / R-Precision 单调改善，验证 Humanoid-X 规模的实际收益。
- **两阶段 vs 端到端**：直接 text→humanoid 的 UH-1 优于"text→human→retarget"两阶段，说明 retargeting 阶段的信息损失非平凡。
- **真机部署**：Unitree H1 上 12 类文本指令（挥手、拥抱、踢腿、转身、太极等）成功率近 100%（论文 Fig. 6）。

---

## 🤖 对人形机器人领域的意义

| 方向 | 含义 |
|------|------|
| **数据范式** | 第一次系统性地把「YouTube → 机器人可部署动作」做成一条端到端流水线，是人形控制走向 internet-scale 的关键基础设施 |
| **控制接口** | 把「自然语言」直接做成人形控制的顶层 prompt 接口，与 GR00T / VLA 这类 system-2 模型天然兼容 |
| **模型架构** | 用 motion token + Transformer 复刻了 LLM 的 scaling pattern，与同期 BeyondMimic / SONIC / GMT 的「连续策略 + 大规模 MoCap」路线形成有意思的对照 |
| **数据集贡献** | Humanoid-X 是目前规模最大的「视频→人形动作」对齐数据集之一，已在 HuggingFace 公开，后续 humanoid foundation model 的常用基线之一 |
| **工程链路** | retargeting + RL 蒸馏的两层结构（高层关键点闭环 / 低层 DoF 开环）为后续工作提供了清晰可拆解的 reference pipeline |

---

## 🎤 面试参考

**Q：UH-1 为什么要把动作离散成 token，连续动作不行吗？**  
A：核心动机是「把人形控制对齐到 LLM 的 scaling pattern」——离散 token 之后训练目标就是 NLL，配合 Transformer 自回归既能用 teacher-forcing 高效训练、又能在推理时灵活控制序列长度（[End] token 自然结束）。并且 VQ-VAE 的 codebook 把高维相邻的动作压成同一个 token，等价于学到了一组"motion primitives"，有助于语义级的组合泛化。逐帧 K=1 会让序列过长且容易抖，所以 UH-1 把 K 帧打包成一个 token 同时加一阶差分 loss 保持时间平滑。

**Q：流水线第 5 步为什么还要 PPO 蒸馏？直接执行重定向出来的 q_robot 不行吗？**  
A：因为 IK 出来的 q_robot 只是"几何上对齐"，不带任何稳定性 / 动力学约束 —— 真机执行多半会翻、关节会撞极限、轨迹会跳变。Goal-conditioned PPO 的作用是把"理想轨迹"重写成"机器人能稳定跟住的轨迹"，相当于把 retargeting 的 dream-track 投影到机器人可行流形上。这一步是流水线能输出"可上机"动作的关键。

**Q：UH-1 与 BeyondMimic / SONIC 这类大规模 motion tracker 的本质区别？**  
A：两条路线的 *接口* 完全不同：tracker 路线接口是「参考 motion 序列」，需要外部有 motion 生成器（GENMO / VR teleop）才能驱动；UH-1 直接接「自然语言」，自己包揽 text → motion → action 整个链路。代价是 UH-1 的低层执行依赖一个相对小的 goal-conditioned 策略，对高动态、复杂接触不如专门 tracker；两者更像是 system-2 接口 vs system-1 内核的对应关系，可以叠用。

**Q：和 text-to-human-motion（MDM、T2M-GPT）有什么不同？为什么不直接两阶段？**  
A：两阶段「先生成人 motion 再 retarget」会累积两层误差：MDM/T2M-GPT 的生成误差 + retarget 的几何/动力学误差，且 retargeting 在生成阶段是"事后"信息，模型无法预先规避不可执行姿态。UH-1 把目标分布直接定义在人形动作上，模型在训练时就已经把"机器人能执行什么"内化到 codebook 中，这是它在 HumanoidML3D 上同时拿下 FID 与 R-Precision 的根因。

**Q：Humanoid-X 数据集的局限是什么？**  
A：① caption 都是粗粒度动作描述，缺少细颗粒度（指令-参数）；② SMPL pose 估计依赖单目视频精度，复杂遮挡/快速运动会引入噪声；③ retargeting 只用 12 关节对齐，手指 / 表情 / 接触力等信息丢失；④ goal-conditioned RL 用 PPO 在仿真训练，sim2real gap 与 motor 极限对一些极端动作（连续后空翻、急停冲撞）仍是瓶颈。

---

## 🔗 相关阅读

- [HOVER (2410.21229)](https://arxiv.org/abs/2410.21229)：versatile WBC，下游可作为 UH-1 低层策略的替代方案
- [SONIC (2511.07820)](https://arxiv.org/abs/2511.07820)：大规模 motion tracker，与 UH-1 形成"接口 vs 跟踪器"的互补
- [HumanPlus / OmniH2O / HOMIE]：teleop / motion-imitation 路线，对照理解 UH-1 不需要遥操作即可学动作
- [MDM (2209.14916)](https://arxiv.org/abs/2209.14916) / [T2M-GPT (2301.06052)](https://arxiv.org/abs/2301.06052)：text-to-human-motion 基线，对照理解为什么端到端优于两阶段
- [HumanML3D (2022)](https://github.com/EricGuo5513/HumanML3D)：HumanoidML3D 的来源
- [GR00T N1.5 / VLA]：上游 system-2 模型，可接 UH-1 作为人形 system-1 控制接口
