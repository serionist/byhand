"""Plain Arabic work text, invented, in Modern Standard Arabic and in dialect, against the real catalogue. A strong or
usual sign counts alone, so one that fires on any of these accuses a person of writing like a machine. Office Arabic
runs on set phrases (تحية طيبة وبعد, السلام عليكم ورحمة الله وبركاته, نرجو التكرم, وتفضلوا بقبول فائق الاحترام), and
on what humanizer-ar lists and every office writes: تجدر الإشارة إلى, علاوة على ذلك, في هذا السياق, تم with a verbal
noun, قام بإجراء, نقلة نوعية, لا يقتصر… بل, وفي الختام, يمكن القول, أتمنى أن يكون هذا مفيدًا. Formal Arabic joins
long sentences with و (humanizer-ar's formal sample has a median of 35 words), marks some words and not others
(شكرًا, تُستخدم, كلٌّ), and ends a Hijri year with هـ. Chat is in dialect, Egyptian, Gulf, Levantine and Maghrebi,
mixes in standard Arabic and English, and stretches a word with the tatweel. They are a person's, never a sign. A weak
sign may fire, but plain work text must not reach a cluster.

Arabic typography is how people write too: ، ؛ ؟ and « », Arabic-Indic digits beside Western ones, a right-to-left mark
from a phone, a dash and straight quotes. The tatweel, the dashes and the invisible mark are written as escapes, as
ruff refuses them in source or no editor shows them; the first test holds that they are the real ones."""

import unicodedata

import pytest

from byhand import signs

TATWEEL, RLM = "\N{ARABIC TATWEEL}", "\N{RIGHT-TO-LEFT MARK}"
EN, EM = "\N{EN DASH}", "\N{EM DASH}"
FATHATAN, SHADDA = "\N{ARABIC FATHATAN}", "\N{ARABIC SHADDA}"
HIJRI = "\N{ARABIC LETTER HEH}" + TATWEEL  # the era after a Hijri year
# What an Arabic draft loads: the `any` signs and Arabic's, never another language's.
ARABIC = ("any", "ar")


def _text(*lines: str) -> str:
    """Lines of a text, joined: a newline escape written against an Arabic word reads to ruff as a mixed-script word."""
    return "\n".join(lines)


