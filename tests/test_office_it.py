"""Plain Italian work text, invented, against the real catalogue. A strong or usual sign counts alone, so one that fires
on any of these accuses a person of writing like a machine. Italian office mail runs on set phrases (Cordiali saluti,
Distinti saluti, Gentile Dott.ssa, In allegato Le trasmetto, In attesa di un cortese riscontro, Resto a disposizione,
Spett.le) and on burocratese (ai sensi dell'art., al fine di, con la presente si comunica, nell'ambito di, si è
proceduto alla verifica, u.s.), which avoid-ai-writing-multilingual says are no sign alone. People write what the
sources list and every office writes too: inoltre, pertanto and tuttavia, è importante sottolineare che and va notato
che, non solo… ma anche, svolge un ruolo fondamentale, in conclusione and in sintesi, vediamo insieme, nel mondo di
oggi, al giorno d'oggi (Manzoni's), nell'era digitale in a title. Chat drops an accent (perche, e' for è) and types
straight quotes (scrittura-italiana's false positives). They are a person's, never a sign. A weak sign may fire, but
plain work text must not reach a cluster.

Italian typography is how people write: a dash on each side of an aside and before a line of dialogue (humanizer-it's
ban fired on Pinocchio's), the short dash in a range, « », curly and straight quotes, the curly apostrophe. The dashes,
curly quotes and apostrophe are written as escapes, as ruff refuses them in source; the first test holds that they are
the real marks."""

import unicodedata

import pytest

from byhand import signs

DASH, SHORT, LQ, RQ, APOS = "\u2014", "\u2013", "\u201c", "\u201d", "\u2019"
# What an Italian draft loads: the `any` signs and Italian's, never another language's.
ITALIAN = ("any", "it")

