# 项目待办计划：Humanoid Robot Learning Paper Notebooks

## Context（背景）

本项目是一个基于 Jekyll 的双语（中/英）人形机器人强化学习论文笔记站点，通过 GitHub Pages 部署到 <https://imchong.github.io/Humanoid_Robot_Learning_Paper_Notebooks/>。README 已列出明确的学习路线图（基础 RL → 精确模仿 → 风格学习 → 技能组合 → 扩散终点 → Sim-to-Real），但当前笔记完成情况与路线图仍有差距：部分路线图论文仅有骨架（🚧 标记待核对），部分旧 stub 已扩写完毕，10 个分类目录中仅 `04_Locomotion` 起步了 1 篇骨架，其余仍为空。本计划基于 git 日志、`papers/` 目录与 README 路线图对比生成，目标是把学习路线图主干补齐到"能发布"的状态，并沉淀下一步的长期扩展方向。

## 当前快照（2026-04-18，复核后）

- PR #1 `claude/generate-project-tasks-i9Kyn` 已合并进 `main`（commit `3c7bd71`），上一轮 P0–P2 的骨架/扩写/脚手架均已落地。
- 笔记总数：`papers/` 下 19 篇 `.md`（分布：01=12，02=1，03=5，04=1）。
- 完稿（≥300 行、含 MimicKit 源码对照或完整方法/工程章节）共 13 篇：
  - `01_Foundational_RL/`: PPO(638)、AWR(519)、DeepMimic(890)、AMP(735)、ASE(650)、ADD(569)、LCP(637)、PHC(636)、CALM(416)。
  - `02_High_Impact_Selection/`: Expressive_WBC(248 — 上一轮从 137 扩到 248，按新模板已算完稿)。
  - `03_Loco-Manipulation_and_WBC/`: LessMimic(314)、OmniXtreme(307)、ULTRA(405)。
- 已扩写但仍可继续打磨：`Domain_Randomization(235)`（上一轮从 106 扩到 235，够用）。
- 含 `🚧` 待核对骨架（本轮 **必须** 消除 `🚧`）：
  - `01_Foundational_RL/PULSE_...`（111 行 / 21 处 🚧）
  - `01_Foundational_RL/Diffusion_Policy`（119 行 / 19 处 🚧）
  - `01_Foundational_RL/BeyondMimic`（103 行 / 19 处 🚧）
  - `04_Locomotion/Learning_to_Walk_in_Minutes`（92 行 / 14 处 🚧）
- 仍是短 stub（<80 行、缺"方法/工程"章节）：
  - `03_Loco-Manipulation_and_WBC/Learning_Humanoid_End-Effector_Control_...`（HERO，56 行）
  - `03_Loco-Manipulation_and_WBC/VIGOR_...`（57 行）
- 完全为空的分类目录：`05_Manipulation` ~ `13_Human_Motion`（共 9 个，`04_Locomotion` 已起步 1 篇骨架）。
- `progress.json`：total=175，done=9，pending=166（与 `papers/` 实际 19 篇完稿/骨架 **不一致**，需同步）。

---

## 🧾 上一轮 TODO 核对（✅ 完成 / [ ] 未完成）

### P0 · 补齐路线图主干（最高优先，1–2 周内）

- [x] **P0#1** 新建 `PULSE_Physics-based_Universal_Latent_Space`（01_Foundational_RL） — ✅ 骨架已建，但仍含 21 处 🚧，深度内容留到下一轮
- [x] **P0#2** 新建 `Diffusion_Policy`（arXiv 2303.04137） — ✅ 骨架已建，仍含 19 处 🚧
- [x] **P0#3** 新建 `BeyondMimic`（2025 扩散 + 控制终点） — ✅ 骨架已建，仍含 19 处 🚧
- [x] **P0#4a** `Domain_Randomization_Understanding_Sim-to-Real_Transfer.md` 106 → 235 行，四大块补齐
- [x] **P0#4b** `Expressive_Whole-Body_Control_for_Humanoid_Robots.md` 137 → 248 行，四大块补齐

### P1 · 站点质量与可维护性

