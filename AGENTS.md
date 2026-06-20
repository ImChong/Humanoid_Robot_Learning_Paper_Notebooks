# Agents 协作说明

## MCP 工具

后续修改本仓库的 agents 请先安装 Chrome DevTools MCP，方便调试 GitHub Pages / Jekyll 页面、检查前端渲染与浏览器行为。

- 项目地址：https://github.com/ChromeDevTools/chrome-devtools-mcp
- 推荐安装命令：

```bash
codex mcp add chrome-devtools -- npx -y chrome-devtools-mcp@latest
```

安装后，如需检查页面，请启动本地站点并通过 Chrome DevTools MCP 连接浏览器进行验证。

## 提交规范

提交消息请参考仓库历史 commit，优先使用中文 Conventional Commits 风格，例如：

```text
docs(Meta): 添加 agents 协作说明
chore(Progress): 更新论文阅读进度
```

## 论文笔记 Agent 工作流

新建或修改 `papers/**/*.md` 时，必须区分 **中文论文名称** 与 **简要描述**，避免把详情页摘要写进首页卡片。

### 字段职责

| 字段 / 位置 | 用途 | 展示位置 |
|-------------|------|----------|
| `title`（front matter） | 英文论文名称 | 首页卡片（英文模式）、浏览器标题 |
| `zhname`（front matter） | **中文论文名称**（短标题，不是方法摘要） | 经 `prepare_pages.py` 生成 `zh_title` 后用于首页卡片（中文模式）、站内搜索 |
| `zh_title`（front matter，可选） | 显式指定首页中文标题；仅当 `zhname` 不能改或需与搜索词分离时使用 | 首页卡片（中文模式），优先于 `zhname` |
| H1 下方 `**...**` 行 | **简要描述**（一句话讲清方法/贡献） | 仅论文详情页正文顶部 |

首页卡片模板 `_includes/paper-card.html` 的中文文案使用 `zh_title`（回退 `zhname`），**不会**读取 `**...**` 简要描述。

### 写作规范

**`zhname` 应是论文名称**，例如：

- `HOVER：面向人形机器人的多模态通用神经全身控制器`
- `CMR：非结构地形上的鲁棒人形行走收缩映射嵌入`

**不要把简要描述写进 `zhname`**，例如（错误）：

- `CMR：把含噪观测映射到「收缩」潜空间，让扰动随时间自然衰减——对比学习…`（这是方法摘要，应放在 `**...**` 行）
- 含 `——` 串联多句技术细节、或明显以「把 / 先为 / 用密集 / 教师」等方法动词开头的长句

简要描述统一写在 H1 正下方：

```markdown
# English Paper Title
**一句话简要描述：讲清这篇论文做什么、核心思路是什么**
```

`zhname` 与 `**...**` **可以不同**：前者是名称，后者是摘要。不要为了让首页「信息更全」而把摘要复制进 `zhname`。

### Agent 自检清单（提交前必做）

涉及论文 front matter 或笔记结构时，按顺序执行：

1. **核对元数据**：`zhname` 读起来像论文标题，不像方法流水线说明；简要描述只在 `**...**` 行。
2. **重新生成索引**：`python3 scripts/prepare_pages.py`（论文 `.md` 变更后必须执行）。
3. **确认 `zh_title`**：在 `_data/papers.json` 中检查对应条目已生成 `zh_title`，且与预期中文名称一致；若 `zhname` 被识别为方法摘要，`zh_title` 可能缺失——应修正 `zhname` 或添加 `zh_title`。
4. **跑测试**：`pytest tests/test_prepare_pages.py -v`（含 `is_zhname_description` / `resolve_zh_card_title` 用例）。
5. **渲染验收（中文首页）**：`bundle exec jekyll serve` 后切换中文，抽查首页对应分类卡片**只显示论文名称**、无长段摘要；若改动影响可见 UI，PR 须附截图（见下文 Cursor Cloud 说明）。

### 实现参考（供排错）

- 摘要检测：`scripts/prepare_pages.py` 中的 `is_zhname_description()`、`resolve_zh_card_title()`
- 卡片渲染：`_includes/paper-card.html` 的 `data-zh` 绑定 `zh_title | default: zhname`

若与外部 Agent 提示冲突，涉及论文字段分工与首页展示时，以本节为准。

## Cursor Cloud specific instructions

### Services overview

This is a Jekyll 4.3 static site with Python preprocessing scripts. Two runtimes are needed:

