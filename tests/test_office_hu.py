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
from collections.abc import Callable

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
    # a hotel's, a club's and a county's name, and a verb that takes -ban/-ben (#28's review, F8)
    "A konferencia a Corinthia Hotel Budapestben lesz, a nagyteremben.",
    "A vacsorát a Müpa Budapestben foglaltuk le.",
    "A partnereink a Hilton Budapestben szállnak meg.",
    "A Hotel Kecskemétben tartjuk a kihelyezett ülést.",
    "Az unokaöcsém a Pick Szegedben kézilabdázik.",
    "Régebben a Kaposvárban játszott, most edző.",
    "Jász-Nagykun-Szolnokban három új telephelyünk van.",
    "Őszintén szólva csalódtam Budapestben, többet vártam.",
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
    "A műszakot átszerveztük, biztosítva a hétvégi ügyeletet is.",
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
def test_no_sign_that_counts_alone_fires_on_plain_hungarian_work_text(counted_alone, reads, text, kind):
    fired = [sign.id for sign in counted_alone if reads(sign, kind) and sign.pattern and sign.pattern.search(text)]
    assert fired == []


def test_the_one_hungarian_check_that_counts_alone_is_the_hyphen(counted_alone):
    # The maintainer (#4): a native speaker never writes it. The place suffix is for the model's read, as names and
    # verbs take -ban/-ben rightly (#28's review, F8). Any other Hungarian check that counts alone needs its lines in
    # MACHINE and a reason.
    assert [sign.id for sign in counted_alone if sign.language == "hu"] == ["hu-hyphenated-case-ending"]


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


@pytest.mark.parametrize(("text", "kind"), KINDS)
def test_plain_hungarian_work_text_makes_no_weak_cluster(weak_hits, text, kind):
    for paragraph in text.split("\n\n"):
        assert weak_hits(paragraph, kind) < signs.WEAK_CLUSTER, paragraph


def test_weak_hits_count_as_the_rule_does(weak_hits):
    # three different words are a cluster; one word three times is a habit, and counts once
    three = "Az átfogó terv kulcsfontosságú lépései elengedhetetlenek."
    again = "Átfogó felmérés, átfogó jelentés, átfogóbb terv."
    assert weak_hits(three, "document") == 3
    assert weak_hits(again, "document") == 1
    # a dash pair around one aside is one habit, and so are two quotes in English marks
    dashes = "Az ajánlat " + EM + " bár drágább a tavalyinál " + EM + " megéri."
    quotes = "A gomb neve " + OPEN + "Mentés" + HIGH + ", a menüé " + OPEN + "Fájl" + HIGH + "."
    assert weak_hits(dashes, "document") == 1
    assert weak_hits(quotes, "document") == 1


def test_three_different_weak_phrases_in_a_report_are_a_cluster(weak_hits):
    # The maintainer judged a two-sentence report of this shape machine-made (#28): three different phrases are three.
    report = "Az átfogó leltár lezárult. A frissítés minden gépen elengedhetetlen, beleértve a laptopokat is."
    assert weak_hits(report, "document") == signs.WEAK_CLUSTER


def test_a_term_s_alternatives_are_split_at_the_top_level(alternatives):
    assert alternatives("a|b(?:c|d)|[|]e") == ["a", "b(?:c|d)", "[|]e"]
    assert alternatives(r"x\|y") == [r"x\|y"]


def _plain(text: str) -> str:
    """A text as the alphabetical rule reads it: accents and case ignored."""
    decomposed = unicodedata.normalize("NFD", text.lower())
    return "".join(char for char in decomposed if not unicodedata.combining(char))


def _groups(regex: str) -> list[str]:
    """The inside of every (?:…) group in a regex, nested ones too."""
    found = []
    for opened in (n for n in range(len(regex)) if regex.startswith("(?:", n) and (n == 0 or regex[n - 1] != "\\")):
        depth, escaped, in_class = 0, False, False
        for n in range(opened, len(regex)):
            char = regex[n]
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
                if depth == 0:
                    found.append(regex[opened + 3 : n])
                    break
    return found


def _start(alternative: str) -> str:
    """An alternative's literal start, up to the first class, group or escape, as the alphabetical rule reads it."""
    return _plain(re.split(r"[\[(\\]", alternative, maxsplit=1)[0])


def _misordered(regex: str, alternatives: Callable[[str], list[str]]) -> list[list[str]]:
    groups = [alternatives(group) for group in _groups(regex)]
    return [items for items in groups if len(items) > 1 and [_start(i) for i in items] != sorted(map(_start, items))]


