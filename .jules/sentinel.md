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
## 2024-05-10 - [Stored XSS in Jekyll Templates]
**Vulnerability:** Found a Stored XSS vulnerability where Jekyll templates directly interpolated variables (like `{{ paper.title }}`) into HTML attributes (`data-en="... "`, `data-zh="..."`) and element text contents without properly escaping them.
**Learning:** By default, Jekyll's Liquid templating engine does not HTML-escape output variables unless explicitly requested. If malicious payload (e.g., `<script>alert(1)</script>` or `"><img src=x onerror=alert(1)>`) is injected into the markdown front matter, it will be rendered verbatim, leading to Cross-Site Scripting (XSS).
**Prevention:** Always append the `| escape` filter (e.g., `{{ variable | escape }}`) whenever injecting dynamic content into HTML, especially within attributes where unescaped double quotes can break out of the string boundary.
## 2025-05-15 - [DOM-based XSS in Mermaid SVG Rendering]
**Vulnerability:** Found a DOM-based XSS vulnerability in `_layouts/default.html` where Mermaid dynamically generated SVG content was directly assigned to `mermaidRoadmap.innerHTML` and a cache object.
**Learning:** Even though Mermaid has a `securityLevel: 'strict'` configuration which runs labels through DOMPurify, it is safer to run the *entire* generated SVG string through `DOMPurify.sanitize()` prior to setting `innerHTML`. This provides an additional layer of defense against XSS that could be introduced by bypasses in Mermaid's internal sanitization or maliciously crafted code that escapes label boundaries.
**Prevention:** Always use `DOMPurify.sanitize()` on generated HTML or SVG strings from third-party libraries before assigning them to `innerHTML`, even if the library claims to perform its own sanitization.

## 2025-05-18 - HTML Attribute Injection in Jekyll Templates
**Vulnerability:** Found a vulnerability in `index.html` where dynamically generated file URLs (like `paper.url` and `page.url`) were injected into `href` attributes without HTML escaping (e.g., `href="{{ site.baseurl }}{{ paper.url }}"`).
**Learning:** If a paper's file path contains quote characters (`"` or `'`), injecting it unescaped into an HTML attribute allows an attacker to break out of the attribute context and inject arbitrary HTML attributes or events, leading to Cross-Site Scripting (XSS).
**Prevention:** Always append the `| escape` filter when injecting dynamic content, including URLs and paths generated from filenames, into HTML attributes in Jekyll templates.

## 2025-05-20 - [Fail-open XSS in Client-Side Sanitization]
**Vulnerability:** Found a fail-open XSS vulnerability where client-side JavaScript (in `assets/js/mermaid-config.js`, `assets/js/mermaid-zoom.js`, and `_layouts/default.html`) conditionally used `DOMPurify` to sanitize HTML/SVG, but fell back to returning/using the raw, unsanitized string if `DOMPurify` was not loaded or undefined.
**Learning:** If a critical security dependency like `DOMPurify` fails to load (e.g., due to network issues, ad blockers, or CDN unavailability), a "fail-open" logic path that uses the raw input completely bypasses the intended security controls. This allows any underlying XSS payload to be executed.
**Prevention:** Always design security controls to "fail-closed." If a required sanitization library is unavailable, the application should return a safe default (like an empty string) or throw an error, rather than processing potentially malicious data unsanitized.

## 2025-05-28 - [Stored XSS in Jekyll JSON serialization]
**Vulnerability:** Found a Stored XSS vulnerability in `_layouts/paper.html` where Jekyll's `jsonify` filter was used inside a `<script type="application/json">` block without additional escaping for HTML characters.
**Learning:** The Jekyll `jsonify` filter converts data objects to valid JSON, but it does NOT escape HTML characters (like `<`, `>`, or `&`) inside the JSON string values. When this JSON is placed inside a `<script>` tag in the DOM, an attacker can embed `</script><script>alert(1)</script>` within a data field (like a paper title), breaking out of the original script block and executing arbitrary JavaScript on the page before the data is even read.
**Prevention:** When injecting JSON data directly into an HTML template using `jsonify`, always chain `| replace: '<', '\u003c' | replace: '>', '\u003e' | replace: '&', '\u0026'` to ensure any embedded HTML tags are safely converted into Unicode escape sequences, which preserves the JSON format but neutralizes the XSS vector.
## 2025-05-30 - [DOM Clobbering in JSON Parsing]
**Vulnerability:** Found a DOM Clobbering vulnerability in `assets/js/paper.js` where `initPaperNav()` relied on `document.getElementById('paper-nav-data')` to retrieve a trusted JSON `<script>` block.
**Learning:** If a user injects an arbitrary element like `<div id="paper-nav-data">{"malicious": "payload"}</div>` into the markdown body, it appears in the DOM before the legitimate `<script>` block at the bottom of the page. `getElementById` returns the first matching element, allowing an attacker to hijack the navigation data object, which can lead to Stored XSS via `javascript:` URLs in the "prev" or "next" links.
**Prevention:** To prevent DOM Clobbering attacks where maliciously injected HTML elements hijack element lookups, avoid using generic `document.getElementById('id')` when retrieving expected configuration scripts. Instead, use specific tag selectors like `document.querySelector('script#id')` to ensure the correct element type is retrieved.

## 2025-05-31 - [DOM Clobbering in JSON Parsing / Stored XSS in JSON]
**Vulnerability:** Found a DOM Clobbering vulnerability in `_layouts/default.html` where `attachRoadmapNodeLinks()` relied on `document.getElementById('roadmap-node-links')` to retrieve a trusted JSON `<script>` block. Also found a Stored XSS vector in `index.html` where `site.data.roadmap_links` was passed to `jsonify` but not escaped.
**Learning:** If a user injects `<div id="roadmap-node-links">{"malicious": "payload"}</div>` into the markdown, `getElementById` fetches it before the actual script tag, hijacking navigation. Meanwhile, `jsonify` outputs raw `<` and `>`, allowing escaping the `<script>` tag.
**Prevention:** Use `document.querySelector('script#roadmap-node-links')` instead of `getElementById` for configuration scripts. Append `| replace: '<', '\u003c' | replace: '>', '\u003e' | replace: '&', '\u0026'` to `jsonify` inside script tags.