MAIL = [
    _text(
        "السادة شركة النور للتوريدات المحترمين،",
        "",
        "تحية طيبة وبعد،",
        "",
        "نرفق لكم فاتورة شهر أكتوبر رقم 4521، ونرجو التكرم بسدادها قبل نهاية الشهر الجاري.",
        "",
        "وتفضلوا بقبول فائق الاحترام،",
        "إدارة الحسابات",
    ),
    _text(
        "سعادة مدير إدارة الموارد البشرية المحترم،",
        "",
        "السلام عليكم ورحمة الله وبركاته، وبعد،",
        "",
        "فأفيدكم بأنني تقدمت بطلب إجازة اعتيادية لمدة عشرة أيام اعتبارًا من يوم الأحد الموافق 15 ربيع الآخر 1447"
        + HIJRI
        + "، وقد سلّمت المهام الجارية إلى الزميل أحمد العتيبي وأطلعته على ملفات العملاء المفتوحة واتفقنا على أن يتابع "
        "معاملات التوريد ويرد على استفسارات الفروع ويرفع تقريرًا أسبوعيًا إلى المشرف، وسأكون متاحًا على الهاتف عند "
        "الحاجة.",
        "",
        "وتفضلوا بقبول خالص التحية والتقدير،",
        "محمد الشمري",
    ),
    _text(
        "الزملاء الأعزاء،",
        "",
        "تجدر الإشارة إلى أن نظام الحضور الجديد يبدأ العمل يوم الأحد. علاوة على ذلك، تم تحديث بطاقات الدخول لجميع "
        "الموظفين، ويرجى استلامها من الاستقبال.",
        "",
        "مع التحية،",
        "شؤون الموظفين",
    ),
    _text(
        "عزيزتي سارة،",
        "",
        "شكرًا جزيلًا على ملاحظاتك على العرض. أرسلت النسخة المعدلة إلى العميل صباح اليوم، وسأخبرك بردّه.",
        "",
        "تحياتي،",
        "ليلى",
    ),
    _text(
        "الأستاذ خالد المحترم،",
        "",
        "في هذا السياق، نود إعلامكم بأن موعد تسليم المشروع تأجل إلى ٢٠ نوفمبر بسبب تأخر وصول المعدات.",
        "",
        "وفي الختام، نشكركم على تفهمكم.",
        "",
        "مع خالص التقدير،",
        "فريق المشروع",
    ),
    _text(
        "مرحبا أستاذة هدى،",
        "",
        "قام الفريق بإجراء الاختبارات على النسخة الجديدة من التطبيق، ولم نجد أخطاء تُذكر. هل يناسبك اجتماع يوم "
        "الثلاثاء؟",
        "",
        "مع الشكر،",
        "يوسف",
    ),
    _text(
        "عميلنا العزيز،",
        "",
        "نعتذر عن التأخير في توصيل طلبكم رقم 88213. سيصلكم الطلب يوم الخميس القادم بإذن الله.",
        "",
        "نتمنى لكم يومًا سعيدًا،",
        "خدمة العملاء",
    ),
    _text(
        "أخي العزيز عمر،",
        "",
        "أرفقت لك جدول الرواتب وملاحظات المحاسب، وأتمنى أن يكون الجدول مفيدًا. وإذا احتجت أي توضيح، أخبرني.",
        "",
        "أخوك،",
        "فهد",
    ),
    _text(
        "سعادة الدكتور فيصل،",
        "",
        "يسعدني دعوتكم لحضور حفل تكريم الموظفين المتميزين يوم الأربعاء 12 جمادى الأولى 1447"
        + HIJRI
        + " في قاعة الملك فهد، الساعة السابعة مساءً.",
        "",
        "دمتم بخير،",
        "عبدالله القحطاني",
    ),
    _text(
        "يا جماعة صباح الخير،",
        "",
        "الاجتماع بكرة الساعة 10 في أوضة الاجتماعات الكبيرة، ياريت كله يجيب اللابتوب.",
        "",
        "شكراً،",
        "منى",
    ),
    _text(
        RLM + "مرحبا فريق IT،",
        "",
        "ال" + TATWEEL + "VPN لا يعمل من المنزل منذ الصباح، ورسالة الخطأ: Connection timed out. ممكن تساعدوني؟",
        "",
        "شكرًا،",
        "رنا",
    ),
    _text(
        "حضرة المهندس سامي المحترم،",
        "",
        "بالإشارة إلى خطابكم المؤرخ في 3/11/2025م، نفيدكم بأنه تم اعتماد المخططات المعدلة، وعليه نأمل البدء في أعمال "
        "الحفر خلال أسبوعين.",
        "",
        "والله ولي التوفيق،",
        "مكتب الإشراف الهندسي",
    ),
    _text(
        "صباح الخير أستاذ وليد،",
        "",
        "في ضوء ما ناقشناه أمس، أرسلت لك جدول المهام المحدّث؛ يُرجى مراجعته قبل اجتماع الخميس.",
        "",
        "مع الشكر والتقدير،",
        "نادية",
    ),
]
REPLIES = [
    "بالطبع، إليك نسخة من رسالتك:",
    "بالطبع! إليك نسخة معدلة من العقد:",
    "بالطبع، إليك النسخة الأخيرة من العرض:",
    "بالطبع! إليك رابط الملف:",
    "بالتأكيد، إليك نسختي المعدلة من التقرير:",
    "بالطبع، إليك نسخة مختصرة من الفاتورة، والأصل في البريد:",
    # a person's role or verdict, near the model's role and its lack (#53's review, rounds 1 to 4)
    "نستخدمه كمساعد ذكاء اصطناعي، لا كبديل عن المحاسب.",
    "كمساعد إداري، لا أملك القدرة على اعتماد المصروفات.",
    "لا أملك القدرة على الحضور غدًا، أعتذر.",
    "كمساعد ذكاء اصطناعي، لا بأس به، لكنه يخطئ في التواريخ.",
    "اشترينا Copilot كمساعد ذكاء اصطناعي، لا أملك القدرة على تقييمه بعد.",
    "جربنا Gemini أسبوعين. كمساعد ذكاء اصطناعي، لا أملك القدرة على تقييمه بعد، لكن الفريق مرتاح له.",
    "رأيي في Copilot؟ كمساعد ذكاء اصطناعي، لا أملك القدرة على الحكم عليه قبل نهاية التجربة.",
    "بخصوص الأداة الجديدة: كمساعد ذكاء اصطناعي، لا أملك القدرة على دفع اشتراكها من ميزانية القسم.",
    "حسب آخر تحديث لمعلوماتي، المخزون 12 كرتونة.",
    "حتى آخر تحديث للنظام كان الرصيد سليمًا.",
]
CHAT = [
    "تمام، هبصله وأرد عليك",
    "أنا جاي في الطريق، عشر دقايق بالكتير 🙏",
    "حد معاه لينك الدرايف بتاع المشروع؟",
    "ماشي يا باشا، بكرة إن شاء الله",
    "وش صار على الاجتماع؟ تأجل ولا لا؟",
    "إن شاء الله أرسله لك اليوم، بس أخلص التقرير",
    "يعطيك العافية، وصلني الملف",
    "شو رأيك نأجلها لبكرا؟ اليوم مضغوطين كتير",
    "تمام، بشوفك بالمكتب الساعة ٩",
    "واش كاين شي جديد على الكونطرا؟",
    "صافي، غدا نكملو الخدمة",
    "ok, 7ader, ba3ateh bokra",
    "مب" + TATWEEL * 3 + "روك يا أحمد على الترقية 🎉",
    "شك" + TATWEEL * 3 + "رًا يا شباب",
    "يا جماعة، يرجى تحديث الملف قبل الساعة 5، عشان المدير هيراجعه النهارده",
    "سؤال رائع، ما عندي فكرة 😅",
    "والله ما أدري، اسأل نورة",
    "الحمد لله، وصلنا بالسلامة",
]
NOTES = [
    _text(
        "محضر اجتماع لجنة المشتريات " + EN + " 6 نوفمبر",
        "الحضور: أ. سالم، م. ريم، د. ناصر",
        "- اعتماد ميزانية 2027",
        "- طرح مناقصة التنظيف",
        "- الاجتماع القادم: 4 ديسمبر",
    ),
    _text(
        "ملاحظات:",
        "- الاتصال بالمحامي",
        "- إرسال العقد إلى باسل [قيد الانتظار]",
        "- مراجعة تاريخ التسليم [للتأكيد]",
    ),
    "مواعيد العمل: من الأحد إلى الخميس، ٨ صباحًا " + EN + " ٤ مساءً.",
    "**هام**: ابتداءً من الأحد، بطاقة الدخول إلزامية.",
    "قال المدير: «سنوقّع العقد الأسبوع القادم»، ولا أريد أن أستبق الأحداث.",
    "التاريخ: 18/5/1447" + HIJRI + " الموافق 9/11/2025م",
    _text("مهام الأسبوع:", "1. إقفال الشهر", "2. سداد الموردين", "3. مراجعة عقد الإيجار"),
]
REPORTS = [
    _text(
        "ملخص الدراسة",
        "",
        "تهدف هذه الدراسة إلى تحليل أثر العمل عن بعد على إنتاجية موظفي القطاع المصرفي في الرياض، وتسلط الضوء على دور "
        "المدير المباشر. تم توزيع الاستبانة على 412 موظفًا في ستة بنوك، وتمت معالجة الردود في برنامج R.",
    ),
    _text(
        "التقرير السنوي للجمعية",
        "",
        "صار أقرب مستوصف على بعد خمس دقائق بدل أربعين، وكان افتتاحه في مارس نقلة نوعية لكبار السن في الحي. علاوة على "
        "ذلك، وقّعنا مع كلية التمريض اتفاقية لتدريب 30 متطوعًا، وهي حجر الزاوية في خطة العام القادم.",
    ),
    _text(
        "تقرير صحفي",
        "",
        "سلطت الصحف المحلية الضوء على أزمة المواقف في وسط المدينة. وأعلنت الأمانة عن 600 موقف جديد قرب سوق الزل.",
    ),
    _text("التوصيات", "", "وفي الختام، توصي اللجنة بتمديد العقد سنة واحدة ومراجعة الأسعار في الربع الأول."),
    _text(
        "خبر",
        "",
        "منحت سلطة الطيران المدني الضوء الأخضر لتشغيل الرحلات الداخلية من مطار العلا، في ضوء نتائج التفتيش.",
    ),
    _text(
        "قرار إداري",
        "",
        "بناءً على الصلاحيات الممنوحة لنا، وبعد الاطلاع على محضر اللجنة، وعلى توصية إدارة الشؤون القانونية، وحرصًا على "
        "انتظام العمل، تقرر تكليف الأستاذ ماجد الزهراني بمهام مدير الفرع اعتبارًا من 1/6/1447"
        + HIJRI
        + "، وعلى الجهات المعنية تنفيذ القرار كلٌّ فيما يخصه.",
    ),
    _text(
        "دليل المستخدم",
        "",
        "اضغط على [إدراج] واختر «جدول». يمكن للنظام إرسال تنبيه بالبريد الإلكتروني، وتُحفظ التقارير لمدة 90 يومًا.",
    ),
    _text(
        "المراجعة الداخلية",
        "",
        "لا يقتصر التدقيق على الإدارة المالية، بل يشمل المشتريات والمخازن أيضًا. تسلّم الإدارات بياناتها قبل يوم 20 من "
        "الشهر.",
    ),
    _text(
        "ملخص تنفيذي",
        "",
        "يسلط هذا التقرير الضوء على نتائج الربع الثالث في فروع المنطقة الشرقية.",
        "وفي الختام، يمكن القول إن الفرع حقق هدفه رغم تأخر التوريد.",
    ),
    _text(
        "تقرير الفحص",
        "",
        "تجدر الإشارة إلى أن مصعد المبنى (ب) متوقف منذ مارس بانتظار قطعة غيار من المورد. وفي هذا السياق، طلب المهندس "
        "المشرف مصعدًا مؤقتًا للطابق الخامس، ومن الجدير بالذكر أن الإيجار الشهري لا يتجاوز 4 آلاف ريال.",
    ),
    _text(
        "معرض الكتاب",
        "",
        "بلغ عدد زوار المعرض 18 ألفًا في ثلاثة أيام، مما يعكس اهتمام الأسر بالكتب المترجمة. وفي نهاية المطاف، يبقى "
        "مكان الوقوف التحدي الأكبر أمام الزوار.",
    ),
    _text(
        "الخاتمة",
        "",
        "وفي الختام، يمكن القول إن هذه الدراسة سلطت الضوء على واقع التعليم عن بعد في جامعة الملك عبدالعزيز، وقد "
        "أظهرت أن 62% من الطلاب يفضلون المحاضرات المسجلة.",
    ),
    _text("محضر لجنة", "", "ختامًا، نشكر جميع الأعضاء على حضورهم، ونتطلع إلى لقائكم في الاجتماع القادم."),
    _text(
        "خطة العمل",
        "",
        "أولًا: حصر الأصول. ثانيًا: تقييمها. ثالثًا: رفع التقرير إلى الإدارة العليا قبل نهاية الربع.",
    ),
]
POSTS = [
    "بعد ست سنوات في شركة الأفق للخدمات اللوجستية، أودّعكم اليوم. شكرًا لسارة وأحمد على جرد أيام الجمعة. أبدأ في شركة "
    "المسار يوم 2 ديسمبر. #الرياض #لوجستيات",
    "افتتاح فرعنا الجديد في شارع التحلية يوم السبت 🎉 قهوة وكعك للجميع من 10 الصبح ل" + TATWEEL + " 1 الظهر!",
    "الحمد لله، خلصنا حملة التشجير: 40 متطوع و300 شتلة. شكرًا للجميع 🌱",
    "سعداء بانضمام م. ريم الحربي إلى فريق التصميم. ريم عملت خمس سنوات في مشاريع الإسكان بجدة، ومرحبًا بها بيننا.",
]
TYPOGRAPHY = [
    "اللجنة " + EM + " وهي ثلاثة أعضاء " + EM + " تجتمع كل خميس بعد الظهر.",
    'قال: "نعم، سنحضر" ثم غادر.',
    "السعر: 1,250.50 ريال (شامل الضريبة). المدة: 3" + EN + "5 أيام عمل.",
    "السعر: ١٢٥٠ ريالًا، والتسليم خلال ٣ أيام؛ والدفع عند الاستلام.",
    RLM + "هل وصلك الملف؟ أرسلته الساعة 3:15 م.",
]

