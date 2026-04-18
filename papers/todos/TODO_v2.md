# 项目待办计划 v2：Humanoid Robot Learning Paper Notebooks

> **版本**：v2（继承自 `TODO_v1.md`；v1 计划于 2026-04-18 本轮执行）
> **上一版定位**：把 `papers/` 主干从"骨架蔓生"收敛到"路线图可读"。
> **本版定位**：把 5 个新分类首篇骨架、4 个 🚧 路线图骨架，从"🚧 待核对"升级到"人工已核对"，并逐步扩写为完稿。

## Context（背景）

基于 v1 的执行，项目目前已经：
- 把 `TODO.md` 按版本归档到 `papers/todos/TODO_v*.md` 子目录。
- 打通 `update_badges.py` / `prepare_pages.py` 对 `papers/todos/` 目录的过滤，搬迁不破坏徽章和站点数据生成。
- 为 5 个原本完全为空的分类（Manipulation / Teleoperation / Navigation / State Estimation / Simulation Benchmark）各起了 1 篇 `🚧 待核对` 骨架。
- 同步了 `progress.json` 陈旧的 `current_paper_index`。

下一阶段要把"骨架先覆盖"转为"深度填满"。**R1 / R2 的深度内容必须靠人工读原文填写**，AI 独立完成会臆造公式/源码路径，这一条从 v1 延续，v2 依然严格遵守。

## 当前快照（2026-04-18，v1 执行后）

- PR #1 已合并；v1 TODO 归档到 `papers/todos/TODO_v1.md`。
- 笔记总数：`papers/` 下 **25** 篇 `.md`（`update_badges.py` 口径）。
  - `01_Foundational_RL/`：13 篇（其中 PULSE、Diffusion_Policy、BeyondMimic 仍是骨架）
  - `02_High_Impact_Selection/`：1 篇
  - `03_Loco-Manipulation_and_WBC/`：5 篇
  - `04_Locomotion/`：1 篇（仍是骨架）
  - `05_Manipulation/`：**1 篇（v2 新建骨架：EgoMimic，🚧 待核对）**
  - `06_Teleoperation/`：**1 篇（v2 新建骨架：HumanPlus，🚧 待核对）**
  - `07_Navigation/`：**1 篇（v2 新建骨架：NaVILA，🚧 待核对）**
  - `08_State_Estimation/`：**1 篇（v2 新建骨架：Contact-Aided InEKF，🚧 待核对）**
  - `10_Simulation_Benchmark/`：**1 篇（v2 新建骨架：HumanoidBench，🚧 待核对）**
- 仍完全为空的分类：`09_Sim-to-Real`、`11_Hardware_Design`、`12_Physics-Based_Animation`、`13_Human_Motion`（共 4 个）。
- `🚧` 骨架清单（本轮 **必须由人工补**）：
  - `01_Foundational_RL/PULSE_...`（111 行，v1 遗留）
  - `01_Foundational_RL/Diffusion_Policy`（119 行，v1 遗留）
  - `01_Foundational_RL/BeyondMimic`（103 行，v1 遗留）
  - `04_Locomotion/Learning_to_Walk_in_Minutes`（92 行，v1 遗留）
  - `05_Manipulation/EgoMimic_...`（v2 新建）
  - `06_Teleoperation/HumanPlus_...`（v2 新建）
  - `07_Navigation/NaVILA_...`（v2 新建）
  - `08_State_Estimation/Contact-Aided_Invariant_EKF_...`（v2 新建）
  - `10_Simulation_Benchmark/HumanoidBench`（v2 新建）
- 仍是短 stub（<80 行、缺"方法详解"章节）：
  - `03_Loco-Manipulation_and_WBC/Learning_Humanoid_End-Effector_Control_...`（HERO，57 行）
  - `03_Loco-Manipulation_and_WBC/VIGOR_...`（58 行）
- `progress.json`：total=175，done=9，pending=166，`current_paper_index=6`（已修正）。
- `PROGRESS.md`：523 篇（v1 期间从 490 扩到 523，覆盖 awesome-humanoid-robot-learning 新增条目）。

---

## 🧾 v1 TODO 核对（✅ 完成 / [ ] 未完成）

