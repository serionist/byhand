"""Plain German work text, invented, against the real catalogue. A strong or usual sign counts alone, so one that fires
on any of these accuses a person of writing like a machine. Business German (Nominalstil, im Rahmen, zeitnah,
bezüglich) and German typography (low-high quotes, the spaced short dash, long compounds, capitalised nouns) are a
person's, never a sign. A weak sign may fire: it counts only in a cluster, and plain work text must not make one.

The low and high quotes and the short and long dashes are written as escapes, as ruff refuses them in source; the first
test holds that they are the real marks."""

import unicodedata

import pytest

from byhand import signs

LOW, HIGH, EN, EM = "\u201e", "\u201c", "\u2013", "\u2014"

# A service desk's closing line, word for word a chatbot's: the closing offer reads documents only (#23's review, F3).
SERVICE_DESK = "Gibt es noch etwas, bei dem ich Ihnen helfen kann? Sonst schlie\u00dfe ich das Ticket heute."

MAIL = [
    "Sehr geehrte Frau Dr. Wagner,\n\nvielen Dank für Ihre schnelle Rückmeldung. Den unterschriebenen Vertrag sende "
    "ich Ihnen bis Freitag zurück.\n\nMit freundlichen Grüßen\nTobias Krämer",
    "Liebe Kolleginnen und Kollegen,\n\nam 14. November bleibt die Kantine wegen der Betriebsversammlung geschlossen. "
    "Kaffee gibt es im 2. OG.\n\nViele Grüße\nAnja",
    "Hallo Frau Schulz,\n\nich hoffe, Sie hatten ein schönes Wochenende. Kurze Rückfrage zur Rechnung vom 3. November: "
    "Die Bestellnummer fehlt.\n\nBeste Grüße\nMehmet Demir",
    "Hi Jonas,\n\nkurze Frage: Hast du die Reisekostenabrechnung für Hamburg schon eingereicht? Die Frist ist "
    "Donnerstag.\n\nLG\nSabine",
    "Sehr geehrte Damen und Herren,\n\nim Rahmen unserer Zusammenarbeit bitten wir Sie, uns zeitnah die aktualisierten "
    "Zertifikate zukommen zu lassen. Bezüglich der Lieferfristen melden wir uns gesondert.\n\nMit freundlichen Grüßen",
    SERVICE_DESK,
    "Als Projektleiterin habe ich keine Zeit für ein zweites Meeting, lass uns das am Montag klären.",
    "Als KI-Beauftragte habe ich keine Admin-Rechte, frag bitte die IT.",
    "Bitte beachten Sie, dass das Parkhaus ab 18 Uhr schließt.",
    "Es ist wichtig, dass alle bis Freitag ihre Stunden im System eintragen.",
    "Sie haben völlig recht, das Datum stimmt nicht. Ich schicke die Rechnung neu.",
    "In den bereitgestellten Unterlagen fehlt Seite 3. Können Sie die bitte nachreichen?",
    "Nach meinem Wissensstand ist der Vertrag schon unterschrieben. Stand heute fehlen nur noch die Anlagen.",
    "Könnten Sie mir vielleicht bis morgen Bescheid geben, ob der Termin passt?",
    "Danke für die tolle Zusammenarbeit " + EN + " das war ein echter Meilenstein für unser Team!",
    "Wir dürfen gespannt sein, was der Kunde zu dem Angebot sagt. Ich halte euch auf dem Laufenden.",
]

CHAT = [
    "Moin zusammen, der Build auf main ist wieder grün. Danke an Lea fürs Fixen!",
    "@Markus kannst du kurz drüberschauen? Ist nicht eilig.",
    "Bin heute im Homeoffice, ab 14 Uhr erreichbar.",
    "Sorry, verspäte mich 10 Min " + EN + " S-Bahn steht.",
    "👍 passt",
    "Gibt es noch etwas, das ich für die Feier mitbringen soll?",
    "Möchtest du, dass ich das Protokoll noch kürze, oder passt es so?",
    "Das könnte möglicherweise am VPN liegen. Probier mal, dich neu zu verbinden.",
    "Was wäre, wenn wir das Meeting auf Donnerstag schieben?",
    "Habt ihr euch schon mal gefragt, warum der Drucker im 3. OG immer streikt? Papierfach 2 klemmt.",
    "Bis zu meinem letzten Update lief die App stabil, seitdem stürzt sie beim Login ab.",
    "Als Sprachmodell habe ich Llama genommen, weil es lokal läuft.",
    "Als KI-Assistent kann ich Copilot empfehlen, der ist in Teams schon drin.",
    "Der Kunde hat " + LOW + "dringend" + HIGH + " geschrieben " + EN + " also bitte heute noch.",
    "✅ Raum gebucht\n✅ Catering bestellt",
]

