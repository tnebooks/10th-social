"""Insert PDF content missing from an existing chapter without altering any existing text.

Each PDF block is checked against the chapter. Fully missing blocks are inserted whole; blocks that are
mostly present but contain sentences absent from the chapter get those sentences inserted. Insertions
go directly after the existing paragraph that matched the most recent present block (document order).
"""
import sys, re, os
sys.path.insert(0, os.path.dirname(__file__))
from ta_compare_norm import toks

def shingles(t): return set(' '.join(t[i:i + 3]) for i in range(len(t) - 2))

def merge(existing_path, parsed_path):
    raw = open(existing_path, encoding='utf-8').read()
    m = re.match(r'---\n.*?\n---\n', raw, re.S)
    body_start = m.end()
    # paragraph spans in the original text
    spans = []
    pos = body_start
    for mm in re.finditer(r'\n[ \t]*\n', raw[body_start:]):
        end = body_start + mm.start()
        if raw[pos:end].strip(): spans.append((pos, end))
        pos = body_start + mm.end()
    if raw[pos:].strip(): spans.append((pos, len(raw.rstrip('\n'))))
    psh = [shingles(toks(raw[a:b])) for a, b in spans]
    allsh = set().union(*psh)
    def present(text):
        g = shingles(toks(text))
        return (len(g & allsh) / len(g) if g else 1.0), g
    src = open(parsed_path, encoding='utf-8').read()
    blocks = [b for b in src.split('\n\n') if b.strip() and not b.startswith(('<!--', '!['))]
    inserts, anchor, n_blocks, n_sent = {}, 0, 0, 0
    for b in blocks:
        if len(toks(b)) < 3: continue
        r, g = present(b)
        if r >= 0.5:
            best = max(range(len(spans)), key=lambda i: len(g & psh[i]))
            if g & psh[best] and best >= anchor: anchor = best
            if b.startswith(('#', '|')): continue
            # sentence-level gaps inside a mostly-present paragraph
            miss = [s for s in re.split(r'(?<=[.?!])\s+', b) if len(toks(s)) >= 4 and present(s)[0] < 0.2]
            if miss:
                inserts.setdefault(anchor, []).append(' '.join(miss)); n_sent += len(miss)
            continue
        inserts.setdefault(anchor, []).append(b); n_blocks += 1
    out = raw
    for i in sorted(inserts, reverse=True):
        end = spans[i][1]
        out = out[:end] + '\n\n' + '\n\n'.join(inserts[i]) + out[end:]
    open(existing_path, 'w', encoding='utf-8', newline='').write(out)
    return n_blocks, n_sent
