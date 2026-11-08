"""Plain Hungarian work text, invented, against the real catalogue. A strong or usual sign counts alone, so one that
fires on any of these accuses a person of writing like a machine. Office Hungarian (the "kerül" passive, "-val
kapcsolatban", magázás with a capital Ön) and Hungarian typography (low-high quotes, straight quotes, the spaced short
dash) are a person's, never a sign. A weak sign may fire: it counts only in a cluster, and plain work text must not make
one.

Names and towns appear in their right inflected forms, and product names with the hyphen people give them: the two
Hungarian checks that count alone are about those endings. The quotes and dashes are written as escapes, as ruff refuses
them in source; the first test holds that they are the real marks."""

import re
import unicodedata

import pytest

from byhand import signs

LOW, HIGH, OPEN, EN, EM = "\u201e", "\u201d", "\u201c", "\u2013", "\u2014"

MAIL = [
    "Tisztelt Kovács Úr!\n\nMellékelten küldöm a második negyedéves elszámolást. Kérdés esetén keressen bátran a "
    "+36 30 123 4567-es számon.\n\nTisztelettel:\nSzabó Júlia",
    "Kedves Anna!\n\nKöszönöm a gyors választ. A szerződést holnap délelőtt átküldöm, kérlek, nézd át péntekig.\n\n"
    "Üdv,\nPéter",
    "Kedves Péter,\nköszönöm a levelet, holnap visszahívlak.\nÜdv,\nZsófi",
    "Kedves Kollégák!\n\nEmlékeztetőül: holnap 9-kor tűzriadó-gyakorlat lesz. A gyülekezőhely a parkoló.\n\n"
    "Üdvözlettel:\nHR",
    "Tisztelt Ügyfelünk!\n\nTájékoztatjuk, hogy a számlázási rendszer frissítése miatt december 3-án 18 és 22 "
    "óra között az ügyfélkapu nem érhető el. Megértését köszönjük.",
    "Kedves Réka!\n\nAnnával és Bencével egyeztettem, csütörtökön 10-kor jó mindenkinek. Zsófiától még várok "
    "választ.\n\nÜdv,\nGergő",
    "Tisztelt Nagy Úr!\n\nA szállás biztosítva, az étkezést a helyszínen intézzük. A parkolás nem megoldott, "
    "kérem, tömegközlekedéssel érkezzen.\n\nÜdvözlettel:\nKiss Erika",
    "Szia Bence!\n\nJövő héten Debrecenben leszek, utána Szegeden, a hónap végén pedig Győrben. Ha kell, Pécsre is "
    "le tudok menni.\n\nÜdv,\nCsaba",
    "Kedves Ilona!\n\nFontos, hogy a jelenléti íveket péntekig leadjátok. A bérszámfejtés hétfőn indul.\n\n"
    "Köszi,\nDóra",
    "Tisztelt Hölgyem!\n\nA vezetés döntése alapján az új rendszer bevezetésre kerül a második negyedévben. Az ezzel "
    "kapcsolatos kérdéseit kérem, jelezze.\n\nTisztelettel:\nVarga Attila",
    "Szia Petra!\n\nHa megjön az utalás, biztosítva lesz a fizetés is, addig nem tudok mit tenni.\n\nÜdv,\nLilla",
    "Kedves Mária!\n\nAz árak minden adót tartalmaznak, az áfát is. A szállítás 4500,"
    + EM
    + " Ft, Budapesten belül ingyenes.\n\nÜdvözlettel:\nNóra",
]