- [x] **P1#5** 复核 `03_Loco-Manipulation_and_WBC/` 5 篇：LessMimic / OmniXtreme / ULTRA 完稿；HERO / VIGOR 确认为 stub
- [x] **P1#6** `progress.json` 中 PHC / ADD 等旧中文路径（`papers/01_基础路线图/...`）已统一为 `papers/01_Foundational_RL/...`
- [x] **P1#7** `README.md` MimicKit 源码一览表补充 PULSE / Diffusion Policy / BeyondMimic（均 ❌ 或 N/A）；`_data/papers.json` 由 `prepare_pages.py` 自动生成新骨架条目

### P2 · 长期拓展

- [x] **P2#8** `04_Locomotion` 新增样例骨架 `Learning_to_Walk_in_Minutes`（**深度内容留到下一轮**）
- [x] **P2#9** `09_Sim-to-Real` 在 `_data/papers.json` 中加 `subtitle_zh` 备注，指向 `Domain_Randomization` / `LCP`
- [x] **P2#10** `scripts/prepare_pages.py` 加入 stub 检测（行数<150 且缺 `## 方法详解`/`## 🔧` 时输出 `[STUB]`）

### P3 · 工程杂项

- [x] **P3#11** `update-badges.yml` 自动更新 `Notes-N`；配套在 `update_badges.py` 里增加过滤规则，`TODO.md` 不计入 Notes 徽章
- [x] **P3#12** MimicKit 覆盖表：PULSE / Diffusion Policy / BeyondMimic 已在 README 标 ❌ 或 N/A

> 结论：上一轮 12 条 TODO **全部交付**（含"建骨架 + 留 🚧"这种阶段性交付）。骨架深度填充、HERO/VIGOR 扩写、空分类起步等后续工作整理到下一轮。

---

## 🆕 下一轮 TODO（2026-04-18 新生成）

遵循 karpathy 编程护栏：每一条都带 **可验证成功标准（verify）**，便于独立跑完 → 自检。

### R1 · 消灭骨架里的 🚧（本轮最重要）

- [ ] **R1#1** 填充 `PULSE_Physics-based_Universal_Latent_Space.md`
  - 核对 arXiv 2407.10174（Luo et al., 2024），补齐"方法详解（VAE + prior）/ 公式 / 具体实例 / 工程价值 / Q&A / 附录"。
  - **verify**：`grep -c 🚧 papers/01_Foundational_RL/PULSE_.../PULSE_...md` 返回 `0`，且 `wc -l` ≥ 400。
- [ ] **R1#2** 填充 `Diffusion_Policy.md`
  - 核对 arXiv 2303.04137，DDPM/DDIM 基础 + receding-horizon + 机器人实验。
  - **verify**：🚧 = 0 且 行数 ≥ 400。
- [ ] **R1#3** 填充 `BeyondMimic.md`
  - 路线图中 2025 年扩散 + 控制终点，补齐方法 / 训练 pipeline / 与 AMP·ASE·CALM 对比。
  - **verify**：🚧 = 0 且 行数 ≥ 400。
- [ ] **R1#4** 扩写 `04_Locomotion/Learning_to_Walk_in_Minutes.md`
  - 核对 Rudin et al. 2021，massively parallel PPO、地形课程、奖励设计。
  - **verify**：🚧 = 0 且 行数 ≥ 300（该分类首篇样例，不必追求 600+）。

### R2 · 旧 stub 收尾

- [ ] **R2#5** 扩写 `HERO (Learning_Humanoid_End-Effector_Control_...)` 从 56 行到 ≥300 行
  - 按 CALM 模板补齐：方法详解 / 具体实例 / 工程价值 / Q&A / 附录。
  - **verify**：文件行数 ≥ 300 且包含 `## 方法详解` 与 `## 🔧 工程价值`。
- [ ] **R2#6** 扩写 `VIGOR_Visual_Goal-In-Context_Inference_for_Unified_Humanoid_Fall_Safety.md` 从 57 行到 ≥300 行
  - **verify**：同上。

### R3 · 空分类起步（按主题批量，每个分类至少 1 篇骨架）

> 只建骨架、不求完稿，目的是打通"新分类如何起步"的路径，避免目录空壳。

