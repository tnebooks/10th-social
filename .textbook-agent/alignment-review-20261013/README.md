# Content alignment review — 13 October 2026

The theme's global `list-style-position: inside !important` rule put bullets
and numbers on a separate line above paragraph-based Markdown list items.
The English first-history lesson reproduced the reported defect: all 72
tested paragraph items started 24 pixels below their list item.

The repository now loads `assets/css/textbook-content.css` through the theme's
existing `stylesheets-docs` hook. Article lists use outside markers and hanging
indentation, with consistent spacing between items. Navigation and contents
lists are outside the override's scope. The shared external theme was not edited.

All 110 English and Tamil content Markdown files and their generated articles
were checked. In 44 lesson files, 397 lines containing detached options,
substatements, bibliography continuations or numbered-item continuations were
indented beneath their existing parent items. Every edit preserves the original
line text and order after removing leading whitespace. The five English treaty
continuations were additionally checked against the image of PDF page 14.
Ambiguous body sidebars and separate exercise instructions were left separate.

Verification:

- Hugo built both languages successfully. Existing theme/config deprecation warnings remain.
- All 110 articles load the new stylesheet.
- No empty list items, malformed list children, accidental code blocks or inconsistent table column counts were found.
- All 257 rendered tables and all article image counts are preserved.
- Wording, numbering, units, front matter, source-view blocks and supplemental resource blocks are unchanged.
- Browser geometry checks passed for all 54 lessons and 3,246 paragraph-based list items, with no detached markers.
- The reported first-history objectives were also checked visually in the narrow local preview; see `preview.jpg`.
- `git diff --check` passed.

`before.json` and `after.json` record the per-file structure checks and SHA256
hashes. The two indentation proposal files record exact, hash-checked edits.
`browser-verification.json` and `verification.json` record the final checks.

This review verifies layout and Markdown structure. It does not grant a new
complete semantic textbook approval. Teacher approval is **false**.
