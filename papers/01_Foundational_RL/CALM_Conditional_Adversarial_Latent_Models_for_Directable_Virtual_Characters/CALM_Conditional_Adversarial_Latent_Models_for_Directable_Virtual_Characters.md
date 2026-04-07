---
layout: paper
paper_order: 8
title: "CALM: Conditional Adversarial Latent Models for Directable Virtual Characters"
zhname: "CALM：条件对抗潜变量模型与可控虚拟角色"
category: "Foundational RL"
---

# CALM: Conditional Adversarial Latent Models for Directable Virtual Characters
**条件对抗潜变量模型：可控虚拟角色**

> 📅 阅读日期: 2026-04-07  
> 🏷️ 板块: Reinforcement Learning / Motion Imitation / Skill Composition

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **arXiv** | [2305.02195](https://arxiv.org/abs/2305.02195) |
| **PDF** | [下载](https://arxiv.org/pdf/2305.02195) |
| **作者** | Chen Tessler, Yoni Kasten, Yunrong Guo, Shie Mannor, Gal Chechik, Xue Bin Peng |
| **机构** | NVIDIA, Technion, Bar-Ilan University, Simon Fraser University |
| **发布时间** | 2023年（SIGGRAPH 2023） |
| **项目主页** | [NVIDIA PAR Lab](https://research.nvidia.com/labs/par/calm/) |
| **GitHub** | [NVlabs/CALM](https://github.com/NVlabs/CALM) |

---

## 🎯 一句话总结

CALM 在 ASE 的基础上加了一层"方向控制"能力——训练一个高层策略学"朝哪个 latent 方向走"来完成指定任务，底层负责动作质量；两者组合起来，用一个简单的状态机就能编出复杂的组合动作，不用额外训练。

---

## 📌 英文缩写速查

| 缩写 | 全称 | 简单解释 |
|------|------|----------|
| **CALM** | Conditional Adversarial Latent Models | 条件对抗潜变量模型：让潜变量可控、可定向 |
| **LLC** | Low-Level Controller | 低层控制器（decoder），接收 latent + 状态，输出动作 |
| **HLC** | High-Level Controller | 高层控制器，选择 latent 来引导低层策略 |
| **ASE** | Adversarial Skill Embeddings | 对抗技能嵌入，CALM 的前身 |
| **AMP** | Adversarial Motion Priors | 对抗运动先验，ASE/CALM 判别器的技术基础 |
| **FSM** | Finite-State Machine | 有限状态机，CALM 推理时组合低层/高层策略的调度器 |
| **MoCap** | Motion Capture | 动作捕捉 |

---

## ❓ CALM 要解决什么问题？

ASE 已经做到：把大量技能压进一个连续 latent 空间 $z$，高层策略只学"选哪个 $z$"。

但 ASE 有一个关键缺陷：

> **它只知道"选什么技能"，不知道怎么控制技能的"方向"。**

比如你给 ASE 一个"走"的 latent，它可以生成一个自然的走路动作——但你没法控制它往哪个方向走、朝哪个目标走。

这就是 CALM 要解决的：

> **在 ASE 的 latent skill space 基础上，加入"方向控制"能力，让角色不仅能做某个技能，还能控制技能的执行方向。**

### 问题一：ASE 没有方向感

ASE 的 latent 只编码"做什么技能"，不编码"朝哪个方向做"。

你给 $z_1$ = 冲刺，$z_2$ = 下蹲——但这两个 latent 都没有"朝左走""朝右走"的信息。

### 问题二：任务完成需要方向，但低层策略没有任务信息

比如任务目标是"追着蓝球跑"。低层策略知道怎么跑，但不知道往哪跑。

传统做法是把目标信息塞进低层策略，但这样：
- 每个新任务都得重训低层
- 低层策略变得很复杂

### 问题三：CALM 的核心洞察

作者发现"方向"其实可以**不编码在 latent 里**，而是**在 latent 空间里选一个方向**。

也就是：
- latent $z$ 编码"做什么"（技能语义）
- 在 latent 空间里选哪个 $z$，决定"朝哪个方向/风格执行"
- 高层策略专门学这个选择逻辑

这样低层和高层各司其职，低层负责质量，高层负责方向。

---

## 🔧 CALM 的三层架构

CALM 分三个阶段，每阶段解决一个问题：

### 第一层：Low-Level Controller（LLC）——动作质量

**目标**：训练一个 encoder-decoder，latent 能编码动作风格。

- **Encoder** $E$：把一段 motion clip 编码成 latent $z$
- **Decoder（低层策略）** $\pi_{LLC}$：输入当前状态 $s_t$ + latent $z$，输出动作 $a_t$

整个 LLC 用对抗模仿学习训练（类似 ASE），判别器保证动作自然。

训练好之后，给一个 $z$，LLC 就能生成对应技能的动作序列。

> **但此时只有"技能"，没有"方向"。**

### 第二层：High-Level Controller（HLC）——方向控制

**目标**：训练一个高层策略，学会在 latent 空间里选方向来完成指定任务。

HLC 的输入：
- 当前状态 $s_t$
- 任务目标（比如"朝目标点走"）

HLC 的输出：
- 一个 latent $z_t$

这个 $z_t$ 传给 LLC，LLC 生成对应技能的动作。

**关键设计：方向奖励**

HLC 的奖励里有一项：

$$
r_{dir} = \cos(z_{target}, z_t)
$$

也就是选出的 latent 和目标风格的 latent 之间的余弦相似度。

这样 HLC 学的是：**"我要朝这个方向完成任务，应该选哪个 latent"**。

### 第三层：推理时组合——FSM 调度

推理时不需要再训练，只要用一个有限状态机组合 LLC 和 HLC：

```
状态机：
  "走" → 调 LLC（固定 latent = "走"的 latent）
  "朝某方向走" → 调 HLC（输出方向 latent）
  "攻击" → 调 LLC（固定 latent = "攻击"的 latent）
```

这就像视频游戏的控制：
- 移动摇杆 → 方向控制
- 按键 A → 攻击技能
- 按键 B → 防御技能

---

## 🚶 具体实例：CALM 如何让角色"追着目标踢剑"

以 SIGGRAPH 演示里的场景为例："crouch-walk toward target → kick → celebrate"。

### 阶段一：训练 LLC

1. 准备动捕数据：走路、下蹲、踢、举手庆祝等多种技能片段
2. Encoder 把每段动捕编码成对应的 latent $z$
3. Decoder（低层策略）学会：给定当前状态 $s_t$ + latent $z$，输出自然动作
4. 判别器保证动作质量

现在，给任意 $z$，LLC 都能生成对应技能的动作——但不能控制方向。

### 阶段二：训练 HLC

**任务**：朝某个方向 crouch-walk。

1. HLC 观察当前状态 $s_t$ + 目标方向
2. HLC 输出一个 latent $z_t$
3. LLC 接收 $z_t$，生成 crouch-walk 动作
4. 环境反馈奖励：如果角色朝正确方向移动，奖励高
5. HLC 学的是：**"朝这个目标走，我应该选哪个 latent"**

### 阶段三：FSM 组合

推理时，用户定义状态机：

```text
状态 1: crouch-walk（调用 HLC，朝目标方向）
  条件: 距离目标 < 1m → 切换到状态 2

状态 2: kick（调用 LLC，固定 latent = "kick"）
  条件: 踢完 → 切换到状态 3

状态 3: celebrate（调用 LLC，固定 latent = "celebrate"）
  条件: 动作完成 → 结束
```

整个过程不需要额外训练，直接组合已有模型。

---

## 🤖 CALM 对人形机器人领域的意义

### 1. 分离"做什么"和"往哪做"，是层次化控制的核心思想

以前大多数方法把任务信息和动作质量混在一起。

CALM 证明了：把它们分开，用层次化策略分别处理，是可行且高效的。

这给后续很多工作打了样。

### 2. FSM 组合证明了"免训练技能拼装"的可行性

CALM 最重要的工程启示之一：**不需要为每个新任务重新训练**，只要写一个 FSM 把预训练好的模块拼起来。

这在真实机器人部署时极其有价值。

### 3. latent space 的方向性有语义含义

CALM 展示了 latent 空间不只是一个"随机向量容器"——它可以有语义结构：
- 相近方向 = 相近技能
- latent 插值 = 技能过渡

这让 latent 控制变得更直觉、更可解释。

### 4. 它是 ASE→CALM→PULSE 链路的关键中间节点

```
ASE:  技能 embedding + encoder-decoder
CALM: 加入方向控制层（HLC）+ FSM 组合
PULSE: 进一步扩展到更大规模、更通用的 latent 基座
```

---

## 📁 MimicKit 源码对照

> CALM 官方代码是独立仓库 [NVlabs/CALM](https://github.com/NVlabs/CALM)，基于 IsaacGym 实现，不在 MimicKit 里。以下对照参考 NVIDIA 官方实现的核心机制。

### 1. 低层策略的 Latent 输入

```python
# CALM 官方实现（calm/models/calm.py 思路）
class ConditionalAdversarialLatentModel(nn.Module):
    def __init__(self, latent_dim=32):
        self.encoder = MotionEncoder(latent_dim=latent_dim)
        self.decoder = LowLevelPolicy(latent_dim=latent_dim)
        self.discriminator = MotionDiscriminator()

    def encode(self, motion_sequence):
        # 把一段 motion clip 编码成 latent
        z = self.encoder(motion_sequence)
        return z

    def decode(self, state, z):
        # 给定状态 + latent，输出动作
        in_data = torch.cat([state, z], dim=-1)
        action_dist = self.decoder(in_data)
        return action_dist
```

**关键**：latent $z$ 不仅仅是噪声，而是从**真实参考动作**里提取出来的有语义的方向向量。

### 2. 高层策略的 latent 选择

```python
# 高层策略输出 latent（而非直接输出动作）
class HighLevelController(nn.Module):
    def __init__(self, latent_dim=32):
        self.net = nn.Sequential(
            nn.Linear(state_dim + goal_dim, 512),
            nn.ReLU(),
            nn.Linear(512, latent_dim)
        )

    def forward(self, state, goal):
        z = self.net(torch.cat([state, goal], dim=-1))
        z = F.normalize(z, dim=-1)  # 归一化到单位球面
        return z
```

高层输出的 latent 再传给低层策略——这正是"选 latent"而非"直接选动作"的核心。

### 3. 方向奖励

```python
def compute_direction_reward(z_selected, z_target):
    # 余弦相似度作为方向奖励
    cos_sim = F.cosine_similarity(z_selected, z_target, dim=-1)
    return cos_sim  # 选出的 latent 和目标 latent 越接近，奖励越高
```

### 4. FSM 组合

```python
# 推理时的状态机逻辑
class FSMScheduler:
    def __init__(self, llc, hlc):
        self.llc = llc   # 低层策略
        self.hlc = hlc   # 高层策略

    def step(self, state, current_mode, goal):
        if current_mode == "direction_locomotion":
            z = self.hlc.select_latent(state, goal)  # HLC 选方向
            action = self.llc.decode(state, z)
        elif current_mode == "fixed_skill":
            z = self.llc.encode(self.fixed_motion)    # 用参考动作的 latent
            action = self.llc.decode(state, z)
        return action
```

### 5. 训练命令（NVIDIA 官方）

```bash
# 阶段一：训练低层控制器（LLC）
python calm/run.py \
  --task HumanoidAMPGetup \
  --cfg_env calm/data/cfg/humanoid_calm_sword_shield_getup.yaml \
  --cfg_train calm/data/cfg/train/rlg/calm_humanoid.yaml \
  --motion_file calm/data/motions/reallusion_sword_shield/dataset_reallusion_sword_shield.yaml \
  --headless --track

# 阶段二：训练方向控制高层策略
python calm/run.py \
  --task HumanoidHeadingConditioned \
  --cfg_env calm/data/cfg/humanoid_sword_shield_heading_conditioned.yaml \
  --cfg_train calm/data/cfg/train/rlg/hrl_humanoid_style_control.yaml \
  --motion_file calm/data/motions/reallusion_sword_shield/dataset_reallusion_sword_shield_fsm_movements.yaml \
  --llc_checkpoint calm/data/models/calm_llc_reallusion_sword_shield.pth \
  --headless --track

# 阶段三：FSM 推理（不训练）
python calm/run.py \
  --task HumanoidStrikeFSM \
  --test \
  --num_envs 16 \
  --llc_checkpoint calm/data/models/calm_llc_reallusion_sword_shield.pth \
  --checkpoint calm/data/models/calm_hlc_precision_trained_reallusion_sword_shield.pth
```

### 6. 内置任务配置

| 任务 | 配置文件 | 说明 |
|------|----------|------|
| HumanoidStrikeFSM | `humanoid_sword_shield_strike_fsm.yaml` | 攻击 FSM |
| HumanoidLocationFSM | `humanoid_sword_shield_location_fsm.yaml` | 位置控制 FSM |
| HumanoidReach | `humanoid_sword_shield_reach.yaml` | 到达目标 |
| HumanoidHeading | `humanoid_sword_shield_heading.yaml` | 朝方向走 |
| HumanoidStrike | `humanoid_sword_shield_strike.yaml` | 精确攻击 |

---

## 🎤 面试高频问题 & 参考回答

### Q1: CALM 和 ASE 的核心区别是什么？
**A**：ASE 只学了一个 latent skill space，低层策略给定 $z$ 能生成对应技能，但没有方向控制能力。CALM 在 ASE 基础上加了一层高层策略（HLC），专门学"朝哪个 latent 方向走"来完成指定任务，实现了对技能执行方向的控制。

### Q2: CALM 的 FSM 组合有什么价值？
**A**：FSM 把预训练好的低层和高层策略当成模块拼起来，不需要为每个新任务重新训练整个系统。这对真实机器人部署极其重要——你可以预先训练好各种技能模块，用状态机实时组合出复杂行为。

### Q3: 为什么 HLC 输出 latent 而不是直接输出动作？
**A**：因为 latent 编码了"技能语义"，传给 LLC 后能保证动作质量和风格。如果 HLC 直接输出动作，就绕过了低层的质量保证，丢失了对抗模仿学习训练出的自然运动特性。

### Q4: CALM 的方向奖励是什么？
**A**：是 HLC 选出的 latent 和目标风格 latent 之间的余弦相似度。HLC 被鼓励选出让 $\cos(z_{selected}, z_{target})$ 最大的 latent，从而引导角色朝目标风格运动。

### Q5: CALM 的 latent space 有什么特点？
**A**：它是语义化的——相近的 latent 对应相近的技能；latent 插值会得到平滑的技能过渡。这意味着可以在 latent 空间里做有意义的线性插值，比如从"冲刺"到"下蹲"的过渡会产生语义连贯的中间动作。

---

## 💬 讨论记录

### 2026-04-07：CALM 的真正贡献是"层次化解耦"而非新算法

CALM 用的核心技术（对抗模仿、latent skill embedding）在 ASE/AMP 里都有了。

CALM 的真正贡献是架构设计：

> **把"技能选择"和"方向控制"分开成两个问题，用层次化策略分别解决。**

这个设计思想影响了后来很多工作，包括 PULSE 和更广义的 motion foundation model 设计。

---

## 📎 附录

### A. 与路线图其他论文的关联

| 关系 | 说明 |
|------|------|
| **ASE → CALM** | CALM 在 ASE 的 latent skill space 基础上加入方向控制层 |
| **AMP → CALM** | CALM 的低层判别器技术继承自 AMP |
| **CALM → PULSE** | PULSE 把 CALM 的 latent 思想扩展到更大规模的通用技能提取 |

### B. 与相关方法对比

| 特性 | ASE | CALM | DeepMimic |
|------|-----|------|-----------|
| 核心目标 | 多技能 latent | 可控多技能 latent | 单技能精确模仿 |
| 是否有方向控制 | ❌ | ✅ | ❌ |
| 是否有层次化架构 | ❌ | ✅（两层） | ❌ |
| 是否支持 FSM 组合 | ❌ | ✅ | ❌ |
| latent 是否语义化 | 部分 | ✅（方向有语义） | N/A |

### C. 你该怎么理解 CALM？

如果只记一句：

> **CALM 在 ASE 的技能 latent 空间上加了"方向舵"，用高层策略选 latent 来控制运动方向，用 FSM 组合出复杂行为。**

如果再加一句：

> **它的核心思想是把"做什么"（技能）和"往哪做"（方向）分开——前者由 latent 决定，后者由高层策略决定。**

---

## 参考来源

- arXiv: https://arxiv.org/abs/2305.02195  
- NVIDIA PAR Lab: https://research.nvidia.com/labs/par/calm/  
- GitHub: https://github.com/NVlabs/CALM  

> 注：本文内容基于论文 SIGGRAPH 2023 版本、NVIDIA 官方项目主页与 GitHub 源码整理；部分直觉解释和工程细节属于我的归纳，不是论文原文直述。
