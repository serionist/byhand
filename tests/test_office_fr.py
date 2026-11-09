"""Plain French work text, invented, against the real catalogue. A strong or usual sign counts alone, so one that fires
on any of these accuses a person of writing like a machine. Formal French mail runs on set phrases (Je me permets de,
N'hésitez pas à, Je reste à votre disposition, Veuillez agréer, dans le cadre de): they are a person's, never a sign. A
weak sign may fire, but plain work text must not reach a cluster.

French typography is how people write: « » with no-break spaces, a space before ; : ! ?, the dash of dialogue and an
incise now and then. The curly apostrophe, the no-break spaces and the dashes are written as escapes, as ruff refuses
them in source; the first test holds that they are the real marks."""

import re
import unicodedata

import pytest

from byhand import signs

# A space before a French colon or exclamation mark is a no-break one: NBSP, or the narrow one Word and macOS type.
NB = "\u00a0"
NNB = "\u202f"

FORMAL_MAIL = (
    "Bonjour Madame Leroy,\n\nJe me permets de revenir vers vous au sujet du devis n° 2026-118. Pourriez-vous me "
    f"confirmer la date de livraison{NB}?\n\nJe reste à votre disposition pour tout complément d'information.\n\n"
    "Bien cordialement,\nThomas Girard"
)
NOTICE = (
    "Bonjour à tous,\n\nDans le cadre de la clôture annuelle, merci de transmettre vos notes de frais avant le 15 "
    "décembre. Il convient de rappeler que les justificatifs sont obligatoires. N'hésitez pas à me contacter en cas de "
    "question.\n\nCordialement,\nNadia Belkacem"
)
LETTER = (
    "Madame, Monsieur,\n\nSuite à notre entretien téléphonique du 4 novembre, je vous confirme ma candidature au poste "
    "de comptable. Vous trouverez ci-joint mon CV.\n\nVeuillez agréer, Madame, Monsieur, l\u2019expression de mes "
    "salutations distinguées.\n\nClaire Mounier"
)
QUEBEC_MAIL = (
    "Bonjour Mme Tremblay,\n\nJe vous fais suivre le courriel de la comptabilité. Pourriez-vous me revenir d'ici "
    "vendredi? Merci beaucoup!\n\nBonne journée,\nÉtienne"
)
MINUTES = (
    "Compte rendu du comité de pilotage du 6 novembre\n\nDans le cadre du projet Atlas, le comité a validé le "
    "budget de la phase 2. Il est à noter que le prestataire a livré avec deux semaines de retard. Par ailleurs, la "
    "formation des utilisateurs s'articule autour de trois sessions. Il convient de rappeler que la mise en "
    "production reste fixée au 15 janvier.\n\nEn outre, les équipes métier demandent un second environnement de "
    "test. Pour conclure, le comité maintient le planning. Prochain comité\u00a0: 4 décembre."
)
REPORT = (
    "Rapport mensuel \u2013 octobre\n\nLe chiffre d'affaires atteint 1,2 M€, en hausse de 4 %. Le projet reste au cœur "
    "de notre plan 2027 et c'est un levier important pour réduire les coûts. L'écosystème des fournisseurs locaux est "
    "crucial pour nous ; nous ne pourrons pas nous en passer.\n\nCependant, deux clients ont résilié. Le changement de "
    "transporteur pourrait éventuellement décaler les livraisons de deux jours."
)
TYPOGRAPHY = [
    f"Le client a dit{NB}: «{NB}On signe la semaine prochaine.{NB}» Je reste prudent{NNB}; on verra lundi{NNB}!",
    "\u2014 Tu as vu le mail de Paul\u00a0?\n\u2014 Oui, il veut un délai. Le dossier \u2013 je te l'avais dit \u2013 "
    "reste incomplet.",
    "Le fournisseur \u2014 enfin, son commercial \u2014 nous rappelle demain.",
    f"Horaires{NB}: 9 h \u2013 17 h, du lundi au vendredi. Budget{NB}: 2 000\u20133 000 €.",
    "\u2013 Café pour tout le monde\u00a0?\n\u2013 Non merci, j'en ai déjà pris deux.",
    "Il m\u2019a répondu «\u202fpas avant mars\u202f», ce qui nous arrange.",
]
CHAT = [
    "@Léa tu peux relire la slide 4 stp\u00a0? Merci\u00a0!",
    "Je suis en retard de 10 min, commencez sans moi 🙏",
    "Ok pour moi 👍",
    "Et vous, vous venez au pot jeudi ?",
    "Et si on décalait le point à 15 h ?",
    "Salut! Je suis sur le call avec le client, je te reviens dans 5 min.",
    "Allo Karine! Ça fait du sens pour moi, on peut fermer le dossier. Je te confirme le tout par courriel.",
    "Soyons clairs, la date du 30 est ferme. Pour être honnête, je préfère qu'on ne la bouge pas.",
    "Bonne nouvelle : le client a signé ! On lance la production lundi.",
    "Le serveur de recette est down depuis 9 h, je regarde. Ça pourrait potentiellement venir du certificat.",
]
OWN_POST = (
    "Je quitte Lyon après six ans chez Brico+. Merci à Inès et Paul pour les inventaires du dimanche. Pour être "
    "honnête, le magasin va me manquer. Je commence chez Vélocité le 2 décembre. #Lyon #vélo"
)

