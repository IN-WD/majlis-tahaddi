"""Original flat, outlined category illustrations (viewBox 0 0 160 110) + short descriptions.
Writes data/category_art.json  →  {"art": {key: "<svg inner>"}, "desc": {key: "..."}}"""
import json, sys

K = "#26233a"   # outline colour (set via CSS)
ART = {
# ---------------- ثقافة ومعرفة ----------------
"huroof": '''
<rect x="18" y="36" width="38" height="42" rx="8" fill="#ffd166"/><text class="t" x="37" y="68" fill="#26233a">أ</text>
<rect x="61" y="28" width="38" height="42" rx="8" fill="#7cc4ff" transform="rotate(-6 80 49)"/><text class="t" x="80" y="61" fill="#26233a" transform="rotate(-6 80 49)">ب</text>
<rect x="104" y="36" width="38" height="42" rx="8" fill="#9be3b5"/><text class="t" x="123" y="68" fill="#26233a">ت</text>
<path d="M14 96h132" fill="none"/>''',
"gk": '''
<path d="M80 18c-17 0-29 13-29 28 0 11 6 17 11 23 3 4 4 7 4 11h28c0-4 1-7 4-11 5-6 11-12 11-23 0-15-12-28-29-28z" fill="#ffd75e"/>
<rect x="66" y="80" width="28" height="9" rx="3" fill="#c9cede"/><rect x="69" y="89" width="22" height="8" rx="3" fill="#c9cede"/>
<path d="M73 60l7 8 7-8" fill="none"/><path d="M30 30l9 5M28 52h10M130 30l-9 5M132 52h-10M80 4v6" fill="none"/>''',
"isl": '''
<rect x="38" y="62" width="76" height="40" fill="#f3e6c9"/><path d="M48 62c0-22 14-34 28-34s28 12 28 34z" fill="#3fa66b"/>
<path d="M76 28v-9" fill="none"/><path d="M79 9a6 6 0 1 0 0 10 8 8 0 0 1 0-10z" fill="#ffcf4a"/>
<path d="M66 102V84a10 10 0 0 1 20 0v18" fill="#3b6fb6"/>
<rect x="122" y="34" width="14" height="68" fill="#f3e6c9"/><path d="M120 34l9-16 9 16z" fill="#3fa66b"/><rect x="119" y="52" width="20" height="6" fill="#d9c79f"/>
<path d="M14 102h132" fill="none"/>''',
"geo": '''
<path d="M50 96h60" fill="none"/><path d="M80 86v10" fill="none"/><path d="M42 50a40 40 0 0 0 64 30" fill="none"/>
<circle cx="78" cy="48" r="32" fill="#6cb7f0"/>
<path d="M58 30c8-4 14 2 12 8s-10 4-10 12-8 6-10-2 2-14 8-18zM86 22c8 2 18 8 20 18-6 2-8 8-14 6s-4-10-10-12-2-12 4-12zM84 62c6-4 14-2 14 4s-8 10-14 8-4-8 0-12z" fill="#5cbf72"/>''',
"his": '''
<path d="M30 40l50-24 50 24z" fill="#f3e6c9"/><rect x="30" y="40" width="100" height="9" fill="#e4d2ab"/>
<rect x="38" y="49" width="14" height="44" fill="#f3e6c9"/><rect x="63" y="49" width="14" height="44" fill="#f3e6c9"/><rect x="88" y="49" width="14" height="44" fill="#f3e6c9"/><rect x="113" y="49" width="14" height="44" fill="#f3e6c9"/>
<rect x="24" y="93" width="112" height="10" fill="#e4d2ab"/><circle cx="80" cy="31" r="5" fill="#ffcf4a"/>''',
"lng": '''
<path d="M30 22h70l14 14v64H30z" fill="#ffffff"/><path d="M100 22v14h14" fill="#e9ecf5"/>
<path d="M42 50h52M42 64h52M42 78h34" fill="none"/>
<path d="M146 10c-18 6-34 24-44 46l-4 14 10-10c20-10 34-30 38-50z" fill="#f4a261"/><path d="M98 70l26-34" fill="none"/>''',
"sci": '''
<path d="M62 14h26M66 14v28L42 88c-4 8 1 14 10 14h46c9 0 14-6 10-14L84 42V14" fill="#e8f4ff"/>
<path d="M50 74h50l8 14c4 8-1 14-10 14H52c-9 0-14-6-10-14z" fill="#7ee0b0"/>
<circle cx="68" cy="86" r="4" fill="#ffffff"/><circle cx="84" cy="80" r="3" fill="#ffffff"/><circle cx="80" cy="60" r="3" fill="#7ee0b0"/>
<ellipse cx="128" cy="40" rx="18" ry="7" fill="none"/><ellipse cx="128" cy="40" rx="18" ry="7" fill="none" transform="rotate(60 128 40)"/><ellipse cx="128" cy="40" rx="18" ry="7" fill="none" transform="rotate(-60 128 40)"/><circle cx="128" cy="40" r="4" fill="#ff7b7b"/>''',
"tec": '''
<rect x="30" y="24" width="84" height="56" rx="6" fill="#3b3f5c"/><rect x="37" y="31" width="70" height="42" rx="3" fill="#7cc4ff"/>
<path d="M20 80h104l-8 14H28z" fill="#c9cede"/>
<rect x="118" y="44" width="26" height="50" rx="6" fill="#3b3f5c"/><rect x="122" y="50" width="18" height="36" rx="2" fill="#9be3b5"/>
<path d="M48 44h20M48 54h32M48 64h14" fill="none"/>''',
"ani": '''
<path d="M40 64c4-20 18-28 30-20 6-14 22-16 30-2 8 2 12 10 12 20v10H40z" fill="#d9a35b"/>
<path d="M108 62c4-16 6-28 14-34 6-4 14-2 16 4l-4 6h-6c-4 8-6 18-8 28z" fill="#d9a35b"/>
<path d="M48 72v28M60 72v28M92 72v28M104 72v28" fill="none"/><circle cx="130" cy="31" r="1.5" fill="#26233a"/>
<path d="M14 100h132" fill="none"/>''',
"cap": '''
<rect x="22" y="52" width="24" height="48" fill="#9fb4e8"/><rect x="48" y="30" width="26" height="70" fill="#7c97dd"/><rect x="76" y="44" width="22" height="56" fill="#b8c8f0"/><rect x="100" y="22" width="22" height="78" fill="#6f87cf"/><rect x="124" y="58" width="18" height="42" fill="#9fb4e8"/>
<path d="M111 22V6" fill="none"/><path d="M111 6h16l-4 5 4 5h-16z" fill="#ff7b7b"/>
<path d="M54 40h14M54 52h14M54 64h14M106 34h10M106 46h10M106 58h10" fill="none"/><path d="M14 100h132" fill="none"/>''',
"cur": '''
<rect x="66" y="30" width="78" height="44" rx="6" fill="#8fd19e" transform="rotate(-8 105 52)"/><circle cx="105" cy="52" r="10" fill="#c9f0d2"/>
<ellipse cx="50" cy="92" rx="26" ry="8" fill="#ffcf4a"/><path d="M24 92v-10c0 4 12 8 26 8s26-4 26-8v10" fill="#f2b632"/>
<path d="M24 82v-10c0 4 12 8 26 8s26-4 26-8v10" fill="#ffcf4a"/><ellipse cx="50" cy="62" rx="26" ry="8" fill="#ffd966"/><path d="M24 62v10c0 4 12 8 26 8s26-4 26-8V62" fill="#f2b632"/>''',
# ---------------- رياضة وترفيه ----------------
"spt": '''
<circle cx="56" cy="58" r="30" fill="#f08a3c"/><path d="M26 58h60M56 28v60M35 37c10 10 10 32 0 42M77 37c-10 10-10 32 0 42" fill="none"/>
<circle cx="116" cy="74" r="22" fill="#ffffff"/><path d="M116 64l9 6-3 10h-12l-3-10z" fill="#26233a"/>
<path d="M14 98h132" fill="none"/>''',
"spl": '''
<rect x="16" y="54" width="128" height="44" rx="4" fill="#5cbf72"/><path d="M80 54v44" fill="none"/><circle cx="80" cy="76" r="10" fill="none"/>
<path d="M36 52V20h88v32" fill="none"/><path d="M36 20l10 10h68l10-10M46 30v22M114 30v22M58 30v22M70 30v22M82 30v22M94 30v22M104 30v22" fill="none" stroke-width="1.5"/>
<circle cx="108" cy="80" r="9" fill="#ffffff"/>''',
"big5": '''
<path d="M54 18h52v20c0 18-12 30-26 30S54 56 54 38z" fill="#ffcf4a"/>
<path d="M54 26H40c0 14 6 22 16 24M106 26h14c0 14-6 22-16 24" fill="none"/>
<path d="M74 68h12l2 14H72z" fill="#f2b632"/><rect x="60" y="82" width="40" height="16" rx="3" fill="#7a5c3a"/>
<path d="M80 30l3 6 6 1-4 4 1 6-6-3-6 3 1-6-4-4 6-1z" fill="#ffffff"/>''',
"intl": '''
<path d="M10 16q70 18 140 0" fill="none"/>
<path d="M22 19l8 18 8-16z" fill="#ff7b7b"/><path d="M48 23l7 18 9-17z" fill="#7cc4ff"/><path d="M76 25l8 18 8-18z" fill="#9be3b5"/><path d="M104 24l8 17 7-18z" fill="#ffd166"/><path d="M128 20l7 17 8-18z" fill="#c3a6ff"/>
<path d="M70 48l10 18 10-18" fill="#ff7b7b"/><circle cx="80" cy="78" r="20" fill="#ffcf4a"/><path d="M80 68l3 7 7 1-5 5 1 7-6-3-6 3 1-7-5-5 7-1z" fill="#ffffff"/>''',
"fifa": '''
<path d="M44 40h72c16 0 24 14 24 30 0 14-8 24-18 24-8 0-12-8-18-14H56c-6 6-10 14-18 14-10 0-18-10-18-24 0-16 8-30 24-30z" fill="#3b3f5c"/>
<path d="M44 56v16M36 64h16" fill="none" stroke="#ffffff"/><circle cx="110" cy="58" r="4" fill="#ff7b7b"/><circle cx="120" cy="66" r="4" fill="#7cc4ff"/><circle cx="100" cy="66" r="4" fill="#9be3b5"/><circle cx="110" cy="74" r="4" fill="#ffd166"/>''',
"anime": '''
<path d="M24 56h112c0 26-24 42-56 42S24 82 24 56z" fill="#e85d5d"/><path d="M60 98h40" fill="none"/>
<path d="M32 56c6-10 14-6 20-2s12 6 18-2 14-6 18 0 12 6 20 0 12-4 18 4" fill="#ffe7a3"/>
<ellipse cx="62" cy="50" rx="12" ry="9" fill="#ffffff"/><circle cx="62" cy="50" r="4" fill="#ffb627"/>
<circle cx="96" cy="48" r="9" fill="#ffffff"/><path d="M96 48m-4 0a4 4 0 1 1 4 4" fill="none" stroke="#ff7bb0"/>
<path d="M100 10l22 40M112 8l18 40" fill="none"/>''',
# ---------------- emoji (shared smiley base) ----------------
"emp": '''
<circle cx="64" cy="58" r="34" fill="#ffd23f"/><circle cx="52" cy="50" r="4" fill="#26233a"/><circle cx="76" cy="50" r="4" fill="#26233a"/><path d="M48 66c8 10 24 10 32 0" fill="none"/>
<path d="M122 92s-20-18-20-34a20 20 0 0 1 40 0c0 16-20 34-20 34z" fill="#e85d5d"/><circle cx="122" cy="58" r="7" fill="#ffffff"/>''',
"emf": '''
<circle cx="64" cy="58" r="34" fill="#ffd23f"/><circle cx="52" cy="50" r="4" fill="#26233a"/><circle cx="76" cy="50" r="4" fill="#26233a"/><path d="M46 62c4 14 32 14 36 0z" fill="#ffffff"/>
<circle cx="124" cy="76" r="20" fill="#ffffff"/><path d="M124 66l9 6-3 10h-12l-3-10z" fill="#26233a"/>''',
"ema": '''
<circle cx="64" cy="58" r="34" fill="#ffd23f"/><path d="M44 52l6-6 6 6M72 52l6-6 6 6" fill="none"/><path d="M50 66c8 8 20 8 28 0" fill="none"/>
<circle cx="44" cy="64" r="4" fill="#ff9bb3" stroke="none"/><circle cx="84" cy="64" r="4" fill="#ff9bb3" stroke="none"/>
<path d="M124 30l5 12 12 5-12 5-5 12-5-12-12-5 12-5z" fill="#ffffff"/><path d="M138 70l3 7 7 3-7 3-3 7-3-7-7-3 7-3z" fill="#ffd23f"/>''',
"emo": '''
<circle cx="56" cy="62" r="34" fill="#ffd23f"/><circle cx="44" cy="56" r="4" fill="#26233a"/><circle cx="68" cy="56" r="4" fill="#26233a"/><path d="M44 74h24" fill="none"/>
<path d="M92 14h56v36h-30l-12 12V50H92z" fill="#ffffff"/><path d="M110 26v10M126 26v10" fill="none"/>''',
# ---------------- السعودية والتحديات ----------------
"ksa": '''
<circle cx="30" cy="28" r="12" fill="#ffcf4a"/>
<path d="M96 102l4-78c8-6 16-6 24 0l4 78z" fill="#6b8fd6"/><path d="M104 30c5-3 11-3 16 0l-8 32z" fill="#dbe7fb"/><path d="M100 74c8-4 16-4 24 0" fill="none"/>
<path d="M50 102l5-48h6l3 48z" fill="#a8693e"/>
<path d="M58 54c-10-10-24-10-32-4 10 0 20 2 32 4zM58 54c8-12 22-14 32-8-10 0-22 4-32 8zM58 54c-14-2-24 6-26 16 8-8 18-12 26-16zM58 54c12 0 22 8 24 18-8-8-16-14-24-18zM58 54c0-12 6-20 14-24-6 8-10 16-14 24z" fill="#3fa66b"/>
<path d="M14 102h132" fill="none"/>''',
"dial": '''
<path d="M16 18h74v40H44l-14 14V58H16z" fill="#ffffff"/><circle cx="36" cy="38" r="4" fill="#26233a"/><circle cx="53" cy="38" r="4" fill="#26233a"/><circle cx="70" cy="38" r="4" fill="#26233a"/>
<path d="M144 44H72v40h44l14 14V84h14z" fill="#ffe08a"/><path d="M86 58h44M86 70h28" fill="none"/>''',
"where": '''
<path d="M18 30l38-12 48 12 38-12v66l-38 12-48-12-38 12z" fill="#cde8c3"/><path d="M56 18v66M104 30v66" fill="none"/>
<path d="M30 70c10-8 20 4 30-4s20-10 30 0" fill="none" stroke-dasharray="4 5"/>
<path d="M100 66s-16-14-16-27a16 16 0 0 1 32 0c0 13-16 27-16 27z" fill="#e85d5d"/><circle cx="100" cy="39" r="6" fill="#ffffff"/>''',
"math": '''
<rect x="52" y="12" width="56" height="88" rx="8" fill="#3b3f5c"/><rect x="60" y="20" width="40" height="18" rx="3" fill="#c7f0d8"/>
<circle cx="66" cy="50" r="5" fill="#ffffff"/><circle cx="80" cy="50" r="5" fill="#ffffff"/><circle cx="94" cy="50" r="5" fill="#ff9f43"/>
<circle cx="66" cy="64" r="5" fill="#ffffff"/><circle cx="80" cy="64" r="5" fill="#ffffff"/><circle cx="94" cy="64" r="5" fill="#ff9f43"/>
<circle cx="66" cy="78" r="5" fill="#ffffff"/><circle cx="80" cy="78" r="5" fill="#ffffff"/><circle cx="94" cy="90" r="5" fill="#ff9f43"/><circle cx="94" cy="78" r="5" fill="#ff9f43"/>
<path d="M22 40h16M30 32v16M122 76h18" fill="none"/><circle cx="131" cy="67" r="2.5" fill="#26233a"/><circle cx="131" cy="85" r="2.5" fill="#26233a"/>''',
"rid": '''
<path d="M24 34h22a8 8 0 1 1 16 0h22v22a8 8 0 1 0 0 16v22H24z" fill="#9b8cff"/>
<path d="M84 34h22a8 8 0 1 0 16 0h22v60h-22a8 8 0 1 1-16 0H84V72a8 8 0 1 1 0-16z" fill="#ff9f43"/>
<text class="t" x="54" y="80" fill="#ffffff" style="font-size:30px">؟</text>''',
"mov": '''
<rect x="22" y="40" width="96" height="58" rx="6" fill="#3b3f5c"/><path d="M22 40l8-18 92 0-4 18z" fill="#ffffff"/><path d="M40 22l-6 18M62 22l-6 18M84 22l-6 18M106 22l-6 18" fill="none"/>
<path d="M58 56v28l24-14z" fill="#ffd166"/>
<path d="M126 60h20l-4 40h-12z" fill="#ff7b7b"/><circle cx="130" cy="54" r="6" fill="#fff6d5"/><circle cx="140" cy="52" r="6" fill="#fff6d5"/><circle cx="135" cy="46" r="6" fill="#fff6d5"/>''',
"vg": '''
<rect x="44" y="12" width="72" height="90" rx="10" fill="#9be3b5"/><rect x="54" y="22" width="52" height="38" rx="4" fill="#3b3f5c"/>
<path d="M64 46h8v-8h8v8h8" fill="none" stroke="#ffd166"/><path d="M60 78h14M67 71v14" fill="none"/><circle cx="96" cy="74" r="5" fill="#ff7b7b"/><circle cx="88" cy="84" r="5" fill="#7cc4ff"/>
<path d="M18 30l8 8M142 30l-8 8M18 80l8-6M142 80l-8-6" fill="none"/>''',
"kid": '''
<path d="M30 98V54l20-14 20 14v44z" fill="#ff9f43"/><path d="M50 40l-24 16M50 40l24 16" fill="none"/>
<rect x="84" y="62" width="34" height="34" rx="4" fill="#7cc4ff"/><text class="t" x="101" y="90" fill="#26233a">ب</text>
<rect x="118" y="70" width="26" height="26" rx="4" fill="#ffd166"/><circle cx="50" cy="70" r="8" fill="#fff6d5"/>
<path d="M118 34l4 9 10 1-7 7 2 10-9-5-9 5 2-10-7-7 10-1z" fill="#ffd23f"/><path d="M14 98h132" fill="none"/>''',
"car": '''
<path d="M22 76l8-20c3-6 8-10 16-10h50c8 0 14 4 18 10l14 16 12 4c4 1 6 4 6 8v8H22z" fill="#ff7b7b"/>
<path d="M50 54h22v16H42zM80 54h18l12 16H80z" fill="#cdeaff"/>
<circle cx="50" cy="92" r="12" fill="#3b3f5c"/><circle cx="50" cy="92" r="4" fill="#ffffff"/><circle cx="118" cy="92" r="12" fill="#3b3f5c"/><circle cx="118" cy="92" r="4" fill="#ffffff"/>
<path d="M8 104h144" fill="none"/>''',
"food": '''
<ellipse cx="80" cy="84" rx="62" ry="16" fill="#ffffff"/>
<path d="M36 80c0-24 20-40 44-40s44 16 44 40z" fill="#f2c14e"/>
<path d="M50 64c6-4 12-2 16 2M78 56c6-4 12-2 16 2M98 68c6-4 12-2 16 2" fill="none"/>
<path d="M62 40c-8-8-6-16 2-20 4 6 2 12-2 20zM84 34c-6-10 0-18 8-18 2 8-2 12-8 18z" fill="#5cbf72"/>
<circle cx="66" cy="72" r="4" fill="#e85d5d"/><circle cx="92" cy="66" r="4" fill="#e85d5d"/><circle cx="106" cy="76" r="4" fill="#7a5c3a"/>''',
"spc": '''
<path d="M62 22l18 18 18-18" fill="none"/><circle cx="62" cy="20" r="3" fill="#26233a"/><circle cx="98" cy="20" r="3" fill="#26233a"/>
<rect x="30" y="40" width="100" height="62" rx="10" fill="#c98a4b"/><rect x="40" y="48" width="64" height="46" rx="8" fill="#7cc4ff"/>
<circle cx="72" cy="71" r="11" fill="#ffd166"/><ellipse cx="72" cy="71" rx="20" ry="5" fill="none" transform="rotate(-18 72 71)"/>
<circle cx="117" cy="58" r="5" fill="#3b3f5c"/><circle cx="117" cy="74" r="5" fill="#3b3f5c"/><path d="M112 86h10" fill="none"/>
<path d="M50 56l2 4 4 1-3 3 1 4-4-2-4 2 1-4-3-3 4-1z" fill="#ffffff" stroke-width="1.5"/>''',
"b3": '''
<path d="M80 34c-14-8-34-10-52-6v66c18-4 38-2 52 6z" fill="#ffffff"/><path d="M80 34c14-8 34-10 52-6v66c-18-4-38-2-52 6z" fill="#ffffff"/><path d="M80 34v66" fill="none"/>
<path d="M36 44h34M36 54h28M36 64h32" fill="none" stroke-width="2"/>
<path d="M106 40l4 12 12-4-8 10 10 8-13 1 1 13-8-10-8 10 1-13-13-1 10-8-8-10 12 4z" fill="#ff9f43"/>
<path d="M20 22l8 8M140 22l-8 8M80 8v12" fill="none"/>''',
}