MAIL = [
    "Gentile Dott.ssa Ferri,\n\nin allegato Le trasmetto la fattura n. 312 relativa ai servizi di ottobre. La prego di "
    "provvedere al pagamento entro il 30 novembre.\n\nResto a disposizione per eventuali chiarimenti.\n\nCordiali "
    "saluti,\nGiulia Marchetti",
    "Spett.le Bianchi Impianti S.r.l.,\n\ncon la presente si comunica che, ai sensi dell'art. 7 del contratto, il "
    "canone "
    "di manutenzione è aggiornato a decorrere dal 1° gennaio.\n\nIn attesa di un cortese riscontro, porgiamo distinti "
    "saluti.\n\nUfficio Acquisti",
    "Ciao Marco,\n\nti giro il file del preventivo, dagli un'occhiata quando puoi. Se ti torna, lo mandiamo lunedì.\n\n"
    "A presto,\nLuca",
    "Buongiorno a tutti,\n\nvi informo che venerdì l'ufficio chiude alle 14 per lavori all'impianto elettrico. Ci "
    "scusiamo per il disagio.\n\nCordiali saluti,\nL'Amministrazione",
    "Egregio Avvocato Rinaldi,\n\nfaccio seguito alla telefonata di ieri per trasmetterLe la documentazione richiesta, "
    "al fine di procedere alla registrazione dell'atto.\n\nDistinti saluti,\nDott. Paolo Greco",
    "Ciao Sara,\n\nnon solo il magazzino, ma anche l'ufficio acquisti deve mandare l'inventario entro giovedì. Me lo "
    "ricordi tu a Federica?\n\nGrazie mille,\nAnna",
    "Gentili colleghi,\n\nè importante sottolineare che le note spese vanno consegnate entro il 15 dicembre, con gli "
    "scontrini in originale.\n\nUn saluto,\nRisorse Umane",
    "Buonasera Ing. Conti,\n\ncome d'accordo, Le invio il verbale del sopralluogo. Vediamo insieme le modifiche alla "
    "riunione di martedì.\n\nCordialmente,\nElena Russo",
    "Gentile cliente,\n\nci scusiamo per il ritardo nella consegna del Suo ordine. Il corriere passerà giovedì 12. La "
    "ringraziamo per la pazienza.\n\nIl Servizio Clienti",
    "Ciao Fra,\n\nfino al mio ultimo aggiornamento del gestionale c'erano 12 scatole di carta A4. Ne ordino altre 20 "
    "per "
    "gennaio.\n\nCiao,\nAndrea",
    "Gentile Prof.ssa Galli,\n\nLe scrivo per chiederLe un ricevimento: vorrei discutere la bozza della tesi. Sarei "
    "disponibile mercoledì o giovedì mattina.\n\nCordiali saluti,\nMartina De Luca\nMatricola 845221",
    "Oggetto: Richiesta di ferie\n\nGentile Responsabile,\n\nil sottoscritto Mario Esposito chiede di poter usufruire "
    "di "
    "cinque giorni di ferie dal 22 al 26 luglio.\n\nDistinti saluti,\nMario Esposito",
    "Cari soci,\n\nnell'ambito del progetto con il Comune, il circolo apre anche la domenica mattina. Inoltre, la "
    "quota "
    "per il 2027 resta invariata.\n\nUn caro saluto,\nIl Presidente",
    "Ciao ragazzi,\n\nspero stiate bene. Vi mando il verbale di ieri; la sala 3 è prenotata per venerdì.\n\nUn "
    "abbraccio,\nChiara",
    "Buongiorno,\n\nsecondo le mie conoscenze, aggiornate al corso HACCP di marzo, il frigo va tenuto sotto i 4 gradi. "
    "Controllo e vi dico.\n\nSaluti,\nRoberta",
    "Gentile signora Moretti,\n\nLe confermo l'appuntamento di lunedì 18 alle 9:30 presso i nostri uffici di via "
    "Garibaldi "
    "21. In caso di impedimento, La prego di avvisarci per tempo.\n\nCordiali saluti,\nStudio Lombardi",
]
REPLIES = [
    "Certo! Ecco la versione corretta del preventivo:",
    "Certo, ecco la versione aggiornata della presentazione:",
    "Certo! Ecco la versione rivista del tuo preventivo, con i prezzi nuovi:",
    "Secondo le mie conoscenze aggiornate al corso HACCP, la temperatura va annotata ogni mattina.",
    "Fino al mio ultimo aggiornamento del file mancavano tre fatture.",
    "In qualità di referente IA, non ho accesso ai log di produzione.",
    "Certamente, ecco il contratto firmato:",
    "Con piacere! Ecco il verbale di ieri, con le correzioni di Paolo:",
    "Volentieri, ecco la mia bozza dell'annuncio:",
    # a person's role, contrast or verdict, near the model's role and its first person (#53's review, rounds 1 to 4)
    "Come responsabile IA, non posso approvare questa spesa senza il via libera della direzione.",
    "Come responsabile IA, non ho accesso ai log del fornitore.",
    "In quanto IA, non ho opinioni: lo dice il bot, non io.",
    "Come assistente di direzione, non ho accesso a quell'agenda: chiedi a Ilaria.",
    "Lo usiamo come modello di intelligenza artificiale, non come sostituto del giudizio dei tecnici.",
    "Lo vendono come intelligenza artificiale, non come gestionale.",
    "Copilot, in quanto IA, non ha accesso alla rete aziendale.",
    "Come IA, non ho niente da dire: ci fa risparmiare ore.",
    "Come IA non ho accesso a nessuna al lavoro, faccio tutto a mano.",
    "Come modello di business, non posso garantire margini più alti.",
    "In quanto azienda, non abbiamo accesso ai dati dei clienti.",
    "Ma in quanto ideatore del progetto, non posso accettare.",
    "Secondo le mie conoscenze il corso va rinnovato ogni due anni.",
]
CHAT = [
    "ok, ci sentiamo dopo",
    "Arrivo con 10 min di ritardo, iniziate pure 🙏",
    "Ottima domanda, non lo so 😅",
    "Ottima domanda! Ci penso e ti dico.",
    "Hai assolutamente ragione, ho sbagliato la data. È il 14.",
    "qualcuno ha il link della call?",
    "Domani c'è la riunione?",
    "Perfetto, d'accordo così 👍",
    "e' arrivato il corriere?",
    "perche non lo chiedi a Gianni?",
    "Certo! Te lo mando subito.",
    "vabbè, ne parliamo lunedì",
    "Fatto, l'ho messo nella cartella condivisa.",
    "Bella la presentazione, ingrandisci solo il carattere del grafico.",
    'Ha scritto "va bene", quindi direi che si fa.',
    "Grazie mille!! Domani ti passo quello del cliente",
]
NOTES = [
    "Verbale riunione di coordinamento " + SHORT + " 6 novembre\nPresenti: A. Rossi, B. Verdi, C. Neri\n"
    "- Budget 2027 approvato\n- Assunzioni: 2 posizioni aperte\n- Prossima riunione: 4 dicembre",
    "Note:\n- chiamare il notaio\n- mandare il contratto a Paolo [da confermare]\n- rivedere la data di consegna "
    "[da verificare]",
    "Cose da fare:\n1. Chiudere il mese\n2. Pagare i fornitori\n3. Rivedere il contratto d'affitto",
    "Orari dello sportello: dal lunedì al venerdì, 9" + SHORT + "13 e 14" + SHORT + "17.",
    "**Importante**: da lunedì il badge è obbligatorio.",
    "Turno di notte, 3/4 novembre\n\nNiente da segnalare. Nessun intervento nel parcheggio.",
    "Volantino: Pizzeria Da Gino. Forno a legna. Aperti anche a pranzo.",
]
REPORTS = [
    "Relazione mensile di ottobre\n\nIl fatturato ha raggiunto 1,2 milioni di euro, il 4% in più di settembre. Il "
    "punto "
    "vendita di Bergamo ha chiuso il trimestre in perdita, per il secondo trimestre di fila.\n\nPer quanto riguarda il "
    "personale, sono entrati due tecnici. Va notato che l'affitto aumenta a gennaio.",
    "Con riferimento alla Vs. nota prot. n. 1234 del 3 ottobre u.s., si comunica che si è proceduto alla verifica "
    "della "
    "documentazione trasmessa. La pratica risulta completa e sarà esaminata nella seduta del 20 novembre.",
    "Determinazione dirigenziale n. 45\n\nIl Dirigente, visto il D.Lgs. 267/2000, ai sensi dell'art. 107, al fine di "
    "garantire la continuità del servizio, determina di prorogare l'affidamento fino al 31 marzo 2027.",
    "Risultati\n\nI testi sono stati annotati automaticamente. Inoltre, le frasi sono state analizzate con un parser a "
    "dipendenze. Tuttavia, è importante sottolineare che il campione è ridotto.",
    "Conclusioni\n\nIn conclusione, il progetto rispetta i tempi previsti. Pertanto, si propone di mantenere il "
    "fornitore "
    "attuale anche per il 2027.",
    "In sintesi, la scuola svolge un ruolo fondamentale nel quartiere: 400 iscritti e il doposcuola aperto fino alle "
    "sei.",
    "Relazione della commissione\n\nNon si tratta di un guasto della bilancia, ma di una tara registrata male sul "
    "documento di trasporto. Il documento è stato corretto e il cliente è stato avvisato.",
    "Nel mondo di oggi i ragazzi leggono meno: lo dice l'indagine del 2025, che conta il 38% di lettori tra i 15 e i "
    "17 "
    "anni.",
    "Programma del convegno\n\nLa tutela dei dati nell'era digitale: tavola rotonda con il Garante, ore 15.",
    "Al giorno d'oggi quasi tutti i pagamenti in negozio passano dal POS: a ottobre il contante è sceso al 31%.",
    "Manuale utente\n\nNell'editor, fare clic su [Inserisci] e scegliere Tabella. Il sistema può, facoltativamente, "
    "inviare un avviso via e-mail. Per impostazione predefinita, i report sono generati il lunedì e conservati per 90 "
    "giorni.",
    "Parere tecnico\n\nIl ponte va rinforzato. Il punto è che il lavoro del 2015 non ha risolto le infiltrazioni, e "
    "sempre "
    "più camion usano la provinciale. In un mercato sempre più competitivo, il preventivo va chiuso entro marzo.",
    "Verbale di assemblea condominiale\n\nL'assemblea, dopo ampia discussione, delibera all'unanimità di affidare i "
    "lavori "
    "di rifacimento della facciata alla ditta Edil Sud, per un importo di 48.000 euro più IVA.",
    "Abstract\n\nIl lavoro analizza l'insegnamento della scrittura nell'era dell'intelligenza artificiale, con "
    "particolare "
    "attenzione al ruolo del docente. Lo studio si basa su 120 questionari raccolti in sei licei.",
    "Il lago di Ledro è un lago alpino del Trentino, a 655 metri di altitudine. È noto per il villaggio palafitticolo "
    "scoperto nel 1929, quando il livello delle acque fu abbassato.",
    "Riunione di reparto\n\nVediamo insieme i numeri del trimestre: le vendite scendono dell'8%, i resi sono stabili. "
    "In "
    "definitiva, il budget va rivisto a gennaio.",
]
SPEECHES = [
    "Cari soci,\n\nin un mondo sempre più di corsa, la nostra cooperativa continua ad aprire il mercato il sabato. "
    "Quest'anno eravamo 212. Grazie a tutti.",
    "Caro Antonio,\n\nci mancherai in contabilità, e non poco: trentadue anni non sono pochi. Goditi la casa al lago.",
]
POSTS = [
    "Dopo sei anni in Logistica Nord, saluto tutti. Grazie a Ilaria e a Pietro per gli inventari della domenica. Dal 2 "
    "dicembre sono in Rota Verde. #Milano #logistica",
    "Sabato apriamo il nuovo negozio in via Roma 14: caffè e torta per tutti, dalle 10 alle 13. Vi aspettiamo!",
    "La raccolta di sabato è andata bene: 40 volontari e 300 piantine messe a dimora. Grazie a tutti!",
]
TYPOGRAPHY = [
    "Il fornitore " + DASH + " o meglio, il suo commerciale " + DASH + " richiama domani.",
    DASH + " Hai visto la mail di Luigi?\n" + DASH + " Sì, chiede un'altra settimana " + DASH + " rispose Marta.",
    DASH + " Che vuoi? " + DASH + " disse il falegname. " + DASH + " Niente.",
    "Il cliente ha detto: «Firmiamo la settimana prossima». Preferisco non sbilanciarmi.",
    "Ha risposto " + LQ + "non prima di marzo" + RQ + ", il che ci va bene.",
    'Nel modulo scrivete "da definire" e lasciate vuota la data.',
    "Prezzo: 1.250,50 € (IVA inclusa). Consegna: 3" + SHORT + "5 giorni lavorativi.",
    "L" + APOS + "ufficio " + DASH + " quello al secondo piano " + DASH + " riapre a gennaio.",
    "La riunione " + SHORT + " ricordi? " + SHORT + " è spostata a giovedì.",
]

