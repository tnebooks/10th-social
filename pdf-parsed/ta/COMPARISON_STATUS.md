# Tamil PDF vs content.ta: Comparison Status

Source: `Class_10_Social_Science_Tamil_2025_Edition` (368 pages, 27 units). The per-unit parsed Markdown is in this folder.

| # | Chapter | PDF sentences | Missing before | Missing after | Action | Images |
|---|---|---|---|---|---|---|
| 1 | outbreak-of-world-war-i-and-its-aftermath | 492 | 78 (16%) | 0 | Rebuilt from PDF | 16 |
| 2 | the-world-between-two-world-wars | 353 | 64 (18%) | 0 | Rebuilt from PDF | 15 |
| 3 | world-war-ii | 372 | 65 (17%) | 0 | Rebuilt from PDF | 18 |
| 4 | the-world-after-world-war-ii | 397 | 54 (14%) | 0 | Rebuilt from PDF | 23 |
| 5 | social-and-religious-reform-movements-in-the-19th-century | 287 | 72 (25%) | 0 | Rebuilt from PDF | 23 |
| 6 | early-revolts-against-british-rule-in-tamil-nadu | 310 | 73 (24%) | 0 | Rebuilt from PDF | 14 |
| 7 | anti-colonial-movements-and-the-birth-of-nationalism | 371 | 92 (25%) | 0 | Rebuilt from PDF | 18 |
| 8 | nationalism-gandhian-phase | 513 | 87 (17%) | 0 | Rebuilt from PDF | 34 |
| 9 | freedom-struggle-in-tamil-nadu | 313 | 71 (23%) | 0 | Rebuilt from PDF | 29 |
| 10 | social-transformation-in-tamil-nadu | 349 | 104 (30%) | 0 | Rebuilt from PDF | 24 |
| 11 | india-location-relief-and-drainage | 405 | 59 (15%) | 23 | Missing passages inserted (existing text unchanged) | 0 |
| 12 | climate-and-natural-vegetation-of-india | 247 | 247 (100%) | 0 | Created (was empty stub) | 8 |
| 13 | india-agriculture | 366 | 366 (100%) | 0 | Created (was empty stub) | 13 |
| 14 | india-resources-and-industries | 359 | 359 (100%) | 0 | Created (was empty stub) | 25 |
| 15 | india-population-transport-communication-and-trade | 370 | 370 (100%) | 0 | Created (was empty stub) | 8 |
| 16 | physical-geography-of-tamil-nadu | 456 | 456 (100%) | 0 | Created (was empty stub) | 17 |
| 17 | human-geography-of-tamil-nadu | 445 | 445 (100%) | 0 | Created (was empty stub) | 14 |
| 18 | indian-constitution | 282 | 282 (100%) | 0 | Created (was empty stub) | 12 |
| 19 | central-government | 335 | 335 (100%) | 0 | Created (was empty stub) | 12 |
| 20 | state-government | 277 | 277 (100%) | 0 | Created (was empty stub) | 8 |
| 21 | indias-foreign-policy | 218 | 218 (100%) | 0 | Created (was empty stub) | 10 |
| 22 | indias-international-relations | 299 | 299 (100%) | 0 | Created (was empty stub) | 17 |
| 23 | gross-domestic-product-and-its-growth-an-introduction | 272 | 272 (100%) | 0 | Created (was empty stub) | 20 |
| 24 | globalization-and-trade | 209 | 209 (100%) | 0 | Created (was empty stub) | 8 |
| 25 | food-security-and-nutrition | 233 | 233 (100%) | 0 | Created (was empty stub) | 15 |
| 26 | government-and-taxes | 228 | 228 (100%) | 0 | Created (was empty stub) | 4 |
| 27 | industrial-clusters-in-tamil-nadu | 270 | 270 (100%) | 0 | Created (was empty stub) | 10 |

**Total:** 9028 sentences. Missing before: 5685 (63%). Missing after: 23 (0.3%).

The 23 sentences still flagged are all in Geography Unit 1 and are present in reworded form. That chapter uses its own text style, with spelled-out units ("கிலோமீட்டர்" instead of "கி.மீ") and image descriptions.

## How the Tamil text was extracted

The PDF's Tamil font gives faulty Unicode when text is extracted. The converter (`tamil.py`) fixes this:

- Junk characters between vowel signs: `கொ�ொ` → `கொ`, `பொHொ` → `பொ`.
- Doubled virama marks and doubled vowel signs: `்்` → `்`, `ாா` → `ா`.
- Phantom duplicate consonants: `பபாகிஸ்தான்` → `பாகிஸ்தான்`, `கககா` → `கா`.
  - Real doubles are kept: `வந்தது`, `இருந்ததால்`, `பேரரசு`, `சமமான`. For `த`, glyph widths in the PDF decide between real and faulty.
- Repeated syllables: `ஜப்பாபான்` → `ஜப்பான்`, `நாநாட்டின்` → `நாட்டின்`. Real repeats are kept: `தாதாபாய்`, `கடலிலிருந்து`.
- Line breaks in the middle of a word are joined. Bullets drawn with the Wingdings font become list items.
- Map labels in pre-Unicode Tamil fonts (Latin-1 junk) are dropped. Vector maps and diagrams are saved as PNG images instead.
- Table cells are read in text-stream order, so vowel signs drawn to the left of a consonant stay in the right place.

Audit of the final output: 0 doubled viramas, 0 doubled vowel signs, 0 replacement characters. The doubled consonants that remain are real words (`தது` verb endings, பேரரசு, சமமான, …).

## Note on the previous History 1–10 text

The previous History chapters were made from this PDF with a cleanup that dropped real letters, e.g. `வந்து` where the book has `வந்தது`. They also kept faults such as `அமெரிக்ககா` and `இரண்டடாம்`, and were missing their exercises and info boxes. As agreed, they were rebuilt from the PDF; their existing title and summary front matter was kept.
