---
layout: paper
paper_order: 1
title: "Robust and Generalized Humanoid Motion Tracking"
zhname: "鲁棒且通用的人形机器人动作跟踪：用动力学条件化的命令聚合抵御噪声参考"
category: "全身控制"
---

# Robust and Generalized Humanoid Motion Tracking
**鲁棒且通用的人形机器人动作跟踪：用动力学条件化的命令聚合抵御噪声参考**

> 📅 阅读日期: 2026-05-17
>
> 🏷️ 板块: 04 Loco-Manipulation / WBC · 动作跟踪 / 单策略全身控制
>
> 🔁 推进轨: 模块轮转（14_Human_Motion → **04_Loco-Manipulation_and_WBC**）

---

## 📋 基本信息

| 项目 | 链接 |
|---|---|
| arXiv | [2601.23080](https://arxiv.org/abs/2601.23080) |
| PDF | [arXiv PDF](https://arxiv.org/pdf/2601.23080) |
| HTML | [arXiv HTML](https://arxiv.org/html/2601.23080v1) |
| 项目主页 | [zeonsunlightyu.github.io/RGMT.github.io](https://zeonsunlightyu.github.io/RGMT.github.io/) |
| 项目仓库 | [zeonsunlightyu/RGMT.github.io](https://github.com/zeonsunlightyu/RGMT.github.io)（目前为项目页仓库，训练代码截至论文发布暂未公开） |
| 作者 | Yubiao Ma, Han Yu, Jiayin Xie, Changtai Lv, Qiang Luo, Chi Zhang, Yunpeng Yin, Boyang Xing, Xuemei Ren, Dongdong Zheng |
| 机构 | Beijing Institute of Technology 等 |
| **发布时间** | 2026-01-30 (arXiv) |
| 发表时间 | 2026-01-30（arXiv） |
| 评测平台 | Unitree G1（29 DoF）真机 + 仿真 |

---

## 🎯 一句话总结

> 在通用人形动作跟踪里，**参考动作本身就是带噪声、可能违反机器人动力学的**——本文用「**动力学条件化的命令聚合**（dynamics-conditioned command aggregation）」让策略**自己**根据当前本体动力学去**挑**该执行的命令片段，再叠加一套不稳定初始化 + 渐弱上拉力的摔倒恢复课程，得到**一个**只需 ~3.5 小时数据即可零样本泛化到新动作、并能稳定落地 G1 的单一通用策略。

---

## ❓ 论文要解决什么问题？

通用全身动作跟踪（"一个策略追任意人体动作"）有三个反复被踩的坑：

1. **参考动作天生带噪**：人体→机器人重定向后，存在足滑、自碰撞、关节越界、力矩瞬变等**局部缺陷**，闭环执行会放大这些误差，最终把策略带飞。
2. **高动态 / 富接触行为下漂移严重**：传统做法直接把参考逐帧塞给策略，缺乏"该听 / 不该听"的判别能力。
3. **训练流水线复杂**：很多工作要靠多教师蒸馏、分阶段课程，数据规模动辄数十小时。

作者要的是：**一个端到端策略**，能容忍参考噪声、在富接触和摔倒后稳定恢复，并且**只用 ~3.5 小时动捕数据**就训出来。

---

## 🔧 方法详解

### 1. 因果时序编码器（Causal Temporal Encoder）

- 输入：最近若干帧的**本体感知**（proprioception，关节角 / 速度 / 重力方向 / 上一时刻动作等）。
- 用一个因果（causal）时间序列编码器把"机器人当前的动力学状态"压成一个紧凑表征 $h_t$。
- 这个 $h_t$ 表达的是「**我现在能做什么 / 我现在不稳在哪里**」。

### 2. 多头交叉注意力命令编码器（Multi-Head Cross-Attention Command Encoder）

- 输入：参考动作在当前时刻附近的一个**上下文窗口**（多帧目标姿态 / 速度 / 关键点位置）。
- 以 $h_t$ 作为 query，跨参考帧做 cross-attention，让网络**根据当前动力学**有选择地聚合上下文窗口，**降权那些不一致的参考片段**。
- 直观理解：网络不再"逐帧死追"，而是"看清自己再决定看参考的哪几帧"。

### 3. 摔倒恢复课程（Fall Recovery Curriculum）

- **随机不稳定初始化**：训练开始时从倾倒 / 半摔状态出发，强迫策略学会先把姿态拉回来再追动作。
- **退火上拉力（annealed upward assistance force）**：早期施加沿 base 向上的辅助力托住机器人，让它能"先学到正向反馈"；力随训练步数退火到 0，逐渐放手让策略自己站稳。
- 效果：摔倒后能恢复 + 在外部扰动下保持稳定，无需额外蒸馏一个 fall-recovery 专家。

### 4. 单阶段端到端训练（No Distillation）

- 训练数据仅 **~3.5 小时**人体动作；
- 不需要多教师 → 学生蒸馏，不需要分阶段课程切换；
- 一次 PPO 风格的 RL 直接训完，部署时就是同一张网络。

---

### 🧭 整体流程（mermaid）

<div class="mermaid">
flowchart LR
    subgraph IN["📥 输入"]
        REF["📜 参考动作上下文窗口<br/>(t-W ... t+W 帧)<br/>已重定向到 G1，含噪声"]
        PROP["🦿 本体感知历史<br/>(关节角/速度/重力/上一动作)"]
    end

    subgraph ENC["🧠 双编码器"]
        TENC["⏱ 因果时序编码器<br/>Causal Temporal Encoder<br/>→ 动力学表征 h_t"]
        CENC["🎯 命令编码器<br/>Multi-Head Cross-Attn<br/>q=h_t, kv=参考窗口"]
    end

    subgraph CUR["🛟 摔倒恢复课程"]
        RAND["🎲 随机不稳定初始化"]
        FORCE["⬆ 退火上拉力<br/>annealed upward assist"]
    end

    POL["🤖 策略网络 π(a#124;·)"]
    ENV["🌍 仿真环境 (G1 29 DoF)"]
    REAL["🚶 G1 真机部署<br/>零样本到新动作"]

    PROP --> TENC
    TENC --> CENC
    REF --> CENC
    CENC --> POL
    TENC --> POL
    CUR --> ENV
    POL --> ENV
    ENV --闭环反馈--> PROP
    POL ==单一策略 / 无蒸馏==> REAL

    style IN fill:#e8f4fd,stroke:#1f78b4,color:#0b3954
    style ENC fill:#fef6e4,stroke:#d35400,color:#5e2c00
    style CUR fill:#fde2e2,stroke:#c0392b,color:#5d1a14
</div>

---

## 💡 核心贡献

1. **动力学条件化的命令聚合**：第一次把"是否听参考"显式建模成「**用当前动力学 query 参考窗口**」的 cross-attention，原生具备对噪声参考的容错能力。
2. **极简训练流水线**：~3.5 h 动作数据、单阶段、无蒸馏，仍能覆盖跑跳、舞蹈、富接触等多类行为。
3. **摔倒恢复 + 动作跟踪一体化**：随机不稳定初始化 + 退火上拉力把"恢复"折叠进同一个策略，避免显式切换专家。
4. **G1 真机零样本验证**：在 29 DoF Unitree G1 上对未见过动作做 zero-shot 跟踪，并展示外扰下的稳定性。

---

## 📊 与同期 motion-tracking 工作的关系

| 方法 | 核心思路 | 处理噪声参考 | 训练流水线 |
|---|---|---|---|
| ExBody / ExBody2 | 动作分层 + 上半身放宽 | 手工筛动作 | 多阶段 |
| HOVER | 多模态 versatile controller | 教师蒸馏 | 多阶段蒸馏 |
| GMT | scalable general motion tracker | 大规模数据 + 加权 | 单阶段，但依赖大数据 |
| OmniH2O / TWIST | 遥操作驱动跟踪 | 在线人类介入 | 多阶段 |
| **RGMT（本文）** | **动力学条件化 cross-attn + 摔恢复课程** | **结构上选择性聚合** | **单阶段、~3.5 h 数据、无蒸馏** |

---

## 🤖 工程价值

- **少数据强泛化**：~3.5 h 数据 + 一张策略就能上 G1，对国内大量"无法跑大规模数据采集"的实验室很友好。
- **抗噪结构是底座**：随着 retargeting / motion captioning / 视频生成动作来源越来越多，"参考自带噪声"将是常态；本文的 cross-attn 聚合范式是个可复用的模块化设计。
- **稳态行为兜底**：把摔倒恢复折进同一个策略，避免上层做状态机 switch，工程上更干净。

---

## 🎤 面试参考

**Q：为什么 cross-attention 比直接拼接参考更适合处理噪声参考？**
A：直接拼接相当于让网络"看到所有帧"，但权重需要网络自己分。Cross-attention 显式地用动力学表征作 query、参考窗口作 key/value，给"哪些帧值得听"提供了归纳偏置，对噪声片段天然下采样。

**Q：退火上拉力是不是相当于 reward shaping？会不会让策略学到依赖外力的捷径？**
A：退火（annealing）就是为了避免捷径——训练前期辅助、后期归零，强迫策略最终在没有外力的情况下站稳；这与课程学习里的"先易后难"一致。

**Q：单一策略同时做跟踪 + 摔恢复，会不会两者打架？**
A：两者共享的是"先稳后追"的优先级。随机不稳定初始化让策略大量见到失衡状态，进而把"恢复"内化为跟踪策略的子能力，而不是显式切换。

---

## 🔗 相关阅读 / 后续延伸

- **同期通用跟踪**：[GMT (2506.14770)](https://arxiv.org/abs/2506.14770)、[ResMimic (2510.05070)](https://arxiv.org/abs/2510.05070)、[Track Any Motions under Any Disturbances (2509.13833)](https://arxiv.org/abs/2509.13833)、[RobotDancing (2509.20717)](https://arxiv.org/abs/2509.20717)
- **多模态 versatile controller**：[HOVER (2410.21229)](https://arxiv.org/abs/2410.21229)、[HugWBC (2502.03206)](https://arxiv.org/abs/2502.03206)
- **Retargeting 噪声来源**：[Retargeting Matters (2510.02252)](https://arxiv.org/abs/2510.02252)、[GMR](https://github.com/YanjieZe/GMR)
- **摔倒恢复课程**：[HiFAR (2502.20061)](https://arxiv.org/abs/2502.20061)、[Learning Getting-Up Policies (2502.12152)](https://arxiv.org/abs/2502.12152)

---

> 备注：训练代码截至论文发布暂未在仓库 `zeonsunlightyu/RGMT.github.io` 公开（目前为项目页内容），后续如释出可在本节追加。
