# 🗓️ 每日论文总结日志

> 这是 **Claude 每日论文总结任务** 的执行记录。
>
> - **规则**：从用户的当前阅读位置（`progress.json` 的 `current_paper_index`）开始，按 `papers` 列表顺序推进；如果该索引的笔记已有内容，则跳到下一篇。
> - **节奏**：每天一篇，与用户自己的阅读进度错开。
> - **产出**：Markdown 笔记（含 PDF / HTML / 项目主页 / 源码链接）+ `progress.json` / `PROGRESS.md` / `_data/papers.json` 同步更新。
> - **状态字段**：同步写入 `progress.json` → `daily_summary` 字段，便于下次接续。

---

## 📅 日志表

| 日期 | 论文索引 | 笔记 | 分类 | 源码 |
|------|:---:|------|------|------|
| 2026-04-24 | 14 | [LATENT: Learning Athletic Humanoid Tennis Skills](04_Loco-Manipulation_and_WBC/LATENT__Learning_Athletic_Humanoid_Tennis_Skills_from_Imperfect_Human_Motion_Dat/LATENT__Learning_Athletic_Humanoid_Tennis_Skills_from_Imperfect_Human_Motion_Dat.md) | Loco-Manipulation / WBC | [GalaxyGeneralRobotics/LATENT](https://github.com/GalaxyGeneralRobotics/LATENT) |
| 2026-04-25 | 15 | [Ψ₀: An Open Foundation Model Towards Universal Humanoid Loco-Manipulation](04_Loco-Manipulation_and_WBC/Ψ₀__An_Open_Foundation_Model_Towards_Universal_Humanoid_Loco-Manipulation/Ψ₀__An_Open_Foundation_Model_Towards_Universal_Humanoid_Loco-Manipulation.md) | Loco-Manipulation / WBC | [physical-superintelligence-lab/Psi0](https://github.com/physical-superintelligence-lab/Psi0) |
| 2026-04-25 | 16 | [SteadyTray: Learning Object Balancing Tasks via Residual RL](04_Loco-Manipulation_and_WBC/SteadyTray__Learning_Object_Balancing_Tasks_in_Humanoid_Tray_Transport_via_Resid/SteadyTray__Learning_Object_Balancing_Tasks_in_Humanoid_Tray_Transport_via_Resid.md) | Loco-Manipulation / WBC | [AllenHuangGit/steadytray](https://github.com/AllenHuangGit/steadytray) |
| 2026-04-26 | 17 | [ZeroWBC: Learning Natural Visuomotor Humanoid Control from Egocentric Video](04_Loco-Manipulation_and_WBC/ZeroWBC__Learning_Natural_Visuomotor_Humanoid_Control_from_Egocentric_Video/ZeroWBC__Learning_Natural_Visuomotor_Humanoid_Control_from_Egocentric_Video.md) | Loco-Manipulation / WBC | 待官方释出（[zerowbc.github.io](https://zerowbc.github.io/)） |
| 2026-04-28 | 18 | [Embedding Classical Balance Control Principles in RL for Humanoid Recovery](04_Loco-Manipulation_and_WBC/Embedding_Classical_Balance_Control_Principles_in_RL_for_Humanoid_Recovery/Embedding_Classical_Balance_Control_Principles_in_RL_for_Humanoid_Recovery.md) | Loco-Manipulation / WBC | 待官方释出 |
| 2026-04-29 | 25 | [MeshMimic: Geometry-Aware Humanoid Motion Learning through 3D Scene Reconstruction](04_Loco-Manipulation_and_WBC/MeshMimic__Geometry-Aware_Humanoid_Motion_Learning_through_3D_Scene_Reconstructi/MeshMimic__Geometry-Aware_Humanoid_Motion_Learning_through_3D_Scene_Reconstructi.md) | Loco-Manipulation / WBC | 待官方释出（[meshmimic.github.io](https://meshmimic.github.io/)） |
| 2026-04-29 | 26 | [General Humanoid Whole-Body Control via Pretraining and Fast Adaptation](04_Loco-Manipulation_and_WBC/General_Humanoid_Whole-Body_Control_via_Pretraining_and_Fast_Adaptation/General_Humanoid_Whole-Body_Control_via_Pretraining_and_Fast_Adaptation.md) | Loco-Manipulation / WBC | [BeingBeyond/FAST](https://github.com/BeingBeyond/FAST) |
| 2026-04-29 | 27 | [HAIC: Humanoid Agile Object Interaction Control via Dynamics-Aware World Model](04_Loco-Manipulation_and_WBC/HAIC__Humanoid_Agile_Object_Interaction_Control_via_Dynamics-Aware_World_Model/HAIC__Humanoid_Agile_Object_Interaction_Control_via_Dynamics-Aware_World_Model.md) | Loco-Manipulation / WBC | 待官方释出（[haic-humanoid.github.io](https://haic-humanoid.github.io/)） |
| 2026-04-29 | 28 | [EgoHumanoid: Unlocking In-the-Wild Loco-Manipulation with Robot-Free Egocentric Demonstration](04_Loco-Manipulation_and_WBC/EgoHumanoid__Unlocking_In-the-Wild_Loco-Manipulation_with_Robot-Free_Egocentric_/EgoHumanoid__Unlocking_In-the-Wild_Loco-Manipulation_with_Robot-Free_Egocentric_.md) | Loco-Manipulation / WBC | [OpenDriveLab/EgoHumanoid](https://github.com/OpenDriveLab/EgoHumanoid) |
| 2026-05-01 | 29 | [MOSAIC: Bridging the Sim-to-Real Gap in Generalist Humanoid Motion Tracking and Teleoperation with Rapid Residual Adaptation](04_Loco-Manipulation_and_WBC/MOSAIC__Bridging_the_Sim-to-Real_Gap_in_Generalist_Humanoid_Motion_Tracking_and_/MOSAIC__Bridging_the_Sim-to-Real_Gap_in_Generalist_Humanoid_Motion_Tracking_and_.md) | Loco-Manipulation / WBC | [BAAI-Humanoid/MOSAIC](https://github.com/BAAI-Humanoid/MOSAIC) |
| 2026-05-02 | 30 | [Learning Human-Like Badminton Skills for Humanoid Robots](04_Loco-Manipulation_and_WBC/Learning_Human-Like_Badminton_Skills_for_Humanoid_Robots/Learning_Human-Like_Badminton_Skills_for_Humanoid_Robots.md) | Loco-Manipulation / WBC | 待官方释出（[astrorix.github.io/LHBS](https://astrorix.github.io/LHBS/)） |
| 2026-05-03 | 31 | [TextOp: Real-time Interactive Text-Driven Humanoid Robot Motion Generation and Control](04_Loco-Manipulation_and_WBC/TextOp__Real-time_Interactive_Text-Driven_Humanoid_Robot_Motion_Generation_and_C/TextOp__Real-time_Interactive_Text-Driven_Humanoid_Robot_Motion_Generation_and_C.md) | Loco-Manipulation / WBC | [TeleHuman/TextOp](https://github.com/TeleHuman/TextOp) |
| 2026-05-06 | 35 | [PDF-HR: Pose Distance Fields for Humanoid Robots](04_Loco-Manipulation_and_WBC/PDF-HR__Pose_Distance_Fields_for_Humanoid_Robots/PDF-HR__Pose_Distance_Fields_for_Humanoid_Robots.md) | Loco-Manipulation / WBC | 待官方释出（论文声明 "code and models will be released"） |
| 2026-05-07 | 36 | [HUSKY: Humanoid Skateboarding System via Physics-Aware Whole-Body Control](04_Loco-Manipulation_and_WBC/HUSKY__Humanoid_Skateboarding_System_via_Physics-Aware_Whole-Body_Control/HUSKY__Humanoid_Skateboarding_System_via_Physics-Aware_Whole-Body_Control.md) | Loco-Manipulation / WBC | [TeleHuman/humanoid_skateboarding](https://github.com/TeleHuman/humanoid_skateboarding) |
| 2026-05-08 | 37 | [Embodiment-Aware Generalist Specialist Distillation for Unified Humanoid Whole-Body Control](04_Loco-Manipulation_and_WBC/Embodiment-Aware_Generalist_Specialist_Distillation_for_Unified_Humanoid_Whole-B/Embodiment-Aware_Generalist_Specialist_Distillation_for_Unified_Humanoid_Whole-B.md) | Loco-Manipulation / WBC | 截至论文发布暂未公开 |
| 2026-05-09 | 38 | [HumanX: Toward Agile and Generalizable Humanoid Interaction Skills from Human Videos](04_Loco-Manipulation_and_WBC/HumanX__Toward_Agile_and_Generalizable_Humanoid_Interaction_Skills_from_Human_Vi/HumanX__Toward_Agile_and_Generalizable_Humanoid_Interaction_Skills_from_Human_Vi.md) | Loco-Manipulation / WBC | 待官方释出（[wyhuai.github.io/human-x](https://wyhuai.github.io/human-x/)） |
| 2026-05-13 | 39 | [TTT-Parkour: Rapid Test-Time Training for Perceptive Robot Parkour](04_Loco-Manipulation_and_WBC/TTT-Parkour__Rapid_Test-Time_Training_for_Perceptive_Robot_Parkour/TTT-Parkour__Rapid_Test-Time_Training_for_Perceptive_Robot_Parkour.md) | Loco-Manipulation / WBC | 待官方释出（[ttt-parkour.github.io](https://ttt-parkour.github.io/)） |
| 2026-05-14 | H2 | [HOVER: Versatile Neural Whole-Body Controller for Humanoid Robots](03_High_Impact_Selection/HOVER_Versatile_Neural_Whole-Body_Controller/HOVER_Versatile_Neural_Whole-Body_Controller.md) | 高影响力精选 / 全身控制核心 | [NVlabs/HOVER](https://github.com/NVlabs/HOVER) |
| 2026-05-14 | 40 | [ZEST: Zero-shot Embodied Skill Transfer for Athletic Robot Control](04_Loco-Manipulation_and_WBC/ZEST__Zero-shot_Embodied_Skill_Transfer_for_Athletic_Robot_Control/ZEST__Zero-shot_Embodied_Skill_Transfer_for_Athletic_Robot_Control.md) | Loco-Manipulation / WBC | 截至论文发布暂未公开 |
| 2026-05-15 | H9 | [HOMIE: Humanoid Loco-Manipulation with Isomorphic Exoskeleton Cockpit](03_High_Impact_Selection/HOMIE_Humanoid_Loco-Manipulation_with_Isomorphic_Exoskeleton_Cockpit/HOMIE_Humanoid_Loco-Manipulation_with_Isomorphic_Exoskeleton_Cockpit.md) | 高影响力精选 / 遥操作与模仿学习 | [InternRobotics/OpenHomie](https://github.com/InternRobotics/OpenHomie) |
| 2026-05-15 | 187 | [Biomechanical Comparisons Reveal Divergence of Human and Humanoid Gaits](05_Locomotion/Biomechanical_Comparisons_Reveal_Divergence_of_Human_and_Humanoid_Gaits/Biomechanical_Comparisons_Reveal_Divergence_of_Human_and_Humanoid_Gaits.md) | Locomotion / 生物力学评估 | 含 MuJoCo 可视化与 GDAF Notebook，随论文释出 |
| 2026-05-16 | H23 | [BEHAVIOR Robot Suite: Streamlining Real-World Whole-Body Manipulation for Everyday Household Activities](03_High_Impact_Selection/BEHAVIOR_Robot_Suite_Streamlining_Real-World_Whole-Body_Manipulation/BEHAVIOR_Robot_Suite_Streamlining_Real-World_Whole-Body_Manipulation.md) | 高影响力精选 / 仿真平台与工具 | [behavior-robot-suite/brs-algo](https://github.com/behavior-robot-suite/brs-algo) · [brs-ctrl](https://github.com/behavior-robot-suite/brs-ctrl) |
| 2026-05-16 | 271 | [HumDex: Humanoid Dexterous Manipulation Made Easy](06_Manipulation/HumDex_Humanoid_Dexterous_Manipulation_Made_Easy/HumDex_Humanoid_Dexterous_Manipulation_Made_Easy.md) | Manipulation / 遥操作 / 灵巧手 | [physical-superintelligence-lab/HumDex](https://github.com/physical-superintelligence-lab/HumDex) |
| 2026-05-17 | 329 | [CLOT: Closed-Loop Global Motion Tracking for Whole-Body Humanoid Teleoperation](07_Teleoperation/CLOT__Closed-Loop_Global_Motion_Tracking_for_Whole-Body_Humanoid_Teleoperation/CLOT__Closed-Loop_Global_Motion_Tracking_for_Whole-Body_Humanoid_Teleoperation.md) | Teleoperation / 全身控制 / 动作跟踪 | [zhutengjie/CLOT](https://github.com/zhutengjie/CLOT) |
| 2026-05-18 | 350 | [EgoActor: Grounding Task Planning into Spatial-aware Egocentric Actions for Humanoid Robots via Visual-Language Models](08_Navigation/EgoActor__Grounding_Task_Planning_into_Spatial-aware_Egocentric_Actions_for_Hum/EgoActor__Grounding_Task_Planning_into_Spatial-aware_Egocentric_Actions_for_Hum.md) | Navigation / VLM / 任务规划 / 第一视角 | 待官方释出（[baai-agents.github.io/EgoActor](https://baai-agents.github.io/EgoActor/)） |
| 2026-05-19 | 368 | [AutoOdom: Learning Auto-regressive Proprioceptive Odometry for Legged Locomotion](09_State_Estimation/AutoOdom__Learning_Auto-regressive_Proprioceptive_Odometry_for_Legged_Locomotio/AutoOdom__Learning_Auto-regressive_Proprioceptive_Odometry_for_Legged_Locomotio.md) | State Estimation / 本体感知里程计 / Sim-to-Real | 截至当前未见公开发布 |
| 2026-05-17 | H4 | [HugWBC: A Unified and General Humanoid Whole-Body Controller for Versatile Locomotion](03_High_Impact_Selection/HugWBC_A_Unified_and_General_Humanoid_Whole-Body_Controller/HugWBC_A_Unified_and_General_Humanoid_Whole-Body_Controller.md) | 高影响力精选 / 全身控制核心 | [apexrl/HugWBC](https://github.com/apexrl/HugWBC) · [InternRobotics/HugWBC](https://github.com/InternRobotics/HugWBC) |
| 2026-05-18 | H11 | [iDP3: Generalizable Humanoid Manipulation with Improved 3D Diffusion Policies](03_High_Impact_Selection/iDP3_Generalizable_Humanoid_Manipulation_with_3D_Diffusion_Policies/iDP3_Generalizable_Humanoid_Manipulation_with_3D_Diffusion_Policies.md) | 高影响力精选 / 遥操作与模仿学习 | [YanjieZe/Improved-3D-Diffusion-Policy](https://github.com/YanjieZe/Improved-3D-Diffusion-Policy) · [humanoid_teleoperation](https://github.com/YanjieZe/humanoid_teleoperation) |
| 2026-05-20 | H5 | [SONIC: Supersizing Motion Tracking for Natural Humanoid Whole-Body Control](03_High_Impact_Selection/SONIC_Supersizing_Motion_Tracking_for_Natural_Humanoid_Control/SONIC_Supersizing_Motion_Tracking_for_Natural_Humanoid_Control.md) | 高影响力精选 / 全身控制核心 | 截至当前未公开训练代码，主要参考 [项目主页](https://nvlabs.github.io/SONIC/) 与 [GR00T-WholeBodyControl 文档](https://nvlabs.github.io/GR00T-WholeBodyControl/) |
| 2026-05-21 | H6 | [UH-1: Learning from Massive Human Videos for Universal Humanoid Pose Control](03_High_Impact_Selection/UH-1_Learning_from_Massive_Human_Videos_for_Universal_Humanoid_Pose_Control/UH-1_Learning_from_Massive_Human_Videos_for_Universal_Humanoid_Pose_Control.md) | 高影响力精选 / 全身控制核心 | [sihengz02/UH-1](https://github.com/sihengz02/UH-1) · [HuggingFace USC-PSI-Lab/UH-1](https://huggingface.co/USC-PSI-Lab/UH-1) |

> 备注：2026-04-25 当天首次推进时发现索引 15 (Ψ₀) 已有完整内容，依规则跳到索引 16 (SteadyTray) 完成补写，故同日产生两条记录。
> 备注：2026-04-26 推进索引 17 (ZeroWBC)，arXiv 与项目主页临时不可访问，笔记基于 awesome-humanoid-robot-learning 列表与项目主页公开文字描述整理；后续待 PDF / 官方仓库释出后补充实验数值。
> 备注：2026-05-09 推进索引 38 (HumanX)，arXiv / HuggingFace / 项目主页临时不可访问，笔记基于公开搜索结果与作者前作 (PhysHOI / SkillMimic) 整理；后续待 PDF / 官方仓库释出后补充实验细节与消融数值。
> 备注：2026-05-14 起并行两条推进轨：
> - **轨 A · 高影响力精选轮转**：在「⭐ 高影响力精选」内按子类 round-robin 推进；2026-05-14 起首篇 H2 HOVER。
> - **轨 B · 模块轮转**：按 04_WBC → 05_Locomotion → 06_Manipulation → ... → 14_Human_Motion → 回到 04 顺序推进；当日推进了索引 40 ZEST。
> 两条轨各自维护状态，已有完整笔记的论文自动跳过；同一天可能各产出一篇。
> 备注（2026-05-22 更正）：轨 A 早期被误缩小为「**三分类**」（全身控制核心 / 遥操作与模仿学习 / 仿真平台与工具），把「Locomotion 经典 / Sim-to-Real & Foundation Model」当作另一路自动化的责任。用户原始任务要求「在高影响力精选模块内循环」，**应覆盖 03_High_Impact_Selection 全部 5 个子类**。自 2026-05-22 起，轨 A 循环为**五类**：全身控制核心 → 遥操作与模仿学习 → Locomotion 经典 → Sim-to-Real & Foundation Model → 仿真平台与工具 → 回到全身控制核心。`progress.json → daily_summary.high_impact_cycle.categories` 同步改为五类。

---

## ⏭️ 下一篇候选

> 当前并行两条推进轨，各自独立挑选；同一天可能各产出一篇。

### 🅰️ 轨 A · 高影响力精选轮转（五类，2026-05-22 起）

> **循环顺序**：全身控制核心 → 遥操作与模仿学习 → **Locomotion 经典** → **Sim-to-Real & Foundation Model** → 仿真平台与工具 → 全身控制核心 …
>
> **跳过原则**：当轮到的子类已全部覆盖时，按循环自动 round-robin 到下一类。
>
> ⚠️ 早期（2026-05-14 至 2026-05-21）该循环被误缩小为三类，将「Locomotion 经典 / Sim-to-Real & Foundation Model」当作另一路自动化的责任；现已更正为五类，与 `progress.json → daily_summary.high_impact_cycle.categories` 同步。

#### 1. 全身控制核心（H1–H6）
| 编号 | 论文 | 状态 |
|:---:|------|------|
| H1 | Expressive Whole-Body Control for Humanoid Robots | ✅ 已完成 |
| H2 | HOVER: Versatile Neural Whole-Body Controller for Humanoid Robots | ✅ 已完成（2026-05-14） |
| H3 | ExBody2: Advanced Expressive Humanoid Whole-Body Control | ✅ 已完成 |
| H4 | HugWBC: A Unified and General Humanoid Whole-Body Controller | ✅ 已完成（2026-05-17） |
| H5 | SONIC: Supersizing Motion Tracking | ✅ 已完成（2026-05-20） |
| H6 | UH-1: Learning from Massive Human Videos for Universal Humanoid Pose Control | ✅ 已完成（2026-05-21） |

> 子类小计：**6 / 6 ✅ 已全部完成**

#### 2. 遥操作与模仿学习（H7–H11）
| 编号 | 论文 | 状态 |
|:---:|------|------|
| H7 | HumanPlus | ✅ 已存在（笔记位于 07_Teleoperation） |
| H8 | OmniH2O | ✅ 已完成 |
| H9 | HOMIE | ✅ 已完成（2026-05-15） |
| H10 | EgoMimic | ✅ 已存在（笔记位于 06_Manipulation） |
| H11 | Generalizable Humanoid Manipulation with Improved 3D Diffusion Policies | ✅ 已完成（2026-05-18） |

> 子类小计：**5 / 5 ✅ 已全部完成**

#### 3. Locomotion 经典（H12–H16）
| 编号 | 论文 | arXiv | 状态 |
|:---:|------|:---:|------|
| H12 | Real-World Humanoid Locomotion with Reinforcement Learning | [2303.03381](https://arxiv.org/abs/2303.03381) | ✅ 已完成（见 03 高影响力精选目录内笔记） |
| H13 | Humanoid Locomotion as Next Token Prediction | [2402.19469](https://arxiv.org/abs/2402.19469) | ⏳ 待写（**下一篇候选**） |
| H14 | Humanoid Parkour Learning | [2406.10759](https://arxiv.org/abs/2406.10759) | ⏳ 待写 |
| H15 | Learning Sim-to-Real Humanoid Locomotion in 15 Minutes | [2512.01996](https://arxiv.org/abs/2512.01996) | ⏳ 待写 |
| H16 | ECO: Energy-Constrained Optimization with RL for Humanoid Walking | [2602.06445](https://arxiv.org/abs/2602.06445) | ⏳ 待写 |

> 子类小计：**1 / 5**（缺 H13 / H14 / H15 / H16）

#### 4. Sim-to-Real & Foundation Model（H17–H20）
| 编号 | 论文 | arXiv / 链接 | 状态 |
|:---:|------|:---:|------|
| H17 | Learning Agile and Dynamic Motor Skills for Legged Robots（ANYmal） | [1901.08652](https://arxiv.org/abs/1901.08652) | ✅ 已完成 |
| H18 | ASAP: Aligning Simulation and Real-World Physics for Agile Humanoid Skills | [agile.human2humanoid.com](https://agile.human2humanoid.com/) | ⏳ 待写 |
| H19 | GR00T N1: An Open Foundation Model for Generalist Humanoid Robots | [2503.14734](https://arxiv.org/abs/2503.14734) | ✅ 已存在（97 行基础笔记，深度细节可后续补充） |
| H20 | Behavior Foundation Model for Humanoid Robots | [2509.13780](https://arxiv.org/abs/2509.13780) | ⏳ 待写 |

> 子类小计：**2 / 4**（缺 H18 / H20）

#### 5. 仿真平台与工具（H21–H23）
| 编号 | 论文 | 状态 |
|:---:|------|------|
| H21 | Humanoid-Gym | ✅ 已完成（见 03 高影响力精选目录内笔记） |
| H22 | HumanoidBench | ✅ 已存在（笔记位于 11_Simulation_Benchmark） |
| H23 | BEHAVIOR Robot Suite | ✅ 已完成（2026-05-16） |

> 子类小计：**3 / 3 ✅ 已全部完成**

---

#### 五类总览与下次推进

整体进度：**17 / 23**（剩 6 篇，全部集中在「Locomotion 经典」与「Sim-to-Real & Foundation Model」两类）。

剩余写作顺序（按五类循环、跳过已全覆盖子类得到）：

1. 2026-05-22 → **H13 Humanoid Locomotion as Next Token Prediction**（Locomotion 经典）
2. 2026-05-23 → H18 ASAP（Sim-to-Real & FM）
3. 2026-05-24 → 仿真平台与工具（已全覆盖，跳过）→ H14 Humanoid Parkour Learning（Locomotion 经典）
4. 2026-05-25 → H20 Behavior Foundation Model（Sim-to-Real & FM）
5. 2026-05-26 → H15 Learning Sim-to-Real Humanoid Locomotion in 15 Minutes（Locomotion 经典）
6. 2026-05-27 → H16 ECO（Locomotion 经典）

写完 H16 后，「⭐ 高影响力精选」H1–H23 才真正全部完成，届时再提示用户补充新待读论文。

---

### 🅱️ 轨 B · 模块轮转

> 循环顺序：04_WBC → 05_Locomotion → 06_Manipulation → 07_Teleoperation → 08_Navigation → 09_State_Estimation → 10_Sim-to-Real → 11_Simulation_Benchmark → 12_Hardware_Design → 13_Physics-Based_Animation → 14_Human_Motion → 回到 04
>
> 每天选当前轮转模块下索引最小的未完成论文；已有内容的笔记自动跳过。

| 索引 | 论文 | 模块 | 状态 |
|:---:|------|------|------|
| 39 | TTT-Parkour: Rapid Test-Time Training for Perceptive Robot Parkour | 04_WBC | ✅ 已完成（2026-05-13） |
| 40 | ZEST: Zero-shot Embodied Skill Transfer for Athletic Robot Control | 04_WBC | ✅ 已完成（2026-05-14） |
| 187 | Biomechanical Comparisons Reveal Divergence of Human and Humanoid Gaits | 05_Locomotion | ✅ 已完成（2026-05-15） |
| 271 | HumDex: Humanoid Dexterous Manipulation Made Easy | 06_Manipulation | ✅ 已完成（2026-05-16） |
| 329 | CLOT: Closed-Loop Global Motion Tracking for Whole-Body Humanoid Teleoperation | 07_Teleoperation | ✅ 已完成（2026-05-17） |
| 350 | EgoActor: Grounding Task Planning into Spatial-aware Egocentric Actions for Humanoid Robots via Visual-Language Models | 08_Navigation | ✅ 已完成（2026-05-18） |
| 368 | AutoOdom: Learning Auto-regressive Proprioceptive Odometry for Legged Locomotion | 09_State_Estimation | ✅ 已完成（2026-05-19） |
| ? | （明日：10_Sim-to-Real 模块首个未完成论文） | 10_Sim-to-Real | ⏭️ 下一篇候选 |

> 实际推进时会按当天轮转到的模块在 `papers` 列表中扫描，跳过已有内容的笔记。
