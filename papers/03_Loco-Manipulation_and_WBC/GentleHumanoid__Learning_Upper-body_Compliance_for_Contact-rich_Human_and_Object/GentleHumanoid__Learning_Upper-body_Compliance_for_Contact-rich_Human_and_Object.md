---
layout: paper
paper_order: 14
title: "GentleHumanoid: Learning Upper-body Compliance for Contact-rich Human and Object Interaction"
zhname: "GentleHumanoid：面向密集接触人机与物体交互的上半身柔顺学习"
category: "Loco-Manipulation and WBC"
---

# GentleHumanoid: Learning Upper-body Compliance for Contact-rich Human and Object Interaction
**让人形机器人在拥抱、搀扶和脆弱物体操作中学会“上半身柔顺”**

> 📅 阅读日期: 2026-04-19
> 🏷️ 板块: Loco-Manipulation and Whole-Body-Control

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **arXiv** | [2511.04679](https://arxiv.org/abs/2511.04679) |
| **HTML** | [在线阅读](https://arxiv.org/html/2511.04679) |
| **PDF** | [下载](https://arxiv.org/pdf/2511.04679) |
| **项目主页** | [gentle-humanoid.axell.top](https://gentle-humanoid.axell.top) |
| **GitHub** | 论文首页未见公开仓库（以论文发布时信息为准） |
| **发布时间** | 2025年11月6日 |
| **机构** | Stanford University |
| **实验平台** | Unitree G1 humanoid |
| **控制频率** | 高层策略 50 Hz，低层 PD 跟踪 |

**作者**: Qingzhou Lu*, Yao Feng*, Baiyu Shi, Michael Piseno, Zhenan Bao, C. Karen Liu

---

## 🎯 一句话总结

GentleHumanoid 把**阻抗控制 + 全身 motion tracking RL**结合起来，让人形机器人在维持任务成功的同时，能用肩、肘、手形成**整条上肢运动链上的柔顺响应**，并且通过**可调力阈值**把交互力控制在更安全、更舒适的范围内。

---

## 📖 英文缩写速查

| 缩写 | 全称 | 简单解释 | 生活类比 |
|------|------|----------|----------|
| **RL** | Reinforcement Learning | 强化学习：通过奖惩训练控制策略 | 像带小孩学骑车，做对了鼓励、做错了纠正 |
| **PPO** | Proximal Policy Optimization | 常用稳定 RL 算法 | 每次只小步改策略，避免一把改坏 |
| **PD** | Proportional-Derivative | 比例-微分控制 | 像弹簧 + 阻尼器，一边拉回目标一边防抖 |
| **HRI** | Human-Robot Interaction | 人机交互 | 人和机器人发生直接协作或身体接触 |
| **SMPL / SMPL-X** | Skinned Multi-Person Linear Model | 参数化人体模型 | 用一串数字描述人体姿态和形状 |
| **GMR** | General Motion Retargeting | 人类动作到机器人动作的重定向方法 | 把“人做的动作”翻译成“机器人能做的动作” |
| **AMASS** | Archive of Motion Capture as Surface Shapes | 大规模人体动捕数据集 | 人类运动的大图书馆 |
| **InterX** | Human-Human Interaction Dataset | 人-人交互数据集 | 专门收录接触互动动作的录像库 |
| **LAFAN** | Lafayette Animation Dataset | 动作捕捉数据集 | 常见的全身动作素材库 |
| **BEDLAM** | Benchmark / dataset for detailed human body shape & motion | 论文在自动拥抱管线里引用的人体形状数据/基准，用于支撑 body mesh 估计 | 像一个“真人体型与动作素材库”，帮助视觉模型学会从图像还原人体外形 |
| **PromptHMR** | Promptable Human Mesh Recovery | 从单目 RGB 视频估计人体 SMPL-X 运动序列的方法 | 用手机视频恢复人的 3D 动作和身体网格的“视觉重建器” |
| **RGB** | Red-Green-Blue | 普通彩色相机图像 | 手机拍照那种彩色画面 |
| **Sim-to-Real** | Simulation to Reality | 仿真训练迁移到真机 | 游戏里练熟，再上真实赛场 |

---

## ❓ 要解决什么问题

这篇论文解决的是一个很“反直觉”但很关键的问题：

**为什么现在很多人形机器人看起来动作很强，但一跟人或脆弱物体接触就显得太“硬”？**

### 1. 现有 tracking policy 默认追求“别偏离参考动作”
很多最近的人形 RL 控制器本质上都在做一件事：
- 尽量跟踪参考 motion
- 把外力当成扰动
- 一旦被推、被拉、接触物体，就拼命“拉回去”

这会导致机器人在拥抱、搀扶、握手、拿气球这类任务里显得很僵硬。

### 2. 以前的柔顺控制大多只管末端，不管整条上肢链路
有些方法把 impedance / admittance 控制接到 base 或 end-effector 上，但真正的人机接触通常不是只碰“手掌一个点”：
- 拥抱时，手、前臂、肘、肩都可能同时接触
- 搀扶站起时，力量会沿手—肘—肩—躯干传递
- 处理软物体时，局部挤压和整体姿态也会联动

只控制末端执行器，往往做不到整条运动链的自然协调。

### 3. “安全”和“任务成功”常常互相打架
如果你把策略训得很软，它可能抱不住人、扶不起人、拿不稳东西；
如果你把策略训得很硬，它虽然能完成任务，但会让接触很生硬，甚至超过安全或舒适阈值。

> 💡 **类比**：以前很多策略像“只会按既定动作出拳的拳击陪练”。GentleHumanoid 更像一个有分寸的康复师——既能给力，也知道什么时候该顺着你、托着你，而不是硬顶着你。

---

## 🔧 方法详解

GentleHumanoid 的核心思想可以概括成一句话：

**先用阻抗模型定义“应该怎样柔顺”，再让 RL 策略去学习复现这种柔顺的参考动力学。**

### 1）问题建模：上半身多链接柔顺系统
论文把上半身关键点建成一个多链接的阻抗系统，重点跟踪这些 link：
- shoulder
- elbow
- hand

每个 link 的运动都受两类力共同影响：

$$M \ddot{x}_i = f_{drive,i} + f_{interact,i}$$

其中：
- $M$ 是虚拟质量，论文里每个 link 取 **0.1 kg**
- $f_{drive}$ 是“把机器人拉向目标 motion”的驱动力
- $f_{interact}$ 是“来自人或物体接触”的交互力

这一步很关键，因为它把“柔顺”从一个模糊概念，变成了一个明确可积分的参考动力学系统。

### 2）驱动力：来自目标 motion 的阻抗弹簧-阻尼
驱动力采用经典 spring-damper 形式：

$$f_{drive} = K_p(x_{tar} - x_{cur}) + K_d(v_{tar} - v_{cur})$$

其中：
- $x_{tar}, v_{tar}$ 来自参考动作
- $x_{cur}, v_{cur}$ 是当前 link 状态
- $K_d = 2\sqrt{MK_p}$，即取临界阻尼

直观理解：
- 参考 motion 不是“死命令”
- 而是像一根弹簧，把机器人温和地拉回目标
- 外界施力时，系统允许偏移，但不会完全散掉

### 3）交互力：统一的 spring-based 建模
论文最核心的创新，是把 interaction force 统一成：

$$f_{interact} = K_{spring}(x_{anchor} - x_{cur})$$

但 anchor 的定义分两种：

#### A. Resistive contact（阻抗式抵抗接触）
当机器人自己压到表面上时：
- 把**刚开始接触那一刻的 link 位置**固定为弹簧锚点
- 之后如果继续偏离，就产生 restoring force

即：
- 像一根“接触后锁住起点”的虚拟弹簧
- 适合描述“压住某个物体/人体后，对方把你往外推时”的回复

#### B. Guiding contact（引导式接触）
当外部主体在推/拉机器人手臂时：
- 不从当前接触面随机造力
- 而是从**人类 motion dataset 的完整上半身姿态**中采样一个 posture
- 把采样姿态里的 link 位置作为 spring anchor

这样做的意义很大：
- 不是给肩/肘/手各自独立乱施力
- 而是从整个人体姿态里采样，保证肩-肘-腕之间的**运动学一致性**
- 学到的是“整条上肢一起顺从/一起引导”的协调力响应

### 4）如何做多样化 force exposure
训练时，作者会随机化：
- **弹簧刚度**：$K_{spring} \sim U(5, 250)$
- **受力 link 集合**：
  - 40% 无外力
  - 15% 双臂 6 个 link 同时受力
  - 30% 单臂 3 个 link 受力
  - 15% 单个 link 受力
- **重采样频率**：每 5 秒重采样一次，并加过渡窗口保证连续

这样策略在训练中见过非常多的人/物体接触情况，不会只会一种“标准拥抱姿势”。

### 5）安全力阈值：让柔顺程度可调
论文引入了一个很实用的设计：**force-thresholding**。

当驱动力太大时，不允许无限增大，而是按阈值缩放：

$$f_{drive}^{limited} = \min\left(1, \frac{\tau_{safe}}{\|f_{drive}\|} \right) f_{drive}$$

其中：
- 训练时 $\tau_{safe}$ 在 **5 N 到 15 N** 之间分段采样
- 部署时用户可以按任务调节这个阈值

它带来的直接效果是：
- **5 N**：适合握手、气球、柔和接触
- **10 N**：适合普通拥抱
- **15 N**：适合 sit-to-stand 这类需要更强支撑的场景

论文还给了安全依据：
- 即使按最极端小接触面积算，15 N 也低于 ISO/TS 15066 对 torso / arm 的痛感阈值
- 对更真实的拥抱接触面积，换算压力约落在 **3–9 kPa**，属于舒适导向区间

### 6）RL 控制策略：学会追随“参考柔顺动力学”
策略目标不是直接拟合 reference motion，而是拟合积分后的 reference dynamics：

$$\dot{x}^{ref}_{t+1} = \dot{x}^{ref}_t + \Delta t \cdot \frac{f_{drive} + f_{interact}}{M}$$

$$x^{ref}_{t+1} = x^{ref}_t + \Delta t \cdot \dot{x}^{ref}_{t+1}$$

也就是说：
- reference motion 先经过“驱动力 + 交互力”的动力学融合
- 得到一个更柔顺、更接触感知的参考轨迹
- RL 策略再学习在仿真里复现这个 reference dynamics

### 7）Teacher-Student sim-to-real 架构
论文采用 teacher-student 两阶段训练，并且两者都用 **PPO**。

#### Student 可见观测（真机可部署）
学生策略只看真实可获得信息：
- 当前安全阈值 $\tau_{safe}$
- target motion 信息（未来 root pose、target joint position）
- root angular velocity
- projected gravity
- joint 历史
- 近几步 action 历史

#### Teacher 额外看 privileged observation
教师策略还看：
- reference dynamics 的 $x^{ref}, \dot{x}^{ref}$
- reference 预测交互力与仿真实际交互力
- link heights
- 上一步关节力矩
- 累积 tracking error

策略输出为 **29 维 joint position targets**，由底层 PD controller 跟踪。

### 8）训练数据与奖励
#### Motion data
论文使用了三类数据，经 GMR 重定向后训练：
- **AMASS**
- **InterX**
- **LAFAN**

并过滤掉与交互场景不符的高动态动作，最终得到：
- **约 25 小时数据**
- **50 Hz 采样频率**

#### Compliance reward
柔顺奖励由三部分组成：
1. **Reference dynamics tracking**：让仿真状态跟随参考柔顺动力学
2. **Reference force tracking**：让预测交互力和仿真交互力一致
3. **Unsafe force penalty**：对超阈值力进行惩罚

论文表中的关键权重：
- reference dynamics tracking：**2.0**
- reference force tracking：**2.0**
- unsafe force penalty：**6.0**

可以看出作者明显把“不要越界施力”看得比“单纯动作像不像”更重要。

---

## 🚶 具体实例：这篇论文到底怎么让机器人“抱得更柔和”？

### 例子 1：拥抱中被人往外拉
假设 G1 正在执行 hugging motion：
- 参考动作希望手臂继续闭合
- 但人往外轻拉机器人手腕

如果是传统 tracking RL：
- 会把这股外力当成扰动
- 力图迅速把手拉回参考位置
- 导致手、肘、肩上的接触力上冲，动作很僵硬

在 GentleHumanoid 里：
1. wrist、elbow、shoulder 同时有 interaction force
2. guiding / resistive spring 让整条手臂都“跟着让一点”
3. 如果当前 $\tau_{safe}=10N$，驱动力也会被限制在大约这个量级
4. 结果不是“硬顶住”，而是边保持 hug、边顺着外力调整姿态

论文的仿真结果是：
- **GentleHumanoid** 在手部大致稳定在 **10 N** 左右
- **Vanilla-RL** 往往超过 **20 N**
- **Extreme-RL** 也会超过 **13 N**
- 肘部和肩部同样呈现类似趋势：GentleHumanoid 大多保持在 **7–10 N** 范围，baseline 则容易到 **15–20 N**

### 例子 2：真人/人体模型轻微错位的拥抱
真实拥抱最怕的不是“正好对齐”，而是人站歪了一点、身体前后位置有一点偏差。

论文做了 mannequin hugging，并专门测试：
- **对齐 hugging**
- **错位 hugging**

他们给人体模型贴了自定义 pressure-sensing pad：
- **40 个校准过的 capacitive taxels**
- 每个 texel 近似接触面积 **6 mm × 6 mm**

结果是：
- GentleHumanoid 在错位时仍能把峰值力维持在更可控范围
- baseline 更容易出现局部高压峰值
- 尤其 Vanilla-RL 会在局部形成非常集中的压力热点

这说明它不只是“总力变小”，而是**接触分布也更均匀、更像自然拥抱**。

### 例子 3：拿气球
这是很能说明问题的场景：
- 力太小：抓不住
- 力太大：气球被挤爆或变形，机器人还可能失衡

论文把 GentleHumanoid 的阈值设成 **5 N**：
- 成功抓住并保持气球
- baseline 因为太硬，会越挤越狠，最后把气球挤坏甚至导致 G1 失衡掉落

这个例子非常直观地说明：
**柔顺不是“更弱”，而是“更有分寸”。**

---

## 🏗️ 工程复现要点

### 平台与控制栈
- **机器人**：Unitree G1
- **策略输出**：29 维 joint position target
- **控制频率**：50 Hz
- **低层控制**：joint PD
- **积分方法**：semi-implicit Euler
- **积分步长**：0.005 s

### 数据与预处理
- 人类 motion 来源：AMASS / InterX / LAFAN
- 通过 **GMR** 做 retargeting
- 保留与 interaction 场景相符的动作
- 重点覆盖 upper-body contact 相关姿态

### 训练关键点
1. 建 reference dynamics，而不是直接追 motion
2. 给 teacher 提供 privileged info，student 只看可部署观测
3. 对 interaction force 做多 link、成组、连续采样
4. 训练阶段随机化安全阈值，部署阶段按任务切换阈值
5. 奖励里要显式加入 force tracking 和 unsafe force penalty

### Hugging 评估硬件
- 手持测力计：**Mark-10 M5-10**
- 自定义腰部压力传感垫：**40 taxels**
- 用 motorized stage + PDMS applicator 做标定

### Autonomous hugging pipeline
论文里把“自动拥抱”和“视频到机器人”分成两条链路：
1. **Autonomous, shape-aware hugging**：先用 motion capture 标记点获得人的位置和绝对身高，再用 G1 头部的 RGB 相机获取单张图；随后结合 **BEDLAM** 支撑的人体形状估计流程恢复 body mesh，提取腰部 target points，优化 G1 的 upper-body joint angles 与平面 base pose，使双手/手肘对准目标区域。
2. **站位控制**：再训练 locomotion policy，让机器人先走到人前方 **10 cm standoff** 的合适位置，并保持 frontal alignment。
3. **执行切换**：站位满足后，再切换到 GentleHumanoid 执行 hug。
4. **Video to Humanoid**：论文还额外展示了另一条从手机 **monocular RGB video** 出发的链路，使用 **PromptHMR** 把视频估计为 SMPL-X motion sequence，再通过 **GMR** 重定向到 G1，最后交给训练好的 GentleHumanoid policy 执行。

这一步很有工程价值，因为它把“柔顺控制”接上了“自动感知 + 自动站位 + 自动接触”，并进一步延伸到“视频动作 → humanoid 执行”的完整闭环。

---

## 🤖 工程价值

我觉得这篇论文最值得你关注的，不只是“又一个人形控制策略”，而是它把一个经常被忽视的能力做成了明确框架：

### 1. 从“能碰”升级到“会碰”
很多 humanoid 工作关心的是运动完成度、鲁棒性、泛化性；
这篇则直接把**接触品质**变成核心优化目标。

### 2. 给上肢柔顺控制一个可训练、可部署、可调阈值的统一方案
它不是单纯塞一个力控器，而是把：
- 目标动作
- 接触建模
- 安全阈值
- RL policy
- sim-to-real teacher-student

整成了一套统一方案。

### 3. 很适合延伸到康复辅助 / 陪伴 / 人机协作
例如：
- sit-to-stand assist
- handshaking
- hugging
- fragile object manipulation
- teleop 下的安全接触

这些任务对“舒服、自然、不吓人”比对“速度极快、轨迹极准”更敏感。

### 4. 对你做 humanoid RL 的启发
如果你后面做 imitation / RL 控制，尤其涉及上肢与外界接触，这篇论文给了一个很值得借鉴的方向：
- 不要只学 rigid tracking
- 可以把 contact response 先写成参考动力学
- 再让 policy 去模仿这个“期望柔顺行为”

---

## 🎤 面试高频 Q&A

### Q1：GentleHumanoid 和普通 whole-body tracking policy 的本质区别是什么？
**A：** 普通 tracking policy 的目标是“动作别偏离参考轨迹”，所以外力通常被当成扰动来压制；GentleHumanoid 则先用阻抗参考动力学定义“遇到接触后应该怎样偏移”，再让 RL 策略学习复现这种柔顺响应。因此它优化的不是 rigid tracking，而是 compliant tracking。

### Q2：为什么作者强调 shoulder、elbow、wrist 的整条上肢链，而不是只做 end-effector compliance？
**A：** 因为真实的人机接触通常会在多个 link 同时发生，比如拥抱和搀扶站起。只让 hand 柔顺，肘和肩仍然僵硬，会造成整体姿态不自然、局部压强过大，甚至影响平衡。GentleHumanoid 的价值就在于把多 link 协调力响应当成核心问题处理。

### Q3：guiding contact 为什么要从 human motion dataset 的完整 posture 里采样 anchor？
**A：** 这样能保证肩、肘、腕之间的运动学一致性。如果每个 link 独立随机给一个力，学到的是互相打架的局部扰动；从完整姿态采样，则相当于给整条手臂一个“像真人推/拉时那样协调”的引导方向。

### Q4：force thresholding 的作用是什么？
**A：** 它把“最大可接受交互力”变成显式可调参数。低阈值对应更软、更安全的接触；高阈值对应更有支撑力的任务。这样同一个策略可以通过阈值切换任务风格，而不是为每个任务重训一个新策略。

### Q5：这篇论文的 sim-to-real 关键在哪里？
**A：** 一是 teacher-student 结构，teacher 用 privileged observation 学更强的 compliant dynamics，student 只保留真机可见输入；二是 reference dynamics 把复杂柔顺行为变成更稳定的学习目标；三是训练中显式暴露多种 interaction force 场景，让策略在真机接触时不至于“没见过这种被推拉方式”。

### Q6：论文的 baseline 为什么会失败？
**A：** Vanilla-RL 没见过 force perturbation，遇到接触就僵硬抵抗；Extreme-RL 虽然见过大外力，但偏向“抗冲击/抗扰动”，不是“顺从而稳定地配合接触”。所以在拥抱、握手、拿气球这种任务里，baseline 会出现更高峰值力、更差压力分布，甚至失衡。

### Q7：这篇工作最大的局限是什么？
**A：** 第一，interaction force 仍是基于 simulated spring 的近似，不完全等价于真实人体/软物体接触；第二，数据集本身限制了可学到的受力分布，尤其肩部变化还不够丰富；第三，真机仍会偶发 **1–3 N** overshoot；第四，人的定位和身高目前还依赖 mocap，不够完全自主。

---

## 📖 相关工作速览

- **HumanPlus (2024)**：强调人到人形机器人的 shadowing / imitation
- **OmniH2O (2024)**：强调通用 human-to-humanoid teleoperation
- **TWIST (2025)**：全身遥操作系统，适合与本文的 compliant policy 结合
- **FALCON / FACET / Learning Force Control for Legged Manipulation**：更偏向末端或特定 force-adaptive control
- **BeyondMimic / GMT / ExBody2**：强调 whole-body control 的通用性和 tracking 能力，但不像本文这样把“柔顺接触品质”放在中心位置

---

## 💬 讨论记录

> 📅 2026-04-19

### Q1：这篇论文最重要的技术点到底是哪一个？
**答：** 不是单纯“把 impedance control 接进 RL”，而是**用统一 spring-based 交互力模型，把 resistive contact 和 guiding contact 放进同一参考动力学框架里**。这样策略学到的是一整条上肢链路的协调柔顺，而不是单个末端点的局部顺从。

### Q2：为什么这篇论文对 humanoid 上肢接触任务特别有参考价值？
**答：** 因为很多 humanoid 论文关注的是“移动 + 操作能不能完成”，但真正落到陪伴、辅助、协作场景，用户更在意的是“你碰我的感觉是不是自然”。GentleHumanoid 把 contact force、pressure distribution 和可调安全阈值作为第一等公民，这点非常适合扩展到 assistive robotics。

### Q3：如果我要在自己的项目里借鉴这篇论文，最值得先复现哪一块？
**答：** 我会优先复现这三步：
1. 给 upper-body key links 建 impedance reference dynamics；
2. 加一个统一的 spring-based interaction-force sampler；
3. 在 reward 里显式加入 dynamics tracking + force tracking + unsafe force penalty。

这样即使先不做完整的 autonomous hugging pipeline，也能先验证“上肢是否明显更柔顺”。

---

## ⚠️ 局限性

论文最后明确提到几个限制：
- **数据集限制**：肩部受力分布还不够丰富，因为 motion dataset 本身缺少更多这类变化；作者提到可考虑引入舞蹈等更丰富数据。
- **接触建模仍是近似**：目前依赖 simulated spring force，虽然结构化、可控，但还不能完整覆盖真实接触里的摩擦、组织粘弹性等复杂效应。
- **真机仍有轻微超调**：实机里偶尔会超出目标力阈值 **1–3 N**，说明 sim-to-real 还没完全对齐。
- **自主感知还不够完整**：人的定位和身高目前还是 mocap 提供，未来更理想是用纯视觉管线替代。

---

## 🔚 我对这篇论文的判断

如果你关心的是**人形机器人在真实人机接触里的“分寸感”**，这篇论文非常值得认真看。

它不是那种靠更大模型、更大数据把 benchmark 做高一点的工作，而是明确回答了一个落地问题：

**怎么让 humanoid 在接触时既不软趴趴，也不硬邦邦，而是像人一样“该让就让、该托就托”？**

从这个角度看，GentleHumanoid 是一篇很典型的“面向真实交互质量”的 humanoid whole-body control 论文。对后续做上肢 compliance、assistive interaction、safe teleop 都有很强参考价值。