CHAT = [
    "Szia Bence, a holnapi meeting 10 helyett 11-kor lesz, a 3. emeleti tárgyalóban.",
    "Sziasztok! Ma home office-ból dolgozom, Teamsen elértek.",
    "Feltöltöttem a prezit a SharePointra, a Jira-ban is frissítettem a ticketet.",
    "Bocsi a késésért, dugóban ültem. 5 perc és ott vagyok.",
    "Segítesz feltölteni a táblázatot? Nekem nem megy a jogosultság miatt.",
    "Annával beszéltem, ő is jön csütörtökön. Rékának még szólni kell.",
    "Anna-Mária írt, hogy késik, kezdjétek nélküle.",
    "Ki írta a jegyzőkönyvet? Anna-e vagy Kata?",
    "Az Excel-ben van egy hiba, a második fül képlete rossz.",
    "Miközben a szerver újraindult, néhány kérés elveszett. Holnap megnézem a logokat.",
    "Sopronból jövök vonattal, Győrben átszállok, 9-re ott vagyok.",
    "Nyíregyházán és Kecskeméten is nyitottunk boltot, a többi jövőre jön.",
    "A kliens azt írta, hogy " + LOW + "sürgős" + HIGH + " " + EN + " szóval ma még kéne.",
    'A tárgyba írd be, hogy "Leltár 2025", különben a szűrő nem találja.',
    "Tegnapelőtt Egerben voltunk a csapattal, lenyűgöző volt a vár.",
    "Köszi! Nagyon szép volt a hétvégi esküvő.",
    # right Hungarian a wider check fired on (#28's review, F2 to F4): place endings in other senses, the KATA tax,
    # a participle that mirrors or that a subject follows, and the fontos phrase inside a sentence
    "Győrön keresztül megyünk, ott van a legkevesebb dugó.",
    "Debrecenen át jövünk, mert a 4-es úton terelés van.",
    "Sopronon át megyünk Bécsbe, onnan vonattal tovább.",
    "Veszprémen keresztül megyünk.",
    "Elküldtem a Debrecenről szóló jelentést a vezetésnek.",
    "A Győrre vonatkozó adatokat holnapig kérem.",
    "Végül Veszprémre esett a választás, ott lesz a tréning.",
    "Az Egerről készült fotókat feltöltöttem a SharePointra.",
    "Büszkék vagyunk Sopronra, ott a legjobb az elégedettség.",
    "Elegem van Budapestből, jövőre vidékre költözöm.",
    "Beleszeretett Budapestbe, nem is akar hazajönni.",
    "Jövőre kilépek a KATA-ból, átállok átalányadóra.",
    "A KATA-t tavaly szigorították, nézd meg a feltételeket.",
    "Még KATA-val vagy, vagy már átálltál?",
    "Az ikont tedd át a jobb sarokba, tükrözve a függőleges tengelyre.",
    "A helyszín a nagytárgyaló, biztosítva a kivetítő és a flipchart is.",
    "A meghívóban fontos kiemelni, hogy a parkolás fizetős.",
    "Most nem fontos kiemelni, hogy ki hibázott, inkább javítsuk ki.",
]

NOTES = [
    "Emlékeztető " + EN + " heti státusz, nov. 7.\n- Jelen: Anna, Bence, Csaba\n- Leltár: Sopronban kész, "
    "Szolnokon jövő héten\n- Következő alkalom: nov. 14., 10 óra",
    "TEENDŐK\n- árajánlat Kovács Kft.-nek\n- a 2026/0412-es számla ellenőrzése\n- kiküldetési kérelem Veszprémbe",
    "Jegyzet: a szerver (192.168.1.10) karbantartása szombaton 22" + EN + "24 óra között lesz.",
    "Összefoglalva: péntekig kell a jóváhagyás, különben csúszik a szállítás.",
    "## Szabadságok decemberben",
    "Ülés 10" + EN + "12 óráig, 3.14-es terem " + EN + " kérem, pontosan érkezzetek.",
    "Szabó Júlia\nértékesítési vezető\n" + EM * 12 + "\nTel.: +36 1 234 5678",
    "Belépődíj: 3000," + EM + " Ft, gyerekeknek ingyenes.",
    "Fontos kiemelni a határidőt a meghívóban, a múltkor többen lekésték.",
]

