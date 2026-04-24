# 项目待办计划 v4：从"补骨架"转向"质量校准"

> **版本**：v4（继承自 `TODO_v3.md`；本轮核对日期：2026-04-24）
> **本版定位**：v3 的主线目标已基本完成，High Impact 的 4 篇空骨架已扩成可读笔记；下一阶段重点不再是堆数量，而是修正统计口径、消除剩余 stub、补齐本地站点验证和源码/论文对照。

---

## Context（背景）

本轮已同步远端 `main`，确认仓库是最新版本。按 `papers/todos/TODO_v3.md` 核对：

- R1 / R2 / R3 / R5 已完成。
- R4#8 已完成。
- R4#7（`bundle exec jekyll serve` 真机渲染）仍未完成：本机缺少 `bundle` 命令，当前无法启动 Jekyll。

此外，`python3 scripts/prepare_pages.py` 的当前输出显示：

- `_data/papers.json` 生成 **40** 篇笔记 / **13** 个分类。
- 原 TODO_v3 中 4 篇 `02_High_Impact_Selection/` 骨架已扩充，不再触发 `[STUB]`。
- 本轮继续补齐 `Unitree_H1_Whitepaper` 与 `HumanML3D` 后，`prepare_pages.py` 已不再输出 `[STUB]`。

---

## 当前改进判断

仓库已经从"目录覆盖不足"进入"质量控制不足"阶段。下一步最值得做的不是继续新增论文，而是：

1. **统一统计口径**：`prepare_pages.py` 统计的是实际 `.md` 笔记，`progress.json` 仍包含大量路线图候选条目，不能直接当作完稿率。
2. **消除剩余 stub**：Unitree H1 和 HumanML3D 是当前唯一被脚本明确标出的短笔记。
3. **站点验证自动化**：TODO_v1/v2/v3 都提到 Jekyll 真机渲染，但一直没有稳定完成，应补 `bundle` 安装说明或 CI 构建检查。
4. **减少 `🚧` 语义债务**：部分完稿笔记仍保留"深度技术细节待细化"或"代码待确认"，建议区分"可发布待精读"与"真实缺失信息"。
5. **源码对照增强**：高价值笔记应逐步补"论文概念 -> 代码文件/模块"映射，而不是只停留在摘要。

---

## 🧾 v4 TODO 核对（✅ 完成 / [ ] 未完成）

### R1 · 剩余 Stub 清零

| # | 任务 | 验收标准 | 负责人 |
|---|------|---------|--------|
| 1 | ✅ 扩写 `Unitree_H1_Whitepaper` | `prepare_pages.py` 不再输出该文件 `[STUB]`；补 `## 🔧 方法详解` / 硬件参数 / 控制意义 | AI (Done) |
| 2 | ✅ 扩写 `HumanML3D` | `prepare_pages.py` 不再输出该文件 `[STUB]`；补数据格式 / 文本动作任务 / 与 humanoid motion prior 的关系 | AI (Done) |

### R2 · 站点构建与依赖

| # | 任务 | 验收标准 | 负责人 |
|---|------|---------|--------|
| 3 | [ ] 补本地 Jekyll 依赖说明 | README 或新文档说明 `bundle`/Ruby 依赖安装方式 | AI |
| 4 | [ ] 本地执行 `bundle exec jekyll serve` 或等价 build | 13 个分类和 40 篇笔记可正常渲染；记录日志 | 人工 + AI |
| 5 | [ ] 考虑加 GitHub Actions 构建检查 | PR / push 后自动跑页面构建，避免只靠本机验证 | AI |

### R3 · 统计口径治理

| # | 任务 | 验收标准 | 负责人 |
|---|------|---------|--------|
| 6 | [ ] 拆分 `progress.json` 的"路线图候选"与"已有笔记"状态 | 现有笔记完稿率不被 100+ 候选条目稀释 | AI |
| 7 | [ ] 新增一个只统计 `papers/**/*.md` 的报告脚本 | 输出总数、done/stub、含 `🚧` 文件、缺关键章节文件 | AI |
| 8 | [ ] 让 `prepare_pages.py` 的 `[STUB]` 规则与 `sync_progress.py` 对齐 | 同一文件不会在两个脚本中得到矛盾状态 | AI |

### R4 · 笔记质量升级

| # | 任务 | 验收标准 | 负责人 |
|---|------|---------|--------|
| 9 | [ ] 对 High Impact 7 篇做二读校准 | 每篇补实验数字、失败案例、与相邻论文差异 | 人工 + AI |
| 10 | [ ] 每个大类挑 1 篇加"源码对照" | 至少列出官方仓库入口、关键模块、复现注意事项 | AI + 人工校对 |
| 11 | [ ] 清理非必要 `🚧` | 保留真正缺失项；泛泛的"待细化"改成明确 TODO | AI |

---

## 建议优先级

1. 先做 R2：站点构建验证是 v1/v2/v3 延续下来的唯一老债务。
2. 再做 R3：统计口径不清会持续误导后续计划。
3. 最后做 R4：深度二读和源码对照适合成批推进。

---

## 验证命令

```bash
python3 scripts/prepare_pages.py
python3 scripts/sync_progress.py
git status --short
```

当前限制：

```bash
bundle --version
# /bin/bash: line 1: bundle: command not found
```

---

## 历史快照归档

- **v3 第三轮执行后**：38 篇 / 34 完稿 / 4 骨架 / 0 短 stub / 0 空分类。
- **v4 创建时**：40 篇 / 13 分类；High Impact 4 篇骨架已扩充；Unitree H1 与 HumanML3D 已补齐到脚本通过；`prepare_pages.py` 当前 0 篇 `[STUB]`；Jekyll 本机渲染仍未验证。
