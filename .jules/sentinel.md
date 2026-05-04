## 2024-05-04 - [Reverse Tabnabbing]
**Vulnerability:** Found a `target="_blank"` link pointing to GitHub in `_includes/header.html` without the `rel="noopener noreferrer"` attribute.
**Learning:** This is a classic "Reverse Tabnabbing" vulnerability where the newly opened tab can gain access to the `window.opener` object and potentially redirect the original page to a malicious site.
**Prevention:** Always add `rel="noopener noreferrer"` to external links that open in a new tab via `target="_blank"`.