# a person handing over or returning their own draft
REPLIES = [
    "Itt vannak a tegnapi számok:",
    "Csatolom a megjegyzéseimet:",
    "Persze, itt a link:",
    "Átírtam a bevezetőt, nézd át, kérlek:",
    "Itt a rövidebb változat a hirdetőtáblára:",
    "Íme a végleges menetrend, ahogy megbeszéltük:",
    "Javítottam a táblázatot, a megjegyzéseitek benne vannak.",
]

REPORTS = [
    "A harmadik negyedévben a forgalom 4%-kal nőtt, főként az alkatrészüzletág miatt. Két új nagy ügyfelet is "
    "szereztünk. A bérköltség nem változott; a költségvetési tervezés keretében megvizsgáljuk, kell-e új kolléga.",
    "Az új ERP-rendszerre való átállás határidőn és költségkereten belül maradt. A raktári oktatás még hátravan. "
    "A licencekkel kapcsolatban november végéig jelentkezünk.",
    "Az ügyfél szempontjából a szállítási határidő kulcsfontosságú, ezért a gyártást két héttel előrehoztuk. A "
    "pótlólagos költség 1,2 millió forint.",
    "Az új jegykezelő lehetővé teszi, hogy a kollégák a hibákat a telefonjukról is bejelentsék. Az első hónapban 140 "
    "bejelentés érkezett.",
    "A felmérés átfogó volt: mind a 12 telephelyről érkezett válasz. A dolgozók fele a rugalmas munkaidőt tartja a "
    "legfontosabbnak.",
    "Jegyzőkönyv, irányítóbizottság, november 6.\n\n1. napirendi pont: Az Észak projekt mérföldköve teljesült. A "
    "Dél élesítése januárra csúszik.\n\n2. napirendi pont: A keret 20 millió forinttal nő a drágább hardver miatt.",
    "Az árak minden díjat tartalmaznak, beleértve a kiszállítást is. A szerződés egy évre szól, utána havonta "
    "felmondható.",
    "A rendszer kulcsfontosságú a beszerzés számára, és lehetővé teszi a rendelések nyomon követését. A bevezetés "
    "márciusban kezdődik.",
    "Fontos, hogy a leltárt december 15-ig lezárjuk. A raktár két napig zárva lesz, a kiszállítás szünetel.",
    "A pilot lezárult. Mindegyik telephely részt vett benne, a költség 8%-kal a terv alatt maradt.",
    "A tárolóként szolgáló konténert a hónap végén elszállítják. A bérleti díj 45 000 forint havonta.",
]

# posts a person writes: a short post on the company channel and a bakery's newsletter
POSTS = [
    "Ma tíz éve kezdtem itt gyakornokként. Köszönöm mindenkinek " + EN + " a konyhában van süti!",
    "A pékségünk a falu közepén van, kovászos kenyérrel és házi lekvárral. Szombatonként friss kalácsot is sütünk, "
    "decembertől beiglit.",
]

OFFICE = MAIL + CHAT + NOTES + REPLIES + REPORTS + POSTS
# Each text with the kind of writing it is: a sign counts alone only in the kinds it reads.
KINDS = [
    *((text, "email") for text in MAIL + REPLIES),
    *((text, "message") for text in CHAT),
    *((text, "document") for text in NOTES + REPORTS),
    *((text, "post") for text in POSTS),
]


def _reads(sign: signs.Sign, kind: str) -> bool:
    return bool({"any", kind} & set(sign.kinds))


@pytest.fixture(scope="module")
def catalogue():
    found, problems = signs.load()
    assert problems == []
    return found


@pytest.fixture(scope="module")
def counted_alone(catalogue):
    found = [sign for sign in catalogue.signs.values() if sign.pattern and sign.strength != "weak"]
    assert found
    return found


