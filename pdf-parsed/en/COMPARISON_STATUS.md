# PDF vs content.en — Comparison Status

Source: `Class_10_Social_Science_English_2025_Edition` (344 pages, 27 units). The per-unit parsed Markdown is in this folder.

- **Missing (start):** PDF sentences not found in `content.en` before any changes.
- **Layout-only:** sentences still not matched word-for-word only because the PDF stores a caption or map label in the same text block as body text, or because the line is a running page header. Every word is present in the chapter.
- **Truly missing:** sentences with words absent from the chapter, ignoring page numbers and PDF glyph errors such as "Interna onal".

| # | Chapter | PDF sentences | Missing (start) | Layout-only | Truly missing |
|---|---|---|---|---|---|
| 1 | outbreak-of-world-war-i-and-its-aftermath | 475 | 7 | 0 | 0 |
| 2 | the-world-between-two-world-wars | 328 | 8 | 1 | 0 |
| 3 | world-war-ii | 304 | 6 | 1 | 0 |
| 4 | the-world-after-world-war-ii | 432 | 8 | 0 | 0 |
| 5 | social-and-religious-reform-movements-in-the-19th-century | 258 | 4 | 0 | 0 |
| 6 | early-revolts-against-british-rule-in-tamil-nadu | 327 | 8 | 0 | 0 |
| 7 | anti-colonial-movements-and-the-birth-of-nationalism | 371 | 7 | 1 | 0 |
| 8 | nationalism-gandhian-phase | 472 | 9 | 1 | 0 |
| 9 | freedom-struggle-in-tamil-nadu | 292 | 9 | 1 | 0 |
| 10 | social-transformation-in-tamil-nadu | 327 | 4 | 0 | 0 |
| 11 | india-location-relief-and-drainage | 425 | 4 | 2 | 0 |
| 12 | climate-and-natural-vegetation-of-india | 256 | 5 | 4 | 0 |
| 13 | india-agriculture | 377 | 25 | 0 | 0 |
| 14 | india-resources-and-industries | 371 | 21 | 0 | 0 |
| 15 | india-population-transport-communication-and-trade | 376 | 39 | 17 | 0 |
| 16 | physical-geography-of-tamil-nadu | 472 | 15 | 1 | 0 |
| 17 | human-geography-of-tamil-nadu | 455 | 12 | 0 | 0 |
| 18 | indian-constitution | 264 | 34 | 0 | 0 |
| 19 | central-government | 286 | 3 | 0 | 0 |
| 20 | state-government | 246 | 0 | 0 | 0 |
| 21 | indias-foreign-policy | 223 | 4 | 0 | 0 |
| 22 | indias-international-relations | 317 | 7 | 1 | 0 |
| 23 | gross-domestic-product-and-its-growth-an-introduction | 255 | 5 | 0 | 0 |
| 24 | globalization-and-trade | 207 | 8 | 1 | 0 |
| 25 | food-security-and-nutrition | 224 | 7 | 2 | 0 |
| 26 | government-and-taxes | 200 | 19 | 0 | 0 |
| 27 | industrial-clusters-in-tamil-nadu | 251 | 2 | 2 | 0 |

**Total:** 8791 sentences. Missing at start: 280. Truly missing now: 0.

## Pass 1: missing body content

