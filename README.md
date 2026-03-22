# 📚 每日论文阅读计划

[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](LICENSE)
[![Papers](https://img.shields.io/badge/Papers-468-orange.svg)](papers/PROGRESS.md)
[![Notes](https://img.shields.io/badge/Notes-11-green.svg)](papers/)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-brightgreen.svg)](https://imchong.github.io/Humanoid_Robot_Learning_Paper_Notebooks/)
[![Deploy](https://github.com/ImChong/Humanoid_Robot_Learning_Paper_Notebooks/actions/workflows/deploy.yml/badge.svg)](https://github.com/ImChong/Humanoid_Robot_Learning_Paper_Notebooks/actions/workflows/deploy.yml)
[![Update Badges](https://github.com/ImChong/Humanoid_Robot_Learning_Paper_Notebooks/actions/workflows/update-badges.yml/badge.svg)](https://github.com/ImChong/Humanoid_Robot_Learning_Paper_Notebooks/actions/workflows/update-badges.yml)

**来源**: [awesome-humanoid-robot-learning](https://github.com/YanjieZe/awesome-humanoid-robot-learning)

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
│   ├── 02_High_Impact_Selection/      # 高影响力精选论文
│   ├── 03_Loco-Manipulation_and_WBC/  # 全身控制与移动操作
│   ├── 04_Locomotion/                 # 行走/跑酷等运动控制
│   ├── 05_Manipulation/               # 操作与灵巧手
│   ├── 06_Teleoperation/              # 遥操作
│   ├── 07_Navigation/                 # 导航
│   ├── 08_State_Estimation/           # 状态估计
│   ├── 09_Sim-to-Real/                # 仿真到真实迁移
│   ├── 10_Simulation_Benchmark/       # 仿真平台与基准测试
│   ├── 11_Hardware_Design/            # 硬件设计
│   ├── 12_Physics-Based_Animation/    # 基于物理的角色动画
│   ├── 13_Human_Motion/              # 人体运动分析与合成
│   └── PROGRESS.md                    # 全部论文阅读进度表
├── progress.json                      # 当前阅读进度追踪（JSON）
├── scripts/                           # 辅助脚本
│   └── prepare_pages.py               # GitHub Pages 部署预处理
├── _data/                             # Jekyll 数据文件
│   └── papers.json                    # 论文索引数据
├── .github/workflows/                 # CI/CD
│   └── deploy.yml                     # GitHub Pages 自动部署
├── _layouts/ _includes/ assets/       # Jekyll 网页模板和样式
├── _config.yml                        # Jekyll 配置
└── README.md                          # 本文件
```

每篇论文的笔记通过 [GitHub Pages](https://imchong.github.io/Humanoid_Robot_Learning_Paper_Notebooks/) 自动部署为在线网页。


## 笔记说明

每篇笔记采用统一结构，兼顾**深度理解**和**面试准备**：

### 正文部分

| 章节 | 内容 | 示例 |
|------|------|------|
| 📋 基本信息 | arXiv、PDF、作者、机构、发表时间 | `arXiv: 1707.06347` |
| 🎯 一句话总结 | 用一句大白话概括论文核心贡献 | "PPO 通过裁剪机制让策略更新既大胆又安全" |
| ❓ 要解决什么问题 | 问题背景 + 生活化类比，零基础能看懂 | 用"走台阶 vs 瞎子爬山"类比 PPO vs TRPO |
| 🔧 方法详解 | 逐步拆解核心方法，配公式、表格、流程图 | 概率比 → 优势函数 → 裁剪机制 → 训练流程 |
| 🚶 具体实例 | **完整数值走通**：用人形机器人场景演示算法全过程 | 状态设定 → 采样 → GAE 计算 → 裁剪更新 → 训练进展 |
| 🤖 工程价值 | 为什么这个方法对人形机器人控制重要 | PPO 成为 sim-to-real 首选的原因 |
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
| 英文缩写速查 | 论文中出现的术语缩写表 |

> 💡 附录内容因论文而异，不是每篇都有全部附录。核心原则：**有用就写，没必要就省**。

## 学习路线图

```
【基础RL】
  PPO → AWR
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