def test_the_marks_are_the_real_ones():
    # an escape that lost its backslash would leave the lines holding ASCII, and the test passing on nothing
    assert unicodedata.name(LOW) == "DOUBLE LOW-9 QUOTATION MARK"
    assert unicodedata.name(HIGH) == "RIGHT DOUBLE QUOTATION MARK"
    assert unicodedata.name(OPEN) == "LEFT DOUBLE QUOTATION MARK"
    assert unicodedata.name(EN) == "EN DASH"
    assert unicodedata.name(EM) == "EM DASH"
    assert sum(EN in text for text in OFFICE) >= 4
    assert len(OFFICE) >= 40


@pytest.mark.parametrize(("text", "kind"), KINDS)
def test_no_sign_that_counts_alone_fires_on_plain_hungarian_work_text(counted_alone, text, kind):
    fired = [sign.id for sign in counted_alone if _reads(sign, kind) and sign.pattern and sign.pattern.search(text)]
    assert fired == []


def test_the_hungarian_checks_that_count_alone_are_the_two_inflection_errors(counted_alone):
    # The maintainer (#4): a native speaker writes neither. Any other Hungarian check that counts alone needs its lines
    # in MACHINE and a reason.
    assert sorted(sign.id for sign in counted_alone if sign.language == "hu") == [
        "hu-hyphenated-case-ending",
        "hu-place-name-suffix",
    ]


# What each sign that counts alone exists to catch, inside Hungarian text: a line per branch of its Hungarian check, so
# silence above can't come from a sign that finds nothing, or from a branch that stopped finding. The artefacts are the
# same strings in every language, here inside Hungarian sentences.
MACHINE = [
    ("any-didactic-aside", "Fontos megjegyezni, hogy az eredmények régiónként eltérhetnek."),
    ("any-didactic-aside", "Fontos hangsúlyozni, hogy a döntés nem végleges."),
    ("any-didactic-aside", "Fontos kiemelni, hogy a csapat határidőre végzett."),
    ("any-didactic-aside", "Fontos azonban megjegyezni, hogy a költségek nőttek."),
    ("any-didactic-aside", "Fontos ugyanakkor hangsúlyozni, hogy a próba rövid volt."),
    ("any-didactic-aside", "Fontos még kiemelni hogy a raktár zárva lesz."),
    ("any-didactic-aside", "A tesztek lefutottak. Fontos viszont kiemelni, hogy két hiba maradt."),
    ("any-didactic-aside", "Kész a terv! Fontos itt megjegyezni, hogy a keret változhat."),
    ("any-tacked-on-analysis", "A kiállítás hétfőn nyílt meg, tükrözve a város kulturális ambícióit."),
    ("any-tacked-on-analysis", "A cég két új üzemet nyitott, hozzájárulva a régió fejlődéséhez."),
    ("any-tacked-on-analysis", "A program ingyenes, elősegítve az esélyegyenlőséget."),
    ("any-tacked-on-analysis", "A rendszer naponta ment, biztosítva az adatok épségét."),
    ("any-tacked-on-analysis", "A gyár napelemre állt át, ezzel is hozzájárulva a klímacélokhoz."),
    ("any-tacked-on-analysis", "A belső képzés kötelező lett, így biztosítva az egységes tudást."),
    ("hu-hyphenated-case-ending", "Holnap Anna-val egyeztetek a szerződésről."),
    ("hu-hyphenated-case-ending", "A táblát Réka-nak küldtem el."),
    ("hu-hyphenated-case-ending", "Bence-vel beszéltem a határidőről."),
    ("hu-hyphenated-case-ending", "Mária-tól kaptam meg a számlát."),
    ("hu-hyphenated-case-ending", "Éva-ért megyek az állomásra."),
    ("hu-hyphenated-case-ending", "A raktár Nyíregyháza-n van."),
    ("hu-hyphenated-case-ending", "Dóra-hoz fordulj, ha kérdésed van."),
    ("hu-hyphenated-case-ending", "Lilla-ban megbízom."),
    ("hu-hyphenated-case-ending", "Az ügyfél Attila-t kereste."),
    ("hu-hyphenated-case-ending", "Csaba-ként írta alá."),
    ("hu-hyphenated-case-ending", "Gyula-nál van a kulcs."),
    ("hu-hyphenated-case-ending", "Imre-ről nem tudok semmit."),
    ("hu-place-name-suffix", "A központ Budapestben van."),
    ("hu-place-name-suffix", "A raktárunk Kaposvárban van."),
    ("hu-place-name-suffix", "A konferencia Kecskemétben lesz."),
    ("hu-place-name-suffix", "Miskolcban nyílt az új bolt."),
    ("hu-place-name-suffix", "Nyíregyházában nyitunk irodát."),
    ("hu-place-name-suffix", "A gyár Pécsben működik."),
    ("hu-place-name-suffix", "A képzés Szegedben lesz."),
    ("hu-place-name-suffix", "A tréning Székesfehérvárban lesz."),
    ("hu-place-name-suffix", "Szolnokban lakik a csapat fele."),
    ("any-chatgpt-citation-markup", "A híd 1932-ben nyílt meg. :contentReference[oaicite:0]{index=0}"),
    ("any-chatbot-url-tag", "Bővebben: https://example.hu/jelentes?utm_source=chatgpt.com"),
    ("any-gemini-citation-markup", "A pékség 1998-ban költözött Szegedre.[cite: 2]"),
    ("any-deepseek-citation-markup", "A komp 1987 óta jár【3†forrás】."),
    ("any-unfilled-placeholder", "Üdvözlettel:\n[Your Name]"),
    ("any-emoji-markers", "## 📊 Októberi számok"),
]


