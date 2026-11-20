# Review task: Arabic quiz questions for a two-team party game

The game: a host reads a question aloud to two teams of Saudi adults. Teams answer OUT LOUD, with NO answer choices shown. Then the host reveals the correct answer. Points: 200 (easy), 400 (medium), 600 (hard).

Each input line is: `ID<TAB>[category] س: question<TAB>ج: correct answer<TAB>خيارات خاطئة: wrong choices`

Give every line exactly one verdict:

- `K` keep — a fair open question: a knowledgeable adult could give the answer without seeing choices, and the host can judge the spoken answer easily.
- `C` needs choices — drop it. Use C when ANY of these holds:
  - wording only works with a list: «أي مما يلي/من الآتي/التالية», «جميع ما سبق», «كلاهما», «ليس من/عدا/باستثناء», «العبارة الصحيحة/الخاطئة», true/false judgement;
  - many different answers would be equally correct without the list (e.g. «من التيارات البحرية الباردة تيار:», «من أمثلة الفلزات:», «من نتائج الحرب:»);
  - the correct answer is a long sentence, definition or explanation (roughly more than 6–7 words) that nobody would say word-for-word, so the host can't judge it;
  - the answer is a comparative pick that only makes sense against the listed options («الأكبر بين…»), or the answer refers to options (أ و ب).
- `E` too easy / common sense — drop it. Any Saudi adult would know it instantly with no real knowledge needed, or the answer is given away by the question text. Examples: days in a week, colour of the sky, «عاصمة السعودية», 2+3, «ما الحيوان الذي يقول مياو». Mental-math items: E if a typical adult does it instantly (single-digit arithmetic, ×10, halves of round numbers); K if it needs a moment of calculation. Letter-category items («حرف «ب»: …») are judged by the same rule — the first letter is the game's built-in hint, not a reason for E by itself.
- `W` wrong or broken — drop it. The given answer is factually wrong, the text is garbled/incomplete, or the question is ambiguous so that another answer is equally right.

Be strict about C and E, but do not drop good questions just because they are hard. Dialect («لهجات», «من وين العبارة؟») and football questions are usually K unless one of the rules applies.

## Output
Write a file (path given in your task) with ONE line per input line, in the same order:
`ID<TAB>VERDICT`
For W, add `<TAB>` and a few words why. Nothing else in the file — no header, no commentary. Every input ID must appear exactly once.
When finished, reply with just the counts of K/C/E/W.
