"""Tamil PDF -> Markdown converter with glyph-artifact cleanup."""
import re, pymupdf, os
from collections import Counter

SRC = r'D:/DevOps/TNEbooks/PDF/Class_10_Social_Science_Tamil_2025_Edition-www.tntextbooks.in.pdf'
# PDF start page of each unit (book page + 6); last entry = end sentinel
STARTS = [7, 24, 37, 50, 64, 74, 86, 101, 119, 130, 144, 159, 169, 185, 202, 218, 238,
          259, 269, 281, 291, 300, 315, 327, 336, 346, 354, 365]

TA = '\u0B80-\u0BFF'
CONS = '\u0B95-\u0BB9'
O_SIGNS = '\u0BCA\u0BCB\u0BCC'          # ொ ோ ௌ
JUNK = '\ufffdHEIFKLSA>@'
PULLI = '\u0BCD'
BULLET = '\u2022'

# Real Tamil words that legitimately contain a doubled consonant without virama
KEEP_DOUBLE = ('பேரரச', 'சமம', 'மகரரேகை', 'தொடக்ககால', 'பஞ்சசீல', 'இராணுவவீர', 'ரரீதி', 'சங்ககிரி',
               'சந்ததி', 'லலித', 'மமதா', 'ததும்')
TH = 'த'

def dbl(m):
    """Decide whether a doubled consonant (no virama between) is a PDF artefact."""
    s, i, c = m.string, m.start(), m.group(1)
    for k in KEEP_DOUBLE:
        j = s.find(k, max(0, i - len(k)))
        while 0 <= j <= i:
            if j <= i and i + 1 < j + len(k):
                return m.group(0)
            j = s.find(k, j + 1)
    nxt = s[m.end():m.end() + 1]
    nxt2 = s[m.end() + 1:m.end() + 2]
    prev = s[i - 1:i]
    if c == TH:
        if nxt == 'ு':                                  # தது  (இருந்தது, வந்தது)
            return m.group(0)
        if prev == PULLI and nxt in ('ா', 'ோ', 'ன', 'ி', 'ே'):
            return m.group(0)                                # ந்ததால், த்ததன், ந்ததோடு, ந்ததில், த்ததே
        if prev == PULLI and nxt == 'ை' and nxt2 != 'ய':
            return m.group(0)                                # வந்ததை (but not பிந்தைய)
    return c

WJ = '⁠'   # marks a doubled த that glyph widths showed to be genuine

def raw_line_text(line):
    """Build span texts from rawdict chars, resolving doubled த via glyph widths."""
    chars = [(sp, c) for sp in line['spans'] for c in sp['chars']]
    out = {id(sp): [] for sp in line['spans']}
    for i, (sp, c) in enumerate(chars):
        ch = c['c']
        if ch == TH and i > 0 and chars[i - 1][1]['c'] == TH:
            w1 = chars[i - 1][1]['bbox'][2] - chars[i - 1][1]['bbox'][0]
            w2 = c['bbox'][2] - c['bbox'][0]
            nxt = ''.join(x[1]['c'] for x in chars[i + 1:i + 4])
            if w2 <= 0.01:
                genuine = nxt.startswith(('ோ', 'ால்'))          # ததோடு, ததால்
            else:
                genuine = (nxt.startswith(('ு', 'ை', 'ே', 'ோ'))  # தது ததை ததே ததோ
                           or nxt.startswith(('ால்', 'ாக')))  # ததால் ததாக
                if nxt.startswith('ைய'): genuine = False                   # பிந்தைய
            if not genuine:
                continue                                                           # drop phantom த
            out[id(sp)].append(WJ)
        out[id(sp)].append(ch)
    for sp in line['spans']:
        sp['text'] = ''.join(out[id(sp)])