OFFICE = MAIL + REPLIES + CHAT + NOTES + REPORTS + SPEECHES + POSTS + TYPOGRAPHY

KINDS = [
    *((text, "email") for text in MAIL + REPLIES),
    *((text, "message") for text in CHAT),
    *((text, "document") for text in NOTES + REPORTS + SPEECHES + TYPOGRAPHY),
    *((text, "post") for text in POSTS),
]


def test_the_marks_are_the_real_ones():
    # an escape that lost its backslash would leave the lines holding ASCII, and the test passing on nothing
    assert unicodedata.name(DASH) == "EM DASH"
    assert unicodedata.name(SHORT) == "EN DASH"
    assert unicodedata.name(LQ) == "LEFT DOUBLE QUOTATION MARK"
    assert unicodedata.name(RQ) == "RIGHT DOUBLE QUOTATION MARK"
    assert unicodedata.name(APOS) == "RIGHT SINGLE QUOTATION MARK"
    assert sum(DASH in text for text in OFFICE) >= 3
    assert sum("«" in text for text in OFFICE) >= 1
    assert len(OFFICE) >= 60


@pytest.mark.parametrize(("text", "kind"), KINDS)
def test_no_sign_that_counts_alone_fires_on_plain_italian_work_text(counted_alone, reads, text, kind):
    fired = [sign.id for sign in counted_alone if reads(sign, kind) and sign.pattern and sign.pattern.search(text)]
    assert fired == []


