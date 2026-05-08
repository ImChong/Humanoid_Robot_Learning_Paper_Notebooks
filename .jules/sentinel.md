## 2024-05-04 - [Reverse Tabnabbing]
**Vulnerability:** Found a `target="_blank"` link pointing to GitHub in `_includes/header.html` without the `rel="noopener noreferrer"` attribute.
**Learning:** This is a classic "Reverse Tabnabbing" vulnerability where the newly opened tab can gain access to the `window.opener` object and potentially redirect the original page to a malicious site.
**Prevention:** Always add `rel="noopener noreferrer"` to external links that open in a new tab via `target="_blank"`.
## 2025-05-09 - [DOM-based XSS in Mermaid Rendering]
**Vulnerability:** Found a DOM-based XSS vulnerability in `_layouts/default.html` where Mermaid diagram content stored in `data-original-code` was restored using `el.innerHTML = el.getAttribute('data-original-code')`.
**Learning:** If a markdown file contains a malicious Mermaid block (e.g., `<img src=x onerror=alert(1)>`), the script will assign the unescaped payload directly to `innerHTML`, triggering XSS.
**Prevention:** Always use `textContent` when retrieving or assigning raw strings or code definitions to prevent them from being parsed and executed as HTML.
## 2025-05-09 - [DOM-based XSS in Paper Navigation Initialization]
**Vulnerability:** Found a DOM-based XSS vulnerability in `assets/js/paper.js` within the `initPaperNav()` function, where parsed JSON fields (`prev.short`, `next.short`, `prev.url`, `next.url`) from `_data/roadmap_order.yml` were concatenated into strings and assigned directly to `innerHTML` via `nav.innerHTML = html;` and `sidebarNav.innerHTML = sidebarHtml;`.
**Learning:** The Jekyll `jsonify` filter encodes objects into JSON format, but it does NOT HTML-escape the string values inside the JSON. When JavaScript later parses this JSON block and reads fields like `paper.title` or `paper.short`, the string values are decoded back to raw text. Therefore, assigning these values to `innerHTML` is insecure and leads to XSS if the data (even originating from trusted markdown front matter) contains `<` or `>` characters.
**Prevention:** Always construct HTML structures dynamically using safer DOM APIs like `document.createElement()`, `setAttribute()`, and `textContent` rather than concatenating strings containing unescaped data and assigning them to `innerHTML`.