def clean(s):
    s = re.sub(r'[\x00-\x08\x0b-\x1f]', '', s)
    s = s.replace('\u00ad', '').replace('\u2002', ' ').replace('\ufeff', '')
    s = re.sub(f'([{O_SIGNS}])[{JUNK}]?\\1', r'\1', s)                    # கொ�ொ -> கொ
    s = re.sub(f'([{O_SIGNS}])[{JUNK[:-2]}](?=[{TA}])', r'\1', s)          # stray junk after o-sign
    s = re.sub(f'([{O_SIGNS}])\\1+', r'\1', s)                             # ொொ -> ொ
    s = re.sub(PULLI + '+', PULLI, s)                                      # ்் -> ்
    s = re.sub('([\u0BBE-\u0BC2\u0BC6-\u0BC8])\\1+', r'\1', s)              # ாா -> ா
    s = re.sub(f'([{CONS}])\\1+(?!{PULLI})', dbl, s)                      # ககை / கககா -> கை / கா
    s = re.sub(f'([{CONS}]{PULLI})\\1+', r'\1', s)                         # க்க் -> க்
    s = re.sub(r'[ \t]+', ' ', s)
    s = re.sub(r' *\n *', '\n', s)
    return s.replace(WJ, '').strip()

LEGACY = set(chr(c) for c in range(0xA0, 0x100)) | set('‚ƒ„…†‡ˆ‰Š‹ŒŽ‘’“”–—˜™š›œžŸ')

def is_legacy(t):
    """Map labels in legacy (non-Unicode) Tamil fonts come out as Latin-1 junk."""
    letters = [c for c in t if not c.isspace() and not c.isdigit()]
    if not letters: return False
    junk = sum(1 for c in letters if c in LEGACY)
    return junk / len(letters) > 0.25

def join_lines(lines):
    out = ''
    for ln in lines:
        if not out:
            out = ln; continue
        if ln.startswith('\n'):
            out += ln
        elif out.endswith((' ', '\t')) or ln.startswith(' '):
            out += ln
        elif re.match(r'\s*(?:[அஆஇஈ]\)|\(?[a-dA-D]\)|\d{1,2}[.)]\s|\([ivx]+\))', ln):
            out += ' ' + ln                 # option / numbered item always starts a new token
        elif re.search(f'[{TA}]$', out) and re.match(f'[{TA}]', ln):
            out += ln                       # spurious mid-word break
        else:
            out += ' ' + ln
    return out

def cell_text(page, bbox):
    """Text of a table cell in content-stream order (geometric sorting breaks Tamil vowel signs)."""
    if not bbox: return ''
    r = pymupdf.Rect(bbox)
    key = (page.parent.name, page.number)
    if key not in _RAW_CACHE:
        _RAW_CACHE.clear()
        _RAW_CACHE[key] = page.get_text('rawdict')['blocks']
    lines = []
    for b in _RAW_CACHE[key]:
        if b['type'] != 0 or not pymupdf.Rect(b['bbox']).intersects(r): continue
        for l in b['lines']:
            # keep chars whose glyph centre lies in the cell; zero-width marks follow their base char
            kept_spans, inside = [], False
            for sp in l['spans']:
                cs = []
                for c in sp['chars']:
                    x0, y0, x1, y1 = c['bbox']
                    if x1 - x0 > 0.01:
                        inside = r.contains(pymupdf.Point((x0 + x1) / 2, (y0 + y1) / 2))
                    if inside: cs.append(c)
                if cs: kept_spans.append(dict(sp, chars=cs))
            if not kept_spans: continue
            ln = dict(l, spans=kept_spans)
            raw_line_text(ln)
            t = ''.join(sp['text'] for sp in ln['spans'])
            if t.strip() and not is_legacy(t): lines.append(t)
    return clean(join_lines(lines)).replace('\n', ' ')

_RAW_CACHE = {}

def block_lines(b):
    raw = []
    for l in b['lines']:
        sps = [sp for sp in l['spans'] if sp['text']]
        bullet = False
        while sps and (any(k in sps[0]['font'] for k in ('Wingdings', 'Symbol', 'Dingbat'))
                       or sps[0]['text'].strip() in (BULLET, '')):
            if sps[0]['text'].strip(): bullet = True
            sps = sps[1:]
        t = ''.join(sp['text'] for sp in sps)
        if not t.strip() or is_legacy(t): continue
        raw.append(('\n' + BULLET + ' ' if bullet else '') + t)
    return raw

