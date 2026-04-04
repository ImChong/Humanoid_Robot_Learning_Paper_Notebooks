---
layout: paper
title: "PHC: Perpetual Humanoid Control for Real-time Simulated Avatars"
category: "Foundational RL"
---

# PHC: Perpetual Humanoid Control for Real-time Simulated Avatars
**永续人形控制：面向实时仿真虚拟角色**

> 📅 阅读日期: -  
> 🏷️ 板块: Reinforcement Learning / Motion Imitation / Fault Recovery

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **arXiv** | [2305.06456](https://arxiv.org/abs/2305.06456) |
| **PDF** | [下载](https://arxiv.org/pdf/2305.06456) |
| **作者** | Zhengyi Luo, Jinkun Cao, Alexander W. Winkler, Kris Kitani, Weipeng Xu |
| **机构** | Carnegie Mellon University, Meta Reality Labs |
| **发布时间** | 2023年（ICCV 2023） |
| **项目主页** | [zhengyiluo.github.io/PHC](https://zhengyiluo.github.io/PHC/) |
| **代码** | [GitHub](https://github.com/ZhengyiLuo/PHC) |

---

## 🎯 一句话总结

PHC 通过**渐进式乘法控制策略（PMCP）**，让仿真人形角色能模仿上万条动作序列、从摔倒中自然恢复、永不需要 reset——是从 DeepMimic "单动作模仿"迈向"大规模通用控制"的关键一步。

---


## 📌 英文缩写速查
| 缩写 | 全称 | 中文 |
|------|------|------|
| PHC | Perpetual Humanoid Control | 永续人形控制 |
| PMCP | Progressive Multiplicative Control Policy | 渐进式乘法控制策略 |
| MCP | Multiplicative Compositional Policies | 乘法组合策略 |
| PNN | Progressive Neural Networks | 渐进式神经网络 |
| RSI | Reference State Initialization | 参考状态初始化 |
| RET | Relaxed Early Termination | 放松早停 |
| AMP | Adversarial Motion Priors | 对抗运动先验 |
| AMASS | Archive of Motion Capture as Surface Shapes | 动作捕捉数据集 |
| SMPL | Skinned Multi-Person Linear Model | 蒙皮多人线性模型 |
| PD | Proportional-Derivative | 比例-微分控制 |
| PULSE | Physics-based Universal Latent Skill Extraction | 基于物理的通用潜在技能提取 |
---
## ❓ 这篇论文要解决什么问题？

回顾一下我们的学习路线：DeepMimic 解决了"如何模仿一段动作"的问题。但实际应用中，问题远不止于此：

### 问题一：大规模学习的灾难性遗忘

假如你有 10000 段不同的动作捕捉数据（走路、跑步、跳舞、翻跟斗……），想让一个策略网络全都学会。

- **直接训全部**：简单动作（走路）学会了，但复杂动作（后空翻）总学不好
- **先学简单再学复杂**：学会后空翻了，但走路又忘了（灾难性遗忘）
- **用多个独立策略**：每个动作一个网络？那 10000 个网络怎么切换？

> 💡 **类比**：就像一个钢琴学生，先学了《小星星》再学《钢琴协奏曲》——学完协奏曲回头弹《小星星》反而手生了。需要一个"不忘旧技能、还能学新技能"的方法。

### 问题二：摔倒后怎么办？

DeepMimic 和之前的方法有个共同问题：角色一旦偏离参考动作太多就直接 reset 重来。但真实应用中（比如 VR 虚拟角色），你不能让角色摔倒后"消失重置"。

- 之前的方案用**外部稳定力**（invisible hand）帮角色站稳——但这不真实
- PHC 的目标是：**不用任何外力，角色摔倒后自己爬起来继续**

### 问题三：输入噪声

真实使用中，参考动作来自视频姿态估计或文本生成，噪声很大。控制器需要对噪声输入鲁棒。

---

## 🔧 PHC 是怎么做的？

### 整体架构

PHC 的核心是 **PMCP（Progressive Multiplicative Control Policy）**，由三个关键组件组成：

```
输入: 当前身体状态 + 目标姿态
         ↓
  ┌──────────────────────────────┐
  │  多个 Primitive（技能网络）   │
  │  P¹: 基础技能（走、跑、跳）   │
  │  P²: 进阶技能（难动作）       │
  │  P³: 更难的技能              │
  │  Pᶠ: 摔倒恢复技能            │
  └──────┬───────────────────────┘
         ↓
  ┌──────────────────────────────┐
  │  Composer C（调度网络）       │
  │  决定当前时刻各 Primitive 权重 │
  └──────┬───────────────────────┘
         ↓
  输出: PD 控制目标 → 关节扭矩 → 仿真
```

### 第一步：状态和动作设计

**状态空间 $s_t$：**

| 组成 | 内容 | 说明 |
|------|------|------|
| 本体感知 | 身体 3D 姿态 $q_t$，速度 $\dot{q}_t$ | 当前身体在干嘛 |
| 目标差异 | 参考与当前的旋转/位置/速度差 | 下一步应该去哪 |

两种目标表示：
- **Rotation-based** $s_{rot}$：关节旋转差、位置差、线速度差、角速度差
- **Keypoint-based** $s_{kp}$：3D 关键点位置差、速度差（更鲁棒，适合噪声输入）

所有量都相对于角色当前朝向和根节点归一化。

**动作空间 $a_t$：**

直接输出各关节的 PD 控制目标（**不加残差**，不用外力）：

$$\tau = k_p(a_t - q_{sim}) - k_d(\dot{q}_{sim})$$

> ⚠️ 关键区别：DeepMimic 用的是参考动作 + 残差，PHC 直接输出绝对目标。这更难学但更通用。

### 第二步：奖励设计

$$r_t = 0.5 \cdot r_{task} + 0.5 \cdot r_{amp} + r_{energy}$$

| 奖励项 | 公式/说明 | 作用 |
|--------|----------|------|
| $r_{task}$（模仿） | 关节位置、旋转、速度、角速度 L2 差的加权和 | 跟上参考动作 |
| $r_{amp}$（对抗） | 判别器打分，鼓励动作像真人 | 保持自然 |
| $r_{energy}$ | $-0.0005 \sum_j \|\tau_j \cdot \omega_j\|^2$ | 防止关节抖动 |

恢复模式下任务奖励变为：

$$r_{recover} = 0.5 \cdot r_{point} + 0.5 \cdot r_{amp} + 0.1 \cdot r_{energy}$$

其中 $r_{point}$ 只关注根节点是否靠近目标位置（不管全身姿态）。

### 第三步：渐进式训练（Progressive Training）

这是 PHC 最核心的创新。训练过程分多轮：

```
第 1 轮：训练 P¹ 在全部 AMASS 数据集 Q 上
         ↓ 收敛后冻结 P¹
         ↓ 找出 P¹ 失败的"难例" Q_hard²
第 2 轮：训练 P² 只在 Q_hard² 上
         ↓ 收敛后冻结 P²
         ↓ 找出 P² 仍然失败的 Q_hard³
第 3 轮：训练 P³ 只在 Q_hard³ 上
         ↓ 收敛后冻结 P³
第 F 轮：训练 Pᶠ 专门学摔倒恢复
         ↓ 冻结 Pᶠ
最终：训练 Composer C 学习如何组合所有 Primitive
```

**关键细节——权重共享：**
- $P^{(k+1)}$ 的参数从 $P^{(k)}$ 复制初始化，然后在难例上微调
- 这保证了新 Primitive 保留已学技能，同时专攻新难度

> 💡 **类比**：像"老师带学生"——第一个老师教基础，教不会的学生交给第二个更专业的老师，以此类推。最后一个"教练"专门教摔倒后怎么爬起来。

### 第四步：乘法组合（Multiplicative Composition）

所有 Primitive 冻结后，Composer $C$ 学习动态混合它们：

$$\Pi_{PHC}(a_t \mid s_t) = \frac{1}{\sum_i C_i(s_t)} \sum_i C_i(s_t) \cdot \Pi_{P^{(i)}}(a_t \mid s_t)$$

- $C_i(s_t) \geq 0$：Composer 对第 $i$ 个 Primitive 的权重
- 这不是简单的开关切换，而是**连续混合**，允许多个技能同时发挥作用

> 为什么叫"乘法"？因为最终动作分布是各 Primitive 分布的**加权乘积**（论文采用 MCP 框架），相比简单加法混合更能保留各 Primitive 的特长。

### 第五步：摔倒恢复（Fail-State Recovery）

$P^F$ 的训练有专门设计：

- **初始化**：角色被随机扔到地上（各种姿态）、距参考 2-5m 远
- **简化目标**：恢复模式下只关注根节点位置，不管全身姿态
- **切换机制**：当角色根节点距参考 < 0.5m 时，自动切回正常模仿模式
- **训练数据**：只用简单移动数据 $Q_{loco}$

---

## 🚶 具体实例：PHC 如何处理一段视频输入

### 场景

用户在摄像头前做动作，视频姿态估计器（HybrIK）输出带噪声的骨骼姿态，PHC 驱动虚拟角色实时模仿。

### 第 1 步：获取参考姿态

```
用户做"挥手"动作
  → HybrIK 提取每帧关节旋转 θ_t（有噪声）
  → 高斯滤波平滑
  → 得到参考动作序列 {q_ref_1, q_ref_2, ...}
```

### 第 2 步：计算状态

```
当前帧 t：
  本体感知: q_sim = 角色当前关节角度和速度
  目标差异: s_goal = (q_ref_{t+1} - q_sim, p_ref - p_sim, ...)
  → 拼接得到状态 s_t
```

### 第 3 步：Primitive 各自输出

```
P¹(s_t) → μ¹, σ¹   (基础技能建议: "左臂向上抬 30°")
P²(s_t) → μ², σ²   (进阶技能建议: "协调肩膀旋转")  
Pᶠ(s_t) → μᶠ, σᶠ  (恢复技能建议: "不需要恢复")
```

### 第 4 步：Composer 混合

```
C(s_t) → w = [0.7, 0.3, 0.0]  (主要用P¹，辅以P²，不需要恢复)
最终动作 = 0.7 * μ¹ + 0.3 * μ²
→ PD 控制 → 关节扭矩 → 角色挥手
```

### 第 5 步：突然摔倒！

```
用户突然蹲下，噪声导致参考姿态跳变
→ 角色失衡摔倒

下一帧:
  C(s_t) → w = [0.0, 0.0, 1.0]  (全部交给恢复 Primitive)
  Pᶠ: "先撑地，然后站起来，走向参考位置"
  
几秒后:
  角色站稳，距参考 < 0.5m
  → 切回正常模仿模式
  C(s_t) → w = [0.6, 0.4, 0.0]
```

---

## 🤖 PHC 在学习路线中的位置

```
DeepMimic (2018)     →    PHC (2023)         →    PULSE (2024)
单动作模仿              大规模+自恢复           通用运动潜空间
"学会翻跟斗"           "学会10000个动作        "把所有技能压缩成
                        +摔倒自己爬起来"        一个潜空间编码"
```

PHC 解决了 DeepMimic 的三个痛点：
1. **规模**：从几个动作 → 10000+ 动作（PMCP 解决遗忘）
2. **鲁棒性**：摔倒自恢复，无需 reset（Fail-state Recovery）
3. **噪声容忍**：支持视频/语言等噪声输入（Keypoint-based 输入）

---

## 🎤 面试高频问题 & 参考回答

### Q1: PHC 和 DeepMimic 的核心区别？

DeepMimic 一次只学一个动作片段，用参考动作 + 残差作为动作空间，角色偏离就 reset。PHC 能同时学上万条动作、直接输出绝对 PD 目标（不加残差不用外力），摔倒后自动恢复，支持永续运行。核心创新是 PMCP 架构解决大规模学习的灾难性遗忘问题。

### Q2: PMCP 怎么解决灾难性遗忘？

渐进式训练：先学全部数据，收敛后冻结参数，找出失败的难例交给新网络学习。新网络从旧网络权重初始化（权重共享），保留已有技能。最终用 Composer 网络动态混合所有 Primitive 的输出。这样新技能不会覆盖旧技能，因为旧网络参数是冻结的。

### Q3: 为什么用乘法组合（MCP）而不是简单切换？

简单切换（mixture of experts）在技能边界会出现不连续的动作跳变。MCP 允许多个 Primitive 同时贡献、连续混合，过渡更平滑。比如从走路过渡到跑步时，两个 Primitive 可以按比例混合而不是硬切换。

### Q4: PHC 的摔倒恢复是怎么实现的？

专门训练一个 Recovery Primitive $P^F$：(1) 初始化时将角色随机扔到各种摔倒姿态，(2) 简化目标为只追踪根节点位置，(3) 用简单移动数据训练。当角色根节点距参考 < 0.5m 时自动切回正常模仿。关键是不使用任何外部稳定力。

### Q5: PHC 为什么不用残差动作？

残差动作（$a = a_{ref} + \Delta a$）依赖参考动作作为基准，限制了策略的表达能力。PHC 直接输出绝对 PD 目标，虽然更难学习，但在处理噪声输入和恢复场景时更灵活——因为恢复时根本没有合理的参考动作可以加残差。

### Q6: PHC 的 Relaxed Early Termination 是什么？

当平均关节距参考超过 0.5m 就终止 episode，但**排除脚踝和脚趾关节**。这是因为脚部的精确匹配对维持平衡不那么重要，过早终止反而阻碍了策略学习平衡技巧。

### Q7: PHC 能处理什么样的输入？

两种：(1) Rotation-based：完整关节旋转，适合 MoCap 或 HybrIK 等旋转估计器；(2) Keypoint-based：只需 3D 关键点位置，适合 MeTRAbs 等位置估计器或 VR 控制器。后者更鲁棒，对噪声容忍度更高。

---

## 💬 讨论记录

（待补充）

---

## 📎 附录

### A. 网络架构

| 组件 | 架构 | 参数 |
|------|------|------|
| 每个 Primitive $P^{(k)}$ | MLP [1024, 512] | 高斯策略 $\mathcal{N}(\mu, \sigma)$ |
| Composer $C$ | MLP（输出非负权重） | 对每个 Primitive 一个权重 |
| 判别器 $D$ | MLP [1024, 512] | AMP 风格，含梯度惩罚 |
| 人体模型 | SMPL（24 刚体，23 驱动） | 支持不同体型 $\beta$ |

### B. 训练超参数

| 参数 | 值 | 说明 |
|------|-----|------|
| RL 算法 | PPO | 与 DeepMimic 一致 |
| 控制频率 | 30 Hz | 策略推理 |
| 仿真频率 | 60 Hz | 物理仿真 |
| 终止阈值 | 0.5m | 平均关节距离（排除脚踝/脚趾） |
| 能量惩罚系数 | 0.0005 | $r_{energy}$ |
| Primitive 数量 | 4（含恢复） | 3 个模仿 + 1 个恢复 |
| 训练数据 | AMASS（过滤后） | 去除坐姿、人物交互等 |
| 训练时间 | ~1 周 | 单张 A100 GPU |
| 模型大小 | 28.8 MB | 含所有 Primitive 和 Composer |

### C. 与 DeepMimic、AMP 的对比

| 特性 | DeepMimic | AMP | PHC |
|------|-----------|-----|-----|
| 动作规模 | 单个/少量 | 中等 | 10000+ |
| 动作空间 | 参考+残差 | 直接输出 | 直接输出（PD 目标） |
| 外部力 | 无 | 无 | 无 |
| 摔倒恢复 | ❌ reset | ❌ reset | ✅ 自恢复 |
| 永续运行 | ❌ | ❌ | ✅ |
| 噪声输入 | ❌ | ❌ | ✅ |
| 灾难性遗忘 | N/A | 有 | PMCP 解决 |

### D. PHC+ 改进（ICLR 2024）

PHC+ 是 PHC 的升级版，发表于 ICLR 2024（论文标题：Universal Humanoid Motion Representations for Physics-Based Control）：

| 改进 | 说明 |
|------|------|
| AMASS 成功率 100% | 从 PHC 的部分成功提升到全部动作 |
| PULSE 潜空间 | 将所有技能蒸馏到一个潜空间，可作为下游任务基础模型 |
| 下游泛化 | 支持导航、地形行走、VR 控制等，无需重新训练 |

### E. 关键实验指标

| 数据集 | 成功率 | MPJPE (mm) |
|--------|--------|------------|
| AMASS 测试集 | ~98%+ | ~40-60 |
| H36M-Motion*（MoCap） | 高 | 竞争力强 |
| H36M-Test-Video*（视频噪声） | 鲁棒 | 噪声下仍可用 |