DESC = {
"huroof": "كل إجابة تبدأ بحرف معيّن — أول حرف هو المفتاح.",
"gk": "أسئلة منوّعة في كل مجال: معلومات عامة يعرفها المثقف.",
"isl": "السيرة، القرآن الكريم، الفقه، والتاريخ الإسلامي.",
"geo": "دول، أنهار، جبال، وقارات العالم.",
"his": "أحداث وشخصيات وحضارات من التاريخ.",
"lng": "نحو، معاني كلمات، وأدب وشعر عربي.",
"sci": "فيزياء، كيمياء، أحياء، وجسم الإنسان.",
"tec": "حواسيب، إنترنت، شركات تقنية، واختراعات.",
"ani": "حيوانات البر والبحر والجو وطباعها.",
"cap": "خمّن عاصمة الدولة.",
"cur": "عملات دول العالم.",
"spt": "أسئلة رياضية عامة في مختلف الألعاب.",
"spl": "دوري روشن السعودي: أندية، لاعبون، وأرقام.",
"big5": "الدوريات الأوروبية الكبرى ودوري الأبطال.",
"intl": "كأس العالم والبطولات القارية للمنتخبات.",
"fifa": "سلسلة ألعاب فيفا وEA FC من ٢٠١٣ إلى ٢٠٢٧.",
"anime": "مسلسلات وشخصيات الأنمي المشهورة.",
"emp": "أماكن ومدن وأسماء مخفية في الإيموجي.",
"emf": "أندية ومنتخبات ولحظات كروية بالإيموجي.",
"ema": "مسلسلات وشخصيات أنمي بالإيموجي.",
"emo": "أمثال عربية وشعبية بالإيموجي.",
"ksa": "تاريخ المملكة، مدنها، معالمها، وثقافتها.",
"dial": "معاني كلمات من لهجات مناطق المملكة.",
"where": "من أي منطقة هذه العبارة أو الكلمة؟",
"math": "مسائل حساب ذهني سريعة.",
"rid": "ألغاز وفوازير تحتاج تفكير.",
"mov": "أفلام عالمية مشهورة: ممثلون، شخصيات، وجوائز أوسكار.",
"vg": "ألعاب الفيديو وأجهزتها وشخصياتها من أتاري إلى اليوم.",
"kid": "أسئلة سهلة تناسب الأطفال ليشاركوا في اللعب.",
"car": "شركات السيارات وشعاراتها وموديلاتها وسباقاتها.",
"spc": "أنمي الطفولة المدبلج الذي عُرض على سبيستون والقنوات العربية.",
"b3": "أسئلة متعمّقة في أشهر ثلاث سلاسل أنمي: ون بيس وناروتو ودراغون بول.",
"food": "أكلات سعودية وعربية وعالمية، وتمور وتوابل.",
}

if __name__ == "__main__":
    assert set(ART) == set(DESC)
    json.dump({"art": {k: " ".join(v.split()) for k, v in ART.items()}, "desc": DESC},
              open(sys.argv[1], "w"), ensure_ascii=False, indent=0)
    print(len(ART), "illustrations")