def page_items(doc, pno, body_size):
    """Return ordered items (y, x, kind, payload) for one page."""
    page = doc[pno]
    H = page.rect.height
    items, tabs = [], []
    try:
        for t in page.find_tables().tables:
            rows = [[cell_text(page, c) for c in row.cells] for row in t.rows]
            rows = [r for r in rows if any(x for x in r)]
            cells = [x for r in rows for x in r if x]
            if not cells or sum(is_legacy(x) for x in cells) / len(cells) > 0.2: continue
            if len(rows) >= 2 and max(len(r) for r in rows) >= 2:
                tabs.append(pymupdf.Rect(t.bbox)); items.append((t.bbox[1], t.bbox[0], 'table', rows))
    except Exception:
        pass
    blocks = [b for b in page.get_text('rawdict')['blocks'] if b['type'] == 0]
    for b in blocks:
        for l in b['lines']:
            raw_line_text(l)
    # vector maps / diagrams: drawing clusters whose text is mostly short labels
    maps = []
    try:
        W_, H_ = page.rect.width, page.rect.height
        drs = [d for d in page.get_drawings() if d['rect'].width < 0.8 * W_ or d['rect'].height < 0.8 * H_]
        clusters = page.cluster_drawings(drawings=drs) if drs else []
    except Exception:
        clusters = []
    for cr in clusters:
        if cr.width < 120 or cr.height < 120 or cr.get_area() > 0.9 * page.rect.get_area(): continue
        if any((cr & tb).get_area() > 0.5 * cr.get_area() for tb in tabs if cr.intersects(tb)): continue
        inside = [b for b in blocks if (pymupdf.Rect(b['bbox']) & cr).get_area() > 0.6 * pymupdf.Rect(b['bbox']).get_area()]
        texts = [''.join(sp['text'] for l in b['lines'] for sp in l['spans']).strip() for b in inside]
        texts = [t for t in texts if t]
        legacy = sum(is_legacy(t) for t in texts)
        avg = sum(len(t) for t in texts) / len(texts) if texts else 0
        if (texts and (legacy >= 2 or (len(texts) >= 4 and avg < 30))) or (not texts and cr.width > 200 and cr.height > 200):
            maps.append(cr); items.append((cr.y0, cr.x0, 'map', cr))
    for b in blocks:
        r = pymupdf.Rect(b['bbox'])
        if any(r.intersects(tb) and (r & tb).get_area() > 0.5 * r.get_area() for tb in tabs): continue
        if any(r.intersects(m) and (r & m).get_area() > 0.6 * r.get_area() for m in maps): continue
        if r.y1 < 60 or r.y0 > H - 45: continue                    # header / footer band
        txt = join_lines(block_lines(b))
        if not txt.strip() or 'indd' in txt or re.fullmatch(r'[\d\s:/\-.APM]+', txt.strip()): continue
        if is_legacy(txt): continue
        sizes = [sp['size'] for l in b['lines'] for sp in l['spans'] if sp['text'].strip()]
        bold = [('Bold' in sp['font'] or sp['flags'] & 16) for l in b['lines'] for sp in l['spans'] if sp['text'].strip()]
        sz = max(sizes) if sizes else body_size
        items.append((r.y0, r.x0, 'text', (clean(txt), sz, all(bold) if bold else False)))
    for info in page.get_image_info(xrefs=True):
        x0, y0, x1, y1 = info['bbox']
        if any(pymupdf.Rect(info['bbox']) in m for m in maps): continue
        if info['xref'] and (x1 - x0) > 40 and (y1 - y0) > 40:
            items.append((y0, x0, 'image', info['xref']))
    mid = page.rect.width / 2
    items.sort(key=lambda it: (1 if it[1] >= mid - 15 else 0, it[0]))
    return items

def body_font_size(doc, pages):
    c = Counter()
    for p in pages:
        for b in doc[p].get_text('dict')['blocks']:
            for l in b.get('lines', []):
                for sp in l['spans']:
                    if sp['text'].strip(): c[round(sp['size'], 1)] += len(sp['text'])
    return c.most_common(1)[0][0]

