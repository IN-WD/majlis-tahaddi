"""Saudi dialect categories from the Absher benchmark (CC BY 4.0, Al-Monef et al.).
  dial  — "ما معنى عبارة …؟"  from *_Meaning_questions.csv (options re-shuffled, quality-filtered)
  where — "من لهجة أي منطقة؟" built from the dataset's human-labelled Dialect type column
Each question carries the dictionary meaning as a note shown with the answer.
Usage: python3 tools/absher_categories.py <dir-with-csvs> data/absher_ar.json"""
import glob, json, random, re, sys
import pandas as pd

rnd = random.Random(11)
LET = {"أ":0,"ا":0,"A":0,"ب":1,"B":1,"ج":2,"C":2,"د":3,"D":3}
REG = {"Central":"الوسطى (نجد)","Western":"الغربية (الحجاز)","Southern":"الجنوبية","Northern":"الشمالية","Eastern":"الشرقية"}
STOP = set("في من على عن إلى الى أو او و ما ماذا هو هي أن ان لا يعني تعني كلمة عبارة شيء شخص الذي التي".split())

def opts_of(text):
    out = []
    for line in str(text).splitlines():
        m = re.match(r"\s*([أابجدABCD])\s*[\)\.\-:]\s*(.+)", line.strip())
        if m: out.append((m.group(1), m.group(2).strip().rstrip(".")))
    return out
def words(s):
    s = re.sub(r"[^؀-ۿ ]", " ", str(s))
    return {re.sub(r"^(ال|وال|بال|لل)", "", w) for w in s.split() if len(w) > 2 and w not in STOP}
def note(m):
    m = re.sub(r"\s+", " ", str(m)).strip().lstrip(" .:-،")
    m = re.sub(r"^(تعني|يعني|أي|اي)\s*[:：]?\s*", "", m)
    return (m[:110] + "…") if len(m) > 110 else m

def main(src, dst):
    f = glob.glob(f"{src}/*Phrases_Meaning_questions.csv")[0]
    d = pd.read_csv(f); d.columns = ["term","meaning","dialect","q","ans"]
    d["dialect"] = d["dialect"].astype(str).str.strip()
    dial = {"200": [], "400": [], "600": []}; where = {"200": [], "400": [], "600": []}
    kept = dropped = 0
    for r in d.itertuples(index=False):
        term = str(r.term).strip(); o = opts_of(r.q); k = LET.get(str(r.ans).strip())
        if len(o) != 4 or k is None or len(term) > 40: dropped += 1; continue
        texts = [t for _, t in o]; correct = texts[k]
        # keep only if the keyed option agrees with the dictionary meaning
        if not (words(correct) & words(r.meaning)) or len(set(texts)) < 4 or any(len(t) > 60 for t in texts):
            dropped += 1; continue
        kept += 1
        rnd.shuffle(texts)
        lvl = {"General":"200","Western":"400","Central":"400"}.get(r.dialect, "600")
        dial[lvl].append([f"ما معنى عبارة «{term}»؟", texts, texts.index(correct), note(r.meaning)])
    for r in d.itertuples(index=False):
        if r.dialect not in REG: continue
        term = str(r.term).strip()
        if len(term) > 40: continue
        right = REG[r.dialect]; others = [v for v in REG.values() if v != right]
        opts = [right] + rnd.sample(others, 3); rnd.shuffle(opts)
        lvl = {"Western":"200","Central":"400"}.get(r.dialect, "600")
        where[lvl].append([f"عبارة «{term}» من لهجة أي منطقة؟", opts, opts.index(right), note(r.meaning)])
    json.dump({"dial": dial, "where": where}, open(dst, "w"), ensure_ascii=False, indent=0)
    print("meaning kept", kept, "dropped", dropped)
    print({c: {p: len(v) for p, v in x.items()} for c, x in {"dial": dial, "where": where}.items()})

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
