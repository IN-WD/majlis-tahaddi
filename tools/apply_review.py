"""Apply the per-question review (K keep / C needs choices / E too easy / W wrong or broken).
Usage: python3 tools/apply_review.py RESULTS_DIR file.html [file2.html ...]
IDs are cat|level|index into the bank as it was when the review batches were made."""
import json, sys, glob, collections
rdir, files = sys.argv[1], sys.argv[2:]
drop = collections.defaultdict(set)
for p in sorted(glob.glob(rdir + '/result_*.txt')):
    for l in open(p):
        x = l.rstrip('\n').split('\t')
        if len(x) >= 2 and x[1] in 'CEW':
            k, lv, i = x[0].split('|'); drop[(k, lv)].add(int(i))
for f in files:
    L = open(f).read().split('\n')
    n = [i for i, l in enumerate(L) if l.startswith('const BANK=')][0]
    bank = json.loads(L[n][len('const BANK='):].rstrip(';'))
    before = sum(len(q) for lv in bank.values() for q in lv.values())
    for (k, lv), idx in drop.items():
        bank[k][lv] = [x for i, x in enumerate(bank[k][lv]) if i not in idx]
    after = sum(len(q) for lv in bank.values() for q in lv.values())
    L[n] = 'const BANK=' + json.dumps(bank, ensure_ascii=False, separators=(',', ':')) + ';'
    open(f, 'w').write('\n'.join(L))
    print(f, before, '->', after)
    for k, lv in bank.items():
        thin = {l: len(q) for l, q in lv.items() if len(q) < 4}
        if thin: print('  thin', k, thin)
