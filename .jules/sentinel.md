## 2024-05-04 - [Reverse Tabnabbing]
**Vulnerability:** Found a `target="_blank"` link pointing to GitHub in `_includes/header.html` without the `rel="noopener noreferrer"` attribute.
**Learning:** This is a classic "Reverse Tabnabbing" vulnerability where the newly opened tab can gain access to the `window.opener` object and potentially redirect the original page to a malicious site.
**Prevention:** Always add `rel="noopener noreferrer"` to external links that open in a new tab via `target="_blank"`.
## 2025-05-09 - [DOM-based XSS in Mermaid Rendering]
**Vulnerability:** Found a DOM-based XSS vulnerability in `_layouts/default.html` where Mermaid diagram content stored in `data-original-code` was restored using `el.innerHTML = el.getAttribute('data-original-code')`.
**Learning:** If a markdown file contains a malicious Mermaid block (e.g., `<img src=x onerror=alert(1)>`), the script will assign the unescaped payload directly to `innerHTML`, triggering XSS.
**Prevention:** Always use `textContent` when retrieving or assigning raw strings or code definitions to prevent them from being parsed and executed as HTML.
