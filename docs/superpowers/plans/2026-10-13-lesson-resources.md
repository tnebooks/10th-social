# Lesson resources and activities implementation plan

> Execution: use superpowers:executing-plans inline in this shared checkout. The user authorized both panel repairs and new lesson activities.

**Goal:** Make references, videos and learning activities accessible in every English and Tamil lesson.

**Architecture:** Store a bilingual resource catalogue in Hugo data, derived from the existing audited resource records and printed bibliography text. Repository-local partials populate the existing reference/video panels and add a visible lesson activity entry point. Local JavaScript provides guided topic review for every lesson and source-backed climate, GDP and GST calculators.

**Tech stack:** Hugo templates, JSON, plain browser JavaScript, Python structural verification and Node arithmetic tests. No new dependencies or shared-theme edits.

**Constraints:** Preserve every existing textbook Markdown file and asset, including the preceding alignment repairs. Preserve external-resource language and verification limitations. Quotes and formulas come only from the supplied textbooks. Activities supplement source text; teacher approval remains false. Do not store or transmit student responses.

**Review focus:** Missing lesson metadata must show a useful fallback; Tamil controls must be localized; source topics and references must remain in order; invalid calculator values must not produce misleading results; video controls must retain a usable external link when embedding fails.

- [x] Reproduce empty resource panels and write all-54-lesson coverage checks before implementation.
- [x] Generate bilingual catalogue with printed bibliography, original-page links, existing videos/activities, topic anchors and provenance hashes.
- [x] Add repository-local reference/book/video partials and accessible resource shortcuts.
- [x] Add guided recall/review controls for all 180 topics in each language; reveal complete source sections rather than invented answers.
- [x] Verify three calculator formulas against English and Tamil page images, write failing arithmetic/input tests, then implement climate lapse rate, expenditure GDP and textbook GST examples with source citations and fictional inputs.
- [x] Build both languages, run all structural/arithmetic checks and verify panels, review controls and calculators in the live browser, including narrow screens. Save screenshots and a coverage report.
