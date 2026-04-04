"""
fill_cards.py — Anki flashcard generator for ObsidianJP lesson files.

Usage:
    python3 .cowork/fill_cards.py <path_to_lesson.md>

What it does:
  - Reads all #w, #wc, #wp lines from the lesson file
  - Generates Anki card templates (conjugations for verbs, forms for adjectives)
  - Adds #k tag when the word contains a known kanji (from KanjiList.md)
  - Appends # Summary + Rzeczowniki: block to the file
  - Creates a .bak backup before writing

Paths are resolved relative to this script's location (vault root).
"""

import re, sys, shutil
from pathlib import Path

VAULT       = Path(__file__).parent.parent          # ObsidianJP/
KANJI_LIST  = VAULT / 'KanjiList.md'

# ── Kanji list ────────────────────────────────────────────────────────────────
with open(KANJI_LIST) as f:
    KNOWN_KANJI = set(l.strip() for l in f if l.strip())

def has_k(text):   return any(c in KNOWN_KANJI for c in text)
def jp_start(t):
    return bool(t) and (('\u3040' <= t[0] <= '\u30ff') or ('\u4e00' <= t[0] <= '\u9fff'))

def clean_trans(t):
    t = t.replace('**', '').strip()
    if t.startswith('ほんやく: '):
        t = t[len('ほんやく: '):]
    return t.strip()

# ── Split japanese / translation ──────────────────────────────────────────────
def split(content):
    m = re.search(r'(?<=[）)])\s*-\s+', content)
    if m:
        return content[:m.start()].strip(), content[m.end():].strip()
    if ' - ' in content:
        i = content.index(' - ')
        return content[:i].strip(), content[i+3:].strip()
    return content.strip(), ''

def base(jp_raw):
    c = jp_raw
    for open_, close in [('(', ')'), ('（', '）')]:
        if c.startswith(open_) and close in c:
            c = c[c.index(close)+1:].strip()
    return re.sub(r'[（(][^）)]*[）)]', '', c).strip()

# ── Conjugation tables ────────────────────────────────────────────────────────
_G = {
    'う':('い','って','った','わない','わなかった','えば','われる','い出す'),
    'く':('き','いて','いた','かない','かなかった','けば','かれる','き出す'),
    'ぐ':('ぎ','いで','いだ','がない','がなかった','げば','がれる','ぎ出す'),
    'す':('し','して','した','さない','さなかった','せば','される','し出す'),
    'つ':('ち','って','った','たない','たなかった','てば','たれる','ち出す'),
    'ぬ':('に','んで','んだ','なない','ななかった','ねば','なれる','に出す'),
    'ぶ':('び','んで','んだ','ばない','ばなかった','べば','ばれる','び出す'),
    'む':('み','んで','んだ','まない','まなかった','めば','まれる','み出す'),
    'る':('り','って','った','らない','らなかった','れば','られる','り出す'),
}

def cg(b):
    e = b[-1] if b else ''
    if e not in _G: return None
    ms,te,ta,nai,nkt,ba,rar,dasu = _G[e]
    r,stem = b[:-1], b[:-1]+ms
    return dict(masu=stem+'ます',te=r+te,ta=r+ta,nai=r+nai,nakatta=r+nkt,
                ba=r+ba,rareru=r+rar,dasu=r+dasu,sonkei=r+rar,ohoni='お'+stem+'になる')

def ci(b):
    if not b.endswith('る'): return None
    s=b[:-1]
    return dict(masu=s+'ます',te=s+'て',ta=s+'た',nai=s+'ない',nakatta=s+'なかった',
                ba=s+'れば',rareru=s+'られる',dasu=s+'出す',sonkei=s+'られる',ohoni='お'+s+'になる')

def ck():
    return dict(masu='来ます',te='来て',ta='来た',nai='来ない',nakatta='来なかった',
                ba='来れば',rareru='来られる',dasu='来出す',sonkei='来られる',ohoni='お出でになる')