def test_hungarian_alternations_run_in_alphabetical_order(catalogue, alternatives):
    # hu.toml's header: our own order is alphabetical, so no source's order can come back (#28's review). A group with
    # a class or an escape in it is read by each alternative's literal start (F9); any-didactic-aside's English groups
    # are main's, already in order.
    regexes = [
        (sign.id, term.term) for sign in catalogue.signs.values() if sign.language == "hu" for term in sign.terms
    ]
    regexes += [
        (sign.id, sign.grep)
        for sign in catalogue.signs.values()
        if sign.language == "hu" and sign.pattern and not sign.terms
    ]
    regexes.append(("any-didactic-aside", catalogue.signs["any-didactic-aside"].grep))
    assert sum(len(_groups(regex)) for _, regex in regexes) >= 15  # the parse finds the groups, so the test can fail
    wrong = [(sign, items) for sign, regex in regexes for items in _misordered(regex, alternatives)]
    assert wrong == []


def test_the_order_rule_reads_groups_with_classes_and_escapes(alternatives):
    # reversed, a suffix group with classes and a group with escapes both fail, so the test above can't pass on nothing
    assert _misordered(r"-(?:v[ae]l|t|n[ae]k|b[ae]n?)\b", alternatives) == [["v[ae]l", "t", "n[ae]k", "b[ae]n?"]]
    assert _misordered(r",\s+(?:így\s+|ezzel is\s+)?", alternatives) == [["így\\s+", "ezzel is\\s+"]]
    assert _misordered(r"(?:b[ae]n?|n[ae]k|t|v[ae]l)(?:ezzel is\s+|így\s+)", alternatives) == []


def test_hungarian_term_lists_run_in_alphabetical_order(catalogue):
    for sign in catalogue.signs.values():
        if sign.language != "hu" or len(sign.terms) < 2:
            continue
        keys = [_plain(re.split(r"[(\[]", term.term, maxsplit=1)[0]) for term in sign.terms]
        assert keys == sorted(keys), sign.id


def test_the_model_s_read_signs_have_no_check(catalogue):
    # Te and Ön live in verb endings, and a check can't see capitals: these are for the model's own read (#4).
    for sign in (
        "hu-place-name-suffix",
        "hu-address-switching",
        "hu-title-case-headings",
        "hu-explicit-subject-repeat",
        "hu-parenthetical-gloss",
    ):
        assert catalogue.signs[sign].pattern is None, sign


def test_the_calques_leave_out_the_contrastive_mikozben(catalogue):
    # the maintainer writes ", miközben" (#4): it is no term of the sign
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
    ("hu-tacked-on-participle", "A kiállítás hétfőn nyílt meg, tükrözve a város kulturális ambícióit."),
    ("hu-tacked-on-participle", "A cég két új üzemet nyitott, hozzájárulva a régió fejlődéséhez."),
    ("hu-tacked-on-participle", "A program ingyenes, elősegítve az esélyegyenlőséget."),
    ("hu-tacked-on-participle", "A rendszer naponta ment, biztosítva az adatok épségét."),
    ("hu-tacked-on-participle", "A gyár napelemre állt át, ezzel is hozzájárulva a klímacélokhoz."),
    ("hu-tacked-on-participle", "A belső képzés kötelező lett, így biztosítva az egységes tudást."),
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
    ("any-didactic-aside", "Fontos, hogy péntekig leadjátok a jelenléti ívet."),
    ("any-didactic-aside", "Fontos kiemelni a határidőt a meghívóban."),
    ("any-didactic-aside", "Fontosnak tartom hangsúlyozni, hogy nem volt baleset."),
    ("hu-tacked-on-participle", "Az ikont tedd át a jobb sarokba, tükrözve a függőleges tengelyre."),
    ("hu-tacked-on-participle", "A helyszín a nagytárgyaló, biztosítva a kivetítő és a flipchart is."),
    ("hu-tacked-on-participle", "A szállás biztosítva."),
    ("hu-tacked-on-participle", "Az ebéd biztosítva, a parkolás nem."),
    ("hu-tacked-on-participle", "Ha megjön az utalás, biztosítva lesz a fizetés."),
    ("hu-tacked-on-participle", "Kérem, a hozzáférés legyen biztosítva hétfőre."),
    ("hu-tacked-on-participle", "A wifi biztosítva a vendégeknek is."),
    ("hu-tacked-on-participle", "Előre biztosítva a helyet, nyugodtan érkezhetsz."),
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
