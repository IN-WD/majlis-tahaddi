import pandas as pd, json, re, sys, random
d=pd.read_csv(sys.argv[1])
CAT={
 'General Knowledge':'gk','Islamic Studies':'isl','Geography':'geo','History':'his',
 'Arabic Language':'lng','Natural Science':'sci','Biology':'sci','Physics':'sci',
 'Computer Science':'tec',}
LVL={'Primary':200,'Middle':400,'High':600,'Univ':600}
BAD=re.compile(r'(جميع ما سبق|كل ما سبق|لا شيء مما سبق|جميع الإجابات|كل الإجابات|ليس مما سبق|الشكل|الصورة|الجدول|المجاور|المقابل|الرسم|الخريطة|النص السابق|الفقرة|الدرس|الأبيات|البيت السابق|مما يلي عدا|ب و ج|أ و ب|ا و ب|ما ذكر|غير صحيح|كلاهما|إجابتين|الإجابتين|الورقة النقاشية|الأردن|الاردن|فلسطين|الفلسطيني|وضح|علل|‫|‪|اآل|األ|ال )')
rows=[]
for r in d.itertuples(index=False):
    s=getattr(r,'Subject'); lv=getattr(r,'Level')
    if s not in CAT or lv not in LVL: continue
    if isinstance(getattr(r,'Context'),str) and r.Context.strip(): continue
    q=str(r.Question).strip()
    opts=[getattr(r,f'_{i}') for i in range(9,14)]
    opts=[str(o).strip() for o in opts if isinstance(o,str) and o.strip()]
    if len(opts)<2: continue
    key='ABCDE'.find(str(getattr(r,'_8')).strip())
    if key<0 or key>=len(opts): continue
    if len(q)<8 or len(q)>150: continue
    if any(len(o)>45 for o in opts): continue
    if BAD.search(q) or any(BAD.search(o) for o in opts): continue
    if set(o.replace('ـ','') for o in opts) <= {'صح','خطأ','صواب','خاطئ','صحيح','خطا','صحيحة','خاطئة'}: continue
    if 'مصعب بن عمير' in q: continue
    rows.append((CAT[s],LVL[lv],q,opts,key))
random.seed(7)
bank={}
for c,p,q,o,k in rows: bank.setdefault(c,{}).setdefault(p,[]).append([q,o,k])
out={}
for c,lv in bank.items():
    out[c]={}
    for p,lst in lv.items():
        random.shuffle(lst); out[c][p]=lst
for c in out: print(c,{p:len(v) for p,v in out[c].items()})
json.dump(out,open(sys.argv[2],'w'),ensure_ascii=False,separators=(',',':'))