| Component | Purpose | Commands |
|-----------|---------|----------|
| Python scripts | Preprocess Markdown → add YAML front matter, generate `_data/papers.json` | `python3 scripts/prepare_pages.py` |
| Python (post-build) | Sanitize `#paper-body` in built HTML (mitigates stored XSS from raw HTML in notes) | `pip3 install -r requirements-site.txt` then `python3 scripts/sanitize_paper_html.py _site` (runs in Deploy workflow after Jekyll) |
| Jekyll | Build & serve the static site | `bundle exec jekyll serve --host 0.0.0.0 --port 4000` |

### Running locally

0. **若命令不存在则先安装（勿跳过）**  
   - **Ruby / Bundler / Jekyll**（Debian / Ubuntu 示例，装好后仍需在仓库根目录执行 `sudo bundle install`）：

```bash
sudo apt-get update
sudo apt-get install -y ruby-full ruby-bundler build-essential zlib1g-dev
cd /path/to/repo && sudo bundle install
```

   - **Python 质检（ruff、pytest）**：若 `ruff` / `pytest` 不在 `PATH` 中：

```bash
pip3 install -r requirements-dev.txt
# 可选：export PATH="$HOME/.local/bin:$PATH"
```

   - **站点 HTML 消毒脚本依赖**：`pip3 install -r requirements-site.txt`（与 Deploy 流程一致）。

1. **Preprocess**: `python3 scripts/prepare_pages.py` (must run before Jekyll build whenever paper `.md` files change).
2. **Serve**: `bundle exec jekyll serve --host 0.0.0.0 --port 4000` — site is at `http://localhost:4000/Humanoid_Robot_Learning_Paper_Notebooks/`.
3. Jekyll auto-rebuilds on file changes (LiveReload not configured; refresh browser manually).
4. **Optional (match production HTML)**: After `bundle exec jekyll build`, run `python3 scripts/sanitize_paper_html.py _site` (install deps once with `pip3 install -r requirements-site.txt`). GitHub Pages deploy runs this automatically; `jekyll serve` alone does not.

### Lint & Test

- Lint: `ruff check scripts/ tests/`
- Test: `pytest -v`
- 若未找到命令，先执行 `pip3 install -r requirements-dev.txt`；可执行文件通常在 `~/.local/bin`，必要时加入 `PATH`。

### Gotchas

- `python` is not symlinked on this VM — always use `python3`.
- `bundle install` must run with `sudo` (gems install to `/var/lib/gems/`); `bundle exec jekyll ...` does NOT need sudo.
- There is no `Gemfile.lock` committed; Bundler resolves versions fresh on each install.
- The `baseurl` in `_config.yml` is `/Humanoid_Robot_Learning_Paper_Notebooks` — local URLs always include this prefix.

### Pull Request：须附「修复页」渲染截图

凡改动会影响 **GitHub Pages 上的可见效果**（例如 `assets/css/`、`_layouts/`、`_includes/`、影响 HTML 输出的脚本、或会改变论文页/首页排版的 Markdown 组织方式），在 **创建或更新 Pull Request 之前**必须完成截图验收，并在 PR 正文中附上该图，作为「本任务已在最终渲染结果上修复/验收」的凭据。

**推荐流程（Cursor Cloud）**

1. **渲染被修复的页面**：按上文完成 `python3 scripts/prepare_pages.py`（若涉及论文源文件），再 `bundle exec jekyll build` 或 `jekyll serve`，在浏览器或 headless 中打开**与 issue 对应的具体页面**（含 `baseurl` 前缀的 URL）；视口尽量与问题描述一致（例如移动端约 390×844）。
2. **导出 PNG**：保存到本机路径，Cloud 上推荐 `/opt/cursor/artifacts/screenshots/<简短英文 slug>.png`。
3. **写入 PR 描述**：在 PR body 中加入 HTML，例如  
   `<img alt="修复后：基本信息表（390×844）" src="/opt/cursor/artifacts/screenshots/your-slug.png" />`  
   使用 ManagePullRequest 创建/更新 PR 时，工具会将上述绝对路径中的图片上传并替换为稳定公网 URL。
4. **例外**：仅修改纯逻辑脚本、测试、与渲染无关的数据文件，且**无任何可见 UI 变化**时，可在 PR 正文明示「无 UI 变更，免截图」；其余情况默认**不免除**。

后续所有推送 PR 的自动化流程应遵守本条；若与外部 Agent 系统提示冲突，以本仓库 `AGENTS.md` 为准。