NOTES = [
    "Protokoll Teamrunde 07.11.\n- Anwesend: Anna, Ben, Carla\n- Urlaubsplanung: Weihnachten bis 30.11. eintragen\n"
    "- Nächster Termin: 21.11., 10 Uhr",
    "TODO\n- Angebot an Müller GmbH nachfassen\n- Rechnungsnummer 2026-0412 prüfen\n- Dienstreiseantrag stellen",
    "**Wichtig:** Die Abgabefrist ist Freitag, 12 Uhr.",
    "Die Arbeitsschutzunterweisungsunterlagen liegen im Ordner Qualitätsmanagementhandbuch.",
    "Sitzung 10" + EN + "12 Uhr, Raum 3.14 " + EN + " bitte pünktlich.",
    "Fazit: Wir bleiben beim alten Anbieter, der neue ist 20 % teurer.",
    "Zusammenfassend: Angebot B, Start im Januar.",
    "Vorlage für die Einladung: Hallo [Name], wir freuen uns auf dich am 12.12.!",
    "## Neue Regeln für die Urlaubsplanung",
    # prices, with the dash Swiss and German invoices write for no cents (#23's review, F6)
    "Eintritt: CHF 20." + EM + " pro Person, Kinder frei.",
    "Gesamtbetrag: 1.250," + EM + " € netto, zahlbar in 30 Tagen.",
    # first-person questions as headings of an FAQ, which the closing offer reads (#23's review, m4)
    "## Soll ich den Antrag selbst erstellen oder eine Vorlage nutzen?\nDie Vorlage spart Zeit.",
    "## Soll ich es notariell machen lassen?\nNur beim Grundstückskauf.",
    "Soll ich ihn selbst erstellen? Nein, die Personalabteilung schickt ihn zu.",
]

# a reply ending on a colon, before the link, the file or the text; a person handing over or returning their own draft
REPLIES = [
    "Hier die Zahlen von gestern:",
    "Anbei meine Anmerkungen:",
    "Klar, hier ist der Link:",
    "Natürlich! Hier ist der Entwurf für das Protokoll:",
    "Gerne! Hier ist meine überarbeitete Fassung:",
    "Gerne! Hier ist Ihre überarbeitete Präsentation:",
    # reworked text that doesn't name the reader's: a person's too (#23's review, F2)
    "Gerne! Hier ist eine überarbeitete Version mit deinen Anmerkungen:",
    "Gerne! Hier ist ein überarbeiteter Entwurf:",
    "Sehr gerne, hier ist die kürzere Fassung für den Aushang:",
    # ihrer, a third person's: only the polite Ihrer, capitalised, is the reader's (#23's review, m1)
    "Gerne! Hier ist die überarbeitete Fassung ihrer Rede, Frau Klein hat sie heute Morgen geschickt:",
    "Gerne! Hier ist ihr überarbeiteter Entwurf, so wie Frau Klein ihn mir geschickt hat:",
    "Klar, hier ist die kürzere Fassung:",
    "Gerne, hier meine Vorschläge für die Agenda:",
    "Ich habe einen ersten Entwurf geschrieben, schau gern drüber:",
    "Hier ist mein Entwurf für den Newsletter. Kürzen ist erlaubt:",
    "Anbei die überarbeitete Version, eure Kommentare sind eingearbeitet.",
]

