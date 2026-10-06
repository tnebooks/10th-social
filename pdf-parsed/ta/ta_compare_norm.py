"""Normalisation used only for comparing Tamil text (both sides get the same treatment)."""
import re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
import tamil

TOK = re.compile(r'[஀-௿A-Za-z0-9]+')
ABBR = [('ச.கி.மீட்டர்', 'சதுர கிலோமீட்டர்'), ('ச.கி.மீ', 'சதுர கிலோமீட்டர்'), ('கி.மீ', 'கிலோமீட்டர்'),
        ('செ.மீ', 'சென்டிமீட்டர்'), ('மி.மீ', 'மில்லிமீட்டர்')]
METRE = re.compile(r'(\d)\s*மீ(?![஀-௿])')
DOUBLE = re.compile(r'([க-ஹ])\1+(?!்)')
REPEAT = re.compile(r'([க-ஹ])([ா-ூெ-ை])\1\2')

def cmpnorm(s):
    s = tamil.clean(s)
    for a, b in ABBR:
        s = s.replace(a, b)
    s = METRE.sub(lambda m: m.group(1) + ' மீட்டர்', s)
    s = DOUBLE.sub(lambda m: m.group(1), s)          # neutralise doubled-consonant differences
    s = REPEAT.sub(lambda m: m.group(1) + m.group(2), s)
    return s

def toks(s):
    return [t.lower() for t in TOK.findall(cmpnorm(s))]

if __name__ == '__main__':
    for w in ['இந்தியா 15,200 கி.மீ நில', 'உயரம் 6000 மீ ஆகும்', 'வந்தது', 'அமெரிக்ககா']:
        print(w, '->', cmpnorm(w))