@pytest.mark.parametrize(("sign", "text"), MACHINE)
def test_the_signs_still_find_what_they_are_for_in_hungarian(counted_alone, sign, text):
    pattern = {found.id: found.pattern for found in counted_alone}[sign]
    assert pattern is not None
    assert pattern.search(text), sign


def _alternatives(term: str) -> list[str]:
    """A term's top-level alternatives: `a|b` is two phrases, `(?:a|b)c` one phrase with two spellings."""
    found, depth, start, escaped, in_class = [], 0, 0, False, False
    for n, char in enumerate(term):
        if escaped:
            escaped = False
        elif char == "\\":
            escaped = True
        elif in_class:
            in_class = char != "]"
        elif char == "[":
            in_class = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "|" and depth == 0:
            found.append(term[start:n])
            start = n + 1
    return [*found, term[start:]]


def _weak_hits(catalogue: signs.Catalogue, text: str, kind: str) -> int:
    """Hits of the weak signs a kind of writing reads, as the cluster rule counts them: each a different word or phrase.
    Each alternative of a term is a phrase of its own, one phrase however its endings vary; a check is one habit however
    often it fires; one phrase two signs find counts once. Hungarian is written with spaces, so a phrase has word edges,
    as `validate` gives it."""
    counted: set[str] = set()
    spans: list[tuple[int, int]] = []
    for sign in catalogue.signs.values():
        if not sign.pattern or sign.strength != "weak" or not _reads(sign, kind):
            continue
        phrases = [
            (phrase, re.compile(rf"\b(?:{phrase})\b", re.IGNORECASE | re.MULTILINE))
            for term in sign.terms
            for phrase in _alternatives(term.term)
        ]
        for phrase, pattern in phrases or [(sign.id, sign.pattern)]:
            for found in pattern.finditer(text):
                if phrase not in counted and any(found.start() < end and start < found.end() for start, end in spans):
                    continue
                counted.add(phrase)
                spans.append(found.span())
    return len(counted)


@pytest.mark.parametrize(("text", "kind"), KINDS)
def test_plain_hungarian_work_text_makes_no_weak_cluster(catalogue, text, kind):
    for paragraph in text.split("\n\n"):
        assert _weak_hits(catalogue, paragraph, kind) < signs.WEAK_CLUSTER, paragraph


