# Lesson resource panels and activities — 13 October 2026

The existing theme displayed empty References and Videos panels because it read
front-matter resource fields, while the researched links were present only in
the lesson Markdown. Repository-local partials now populate those panels from
`data/lesson_resources.json`, generated with `scripts/build-lesson-resources.py`.

All 27 English and 27 Tamil lessons now provide visible References, Videos and
Activities shortcuts. References include original textbook pages, recorded
source URLs with their check statuses/alternatives, and the printed bibliography.
Videos retain known titles, publishers and honest language labels; playback
remains unverified. Existing topic-specific resource tables remain intact.

Each lesson has a topic recall activity: select a topic, write a draft, compare
with its source section, mark it reviewed, or reset. All 180 topics in each
language are covered. Responses stay in page memory and clear on reload; no
automatic grading or answer transmission is introduced.

Three numerical study models are provided in both languages: normal lapse rate,
expenditure GDP, and textbook GST rates. All six formula/rule sources were checked
against the supplied page images, with source-item IDs and original-page links.
See `simulation-source-items.json`. Inputs are explicitly fictional study values
and the GST model uses the 2025 textbook's rates. These are supplemental models,
not changes to the textbook and not current tax guidance.

Verification:

- Both Hugo language builds pass, with existing configuration/theme deprecation warnings.
- Five Node arithmetic/input/overflow tests pass.
- Two Python tests pass across all 54 lessons and all 54 original-page galleries.
- Browser checks passed on all 54 lesson pages: 372 video references, 360 topic controls, valid source targets, populated panels and initialized activities.
- All six calculator instances were exercised with changed inputs: 28.5°C, GDP ₹140 crore with net exports −₹30 crore, and GST ₹100 / total ₹2,100.
- Topic draft restoration, review progress and reset were exercised in the browser.
- Keyboard comparison moves focus to the source heading; Back restores the activity and its heading focus. New shortcuts avoid the shared theme's interrupted smooth-scroll behavior.
- The visible narrow preview was inspected for References, Videos and the Tamil GST model; screenshots are in this directory.
- All 1,787 content files/assets match the starting SHA256 snapshot, preserving the preceding alignment repairs.
- `git diff --check` passes. The external shared theme is unchanged.

Independent review identified arithmetic overflow, missing reference status
labels, and keyboard focus handling. These findings were fixed and verified.

Run verification after building:

```sh
python3 scripts/build-lesson-resources.py
hugo --destination /private/tmp/10th-social-resource-build --baseURL http://127.0.0.1:1313/10th-social/
python3 -m unittest discover -s tests -p 'test_*.py'
node --test tests/lesson-calculators.test.cjs
```

Teacher approval remains **false**. This is a resource/UI review, not a new
complete semantic or character-level textbook review.