def table_md(rows):
    n = max(len(r) for r in rows)
    rows = [[(c or '').replace('|', '/').replace('\n', ' ') for c in r] + [''] * (n - len(r)) for r in rows]
    out = ['| ' + ' | '.join(rows[0]) + ' |', '|' + '---|' * n]
    out += ['| ' + ' | '.join(r) + ' |' for r in rows[1:]]
    return '\n'.join(out)

ROMAN = r'(?:I|II|III|IV|V|VI|VII|VIII|IX|X|XI)'

def tamil_len(s): return len(re.findall(f'[{TA}A-Za-z]', s))

def split_exercise(p):
    """'I சரியான விடை… 1. q… 2. q…' -> bold section label + numbered lines."""
    out = []
    m = re.match(rf'^({ROMAN})[\s.)]+(.*)$', p)
    if m:
        rest = m.group(2)
        k = re.search(r'\s(?=1\.\s)', ' ' + rest)
        label, rest = (rest[:k.start() - 1], rest[k.start():]) if k else (rest, '')
        out.append(f'**{m.group(1)} {label.strip()}**')
        p = rest.strip()
        if not p: return out
    if re.match(r'^\d{1,2}\.\s', p) or out:
        parts = re.split(r'\s+(?=\d{1,2}\.\s)', p)
        out += [x.strip() for x in parts if x.strip()]
    else:
        out.append(p)
    return out

def convert_unit(doc, u, assets_dir=None, min_img=60):
    pages = list(range(STARTS[u] - 1, STARTS[u + 1] - 1))
    body = body_font_size(doc, pages)
    per_page = [page_items(doc, p, body) for p in pages]
    # running headers: identical (digit-stripped) short texts that repeat on >= 3 pages
    rep = Counter()
    for items in per_page:
        seen = set()
        for it in items:
            if it[2] == 'text':
                k = re.sub(r'[\d\s]+', '', it[3][0])
                if len(k) < 120: seen.add(k)
        rep.update(seen)
    running = {k for k, v in rep.items() if v >= 3 and k}
    md = []
    for i, items in enumerate(per_page):
        pic = 0
        for y, x, kind, val in items:
            if kind == 'table':
                md.append(table_md(val))
            elif kind == 'map':
                if assets_dir is None: continue
                pic += 1
                name = f'page_{i + 1:03d}_picture_{pic:03d}.png'
                os.makedirs(assets_dir, exist_ok=True)
                doc[pages[i]].get_pixmap(clip=val, dpi=150).save(os.path.join(assets_dir, name))
                md.append(f'![](assets/{name})')
            elif kind == 'image':
                if assets_dir is None: continue
                try:
                    pix = pymupdf.Pixmap(doc, val)
                    if pix.width < min_img or pix.height < min_img: continue
                    if pix.n - pix.alpha >= 4: pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
                    if pix.alpha: pix = pymupdf.Pixmap(pix, 0)
                    pic += 1
                    name = f'page_{i + 1:03d}_picture_{pic:03d}.png'
                    os.makedirs(assets_dir, exist_ok=True)
                    pix.save(os.path.join(assets_dir, name))
                    md.append(f'![](assets/{name})')
                except Exception:
                    continue
            else:
                txt, sz, bold = val
                if re.sub(r'[\d\s]+', '', txt) in running: continue
                if tamil_len(txt) < 3: continue
                pieces = [x.strip() for x in txt.split('\n' + BULLET) if x.strip()]
                if txt.startswith(BULLET): pieces = [x.strip() for x in txt.split(BULLET) if x.strip()]
                is_list = txt.startswith(BULLET) or len(pieces) > 1
                for j, pc in enumerate(pieces):
                    pc = pc.replace('\n', ' ')
                    if is_list and (j > 0 or txt.startswith(BULLET)):
                        md.append('- ' + pc); continue
                    n = len(pc)
                    if sz >= body + 3 and n < 90 and tamil_len(pc) >= 3:
                        md.append('## ' + pc)
                    elif (sz >= body + 0.8 or bold) and n < 80 and not pc.endswith(('.', ':', '?')) \
                            and tamil_len(pc) >= 3 and not re.match(r'^\d{1,2}\.\s', pc):
                        md.append('### ' + pc)
                    else:
                        md.append(pc)
    # merge paragraphs split across columns/pages
    merged = []
    for blk in md:
        if (merged and not blk.startswith(('#', '|', '!', '- ', '**')) and not merged[-1].startswith(('#', '|', '!', '**'))
                and not re.search(r'[.?!:;)\]”"]$', merged[-1]) and re.match(f'[{TA}a-z]', blk)):
            merged[-1] = merged[-1] + ' ' + blk
        else:
            merged.append(blk)
    final = []
    in_ex = False
    for blk in merged:
        if blk.startswith('#') and re.search('பயிற்சி|மதிப்பீடு', blk): in_ex = True
        if in_ex and not blk.startswith(('#', '|', '!', '- ')):
            final += split_exercise(blk)
        else:
            final.append(blk)
    return fix_repeats('\n\n'.join(final) + '\n', vocab(doc))

