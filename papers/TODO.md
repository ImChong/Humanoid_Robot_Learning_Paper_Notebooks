# 项目待办计划：Humanoid Robot Learning Paper Notebooks

## Context（背景）

本项目是一个基于 Jekyll 的双语（中/英）人形机器人强化学习论文笔记站点，通过 GitHub Pages 部署到 <https://imchong.github.io/Humanoid_Robot_Learning_Paper_Notebooks/>。学习路线图：基础 RL → 精确模仿 → 风格学习 → 技能组合 → 扩散终点 → Sim-to-Real。

---

## 当前快照（2026-04-18 执行后）

- **Notes 徽章**：`Notes-20`（16 → 20，本轮新增 4 篇骨架）
- **Papers 徽章**：`Papers-489`（progress.json 追踪计划总量）
- **完善笔记**（>200 行，含方法/实例/Q&A）：PPO、AWR、DeepMimic、AMP、ASE、ADD、LCP、PHC、CALM、Domain_Randomization（扩写后）、Expressive_WBC（扩写后）、LessMimic、OmniXtreme、ULTRA — 共 **14 篇**
- **骨架笔记**（🚧 待填充内容）：PULSE、Diffusion_Policy、BeyondMimic、Learning_to_Walk_in_Minutes — 共 **4 篇**
- **Stub 笔记**（< 150 行，缺方法详解）：HERO（56行）、VIGOR（57行）— 共 **2 篇**

---

## 📋 待办清单

### P0 · 路线图主干

- [x] **#1** 新建 `PULSE` 骨架（`01_Foundational_RL/PULSE_Physics-based_Universal_Latent_Space/`）
- [x] **#2** 新建 `Diffusion_Policy` 骨架（`01_Foundational_RL/Diffusion_Policy/`）
- [x] **#3** 新建 `BeyondMimic` 骨架（`01_Foundational_RL/BeyondMimic/`）
- [x] **#4a** 扩写 `Domain_Randomization` stub（106 → 235 行，补具体实例/工程价值/Q&A/附录）
- [x] **#4b** 扩写 `Expressive_Whole-Body_Control` stub（137 → 248 行，补具体实例/Q&A/附录）
- [ ] **#5** 读 PULSE 原论文并填充骨架（正文/公式/Q&A）——**需要人工**
- [ ] **#6** 读 Diffusion Policy 原论文并填充骨架——**需要人工**
- [ ] **#7** 读 BeyondMimic 原论文并填充骨架——**需要人工**

### P1 · 站点质量

- [x] **#8** 审阅 `03_Loco-Manipulation_and_WBC/` 5 篇完整度（发现 HERO/VIGOR 为 stub）
- [x] **#9** 同步 `progress.json`：已完稿论文 folder 路径统一至 `01_Foundational_RL/`，status 设为 done
- [x] **#10** `README.md` MimicKit 源码一览表补 PULSE / Diffusion Policy / BeyondMimic 三行
- [ ] **#11** 扩写 `HERO`（Learning_Humanoid_End-Effector_Control，56行）——建议人工通读论文后填充
- [ ] **#12** 扩写 `VIGOR`（57行）——同上
- [ ] **#13** 补全 `progress.json` 中 Domain Randomization 2017 Tobin 原始论文条目的 folder 路径（当前指向不存在的旧目录，与 Chen 2021 笔记是两篇不同论文）

### P2 · 长期拓展

- [x] **#14** `04_Locomotion` 新增 `Learning_to_Walk_in_Minutes` 骨架
- [x] **#15** `09_Sim-to-Real` 在 `_data/papers.json` 加 `subtitle_zh` 交叉引用备注
- [x] **#16** `scripts/prepare_pages.py` 加入 `[STUB]` 构建时检测（< 150 行 + 缺方法章节）
- [ ] **#17** 读 `Learning_to_Walk_in_Minutes` 并填充 `04_Locomotion` 样例骨架——**需要人工**
- [ ] **#18** 为 `05_Manipulation`、`06_Teleoperation`、`07_Navigation` 各选一篇样例论文建骨架
- [ ] **#19** `09_Sim-to-Real` 正式添加专项论文（ADR、Real-to-Sim、Privileged Learning 等）

### P3 · 工程杂项

- [x] **#20** `update_badges.py` 排除 `TODO.md`，Notes 徽章 16 → 20 ✓
- [x] **#21** README MimicKit 覆盖表新增三行，未覆盖论文标 ❌
- [ ] **#22** CI 部署后验证线上站点新页面正常渲染（打开 GitHub Pages 实际页面检查）
- [ ] **#23** 在 `_data/papers.json` 中为 `02_High_Impact_Selection` 的其余 4 个空子分类补充至少 1 篇骨架

---

## 🔜 新待办（本轮执行后发现的新需求）

> 以下是本轮扫描中新发现、计划中未列出的项目。

- [ ] **A** `progress.json` 中有多条 `03_Loco-Manipulation_and_WBC` 规划论文（LATENT 等）尚未建目录——按需建骨架
- [ ] **B** `PULSE` 骨架标题已用 progress.json 核对（"Physically Plausible Universal Latent Skill Extraction"），但 arXiv 号留空；CALM → PULSE 链路上可能对应多个版本，需核对实际是 ICLR 2024 的哪篇
- [ ] **C** `BeyondMimic` arXiv 号完全为 🚧——需查原文 URL 后更新骨架 `## 📋 基本信息` 表
- [ ] **D** `Diffusion_Policy` 的 arXiv 号 2303.04137 需核对（我当前标记的是 🚧 待核对）；若确认正确，去掉骨架中的 🚧
- [ ] **E** 现有完善笔记（如 ASE、ADD）缺少"讨论记录"正文——后续阅读过程中随时补充
- [ ] **F** Jekyll 本地构建尚未测试（`bundle exec jekyll serve`）——建议在 merge 前做一次

---

## 涉及的关键文件

| 文件 | 用途 |
|------|------|
| `README.md` | 路线图 / 徽章 / MimicKit 源码一览表 |
| `progress.json` | 阅读进度 JSON（489 条计划论文） |
| `_data/papers.json` | Jekyll 站点索引（由 prepare_pages.py 生成） |
| `scripts/prepare_pages.py` | front matter 添加 + stub 检测 + 索引生成 |
| `scripts/update_badges.py` | Notes-N 徽章自动更新 |
| `papers/01_Foundational_RL/CALM_.../...md` | 最新完整笔记模板 |
| `papers/01_Foundational_RL/PHC_.../...md` | 含 MimicKit 源码对照的样板 |
| `.github/workflows/deploy.yml` | GitHub Pages 部署流水线 |

---

## 验证方式

1. 本地构建：`bundle exec jekyll serve`，确认新论文卡片出现。
2. 新增笔记后：`python scripts/prepare_pages.py`，检查 `[STUB]` 警告与 `_data/papers.json` 更新。
3. push 后：等待 `deploy.yml` 绿灯，访问线上站点确认新页面。
4. 徽章检查：`python scripts/update_badges.py`，确认 `Notes-N` 正确。
5. `progress.json` 抽查：`status: done` 数量应与 papers/ 完善笔记数一致（目前为 14）。
