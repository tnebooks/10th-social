"""Generate content.ta chapter files from the Tamil PDF (for stub chapters, or chapters passed on argv)."""
import sys, os, re, glob, json, shutil
sys.path.insert(0, os.path.dirname(__file__))
import tamil, pymupdf

KEEP_FM = True
BASE = r'D:/DevOps/TNEbooks/10th-social/content.ta/docs'
TITLES = {
 1: 'முதல் உலகப்போரின் வெடிப்பும் அதன் பின்விளைவுகளும்', 2: 'இரு உலகப்போர்களுக்கு இடையில் உலகம்',
 3: 'இரண்டாம் உலகப்போர்', 4: 'இரண்டாம் உலகப்போருக்குப் பிந்தைய உலகம்',
 5: '19ஆம் நூற்றாண்டில் சமூக, சமய சீர்திருத்த இயக்கங்கள்',
 6: 'ஆங்கிலேய ஆட்சிக்கு எதிராக தமிழகத்தில் நிகழ்ந்த தொடக்ககால கிளர்ச்சிகள்',
 7: 'காலனியத்துக்கு எதிரான இயக்கங்களும் தேசியத்தின் தோற்றமும்', 8: 'தேசியம்: காந்திய காலகட்டம்',
 9: 'தமிழ்நாட்டில் விடுதலைப் போராட்டம்', 10: 'தமிழ்நாட்டில் சமூக மாற்றங்கள்',
 11: 'இந்தியா - அமைவிடம், நிலத்தோற்றம் மற்றும் வடிகாலமைப்பு', 12: 'இந்தியா – காலநிலை மற்றும் இயற்கைத் தாவரங்கள்',
 13: 'இந்தியா – வேளாண்மை', 14: 'இந்தியா – வளங்கள் மற்றும் தொழிலகங்கள்',
 15: 'இந்தியா – மக்கள் தொகை, போக்குவரத்து, தகவல் தொடர்பு மற்றும் வணிகம்',
 16: 'தமிழ்நாடு - இயற்கைப் பிரிவுகள்', 17: 'தமிழ்நாடு - மானுடப் புவியியல்',
 18: 'இந்திய அரசியலமைப்பு', 19: 'நடுவண் அரசு', 20: 'மாநில அரசு', 21: 'இந்தியாவின் வெளியுறவுக் கொள்கை',
 22: 'இந்தியாவின் சர்வதேச உறவுகள்', 23: 'மொத்த உள்நாட்டு உற்பத்தி (GDP) மற்றும் அதன் வளர்ச்சி: ஓர் அறிமுகம்',
 24: 'உலகமயமாதல் மற்றும் வர்த்தகம்', 25: 'உணவுப் பாதுகாப்பு மற்றும் ஊட்டச்சத்து', 26: 'அரசாங்கமும் வரிகளும்',
 27: 'தமிழ்நாட்டில் தொழில்துறை தொகுப்புகள்'}

def section(u):
    if u <= 10: return 'வரலாறு', u
    if u <= 17: return 'புவியியல்', u - 10
    if u <= 22: return 'குடிமையியல்', u - 17
    return 'பொருளியல்', u - 22

def slug_of(u):
    for f in glob.glob(BASE + '/*/_index.md'):
        m = re.search(r'^weight:\s*(\d+)', open(f, encoding='utf-8').read(), re.M)
        if m and int(m.group(1)) == u: return os.path.basename(os.path.dirname(f))

def build(doc, u):
    slug = slug_of(u)
    d = os.path.join(BASE, slug)
    assets = os.path.join(d, 'assets')
    shutil.rmtree(assets, ignore_errors=True)
    body = tamil.convert_unit(doc, u - 1, assets_dir=assets)
    blocks = body.split('\n\n')
    # opening page: keep images, drop the split title lines, start at learning objectives
    k = next((i for i, b in enumerate(blocks) if 'கற்றலின் நோக்கங்கள்' in b), 0)
    lead_imgs = [b for b in blocks[:k] if b.startswith('![')]
    blocks = blocks[k:]
    if blocks and 'கற்றலின் நோக்கங்கள்' in blocks[0]:
        blocks[0] = '## கற்றலின் நோக்கங்கள்'
    # summary = first prose paragraph after அறிமுகம்
    j = next((i for i, b in enumerate(blocks) if b.startswith('#') and 'அறிமுகம்' in b), None)
    summ = ''
    for b in blocks[(j + 1 if j is not None else 1):]:
        if not b.startswith(('#', '!', '|', '- ', '**')) and len(b) > 80:
            summ = b; break
    summ = summ.replace('"', '”')
    if len(summ) > 260: summ = summ[:260].rsplit(' ', 1)[0] + '…'
    sec, n = section(u)
    old = open(os.path.join(d, '_index.md'), encoding='utf-8').read()
    m = re.match(r'---\n.*?\n---\n', old, re.S)
    if KEEP_FM and m and re.search(r'^title:\s*[\'"][^\'"]*[஀-௿]', m.group(0), re.M):
        fm = m.group(0) + '\n'                       # keep existing Tamil front matter verbatim
    else:
        fm = f'---\ntitle: "{TITLES[u]}"\ncategories:\n- {slug}\nweight: {u}\nsummary: "{summ}"\n---\n\n'
    fm += f'# {sec} அலகு {n}: {TITLES[u]}\n\n'
    md = fm + '\n\n'.join(blocks[:1] + lead_imgs + blocks[1:]) + '\n'
    open(os.path.join(d, '_index.md'), 'w', encoding='utf-8', newline='\n').write(md)
    nimg = len(os.listdir(assets)) if os.path.isdir(assets) else 0
    return slug, len(md), nimg

if __name__ == '__main__':
    doc = pymupdf.open(tamil.SRC)
    units = [int(a) for a in sys.argv[1:]]
    for u in units:
        slug, n, nimg = build(doc, u)
        print(f'{u:2d} {slug:58s} {n:7d} chars {nimg:3d} images', flush=True)
