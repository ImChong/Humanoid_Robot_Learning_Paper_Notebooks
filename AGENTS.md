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

## Cursor Cloud specific instructions

### Services overview

This is a Jekyll 4.3 static site with Python preprocessing scripts. Two runtimes are needed:

| Component | Purpose | Commands |
|-----------|---------|----------|
| Python scripts | Preprocess Markdown → add YAML front matter, generate `_data/papers.json` | `python3 scripts/prepare_pages.py` |
| Python (post-build) | Sanitize `#paper-body` in built HTML (mitigates stored XSS from raw HTML in notes) | `pip install -r requirements-site.txt` then `python3 scripts/sanitize_paper_html.py _site` (runs in Deploy workflow after Jekyll) |
| Jekyll | Build & serve the static site | `bundle exec jekyll serve --host 0.0.0.0 --port 4000` |

### Running locally

1. **Preprocess**: `python3 scripts/prepare_pages.py` (must run before Jekyll build whenever paper `.md` files change).
2. **Serve**: `bundle exec jekyll serve --host 0.0.0.0 --port 4000` — site is at `http://localhost:4000/Humanoid_Robot_Learning_Paper_Notebooks/`.
3. Jekyll auto-rebuilds on file changes (LiveReload not configured; refresh browser manually).
4. **Optional (match production HTML)**: After `bundle exec jekyll build`, run `python3 scripts/sanitize_paper_html.py _site` (install deps once with `pip install -r requirements-site.txt`). GitHub Pages deploy runs this automatically; `jekyll serve` alone does not.

### Lint & Test

- Lint: `ruff check scripts/ tests/`
- Test: `pytest -v`
- Both are in `PATH` at `~/.local/bin` (user-installed via pip).

### Gotchas

- `python` is not symlinked on this VM — always use `python3`.
- `bundle install` must run with `sudo` (gems install to `/var/lib/gems/`); `bundle exec jekyll ...` does NOT need sudo.
- There is no `Gemfile.lock` committed; Bundler resolves versions fresh on each install.
- The `baseurl` in `_config.yml` is `/Humanoid_Robot_Learning_Paper_Notebooks` — local URLs always include this prefix.

### Pull Request：附带页面渲染验证截图

推送工作分支并**创建或更新 GitHub PR 后**，在 **PR 描述中附上「页面渲染验证成功」的截图**，便于审阅者在未本地起站的情况下确认样式或交互是否符合预期。

- **截图内容**：优先截取本次改动直接影响的区域（例如 `#paper-body` 内 Mermaid、暗色主题切换后、窄视口移动端等），并在正文中用一两句话说明对应页面路径或验证方式。
- **验证方式**（任选其一即可）：本地执行 `python3 scripts/prepare_pages.py` 与 `bundle exec jekyll serve` 后用浏览器截图；环境无完整 Jekyll 时，可用 **headless Chrome**（如 `puppeteer-core`）加载临时 HTML fixture、内联或引用本次改动的 `assets/css/style.css` 相关规则后截图；已安装 **Chrome DevTools MCP** 时，可在真实浏览器中打开本地站点并截图。
- **嵌入 PR**：使用 Cursor Cloud 的 PR 管理能力时，在说明里使用 `<img alt="…" src="/opt/cursor/artifacts/screenshots/某文件.png" />` 引用本地截图路径，由工具侧上传并重写为可访问 URL；亦可手动将图片粘贴到 GitHub PR 描述。