# A plain compte rendu, which a review found reaching a weak cluster on three set phrases (#24, F3).
MEETING_NOTE = (
    "Compte rendu de l'entretien avec le transporteur, 3 novembre\n\nIl convient de noter que les retards viennent du "
    "dépôt de Rungis. Force est de constater que le nouveau planning n'a rien changé. Il ressort de cet échange que le "
    "transporteur paiera les pénalités d'octobre."
)
# Plain reports that a review found reaching 3 weak hits, written anew: each a set phrase of a compte rendu (#24, F9).
REPORTS = [
    "En conclusion, il ne s'agit pas de fermer l'accueil de Blois, mais de le regrouper avec celui d'Orléans. "
    "Il convient de noter qu'aucun poste n'est supprimé.",
    "Compte rendu du CSE du 14 octobre\n\nLa direction précise qu'il ne s'agit pas de vendre l'entrepôt, mais de le "
    "louer à la coopérative. Il convient de noter que le bail court sur trois ans. Soyons lucides : les élus n'ont pas "
    "eu les chiffres avant la séance.",
    "En conclusion, l'intérêt de ce partenariat avec la mairie n'est plus à démontrer. Il est important de noter qu'il "
    "prend fin le 31 décembre.",
]
# People open speeches and editos on the fast-changing world too, so fr-stock-openers is weak (#24, F2).
SPEECHES = [
    "Chers coopérateurs,\n\nDans un monde en pleine mutation, notre coopérative a tenu bon : 212 adhérents, deux "
    "magasins et un bilan à l'équilibre. Merci à chacun.",
    "Le mot du maire\n\nDans un monde qui change à toute vitesse, Saint-Aubin garde ses commerces : la boulangerie "
    "rouvre le 2 décembre et le marché passe au samedi.",
    "Cher Gérard,\n\nDans un monde en constante évolution, tu as été notre point fixe pendant 32 ans à la compta. "
    "Profite bien de ton potager.",
]

