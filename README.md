# مجلس العمدة — Majlis Al-Omda

لعبة أسئلة جماعية عربية بين فريقين: ٦ فئات، ٣٦ سؤالاً، و٣ وسائل مساعدة لكل فريق. تعمل في المتصفح وكتطبيق أندرويد بدون إنترنت.

An Arabic two-team quiz game: pick 6 categories, play 36 questions worth 200/400/600 points, with three lifelines per team. Runs in any browser and as an offline Android app.

## تحميل التطبيق · Download
**[⬇️ majlis-alomda-v3.1.apk](release/majlis-alomda-v3.1.apk)** — Android 5.0+، يعمل بدون إنترنت.

افتح الملف على جوالك ← اسمح بالتثبيت من هذا المصدر ← تثبيت. قد يظهر تحذير Play Protect لأن التطبيق من خارج المتجر: اختر «تثبيت على أي حال».

Open the file on your phone → allow installs from this source → Install.

## المزايا · Features
- ٣٣ فئة: حروف، إيموجي أماكن وأسماء، إيموجي كرة قدم، إيموجي أنمي، إيموجي أمثال، ثقافة عامة، إسلاميات، جغرافيا، تاريخ، لغة عربية، علوم، تقنية، رياضة، عالم الحيوان، السعودية، لهجات سعودية، من وين العبارة؟، عواصم، عملات، حساب ذهني، ألغاز، دوري روشن، الدوريات الكبرى، بطولات المنتخبات، ألعاب فيفا، أنمي، أنمي سبيستون، ون بيس وناروتو ودراغون بول، أفلام عالمية، ألعاب فيديو، سيارات، أكلات، أسئلة للصغار
- ~٧٩٠٠ سؤال بعد التدقيق اللغوي وحذف المكرر، تُسحب عشوائياً لكل لعبة، ولا يتكرر السؤال في نفس اللعبة ولا الأسئلة التي لُعبت على نفس الجهاز
- مؤقت ٦٠ ثانية للفريق صاحب الدور ثم ٣٠ ثانية للفريق الآخر
- وسائل المساعدة: دبّل ×٢، الحفرة، وقت إضافي
- حفظ تلقائي للعبة (النقاط، الدور، الأسئلة)
- وضع ملء الشاشة للتلفاز والآيباد
- تصميم مسطّح مع وضع نهاري (افتراضي) ووضع ليلي، وأيقونات مرسومة لكل فئة
- في التطبيق: زر بث الشاشة إلى التلفاز (Smart View) وزر تدوير الشاشة

## هيكل المشروع · Layout
| Path | What |
|---|---|
| `web/index.html` | The whole game in one self-contained HTML file (questions embedded). Open it in a browser. |
| `android/` | apktool project: `AndroidManifest.xml`, `smali/` (WebView activity), `res/` (icon, app name), `assets/` (app build of the game + Tajawal font). |
| `tools/build_apk.sh` | Builds and signs the APK with apktool + apksigner. |
| `tools/build_arabicmmlu.py` | Extracts and filters ArabicMMLU into the question bank. |
| `tools/zipalign.py` | Minimal 4-byte zip aligner used before signing. |
| `data/opentriviaqa_ar.json` | Arabic translations of selected OpenTriviaQA sports/animal questions. |

## بناء تطبيق أندرويد · Building the APK
```bash
keytool -genkeypair -keystore my.jks -alias majlis -keyalg RSA -keysize 2048 -validity 10000
APKTOOL=apktool.jar APKSIGNER=apksigner.jar KEYSTORE=my.jks KS_PASS=yourpass ./tools/build_apk.sh
```
Keep your keystore private and reuse it for every update — Android only installs an update signed with the same key.

The app loads `android/assets/index.html` in a full-screen WebView, adds `MajlisApp` to the user agent (the page uses it to switch full-screen behaviour), and opens external links in the browser. Progress is saved in the WebView's localStorage.

## مصادر الأسئلة والتراخيص · Question sources & licenses
The question data is third-party content under its own licenses — **non-commercial use only** because of ArabicMMLU:

- **ArabicMMLU** (MBZUAI) — https://github.com/mbzuai-nlp/ArabicMMLU — CC BY-NC-SA 4.0. Filtered and regrouped by subject/level.
- **EXAMS** (Hardalov et al., 2020) — https://github.com/mhardalov/exams-qa — CC BY-SA 4.0. Arabic subset, filtered.
- **OpenTriviaQA** — https://github.com/uberspot/OpenTriviaQA — CC BY-SA 4.0. Selected sports/animal questions translated into Arabic (`data/opentriviaqa_ar.json`, shared under CC BY-SA 4.0).
- Original categories written for this project: Saudi Arabia, capitals, currencies, mental math (generated) and traditional folk riddles — `tools/extra_categories.py` → `data/extra_ar.json`. Driving questions come from ArabicMMLU.
- **Absher** (Al-Monef et al., 2025) — https://huggingface.co/datasets/Renad10/Absher-Benchmark — CC BY 4.0. Saudi dialect phrases: meaning questions (re-shuffled, filtered against the dictionary meaning) and region questions built from the dataset's dialect labels — `tools/absher_categories.py` → `data/absher_ar.json`.
- **openfootball** — https://github.com/openfootball/football.json — CC0 (public domain). League tables computed from match results → `data/openfootball_champions.json`. Football questions (Saudi Pro League, big leagues, Champions League, Ballon d'Or, national-team tournaments, FIFA/EA FC games) are written from facts in `tools/football_categories.py` → `data/football_ar.json`.
- Anime: original questions written for this project plus 23 translated/adapted from OpenTriviaQA (CC BY-SA 4.0) — text only, no images or lyrics — `tools/anime_category.py` → `data/anime_ar.json`.
- حروف (Huroof-style): questions from the game's own bank whose answer is a single term, shown with the answer's first letter, plus ~350 original questions (mostly hard) so nearly every letter has 30 — `tools/huroof_hard.py` + `tools/letters_category.py` → `data/letters_ar.json`.
- Emoji categories (إيموجي أماكن وأسماء / كرة قدم / أنمي / أمثال): 150 original emoji rebus puzzles with explanations and a hint button that halves the points — `tools/picture_category.py` → `data/pictures_ar.json`.
- أفلام عالمية / ألعاب فيديو / سيارات / أكلات / أسئلة للصغار: 254 questions, 62 translated/adapted from OpenTriviaQA (CC BY-SA 4.0) and the rest written for this project — `tools/more_categories.py` → `data/more_ar.json`.
- أنمي سبيستون / ون بيس وناروتو ودراغون بول: 129 questions — 8 adapted from **Open Trivia DB** (https://opentdb.com, CC BY-SA 4.0, via https://github.com/QuartzWarrior/OTDB-Source; wrong choices written for this project) and the rest original. Years, episode counts and studios checked against **anime-offline-database** (manami-project, https://github.com/manami-project/anime-offline-database, ODbL 1.0 / DbCL 1.0) — `tools/anime_more.py` → `data/anime_more_ar.json`.
- About 50 other original questions.
- Font: **Tajawal** (Boutros Fonts / Mourad Boutros), SIL Open Font License 1.1 — `android/assets/fonts/OFL-LICENSE.txt`.

Some dataset questions contain errors or curriculum-specific content; the in-game «سؤال آخر» button swaps a question.
- `tools/clean_bank.py`: language clean-up (broken «لا» letters from PDF extraction, stray punctuation, spacing, decimal percentages, repeated choices) and de-duplication of exact and near-identical questions.