### v1 的"本轮执行目标" R1 ~ R6

- [ ] **R1 · 消灭骨架里的 🚧（4 条）** —— **未完成**。本轮只做了机械搬迁、没有触碰深度内容。PULSE / Diffusion Policy / BeyondMimic / Learning_to_Walk_in_Minutes 仍为骨架，v2 必须靠人工或逐篇 "AI 辅助 + 人工校对" 完成。
- [ ] **R2 · 旧 stub 收尾（2 条）** —— **未完成**。HERO、VIGOR 仍在 57–58 行。同上，需要人工读完原文再扩写。
- [x] **R3 · 空分类起步（5 条）** —— **已完成**。本轮为 5 个原本完全为空的分类各建了 1 篇 🚧 骨架（EgoMimic / HumanPlus / NaVILA / Contact-Aided InEKF / HumanoidBench）。**⚠️ 所有基本信息（arXiv/作者/机构/日期）均为推测，标 🚧 待人工核对**。
- [x] **R4#12 · 同步 progress.json**（部分完成）—— `current_paper_index` 从陈旧的 3 修正为 6。新增入口 8 条 / Domain_Randomization 升级 done 等设计决策未做，留到 R4a。
- [x] **R4#13 · 检查 [STUB] 告警** —— 已跑 `prepare_pages.py`，仅 2 个旧 stub 触发告警，新骨架因为有 `## 🔧 方法详解` 标题被放行（脚本弱点，记进 R6）。
- [ ] **R4#14 · Jekyll 本地渲染校验** —— 本轮未做，需要 `bundle exec jekyll serve` 实际启动。
- [x] **R5#15 · 徽章自动更新** —— `update_badges.py` 已更新 README：Papers=512, Notes=25。
- [ ] **R5#16 · 推新分支 / PR 部署** —— 直接合入 main，未走新分支流程（用户此前明确要求直接推 main）。
- [ ] **R6 长期可选（3 条）** —— 未做，留入 v2 的 R6。

### v1 交付物（实际 commit）

- [x] **搬迁**：`papers/TODO.md` → `papers/todos/TODO_v1.md`。
- [x] **脚本兼容**：`update_badges.py`、`prepare_pages.py` 跳过 `papers/todos/` 与 `TODO*.md`。
- [x] **R3 骨架**：5 篇新骨架落地。
- [x] **progress.json**：`current_paper_index` 修正。
- [x] **徽章同步**：README Papers=512、Notes=25。
- [x] **v2 TODO**：本文件。

---

## 🔭 v2 本轮目标（R1 – R7）

### R1 · 消灭 🚧（⚠️ 人工读原文，不建议 AI 独立写）

| # | 任务 | 验收标准 | 负责人 |
|---|------|---------|--------|
| 1 | `PULSE_Physics-based_Universal_Latent_Space` 深度填充 | ≥ 300 行，含方法公式、MimicKit 源码对照、🚧 数归零 | 人工 |
| 2 | `Diffusion_Policy` 深度填充 | 同上 | 人工 |
| 3 | `BeyondMimic` 深度填充 | 同上 | 人工 |
| 4 | `Learning_to_Walk_in_Minutes` 深度填充 | 同上，侧重 massively parallel sim 细节 | 人工 |

### R2 · 旧 stub 扩写

| # | 任务 | 验收标准 | 负责人 |
|---|------|---------|--------|
| 5 | `HERO`（Open-Vocabulary Visual Loco-Manipulation）扩写 | ≥ 300 行，`prepare_pages.py` 不再 `[STUB]` | 人工 |
| 6 | `VIGOR` 扩写 | ≥ 300 行，`prepare_pages.py` 不再 `[STUB]` | 人工 |

### R3 · v2 新骨架人工核对

| # | 任务 | 验收标准 | 负责人 |
|---|------|---------|--------|
| 7 | EgoMimic：核对 arXiv ID（候选 2410.24221）、作者、机构、日期 | 🚧 数 ≤ 3（只保留真正待补的技术细节） | 人工 |
| 8 | HumanPlus：核对 arXiv ID（候选 2406.10454）、作者、机构 | 同上 | 人工 |
| 9 | NaVILA：核对 arXiv ID（候选 2412.04453）、作者、机构 | 同上 | 人工 |
| 10 | Contact-Aided InEKF：核对具体论文版本（Hartley 2018 vs 2020 扩展）、作者清单 | 同上 | 人工 |
| 11 | HumanoidBench：核对 arXiv ID（候选 2403.10506）、作者、机构 | 同上 | 人工 |