# ── Card builders ─────────────────────────────────────────────────────────────
def vcard(front, honnyaku, conj, k):
    t = '#k ' if k else ''
    L = [f'{front} {t}#card', f'ほんやく: {honnyaku}']
    if conj:
        L += [f'ます形: {conj["masu"]}',f'て形: {conj["te"]}',f'た形: {conj["ta"]}',
              f'ない形: {conj["nai"]}',f'なかった形: {conj["nakatta"]}',f'ば形: {conj["ba"]}',
              f'られる形: {conj["rareru"]}',f'出す形: {conj["dasu"]}',
              f'尊敬語: {conj["sonkei"]}',f'お〜になる: {conj["ohoni"]}']
    return '\n'.join(L)

def acard(front, h, past, neg, adv, k):
    t = '#k ' if k else ''
    return '\n'.join([f'{front} {t}#card',f'ほんやく: {h}',
                      f'過去形: {past}',f'否定形: {neg}',f'副詞形: {adv}'])

def wcard(front, jp, k):
    t = '#k ' if k else ''
    return f'{front} {t}#card\n{jp}'

# ── Verb type lookup  ─────────────────────────────────────────────────────────
# Extend this dict as new lessons introduce new verbs.
VTYPES = {
    '伝える':'ichidan','話す':'godan','答える':'ichidan','置く':'godan',
    '売る':'godan','困る':'godan','勤める':'ichidan','手伝う':'godan',
    '立つ':'godan','点ける':'ichidan','消す':'godan','出席':'suru',
    '覚える':'ichidan','忘れる':'ichidan','使う':'godan','生まれる':'ichidan',
    '上げる':'ichidan','頼む':'godan','呼ぶ':'godan','見せる':'ichidan',
    '来る':'kuru','来':'kuru',
}

def vtype(jp_raw, b):
    for k,v in VTYPES.items():
        if k in jp_raw or k in b: return v
    return None

# ── Process one file ──────────────────────────────────────────────────────────
def process(path: Path):
    cards = []
    for raw in path.read_text(encoding='utf-8').splitlines():
        s = raw.strip()

        if s.startswith('#wc '):
            content       = s[4:]
            jp, trans     = split(content)
            if jp_start(trans):
                jp2, _ = split(trans)
                front  = honnyaku = jp2 or jp
            else:
                front    = clean_trans(trans) if trans else jp
                honnyaku = jp
            if not front: continue
            b  = base(jp)
            vt = vtype(jp, b)
            k  = has_k(jp)
            conj = {'suru':None,'ichidan':ci(b),'godan':cg(b),'kuru':ck()}.get(vt)
            cards.append(vcard(front, honnyaku, conj, k))

        elif s.startswith('#wp '):
            jp, trans = split(s[4:])
            if not trans: continue
            front = clean_trans(trans)
            b     = base(jp)
            k     = has_k(jp)
            if any(x in jp for x in ['次','はじめて']):
                cards.append(acard(front, jp, '—','—','—', k))
            elif b.endswith('い'):
                st = b[:-1]
                if b in ['いい','よい']:
                    cards.append(acard(front, jp,'よかった','よくない','よく', k))
                else:
                    cards.append(acard(front, jp, st+'かった', st+'くない', st+'く', k))
            else:
                cards.append(acard(front, jp, '—','—','—', k))

        elif s.startswith('#w '):
            jp, trans = split(s[3:])
            if not jp or not trans: continue
            cards.append(wcard(clean_trans(trans), jp.replace('**',''), has_k(jp)))

    return cards

# ── Entry point ───────────────────────────────────────────────────────────────
def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    path = Path(sys.argv[1])
    if not path.exists():
        print(f"Not found: {path}"); sys.exit(1)

    shutil.copy(path, path.with_suffix('.md.bak'))
    print(f"Backup → {path.with_suffix('.md.bak')}")

    cards = process(path)
    print(f"Generated {len(cards)} cards")

    section = ('\n# Summary\n\n --- \n\n\n Rzeczowniki:\n\n'
               + '\n\n\n'.join(cards)
               + '\n\n\n --- \n\n\n')

    with open(path, 'a', encoding='utf-8') as f:
        f.write(section)
    print(f"Saved → {path}")

if __name__ == '__main__':
    main()