OFFICE = [
    # mail, vous and tu, France and Quebec, with the set phrases of formal French
    FORMAL_MAIL,
    NOTICE,
    LETTER,
    QUEBEC_MAIL,
    "Bonjour Monsieur Benali,\n\nVous avez tout à fait raison, la facture comporte une erreur sur la TVA. Je vous fais "
    "parvenir un avoir d'ici vendredi.\n\nToutes mes excuses pour ce contretemps.\nSophie",
    "Salut Julien,\n\nJe t'envoie le compte rendu de jeudi. Dis-moi si j'ai oublié quelque chose, sinon je le diffuse "
    "lundi.\n\nBonne soirée,\nMarc",
    "Bonjour,\n\nNous sommes heureux de vous accueillir le 12 janvier pour votre premier jour. Votre badge sera prêt à "
    "l'accueil.\n\nÀ bientôt,\nL'équipe RH",
    "Petite correction\u00a0: la réunion a lieu le 12 mars, et non le 15 comme indiqué hier.",
    "Le changement de transporteur pourrait éventuellement décaler la livraison de deux jours. Je vous tiens informé.",
    "Ce n'est pas la bonne version, c'est celle de mardi qu'il faut imprimer.",
    "Je vous joins la nouvelle version du contrat. N'hésitez pas à revenir vers moi si besoin.",
    "Comme convenu, je vous adresse le bon de commande signé. Je reste à votre disposition.",
    "Pour être transparent avec vous, nous n'aurons pas le budget avant mars.",
    "Pour conclure, je propose qu'on garde le prestataire actuel jusqu'en juin.",
    # chat: Teams and Slack
    *CHAT,
    "Quelqu'un a le lien du Drive pour le projet Atlas ?",
    # a person's role, near the model's "en tant qu'IA, je"
    "En tant qu'assistante de direction, je gère les agendas du comité ; écris-moi pour un créneau.",
    "En tant qu'IA lead, je pilote le chantier données avec Hugo.",
    "En tant que responsable du site, je vous confirme la fermeture du parking samedi.",
    "En tant qu\u2019assistant de Mme Roy, je vous transmets son accord.",
    # colon-ended replies, and a person handing over or returning their own draft
    f"Bien sûr{NB}! Voici la version corrigée{NB}:",
    f"Bien sûr{NNB}! Voici une version plus courte{NNB}:",
    f"Avec plaisir{NB}! Voici ma proposition pour le planning{NB}:",
    "Voici le brouillon de l'annonce, dis-moi ce que tu en penses :",
    f"Bien sûr{NB}! Voici une version améliorée du planning{NB}:",
    f"Certainement. Voici la nouvelle version de votre contrat, avec les deux corrections demandées{NB}:",
    "Absolument! Voici une version retravaillée de mon texte d'hier:",
    f"Bien sûr{NB}! Voici une version corrigée de votre bon de commande, avec le bon RIB{NB}:",
    # a supplier and an assistant reworking the reader's own document, which names no text of theirs (#24's review)
    f"Avec plaisir. Voici une version retravaillée de votre devis, avec la remise de 5{NB}%{NB}:",
    f"Bien sûr{NB}! Voici une version plus formelle de votre courrier{NB}:",
    f"Bien sûr{NB}! Voici une version corrigée de votre texte, avec les deux fautes en moins{NB}:",
    "Je te renvoie mon texte retravaillé :\n\nL'atelier vélo ouvre le samedi de 10 h à 13 h.",
    # notes, minutes and reports
    "Compte rendu \u2013 réunion du 6 novembre\nPrésents : A. Martin, B. Diallo, C. Roy\n- Budget 2027 validé\n"
    "- Recrutement : 2 postes ouverts\n- Prochaine réunion le 4 décembre",
    "Notes perso :\n- rappeler le notaire\n- envoyer le [date à confirmer] à Paul\n- relire le contrat [à compléter]",
    "Modèle de relance\u00a0: «\u00a0Bonjour, je reviens vers vous concernant la facture du mois dernier.\u00a0»",
    "**Important** : le badge est obligatoire à partir de lundi.",
    MINUTES,
    MEETING_NOTE,
    *REPORTS,
    *SPEECHES,
    REPORT,
    "Notre secteur est en constante évolution : trois concurrents ont fermé cette année.",
    "Dans le monde de la logistique, tout va très vite ; on a changé deux fois de transporteur.",
    "Dans un monde idéal, on livrerait tout avant Noël.",
    "Selon ma dernière mise à jour du tableau, il reste 12 colis à livrer.",
    "Mes connaissances en droit fiscal s'arrêtent là, je demande à Inès.",
    # French typography
    *TYPOGRAPHY,
    OWN_POST,
]