REPORTS = [
    "Im dritten Quartal stieg der Umsatz um 4 %, vor allem durch das Ersatzteilgeschäft. Darüber hinaus haben wir zwei "
    "Großkunden gewonnen. Die Personalkosten blieben stabil; im Rahmen der Budgetplanung prüfen wir zeitnah, ob wir "
    "eine weitere Stelle ausschreiben.",
    "Zusammenfassend lässt sich sagen, dass die Umstellung auf das neue ERP-System im Zeit- und Kostenrahmen blieb. Es "
    "ist wichtig zu beachten, dass die Schulungen für das Lager noch ausstehen. Bezüglich der Lizenzen melden wir uns "
    "bis Ende November.",
    "Die Software spielt eine zentrale Rolle in unserem Bestellprozess. Eine Vielzahl von Kunden hat Rückmeldung "
    "gegeben; die Rückmeldungen dienen als Grundlage für die nächste Version. Es bleibt abzuwarten, ob die Lieferanten "
    "mitziehen.",
    "Protokoll Lenkungskreis, 6. November\n\nTOP 1: Der Meilenstein " + LOW + "Rollout Nord" + HIGH + " ist erreicht. "
    "Ferner wurde beschlossen, den Go-live für Süd auf Januar zu verschieben.\n\nTOP 2: Das Budget steigt um "
    "20.000 €. Begründung: höhere Hardwarekosten.",
    "Hinweis zur Datenschutzschulung: Es ist zu beachten, dass die Teilnahme für alle Beschäftigten verpflichtend ist. "
    "Die Schulung dauert etwa 45 Minuten und kann bis 31. Dezember absolviert werden.",
    # summaries, notes and official phrases a plain report writes, which reached 3 weak hits (#23's review, F1)
    "Alles in allem lässt sich sagen, dass die Inventur ohne größere Abweichungen verlief. Es sei darauf hingewiesen, "
    "dass zwei Lagerplätze noch nachgezählt werden. Abschließend sei noch erwähnt, dass die Zählung eine halbe Stunde "
    "kürzer dauerte als im Vorjahr.",
    "Geprüft wurden sowohl die Reisekostenbelege als auch die Bankauszüge und das Fahrtenbuch. Zusammenfassend lässt "
    "sich feststellen, dass es keine Beanstandungen gibt. Es ist wichtig zu bedenken, dass die Prüfung nur Stichproben "
    "umfasst.",
    "Der neue Lieferant hat eine große Palette von Ersatzteilen. Abschließend lässt sich festhalten, dass die Preise "
    "stabil bleiben. Es ist wichtig zu beachten, dass die Lieferzeit auf sechs Wochen gestiegen ist.",
    "Insgesamt lässt sich festhalten, dass die neue Schichtplanung angenommen wird. Bemerkenswert ist, dass die "
    "Überstunden um 12 % gesunken sind. Es ist anzumerken, dass zwei Teams noch nach dem alten Plan arbeiten.",
    "Es bleibt festzuhalten, dass das Budget eingehalten wurde. Eine Vielzahl von Rückmeldungen betraf die Kantine; im "
    "Rahmen der nächsten Befragung fragen wir dort gezielter nach.",
    "Zusammenfassend: Das Pilotprojekt ist abgeschlossen. Es ist wichtig zu betonen, dass alle Standorte teilgenommen "
    "haben. Die Kosten lagen 8 % unter Plan.",
    "Die Umstellung betraf sowohl Einkauf, Lager als auch Versand. Die Schulungen sind abgeschlossen; offen ist nur "
    "noch die Anbindung des Kassensystems.",
]