OFFICE = MAIL + REPLIES + CHAT + NOTES + REPORTS + POSTS + TYPOGRAPHY

KINDS = [
    *((text, "email") for text in MAIL + REPLIES),
    *((text, "message") for text in CHAT),
    *((text, "document") for text in NOTES + REPORTS + TYPOGRAPHY),
    *((text, "post") for text in POSTS),
]


def test_the_marks_are_the_real_ones():
    # an escape that lost its backslash would leave the lines holding ASCII, and the test passing on nothing
    assert unicodedata.name(TATWEEL) == "ARABIC TATWEEL"
    assert unicodedata.name(RLM) == "RIGHT-TO-LEFT MARK"
    assert sum(TATWEEL in text for text in OFFICE) >= 6
    assert sum(FATHATAN in text for text in OFFICE) >= 15
    assert sum(SHADDA in text for text in OFFICE) >= 5
    assert sum(RLM in text for text in OFFICE) >= 2
    for mark in "،؛؟«":
        assert any(mark in text for text in OFFICE), mark
    assert len(OFFICE) >= 60


@pytest.mark.parametrize(("text", "kind"), KINDS)
def test_no_sign_that_counts_alone_fires_on_plain_arabic_work_text(counted_alone, reads, text, kind):
    fired = [sign.id for sign in counted_alone if reads(sign, kind) and sign.pattern and sign.pattern.search(text)]
    assert fired == []