# What each sign that counts alone exists to catch, inside Italian text: a line per Italian branch of its check, and one
# for each artefact, which is the same string in every language, so silence above can't come from a sign that finds
# nothing. Branches that read other languages' words have their lines in the other office tests.
MACHINE = [
    ("any-ai-self-reference", "In quanto IA, non ho accesso al listino del fornitore."),
    ("any-ai-self-reference", "In qualità di IA, non ho accesso a internet."),
    ("any-assistant-preamble", "Certo! Ecco una versione più formale della tua email:"),
    ("any-assistant-preamble", "Certamente! Ecco la versione corretta del tuo curriculum:"),
    ("any-assistant-preamble", "Con piacere! Ecco a te una versione più breve del tuo post, senza ripetizioni:"),
    ("any-knowledge-cutoff", "Secondo le mie conoscenze aggiornate a ottobre 2023, la fusione non era conclusa."),
    ("any-knowledge-cutoff", "Secondo le mie conoscenze aggiornate al 2021, il marchio apparteneva al gruppo."),
    ("any-ai-self-reference", "Come modello di intelligenza artificiale, non ho accesso al tuo calendario."),
    ("any-ai-self-reference", "Mi dispiace, ma in quanto IA non ho accesso a internet."),
    ("any-ai-self-reference", "Come modello di intelligenza artificiale non ho accesso al web."),
    ("any-ai-self-reference", "Tuttavia, in quanto IA, non ho accesso ai dati della tua azienda."),
    ("any-emoji-markers", "- 🚀 Nuova offerta di formazione"),
    ("any-emoji-markers", "## 📊 I numeri del mese"),
    ("any-unfilled-placeholder", "Iscrizioni: insert_link_here"),
    ("any-chatgpt-citation-markup", "Il fatturato è cresciuto. :contentReference[oaicite:0]{index=0}"),
    ("any-chatgpt-citation-markup", "Il fatturato è cresciuto. turn0search4"),
    ("any-chatbot-url-tag", "Fonte: https://esempio.it/relazione?utm_source=chatgpt.com"),
    ("any-gemini-citation-markup", "Lo stabilimento ha aperto nel 1998 [cite: 3]."),
    ("any-grok-citation-markup", "Lo stabilimento ha aperto nel 1998. grok_card"),
    ("any-deepseek-citation-markup", "Lo stabilimento ha aperto nel 1998【4†source】."),
    ("any-chat-tool-markup", "Secondo il documento allegato[attached_file:1], il margine scende."),
]


