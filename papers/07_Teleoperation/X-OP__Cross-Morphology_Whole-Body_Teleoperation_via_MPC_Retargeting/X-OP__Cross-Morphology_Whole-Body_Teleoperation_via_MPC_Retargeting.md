---
layout: paper
paper_order: 9
title: "X-OP: Cross-Morphology Whole-Body Teleoperation via MPC Retargeting"
zhname: "X-OP：用一台 Apple Vision Pro 驱动、跨机器人形态都不用重训的分层全身遥操作——上层 MPC（KMPPI）重定向器同时优化「贴合操作者意图」与「机器人动力学可行性」，下层直接复用现成低级控制器，配「每步重置仿真态」做状态同步 + LiDAR-SLAM 全局位姿纠漂；Unitree G1 与 RB-Y1 即插即用"
category: "Teleoperation"
---

# X-OP: Cross-Morphology Whole-Body Teleoperation via MPC Retargeting
**分层、跨形态、即插即用的全身遥操作：只用一台 Apple Vision Pro，上层用 MPC 重定向器把操作者意图转成「动力学可行」的指令喂给现成低级控制器，无需为每种机器人重新训练策略；并用「每个 MPC 步重置仿真状态」的状态同步对抗真机噪声与接触敏感，用 LiDAR-Inertial SLAM 抑制长时漂移。同一套方法直接部署到人形 Unitree G1 与移动操作机 Rainbow RB-Y1**

> 📅 阅读日期: 2026-06-17
>
> 🏷️ 板块: 07 Teleoperation · 全身遥操作 / 跨形态 / MPC 运动重定向 / XR 单设备 / 即插即用
>
> 🔁 推进轨: 模块轮转（06_Manipulation → **07_Teleoperation**）

---

## 📋 基本信息

