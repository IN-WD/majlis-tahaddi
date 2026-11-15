"""Language clean-up and de-duplication for the game's question bank.

Usage: python3 tools/clean_bank.py IN.html [IN2.html ...]   (rewrites `const BANK=` in place)
Writes a report to /tmp/clean_report.json.

Fixes
- broken «لا»/«لإ»/«لأ»/«لآ» from PDF extraction (االستوائية → الاستوائية, الواليات → الولايات),
  verified against word frequencies in the whole bank
- leading stray punctuation / question numbers, extra spaces, dot runs → «…»
- percentages stored as decimals (0.3 → 30%) when every choice is a decimal and the question is about a ratio
- repeated answer choices in one question
De-duplication
- identical questions (after normalising spelling/diacritics/punctuation) → keep one
- near-identical questions with the same answer and the same numbers → keep one
- «حروف» questions that copy another category are kept; the game treats them as one question at run time.
"""
import json, re, sys, math, collections

DI = re.compile(r'[ؗ-ًؚ-ْٰـ]')
PRIORITY = ["cap","cur","ani","spt","spl","big5","intl","fifa","anime","ksa","dial","where","math","rid",
            "isl","his","lng","sci","tec","geo","gk","huroof"]
HUROOF_PREFIX = re.compile(r'^حرف «.» ?: ?')

def norm(t):
    t = DI.sub('', str(t)); t = re.sub('[أإآٱ]', 'ا', t)
    t = t.replace('ة', 'ه').replace('ى', 'ي').replace('ؤ', 'و').replace('ئ', 'ي')
    t = HUROOF_PREFIX.sub('', t)
    t = re.sub(r'[^\w\s%]', ' ', t)
    return re.sub(r'\s+', ' ', t).strip().lower()

def is_mcq(x): return isinstance(x[1], list)
def ans(x): return x[1][x[2]] if is_mcq(x) else x[1]
def strings(x):
    """indices of text fields in an item"""
    if is_mcq(x): return [('q',)] + [('o', i) for i in range(len(x[1]))] + ([('n',)] if len(x) > 3 and x[3] else [])
    return [('q',), ('a',)] + ([('n',)] if len(x) > 2 and x[2] else [])
def get(x, f):
    if f[0] == 'q': return x[0]
    if f[0] == 'o': return x[1][f[1]]
    if f[0] == 'a': return x[1]
    return x[3] if is_mcq(x) else x[2]
def put(x, f, v):
    if f[0] == 'q': x[0] = v
    elif f[0] == 'o': x[1][f[1]] = v
    elif f[0] == 'a': x[1] = v
    elif is_mcq(x): x[3] = v
    else: x[2] = v

WORD = re.compile(r'[ء-يٰٱ]+')

HN = lambda w: re.sub('[أإآ]', 'ا', w)
SPELL = {}
def build_freq(bank):
    raw = collections.Counter()
    for k, lv in bank.items():
        for l, qs in lv.items():
            for x in qs:
                for f in strings(x): raw.update(WORD.findall(str(get(x, f))))
    c = collections.Counter()
    best = {}
    for w, n in raw.items():
        c[HN(w)] += n
        if n > best.get(HN(w), ('', 0))[1]: best[HN(w)] = (w, n)
    SPELL.update({k: v[0] for k, v in best.items()})
    return c