def test_no_french_check_counts_alone(counted_alone):
    # fr-stock-openers was the last, made weak in #24's review: a speech or an edito opens that way too. A French sign
    # with a pattern that counts alone needs its lines in MACHINE below, a line per branch of its check.
    assert [sign.id for sign in counted_alone if sign.language == "fr"] == []


def test_the_marks_are_the_real_ones():
    # an escape that lost its backslash would leave the lines holding ASCII, and the test passing on nothing
    assert unicodedata.name(NB) == "NO-BREAK SPACE"
    assert unicodedata.name(NNB) == "NARROW NO-BREAK SPACE"
    assert sum(NB in text or NNB in text for text in OFFICE) >= 10
    assert sum("\u2019" in text for text in OFFICE) >= 3
    assert sum("\u2014" in text for text in OFFICE) >= 2
    assert len(OFFICE) >= 40


@pytest.mark.parametrize("text", OFFICE)
def test_no_sign_that_counts_alone_fires_on_plain_french_work_text(counted_alone, text):
    assert [sign.id for sign in counted_alone if sign.pattern and sign.pattern.search(text)] == []


# What each sign that counts alone exists to catch, inside French text: a line per branch of its check, so silence above
# can't come from a sign that finds nothing, or a branch that stopped finding. Branches that read only English, German,
# Russian, Chinese or Japanese words have their lines in the other office tests.
MACHINE = [
    ("any-ai-self-reference", "En tant qu'IA, je n'ai pas d'avis sur le choix du prestataire."),
    ("any-ai-self-reference", "En tant qu\u2019intelligence artificielle, je ne peux pas signer ce document."),
    ("any-ai-self-reference", "En tant que modèle de langage, je ne dispose pas de vos chiffres."),
    ("any-ai-self-reference", "En tant que grand modèle de langage, je ne peux pas vérifier ce lien."),
    ("any-ai-self-reference", "En tant qu'assistant virtuel, je vous propose trois options."),
    ("any-ai-self-reference", "En tant qu\u2019assistant d\u2019IA, je n'ai pas accès à votre agenda."),
    ("any-assistant-preamble", f"Bien sûr{NB}! Voici une version améliorée de votre e-mail{NB}:"),
    ("any-assistant-preamble", f"Avec plaisir{NNB}! Voici une version plus professionnelle de votre message{NNB}:"),
    ("any-assistant-preamble", "Certainement ! Voici une nouvelle version reformulée de votre courriel :"),
    ("any-assistant-preamble", "Absolument! Voici une version plus chaleureuse de votre annonce:"),
    ("any-assistant-preamble", "Bien sûr ! Voici une version révisée de votre mail :"),
    ("any-assistant-preamble", "Avec plaisir ! Voici une version plus concise de votre message :"),
    ("any-assistant-preamble", "Certainement ! Voici une version plus courte de ton post LinkedIn :"),
    ("any-assistant-preamble", "Bien sûr ! Voici une version plus claire de votre courriel :"),
    ("any-assistant-preamble", "Absolument ! Voici une version plus professionnelle et plus claire de votre e-mail :"),
    ("any-assistant-preamble", "Avec plaisir ! Voici votre e-mail reformulé :"),
    ("any-assistant-preamble", "Bien sûr ! Voici une version plus concise de votre rapport :"),
    ("any-assistant-preamble", "Avec plaisir ! Voici une version améliorée de ton CV :"),
    ("any-assistant-preamble", "Certainement ! Voici votre compte rendu retravaillé :"),
    ("any-assistant-preamble", "Bien sûr ! Voici ton texte retravaillé, prêt à envoyer :"),
    ("any-assistant-preamble", "Bien sûr ! Voici une version plus fluide de ton texte, prête à poster :"),
    ("any-assistant-preamble", "Avec plaisir ! Voici une version peaufinée de ta lettre de motivation :"),
    ("any-assistant-preamble", "Certainement ! Voici une version plus engageante de votre publication LinkedIn :"),
    ("any-unfilled-placeholder", "Bien cordialement,\n[Votre nom]"),
    ("any-unfilled-placeholder", "Je travaille chez [Nom de l\u2019entreprise] depuis trois ans."),
    ("any-unfilled-placeholder", "Pour plus d'informations : [Insérer le lien]"),
    ("any-unfilled-placeholder", "Contact : [vos coordonnées]"),
    ("any-unfilled-placeholder", "Bonjour [Nom du destinataire],"),
    ("any-unfilled-placeholder", "Le bilan sera publié le 2026-xx-xx."),
    ("any-unfilled-placeholder", "Inscriptions : insert_link_here"),
    ("any-knowledge-cutoff", "À la date de mes connaissances, la société n'a pas fusionné."),
    ("any-emoji-markers", "- 🚀 Nouvelle offre de formation"),
    ("any-emoji-markers", "## 📊 Les chiffres du mois"),
    ("any-emoji-markers", "1. ✨ Un accueil plus rapide"),
    ("any-chatgpt-citation-markup", "Le chiffre d'affaires a progressé. :contentReference[oaicite:0]{index=0}"),
    ("any-chatgpt-citation-markup", "Le chiffre d'affaires a progressé. oaicite:2"),
    ("any-chatgpt-citation-markup", "Le chiffre d'affaires a progressé. oai_citation:1"),
    ("any-chatgpt-citation-markup", "Le chiffre d'affaires a progressé. attributableIndex"),
    ("any-chatgpt-citation-markup", "Le chiffre d'affaires a progressé. turn0search4"),
    ("any-chatbot-url-tag", "Source : https://exemple.fr/rapport?utm_source=chatgpt.com"),
    ("any-chatbot-url-tag", "Source : https://exemple.fr/rapport?utm_source=openai"),
    ("any-chatbot-url-tag", "Source : https://exemple.fr/rapport?utm_source=copilot.com"),
    ("any-chatbot-url-tag", "Source : https://exemple.fr/rapport?utm_source=claude.ai"),
    ("any-chatbot-url-tag", "Source : https://exemple.fr/rapport?utm_source=perplexity.ai"),
    ("any-chatbot-url-tag", "Source : https://exemple.fr/rapport?referrer=grok.com"),
    ("any-gemini-citation-markup", "L'usine a ouvert en 1998.[span_1](start_span)"),
    ("any-gemini-citation-markup", "L'usine a ouvert en 1998 [cite: 3]."),
    ("any-grok-citation-markup", "L'usine a ouvert en 1998. grok_render_citation_card_json"),
    ("any-grok-citation-markup", "L'usine a ouvert en 1998. grok_card"),
    ("any-grok-citation-markup", "L'usine a ouvert en 1998. <grok-card id=2>"),
    ("any-deepseek-citation-markup", "L'usine a ouvert en 1998【4†source】."),
    ("any-chat-tool-markup", "Selon le document joint[attached_file:1], la marge recule."),
    ("any-chat-tool-markup", "Selon le site officiel[web:3], la marge recule."),
    ("any-chat-tool-markup", "Voir ppl-ai-file-upload pour le détail."),
    ("any-chat-tool-markup", ":::writing{variant=standard}"),
]