# ---------------------------------------------------------------- dictionary vote for repeated syllables
_VOCAB = None
# words with a genuinely repeated syllable (names, -இலிருந்து after -இல், பதவி+விலக, …)
NAMES = ('பிபின்', 'தாதாபா', 'கோகோ', 'சந்தாதார', 'லிலிருந்', 'பதவிவில', 'பாபாராம்')
WHOLE_NAMES = {'லாலா', 'பாபா', 'டுடு'}
SYL = re.compile(r'([\u0B95-\u0BB9])([\u0BBE-\u0BC2\u0BC6-\u0BC8])\1\2')

def vocab(doc):
    global _VOCAB
    if _VOCAB is None:
        txt = clean(' '.join(join_lines(p.get_text().split('\n')) for p in doc))
        _VOCAB = Counter(re.findall('[\u0B80-\u0BFF]+', txt))
    return _VOCAB

def fix_repeats(text, V):
    def fix_word(m):
        w = m.group(0)
        if not SYL.search(w) or any(n in w for n in NAMES) or w in WHOLE_NAMES: return w
        return SYL.sub(lambda k: k.group(1) + k.group(2), w)
    text = re.sub('[\u0B80-\u0BFF]+', fix_word, text)
    return fix_th(text, V)

WORD_FIXES = {'\u0BAA\u0BC2\u0BB2\u0BBF\u0BA4\u0BCD\u0BA4\u0BA4\u0BC7\u0BB5': '\u0BAA\u0BC2\u0BB2\u0BBF\u0BA4\u0BCD\u0BA4\u0BC7\u0BB5', '\u0BAA\u0BC2\u0BB2\u0BBF\u0BA4\u0BCD\u0BA4\u0BA4\u0BC7': '\u0BAA\u0BC2\u0BB2\u0BBF\u0BA4\u0BCD\u0BA4\u0BC7\u0BB5', '\u0B95\u0BC1\u0BB4\u0BA8\u0BCD\u0BA4\u0BA4\u0BC8': '\u0B95\u0BC1\u0BB4\u0BA8\u0BCD\u0BA4\u0BC8', '\u0B9A\u0BA8\u0BCD\u0BA4\u0BA4\u0BC8': '\u0B9A\u0BA8\u0BCD\u0BA4\u0BC8',
              '\u0B95\u0BB0\u0BC1\u0BA4\u0BCD\u0BA4\u0BA4\u0BC8': '\u0B95\u0BB0\u0BC1\u0BA4\u0BCD\u0BA4\u0BC8', '\u0BB5\u0B9F\u0BCD\u0B9F\u0BAE\u0BC7\u0B9A\u0BC8\u0B9A\u0BC8': '\u0BB5\u0B9F\u0BCD\u0B9F\u0BAE\u0BC7\u0B9A\u0BC8', '\u0BAE\u0BC7\u0B9A\u0BC8\u0B9A\u0BC8': '\u0BAE\u0BC7\u0B9A\u0BC8',
              '\u0B90\u0BB0\u0BCB\u0BAA\u0BCD\u0BAA\u0BBE\u0BAA\u0BBE': '\u0B90\u0BB0\u0BCB\u0BAA\u0BCD\u0BAA\u0BBE', '\u0B9C\u0BAA\u0BCD\u0BAA\u0BBE\u0BAA\u0BBE\u0BA9': '\u0B9C\u0BAA\u0BCD\u0BAA\u0BBE\u0BA9', '\u0B9A\u0BAE\u0BAE\u0BAF\u0BAE': '\u0B9A\u0BAE\u0BAF\u0BAE', '\u0B9A\u0BAE\u0BAE\u0BAF\u0BA4\u0BCD': '\u0B9A\u0BAE\u0BAF\u0BA4\u0BCD',
              '\u0BAE\u0BCB\u0B9A\u0BAE\u0BAE\u0BBE': '\u0BAE\u0BCB\u0B9A\u0BAE\u0BBE', '\u0BAA\u0BBF\u0BB0\u0BA4\u0BAE\u0BAE\u0BA8\u0BCD': '\u0BAA\u0BBF\u0BB0\u0BA4\u0BAE\u0BA8\u0BCD', '\u0BAA\u0BC2\u0BB0\u0BCD\u0BB7\u0BCD\u0BB5\u0BBE\u0BB5\u0BBE': '\u0BAA\u0BC2\u0BB0\u0BCD\u0BB7\u0BCD\u0BB5\u0BBE',
              '\u0B95\u0BBE\u0B95\u0BBE\u0B9F\u0BCD': '\u0B95\u0BBE\u0B9F\u0BCD', '\u0B95\u0BBE\u0B95\u0BBE\u0BAE\u0BBE': '\u0B95\u0BBE\u0BAE\u0BBE', '\u0B95\u0BC0\u0BB4\u0BCD\u0B95\u0BCD\u0B95\u0BBE\u0B95\u0BBE\u0BA3\u0BCD': '\u0B95\u0BC0\u0BB4\u0BCD\u0B95\u0BCD\u0B95\u0BBE\u0BA3\u0BCD', '\u0B85\u0BB5\u0BCD\u0BB5\u0BBE\u0BB5\u0BBE\u0BB1\u0BC1': '\u0B85\u0BB5\u0BCD\u0BB5\u0BBE\u0BB1\u0BC1',
              '\u0B9A\u0BB0\u0BCD\u0B95\u0BCD\u0B95\u0BBE\u0B95\u0BBE\u0BB0\u0BBF\u0BAF\u0BBE': '\u0B9A\u0BB0\u0BCD\u0B95\u0BCD\u0B95\u0BBE\u0BB0\u0BBF\u0BAF\u0BBE', '\u0B85\u0BA9\u0BA8\u0BCD\u0BA4\u0BBE\u0BA4\u0BBE\u0B9A\u0BCD\u0B9A\u0BBE\u0BB0\u0BCD\u0BB2\u0BC1': '\u0B85\u0BA9\u0BA8\u0BCD\u0BA4\u0BBE\u0B9A\u0BCD\u0B9A\u0BBE\u0BB0\u0BCD\u0BB2\u0BC1',
              '\u0B87\u0BB0\u0BBE\u0B9C\u0BB8\u0BCD\u0BA4\u0BA4\u0BBE': '\u0B87\u0BB0\u0BBE\u0B9C\u0BB8\u0BCD\u0BA4\u0BBE', '\u0BAE\u0BC0\u0BA4\u0BCD\u0BA4\u0BA4\u0BC7\u0BA9\u0BCD': '\u0BAE\u0BC0\u0BA4\u0BCD\u0BA4\u0BC7\u0BA9\u0BCD', '\u0B9A\u0BAE\u0BAE\u0BA4\u0BCD\u0BA4\u0BC1\u0BB5': '\u0B9A\u0BAE\u0BA4\u0BCD\u0BA4\u0BC1\u0BB5', '\u0B9A\u0BAE\u0BAE\u0BA8\u0BBF\u0BB2\u0BC8': '\u0B9A\u0BAE\u0BA8\u0BBF\u0BB2\u0BC8',
              '\u0B9A\u0BAE\u0BAE\u0BBE\u0BA4\u0BBE\u0BA9': '\u0B9A\u0BAE\u0BBE\u0BA4\u0BBE\u0BA9', '\u0B9A\u0BAE\u0BAE\u0B89\u0BB0\u0BBF\u0BAE\u0BC8': '\u0B9A\u0BAE \u0B89\u0BB0\u0BBF\u0BAE\u0BC8', '\u0BAA\u0BCB\u0BB0\u0BCD\u0BA4\u0BCD\u0BA4\u0BA4\u0BC7\u0BB5\u0BC8': '\u0BAA\u0BCB\u0BB0\u0BCD\u0BA4\u0BCD\u0BA4\u0BC7\u0BB5\u0BC8',
              '\u0BAA\u0BC7\u0B9A\u0BCD\u0B9A\u0BC1\u0BB5\u0BBE\u0BB0\u0BCD\u0BA4\u0BCD\u0BA4\u0BA4\u0BC8': '\u0BAA\u0BC7\u0B9A\u0BCD\u0B9A\u0BC1\u0BB5\u0BBE\u0BB0\u0BCD\u0BA4\u0BCD\u0BA4\u0BC8', '\u0B9A\u0BBE\u0BB0\u0BCD\u0BA8\u0BA8\u0BCD\u0BA4\u0BA4\u0BCB\u0BA4\u0BCB\u0BB0\u0BCD': '\u0B9A\u0BBE\u0BB0\u0BCD\u0BA8\u0BCD\u0BA4\u0BCB\u0BB0\u0BCD', '\u0B85\u0BAE\u0BC8\u0BA8\u0BCD\u0BA4\u0BCD\u0BA4\u0BA4\u0BBE\u0BB2\u0BCD': '\u0B85\u0BAE\u0BC8\u0BA8\u0BCD\u0BA4\u0BA4\u0BBE\u0BB2\u0BCD',
              '\u0BB5\u0BBE\u0BAF\u0BCD\u0BA8\u0BCD\u0BA4\u0BCD\u0BA4\u0BA4\u0BBE\u0B95': '\u0BB5\u0BBE\u0BAF\u0BCD\u0BA8\u0BCD\u0BA4\u0BA4\u0BBE\u0B95', '\u0BA4\u0BCA\u0BCA\u0B9F\u0BC1\u0BA4\u0BCD\u0BA4\u0BA4\u0BC8': '\u0BA4\u0BCA\u0B9F\u0BC1\u0BA4\u0BCD\u0BA4\u0BA4\u0BC8'}