def fix_lamalef(word, freq, affected):
    """the PDF extractor wrote «لX» as «Xل» (X = ا أ إ آ). Undo it only in text from an affected source
    (one that shows the certain «اال» pattern), and only when the result is a known word."""
    if not affected: return word
    best = word.replace('االله', 'الله')
    for _ in range(3):
        cands = []
        for m in re.finditer(r'[اأإآ]ل', best):
            p = m.start()
            if p == 0: continue                      # real article «ال» at word start
            cands.append(best[:p] + 'ل' + best[p] + best[p + 2:])
        good = None
        F = lambda w: freq[HN(w)]
        sc = lambda w: F(w) + F(re.sub(r'^[وبفلك]', '', w)) + (F(re.sub(r'^[وبفلك]?ال', '', w)) if not re.match(r'^[وبفلك]?ال', w) else 0)
        m = re.search(r'ا([اأإآ])ل', best)
        if m:   # «اال…»: either a swapped «لا» or a doubled alef — take whichever reading is a known word
            drop = best[:m.start() + 1] + best[m.start() + 2:] if m.group(1) == 'ا' else None
            swap = best[:m.start() + 1] + 'ل' + m.group(1) + best[m.start() + 3:]
            good = drop if drop and F(drop) > F(swap) else swap
        else:
            for c in cands:
                if freq[HN(c)] >= 2 and freq[HN(c)] > 2 * freq[HN(best)]:
                    good = c; break
        if not good: break
        best = good
    if best != word:   # restore the bank's usual hamza spelling (الانهار → الأنهار)
        best = SPELL.get(HN(best), best) if HN(SPELL.get(HN(best), '')) == HN(best) else best
    return best

MANUAL = {'منتصفاالليل': 'منتصف الليل', 'الأمطاراالعصارية': 'الأمطار الإعصارية', 'وزيادةاالحتباس': 'وزيادة الاحتباس',
          'تظهراالعاصير': 'تظهر الأعاصير', 'للبيئةواإلنتاج': 'للبيئة والإنتاج', 'االنيموميترذو': 'الأنيمومتر ذو', 'االنيموميتر': 'الأنيمومتر', 'االصطالحي': 'الاصطلاحي', 'الموصالت': 'الموصلات'}
AFFECTED = re.compile(r'ا[اأإآ]ل(?!له)')

def clean_text(t, freq, is_question, affected=False):
    s = str(t)
    if s.startswith('🖼|'): return s
    s = s.replace(' ', ' ')
    s = re.sub(r'\s+', ' ', s).strip()
    for a, b in MANUAL.items(): s = s.replace(a, b)
    s = WORD.sub(lambda m: fix_lamalef(m.group(0), freq, affected), s)
    s = re.sub(r'^\(?\d{1,3}\s*[\(\)\-–]\s*(?=[ء-ي])', '', s)       # «24( وحدة…»
    s = re.sub(r'^[\s:：.،,؛\-–]+', '', s)   # leading stray punctuation
    if not is_question: s = re.sub(r'^[أابجدهـ]\s*[-–)]\s*(?=\S)', '', s)   # leftover choice letters «ج- …»
    s = re.sub(r'(\s*[.…]){3,}', ' … ', s); s = re.sub(r'[.…]{2,}', '…', s)  # dot runs
    s = re.sub(r'\(\s+', '(', s); s = re.sub(r'\s+\)', ')', s)
    s = re.sub(r'\s+([،,:؟?!])', r'\1', s)
    s = re.sub(r'(\d)\s+%', r'\1%', s)
    if not is_question: s = re.sub(r'[\s:.،؛]+$', '', s)                      # answers: trailing punctuation
    s = re.sub(r'\s+', ' ', s).strip()
    return s or str(t).strip()

def pct(v):
    f = float(v) * 100
    return (f"{f:.1f}".rstrip('0').rstrip('.')) + '%'