@pytest.mark.parametrize(("sign", "text"), MACHINE)
def test_the_signs_still_find_what_they_are_for_in_french(counted_alone, sign, text):
    pattern = {found.id: found.pattern for found in counted_alone}[sign]
    assert pattern is not None
    assert pattern.search(text), sign


WEAK_CASES = [
    (FORMAL_MAIL, "email"),
    (NOTICE, "email"),
    (LETTER, "email"),
    (QUEBEC_MAIL, "email"),
    (MINUTES, "document"),
    (REPORT, "document"),
    (REPORT, "email"),
    (OWN_POST, "post"),
    (MEETING_NOTE, "document"),
    *((line, "document") for line in REPORTS),
    *((line, "document") for line in SPEECHES),
    *((line, "message") for line in CHAT),
    *((line, "document") for line in TYPOGRAPHY),
]


@pytest.mark.parametrize(("text", "kind"), WEAK_CASES)
def test_plain_french_work_text_is_no_weak_cluster(weak_hits, text, kind):
    assert weak_hits(text, kind) < signs.WEAK_CLUSTER


def test_the_weak_counting_counts_a_cluster(weak_hits):
    # so the test above can fail: three different weak phrases in one paragraph of a post
    text = (
        "Dans cet article, nous allons voir pourquoi ce partenariat crée une synergie rare. "
        "Il convient de souligner que nos équipes sont plus motivées que jamais."
    )
    assert weak_hits(text, "post") >= signs.WEAK_CLUSTER


