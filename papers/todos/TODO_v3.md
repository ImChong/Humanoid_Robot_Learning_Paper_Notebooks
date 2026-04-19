# 项目待办计划 v3：Humanoid Robot Learning Paper Notebooks

> **版本**：v3（继承自 `TODO_v2.md`；v2 计划于 2026-04-19 部分执行）
> **上一版定位**：从 5 个新分类的"骨架先覆盖"扩到 4 个剩余空分类、并把工具链补齐。
> **本版定位**：把所有 13 个分类全部脱"空"——剩余的事情是**人工读原文 + 把 🚧 字段替换成真实信息**。AI 能做的"机械性铺路"已基本完成。

---

## Context（背景）

v2 执行后，13 个分类目录全部至少有 1 篇 `.md`，没有任何"空目录"。本轮把 09 / 11 / 12 / 13 这 4 个剩余空分类各补了 1 篇 🚧 骨架，并升级 `prepare_pages.py` 的 `check_stub()`：除原有"行数 + 缺方法详解"双条件外，加入"🚧 标记数 ≥ 5"作为骨架判定，避免新骨架因为含有 `## 🔧 方法详解` 标题就被放行。

下一阶段的核心矛盾：**所有空分类都已起步，剩下的任务必须靠人工读论文**。AI 能做的"补孔"工作 v3 之后边际收益会迅速下降。

---

## 当前快照（2026-04-19，v2 执行后）

- 笔记总数：`papers/` 下 **29** 篇 `.md`（`update_badges.py` 口径）。
  - `01_Foundational_RL/`：13 篇（其中 PULSE / Diffusion_Policy / BeyondMimic 仍是骨架）
  - `02_High_Impact_Selection/`：1 篇
  - `03_Loco-Manipulation_and_WBC/`：5 篇（其中 HERO / VIGOR 仍是短 stub）
  - `04_Locomotion/`：1 篇（仍是骨架）
  - `05_Manipulation/`：1 篇（v2 骨架，🚧 待核对）
  - `06_Teleoperation/`：1 篇（v2 骨架，🚧 待核对）
  - `07_Navigation/`：1 篇（v2 骨架，🚧 待核对）
  - `08_State_Estimation/`：1 篇（v2 骨架，🚧 待核对）
  - `09_Sim-to-Real/`：**1 篇（v3 新骨架：RMA，🚧 待核对）**
  - `10_Simulation_Benchmark/`：1 篇（v2 骨架，🚧 待核对）
  - `11_Hardware_Design/`：**1 篇（v3 新骨架：Unitree H1 Whitepaper，🚧 待核对）**
  - `12_Physics-Based_Animation/`：**1 篇（v3 新骨架：MotionVAE，🚧 待核对）**
  - `13_Human_Motion/`：**1 篇（v3 新骨架：HumanML3D，🚧 待核对）**
- **空分类数：0**（v3 首次实现）。
- `🚧` 骨架清单（**必须由人工补**）：
  - `01_Foundational_RL/PULSE_...`、`01_Foundational_RL/Diffusion_Policy`、`01_Foundational_RL/BeyondMimic`（v1 遗留）
  - `04_Locomotion/Learning_to_Walk_in_Minutes`（v1 遗留）
  - `05_Manipulation/EgoMimic_...`、`06_Teleoperation/HumanPlus_...`、`07_Navigation/NaVILA_...`、`08_State_Estimation/Contact-Aided_Invariant_EKF_...`、`10_Simulation_Benchmark/HumanoidBench`（v2 新建）
  - `09_Sim-to-Real/RMA_...`、`11_Hardware_Design/Unitree_H1_Whitepaper`、`12_Physics-Based_Animation/MotionVAE`、`13_Human_Motion/HumanML3D`（v3 新建）
- 短 stub（< 80 行、缺"方法详解"章节）：
  - `03_Loco-Manipulation_and_WBC/Learning_Humanoid_End-Effector_Control_...`（HERO，57 行）
  - `03_Loco-Manipulation_and_WBC/VIGOR_...`（58 行）
- 徽章：Papers=530，Notes=29。
- `_data/papers.json`：28 papers in 13 categories（一个分类的 papers.json 计数与 `update_badges.py` 不同源，已记录到 R5）。

---

## 🧾 v2 TODO 核对（✅ 完成 / [ ] 未完成）

### v2 R1 / R2 / R3：人工任务

- [ ] **R1（4 条骨架深度填充）** —— **未完成**。AI 不能独立写。
- [ ] **R2（HERO / VIGOR 扩写）** —— **未完成**。同上。
- [ ] **R3（5 个 v2 新骨架人工核对 arXiv/作者）** —— **未完成**。

### v2 R4：剩余空分类起步