def main(paths):
    s = open(paths[0]).read()
    line = [l for l in s.split('\n') if l.startswith('const BANK=')][0]
    bank = json.loads(line[len('const BANK='):].rstrip(';'))
    freq = build_freq(bank)
    rep = collections.defaultdict(list)
    # ---- 1. text fixes ----
    for k, lv in bank.items():
        for l, qs in lv.items():
            for x in qs:
                aff = any(AFFECTED.search(str(get(x, f))) for f in strings(x))
                for f in strings(x):
                    old = get(x, f); new = clean_text(old, freq, f[0] == 'q', aff)
                    if new != old:
                        put(x, f, new)
                        tag = 'lamalef' if DI.sub('', new).replace(' ', '') != DI.sub('', old).replace(' ', '') and re.sub(r'[^ء-ي]', '', new) != re.sub(r'[^ء-ي]', '', old) else 'format'
                        rep[tag].append((k, old, new))
                if is_mcq(x):
                    o = x[1]
                    if all(re.fullmatch(r'0?\.\d+|1(\.0+)?', str(a).strip()) for a in o) and re.search(r'نسب|%|مساحة|يغطي', x[0]):
                        x[1] = [pct(a) for a in o]; rep['percent'].append((k, x[0], o, x[1]))
                    # repeated choices
                    seen, keep = set(), []
                    for i, a in enumerate(x[1]):
                        key = re.sub(r'\s+', '', str(a))
                        if key in seen and i != x[2]: continue
                        if key in seen and i == x[2]:  # correct one duplicated earlier: drop the earlier copy
                            keep = [j for j in keep if re.sub(r'\s+', '', str(x[1][j])) != key]
                        seen.add(key); keep.append(i)
                    if len(keep) < len(x[1]):
                        rep['dup_choices'].append((k, x[0], x[1]))
                        x[2] = keep.index(x[2]); x[1] = [x[1][i] for i in keep]
    # ---- 2. exact duplicates ----
    items = []
    for k, lv in bank.items():
        for l, qs in lv.items():
            for i, x in enumerate(qs):
                if str(x[0]).startswith('🖼|'): continue
                items.append((k, l, i, x))
    def quality(it):
        k, l, i, x = it
        t = ' '.join(str(get(x, f)) for f in strings(x))
        bad = len(re.findall(r'\s{2,}|ا[اأإآ]ل|[:.]{2,}', t))
        return (PRIORITY.index(k) if k in PRIORITY else 99, bad, -len(x[1]) if is_mcq(x) else 0)
    drop = set()
    groups = collections.defaultdict(list)
    for it in items: groups[(it[0] == 'huroof', norm(it[3][0]))].append(it)
    for (_, q), g in groups.items():
        if len(g) < 2 or not q: continue
        g = sorted(g, key=quality)
        for it in g[1:]:
            drop.add((it[0], it[1], it[2])); rep['dup_exact'].append((it[0], it[3][0], str(ans(it[3])), g[0][0], g[0][3][0]))
    # ---- 3. near duplicates: same answer, same numbers, very similar wording ----
    live = [it for it in items if (it[0], it[1], it[2]) not in drop]
    toks = {id(it): set(norm(it[3][0]).split()) for it in live}
    df = collections.Counter(); [df.update(t) for t in toks.values()]
    N = len(live); idf = {w: math.log(N / df[w]) for w in df}
    nums = lambda t: sorted(re.findall(r'\d+', str(t).translate(str.maketrans('٠١٢٣٤٥٦٧٨٩', '0123456789'))))
    bya = collections.defaultdict(list)
    for it in live: bya[(it[0] == 'huroof', norm(ans(it[3])))].append(it)
    for _, g in bya.items():
        g = sorted(g, key=quality)
        for a in range(len(g)):
            A = g[a]
            if (A[0], A[1], A[2]) in drop: continue
            for b in range(a + 1, len(g)):
                B = g[b]
                if (B[0], B[1], B[2]) in drop: continue
                ta, tb = toks[id(A)], toks[id(B)]
                if not ta or not tb: continue
                sim = sum(idf[w] for w in ta & tb) / sum(idf[w] for w in ta | tb)
                if sim >= 0.8 and nums(A[3][0]) == nums(B[3][0]):
                    drop.add((B[0], B[1], B[2])); rep['dup_near'].append((round(sim, 2), B[0], B[3][0], A[0], A[3][0], str(ans(A[3]))))
    for k, l, i in sorted(drop, key=lambda d: -d[2]):
        del bank[k][l][i]
    out = 'const BANK=' + json.dumps(bank, ensure_ascii=False, separators=(',', ':')) + ';'
    for p in paths:
        t = open(p).read().split('\n')
        t = [out if l.startswith('const BANK=') else l for l in t]
        open(p, 'w').write('\n'.join(t))
    json.dump(rep, open('/tmp/clean_report.json', 'w'), ensure_ascii=False, indent=0)
    print({k: len(v) for k, v in rep.items()})
    print('questions now:', sum(len(q) for lv in bank.values() for q in lv.values()))

if __name__ == '__main__':
    main(sys.argv[1:])