def fix_th(text, V):
    """Second-pass decisions for doubled \u0BA4 that glyph widths could not settle."""
    for a, b in WORD_FIXES.items():
        text = text.replace(a, b)
    def fw(m):
        w = m.group(0)
        # noun accusative/instrumental: stem+\u0BAE\u0BCD is a known noun (\u0BAA\u0BCA\u0BB0\u0BC1\u0BB3\u0BBE\u0BA4\u0BBE\u0BB0\u0BAE\u0BCD -> \u0BAA\u0BCA\u0BB0\u0BC1\u0BB3\u0BBE\u0BA4\u0BBE\u0BB0\u0BA4\u0BCD\u0BA4\u0BC8)
        k = re.search('\u0BA4\u0BCD\u0BA4\u0BA4(?=\u0BC8|\u0BBE\u0BB2\u0BCD)', w)
        if k and (V.get(w[:k.start()] + '\u0BAE\u0BCD', 0) >= 1
                  or (k.start() > 0 and '\u0B95' <= w[k.start() - 1] <= '\u0BB9')):
            w = w[:k.start() + 2] + w[k.start() + 3:]
        # \u0BA4\u0BA4\u0BBE\u0BB2\u0BCD not preceded by virama is never a past-tense verb form (\u0B87\u0BB0\u0BC1\u0BAA\u0BCD\u0BAA\u0BA4\u0BA4\u0BBE\u0BB2\u0BCD -> \u0B87\u0BB0\u0BC1\u0BAA\u0BCD\u0BAA\u0BA4\u0BBE\u0BB2\u0BCD)
        w = re.sub('(?<!\u0BCD)\u0BA4\u0BA4(?=\u0BBE\u0BB2\u0BCD)', '\u0BA4', w)
        return w
    return re.sub('[\u0B80-\u0BFF]+', fw, text)
