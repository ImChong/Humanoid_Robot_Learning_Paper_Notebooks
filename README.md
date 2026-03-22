# 📚 每日论文阅读计划

**来源**: [awesome-humanoid-robot-learning](https://github.com/YanjieZe/awesome-humanoid-robot-learning)

## 规则

1. 每天早上 7:00 推送当日论文阅读提醒
2. 冲回复"理解了"后，才进入下一篇
3. 如果当天没有回复"理解了"，第二天继续提醒同一篇
4. 回复"理解了"后，对话记录也会保存到对应的 MD 笔记中
5. 可以随时说"读下一篇"跳到一篇

## 项目结构

```
├── papers/                        # 论文笔记（按类别分目录）
│   ├── 01_Foundational_RL/        # 基础 RL 算法（PPO、AWR、DeepMimic、AMP 等）
│   ├── 03_Loco-Manipulation_and_WBC/  # 全身控制与移动操作
│   ├── 04_Locomotion/             # 行走/跑酷等运动控制
│   ├── ...                        # 其他类别（操作、遥操作、导航、仿真等）
│   └── 每篇论文一个子目录/          # 包含 .md 笔记和 .pdf 原文
├── progress.json                  # 阅读进度追踪（当前论文、状态、日期）
├── scripts/                       # 辅助脚本
│   └── prepare_pages.py           # GitHub Pages 部署预处理
├── _layouts/ _includes/ assets/   # Jekyll 网页模板和样式
├── _config.yml                    # Jekyll 配置
└── README.md                      # 本文件
```

每篇论文的笔记通过 [GitHub Pages](https://imchong.github.io/Humanoid_Robot_Learning_Paper_Notebooks/) 自动部署为在线网页。


## 笔记说明

每篇笔记包含：
- 论文基本信息（PDF、GitHub、项目主页等）
- 核心问题与动机
- 方法详解（深入浅出，面试可答）
- 工程复现要点
- 关键公式与算法
- 面试高频问题 & 参考回答
- 讨论记录

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

