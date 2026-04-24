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

