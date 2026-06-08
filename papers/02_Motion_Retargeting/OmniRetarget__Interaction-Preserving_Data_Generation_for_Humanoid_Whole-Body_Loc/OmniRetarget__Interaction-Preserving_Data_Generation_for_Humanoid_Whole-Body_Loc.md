---
layout: paper
title: "OmniRetarget: Interaction-Preserving Data Generation for Humanoid Whole-Body Loco-Manipulation and Scene Interaction"
zhname: "OmniRetarget：面向人形全身运动操作与场景交互的交互保持数据生成"
category: "Motion Retargeting"
paper_order: 4
---

# OmniRetarget: Interaction-Preserving Data Generation for Humanoid Whole-Body Loco-Manipulation and Scene Interaction
**用 interaction mesh + 硬约束优化，把「人-物-地形」的空间关系保真地搬到机器人上，再系统性扩增数据**

> 📅 阅读日期: 2026-06-08
>
> 🏷️ 板块: Motion Retargeting · 交互保持重定向 · 数据扩增
>
> 🧭 状态: 深度技术细节已填充（基于 arXiv:2509.26633 + 项目页 + Holosoma 仓库）

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **论文** | OmniRetarget: Interaction-Preserving Data Generation for Humanoid Whole-Body Loco-Manipulation and Scene Interaction |
| **会议** | **ICRA 2026** |
| **arXiv** | [2509.26633](https://arxiv.org/abs/2509.26633) |
| **项目页** | [omniretarget.github.io](https://omniretarget.github.io) |
| **论文 PDF** | [项目页 PDF](https://omniretarget.github.io/static/images/paper.pdf) |
| **代码 / 数据入口** | [amazon-far/holosoma](https://github.com/amazon-far/holosoma) |
| **数据集** | [Hugging Face · OmniRetarget_Dataset](https://huggingface.co/datasets/omniretarget/OmniRetarget_Dataset) |
| **发布时间** | 2025 年 9 月（arXiv） |
| **实验平台** | Unitree G1（主硬件验证）；亦支持 H1、Booster T1 跨本体 |

**作者**: Lujie Yang*, Xiaoyu Huang*, Zhen Wu*, Angjoo Kanazawa†, Pieter Abbeel†, Carmelo Sferrazza†, C. Karen Liu†, Rocky Duan†, Guanya Shi†

**机构**: 1 Amazon FAR (Frontier AI & Robotics), 2 MIT, 3 UC Berkeley, 4 Stanford University, 5 CMU

**一行定位**：首个**显式保持人-物-地形交互关系**的开源人形重定向引擎——用 interaction mesh 最小化 Laplacian 形变 + **硬运动学约束**（非穿透、脚粘地、关节/速度限位），从单条人体演示系统性扩增到不同物体位姿/形状、地形高度与机器人本体，生成 9+ 小时高质量参考轨迹，下游 RL 仅用 **5 项奖励 + 4 项域随机化**（与 BeyondMimic 同款超参、零调参）即可在 G1 上零样本 sim-to-real 完成 30 秒级跑酷与 loco-manipulation。

---

## 🎯 一句话总结

OmniRetarget 把重定向从「关键点匹配 + 软惩罚」升级为「**interaction mesh 保形 + 序贯 SOCP 硬约束**」：在保持人与物体/地形相对空间关系的同时，消除脚滑与穿透；并能把一条 OMOMO / LAFAN1 / 自采 MoCap 演示扩成覆盖多物体配置、地形与机器人本体的数据集，使 proprioceptive RL 跟踪器无需课程学习与繁重 reward 工程即可跟住长时程动态交互。

---

## 📌 英文缩写速查

| 缩写 | 全称 / 含义 | 简单解释 |
|------|-------------|----------|
| **IMMA** | Interaction Mesh based Motion Adaptation | 图形学中基于 interaction mesh 的动作适配（OmniRetarget 最近邻 prior） |
| **SOCP** | Second-Order Cone Program | 二阶锥规划；OmniRetarget 每帧用 SQP 式序贯求解 |
| **SQP** | Sequential Quadratic Programming | 序贯二次规划；非凸约束每步线性化 |
| **GMR** | General Motion Retargeting | 关键点 + 朝向匹配基线（本文对比方法之一） |
| **PHC** | Perpetual Humanoid Control | 无约束优化 retargeting 基线 |
| **OMOMO** | Object MOtion with human MOtion | 人-物交互 mocap 数据集 |
| **LAFAN1** | Lafayette Animation Dataset | 常用 BVH 动作库（本文 flat-terrain 来源之一） |
| **RL** | Reinforcement Learning | 下游用参考轨迹训练跟踪策略 |
| **Laplacian** | 图 Laplacian 坐标 | 衡量关键点相对邻域的局部几何关系 |

---

## ❓ OmniRetarget 要解决什么问题？

### 问题 1：现有 retargeting 忽视「交互」，只盯人体关键点

人形 loco-manipulation 需要的不只是「关节角像人」，还要保持：

- 手与箱子的相对位姿与接触关系；
- 脚与台阶/坡面的接触序列；
- 身体与墙壁、平台的空间关系。

PHC、GMR 等主流管线以**无约束或软惩罚优化**做关键点匹配，**不显式建模物体与地形**，导致参考轨迹在交互任务上 contact 失真，下游 RL 不得不靠大量 ad-hoc 正则（脚滞空、接触时长等）补救。

### 问题 2：软约束无法杜绝物理不可行动作

常见 artifact：

| 现象 | 后果 |
|------|------|
| 脚滑（foot skating） | 策略学到错误接触时序 |
| 自穿 / 地穿 | 仿真与真机跟踪发散 |
| 关节突变 | 参考不连续，跟踪难收敛 |

VideoMimic 用软接触/碰撞惩罚有所改善，但**无保证**且需仔细调参。OmniRetarget 把碰撞、关节限位、速度限位、stance 脚位置**写成硬约束**。

### 问题 3：交互数据稀缺，单演示难以覆盖场景变化

遥操作可在线适应，但难规模化；离线 retargeting 若不能从**一条演示**扩增到不同物体位姿、尺寸、地形高度与机器人本体，数据瓶颈依旧。OmniRetarget 把每次扩增都建模为**新的约束优化问题**（固定源 interaction mesh，变换目标侧采样点/物体/地形）。

> 💡 **范式**：高质量参考 → 极简 RL 配方。与 BeyondMimic 一致，当参考干净时，DeepMimic 式 5 项奖励已足够；脏参考才逼出十几项 reward 调参。

---

## 🔧 方法详解

### 系统总览

```
人体演示 (OMOMO / LAFAN1 / 自采 MoCap)
        │
        ▼
┌───────────────────────────────────────┐
│ Interaction Mesh 构建                  │
│ 人体关键点 + 物体/地形表面采样点        │
│ → Delaunay 四面体剖分                  │
└───────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────┐
│ 序贯 SOCP / SQP 优化（每帧）            │
│ min Laplacian 形变能 + 时间平滑        │
│ s.t. 非穿透、关节/速度限位、脚粘地      │
└───────────────────────────────────────┘
        │
        ▼
可选数据扩增（物体位姿/形状、地形高度、本体）
        │
        ▼
机器人关节参考轨迹 → RL 跟踪（5 rewards + 4 DR）
        │
        ▼
Unitree G1 真机零样本部署（最长 ~30 s 多阶段跑酷）
```

### 1. Interaction Mesh 与硬约束优化

#### 1.1 网格构建

- 顶点 = 用户指定的人体/机器人**语义关键点** + 物体与环境的**随机表面采样点**（接触区域更密采样）。
- 对顶点集做 **Delaunay 四面体剖分**，得到 volumetric interaction mesh。
- 人体与机器人只需**语义一致**的 keypoint 对应（如 hand↔hand），对精确解剖位置相对鲁棒。

#### 1.2 目标函数：Laplacian 形变能

对关键点 \(p_{t,i}\)，Laplacian 坐标：

\[
L(p_{t,i}) = p_{t,i} - \sum_{j \in \mathcal{N}(i)} w_{ij} \cdot p_{t,j}
\]

形变能（源 mesh \(\mathcal{P}^{\text{source}}\) vs 目标 mesh \(\mathcal{P}^{\text{target}}(q_t)\)）：

\[
E_L = \sum_i \| L(p_{t,i}^{\text{source}}) - L(p_{t,i}^{\text{target}}(q_t)) \|^2
\]

每帧求解：

\[
q_t^\star = \arg\min_{q_t} \sum_i \| L(p_{t,i}^{\text{source}}) - L(p_{t,i}^{\text{target}}(q_t)) \|^2 + \| q_t - q_{t-1} \|_Q^2
\]

\[
\text{s.t. } \phi_j(q_t) \geq 0 \;(\text{碰撞对 SDF}),\; q_{\min} \leq q_t \leq q_{\max},\; v_{\min} dt \leq q_t - q_{t-1} \leq v_{\max} dt,\; p_t^F = p_{t-1}^F \;(\text{stance 脚})
\]

- **Stance 判定**：源动作中脚在 xy 平面速度 < 1 cm/s → 该脚位置硬约束为上一帧。
- **求解器**：自定义 SQP——目标二次近似、约束线性化；用 Drake 自动微分处理四元数浮基在 \(\mathbb{S}^3\) 上的导数；**warm-start** 上一帧解。

#### 1.3 与 prior 方法对比（论文 Table I）

| 方法 | 硬运动学约束 | 物体交互 | 地形交互 | 数据扩增 | 优化 |
|------|:---:|:---:|:---:|:---:|------|
| IMMA | ✓ | ✗ | ✗ | ✗ | QP |
| PHC | ✗ | ✗ | ✗ | ✗ | 梯度下降 |
| GMR | ✗ | ✗ | ✗ | ✗ | Mink |
| VideoMimic | 软惩罚 | ✗ | ✓ | ✗ | JAX L-M |
| **OmniRetarget** | **✓** | **✓** | **✓** | **✓** | **序贯 SOCP** |

### 2. 系统性数据扩增

固定源 demonstration 的 \(\mathcal{P}_t^{\text{source}}\)，变换目标侧配置后**重新求解**同一优化问题。

| 扩增类型 | 做法 | 防平凡解技巧 |
|----------|------|----------------|
| **物体初始位姿** | 平移/旋转物体初始姿态，与原始物体轨迹指数插值混合 | 物体局部系建 mesh；下身锚定名义轨迹 \(\bar{q}_t^\star\) |
| **物体形状** | 三轴缩放物体几何 | 同上 |
| **地形高度** | 缩放平台高度/深度；地面网格点加入 mesh | 鼓励稳定接地接触 |
| **机器人本体** | 改 keypoint 对应与碰撞模型（G1 / H1 / T1） | 跨本体复用同一套管线 |

下身锚定示例：对 pick-up 任务加重惩罚下身偏离 \(\bar{q}_t^\star\)，并约束初始双脚位置与名义轨迹一致，避免「整机关节刚体平移」式无效扩增。

### 3. 下游 RL：极简配方（与 BeyondMimic 对齐）

#### 3.1 观测（纯本体感受，无显式场景/物体感知）

- 参考：关节 pos/vel、骨盆位姿误差；
- 本体：骨盆线/角速度、关节 pos/vel；
- 上一步动作。

高动态动作（如 wall-flip）可 mask 骨盆线速度/位置误差（状态估计不可靠）。

#### 3.2 奖励（仅 5 项，权重直接沿用 BeyondMimic，零调参）

1. **Body Tracking** — DeepMimic 式 body pos/ori/线角速度；
2. **Object Tracking**（适用时）— 物体 pos/ori；
3. **Action Rate**；
4. **Soft Joint Limit**；
5. **Self-Collision** — 自碰力 > 1 N 时二值惩罚。

#### 3.3 域随机化（仅 4 项）

- 躯干质心位置；
- 关节默认位置；
- 随机推力；
- 观测噪声。

物体侧另随机：质量 0.1–2 kg、质心 ±0.08 m、惯量 50–150%、形状 ±10%。

#### 3.4 训练分组

- 所有搬箱动作 → **单一多任务策略**；
- 爬平台 → **每条参考一个策略**。

---

## 📊 实验结果

### 运动学质量 vs 基线（OMOMO 人-物交互）

| 方法 | 穿透时长 ↓ | 最大深度 (cm) ↓ | 脚滑时长 ↓ | 接触保持 ↑ | 下游 RL 成功率 ↑ |
|------|:---:|:---:|:---:|:---:|:---:|
| PHC | 0.68±0.21 | 5.11±3.09 | 0.05±0.05 | 0.96±0.09 | 71.3%±22.6% |
| GMR | 0.83±0.14 | 8.50±3.94 | 0.02±0.01 | 0.99±0.04 | 50.8%±23.9% |
| VideoMimic | 0.60±0.27 | 7.48±4.95 | 0.12±0.07 | — | — |
| **OmniRetarget** | **最优档** | **最优档** | **最优档** | **最优档** | **显著高于基线** |

（具体数值见论文 Table II；OmniRetarget 在穿透、脚滑、接触保持与下游成功率上全面优于 PHC/GMR。）

### 真机亮点（Unitree G1）

| 任务 | 要点 |
|------|------|
| 搬箱（OMOMO） | 多样搬箱风格，自然全身协调 |
| 爬 0.9 m 平台 | 约为机器人身高 70% |
| 坡面爬行 | 干净接触序列 |
| **30 s 跑酷串联** | 搬 4.6 kg 椅子 → 踩椅上台 → 跳下翻滚缓冲（灵感来自 Atlas demo） |
| **Wall-flip** | ~0.5 s 完成翻转，峰值角速度 **15 rad/s**；真机 **5/5** 成功率 |

扩增数据评估：全扩增集训练、名义轨迹上评测成功率 **79.1%**，仅名义轨迹评测 **82.2%**——扩增显著扩大覆盖且性能几乎不降级。

### 数据规模

- 从 OMOMO、LAFAN1、自采 MoCap **retarget 生成 9+ 小时**轨迹（项目页；摘要写 8+ 小时）。
- 开源：[Hugging Face 数据集](https://huggingface.co/datasets/omniretarget/OmniRetarget_Dataset) + [Holosoma 代码](https://github.com/amazon-far/holosoma)。

---

## 🔗 与重定向主线关系

```
人体 mocap / 视频重建
        │
        ├─► GMR / PHC（关键点 IK，无交互建模）──► 平面动作 tracking
        │
        ├─► ReActor（RL 内嵌双层优化）──────────► 跨本体 + 物理可行参考
        │
        ├─► NMR（学习式时序映射 + CEPR）───────► 抑制 IK 跳变
        │
        └─► OmniRetarget（interaction mesh + 硬约束 + 扩增）► 人-物-地形交互 + loco-manipulation 数据工厂
```

**阅读顺序建议**：先读 [Retargeting Matters](Retargeting_Matters__General_Motion_Retargeting_for_Humanoid_Motion_Tracking/Retargeting_Matters__General_Motion_Retargeting_for_Humanoid_Motion_Tracking.md) 理解「重定向质量决定下游 RL」；再读本文看**交互保持 + 硬约束 + 数据扩增**如何把 loco-manipulation 参考做到 BeyondMimic 级简洁 RL 可跟踪。

---

## 💻 代码与数据入口

| 资源 | 说明 |
|------|------|
| [amazon-far/holosoma](https://github.com/amazon-far/holosoma) | Amazon FAR 统一仿真/训练栈；OmniRetarget 重定向与 RL 训练代码入口 |
| [OmniRetarget_Dataset](https://huggingface.co/datasets/omniretarget/OmniRetarget_Dataset) | 已 retarget 的大规模 loco-manipulation 轨迹 |
| [项目页交互 Demo](https://omniretarget.github.io) | 物体位姿/尺寸、地形高度、本体扩增的 3D 对比可视化 |

---

## 📝 个人笔记 / 待跟进

- [ ] 在 Holosoma 中跑通单条 OMOMO → G1 retarget → RL 跟踪闭环
- [ ] 对照 GMR 输出，统计同一段动作的穿透/脚滑指标
- [ ] 阅读 Drake SQP 实现细节与每帧耗时（是否满足离线批处理规模）
- [ ] 与 LessMimic / MeshMimic 等「场景感知模仿」对比数据侧差异

---

## 📚 参考文献（核心）

- Yang et al., **OmniRetarget**, arXiv:2509.26633, ICRA 2026.
- Kim et al., **Interaction Mesh** (SIGGRAPH 2013) — Laplacian 保形核心。
- Araújo et al., **GMR / Retargeting Matters** — 关键点 IK 强基线。
- Luo et al., **BeyondMimic** — 极简 reward 跟踪框架。
- Li et al., **OMOMO** — 人-物交互 mocap 来源。