def test_weak_hits_count_as_the_rule_does(catalogue):
    # three different words are a cluster; one word three times is a habit, and counts once
    three = "Az átfogó terv kulcsfontosságú lépései elengedhetetlenek."
    again = "Átfogó felmérés, átfogó jelentés, átfogóbb terv."
    assert _weak_hits(catalogue, three, "document") == 3
    assert _weak_hits(catalogue, again, "document") == 1
    # a dash pair around one aside is one habit, and so are two quotes in English marks
    dashes = "Az ajánlat " + EM + " bár drágább a tavalyinál " + EM + " megéri."
    quotes = "A gomb neve " + OPEN + "Mentés" + HIGH + ", a menüé " + OPEN + "Fájl" + HIGH + "."
    assert _weak_hits(catalogue, dashes, "document") == 1
    assert _weak_hits(catalogue, quotes, "document") == 1


def test_three_different_weak_phrases_in_a_report_are_a_cluster(catalogue):
    # The maintainer judged a two-sentence report of this shape machine-made (#28): three different phrases are three.
    report = "Az átfogó leltár lezárult. A frissítés minden gépen elengedhetetlen, beleértve a laptopokat is."
    assert _weak_hits(catalogue, report, "document") == signs.WEAK_CLUSTER


def test_a_term_s_alternatives_are_split_at_the_top_level():
    assert _alternatives("a|b(?:c|d)|[|]e") == ["a", "b(?:c|d)", "[|]e"]
    assert _alternatives(r"x\|y") == [r"x\|y"]


def _plain(text: str) -> str:
    """A text as the alphabetical rule reads it: accents and case ignored."""
    decomposed = unicodedata.normalize("NFD", text.lower())
    return "".join(char for char in decomposed if not unicodedata.combining(char))


# A group of plain words, with no regex syntax nested in it: the groups the rule can be checked on mechanically.
_SIMPLE_GROUP = re.compile(r"\(\?:([^()\[\]\\?*+{}^$.]+)\)")


def test_hungarian_alternations_run_in_alphabetical_order(catalogue):
    # hu.toml's header: our own order is alphabetical, so no source's order can come back (#28's review). The Hungarian
    # branches of the two any signs follow it too; their English branches are not ours to reorder here.
    regexes = [
        (sign.id, term.term)
        for sign in catalogue.signs.values()
        if sign.language == "hu"
        for term in sign.terms
    ]
    regexes += [
        (sign.id, sign.pattern.pattern)
        for sign in catalogue.signs.values()
        if sign.language == "hu" and sign.pattern and not sign.terms
    ]
    for sign in ("any-didactic-aside", "any-tacked-on-analysis"):
        pattern = catalogue.signs[sign].pattern
        assert pattern is not None
        regexes.append((sign, pattern.pattern.split("|(?:^|", 1)[-1] if "didactic" in sign else pattern.pattern))
    groups = [(sign, group.split("|")) for sign, regex in regexes for group in _SIMPLE_GROUP.findall(regex)]
    assert len(groups) >= 8  # the parse finds the groups, so the test can fail
    wrong = [(sign, items) for sign, items in groups if [_plain(item) for item in items] != sorted(map(_plain, items))]
    assert wrong == []


def test_hungarian_term_lists_run_in_alphabetical_order(catalogue):
    for sign in catalogue.signs.values():
        if sign.language != "hu" or len(sign.terms) < 2:
            continue
        keys = [_plain(re.split(r"[(\[]", term.term, maxsplit=1)[0]) for term in sign.terms]
        assert keys == sorted(keys), sign.id


def test_the_model_s_read_signs_have_no_check(catalogue):
    # Te and Ön live in verb endings, and a check can't see capitals: these are for the model's own read (#4).
    for sign in (
        "hu-address-switching",
        "hu-title-case-headings",
        "hu-explicit-subject-repeat",
        "hu-parenthetical-gloss",
    ):
        assert catalogue.signs[sign].pattern is None, sign