| 项目 | 链接 |
|---|---|
| arXiv | [2606.07934](https://arxiv.org/abs/2606.07934) |
| HTML | [arXiv HTML](https://arxiv.org/html/2606.07934) |
| PDF | [arXiv PDF](https://arxiv.org/pdf/2606.07934) |
| **发布时间** | 2026-06-06 (arXiv) |
| 源码 | 截至当前未见公开代码仓库 / 项目主页（以 arXiv 后续版本为准） |
| 作者 | Jen-Wei Wang, Sarthak Kaingade, Andrea Tagliabue, Nicholas Morozovsky |
| 机构 | Amazon · University of California, Berkeley（第一作者） |
| 输入设备 | Apple Vision Pro（头 + 双腕 6D 位姿，双指捏合手势切换站立/移动） |
| 平台 | 人形 Unitree G1（29 DoF，低级控制器 FALCON）· 移动操作机 Rainbow RB-Y1（22 DoF，差速底盘比例控制） |
| 验证 | 仿真 + 真机（两个平台均部署同一套重定向器） |

---

## 🎯 一句话总结

> 全身遥操作是给 loco-manipulation 任务**规模化采数据**的关键，但外骨骼套装、多相机方案又贵又笨、对环境要求高；新近用**单台 XR 设备 + 端到端 RL 策略**的方案虽然便宜，却**要为每种机器人重训**、容易在分布外（OOD）失败，且重定向时**不管动力学可行性**。X-OP 提出一个**分层、跨形态、即插即用**的框架：上层用 **MPC（KMPPI 路径积分）重定向器**，把 Apple Vision Pro 给出的「头 + 双腕位姿」同时对齐**操作者意图**与**机器人动力学可行性**，直接生成现成低级控制器能吃的指令；为保证在线鲁棒，提出**每个 MPC 步重置仿真状态**的状态同步（对抗噪声测量与接触敏感），并接入 **LiDAR-Inertial SLAM（Fast-LIO）全局位姿反馈**抑制长时漂移。同一套方法在人形 **Unitree G1** 与移动操作机 **Rainbow RB-Y1** 上**都不改、都能跑**。

---

## 📌 英文缩写速查

| 缩写 | 全称 | 解释 |
|---|---|---|
| X-OP | Cross-morphology teleOPeration | 本文方法名：跨形态全身遥操作 |
| MPC | Model Predictive Control | 模型预测控制，上层重定向用 |
| KMPPI | Kernel(ized) Model Predictive Path Integral | 采样式 MPC 求解器，用核插值平滑控制序列 |
| XR / AVP | Apple Vision Pro | 唯一输入设备，自带视觉-惯性 SLAM 跟踪头/腕 |
| SLAM | Simultaneous Localization and Mapping | 此处用 LiDAR-Inertial（Fast-LIO）做全局位姿反馈 |
| OOD | Out-of-Distribution | 端到端 RL 策略部署时的失败来源之一 |
| WBC | Whole-Body Control | 全身控制 |

---

## ❓ 论文要解决什么问题？

1. **现有遥操作太贵/太受限**：外骨骼套装、多相机阵列成本高、复杂、对环境有约束，难规模化采数据。
2. **端到端 RL 遥操作有三痛**：① 换机器人就要**重训**；② 容易 **OOD 失败**；③ 运动重定向**只对齐姿态、忽略动力学可行性**，导致动作不稳。
3. **真机在线执行不鲁棒**：实测量噪声大、接触动力学敏感，长时遥操作还会**累积漂移**。

**目标**：一套**与形态无关、与低级控制器无关**、即插即用、可实时按用户偏好调行为的全身遥操作框架。

---

## 🔧 方法详解

### 分层结构

- **上层：MPC 重定向器（KMPPI）**——把 AVP 的「头 + 双腕」目标位姿解算成最优指令；把**低级策略与仿真动力学当作内部约束**，从而生成「动力学可行」的命令。
- **下层：现成低级控制器**——既可是 RL 策略也可是模型控制器（框架对其类型不可知）；人形用 **FALCON**（RL，7 维指令：腰高/朝向/速度/偏航率），移动操作机用差速底盘比例控制（8–13 维）。

### MPC 重定向目标（式 1）

最小化多项加权代价：
- **目标跟踪代价**：基座位置/朝向对齐操作者目标
- **接触点代价**：站立支撑时维持稳定
- **避碰代价**：指数障碍函数
- **控制能量代价**：动作幅度惩罚
- **终端代价**：horizon 末端收敛

核心思想：**联合优化「贴合操作者意图」与「机器人动力学可行性」**，而不是先重定向再丢给控制器硬跟。

### 状态同步：每个 MPC 步重置仿真态（式 2）

用一个**非线性最小二乘**把带噪 SLAM/编码器测量对齐到估计的关节/位姿配置，并用软惩罚强制接触约束（脚-地或轮-地），由 **SQP（DAQP，经 Mink）** 求解。这样在每个 MPC 步把仿真状态"拉回"真机当前态，专治**噪声测量与接触敏感**。

### 全局位姿反馈：LiDAR-Inertial SLAM

用 **Fast-LIO** 持续给出全局位姿（位置/朝向/速度），抑制长时遥操作的**累积漂移**，两个平台通用。

---

## 🧭 整体流程（mermaid）

<div class="mermaid">
flowchart LR
    subgraph IN["🥽 输入: Apple Vision Pro"]
        AVP["头 T_head + 双腕 T_lw/T_rw<br/>双指捏合切换 站立/移动"]
    end

    subgraph HI["🧠 上层: MPC 重定向器 (KMPPI)"]
        OBJ["代价: 目标跟踪 + 接触<br/>+ 避碰 + 能量 + 终端"]
        SYNC["状态同步<br/>每步重置仿真态 (NLS/SQP)"]
        SLAM["LiDAR-SLAM (Fast-LIO)<br/>全局位姿纠漂"]
    end

    subgraph LO["🦿 下层: 现成低级控制器"]
        CTRL["RL 或 模型控制器<br/>(框架不可知)"]
    end

    subgraph ROB["🤖 跨形态部署 (不改不重训)"]
        G1["Unitree G1 (29DoF)<br/>FALCON 策略"]
        RBY1["Rainbow RB-Y1 (22DoF)<br/>差速底盘比例控制"]
    end

    AVP --> OBJ
    SLAM --> SYNC
    SYNC --> OBJ
    OBJ -->|"动力学可行指令"| CTRL
    CTRL --> G1
    CTRL --> RBY1

    style IN fill:#e8eef8,stroke:#2c3e80,color:#1a2452
    style HI fill:#fdecea,stroke:#c0392b,color:#641e16
    style LO fill:#e8f8e8,stroke:#27ae60,color:#1b5e20
    style ROB fill:#fff3e0,stroke:#fb8c00,color:#4e342e
</div>

---

## 💡 核心贡献

1. **跨形态 + 即插即用**：单台 AVP 驱动，**不为每种机器人重训策略**，人形与移动操作机共用一套重定向器。
2. **MPC 重定向兼顾「意图 + 可行性」**：把低级策略与仿真动力学作内部约束，生成动力学可行的指令，而非只做姿态映射。
3. **状态同步（每步重置仿真态）**：用 NLS/SQP 把仿真态拉回带噪真机态，专治接触敏感与测量噪声。
4. **SLAM 全局位姿反馈**：Fast-LIO 抑制长时漂移。
5. **实时行为可定制**：用户可按偏好在线调遥操作行为。

---

## 📊 关键实验结果（结构性总结）

| 维度 | 设置 / 结论 |
|---|---|
| 人形（仿真） | 双点触摸 / 抓放：10/10 成功；较基线**完成时间 ↓约 30%、平衡功耗 ↓约 20%** |
| 人形（真机） | 双点触摸 10/10（基线 6/10）；抓放 9/10（基线 5/10） |
| 移动操作机（仿真） | 双点触摸/抓放 10/10 成功且**0 碰撞**（基线分别 4/10、9/10 次碰撞） |
| 移动操作机（真机） | 双点触摸 10/10、0 碰撞；抓放 7/10、0 碰撞（失败主因为抓取不稳） |
| 对比基线 | ① 直接映射 + FALCON；② 直接映射 + AMO；③ 去掉状态同步的 MPC（消融） |

> ⚠️ 详细数值与图表以 arXiv [2606.07934](https://arxiv.org/abs/2606.07934) 正文为准。

---

## 🤖 工程价值

- **"重定向 = 优化"而非"映射"**：把动力学可行性显式塞进 MPC 代价，是比手工 IK + 有限差分更稳的遥操作重定向思路。
- **与低级控制器解耦**：上层 MPC 对下层（RL/模型）不可知，换机器人/换控制器都能复用，规模化采数据友好。
- **状态同步是真机鲁棒关键**：每步把仿真态对齐到带噪真机态，针对接触敏感这一遥操作老大难。
- **限制**：① AVP 视野有限会遮挡障碍、增加导航难度；② 避碰与完成时间存在权衡（仿真里斥力会略增耗时）；③ 抓取稳定性仍是独立难题（真机抓放失败多因抓取不稳）；④ 截至当前未见开源代码。
- **未来**：把 MPC 蒸馏进神经网络提响应速度、引入力觉做接触密集任务。

---

## 🎤 面试参考

**Q：X-OP 相比「单 XR + 端到端 RL」遥操作好在哪？**
A：端到端 RL 要换机器人就重训、易 OOD、重定向忽略动力学。X-OP 把重定向做成 MPC 优化，跨形态共用、即插即用，且显式约束动力学可行性，配状态同步与 SLAM 反馈在真机更稳。

**Q：为什么要「每个 MPC 步重置仿真状态」？**
A：真机测量带噪、接触动力学敏感，若仿真态与真机态偏离，MPC 预测就失真。每步用 NLS/SQP 把仿真态对齐到当前真机态（含接触约束），让 MPC 的滚动预测始终基于真实当前态，从而鲁棒在线执行。

**Q：MPC 重定向器的代价由哪些项构成？**
A：目标跟踪（基座位姿对齐操作者）+ 接触点稳定 + 指数避碰 + 控制能量 + 终端收敛，整体在「贴合意图」与「动力学可行」间联合权衡。

---

## 🔗 相关阅读

- [CLOT: Closed-Loop Global Motion Tracking for Whole-Body Humanoid Teleoperation](../CLOT__Closed-Loop_Global_Motion_Tracking_for_Whole-Body_Humanoid_Teleoperation/CLOT__Closed-Loop_Global_Motion_Tracking_for_Whole-Body_Humanoid_Teleoperation.md) — 同为闭环全身遥操作，可对比跟踪与重定向思路
- [TeleGate: Whole-Body Humanoid Teleoperation via Gated Expert Selection](../TeleGate__Whole-Body_Humanoid_Teleoperation_via_Gated_Expert_Selection_with_Motion_Prior/TeleGate__Whole-Body_Humanoid_Teleoperation_via_Gated_Expert_Selection_with_Motion_Prior.md) — 用门控专家而非 MPC 重定向的另一条路线
- [SEW-Mimic: Closed-Form Geometric Retargeting Solver](../SEW-Mimic__Closed-Form_Geometric_Retargeting_Solver_for_Upper_Body_Humanoid_Teleoperation/SEW-Mimic__Closed-Form_Geometric_Retargeting_Solver_for_Upper_Body_Humanoid_Teleoperation.md) — 上肢闭式几何重定向，与本文优化式重定向对照
- [CLONE: Closed-Loop Whole-Body Humanoid Teleoperation for Long-Horizon Tasks (2506.08931)](https://arxiv.org/abs/2506.08931) — 同用 AVP 头+双腕信号的长时遥操作
- [X-OP arXiv 2606.07934](https://arxiv.org/abs/2606.07934)

---

> 备注：本笔记基于 arXiv 摘要、[arXiv HTML 正文](https://arxiv.org/html/2606.07934)与公开搜索结果整理；公式记号与详细数值以 arXiv [2606.07934](https://arxiv.org/abs/2606.07934) 论文正文为准。
