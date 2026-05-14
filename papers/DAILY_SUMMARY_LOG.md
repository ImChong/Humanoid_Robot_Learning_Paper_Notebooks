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
| 2026-05-14 | 40 | [ZEST: Zero-shot Embodied Skill Transfer for Athletic Robot Control](04_Loco-Manipulation_and_WBC/ZEST__Zero-shot_Embodied_Skill_Transfer_for_Athletic_Robot_Control/ZEST__Zero-shot_Embodied_Skill_Transfer_for_Athletic_Robot_Control.md) | Loco-Manipulation / WBC | 截至论文发布暂未公开 |

> 备注：2026-04-25 当天首次推进时发现索引 15 (Ψ₀) 已有完整内容，依规则跳到索引 16 (SteadyTray) 完成补写，故同日产生两条记录。
> 备注：2026-04-26 推进索引 17 (ZeroWBC)，arXiv 与项目主页临时不可访问，笔记基于 awesome-humanoid-robot-learning 列表与项目主页公开文字描述整理；后续待 PDF / 官方仓库释出后补充实验数值。
> 备注：2026-05-09 推进索引 38 (HumanX)，arXiv / HuggingFace / 项目主页临时不可访问，笔记基于公开搜索结果与作者前作 (PhysHOI / SkillMimic) 整理；后续待 PDF / 官方仓库释出后补充实验细节与消融数值。
> 备注：2026-05-14 起改为按模块轮转（04_WBC → 05_Locomotion → 06_Manipulation → ... → 14_Human_Motion → 回到 04），每天选当前轮转模块下索引最小的未完成论文。

---

## ⏭️ 下一篇候选（供参考）

按"模块轮转"规则，下一篇应选 **05_Locomotion** 模块里索引最小的未完成论文：

| 索引 | 论文 | 模块 | 状态 |
|:---:|------|------|------|
| 39 | TTT-Parkour: Rapid Test-Time Training for Perceptive Robot Parkour | 04_WBC | ✅ 已完成 |
| 40 | ZEST: Zero-shot Embodied Skill Transfer for Athletic Robot Control | 04_WBC | ✅ 已完成 |
| ? | （明日：05_Locomotion 模块首个未完成论文） | 05_Locomotion | ⏭️ 下一篇候选 |

> 实际推进时会按当天轮转到的模块在 `papers` 列表中扫描，跳过已有内容的笔记。
