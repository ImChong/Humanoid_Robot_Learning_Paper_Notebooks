# 项目待办计划：Humanoid Robot Learning Paper Notebooks

## Context（背景）

本项目是一个基于 Jekyll 的双语（中/英）人形机器人强化学习论文笔记站点，通过 GitHub Pages 部署到 <https://imchong.github.io/Humanoid_Robot_Learning_Paper_Notebooks/>。README 已列出明确的学习路线图（基础 RL → 精确模仿 → 风格学习 → 技能组合 → 扩散终点 → Sim-to-Real），但当前笔记完成情况与路线图仍有差距：部分路线图论文缺失文件夹，部分现有笔记体量远小于完整笔记（疑似 stub），且 10 个分类目录（04–13）完全为空。本计划基于 git 日志、`papers/` 目录与 README 路线图对比生成，目标是把学习路线图主干补齐到"能发布"的状态，并沉淀下一步的长期扩展方向。

## 当前快照（2026-04-18）

- 笔记徽章：`Notes-16`，`Papers-489`（`progress.json` 追踪 489 篇，但笔记仅 16 篇）。
- 已完善（>500 行、含 MimicKit 源码对照）：`PPO`、`AWR`、`DeepMimic`、`AMP`、`ASE`、`ADD`、`LCP`、`PHC`、`CALM`。
- 体量偏小疑似 stub（<200 行）：
  - `papers/01_Foundational_RL/Domain_Randomization_Understanding_Sim-to-Real_Transfer/` (106 行)
  - `papers/02_High_Impact_Selection/Expressive_Whole-Body_Control_for_Humanoid_Robots/` (137 行)
- 中等体量需复核：`papers/03_Loco-Manipulation_and_WBC/` 下 5 篇（ULTRA / VIGOR / LessMimic / OmniXtreme / Learning_Humanoid_End-Effector_Control）。
- 路线图中尚未建目录：`PULSE (2024)`、`Diffusion Policy`、`BeyondMimic (2025)`。
- 完全为空的分类目录：`04_Locomotion` ~ `13_Human_Motion`（共 10 个）。
- 最近提交集中在 footer / 徽章样式修复，笔记内容改动本周已暂停。

## TODO 计划（按优先级）

### P0 · 补齐路线图主干（最高优先，1–2 周内）

1. **新建 `PULSE_Physics-based_Universal_Latent_Space`（01_Foundational_RL）**
   - arXiv：2407.10174（Luo et al., 2024）
   - 路线位置：技能组合主线 ASE → CALM → **PULSE**。
   - 参考模板：`papers/01_Foundational_RL/CALM_Conditional_Adversarial_Latent_Models_for_Directable_Virtual_Characters/`（最近刚完成、结构最新）。
2. **新建 `Diffusion_Policy`（新建 `01_Foundational_RL` 或并入 `02_High_Impact_Selection`，读完后定）**
   - arXiv：2303.04137。扩散控制终点主线起点，需与 BeyondMimic 配套。
3. **新建 `BeyondMimic`（02_High_Impact_Selection 或单列）**
   - 路线图中 2025 年扩散 + 控制的终点论文。
4. **补完两个 stub：**
   - `Domain_Randomization_Understanding_Sim-to-Real_Transfer.md`：按模板扩充"方法详解/具体实例/工程价值/Q&A"四大块。
   - `Expressive_Whole-Body_Control_for_Humanoid_Robots.md`：补足方法详解与工程价值（目前只有 137 行）。

### P1 · 站点质量与可维护性（并行推进）

5. **复核 `03_Loco-Manipulation_and_WBC/` 5 篇状态**
   - 逐一对照 `CALM` 笔记的完整结构（基本信息/一句话/缩写/问题/方法/实例/工程价值/Q&A/讨论），确定是完稿还是需要扩写；把结论写入 `progress.json` 的 `status` 字段。
6. **同步 `progress.json` 与实际笔记**
   - 当前 `progress.json` 记录 489 条、有 `status: done/reading/pending` 字段；以 `papers/` 目录为准校对并更新，消除"徽章 16 vs 表单 489"带来的歧义。
7. **`README.md` 路线图小修**
   - PULSE / Diffusion Policy / BeyondMimic 建目录后在 README "源码层面一览"表和学习路线图里补齐勾选与链接。

### P2 · 长期拓展（按主题批量推进，可做可不做）