@pytest.mark.parametrize(("sign", "text"), MACHINE)
def test_the_signs_still_find_what_they_are_for_in_italian(catalogue, read_in, sign, text):
    # as a Italian check runs it: the forms under it and any, never another language's
    pattern = read_in(catalogue.signs[sign], "it")
    assert pattern is not None
    assert pattern.search(text), sign


def test_every_italian_form_of_a_shared_sign_has_a_machine_line(unproven):
    assert unproven(MACHINE + FORMS, "it") == []


@pytest.mark.parametrize(("text", "kind"), KINDS)
def test_plain_italian_work_text_makes_no_weak_cluster(weak_hits, text, kind):
    for paragraph in text.split("\n\n"):
        assert weak_hits(paragraph, kind, ITALIAN) < signs.WEAK_CLUSTER, paragraph


def test_the_weak_counting_counts_a_cluster(weak_hits):
    # so the test above can fail: three different weak habits in one paragraph of a post
    text = "Ottima domanda! In un mondo sempre più veloce, il quartiere riapre il mercato " + DASH + " e con la musica."
    assert weak_hits(text, "post", ITALIAN) == signs.WEAK_CLUSTER


@pytest.mark.parametrize(
    "text",
    [
        "In un mondo sempre più veloce, la fiera torna domenica " + DASH + " e stavolta con **la banda**.",
        "**Novità:** in un mondo sempre più veloce, la fiera torna domenica " + DASH + " e con la banda.",
    ],
)
def test_a_dash_pivot_takes_no_other_sign_s_words(weak_hits, text):
    # the dash's match runs from the line's start over another sign's phrase or check, but Grep runs each sign on its
    # own: three (#56)
    assert weak_hits(text, "post", ITALIAN) == signs.WEAK_CLUSTER


def test_one_habit_repeated_counts_once(weak_hits):
    text = "In un mondo sempre più veloce, in un mondo sempre più caro e in un mondo sempre più stanco."
    assert weak_hits(text, "document", ITALIAN) == 1


