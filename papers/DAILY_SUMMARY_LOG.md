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

> 备注：2026-04-25 当天首次推进时发现索引 15 (Ψ₀) 已有完整内容，依规则跳到索引 16 (SteadyTray) 完成补写，故同日产生两条记录。

---

## ⏭️ 下一篇候选（供参考）

按 `progress.json` → `papers` 顺序：

| 索引 | 论文 | 状态 |
|:---:|------|------|
| 17 | ZeroWBC: Learning Natural Visuomotor Humanoid Control from Egocentric Video | ⏳ 待写 |
| 18 | Embedding Classical Balance Control Principles in RL for Humanoid Recovery | ⏳ 待写 |
| 19 | ULTRA: Unified Multimodal Control for Autonomous Humanoid Whole-Body Loco-Manipulation | ✅ 已有内容（应跳过） |
| 20 | OmniXtreme: Breaking the Generality Barrier in High-Dynamic Humanoid Control | ✅ 已有内容（应跳过） |

> 实际推进时会再次检查对应 folder 是否已存在内容，避免重复劳动。