- [ ] **R3#7** `05_Manipulation`：新增首篇骨架（建议 `Diffusion Policy for Manipulation` 或 `RT-2`）。
- [ ] **R3#8** `06_Teleoperation`：新增首篇骨架（建议 `OpenTeleVision` 或 `HumanPlus Teleoperation`）。
- [ ] **R3#9** `07_Navigation`：新增首篇骨架（建议 `ViNT` / `GNM`）。
- [ ] **R3#10** `08_State_Estimation`：新增首篇骨架（建议 `TRAM` / `TRACE`）。
- [ ] **R3#11** `10_Simulation_Benchmark`：新增首篇骨架（建议 `HumanoidBench` 或 `Isaac Lab`）。
- **verify（R3 整体）**：`find papers/{05..10}_* -name "*.md" | wc -l` ≥ 5；每个骨架至少含"基本信息 / 一句话 / 缩写 / 讨论"四节。
- （`11_Hardware_Design` / `12_Physics-Based_Animation` / `13_Human_Motion` 暂缓到 R+1 轮。）

### R4 · 站点数据一致性

- [ ] **R4#12** 同步 `progress.json` 与 `papers/` 实际笔记
  - 当前 total=175 / done=9 / pending=166，而 `papers/` 实际完稿 13 篇 + 骨架 6 篇。
  - **verify**：`progress.json` 中 `status=done` 的条目数 = `papers/**/*.md` 行数 ≥ 300 的文件数（13）；新建的 6 个骨架 `status=reading`。
- [ ] **R4#13** 跑一次 `python scripts/prepare_pages.py` 并盯 `[STUB]` 日志，确认 R1/R2 完成后日志里不再出现 PULSE / Diffusion Policy / BeyondMimic / Learning_to_Walk / HERO / VIGOR。
  - **verify**：`python scripts/prepare_pages.py 2>&1 | grep '\[STUB\]'` 输出 0 行（HERO/VIGOR 已扩写、其余 🚧 已清）。
- [ ] **R4#14** 本地 `bundle exec jekyll serve` 打开首页，R3 新建的 5 个分类各自的索引页能渲染出骨架卡片（不 404）。

### R5 · 徽章 & 发布

- [ ] **R5#15** 验证 `Notes-N` 徽章：完成 R1–R3 后应从 `Notes-16`（原旧值）自动跳到 ≥24（13 完稿 + 6 骨架 + 5 新骨架）。
  - **verify**：`python scripts/update_badges.py` 预览，README 徽章数字对上。
- [ ] **R5#16** 推送到 `claude/generate-project-tasks-*` 新分支 → 等 `deploy.yml` 绿灯 → 访问线上站点抽查 3 个新页面。

### R6 · 长期（可选，按兴趣）

- [ ] **R6#17** MimicKit 源码对照补全：给 PULSE / Diffusion Policy 加一章"官方代码/复现仓库"链接（没有就写明 N/A，不要臆造）。
- [ ] **R6#18** 脚本增强：`prepare_pages.py` 的 `[STUB]` 检测升级成"行数 + 章节关键词 + 🚧 计数"三合一报告，输出到 `papers/PROGRESS.md` 底部。
- [ ] **R6#19** `09_Sim-to-Real` 从"只是 alias"升级成"独立分类页"：新增 1 篇 sim-to-real 专题总结笔记（可引用 DR + LCP 的结论，不必重复）。

---

## 涉及的关键文件（不变）

- `README.md`（路线图 / 徽章 / 源码一览表）
- `progress.json`（阅读进度 JSON）
- `_data/papers.json`（站点索引，新增论文必须同步；由 `prepare_pages.py` 生成）
- `scripts/prepare_pages.py`（front matter / 索引生成；已带 `[STUB]` 检测）
- `scripts/update_badges.py`（`Notes-N` 徽章自动化，已过滤 `TODO.md`）
- `papers/01_Foundational_RL/CALM_.../CALM_...md`（最新完整模板，写新笔记首选参照）
- `papers/01_Foundational_RL/PHC_.../PHC_...md`（含 MimicKit 源码对照的样板）
- `.github/workflows/deploy.yml`（部署流水线）

## 验证方式（每轮通用）