def test_no_arabic_check_counts_alone(counted_alone):
    # Until a native speaker reads them, every Arabic sign with a pattern is weak (#49): an Arabic sign with a pattern
    # that counts alone needs its lines in MACHINE below, a line per branch of its check.
    assert [sign.id for sign in counted_alone if sign.language == "ar"] == []


def test_every_arabic_sign_is_weak_until_a_native_review(catalogue):
    # stricter than the plan, which lets a usual or strong sign with no pattern in: none of these sources settles one
    assert [sign.id for sign in catalogue.signs.values() if sign.language == "ar" and sign.strength != "weak"] == []


# What each sign that counts alone exists to catch, inside Arabic text: a line per Arabic branch of its check, and one
# for each artefact, which is the same string in every language, so silence above can't come from a sign that finds
# nothing. Branches that read other languages' words have their lines in the other office tests.
MACHINE = [
    ("any-ai-self-reference", "كمساعد ذكاء اصطناعي، لا أملك القدرة على تصفح الإنترنت."),
    ("any-ai-self-reference", "عذرًا، لكن كمساعد ذكاء اصطناعي لا أملك القدرة على الوصول إلى الإنترنت."),
    ("any-ai-self-reference", "ولكن، كمساعد ذكاء اصطناعي، لا أملك القدرة على إبداء رأي شخصي."),
    ("any-ai-self-reference", "سؤالك مهم. كمساعد ذكاء اصطناعي لا أملك القدرة على التنبؤ بالأسعار."),
    ("any-assistant-preamble", "بالطبع! إليك نسخة محسّنة من رسالتك:"),
    ("any-assistant-preamble", "بالطبع، إليك صيغة أكثر رسمية من بريدك الإلكتروني:"),
    ("any-assistant-preamble", "بالطبع! إليك النسخة المعدلة من سيرتك الذاتية:"),
    ("any-assistant-preamble", "بالطبع. إليك نسخة مختصرة لمنشورك على لينكدإن:"),
    ("any-assistant-preamble", "بالطبع! إليك نسخة منقحة من خطابكم:"),
    ("any-assistant-preamble", "بالطبع! إليك نسخة أوضح من ردك:"),
    ("any-assistant-preamble", "بالطبع! إليك نسخة أقصر من نصك:"),
    ("any-assistant-preamble", "بالطبع! إليك نسخة معدّلة من مقالك، بلغة أبسط:"),
    ("any-emoji-markers", "- 🚀 عرض تدريبي جديد"),
    ("any-emoji-markers", "## 📊 أرقام الشهر"),
    ("any-unfilled-placeholder", "التسجيل: insert_link_here"),
    ("any-chatgpt-citation-markup", "ارتفعت المبيعات. :contentReference[oaicite:0]{index=0}"),
    ("any-chatgpt-citation-markup", "ارتفعت المبيعات. turn0search4"),
    ("any-chatbot-url-tag", "المصدر: https://example.sa/report?utm_source=chatgpt.com"),
    ("any-gemini-citation-markup", "افتُتح المصنع عام 1998 [cite: 3]."),
    ("any-grok-citation-markup", "افتُتح المصنع عام 1998. grok_card"),
    ("any-deepseek-citation-markup", "افتُتح المصنع عام 1998【4†source】."),
    ("any-chat-tool-markup", "حسب الملف المرفق[attached_file:1]، ينخفض الهامش."),
]


