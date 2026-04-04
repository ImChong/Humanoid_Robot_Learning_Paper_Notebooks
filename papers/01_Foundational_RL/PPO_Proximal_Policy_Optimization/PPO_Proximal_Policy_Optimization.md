---
layout: paper
title: "Proximal Policy Optimization Algorithms (PPO)"
category: "基础路线图"
---

# Proximal Policy Optimization Algorithms (PPO)
**近端策略优化算法**

> 📅 阅读日期: 2026-03-11  
> 🏷️ 板块: Reinforcement Learning / Policy Optimization

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **arXiv** | [1707.06347](https://arxiv.org/abs/1707.06347) |
| **PDF** | [下载](https://arxiv.org/pdf/1707.06347) |
| **作者** | John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, Oleg Klimov |
| **机构** | OpenAI |
| **发布时间** | 2017年7月20日 |

---

## 🎯 一句话总结

PPO 通过一个简单的**裁剪机制**，让强化学习的策略更新既大胆又安全——每一步都在"可控范围"内改进，是目前人形机器人控制领域最常用的基础算法。

---

## 📌 英文缩写速查

| 缩写 | 全称 | 简单解释 |
|------|------|----------|
| **PPO** | Proximal Policy Optimization | 近端策略优化 |
| **RL** | Reinforcement Learning | 强化学习 |
| **GAE** | Generalized Advantage Estimation | 广义优势估计 |
| **KL** | Kullback-Leibler Divergence | KL散度，衡量两个分布的差异 |
| **MuJoCo** | Multi-Joint dynamics with Contact | 物理仿真引擎 |
| **Actor-Critic** | — | 策略网络(actor)+价值网络(critic)架构 |

---

## ❓ 这篇论文要解决什么问题？

假设你在训练一个人形机器人学走路。强化学习的基本思路是：让机器人**试错**，做得好就奖励，做得差就惩罚，逐步改进策略。

但问题在于——**每次改进多少？**

- **改太多**：机器人刚学会站稳，一次大更新把站立技能搞崩了，又开始乱摔
- **改太少**：学得太慢，训练几天都学不会走路
- **之前的方案 TRPO**：用复杂的二阶数学方法来控制更新幅度，有效但实现麻烦、计算量大

> 💡 **类比**：传统方法像"瞎子爬山"——步子迈太大容易摔下山；PPO 像是"走台阶"——每一步都有个护栏，保证在可控范围内。

PPO 的目标就是：**找到一个简单又有效的方法，让策略更新幅度恰到好处。**

---

## 🔧 PPO 是怎么做的？

### 第一个概念：概率比（新旧策略的对比）

每次更新策略后，我们想知道"新策略和旧策略有多大差别"。用一个简单的比值来衡量：

$$r_t(\theta) = \frac{\pi_\theta(a_t \mid s_t)}{\pi_{\theta_{old}}(a_t \mid s_t)}$$

- $r_t = 1$：新旧策略完全一样，没有变化
- $r_t = 1.5$：新策略选择这个动作的概率比旧策略高了 50%
- $r_t = 0.5$：新策略选择这个动作的概率减半了

### 第二个概念：优势函数（这个动作好不好）

优势 $\hat{A}_t$ 衡量的是"在状态 $s_t$ 下，选动作 $a_t$ 比平均水平好多少"：

- $\hat{A}_t > 0$：这是个好动作（比平均好）
- $\hat{A}_t < 0$：这是个差动作（比平均差）

### 核心机制：裁剪（Clip）

PPO 的精髓就一句话：**不管动作好坏，每次策略改变的幅度都要有上限。**

$$L^{CLIP}(\theta) = \mathbb{E}_t \left[ \min\left( r_t(\theta) \cdot \hat{A}_t,\ \text{clip}(r_t(\theta),\ 1-\epsilon,\ 1+\epsilon) \cdot \hat{A}_t \right) \right]$$

$\epsilon$ 通常取 0.2，意味着概率比被限制在 $[0.8, 1.2]$ 之间。

用表格看更直观：

| 情况 | 好动作 $\hat{A}_t > 0$ | 差动作 $\hat{A}_t < 0$ |
|------|----------------------|----------------------|
| **没有裁剪** | 无限增大该动作概率 | 无限减小该动作概率 |
| **PPO 裁剪** | 最多增大到 1.2 倍就停 | 最多减小到 0.8 倍就停 |

> 💡 **关键直觉**：裁剪的作用是"鼓励渐进改进"——发现一个好动作后，不要一次性把所有筹码压上去，而是慢慢加大。

### 训练流程（四步循环）

```
┌──→ ① 收集经验：N个并行环境各跑T步，共 N×T 个样本
│       │
│       ▼
│    ② 计算优势：用 GAE 算出每个动作的好坏程度
│       │
│       ▼
│    ③ 多轮更新：对同一批数据做 K 个 epoch 的梯度更新
│       │         （裁剪机制保证不会过度更新）
│       ▼
│    ④ 更新旧策略：πθ_old ← πθ，回到第①步
│       │
└───────┘
```

**为什么能对同一批数据更新多次？** 因为裁剪机制自动限制了更新幅度——随着更新次数增加，概率比越偏离 1，裁剪越频繁生效，相当于自带"刹车"。

---

## 🚶 具体实例：用 PPO 训练人形机器人走路

> 💡 **平台说明**：PPO 原论文（2017）在 **OpenAI Gym**（MuJoCo 物理引擎）的连续控制任务（HalfCheetah-v1、Hopper-v1、Humanoid-v1 等）和 **Atari** 游戏上做实验。下面示例使用现代等效版本 **Humanoid-v4**，与原论文 v1 版本在接口和环境细节上略有差异，但算法逻辑完全相同。

下面用 OpenAI Gym 的 **Humanoid-v4** 环境（对应原论文 Humanoid-v1），走一遍 PPO 从初始化到收敛的完整流程。Humanoid 是一个 17 关节、376 维观测、17 维动作的人形机器人，目标是学会稳定地向前走。

### 环境设定

| 项目 | 具体值 |
|------|--------|
| **状态空间** | 376 维（关节角度、角速度、质心位置/速度、接触力等） |
| **动作空间** | 17 维连续（各关节的扭矩，范围 [-0.4, 0.4]） |
| **奖励函数** | $r_t = v_x - 0.1 \lVert a_t \rVert^2 - 10 \cdot \mathbb{1}[\text{摔倒}]$ |
| **终止条件** | 质心高度 < 0.8m（摔倒）或达到 1000 步 |

> 💡 奖励设计的直觉：**走得快**（$v_x$）有奖励，**动作太猛**（$\lVert a_t \rVert^2$）有惩罚，**摔倒**重罚。

### 第 0 步：初始化

```
策略网络 πθ:  MLP [376] → 256 → 256 → [17] (输出高斯分布的均值)
价值网络 Vφ:  MLP [376] → 256 → 256 → [1]  (输出标量V值)

超参数:
  clip ε = 0.2
  γ = 0.99, λ = 0.95
  lr = 3e-4 (Adam)
  n_envs = 32, n_steps = 64  → 每轮收集 32×64 = 2048 个样本
  n_epochs = 10, mini_batch_size = 64
```

此时策略随机输出扭矩 → 人形机器人一站起来就乱抖，几步就摔倒。

### 第 1 步：收集经验（多环境并行）

```
环境 #1:  s₀¹ → a₀¹ → r₀¹ → s₁¹ → ... → s₆₃¹  (64步，中途摔倒会自动reset)
环境 #2:  s₀² → a₀² → r₀² → s₁² → ... → s₆₃²  (各环境独立)
  ...
环境 #32: s₀³² → a₀³² → r₀³² → ...  → s₆₃³²

→ 汇总得到 2048 个 (s, a, r, s', done) 样本
```

以环境 #1 为例（训练早期）：

```
t=0:   s₀ = [站立姿态...],  a₀ ~ πθ(·|s₀) = [-0.12, 0.35, ...],  r₀ = 0.3
t=1:   s₁ = [微倾斜...],    a₁ ~ πθ(·|s₁) = [0.28, -0.05, ...],  r₁ = 0.1
t=2:   s₂ = [大幅摇晃...],  a₂ ~ πθ(·|s₂) = [-0.40, 0.22, ...],  r₂ = -0.5
...
t=47:  摔倒！done=True → 环境自动 reset
t=48:  s₄₈ = [重新站立...],  继续收集到 t=63
```

> **为什么要并行？**
> - **降低样本相关性**：单环境中相邻状态几乎一样，32个环境的状态互不相关，梯度估计更准
> - **速度快**：GPU 向量化计算，32个环境几乎和1个一样快（如 Isaac Gym）
> - **覆盖更广**：同时有的环境在站立，有的在行走，有的刚摔倒重置

### 第 2 步：计算优势（GAE）

对每个环境的数据**独立**计算 GAE 优势（不跨环境、不跨摔倒重置点）：

```
① 用价值网络估计V值:
   V(s₀) = 5.2,  V(s₁) = 4.8,  V(s₂) = 3.1, ...

② 计算TD误差:
   δ₀ = r₀ + γ·V(s₁) - V(s₀) = 0.3 + 0.99×4.8 - 5.2 = -0.148
   δ₁ = r₁ + γ·V(s₂) - V(s₁) = 0.1 + 0.99×3.1 - 4.8 = -1.631
   ⚠️ 摔倒时 (done=True): δ₄₇ = r₄₇ + 0 - V(s₄₇)  ← 不加后续V值

③ GAE递推 (从后往前，遇到done截断):
   Â₆₃ = δ₆₃
   Â₆₂ = δ₆₂ + (γλ)·Â₆₃
   ...
   --- 摔倒断点，不跨越 ---
   Â₄₇ = δ₄₇   ← 旧轨迹最后一步，重新开始
   Â₄₆ = δ₄₆ + (γλ)·Â₄₇
   ...
```

结果：站稳时 $\hat{A}_t > 0$（好动作），摔倒前 $\hat{A}_t \ll 0$（差动作）。

### 第 3 步：PPO 裁剪更新（核心！）

保存旧策略 $\pi_{\theta_{old}} \leftarrow \pi_\theta$，然后对 2048 个样本做 **10 个 epoch** 的更新：

```
for epoch in range(10):
    for batch in shuffle_and_split(buffer, size=64):
        
        # 样本 t=15（一个好动作，Â₁₅ = +2.3）
        # 旧策略: πold(a₁₅|s₁₅) = 0.032
        # 新策略: πθ(a₁₅|s₁₅) = 0.048
        # 概率比: r₁₅ = 0.048 / 0.032 = 1.5（新策略更倾向这个动作）
        # 
        # 未裁剪: 1.5 × 2.3 = 3.45
        # 裁剪后: clip(1.5, 0.8, 1.2) × 2.3 = 1.2 × 2.3 = 2.76
        # L = min(3.45, 2.76) = 2.76  ← 用裁剪值，防止过度更新
        
        # 样本 t=42（一个坏动作，Â₄₂ = -3.1）
        # r₄₂ = 0.6（新策略已经不太选这个动作了）
        # 未裁剪: 0.6 × (-3.1) = -1.86
        # 裁剪后: clip(0.6, 0.8, 1.2)=0.8, 0.8 × (-3.1) = -2.48
        # L₄₂ = min(-1.86, -2.48) = -2.48
        # 
        # 但 clip(r)=0.8 是常数，对θ求导梯度为0
        # → 这个样本被"冻结"了，不参与更新
        # → 含义：新策略已经充分远离这个坏动作，不需要再继续远离
        
        # 汇总 loss，梯度更新
        loss = -mean(L_clip) + 0.5 * MSE(V(s), R_target)
        optimizer.step()
```

> 🔑 **关键理解**：epoch 1 时 $r_t \approx 1$（新旧策略一样），随着更新 $r_t$ 逐渐偏离 1，裁剪开始生效，**自动限制更新幅度**——这就是 PPO 的"自带刹车"。

### 第 4 步：训练进展

| 训练阶段 | 迭代次数 | 平均回报 | 行为表现 |
|---------|---------|---------|---------|
| **初期** | 0-100 | ~50 | 站立几步就倒，四肢乱甩 |
| **学会站立** | 100-300 | ~200 | 能稳定站立，开始尝试移动 |
| **学会走路** | 300-800 | ~1000 | 笨拙但稳定地向前走 |
| **步态优化** | 800-2000 | ~3000 | 步态流畅，速度提升 |
| **收敛** | 2000+ | ~5000+ | 高效稳定的行走步态 |

### 完整流程图

```
初始化 πθ, Vφ (随机), 创建 N=32 个并行环境
        │
        ▼
┌──→ 32 个环境并行收集，每个跑 64 步 → 2048 个样本
│       │
│       ▼
│   按环境/轨迹独立计算 GAE 优势 Ât
│       │
│       ▼
│   保存 πθ_old ← πθ
│       │
│       ▼
│   ┌─ for epoch in 10: ─────────────────────┐
│   │   打乱 2048 个样本（跨环境混合）        │
│   │   for mini_batch (64 samples):         │
│   │     r(θ) = πθ(a|s) / πθ_old(a|s)      │
│   │     L = min(r·Â, clip(r,0.8,1.2)·Â)   │
│   │     更新 θ (梯度上升 L)                 │
│   │     更新 φ (梯度下降 MSE)               │
│   └────────────────────────────────────────┘
│       │
│       ▼
│   回报 > 目标? ──Yes──→ 训练完成 🎉
│       │No
└───────┘
```

> 💡 注意：收集时按环境分开（保持轨迹独立），但更新时**打乱混合**所有环境的样本——这是 PPO 样本效率高的关键。

---

## 🤖 为什么 PPO 是人形机器人控制的首选？

1. **高维动作空间友好**：Humanoid 有 17 个关节需要同时控制，PPO 的裁剪机制避免了高维空间中策略的剧烈震荡
2. **容错性强**：人形机器人容易摔倒，PPO 不会因为几次摔倒就把已学会的平衡技能丢掉
3. **工程友好**：只需一阶优化器（Adam），代码简单，易于在 Isaac Gym/Lab 等 GPU 并行环境中部署
4. **生态成熟**：几乎所有人形机器人 RL 论文（AMP、PHC、ASE 等）都以 PPO 为基础算法

> **一句话**：如果只能学一个 RL 算法，PPO 是首选。它是 OpenAI Five (Dota 2)、RLHF (ChatGPT)、以及绝大多数机器人控制的核心算法。

---

## 📁 MimicKit 源码对照

以下代码块对应 [MimicKit](https://github.com/xbpeng/MimicKit) 中 PPO 的实现，与上述讲解的各模块一一对应。

### 1. Actor-Critic 网络结构（PPOModel）

```python
# mimickit/learning/ppo_model.py
class PPOModel(base_model.BaseModel):
    def eval_actor(self, obs):
        h = self._actor_layers(obs)
        a_dist = self._action_dist(h)
        return a_dist
    
    def eval_critic(self, obs):
        h = self._critic_layers(obs)
        val = self._critic_out(h)
        return val
```

Actor 和 Critic 各自独立（不共享 backbone），这是人形机器人领域的主流选择。

### 2. MLP 网络（fc_2layers_1024units）

```python
# mimickit/learning/nets/fc_2layers_1024units.py
def build_net(input_dict, activation):
    layer_sizes = [1024, 512]  # 两层 MLP
    
    input_dim = np.sum([np.prod(curr_input.shape) for curr_input in input_dict.values()])
    
    in_size = input_dim
    layers = []
    for out_size in layer_sizes:
        curr_layer = torch.nn.Linear(in_size, out_size)
        torch.nn.init.zeros_(curr_layer.bias)
        layers.append(curr_layer)
        layers.append(activation())
        in_size = out_size
    
    net = torch.nn.Sequential(*layers)
    return net, info
```

对应 `deepmimic_humanoid_ppo_agent.yaml` 中的配置：
```yaml
model:
  actor_net: "fc_2layers_1024units"  # [obs] → 1024 → 512 → [17] (动作均值)
  critic_net: "fc_2layers_1024units" # [obs] → 1024 → 512 → [1] (价值标量)
```

### 3. 概率比计算（r_t）

```python
# mimickit/learning/ppo_agent.py - _compute_actor_loss()
a_dist = self._model.eval_actor(norm_obs)
a_logp = a_dist.log_prob(norm_a)

# 概率比 r_t(θ) = π_θ(a|s) / π_θ_old(a|s)
a_ratio = torch.exp(a_logp - old_a_logp)
```

### 4. PPO 裁剪机制（核心！）

```python
# mimickit/learning/ppo_agent.py - _compute_actor_loss()
a_ratio = torch.exp(a_logp - old_a_logp)

# L^CLIP(θ) = min(r_t(θ)·Â_t, clip(r_t(θ), 1-ε, 1+ε)·Â_t)
actor_loss0 = adv * a_ratio
actor_loss1 = adv * torch.clamp(a_ratio, 
                                 1.0 - self._ppo_clip_ratio,  # ε=0.2 → 下界 0.8
                                 1.0 + self._ppo_clip_ratio)  # ε=0.2 → 上界 1.2
actor_loss = torch.minimum(actor_loss0, actor_loss1)
actor_loss = -torch.mean(actor_loss)  # 加负号因为 optimizer 做最小化
```

对应配置：
```yaml
ppo_clip_ratio: 0.2   # ε = 0.2，概率比限制在 [0.8, 1.2]
norm_adv_clip: 4.0    # 优势归一化后限制在 [-4, 4]
```

### 5. GAE / TD-λ 回报计算

```python
# mimickit/learning/rl_util.py
def compute_td_lambda_return(r, next_vals, done, discount, td_lambda):
    return_t = torch.zeros_like(r)
    reset_mask = done != base_env.DoneFlags.NULL.value
    reset_mask = reset_mask.type(torch.float)

    last_val = r[-1] + discount * next_vals[-1]
    return_t[-1] = last_val

    timesteps = r.shape[0]
    for i in reversed(range(0, timesteps - 1)):
        curr_r = r[i]
        curr_reset = reset_mask[i]
        next_v = next_vals[i]
        next_ret = return_t[i + 1]

        # λ=0.95 时，遇到 done 截断，不跨越轨迹
        curr_lambda = td_lambda * (1.0 - curr_reset)
        curr_val = curr_r + discount * ((1.0 - curr_lambda) * next_v + curr_lambda * next_ret)
        return_t[i] = curr_val
    
    return return_t
```

对应配置：
```yaml
td_lambda: 0.95        # GAE λ=0.95
discount: 0.99         # 折扣因子 γ=0.99
```

### 6. 价值网络损失（Critic Loss）

```python
# mimickit/learning/ppo_agent.py - _compute_critic_loss()
def _compute_critic_loss(self, batch):
    norm_obs = self._obs_norm.normalize(batch["obs"])
    tar_val = batch["tar_val"]  # TD-λ 回报 target
    pred = self._model.eval_critic(norm_obs)  # V(s) 预测
    pred = pred.squeeze(-1)

    diff = tar_val - pred
    loss = torch.mean(torch.square(diff))  # MSE 损失

    info = {"critic_loss": loss}
    return info
```

### 7. 训练循环（PPO Update）

```python
# mimickit/learning/ppo_agent.py - _update_model()
def _update_model(self):
    num_samples = self._exp_buffer.get_sample_count()
    
    # 先更新 Critic（多个 epoch）
    critic_batch_size = int(np.ceil(self._critic_batch_size * num_envs))
    num_critic_steps = num_critic_batches * self._critic_epochs
    self._update_critic(critic_batch_size, num_critic_steps)
    
    # 再更新 Actor（多个 epoch）
    actor_batch_size = int(np.ceil(self._actor_batch_size * num_envs))
    num_actor_steps = num_actor_batches * self._actor_epochs
    self._update_actor(actor_batch_size, num_actor_steps)
```

对应配置：
```yaml
actor_epochs: 5        # Actor 更新 5 个 epoch
actor_batch_size: 4    # 每个 batch 4 个环境
critic_epochs: 2       # Critic 更新 2 个 epoch
critic_batch_size: 2
```

### 8. Experience Buffer

```python
# mimickit/learning/experience_buffer.py
class ExperienceBuffer():
    def __init__(self, buffer_length, batch_size, device):
        self._buffer_length = buffer_length  # 每环境收集步数（如 32）
        self._batch_size = batch_size        # 并行环境数（如 4096）
    
    def record(self, name, data):
        # 记录 (s, a, r, done, logp) 等数据
        data_buf[self._buffer_head] = data
    
    def sample(self, n):
        # 随机采样 mini-batch 用于更新
        rand_idx = self._sample_rand_idx(n)
        ...
```

对应配置：
```yaml
steps_per_iter: 32     # 每轮收集 32 步 × N 个环境
```

### 9. PPO 超参数一览

```yaml
# deepmimic_humanoid_ppo_agent.yaml
agent_name: "PPO"
discount: 0.99              # 折扣因子 γ
td_lambda: 0.95             # GAE λ
ppo_clip_ratio: 0.2         # 裁剪范围 ε
norm_adv_clip: 4.0          # 优势归一化后截断

actor_epochs: 5             # Actor 更新轮数
actor_batch_size: 4         # Actor batch size
critic_epochs: 2            # Critic 更新轮数
critic_batch_size: 2

action_bound_weight: 10.0   # 动作范围惩罚（防止动作超出边界）
action_entropy_weight: 0.0  # 熵正则（0 表示不用）
```

---

## 🎤 面试高频问题 & 参考回答

### Q1: PPO 和 TRPO 的区别？
**A**: TRPO 用二阶优化（KL 散度硬约束），计算复杂，需要 Hessian 矩阵；PPO 用一阶优化 + 裁剪，更简单且效果相当。PPO 可以看作 TRPO 的"工程友好版"。

### Q2: 裁剪具体怎么起作用？
**A**: 把新旧策略的概率比限制在 $[1-\epsilon, 1+\epsilon]$ 范围内。好动作最多增大到 $1+\epsilon$ 倍就停，差动作最多减小到 $1-\epsilon$ 倍就停。确保每次更新都是"渐进改进"而不是"大跃进"。

### Q3: 为什么 PPO 能对同一批数据更新多次？
**A**: 因为裁剪机制是自适应的——随着更新轮次增加，概率比逐渐偏离 1，裁剪越来越频繁生效，自动限制了累积更新幅度。相当于自带刹车。

### Q4: PPO 的优缺点？
**A**: 
- **优点**：训练稳定、样本效率高（多 epoch 复用数据）、实现简单（一阶优化器）、广泛验证
- **缺点**：对超参数（$\epsilon$, 学习率）敏感、在稀疏奖励任务上可能探索不足

### Q5: PPO 中的 loss 由哪些部分组成？
**A**: 两部分（有时三部分）：
- **策略损失**：$-L^{CLIP}$（加负号因为 optimizer 做的是 minimize）
- **价值损失**：$\frac{1}{2}\|V(s) - R_{target}\|^2$（让价值网络预测更准）
- **（可选）熵正则**：$-c \cdot H(\pi)$（鼓励探索，防止策略过早收敛）

---

## 💬 讨论记录

### 2026-03-15 Surrogate 的理解

**Q: PPO中的surrogate是什么？如何理解？**

**Surrogate = 替代目标函数**，用一个"近似的、好优化的函数"来代替真正的策略梯度目标。

**🍕 生活类比：试吃调味**

想象你是个厨师，在调一锅汤的咸淡：
- **真正的目标**：让客人吃完整碗汤后说"完美"（但你不可能每调一次盐就让客人喝完一整碗再反馈）
- **Surrogate（替代）**：你舀一小勺尝一下，用这一勺的味道来**代替**整碗汤的评价，指导你下一步加多少盐

具体到 PPO：

$$L^{CPI}(\theta) = \hat{\mathbb{E}}_t \left[ \frac{\pi_\theta(a_t \mid s_t)}{\pi_{\theta_{old}}(a_t \mid s_t)} \hat{A}_t \right] = \hat{\mathbb{E}}_t \left[ r_t(\theta) \hat{A}_t \right]$$

- 用旧策略采的数据，通过概率比来估算"如果换成新策略，回报会变好还是变差"，不用真的重新采样
- PPO 的 clip 就是限制你每次最多加/减多少盐——防止估算偏差太大

---

**Q: "用旧策略采的数据，通过概率比来估算新策略的好坏"怎么理解？**

**🎰 类比：换骰子估胜率**

假设你用 **骰子A**（旧策略）投了 1000 次，记录了每次的点数和输赢。现在换了 **骰子B**（新策略），想知道"用 B 玩 1000 次大概能赢多少"——但不想真的再投 1000 次。

> 骰子A投出6点的概率是 1/6，骰子B投出6点的概率是 2/6。
> 那骰子A投出的每个6点，在骰子B的世界里应该"算两倍权重"。

这就是**重要性采样**（Importance Sampling）：

$$r_t(\theta) = \frac{\pi_\theta(a_t \mid s_t)}{\pi_{\theta_{old}}(a_t \mid s_t)}$$

- **$r_t = 1.5$**：新策略选这个动作的概率比旧策略高了 50%
- **$r_t = 0.5$**：新策略选这个动作的概率减半了

$r_t(\theta) \times \hat{A}_t$ 就在告诉你：**新策略整体回报是变好了还是变差了**。PPO 的 clip 再加一层保险：概率比偏太远时估算不准，所以截断掉。

---

## 📎 附录

### A. PPO 两种变体

| 变体 | 方法 | 特点 |
|------|------|------|
| **PPO-Penalty** | 在目标函数中加入 KL 惩罚项 | 类似 TRPO，用拉格朗日乘子自适应调整 |
| **PPO-Clip** (主流) | 使用裁剪操作 | 更简单、更稳定，几乎所有实际应用的默认选择 |

### B. Loss 函数完整拆解

$$\mathcal{L}_{total}(\theta, \phi) = \underbrace{-\mathbb{E}\left[ L^{CLIP}(\theta) \right]}_{\text{策略损失}} + \underbrace{\frac{1}{2} \mathbb{E}\left[ \left( V_\phi(s) - R_t \right)^2 \right]}_{\text{价值损失}}$$

**为什么策略损失要加负号？**
- PPO 的目标是**最大化** $L^{CLIP}$（让好动作概率更大）
- PyTorch/TensorFlow 的 optimizer 默认做**最小化**（梯度下降）
- 所以 minimize $(-L^{CLIP})$ ⟺ maximize $L^{CLIP}$

**价值损失的作用：**
- 让价值网络 $V_\phi(s)$ 拟合目标回报 $R_t$
- V 准 → 优势估计准 → 策略学得更好 → 新数据更好 → V 更准（良性循环）

### C. Actor-Critic 网络架构

| 架构 | 结构 | 特点 |
|------|------|------|
| **共享 backbone** | 输入 → 共享 MLP → 分叉 → Actor/Critic head | 省显存，但两个 loss 可能互相干扰 |
| **完全独立** | Actor MLP + Critic MLP 各自独立 | 更稳定，**人形机器人领域的主流选择**（Isaac Lab、legged_gym 等默认配置） |

### D. 超参数速查表

| 参数 | 含义 | 推荐值 |
|------|------|--------|
| $\epsilon$ (clip range) | 裁剪范围 | 0.1 ~ 0.2 |
| $\gamma$ (discount) | 折扣因子 | 0.99 |
| $\lambda$ (GAE) | 偏差-方差平衡 | 0.95 |
| learning rate | 学习率 | 3e-4 |
| n_envs | 并行环境数 | 1 ~ 256 |
| n_steps (T) | 每环境收集步数 | 64 ~ 2048 |
| n_epochs | 同批数据更新轮数 | 3 ~ 10 |
| mini_batch_size | 小批量大小 | 64 ~ 4096 |

### E. 训练过程中各组件的变化

```
迭代 100 (刚学会站立):
  ┌─ 策略输出: 小幅度扭矩，保持平衡为主
  ├─ V(站立) ≈ 200,  V(倾斜) ≈ 50,  V(摔倒) ≈ 0
  ├─ 优势: 保持直立的动作 Â > 0，导致摔倒的 Â ≪ 0
  └─ clip 生效次数: ~30% (策略还在快速变化)

迭代 1000 (稳定行走):
  ┌─ 策略输出: 周期性的腿部交替扭矩，类似步态
  ├─ V(行走中) ≈ 3000,  V(站立不动) ≈ 500
  ├─ 优势: 加速走的动作 Â > 0，减速/偏移的 Â < 0
  └─ clip 生效次数: ~10% (策略趋于稳定，更新幅度自然变小)
```

### F. 实验结果

论文在多个基准任务上验证了 PPO 的效果：
- **连续控制 (MuJoCo)**：HalfCheetah, Hopper, Walker, Swimmer, Ant, Humanoid，超越 TRPO、A2C
- **Atari 游戏**：在大多数游戏上取得优异表现
- **机械臂控制**：成功完成复杂的连续操作任务

### G. 相关工作

| 算法 | 年份 | 关系 |
|------|------|------|
| **TRPO** | 2015 | PPO 的前身，用信任区域的策略优化 |
| **A2C/A3C** | 2016 | 异步优势 Actor-Critic |
| **SAC** | 2018 | 软 Actor-Critic，off-policy 方法 |
| **TD3** | 2018 | 双延迟 DDPG，off-policy 方法 |

*(已移至上方「📌 英文缩写速查」)*