- [x] **R4 #12** `09_Sim-to-Real/` 首篇骨架 —— RMA（候选 2107.04034）。
- [x] **R4 #13** `11_Hardware_Design/` 首篇骨架 —— Unitree H1 Whitepaper。
- [x] **R4 #14** `12_Physics-Based_Animation/` 首篇骨架 —— MotionVAE（候选 2103.14274）。
- [x] **R4 #15** `13_Human_Motion/` 首篇骨架 —— HumanML3D（候选 2204.09419）。

### v2 R5：progress.json 边界

- [ ] **R5 #16** progress.json 跟踪边界决策 —— **未做**，需人工决策。
- [ ] **R5 #17** 8 个 on-disk-not-in-json 条目同步 —— **未做**，依赖 #16 决策。

### v2 R6：工具与站点一致性

- [x] **R6 #18** 升级 `check_stub()`：加入 🚧 数 ≥ 5 触发条件。验证：13 个新老骨架全部被 STUB 命中。
- [ ] **R6 #19** 本地 `bundle exec jekyll serve` 真机渲染 —— **未做**，需要本地环境。
- [x] **R6 #20** 重新跑 `update_badges.py`：Papers=530, Notes=29。

### v2 R7：README 收尾

- [ ] **R7 #21** README 徽章风格确认 —— **未做**，等设计意图明确。

---

## 🔭 v3 本轮目标（R1 – R5）

### R1 · 消灭 🚧（⚠️ 必须人工读原文）

| # | 任务 | 验收标准 | 负责人 |
|---|------|---------|--------|
| 1 | v1 / v2 / v3 累计 13 个 🚧 骨架，**逐篇核对 arXiv / 作者 / 机构 / 日期**，把 🚧 字段替换为真实链接 | 每篇 🚧 数 ≤ 3（只保留真正待补的技术细节） | 人工 |
| 2 | 在 1 完成的基础上挑 3–5 篇做深度填充（≥ 300 行 + 方法详解 + 实例） | `prepare_pages.py` 不再把它们标 STUB | 人工 |

### R2 · 旧 stub 扩写（v2 R2 顺延）

| # | 任务 | 验收标准 | 负责人 |
|---|------|---------|--------|
| 3 | `HERO`（57 行）扩写至 ≥ 300 行 | `[STUB]` 告警消失 | 人工 |
| 4 | `VIGOR`（58 行）扩写至 ≥ 300 行 | `[STUB]` 告警消失 | 人工 |

### R3 · progress.json 边界决策（v2 R5 顺延）

| # | 任务 | 验收标准 | 负责人 |
|---|------|---------|--------|
| 5 | 决定 `progress.json` 是否覆盖所有 `papers/**/*.md` | 写进 README 一段说明 | 人工决策 |
| 6 | 同步执行 #5 的决议：补 / 剔条目 | `progress.json` 与 `papers/` 一致 | AI 可执行 |

### R4 · 站点一致性（v2 R6 顺延）

| # | 任务 | 验收标准 | 负责人 |
|---|------|---------|--------|
| 7 | 本地 `bundle exec jekyll serve` 真机渲染一次 | 13 个分类全部出现在站点首页 | 人工 + AI |
| 8 | `_data/papers.json` 计数（28）与 `update_badges.py`（29）不一致原因排查 | 两者对齐 | AI |

### R5 · 第二轮分类铺开（可选，AI 可执行）

| # | 任务 | 验收标准 | 负责人 |
|---|------|---------|--------|
| 9 | `02_High_Impact_Selection/` 现仅 1 篇，按 progress.json 路线再补 2–3 篇骨架 | ≥ 3 篇 | AI |
| 10 | `04_Locomotion/` 现仅 1 篇，再补 2 篇骨架（如 ANYmal Parkour、Extreme Parkour） | ≥ 3 篇 | AI |

---

## 🧯 风险与边界（继承 v1 / v2，强化）

1. **AI 不写深度内容**：13 个 🚧 骨架的填充必须人工或"AI + 人工逐句校对"，否则会臆造公式 / 作者 / 源码路径。
2. **v3 之后 AI 能做的事很少**：13 个分类全部脱空，剩下 95% 的工作都属于"读原文 + 写笔记"，AI 唯一能继续做的只有 R5 的二轮铺开。
3. **🚧 字段是债务记号**：上线 > 1 周仍未核对的 🚧 应视为坏信号。
4. **不拆 PROGRESS.md**：当前 670 行 < 2000 行阈值。

---

## 📎 历史快照归档

- **v1 快照**（2026-04-18 前）：19 篇 / 12 完稿 / 4 骨架 + 2 短 stub / 9 空分类。
- **v2 快照**（2026-04-18 后）：25 篇 / 12 完稿 / 9 骨架 + 2 短 stub / 4 空分类。
- **v3 快照**（2026-04-19 后）：29 篇 / 12 完稿 / 13 骨架 + 2 短 stub / **0 空分类**。
- **v3 目标**：≥ 35 篇 / 18 完稿 / ≤ 5 骨架 / 0 短 stub / 0 空分类。