- `outbreak-of-world-war-i-and-its-aftermath`: GLOSSARY (9 terms)
- `the-world-between-two-world-wars`: GLOSSARY (9 terms)
- `world-war-ii`: GLOSSARY (13 terms)
- `the-world-after-world-war-ii`: GLOSSARY (8 terms)
- `social-and-religious-reform-movements-in-the-19th-century`: GLOSSARY (7 terms)
- `early-revolts-against-british-rule-in-tamil-nadu`: GLOSSARY (12 terms)
- `anti-colonial-movements-and-the-birth-of-nationalism`: GLOSSARY (9 terms)
- `nationalism-gandhian-phase`: GLOSSARY (10 terms)
- `freedom-struggle-in-tamil-nadu`: GLOSSARY (11 terms)
- `social-transformation-in-tamil-nadu`: GLOSSARY (12 terms)
- `indian-constitution`: GLOSSARY (8 terms)
- `indias-foreign-policy`: GLOSSARY (5 terms)
- `indias-international-relations`: GLOSSARY (7 terms)
- `food-security-and-nutrition`: GLOSSARY (9 terms)
- `government-and-taxes`: GLOSSARY (8 terms)
- `central-government`: GLOSSARY repaired (terms column was missing)
- `gross-domestic-product-and-its-growth-an-introduction`: SUMMARY + GLOSSARY repaired (were mangled into a table)
- `social-transformation-in-tamil-nadu`: Reference book #3 re-ordered
- `india-location-relief-and-drainage`: Activity box "Find out the following"
- `india-agriculture`: Multipurpose projects table + PMKSY box
- `india-agriculture`: Shifting agriculture names table
- `india-agriculture`: Cropping seasons table
- `india-agriculture`: Agricultural revolutions table
- `india-resources-and-industries`: Iron ore forms table
- `india-resources-and-industries`: Coal India Limited box
- `india-resources-and-industries`: CSTRI box
- `india-resources-and-industries`: Iron & steel plants table
- `india-population-transport-communication-and-trade`: Railway zones table
- `physical-geography-of-tamil-nadu`: Western Ghats peaks table
- `physical-geography-of-tamil-nadu`: Eastern Ghats peaks + Major hills tables
- `physical-geography-of-tamil-nadu`: Waterfalls table
- `physical-geography-of-tamil-nadu`: Seasons table
- `human-geography-of-tamil-nadu`: TN cropping seasons table
- `human-geography-of-tamil-nadu`: Aavin box
- `human-geography-of-tamil-nadu`: Water resources table
- `human-geography-of-tamil-nadu`: GI Tag box + table
- `indian-constitution`: FR vs DPSP table
- `indian-constitution`: Fundamental Rights article list (I–V)
- `central-government`: Parliament session table
- `indias-international-relations`: Typo fix "Tahiland" -> "Thailand" (3x)
- `gross-domestic-product-and-its-growth-an-introduction`: Sector-wise GDP share table
- `gross-domestic-product-and-its-growth-an-introduction`: HDI box
- `globalization-and-trade`: Indian MNCs table
- `globalization-and-trade`: WTO fact box
- `food-security-and-nutrition`: Top/Bottom MPI districts table
- `government-and-taxes`: Corporate tax rates table
- `government-and-taxes`: Tax vs Fee table
- `human-geography-of-tamil-nadu`: Farming types table
- `indian-constitution`: Stamps activity question

## Pass 2: figures, captions and text fixes

- `the-world-between-two-world-wars`: Re-joined sentence "In 1929 the Vietnamese soldiers mutinied…" split by the Ho Chi Minh box
- `world-war-ii`: Re-joined Guadalcanal sentence
- `nationalism-gandhian-phase`: Re-joined Round Table sentence; caption separated
- `freedom-struggle-in-tamil-nadu`: Captions paired with their photos (Raja of Panagal / A Subbarayalu)
- `world-war-ii`: Map: WWII Axis vs Allied powers
- `anti-colonial-movements-and-the-birth-of-nationalism`: Map: Centres of the Great Rebellion 1857
- `india-location-relief-and-drainage`: Map: India states & UTs
- `india-location-relief-and-drainage`: Map: India physical divisions
- `climate-and-natural-vegetation-of-india`: Monsoon map captions (were merged into a heading)
- `climate-and-natural-vegetation-of-india`: Map: Biosphere reserves & wildlife sanctuaries
- `india-resources-and-industries`: Map: Major industries in India
- `india-resources-and-industries`: Diagram: Challenges of Indian Industries
- `india-population-transport-communication-and-trade`: Chart → table: decadal population growth 1901–2011
- `india-population-transport-communication-and-trade`: Map: Air & sea routes
- `physical-geography-of-tamil-nadu`: Map: Location of Tamil Nadu
- `physical-geography-of-tamil-nadu`: Typo "Teh Nilgiri"
- `physical-geography-of-tamil-nadu`: Map: TN wildlife & bird sanctuaries
- `human-geography-of-tamil-nadu`: Map: TN multipurpose projects
- `indias-international-relations`: Map: Neighbouring countries
- `globalization-and-trade`: Diagram: History of Globalization stages
- `food-security-and-nutrition`: Chart → table: largest economies by PPP (replaced scattered axis numbers)
- `government-and-taxes`: Figure → table: Progressive / Proportional / Regressive
- `industrial-clusters-in-tamil-nadu`: Map → table: Industrial clusters in Tamil Nadu
- `india-agriculture`: PDF-ligature typos fixed (Cofefe/Teh/Tehir/Difefr…)