def test_another_language_s_dash_check_takes_no_french_check(weak_hits):
    # de-em-dash's letters beside the dashes overlap both French checks, which a French draft never loads with it (#56)
    text = "Et si notre synergie pourrait potentiellement — enfin — changer tout ?"
    assert weak_hits(text, "post") == signs.WEAK_CLUSTER


def test_one_habit_repeated_counts_once(weak_hits):
    text = "Notre synergie avec Lyon et notre synergie avec Lille comptent. Les synergies se multiplient."
    assert weak_hits(text, "document") == 1


def test_only_the_hedge_stack_reads_mail_and_chat_among_the_french_weak_checks(catalogue, reads):
    # The set phrases of formal mail and office chat (il convient de, soyons clairs, Et vous ?, #canal) would add up in
    # mail; the French weak checks read posts and documents, and only the doubled hedge reads every kind.
    reading_mail = sorted(
        sign.id
        for sign in catalogue.signs.values()
        if sign.language == "fr"
        and sign.pattern
        and sign.strength == "weak"
        and (reads(sign, "email") or reads(sign, "message"))
    )
    assert reading_mail == ["fr-hedge-stack"]
    assert set(catalogue.signs["fr-engagement-lines"].kinds) == {"post"}
    assert set(catalogue.signs["fr-hashtag-block"].kinds) == {"post"}


@pytest.mark.parametrize("text", TYPOGRAPHY)
def test_french_typography_meets_no_formatting_check(catalogue, text):
    # of the files a French draft reads: English's and Korean's dash signs fire here, and no French draft loads them
    fired = [
        sign.id
        for sign in catalogue.signs.values()
        if sign.language in {"any", "fr"}
        and sign.category == "formatting"
        and sign.pattern
        and sign.pattern.search(text)
    ]
    assert fired == []