def test_the_calques_leave_out_the_contrastive_mikozben(catalogue):
    # the maintainer writes ", miközben" himself (#4): it is no term of the sign
    assert not any("miközben" in term.term for term in catalogue.signs["hu-calque-phrases"].terms)


# Hungarian typography: no formatting sign a Hungarian draft reads may fire on it, whatever its strength.
TYPOGRAPHY = [
    "Az ügyfél azt írta: " + LOW + "sürgős" + HIGH + ".",
    'A tárgy: "Leltár 2025".',
    "Ülés 10" + EN + "12 óráig " + EN + " pontosan.",
    "Az ajánlat " + EN + " bár drágább a tavalyinál " + EN + " megéri.",
    "Szállítás: 4500," + EM + " Ft.",
    "Kiss Erika\n" + EM * 12 + "\nértékesítés",
    "A belső idézet: " + LOW + "azt mondta, " + "\u00bb" + "majd holnap" + "\u00ab" + HIGH + ".",
]


@pytest.mark.parametrize("text", TYPOGRAPHY)
def test_hungarian_typography_is_no_sign(catalogue, text):
    fired = [
        sign.id
        for sign in catalogue.signs.values()
        if sign.language in ("any", "hu")
        and sign.category == "formatting"
        and sign.pattern
        and sign.pattern.search(text)
    ]
    assert fired == []


# Hungarian is agglutinative: the forms a weak check must still find, beyond its own `flags`, and what it must leave
# alone. A term matches where the stem starts the word, after a superlative leg- where the term allows it.
FORMS = [
    ("hu-ai-vocabulary", "A döntés kulcsfontosságúnak bizonyult."),
    ("hu-ai-vocabulary", "Ez az átfogóbb felmérés."),
    ("hu-ai-vocabulary", "A frissítés elengedhetetlenül szükséges."),
    ("hu-ai-vocabulary", "Az átállás zökkenőmentesen zajlott."),
    ("hu-ai-vocabulary", "A kérdést mélyrehatóan vizsgáltuk."),
    ("hu-ai-vocabulary", "A projekt több aspektusát is áttekintettük."),
    ("hu-ai-vocabulary", "Az ügyfél perspektívájából nézve más a kép."),
    ("hu-ai-vocabulary", "A csapat kulcsszerepet játszott a sikerben."),
    ("hu-ai-vocabulary", "A tartalék nélkülözhetetlennek tűnt."),
    ("hu-promo-adjectives", "A kilátás lenyűgözött mindenkit."),
    ("hu-promo-adjectives", "Az előadás lenyűgözőbb volt, mint tavaly."),
    ("hu-promo-adjectives", "A díszlet varázslatosan festett."),
    ("hu-promo-adjectives", "Felejthetetlenül szép este volt."),
    ("hu-promo-adjectives", "A zene magával ragadta a közönséget."),
    ("hu-calque-phrases", "A napi séta segíthet csökkenteni a stresszt."),
    ("hu-calque-phrases", "A képzés segít a csapatnak megérteni az új folyamatot."),
    ("hu-calque-phrases", "Az új szabályok segítenek megelőzni a hibákat."),
    ("hu-calque-phrases", "A szoftver lehetővé tette a gyorsabb számlázást."),
    ("hu-calque-phrases", "Új szerződést kötöttünk, lehetővé téve a rugalmas munkát."),
    ("hu-calque-phrases", "A régi raktár irattárként szolgál."),
    ("hu-calque-phrases", "A tárgyalók közösségi térként szolgálhatnak."),
    ("hu-calque-phrases", "Minden költség benne van, beleértve az utazást."),
    ("hu-em-dash", "Három jelentkező maradt" + EM + "mindhárman debreceniek."),
    ("hu-english-quotes", "A fájl neve " + OPEN + "jelentés_v2" + HIGH + "."),
]