8. **挑选 `04_Locomotion` 首篇样例笔记**（建议 `Learning-to-Walk-in-Minutes`/`HumanoidBench` 任一）作为模板，验证"新分类如何起步"。
9. **`09_Sim-to-Real` 建立专题入口**：把 `Domain_Randomization` + `LCP` 从 `01_Foundational_RL` 交叉引用到 `09_Sim-to-Real`（不复制文件，用 `_data/papers.json` 做别名即可）。
10. **脚本增强（可选）**：在 `scripts/prepare_pages.py` 中加一段校验——检测 stub（如行数 < 200 或缺少 `## 方法详解`）并在构建日志里标出，防止再出现"目录建了但内容空"。

### P3 · 工程杂项

11. **`update-badges.yml` 已自动更新 `Notes-N`**；完成 P0 后确认徽章从 16 自动升到 19+。
12. **检查 MimicKit 覆盖表**：README 中仅列到 ADD，PULSE / Diffusion Policy 若 MimicKit 暂无实现，在表中标 ❌ 或 "N/A"，避免误导。

## 涉及的关键文件

- `README.md`（路线图/徽章/源码一览表）
- `progress.json`（阅读进度 JSON，101KB）
- `_data/papers.json`（站点索引，新增论文必须同步）
- `scripts/prepare_pages.py`（front matter / 索引生成，新增论文会被它扫到）
- `scripts/update_badges.py`（`Notes-N` 徽章自动化）
- `papers/01_Foundational_RL/CALM_.../CALM_...md`（最新完整模板，写新笔记首选参照）
- `papers/01_Foundational_RL/PHC_.../PHC_...md`（含 MimicKit 源码对照的样板）
- `.github/workflows/deploy.yml`（部署流水线）

## 验证方式

1. 本地 Jekyll 构建：`bundle exec jekyll serve`，打开 <http://localhost:4000/> 确认新论文卡片出现在首页与对应分类页。
2. 新增笔记后运行 `python scripts/prepare_pages.py`，检查是否自动写入 front matter、并且 `_data/papers.json` 生成成功。
3. `git push` 到 `claude/generate-project-tasks-i9Kyn` → 等待 `deploy.yml` 绿灯 → 访问线上站点核对新页面。
4. 运行 `python scripts/update_badges.py` 预览 README 徽章是否从 `Notes-16` 升到预期数字。
5. P1 完成后抽查 `progress.json` 里 `status: done` 的条目数量与 `papers/` 实际 `.md` 文件数量一致。

## 执行顺序建议

先做 **P0 第 4 项（补 stub）**——工作量最小且能提高现有页面质量；再按 PULSE → Diffusion Policy → BeyondMimic 顺序新增路线图论文（这也与 README 学习路线图阅读顺序一致）；P1 与 P0 可穿插；P2/P3 留作长期目标，不必压在这一轮完成。

---

## 🔎 2026-04-18 执行进度快照

本轮执行（分支 `claude/generate-project-tasks-i9Kyn`）已完成：

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
  | HERO (Learning_Humanoid_End-Effector_Control_...) | 56 | 🚧 **Stub**——仅基本信息/一句话/缩写/讨论。后续扩写。 |
  | VIGOR | 57 | 🚧 **Stub**——同上。后续扩写。 |

- ✅ **P1#6** `progress.json` 中 PHC / ADD 等条目的旧中文路径 (`papers/01_基础路线图/...`) 已统一为 `papers/01_Foundational_RL/...`，status 按实际 papers/ 目录同步。
- ✅ **P1#7** `README.md` MimicKit 源码一览表补充 PULSE / Diffusion Policy / BeyondMimic 三行（均标记 ❌ 或 N/A）。`_data/papers.json` 由 `prepare_pages.py` 自动生成，本次运行后已包含三个新骨架。
- ✅ **P2#8** `04_Locomotion` 新增一篇骨架 `Learning_to_Walk_in_Minutes` 作为分类起步样例。
- ✅ **P2#9** `09_Sim-to-Real` 在 `_data/papers.json` 中添加 `subtitle_zh` 备注，指向 `01_Foundational_RL` 的 `Domain_Randomization` 与 `LCP`。
- ✅ **P2#10** `scripts/prepare_pages.py` 加入 stub 检测：在生成 `papers.json` 时对行数 < 150 且缺 `## 方法详解` / `## 🔧` 任一章节的 .md 打印 `[STUB]` 警告。
- ✅ **配套**：`scripts/update_badges.py` 增加过滤规则，`TODO.md` 不计入 Notes 徽章。

### 本轮后续仍待处理（由你决定是否继续让 AI 跟进）
1. **P0 深度内容**：3 个新骨架的具体公式、源码对照、完整 Q&A 需要读原论文后填写（不建议让 AI 独立完成，易臆造）。
2. **P1 扩写**：`HERO`、`VIGOR` 两个新发现的 stub 等待后续扩写。
3. **P3**：部署成功后用 `update_badges.py` 检查徽章是否从 `Notes-16` 自动跳到新值。