# French elides with either apostrophe and inflects for gender and number: the forms a weak check must still find,
# beyond its own `flags`, and the plain forms it must leave alone.
FORMS = [
    ("fr-inflated-stakes", "Former nos équipes à l\u2019ère de l\u2019IA reste un défi."),
    ("fr-inflated-stakes", "Nous sommes plus motivées que jamais."),
    ("fr-inflated-stakes", "Le vote de mardi fut un moment charnière."),
    ("fr-inflated-stakes", "La coopérative a connu trois moments charnières depuis 1990."),
    ("fr-inflated-stakes", "Ces deux tournants décisifs ont changé le quartier."),
    ("fr-staged-reveal", "C\u2019est là que notre logiciel entre en jeu."),
    ("fr-staged-reveal", "C\u2019est là qu\u2019entre en jeu notre service client."),
    ("fr-staged-reveal", "La question n'est plus de savoir si le télétravail va durer."),
    ("fr-filler-notice", "Rappelons qu\u2019il convient de noter qu\u2019aucun remboursement n'est possible."),
    ("fr-filler-notice", "Il est important de souligner que la salle ferme à 18 h."),
    ("fr-performative-candour", "Pour être tout à fait transparente, le budget est serré."),
    ("fr-performative-candour", "Pour être franc, je n'y crois pas."),
    ("fr-performative-candour", "Soyons franches : le planning ne tient pas."),
    ("fr-performative-candour", "Soyons honnête : personne n'a lu le rapport."),
    ("fr-engagement-lines", "Et vous ?"),
    ("fr-engagement-lines", "Et toi\u202f?"),
    ("fr-engagement-lines", "Et si on arrêtait les réunions du lundi ?"),
    ("fr-calques", "Nous avons adressé l\u2019enjeu du recrutement en mai."),
    ("fr-inflated-stakes", "Seul l\u2019avenir nous le dira."),
    ("fr-staged-reveal", "C\u2019est ici que les choses deviennent intéressantes."),
    ("fr-stock-openers", "Dans un monde en constante évolution, la chorale de Saint-Lô répète le mardi."),
    ("fr-stock-openers", "«\u00a0Dans un monde en perpétuelle mutation, la mutuelle reste fidèle à ses adhérents."),
    ("fr-stock-openers", "**Dans un monde qui évolue à un rythme effréné**, notre cabinet ouvre à Brest."),
    ("fr-stock-openers", "Dans un monde qui bouge à grande vitesse, le marché de Noël garde ses chalets."),
    ("fr-ai-vocabulary", "Ces deux véritables atouts sont nos pierres angulaires."),
    ("fr-ai-vocabulary", "Une maison nichée dans les vignes."),
    ("fr-calques", "Il faut adresser ces enjeux avant l'été."),
    ("fr-calques", "Notre offre délivre plus de valeur."),
    ("fr-article-rituals", "Dans ce guide, je vais vous montrer trois réglages."),
    ("fr-article-rituals", "Vous l\u2019aurez compris, le délai compte."),
    ("fr-false-contrast", "Il ne s\u2019agit pas seulement de vendre, mais d\u2019écouter."),
    ("fr-false-contrast", "Ce n\u2019est pas qu\u2019une affaire de prix\u00a0: c\u2019est une affaire de confiance."),
    ("fr-hedge-stack", "Ces retards sont potentiellement susceptibles d'affecter la marge."),
    ("fr-slogan-mirrors", "Ni file d'attente. Ni rendez-vous. Simplement un café chaud."),
    ("fr-engagement-lines", "Je suis fière d\u2019annoncer mon nouveau poste."),
    ("fr-engagement-lines", "Le lien en premier commentaire."),
    ("fr-hashtag-block", "Merci à tous ! #Équipe #Lyon #Été #Réussite"),
    ("any-closing-summary", "En conclusion, le projet tient ses délais."),
    ("any-closing-summary", "Pour conclure, le budget tient."),
]