def test_the_italian_checks_read_posts_and_documents_but_the_dash(catalogue):
    # the set phrases of mail and chat (cordiali saluti, resto a disposizione, in attesa di un cortese riscontro) would
    # add up in mail: no Italian sign that reads mail has a pattern but the dash, which is one habit however often it
    # fires
    reading_mail = sorted(
        sign.id
        for sign in catalogue.signs.values()
        if sign.language == "it" and sign.pattern and {"any", "email", "message"} & set(sign.kinds)
    )
    assert reading_mail == ["it-dash-pivots"]


@pytest.mark.parametrize("text", TYPOGRAPHY)
def test_italian_typography_meets_no_formatting_check(catalogue, text):
    # of the files an Italian draft reads: English's and Korean's dash signs fire here, and no Italian draft loads them
    fired = [
        sign.id
        for sign in catalogue.signs.values()
        if sign.language in ITALIAN and sign.category == "formatting" and sign.pattern and sign.pattern.search(text)
    ]
    assert fired == []


# Italian sets asides between dashes and opens dialogue with one: the forms a weak check must still find, beyond its
# own `flags`, and the plain forms it must leave alone.
FORMS = [
    ("it-dash-pivots", "Abbiamo provato per una settimana" + DASH + "e nessuno è tornato al vecchio sistema."),
    ("it-dash-pivots", "Il mercato torna domenica " + DASH + " con le frittelle."),
    (
        "it-dash-pivots",
        "La fiera "
        + DASH
        + " quella di agosto "
        + DASH
        + " torna. Il mercato apre domenica "
        + DASH
        + " e con i dolci.",
    ),
    ("it-dash-pivots", DASH + " Arrivo " + DASH + " disse Marta. Poi uscì " + DASH + " e non tornò."),
    ("it-dash-pivots", "Nota: il server è fermo " + DASH + " torna domani."),
    ("it-inflated-stakes", "In un mondo sempre più veloce, la biblioteca apre la sera."),
    ("it-inflated-stakes", "La fiera compie 30 anni in un mondo sempre più distratto."),
    ("any-flattering-agreement", "Ottima domanda! Partiamo dal budget."),
]

LEFT_ALONE = [
    ("it-dash-pivots", "Il fornitore " + DASH + " o il suo commerciale " + DASH + " richiama domani."),
    ("it-dash-pivots", DASH + " Arrivo " + DASH + " disse Marta."),
    ("it-dash-pivots", DASH + " Arrivo. Aspetta un attimo " + DASH + " disse Marta."),
    ("it-dash-pivots", "Marta disse: " + DASH + " Va bene."),
    ("it-dash-pivots", "Il falegname rispose: " + DASH + " Niente, grazie."),
    ("it-dash-pivots", "Il negozio è aperto 10" + SHORT + "20 il sabato."),
    ("it-dash-pivots", "La riunione " + DASH + " ricordi? " + DASH + " è spostata a giovedì."),
    ("it-dash-pivots", "La riunione " + SHORT + " ricordi? " + SHORT + " è spostata a giovedì."),
    ("it-inflated-stakes", "In un mercato sempre più competitivo, il prezzo conta."),
    ("it-inflated-stakes", "Nel mondo di oggi i ragazzi leggono meno."),
    ("it-inflated-stakes", "Sempre più clienti pagano con il POS."),
    ("it-inflated-stakes", "La tutela dei dati nell'era digitale."),
    ("it-inflated-stakes", "Al giorno d'oggi quasi tutti pagano con la carta."),
    # the closers people write: the closing summary has no Italian form (#58's review, F1)
    ("any-closing-summary", "In conclusione, il progetto rispetta i tempi."),
    ("any-closing-summary", "In sintesi, la scuola ha 400 iscritti."),
    ("any-closing-summary", "Per concludere, ringrazio tutti i presenti."),
    ("any-flattering-agreement", "Ottima domanda, non lo so."),
]


@pytest.mark.parametrize(("sign", "text"), FORMS)
def test_a_weak_italian_check_finds_its_forms(catalogue, sign, text):
    pattern = catalogue.signs[sign].pattern
    assert pattern is not None
    assert pattern.search(text), sign


@pytest.mark.parametrize(("sign", "text"), LEFT_ALONE)
def test_a_weak_italian_check_leaves_plain_forms_alone(catalogue, sign, text):
    pattern = catalogue.signs[sign].pattern
    assert pattern is not None
    assert not pattern.search(text), sign