LEFT_ALONE = [
    ("hu-ai-vocabulary", "A tanfolyam átfogja a teljes évet."),
    ("hu-ai-vocabulary", "A kulcsot a portán hagytam."),
    ("hu-calque-phrases", "Segítesz feltölteni a táblázatot?"),
    ("hu-calque-phrases", "Segítenél megérteni ezt a képletet?"),
    ("hu-calque-phrases", "Bence segít feltölteni a táblázatot."),
    ("hu-calque-phrases", "Katonaként szolgált tíz évig."),
    ("hu-calque-phrases", "A szerződés lehetőséget ad a felmondásra."),
    ("hu-calque-phrases", "Miközben vártam, megírtam a jelentést."),
    ("hu-calque-phrases", "Segítettem neki a költözésben."),
    ("hu-em-dash", "Három jelentkező maradt " + EN + " mindhárman debreceniek."),
    ("hu-em-dash", "Szállítás: 4500," + EM + " Ft."),
    ("hu-em-dash", "Belépő: 3000." + EM + " Ft"),
    ("hu-em-dash", EM * 12),
    ("hu-english-quotes", "Az ügyfél azt írta: " + LOW + "sürgős" + HIGH + "."),
    ("hu-english-quotes", 'A tárgy: "Leltár 2025".'),
    ("hu-hyphenated-case-ending", "Anna-Mária írt, hogy késik."),
    ("hu-hyphenated-case-ending", "Anna-e vagy Kata?"),
    ("hu-hyphenated-case-ending", "A Jira-ban frissítettem a jegyet."),
    ("hu-hyphenated-case-ending", "Teams-en elérsz."),
    ("hu-hyphenated-case-ending", "Annával, Bencével és Rékától kaptam választ."),
    ("hu-hyphenated-case-ending", "Az Anna-bálra megyünk Balatonfüredre."),
    ("hu-place-name-suffix", "Szegeden, Győrben, Debrecenben és Pécsett is van irodánk."),
    ("hu-place-name-suffix", "Budapestre, Egerbe és Sopronba visszük az árut."),
    ("hu-place-name-suffix", "A győri és a szegedi telephely nyitva lesz."),
    ("hu-place-name-suffix", "Győr-Moson-Sopron megyében is van ügyfelünk."),
    ("hu-place-name-suffix", "Zalaegerszegen tartjuk a képzést."),
    ("hu-place-name-suffix", "Az egéren nem működik a görgő."),
    ("any-didactic-aside", "Fontos, hogy péntekig leadjátok a jelenléti ívet."),
    ("any-didactic-aside", "Fontos kiemelni a határidőt a meghívóban."),
    ("any-didactic-aside", "Fontosnak tartom hangsúlyozni, hogy nem volt baleset."),
    ("any-tacked-on-analysis", "A szállás biztosítva."),
    ("any-tacked-on-analysis", "Az ebéd biztosítva, a parkolás nem."),
    ("any-tacked-on-analysis", "Ha megjön az utalás, biztosítva lesz a fizetés."),
    ("any-tacked-on-analysis", "Kérem, a hozzáférés legyen biztosítva hétfőre."),
    ("any-tacked-on-analysis", "A wifi biztosítva a vendégeknek is."),
    ("any-tacked-on-analysis", "Előre biztosítva a helyet, nyugodtan érkezhetsz."),
]


@pytest.mark.parametrize(("sign", "text"), FORMS)
def test_a_hungarian_check_finds_its_inflected_forms(catalogue, sign, text):
    pattern = catalogue.signs[sign].pattern
    assert pattern is not None
    assert pattern.search(text), sign


@pytest.mark.parametrize(("sign", "text"), LEFT_ALONE)
def test_a_hungarian_check_leaves_plain_forms_alone(catalogue, sign, text):
    pattern = catalogue.signs[sign].pattern
    assert pattern is not None
    assert not pattern.search(text), sign