@pytest.mark.parametrize(("sign", "text"), MACHINE)
def test_the_signs_still_find_what_they_are_for_in_arabic(counted_alone, sign, text):
    pattern = {found.id: found.pattern for found in counted_alone}[sign]
    assert pattern is not None
    assert pattern.search(text), sign


@pytest.mark.parametrize(("text", "kind"), KINDS)
def test_plain_arabic_work_text_makes_no_weak_cluster(weak_hits, text, kind):
    for paragraph in text.split("\n\n"):
        assert weak_hits(paragraph, kind, ARABIC) < signs.WEAK_CLUSTER, paragraph


def test_the_weak_counting_counts_a_cluster(weak_hits):
    # so the test above can fail: three different weak habits in one paragraph of a document
    text = "سؤال رائع! يسلط هذا التقرير الضوء على **الفروع الثلاثة**."
    assert weak_hits(text, "document", ARABIC) == signs.WEAK_CLUSTER


def test_one_habit_repeated_counts_once(weak_hits):
    text = "يسلط التقرير الضوء على المبيعات، ويسلط الضوء على المخزون، ثم يسلط الضوء على الفروع."
    assert weak_hits(text, "document", ARABIC) == 1


def test_the_arabic_checks_read_posts_and_documents(catalogue):
    # the set phrases of mail and chat (تحية طيبة وبعد, وتفضلوا بقبول فائق الاحترام, يعطيك العافية) would add up there:
    # no Arabic sign that reads mail or chat has a pattern. The one Arabic form of a weak `any` check that reads every
    # kind, سؤال رائع!, needs its exclamation mark, and CHAT holds the person's comma.
    reading_mail = [
        sign.id
        for sign in catalogue.signs.values()
        if sign.language == "ar" and sign.pattern and {"any", "email", "message"} & set(sign.kinds)
    ]
    assert reading_mail == []