### R4 · 剩余空分类起步（AI 可做）

| # | 任务 | 验收标准 | 负责人 |
|---|------|---------|--------|
| 12 | `09_Sim-to-Real/` 首篇骨架（建议 RMA / Learning Agile and Dynamic Motor Skills） | 1 篇 🚧 骨架 | AI + 人工校对 |
| 13 | `11_Hardware_Design/` 首篇骨架（建议 Atlas / Unitree H1 白皮书） | 同上 | AI + 人工校对 |
| 14 | `12_Physics-Based_Animation/` 首篇骨架（建议 NeuralNet / MotionVAE） | 同上 | AI + 人工校对 |
| 15 | `13_Human_Motion/` 首篇骨架（建议 HumanML3D / TRAM / WHAM） | 同上 | AI + 人工校对 |

### R5 · progress.json 设计决策（R4a 延期项）

| # | 任务 | 验收标准 | 负责人 |
|---|------|---------|--------|
| 16 | 决定 `progress.json` 的边界：是只跟踪"基础路线图"还是所有 `papers/**/*.md` | 写进 v2 README 的一段说明 | 人工决策 |
| 17 | 根据决定，补或剔 8 个 on-disk-not-in-json 的条目（Domain_Randomization / Expressive / HERO / LessMimic / OmniXtreme / ULTRA / VIGOR / Learning_to_Walk） | 实际执行一次同步 | AI 可执行 |

### R6 · 工具与站点一致性

| # | 任务 | 验收标准 | 负责人 |
|---|------|---------|--------|
| 18 | 升级 `check_stub()`：除了"有 `## 🔧`"之外，再看"🚧 字符数 / 总字符数" 比例 | 5 个新骨架应被判为 STUB | AI |
| 19 | 本地 `bundle exec jekyll serve` 真机渲染一次，确认 5 个新分类能出现在站点 | 截图 / 日志记录 | 人工 + AI |
| 20 | 重新跑一遍 `update_badges.py`，确认徽章与主页统计一致 | Papers=523, Notes≥25 | AI |

### R7 · README.md 意外改动收尾（v1 遗留）

| # | 任务 | 验收标准 | 负责人 |
|---|------|---------|--------|
| 21 | 确认当前 `README.md` 的徽章是图片 badge（`.svg`）还是普通链接，还原到期望状态 | 与设计意图一致 | 人工决策 |

---

## 🧯 风险与边界（继承自 v1，强化）

1. **不让 AI 独立写深度内容**：R1 / R2 的论文笔记必须人工读原论文或给 AI 提供原论文摘录再让 AI 协助整理。AI 独立填 400 行 = 大概率臆造公式 / 作者 / 源码路径。
2. **不让 AI 独立做设计决策**：R5（progress.json 边界）、R7（README 徽章风格）都是设计决策，AI 只能执行明确意图。
3. **骨架 🚧 字段即"承诺要核对"**：任何 🚧 留在线上 > 1 周，就应视为坏信号——要么人工补，要么降权（挪到 `drafts/`）。
4. **不拆分 PROGRESS.md**：v1 决议延续——当前 670 行 < 2000 行阈值，不值得拆。

---

## 📎 历史快照归档

- **v1 快照**（2026-04-18 本轮前）：19 篇笔记 / 12 完稿 / 4 骨架 + 2 短 stub / 9 空分类 / PROGRESS.md 490 篇。
- **v1 执行结果**：25 篇笔记（+5 R3 骨架 + 1 Domain_Randomization 补计）/ 12 完稿 / 9 骨架（+5 新）+ 2 短 stub / 4 空分类 / PROGRESS.md 523 篇。
- **v2 目标快照**：理想情况下应达到 29+ 篇笔记 / 18 完稿 / ≤ 5 骨架 / 0 短 stub / 0 空分类。
