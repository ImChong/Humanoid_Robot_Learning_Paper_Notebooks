---
layout: paper
title: "Retargeting Matters: General Motion Retargeting for Humanoid Motion Tracking"
zhname: "重定向 matters：面向人形运动跟踪的通用运动重定向"
category: "Loco-Manipulation and WBC"
---

# Retargeting Matters: General Motion Retargeting for Humanoid Motion Tracking
**把"人类动作 → 机器人动作"这一步做到好，是 RL tracking 能不能跟上的关键**

> 📅 阅读日期: 2026-04-19
> 🏷️ 板块: Loco-Manipulation and Whole-Body-Control
> ℹ️ 本笔记基本信息与仓库使用部分取自官方 GitHub README；论文**方法细节与实验数字**受限于无法访问 arXiv，标有 🚧 待核对。

---

## 📋 基本信息

| 项目 | 链接 |
|------|------|
| **arXiv** | [2510.02252](https://arxiv.org/abs/2510.02252) |
| **GitHub** | [YanjieZe/GMR](https://github.com/YanjieZe/GMR) |
| **项目主页** | 🚧 待核对（`yanjieze.com/GMR/` 候选） |
| **PDF** | [arXiv PDF](https://arxiv.org/pdf/2510.02252) |
| **发布时间** | 2025 年 10 月 |
| **许可** | MIT License（代码） |
| **机构** | Stanford University（C. Karen Liu / Jiajun Wu 组） |

**作者**: João Pedro Araújo, Yanjie Ze, Pei Xu, Jiajun Wu, C. Karen Liu

**一行定位**：TWIST 遥操 / GentleHumanoid / OmniXtreme 等一批工作**共用**的那个"人类动作 → 机器人动作"翻译器 —— 把它从藏在实验代码里的工具单独拎出来做成开源论文。

---

## 🎯 一句话总结

GMR 把"人类动作重定向到人形机器人"这件过去被各家方法**藏在附录里**的事情单独做成一个**通用、快速、CPU-only**的库，一条管线支持 18+ 款人形硬件与 4+ 种人体运动格式，让下游的 RL tracking / 遥操 / 模仿学习研究者可以**不重新造轮子**就拿到高质量的机器人参考动作。

---

## 📌 英文缩写速查

| 缩写 | 全称 | 简单解释 | 生活类比 |
|------|------|----------|----------|
| **GMR** | General Motion Retargeting | 本文方法 / 库的名字 | 一个通用的"动作翻译官" |
| **Retargeting** | Motion Retargeting | 把 A 骨架的动作搬到 B 骨架上 | 把姚明的舞步翻译给小学生跳 |
| **DOF** | Degree of Freedom | 自由度 | 一个关节能转几个方向 |
| **SMPL-X** | — | 参数化人体模型（含手指 / 表情） | 用一组数字描述人体的姿态 + 形状 |
| **AMASS** | Archive of Motion Capture as Surface Shapes | 大规模人体 mocap 数据集（统一到 SMPL） | mocap 的"大图书馆" |
| **OMOMO** | Object MOtion with human MOtion | 含人 - 物交互的 mocap 数据集 | 专门录"人和东西一起动"的库 |
| **BVH / FBX** | 标准动捕格式 | 另外两种常见 mocap 文件 | 不同工作室的"录音格式" |
| **LAFAN1** | Lafayette Animation Dataset | 常用动画 BVH 数据集 | 一份 BVH 格式的素材库 |
| **GVHMR** | 近年单目视频 → 人体 motion 方法 | 把手机视频转 SMPL 动作 | 视频 → 骨架的"视觉重建器" |
| **IK** | Inverse Kinematics | 逆运动学：从目标位姿解关节角 | "手要摸到那里" → 算出每个关节转多少 |
| **TWIST** | Teleoperated Whole-body Imitation System | 同组的遥操框架，直接使用 GMR | GMR 的头号"用户"工作 |
| **RL tracking policy** | — | 让机器人跟着一段参考动作跑的 RL 策略 | 让机器人跟拍子跳舞的"训练好的演员" |
| **CPU-only** | — | 不依赖 GPU / CUDA | 普通笔记本也能跑 |

---

## ❓ Retargeting Matters 要解决什么问题？

这篇论文标题里的 "Matters" 有点叫板味道。在 humanoid RL tracking 这条技术主线上：

### 问题 1：大家都把 retargeting 当"前处理脚本"，但它其实是瓶颈
很多 humanoid tracking 论文（OmniH2O / ExBody2 / OmniXtreme / GentleHumanoid 等）都有一条默认流程：

```
人类 mocap (SMPL-X) → [某种 retargeting 脚本] → 机器人关节轨迹 → RL tracking policy
```

作者观察到的痛点：**retargeting 这一步的质量直接决定下游 RL 能否跟得上**。如果翻译的参考动作本身就不可行（超过关节限制、脚穿地板、手臂自碰撞），RL 训练要么跟不上、要么跟上了但 sim-to-real 崩掉。

### 问题 2：每家论文都自己写 retargeting，配方互不兼容
- OmniH2O 的 retargeting 参数化是自家定制的；
- ExBody2 的有自己的 loss；
- OmniXtreme 的又是另一套；
- 搞到研究者每做一个新机器人 / 新数据集，都要重新写一遍。

### 问题 3：很多实现要 GPU 甚至 CUDA，部署不方便
在"带笔记本到实验室做遥操 demo"这种场景里，GPU 依赖是个障碍。

### GMR 的回答
一套**通用、快速、CPU-only、全开源**的管线：

- 一条命令把 SMPL-X / BVH / FBX / Xsens / GVHMR 的人体动作翻译到 18+ 款人形机器人。
- 单 CPU 60–70 FPS（Ryzen Threadripper） / 35–45 FPS（i9-13900K），实时遥操没压力。
- MIT 协议，配合 TWIST 遥操系统发布，后续 GentleHumanoid / OmniXtreme 等都把 GMR 作为默认 retargeting 工具。

---

## 🔧 方法详解

> 🚧 论文方法段的具体 loss / 约束 / 优化器**细节尚未核对**（arXiv 页面在本环境不可访问），下面先给出**管线级**的、可从 GitHub 代码结构推断的概览。真正公式请以论文为准。

### 输入输出

| 部件 | 内容 |
|------|------|
| 输入 | 人类 motion sequence（SMPL-X / BVH / FBX / Xsens / GVHMR，含 root 位姿 + 各骨骼旋转） |
| 机器人规格 | URDF / MJCF + 关节限位 + 骨骼长度（18+ 款已内置） |
| 输出 | 机器人关节角序列（+ root pose），可直接喂给 RL tracking 策略或 PD 控制器 |

### 一条管线的 4 个关键块（推测，🚧 待核对论文公式）

1. **骨骼对齐 Body-to-robot mapping**
   - 人体的 ~52 个 SMPL-X 关节 ↔ 机器人 ~19–29 DOF 的对应关系。
   - 对每款机器人手工定义一次"人 -> 机器人"的骨骼映射表。

2. **Scale / root alignment**
   - 按身高 / 臂展把人类 motion 的 root trajectory 缩放到机器人尺度。
   - 必要时做落脚点对齐（避免脚穿地板或悬空）。

3. **约束 IK 优化 Inverse kinematics with feasibility constraints**
   - 目标：每个机器人关节角尽量复现人类对应骨骼的旋转 / 末端位置。
   - 约束：关节角 / 速度限位、自碰撞、接触 / 足端在地面。
   - 求解：CPU-friendly 的数值优化（Levenberg-Marquardt / SLSQP 等，🚧 待核对）。

4. **后处理 Post-processing**
   - 时序滤波去抖；
   - 必要时对手腕 / 手指做单独重定向（SMPL-X 原生支持手指，一些机器人不支持）；
   - 落地为 `.pkl` 文件，兼容 RL tracking 训练集管线。

### 与其他 retargeting 思路的对比

| 思路 | 代表工作 | GMR 的差异 |
|------|---------|-----------|
| 基于优化的 IK retargeting | 各家自己写的脚本 | GMR 把它**统一通用化 + 加入机器人规格数据库** |
| 基于学习的 retargeting | SkeletonPose 等 | GMR 选择**非学习路线**，牺牲一点表现换来**确定性 + 速度 + 无需训练** |
| 物理仿真 + 策略跟随 | PHC 等把 RL 和 retargeting 混在一起 | GMR 只负责 kinematic 层面的 retargeting，RL 留给下游 |

---

## 🚶 具体实例（仓库脚本走通）

### 例 1：把 AMASS 中的一段 SMPL-X 动作重定向到 Unitree G1

```bash
conda create -n gmr python=3.10 -y
conda activate gmr
pip install -e .

python scripts/smplx_to_robot.py \
    --smplx_file data/amass/Dance_01.npz \
    --robot unitree_g1 \
    --save_path outputs/g1_dance_01.pkl \
    --rate_limit
```

输出：`outputs/g1_dance_01.pkl`，内容是一段与输入同帧率的 G1 关节角 + root 轨迹。

### 例 2：把 LAFAN1 的 BVH 翻译成 Unitree H1 的参考动作

```bash
python scripts/bvh_to_robot.py \
    --bvh_file data/lafan1/walk1_subject1.bvh \
    --robot unitree_h1 \
    --save_path outputs/h1_walk.pkl \
    --format lafan1
```

### 例 3：可视化

```bash
python scripts/vis_robot_motion.py \
    --robot unitree_g1 \
    --robot_motion_path outputs/g1_dance_01.pkl
```

### 典型下游串接

```
(手机 RGB 视频) --GVHMR--> (SMPL-X) --GMR--> (G1 关节角)
                                              └─► RL tracking policy
                                              └─► 真机 PD 控制器
```

---

## 🤖 工程价值

1. **对研究者**：做人形 tracking / 遥操时**不再需要从零写 retargeting**，也不用从同行那里 copy 个别人自用的脚本。`pip install -e .` + 一行命令就能产出训练可用的参考动作。
2. **对 sim-to-real**：GMR 内置了关节限位 / 自碰撞等 feasibility 约束，比"一把 IK 解完就用"的脚本更容易让下游 RL 收敛，也更不容易在真机上崩。
3. **对整个 stack 的意义**：humanoid RL tracking 这条线有一个**长期没被单独命名的瓶颈**，GMR 的贡献就是**把这块砍下来单独发表**，让后续工作可以显式引用它、讨论它，而不是每篇论文都塞在附录 "retargeting details"。

本仓库中已引用 GMR 作为默认 retargeting 工具的笔记（表示本工具的工程辐射范围）：

| 笔记 | 如何引用 GMR |
|------|--------------|
| `03_Loco-Manipulation_and_WBC/GentleHumanoid` | 全部训练 / 视频 → 机器人链路使用 GMR 做 retargeting |
| `03_Loco-Manipulation_and_WBC/OmniXtreme` | 在"重定向工具"表中显式列 GMR |

---

## 📁 源码对照

仓库结构要点（摘自 README）：

| 入口脚本 | 作用 |
|----------|------|
| `scripts/smplx_to_robot.py` | SMPL-X → 机器人关节序列 |
| `scripts/bvh_to_robot.py` | BVH → 机器人关节序列 |
| `scripts/vis_robot_motion.py` | 可视化重定向结果 |
| `robot_cfgs/` (推测) | 18+ 款人形的 URDF / 关节映射 / 限位配置 |

性能基准（README 给出）：
- AMD Ryzen Threadripper 7960X：**60–70 FPS**
- Intel Core i9-13900K：**35–45 FPS**

支持的 18+ 款机器人（部分）：
Unitree G1 (29 DOF) · Unitree H1 (19 DOF) · Unitree H1-2 (27 DOF) · Booster T1 / K1 · Fourier N1 / GR3 · Berkeley Humanoid Lite · HighTorque Hi · PAL Talos · Galaxea R1 Pro · Kuavo S45 · ...（完整列表见仓库）。

支持的输入格式：
- **SMPL-X**：AMASS / OMOMO
- **BVH**：LAFAN1 / Nokov
- **FBX**：OptiTrack
- **Xsens MVN**
- **GVHMR**（单目视频）

---

## 🎤 面试高频问题 & 参考回答

**Q1：为什么 retargeting 这件事值得单独发一篇论文？它不就是一个 IK 脚本吗？**
A：两点。一是**通用性**——过去每家工作都自己写，兼容一款机器人、一种输入格式，换个机器人就要重写；GMR 把 18+ 款人形 + 5 种格式做成一个库。二是**feasibility 约束的工程价值**——很多下游 RL 训练失败的根本原因是参考动作本身不可行（关节超限、自碰撞、脚穿地板），把这些约束做对，下游 RL 就好收敛、sim-to-real 更稳。

**Q2：GMR 为什么是 CPU-only 的？不是 GPU 快吗？**
A：retargeting 的计算量是**每帧几十到上百关节的一个非线性最小二乘**，规模不大；CPU 上的成熟 IK 求解器（SLSQP / LM / ceres 风格的 solver）单帧就几毫秒。GPU 的启动开销反而划不来。CPU-only 还带来部署便利：遥操场景里一台笔记本就够，不必等 CUDA 环境。

**Q3：GMR 和 PHC 的 retargeting 有什么区别？**
A：PHC 的 retargeting 嵌在 kinematic policy + RL 里，是"一边训练一边学 retargeting"的路线；GMR 走**非学习的显式优化**路线，牺牲一点表现力（比如无法"创造"原动作里没有的关节补偿）换来确定性、速度和零训练门槛。两条路线互补：GMR 做一层干净的 kinematic 重定向，下游可以继续叠 PHC 式的 RL tracking 做物理精修。

**Q4：为什么"Retargeting Matters"在标题里用了个略叫板的口气？**
A：🚧 论文原文动机未核对，但从同组工作（TWIST / GentleHumanoid / OmniXtreme）看，作者希望**把 retargeting 提到和 policy learning / sim-to-real 同一级的地位**——过去它是"随便写个脚本就行"的工具，实际却是影响 tracking 成败的关键环节。

**Q5：GMR 支持手指 / SMPL-X 表情吗？**
A：输入格式里 SMPL-X 原生有手指，但是否真的被重定向到机器人手上取决于机器人自由度——G1 / H1 等主流人形大多只到手腕，GMR 会截断到这些关节；支持灵巧手的平台（如 ByteDexter、Galaxea R1）可以通过扩展 `robot_cfgs/` 加入。

---

## 💬 讨论记录

- **Q**（2026-04-19）：GMR 是 kinematic retargeting，为什么 OmniXtreme / GentleHumanoid 的 Q&A 里还说它"影响 sim-to-real"？
  A：**间接影响**。GMR 本身不做物理；但它产出的参考动作是 RL tracking 的 target。如果 retargeting 就不 feasible，RL 要么追不上要么追上了也无法在真机复现。**Sim-to-real 的起点是 feasible 的参考动作**。

- **Q**：如果要给一个新的人形（比如 Fourier GR3）接入 GMR，需要哪些信息？
  A：URDF / MJCF 模型、关节限位表、人体骨骼到机器人关节的手动映射表（一次性工作）、可选的接触 / 自碰撞配置。按 `robot_cfgs/` 里现有的条目抄一份即可。

---

## 📎 附录

### A. BibTeX

```bibtex
@article{joao2025gmr,
  title={Retargeting Matters: General Motion Retargeting for Humanoid Motion Tracking},
  author={Joao Pedro Araujo and Yanjie Ze and Pei Xu and Jiajun Wu and C. Karen Liu},
  year={2025},
  journal={arXiv preprint arXiv:2510.02252}
}

@software{ze2025gmr,
  title={GMR: General Motion Retargeting},
  author={Yanjie Ze and João Pedro Araújo and Jiajun Wu and C. Karen Liu},
  year={2025},
  url={https://github.com/YanjieZe/GMR}
}
```

### B. 与其他方向的关联

| 方向 | 关系 |
|------|------|
| TWIST (Ze 2025, arXiv 2505.02833) | GMR 的头号使用者，一起发布 |
| GentleHumanoid | 用 GMR 把 AMASS / InterX / OMOMO 翻译到 G1，训练阻抗 tracking policy |
| OmniXtreme | 在"重定向工具"中明确列出 GMR |
| PHC / ExBody2 | retargeting 思路的前辈，GMR 走的是"显式、通用、CPU"路线 |
| GVHMR / PromptHMR | 视频 → SMPL-X 的上游，GVHMR 已作为 GMR 的一种输入格式 |

### C. 开放问题

1. GMR 的 IK 用的是哪个 solver？🚧 待核对论文方法段。
2. 对接触丰富的动作（翻滚、地面支撑），显式 IK 是否仍然稳定？论文是否报告了失败模式？🚧 待核对实验段。
3. 对灵巧手的扩展（ByteDexter 等）支持到什么程度？🚧 待核对。
