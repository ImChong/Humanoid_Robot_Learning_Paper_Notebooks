# 📚 每日论文阅读计划

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-brightgreen.svg)](https://imchong.github.io/Humanoid_Robot_Learning_Paper_Notebooks/)
[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](LICENSE)
[![Papers](https://img.shields.io/badge/Papers-531-orange.svg)](papers/PROGRESS.md)
[![Notes](https://img.shields.io/badge/Notes-47-green.svg)](papers/)

**来源**: [awesome-humanoid-robot-learning](https://github.com/YanjieZe/awesome-humanoid-robot-learning)

**📖 待读论文清单**: [papers/PROGRESS.md](papers/PROGRESS.md) — 全量 531 篇论文的阅读进度表（来自上游 awesome 列表）。

**🛠️ 仓库开发待办**: [papers/todos/TODO_v4.md](papers/todos/TODO_v4.md) — 笔记 / 站点 / 工具链的开发任务（最新 v4，历史版本见 [`papers/todos/`](papers/todos/)）。

**📌 当前快照**: 已覆盖 14 个分类、46 篇笔记；`prepare_pages.py` 当前无 `[STUB]` 告警，下一阶段重点是 Jekyll 构建验证、统计口径治理与源码对照增强。

## 规则

1. 每天早上 7:00 推送当日论文阅读提醒
2. 冲回复"理解了"后，才进入下一篇
3. 如果当天没有回复"理解了"，第二天继续提醒同一篇
4. 回复"理解了"后，对话记录也会保存到对应的 MD 笔记中
5. 可以随时说"读下一篇"跳到一篇

## 项目结构

```
├── papers/                            # 论文笔记（按类别分目录）
│   ├── 01_Foundational_RL/            # 基础 RL 算法（PPO、AWR、DeepMimic、AMP 等）
│   ├── 02_Motion_Retargeting/         # 动作重定向（人体骨架 → 机器人骨架）
│   ├── 03_High_Impact_Selection/      # 高影响力精选论文
│   ├── 04_Loco-Manipulation_and_WBC/  # 全身控制与移动操作
│   ├── 05_Locomotion/                 # 行走/跑酷等运动控制
│   ├── 06_Manipulation/               # 操作与灵巧手
│   ├── 07_Teleoperation/              # 遥操作
│   ├── 08_Navigation/                 # 导航
│   ├── 09_State_Estimation/           # 状态估计
│   ├── 10_Sim-to-Real/                # 仿真到真实迁移
│   ├── 11_Simulation_Benchmark/       # 仿真平台与基准测试
│   ├── 12_Hardware_Design/           # 硬件设计
│   ├── 13_Physics-Based_Animation/   # 基于物理的角色动画
│   ├── 14_Human_Motion/              # 人体运动分析与合成
│   ├── todos/                        # 仓库开发待办归档（TODO_v1/v2/v3/v4.md）
│   └── PROGRESS.md                   # 全部论文阅读进度表（待读清单）
├── progress.json                      # 当前阅读进度追踪（JSON）
├── scripts/                           # 辅助脚本
│   └── prepare_pages.py              # GitHub Pages 部署预处理
├── _data/                             # Jekyll 数据文件
│   └── papers.json                   # 论文索引数据
├── .github/workflows/                 # CI/CD
│   └── deploy.yml                   # GitHub Pages 自动部署
├── _layouts/ _includes/ assets/       # Jekyll 网页模板和样式
├── _config.yml                        # Jekyll 配置
└── README.md                          # 本文件
```

每篇论文的笔记通过 [GitHub Pages](https://imchong.github.io/Humanoid_Robot_Learning_Paper_Notebooks/) 自动部署为在线网页。

## 源码对照

笔记中涉及的论文，**如果**在 [MimicKit](https://github.com/xbpeng/MimicKit)（xbpeng 大神的运动模仿框架）中有官方实现，笔记会附上「📁 MimicKit 源码对照」章节，包含：

- **关键代码块**：与笔记讲解一一对应的源码（网络结构、loss 计算、训练循环等）
- **配置示例**：YAML 超参数文件的关键参数说明
- **训练 / 测试命令**：可一键运行的命令行

> MimicKit 是一个轻量级的运动模仿框架，支持 Isaac Gym / Isaac Lab / Newton 等仿真后端。目前已覆盖：DeepMimic、AMP、AWR、ASE、LCP 等主流算法。源码地址：[https://github.com/xbpeng/MimicKit](https://github.com/xbpeng/MimicKit)

## 笔记说明

每篇笔记采用统一结构，兼顾**深度理解**和**面试准备**：

### 正文部分

| 章节 | 内容 | 示例 |
|------|------|------|
| 📋 基本信息 | arXiv、PDF、作者、机构、发表时间 | `arXiv: 1707.06347` |
| 🎯 一句话总结 | 用一句大白话概括论文核心贡献 | "PPO 通过裁剪机制让策略更新既大胆又安全" |
| 📌 英文缩写速查 | 论文中出现的术语缩写表 | 放在一句话总结之后、正文之前 |
| ❓ 要解决什么问题 | 问题背景 + 生活化类比，零基础能看懂 | 用"走台阶 vs 瞎子爬山"类比 PPO vs TRPO |
| 🔧 方法详解 | 逐步拆解核心方法，配公式、表格、流程图 | 概率比 → 优势函数 → 裁剪机制 → 训练流程 |
| 🚶 具体实例 | **完整数值走通**：用人形机器人场景演示算法全过程 | 状态设定 → 采样 → GAE 计算 → 裁剪更新 → 训练进展 |
| 🤖 工程价值 | 为什么这个方法对人形机器人控制重要 | PPO 成为 sim-to-real 首选的原因 |
| 📁 MimicKit 源码对照 | *(可选，有源码时出现)* 对应的 MimicKit 官方实现代码与配置 | PPO/AWR/LCP 等主流算法均有覆盖 |
| 🎤 面试高频 Q&A | 5-8 个高频问题 + 参考回答，直接可用 | "PPO 和 TRPO 的区别？""裁剪具体怎么起作用？" |
| 💬 讨论记录 | 阅读过程中的疑问、讨论和澄清 | surrogate loss 的直觉理解 |

### 附录部分

| 附录 | 内容 |
|------|------|
| 算法变体 | 不同版本对比（如 PPO-Clip vs PPO-Penalty） |
| Loss 完整拆解 | 含各项系数的完整公式 |
| 网络架构 | Actor-Critic 的典型结构 |
| 超参数速查表 | 常用超参数及推荐值 |
| 训练过程可视化 | 各指标随训练的变化趋势 |
| 实验结果 | 关键实验数据与对比 |
| 相关工作 | 上下游论文关系 |

> 💡 附录内容因论文而异，不是每篇都有全部附录。核心原则：**有用就写，没必要就省**。

## 学习路线图

```
【基础RL】
  PPO → AWR
       ↓
【人体动作数据层】          ← 模仿类方法开始需要参考数据
  AMASS / HumanML3D  →  人体 SMPL 动作数据集
       ↓
【动作重定向层】          ← 人体骨架 → 机器人骨架的桥梁
  几何重定向 (IK-based)  →  GMR / Retargeting Matters (2025)
       ↓                    ↑ 决定模仿策略的动作质量上限
       ↓
【精确模仿主线】          【风格学习主线】
  DeepMimic (2018)  →→→  AMP (2021)
       ↓                    ↓
  PHC (2023)            ADD (2025)
       ↓
【技能组合主线】
  ASE (2022) → CALM (2023) → PULSE (2024)
       ↓
【扩散+控制终点】
  Diffusion Policy → BeyondMimic (2025)

【Sim-to-Real 工程层】  ← 横跨整个路线
  Domain Randomization (2017) → LCP (2025)
  ↑ sim环境随机化迁移        ↑ 动作平滑，替代低通滤波器
```

> 💡 **为什么把动作重定向单列一层**：精确模仿 / 风格学习 / 遥操作（OmniH2O、ExBody2 等）都依赖"人体动作 → 机器人可执行轨迹"的转换；重定向质量直接决定下游策略能学到什么动作，是被很多论文一笔带过、却最容易踩坑的工程环节。

## 源码层面一览（MimicKit 覆盖情况）

| 论文 | MimicKit 源码 | 核心实现文件 |
|------|:---:|------|
| PPO | ✅ | `mimickit/learning/ppo_agent.py` |
| AWR | ✅ | `mimickit/learning/awr_agent.py` |
| AMP | ✅ | `mimickit/learning/amp_agent.py` |
| DeepMimic | ✅ | `mimickit/learning/deepmimic_agent.py` |
| ASE | ✅ | `mimickit/learning/ase_agent.py` |
| **LCP** | ✅ | `mimickit/learning/lcp_agent.py` |
| ADD | ✅ | `mimickit/learning/add_agent.py` |
| MimicKit | ✅ | 官方框架论文与仓库总览 |
| PULSE | ❌ | 笔记骨架已建，MimicKit 暂无覆盖 |
| Diffusion Policy | ❌ | 非 MimicKit 覆盖范围（模仿学习框架不同） |
| BeyondMimic | ❌ | 2025 年新工作，MimicKit 暂无覆盖 |
| ProtoMotions3 | N/A | NVIDIA sibling framework，非 MimicKit 覆盖项 |

> 注：打 ✅ 表示笔记中已附「MimicKit 源码对照」章节，可直接对照论文公式与代码实现。