LEFT_ALONE = [
    ("fr-hedge-stack", "Le changement pourrait éventuellement décaler la livraison."),
    ("fr-hedge-stack", "On pourra éventuellement en reparler jeudi."),
    ("fr-false-contrast", "Ce n'est pas la bonne salle, c'est la B12."),
    ("fr-false-contrast", "Ce n'est pas qu'il refuse : il attend le devis."),
    ("fr-false-contrast", "La réunion a lieu le 12 mars, et non le 15."),
    ("fr-calques", "Ça fait sens, on valide."),
    ("fr-calques", "Je vous adresse le bon de commande."),
    ("fr-calques", "J'ai adressé le problème à la DSI."),
    ("fr-engagement-lines", "Et vous, merci encore pour hier."),
    ("fr-calques", "Je vous adresse ces deux devis."),
    ("fr-filler-notice", "Son intérêt n\u2019est plus à démontrer."),
    ("fr-false-contrast", "Il ne s\u2019agit pas de fermer l\u2019atelier, mais de le déplacer à Vierzon."),
    ("fr-inflated-stakes", "Une formation à l\u2019ère du numérique, le 12 mars à Caen."),
    ("fr-staged-reveal", "La réponse est simple : on n\u2019a pas le budget."),
    ("fr-filler-notice", "Il est essentiel de noter les heures sur la feuille de présence."),
    ("fr-filler-notice", "Force est de constater que le stock a baissé."),
    ("fr-filler-notice", "Il ressort de cet échange que la date tient."),
    ("fr-stock-openers", "Chers collègues, dans un monde en pleine mutation, vous avez tenu bon."),
    ("fr-stock-openers", "Notre secteur est en constante évolution."),
    ("fr-hashtag-block", "Voir les tickets #42 #43 #44 #45."),
    ("fr-hashtag-block", "Postez-le sur #général ou #annonces."),
    ("fr-staged-reveal", "La vraie question, c'est qui paie le transport."),
    ("fr-slogan-mirrors", "Moins de réunions depuis septembre, et plus de temps pour les clients."),
    ("fr-engagement-lines", "Nous sommes heureux de vous accueillir lundi."),
]


@pytest.mark.parametrize(("sign", "text"), FORMS)
def test_a_weak_french_check_finds_its_forms(catalogue, sign, text):
    pattern = catalogue.signs[sign].pattern
    assert pattern is not None
    assert pattern.search(text), sign


@pytest.mark.parametrize(("sign", "text"), LEFT_ALONE)
def test_a_weak_french_check_leaves_plain_forms_alone(catalogue, sign, text):
    pattern = catalogue.signs[sign].pattern
    assert pattern is not None
    assert not pattern.search(text), sign


def _plain(text: str) -> str:
    """A text as the alphabetical rule reads it: accents and case ignored."""
    decomposed = unicodedata.normalize("NFD", text.lower())
    return "".join(char for char in decomposed if not unicodedata.combining(char))


# A group of plain words, with no regex syntax nested in it: the groups the rule can be checked on mechanically.
_SIMPLE_GROUP = re.compile(r"\(\?:([^()\[\]\\?*+{}^$.]+)\)")


def _french_regexes(catalogue: signs.Catalogue) -> list[tuple[str, str]]:
    found = []
    for sign in catalogue.signs.values():
        if sign.language != "fr" or not sign.pattern:
            continue
        found += [(sign.id, term.term) for term in sign.terms] or [(sign.id, form) for form in sign.forms.values()]
    return found


def test_french_alternations_run_in_alphabetical_order(catalogue):
    # fr.toml's header: our own order is alphabetical, so no source's order, forward or reversed, can come back (#24's
    # review, F12). A group that breaks it for a prefix says so in a comment and would be listed here.
    regexes = _french_regexes(catalogue)
    groups = [(sign, group.split("|")) for sign, regex in regexes for group in _SIMPLE_GROUP.findall(regex)]
    assert len(groups) >= 20  # the parse finds the groups, so the test can fail
    wrong = [(sign, items) for sign, items in groups if [_plain(item) for item in items] != sorted(map(_plain, items))]
    assert wrong == []


def _term_key(term: str) -> str:
    """A term's plain start: its first word or words, up to the first group or class, or a leading group's first
    alternative."""
    term = term.replace("['\u2019]", "'")
    if term.startswith("(?:"):
        return _plain(re.split(r"[|)]", term[3:], maxsplit=1)[0])
    return _plain(re.split(r"[(\[]", term, maxsplit=1)[0])


def test_french_term_lists_run_in_alphabetical_order(catalogue):
    for sign in catalogue.signs.values():
        if sign.language != "fr" or len(sign.terms) < 2:
            continue
        keys = [_term_key(term.term) for term in sign.terms]
        assert keys == sorted(keys), sign.id