1. 本地 Jekyll 构建：`bundle exec jekyll serve`，打开 <http://localhost:4000/> 确认新论文卡片出现在首页与对应分类页。
2. 新增笔记后运行 `python scripts/prepare_pages.py`，检查 `_data/papers.json` 是否生成成功且 `[STUB]` 警告收敛。
3. `git push` 到分支 → 等待 `deploy.yml` 绿灯 → 访问线上站点核对新页面。
4. 运行 `python scripts/update_badges.py` 预览 README 徽章数字是否符合预期。
5. 抽查 `progress.json` 里 `status: done` 的条目数量与 `papers/` 实际完稿 `.md` 数量一致。

## 执行顺序建议

先 **R2（HERO/VIGOR 扩写，手头信息最全）** → **R1（3 篇 01 骨架 + 04 骨架深度内容，按 PULSE → Diffusion Policy → BeyondMimic → Learning_to_Walk 顺序，与 README 路线图一致）** → **R4（数据一致性，收尾）** → **R3（空分类起步，可拆成多轮）** → **R5（徽章 + 发布）**。R6 留作长期。

---

## 🔎 上一轮执行进度快照（归档，保留作为历史）

> 以下内容来自上一轮 PR `claude/generate-project-tasks-i9Kyn`，已全部合入 main（commit `3c7bd71`）。保留以便追溯。

### 已完成（P0–P2）
- ✅ **P0#4a** `Domain_Randomization` 从 106 行扩展到 235 行，补齐"具体实例/工程价值/Q&A/讨论/附录"。
- ✅ **P0#4b** `Expressive_Whole-Body_Control` 从 137 行扩展到 248 行，补齐"具体实例/工程价值/扩展 Q&A/附录"。
- ✅ **P0#1–3** 新建 3 篇骨架文件（内容标记为 🚧 待核对，等待真正读论文后填充）：
  - `papers/01_Foundational_RL/PULSE_Physics-based_Universal_Latent_Space/`
  - `papers/01_Foundational_RL/Diffusion_Policy/`
  - `papers/01_Foundational_RL/BeyondMimic/`
- ✅ **P1#5** `03_Loco-Manipulation_and_WBC/` 审阅结果：

  | 论文 | 行数 | 结论 |
  |------|-----:|------|
  | LessMimic | 314 | ✅ 完稿（有方法/实验/工程/3阶段训练） |
  | OmniXtreme | 307 | ✅ 完稿（有方法/工程/ADR/执行器细节） |
  | ULTRA | 405 | ✅ 完稿（有3模块方法/工程/创新点） |
  | HERO (Learning_Humanoid_End-Effector_Control_...) | 56 | 🚧 **Stub**——仅基本信息/一句话/缩写/讨论。后续扩写（→ R2#5）。 |
  | VIGOR | 57 | 🚧 **Stub**——同上。后续扩写（→ R2#6）。 |

- ✅ **P1#6** `progress.json` 中 PHC / ADD 等条目的旧中文路径 (`papers/01_基础路线图/...`) 已统一为 `papers/01_Foundational_RL/...`，status 按实际 papers/ 目录同步。
- ✅ **P1#7** `README.md` MimicKit 源码一览表补充 PULSE / Diffusion Policy / BeyondMimic 三行（均标记 ❌ 或 N/A）。`_data/papers.json` 由 `prepare_pages.py` 自动生成，本次运行后已包含三个新骨架。
- ✅ **P2#8** `04_Locomotion` 新增一篇骨架 `Learning_to_Walk_in_Minutes` 作为分类起步样例。
- ✅ **P2#9** `09_Sim-to-Real` 在 `_data/papers.json` 中添加 `subtitle_zh` 备注，指向 `01_Foundational_RL` 的 `Domain_Randomization` 与 `LCP`。
- ✅ **P2#10** `scripts/prepare_pages.py` 加入 stub 检测：在生成 `papers.json` 时对行数 < 150 且缺 `## 方法详解` / `## 🔧` 任一章节的 .md 打印 `[STUB]` 警告。
- ✅ **配套**：`scripts/update_badges.py` 增加过滤规则，`TODO.md` 不计入 Notes 徽章。