# posts a person writes: a short post on the company channel and a farm shop's newsletter
POSTS = [
    "Heute vor zehn Jahren habe ich meine Ausbildung hier angefangen. Wir dürfen gespannt sein, wie es weitergeht "
    + EN
    + " erstmal gibt's Kuchen in der Teeküche!",
    "Unser Hofladen liegt mitten im Dorf und hat Gemüse aus eigenem Anbau. Samstags gibt es frisches Brot vom Bäcker "
    "nebenan, und ab Dezember auch Weihnachtsbäume.",
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
    assert unicodedata.name(HIGH) == "LEFT DOUBLE QUOTATION MARK"
    assert unicodedata.name(EN) == "EN DASH"
    assert unicodedata.name(EM) == "EM DASH"
    assert sum(EN in text for text in OFFICE) >= 4
    assert len(OFFICE) >= 40


@pytest.mark.parametrize(("text", "kind"), KINDS)
def test_no_sign_that_counts_alone_fires_on_plain_german_work_text(counted_alone, reads, text, kind):
    fired = [sign.id for sign in counted_alone if reads(sign, kind) and sign.pattern and sign.pattern.search(text)]
    assert fired == []


def test_a_service_desk_s_closing_line_meets_a_sign_that_reads_only_documents(catalogue):
    # the maintainer's call on #23: the chatbot's line and the service desk's are the same words, so the sign stays
    # strong for documents, where no person writes it, and never reads mail
    offer = catalogue.signs["any-assistant-closing-offer"]
    assert offer.pattern is not None
    assert offer.pattern.search(SERVICE_DESK)
    assert offer.kinds == ("document",)


def test_no_german_check_counts_alone(counted_alone):
    # Every German word list is weak (#4): a German sign with a pattern that counts alone needs its lines in MACHINE.
    assert [sign.id for sign in counted_alone if sign.language == "de"] == []


# What each sign that counts alone exists to catch, inside German text: a line per branch of its check, so silence above
# can't come from a sign that finds nothing, or from a branch that stopped finding. Branches that read only English,
# Russian, Chinese or Japanese words have their lines in the other office tests.
MACHINE = [
    ("any-assistant-preamble", "Gerne! Hier ist eine überarbeitete Version Ihres Anschreibens:"),
    ("any-assistant-preamble", "Natürlich, hier ist der umformulierte Text deiner Bewerbung:"),
    ("any-assistant-preamble", "Sicherlich! Hier ist eine etwas förmlichere Fassung Ihrer E-Mail:"),
    ("any-assistant-preamble", "Selbstverständlich! Hier ist eine kürzere Version Ihres Beitrags:"),
    ("any-assistant-preamble", "Sehr gerne! Hier ist ein überarbeiteter Entwurf eurer Einladung:"),
    ("any-assistant-preamble", "Gerne, hier ist die verbesserte Fassung deiner Nachricht:"),
    ("any-assistant-preamble", "Natürlich! Hier ist Ihr umformulierter Text:"),
    ("any-assistant-preamble", "Gerne! Hier ist eine professionellere Version Ihrer E-Mail:"),
    ("any-assistant-preamble", "Sicherlich! Hier ist deine freundlichere Fassung:"),
    ("any-assistant-closing-offer", "Gibt es noch etwas, womit ich dir behilflich sein kann?"),
    ("any-assistant-closing-offer", "Gibt es noch etwas, bei dem ich Ihnen noch helfen kann?"),
    ("any-assistant-closing-offer", "Möchten Sie, dass ich dies in eine Tabelle umwandle?"),
    ("any-assistant-closing-offer", "Möchtest du, dass ich den Text etwas kürzer fasse?"),
    ("any-assistant-closing-offer", "Möchten Sie, dass ich daraus eine Präsentation erstelle?"),
    ("any-assistant-closing-offer", "Möchtest du, dass ich den Entwurf förmlicher formuliere?"),
    ("any-assistant-closing-offer", "Möchten Sie, dass ich es um ein Fazit ergänze?"),
    ("any-assistant-closing-offer", "Soll ich den Text noch etwas lockerer umschreiben?"),
    ("any-assistant-closing-offer", "Soll ich daraus eine kurze Mail machen?"),
    ("any-assistant-closing-offer", "Soll ich diesen Entwurf noch um Beispiele erweitern?"),
    ("any-assistant-closing-offer", "Lassen Sie mich wissen, wenn ich den Ton noch anpassen soll."),
    ("any-assistant-closing-offer", "Lass mich wissen, ob ich etwas kürzen soll."),
    ("any-ai-self-reference", "Als KI-Sprachmodell habe ich keine persönliche Meinung zum Dienstplan."),
    ("any-ai-self-reference", "Als künstliche Intelligenz kann ich nicht in die Zukunft sehen."),
    ("any-ai-self-reference", "Als großes Sprachmodell bin ich nicht in der Lage, Links zu öffnen."),
    ("any-ai-self-reference", "Als KI-Assistent darf ich keine Rechtsberatung geben."),
    ("any-ai-self-reference", "Als KI habe ich keine Gefühle, aber ich verstehe die Frage."),
    ("any-ai-self-reference", "Als Sprachmodell verfüge ich nicht über aktuelle Kurse."),
    ("any-ai-self-reference", "Als KI-Modell verfüge ich über keine Internetverbindung."),
    ("any-ai-self-reference", "Als KI-Sprachmodell kann ich leider keine Echtzeitdaten abrufen."),
    ("any-ai-self-reference", "Als KI habe ich leider keinen Zugang zu Ihrem Kalender."),
    ("any-ai-self-reference", "Als Sprachmodell kann ich das nicht beurteilen."),
    ("any-knowledge-cutoff", "Stand meines letzten Wissensupdates gab es keine Fusion."),
    ("any-knowledge-cutoff", "Bis zu meinem letzten Wissensupdate war das Werk geöffnet."),
    ("any-knowledge-cutoff", "Bis zu meinem letzten Trainings-Update lag dazu nichts vor."),
    ("any-source-gap-disclaimer", "In den bereitgestellten Quellen findet sich dazu keine Angabe."),
    ("any-source-gap-disclaimer", "In den bereitgestellten Suchergebnissen fehlt das Gründungsjahr."),
    ("any-source-gap-disclaimer", "Spezifische Details bleiben rar, doch die Firma prägte vermutlich den Handel."),
    ("any-source-gap-disclaimer", "Obwohl spezifische Details rar sind, gilt die Mühle als Wahrzeichen."),
    ("any-unfilled-placeholder", "Mit freundlichen Grüßen\n[Ihr Name]"),
    ("any-unfilled-placeholder", "Liebe Grüße, [dein Name]"),
    ("any-unfilled-placeholder", "Sehr geehrte Damen und Herren der [Ihre Firma],"),
    ("any-unfilled-placeholder", "Die Lieferung erfolgt am [Datum einfügen]."),
    ("any-unfilled-placeholder", "Ansprechpartner: [Name hier eintragen]"),
    ("any-unfilled-placeholder", "Mit freundlichen Grüßen\n[Your Name]"),
    ("any-unfilled-placeholder", "Mehr dazu unter insert_link_here."),
    ("any-unfilled-placeholder", "Abgabe am 2026-xx-xx."),
    ("any-emoji-markers", "- 🚀 Neue Funktionen"),
    ("any-emoji-markers", "## 📊 Zahlen im Oktober"),
    ("any-emoji-markers", "1. ✨ Schnellere Ladezeiten"),
    ("any-chatgpt-citation-markup", "Die Brücke wurde 1932 eröffnet. :contentReference[oaicite:0]{index=0}"),
    ("any-chatgpt-citation-markup", "Die Brücke wurde 1932 eröffnet. oaicite:3"),
    ("any-chatgpt-citation-markup", "Die Brücke wurde 1932 eröffnet. oai_citation:1"),
    ("any-chatgpt-citation-markup", "Die Brücke wurde 1932 eröffnet. attributableIndex"),
    ("any-chatgpt-citation-markup", "Die Brücke wurde 1932 eröffnet. turn0search3"),
    ("any-chatgpt-citation-markup", "Die Brücke wurde 1932 eröffnet (Gehe zu Suche Nr.)brücke+1"),
    ("any-chatbot-url-tag", "Mehr unter https://example.de/bericht?utm_source=chatgpt.com"),
    ("any-chatbot-url-tag", "Mehr unter https://example.de/bericht?referrer=grok.com"),
    ("any-gemini-citation-markup", "Die Bäckerei zog 1998 nach Kassel.[span_0](start_span)"),
    ("any-gemini-citation-markup", "Die Bäckerei zog 1998 nach Kassel.[cite: 2]"),
    ("any-grok-citation-markup", "Die Fähre legt um sechs ab. grok_render_citation_card_json"),
    ("any-grok-citation-markup", "Die Fähre legt um sechs ab. grok_card"),
    ("any-grok-citation-markup", "Die Fähre legt um sechs ab. <grok-card id=1>"),
    ("any-deepseek-citation-markup", "Die Fähre fährt seit 1987【3†Quelle】."),
    ("any-chat-tool-markup", "Laut Anhang[attached_file:1] steigt der Umsatz."),
    ("any-chat-tool-markup", "Laut Website[web:2] steigt der Umsatz."),
    ("any-chat-tool-markup", "Siehe ppl-ai-file-upload im Anhang."),
    ("any-chat-tool-markup", ":::writing{variant=standard}"),
]


@pytest.mark.parametrize(("sign", "text"), MACHINE)
def test_the_signs_still_find_what_they_are_for_in_german(counted_alone, sign, text):
    pattern = {found.id: found.pattern for found in counted_alone}[sign]
    assert pattern is not None
    assert pattern.search(text), sign


@pytest.mark.parametrize(("text", "kind"), KINDS)
def test_plain_german_work_text_makes_no_weak_cluster(weak_hits, text, kind):
    for paragraph in text.split("\n\n"):
        assert weak_hits(paragraph, kind) < signs.WEAK_CLUSTER, paragraph


def test_weak_hits_count_as_the_rule_does(weak_hits):
    # three different phrases are a cluster; one phrase three times is a habit, and counts once
    three = "Im Herzen der Altstadt liegt ein atemberaubendes Café mit wegweisendem Konzept."
    again = "Atemberaubend der Blick, atemberaubend das Essen, atemberaubend der Preis."
    assert weak_hits(three, "post") == 3
    assert weak_hits(again, "post") == 1
    # two participles of one term are two different words
    two = "Die Halle wurde erweitert, den Standort betonend und das Wachstum verdeutlichend."
    assert weak_hits(two, "post") == 2
    # the dash check's matches take a letter on each side of the hedge, and Grep runs each check on its own (#56)
    dashes = "Was wäre, wenn die Halle — vielleicht eventuell — schon im Mai öffnet?"
    assert weak_hits(dashes, "post") == 3


def test_a_term_s_alternatives_are_split_at_the_top_level(alternatives):
    assert alternatives("a|b(?:c|d)|[|]e") == ["a", "b(?:c|d)", "[|]e"]
    assert alternatives(r"x\|y") == [r"x\|y"]


# Word lists people use at work: they read posts and documents, never mail or chat (#4).
AT_WORK = [
    "de-dive-in",
    "de-emphasis-phrases",
    "de-future-closers",
    "de-hedging",
    "de-list-announcers",
    "de-promo-words",
    "de-rhetorical-openers",
    "de-significance-phrases",
    "de-sowohl-triad",
    "de-stock-openers",
]


@pytest.mark.parametrize("sign", AT_WORK)
def test_a_word_list_people_use_at_work_reads_posts_and_documents(catalogue, sign):
    found = catalogue.signs[sign]
    assert found.strength == "weak"
    assert set(found.kinds) == {"post", "document"}


def test_the_sowohl_triad_is_for_the_model_s_read(catalogue):
    # as a check it counted toward a cluster on a plain audit report (#23's review, F5)
    assert catalogue.signs["de-sowohl-triad"].pattern is None


@pytest.mark.parametrize(
    ("sign", "text"),
    [
        ("de-hedging", "Das könnte möglicherweise am VPN liegen."),
        ("de-rhetorical-openers", "Was wäre, wenn wir das Meeting auf Donnerstag schieben?"),
        ("de-future-closers", "Wir dürfen gespannt sein, was der Kunde sagt."),
    ],
)
def test_what_chat_says_too_fires_only_where_the_sign_reads(catalogue, reads, sign, text):
    # each fires on a plain chat line, which is why it reads posts and documents only
    found = catalogue.signs[sign]
    assert found.pattern is not None
    assert found.pattern.search(text)
    assert not reads(found, "message")
    assert not reads(found, "email")


# German typography: no formatting sign a German draft reads may fire on it, whatever its strength.
TYPOGRAPHY = [
    "Der Kunde hat " + LOW + "dringend" + HIGH + " geschrieben.",
    "Sitzung 10" + EN + "12 Uhr " + EN + " bitte pünktlich.",
    "Die Übergabe klappt " + EN + " sofern der Schlüssel da ist " + EN + ", sonst Montag.",
    "Die Kundenzufriedenheitsumfrage läuft bis zum 30. November.",
    "Mit freundlichen Grüßen\n" + EM * 12 + "\nAnja Becker, Einkauf",
]


@pytest.mark.parametrize("text", TYPOGRAPHY)
def test_german_typography_is_no_sign(catalogue, text):
    fired = [
        sign.id
        for sign in catalogue.signs.values()
        if sign.language in ("any", "de")
        and sign.category == "formatting"
        and sign.pattern
        and sign.pattern.search(text)
    ]
    assert fired == []


# German inflects and compounds: the forms a weak check must still find, beyond its own `flags`, and what it must leave
# alone. A term matches a compound only where the term starts the word.
FORMS = [
    ("de-em-dash", "Die Übergabe klappt" + EM + "sofern der Schlüssel da ist."),
    ("de-hedging", "Die Kosten könnten unter Umständen steigen."),
    ("de-hedging", "Das wird vielleicht eventuell klappen."),
    ("de-hedging", "Das könnte sich möglicherweise verzögern."),
    ("de-rhetorical-openers", "Haben Sie sich schon einmal gefragt, warum Brot so teuer ist?"),
    ("de-rhetorical-openers", "Hast du dich jemals gefragt, wer die Kantine plant?"),
    ("de-participle-asides", "Die Halle wurde erweitert, die Bedeutung des Standorts betonend."),
    ("de-participle-asides", "Der Plan nennt jede Frist, die Pünktlichkeit hervorhebend."),
    ("de-participle-asides", "Die Regel gilt für alle, die Sicherheit gewährleistend."),
    ("de-significance-phrases", "Die Feier unterstrich die wachsende Bedeutung des Vereins."),
    ("de-significance-phrases", "Der Brauch ist tiefverwurzelt im Ort."),
    ("de-significance-phrases", "Der Abend war einer der Schlüsselmomente des Jahres."),
    ("de-significance-phrases", "Die Mühle stand als Zeugnis für den Fleiß der Bauern."),
    ("de-significance-phrases", "Sie hinterließ ein bleibendes Vermächtnis."),
    ("de-significance-phrases", "Die Pflege des bleibenden Erbes kostet Geld."),
    ("de-significance-phrases", "Die Stiftung wacht über den Erhalt eines bleibenden Vermächtnisses."),
    ("de-promo-words", "Die Aussicht ist atemberaubend."),
    ("de-promo-words", "Das Werk zeigt einen bahnbrechenden Ansatz."),
    ("de-promo-words", "Die App revolutioniert den Einkauf."),
    ("de-promo-words", "Die Stadt mit ihrer reichen Geschichte lädt ein."),
    ("de-promo-words", "Die Region hat ein reiches kulturelles Erbe."),
    ("de-promo-words", "Das Tal mit seinen reichen Traditionen lädt ein."),
    ("de-promo-words", "Die Pflege eines reichen kulturellen Erbes lohnt sich."),
    ("de-promo-words", "Das Hotel liegt im Herzen des Viertels."),
    ("de-promo-words", "Des Paradigmenwechsels wegen gab es Streit."),
    ("de-stock-openers", "In einer sich rasant wandelnden Welt zählt Tempo."),
    ("de-stock-openers", "In der heutigen schnelllebigen Zeit fehlt Ruhe."),
    ("de-stock-openers", "Im Zeitalter der KI lernen alle neu."),
    ("de-future-closers", "Man darf gespannt sein."),
    ("de-future-closers", "Gemeinsam gestalten wir die Zukunft."),
    ("de-future-closers", "Die Zukunft sieht also rosig aus."),
    ("de-emphasis-phrases", "Es ist jedoch wichtig zu bemerken, dass der Raum klein ist."),
    ("de-emphasis-phrases", "Dabei ist es wichtig, zu betonen, dass Parken Geld kostet."),
    ("de-emphasis-phrases", "Hierbei ist es entscheidend zu betonen, dass niemand fehlte."),
    ("any-flattering-agreement", "Tolle Frage! Das erkläre ich gern."),
    ("any-flattering-agreement", "Da haben Sie absolut recht, der Termin war falsch."),
    ("any-flattering-agreement", "Was für eine ausgezeichnete Frage!"),
    ("de-dive-in", "Tauchen Sie ein in unsere kleine Kaffeekunde."),
    ("de-dive-in", "Lasst uns tiefer eintauchen."),
    ("de-dive-in", "Lassen Sie uns gemeinsam eintauchen."),
    ("de-dive-in", "Lass mich das kurz aufschlüsseln."),
    ("de-list-announcers", "Im Kurs lernen Sie eine Vielzahl an Knoten."),
    ("de-list-announcers", "Mit einer breiten Palette an Kursen."),
    ("de-list-announcers", "Es gibt eine breite Palette von Sorten."),
]

LEFT_ALONE = [
    ("de-em-dash", "Die Übergabe klappt " + EN + " sofern der Schlüssel da ist."),
    ("de-em-dash", "Eintritt: CHF 20." + EM + " pro Person"),
    ("de-em-dash", "Summe 1.250," + EM + " €"),
    ("de-em-dash", "Summe 1.250," + EM + "€"),
    ("de-hedging", "Könntest du vielleicht kurz anrufen?"),
    ("de-hedging", "Das kann eventuell klappen."),
    ("de-hedging", "Das könnte vielleicht am Wetter liegen."),
    ("de-participle-asides", "Die hervorhebende Farbe ist Gelb."),
    ("de-participle-asides", "Die Weste ist reflektierend."),
    ("de-significance-phrases", "Das Arbeitszeugnis liegt bei."),
    ("de-significance-phrases", "Er dient als Ansprechpartner für den Einkauf."),
    ("de-significance-phrases", "Sie unterstreicht die Überschrift rot."),
    ("de-promo-words", "Die Bereiche Geschichte und Geografie sind getrennt."),
    ("de-promo-words", "Das war mein Herzenswunsch."),
    ("de-promo-words", "Der Teppichboden im Büro wird erneuert."),
    ("de-promo-words", "Folgen Sie dem Wegweiser im Parkhaus."),
    ("de-stock-openers", "In der heutigen Zeit ist Homeoffice normal."),
    ("de-stock-openers", "In der heutigen Sitzung geht es um das Budget."),
    ("de-future-closers", "Wir sind gespannt auf eure Ideen."),
    ("de-future-closers", "Es bleibt abzuwarten, ob der Kunde zusagt."),
    ("de-emphasis-phrases", "Es ist zu beachten, dass der Raum klein ist."),
    ("de-emphasis-phrases", "Es ist wichtig, dass alle kommen."),
    ("de-emphasis-phrases", "Es ist wichtig zu beachten, dass die Frist endet."),
    ("de-emphasis-phrases", "Es ist wichtig zu bedenken, dass es nur Stichproben sind."),
    ("de-emphasis-phrases", "Es sei darauf hingewiesen, dass Parken Geld kostet."),
    ("de-emphasis-phrases", "Bemerkenswert ist, dass niemand fehlte."),
    ("any-flattering-agreement", "Sie haben völlig recht, das Datum stimmt nicht."),
    ("any-flattering-agreement", "Gute Frage, ich schaue nach."),
    ("de-dive-in", "Die Kosten schlüsseln wir nach Abteilung auf."),
    ("de-dive-in", "Der Taucher taucht ein zweites Mal."),
    ("de-list-announcers", "Eine Vielzahl von Kunden hat geantwortet."),
    ("de-list-announcers", "Der Lieferant hat eine große Palette von Ersatzteilen."),
    ("de-list-announcers", "Die Farbpalette steht im Styleguide."),
]


@pytest.mark.parametrize(("sign", "text"), FORMS)
def test_a_weak_german_check_finds_its_inflected_forms(catalogue, sign, text):
    pattern = catalogue.signs[sign].pattern
    assert pattern is not None
    assert pattern.search(text), sign


@pytest.mark.parametrize(("sign", "text"), LEFT_ALONE)
def test_a_weak_german_check_leaves_plain_forms_alone(catalogue, sign, text):
    pattern = catalogue.signs[sign].pattern
    assert pattern is not None
    assert not pattern.search(text), sign