# Arabic joins و, ف, ل and ب to the next word, puts the verb before its subject and marks some words and not others:
# the forms a weak check must still find, beyond its own `flags`, and the plain forms it must leave alone.
FORMS = [
    ("ar-shed-light", "يسلط هذا التقرير الضوء على المبيعات."),
    ("ar-shed-light", "تسلط الدراسة الحالية الضوء على دور المعلم."),
    ("ar-shed-light", "تسلط هذه الورقة البحثية الضوء على سوق العمل."),
    ("ar-shed-light", "سلطت الدراسة الضوء على العمل عن بعد."),
    ("ar-shed-light", "نسلّط الضوء اليوم على فريق المبيعات."),
    ("ar-shed-light", "يهدف المقال إلى تسليط الضوء على المشروع."),
    ("ar-shed-light", "وتسليط الضوء على التجربة مهم."),
    ("ar-shed-light", "خصصنا العدد لتسليط الضوء على المتطوعين."),
    ("ar-shed-light", "ولتسليط الضوء على التجربة، نشرنا الأرقام."),
    ("ar-shed-light", "وبتسليط الضوء على الفريق نختم العدد."),
    ("any-flattering-agreement", "سؤال رائع! لنبدأ بالميزانية."),
    ("any-raw-markdown", "شكرًا على التحديث. **نقطتان** للتعديل."),
]

LEFT_ALONE = [
    ("ar-shed-light", "منحت سلطة الطيران المدني الضوء الأخضر للرحلات."),
    ("ar-shed-light", "في ضوء النتائج، نوصي بتمديد العقد."),
    ("ar-shed-light", "أطفأ الحارس الضوء في المستودع."),
    ("ar-shed-light", "السلطات أطفأت الضوء في الشارع بعد منتصف الليل."),
    ("ar-shed-light", "الأمير سلطان افتتح الحديقة، والضوء خافت فيها."),
    ("ar-shed-light", "يعرض التقرير أرقام الربع الثالث بالتفصيل."),
    # humanizer-ar's closer is a person's too: the closing summary has no Arabic form (#58's review, F1)
    ("any-closing-summary", "وفي الختام، يمكن القول إن الخطة نجحت."),
    ("any-closing-summary", "وفي الختام، نشكركم على تعاونكم."),
    ("any-closing-summary", "ختامًا، أتمنى لكم التوفيق."),
    ("any-closing-summary", "وفي النهاية وافقت اللجنة على العرض."),
    ("any-flattering-agreement", "سؤال رائع، ما عندي فكرة."),
]


@pytest.mark.parametrize(("sign", "text"), FORMS)
def test_a_weak_arabic_check_finds_its_forms(catalogue, sign, text):
    pattern = catalogue.signs[sign].pattern
    assert pattern is not None
    assert pattern.search(text), sign


@pytest.mark.parametrize(("sign", "text"), LEFT_ALONE)
def test_a_weak_arabic_check_leaves_plain_forms_alone(catalogue, sign, text):
    pattern = catalogue.signs[sign].pattern
    assert pattern is not None
    assert not pattern.search(text), sign
