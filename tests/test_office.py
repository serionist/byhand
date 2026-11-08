"""Plain work mail and messages, invented, against the real catalogue. A strong or usual sign counts alone, so one that
fires on any of these accuses a person of writing like a machine. A weak sign may fire: it counts only in a cluster."""

import pytest

from byhand import signs

OFFICE = [
    # closing and offering, as people do
    "Is there anything else we should know before the audit?",
    "Let me know if you'd like a copy of the minutes.",
    "I hope this helps.",
    "Would you like me to bring the projector, or will Sam?",
    "Would you like me to draft the letter, or shall I leave it with you?",
    "Is there anything else I can get you from the shop?",
    "Let me know if you need anything else before Friday.",
    # opening
    "Of course, here is where it gets harder.",
    "Sure, here's the config I use.",
    "Hi Sam, hope you had a good weekend. Quick one about the March invoice.",
    "Here is what changed in the rota this month.",
    "Certainly not before Tuesday, I'm afraid.",
    # cause and effect
    "Sales fell 8% in the third quarter, reflecting the weaker dollar.",
    "Rain fell all night, contributing to the delays on the A1.",
    "We lost the client in May, which is why the forecast looks thin.",
    # office speech
    "Can we do a deep dive on the Q3 numbers on Friday?",
    "Let's dive in.",
    "Thanks Sam, you played a crucial role in getting the launch out.",
    "The survey gave us valuable insights into why people cancel.",
    "Nurses play a vital role on the ward.",
    "This aligns with what we agreed last week.",
    "We need to leverage the old contract while it lasts.",
    # telling people things
    "It's important to remember your passport.",
    "It is essential to consider fire exits in the design.",
    "Please note the car park closes at 6.",
    "It's important to call them before noon.",
    # caution and sourcing
    "The trial does not by itself prove the drug works.",
    "This distinction matters because the tax rate differs.",
    "According to their website, Anna Lind is the CEO, so I've addressed it to her.",
    "According to the minutes, the supplier missed two deadlines.",
    "No record of it survives in the available sources.",
    # lists and symbols
    "👍 sounds good",
    "🎉 Congrats on the launch, Sam!",
    "- ✓ Book the room",
    "☐ Sign the form",
    "★ Highly recommended",
    "⚠ The car park closes at 6.",
    "- Book the room\n- Order lunch\n- Send the agenda",
    # contrast
    "It's not a bug, it's a feature.",
    "This isn't about money, it's about trust.",
    "Not only was it late but it was wrong.",
    "It's a shame about the rain, isn't it? This is fine.",
    "You're right, I missed the date. I'll resend it today.",
    # plain business
    "The meeting moved to 3pm. Can you still make it?",
    "In conclusion, the Board resolved to adjourn until May.",
    "Today's stand-up is at ten, and the digital team will join.",
    "I'll send the signed copy tomorrow. Thanks for your help.",
    "As of my last check on Tuesday, the shipment was still in Rotterdam.",
    "Our rent went up 12% in June, so we need to talk about the second office.",
    "Can you review the attached draft before the client call?",
    # a plain reply that opens on a yes, in each language the preamble reads
    "Hi Anna,\n\nSure! Here's the link.\n\nTom",
    "Sure! Here are the slides from yesterday.",
    "Of course! Here's the invoice you asked for.",
    "Certainly, here is the file you asked for.",
    "Sure! Here's a draft of the letter.",
    "Natürlich! Hier ist der Link.",
    "Конечно! Вот ссылка.",
    "当然可以\uff01我下午发给你。",  # full-width marks, as Chinese writes them
    # asides people write
    "The audit is worth noting in the minutes.",
    "The credit is important to note on the invoice.",
    # an eager yes handing over what a person has, a colon before the link or the text (round 3 of #15)
    "Sure! Here's the email from the landlord:",
    "Sure! Here's the summary of Monday's call:",
    "Of course! Here's the message I sent her:",
    "Sure! Here's your invoice:",
    "Natürlich! Hier ist der Link:",
    "Конечно! Вот ссылка:",
    "当然可以\uff01链接在这里\uff1a",
    # a person handing over their own draft, version or options (round 4 of #15): only reworked text is a chatbot's
    "Sure! Here's a draft of the agenda for Monday:",
    "Of course! Here's a draft of the minutes:",
    "Absolutely! Here's an updated version of the rota:",
    "Sure! Here's your draft back with my comments:",
    "Sure! Here's a revision of the timeline after today's call:",
    "Natürlich! Hier ist die neue Version der Präsentation:",
    "Gerne! Hier ist der Entwurf vom Vertrag:",
    "Gerne! Hier ist die Versionsnummer:",
    "Конечно! Вот черновик договора:",
    "Конечно! Вот варианты:",
    "Безусловно! Вот мой вариант ответа:",
    "当然可以\uff01这是合同的草稿\uff1a",
    "当然可以\uff01这是最新版本\uff1a",
    "当然可以\uff01这是我的修改意见\uff1a",
    # a bold list a person writes: weak, so it may fire, but it must not count alone
    "- **Mon:** stand-up at ten\n- **Tue:** client call\n- **Wed:** off",
]


@pytest.fixture(scope="module")
def counted_alone():
    catalogue, problems = signs.load()
    assert problems == []
    found = [sign for sign in catalogue.signs.values() if sign.pattern and sign.strength != "weak"]
    assert found
    return found


@pytest.mark.parametrize("text", OFFICE)
def test_no_sign_that_counts_alone_fires_on_plain_office_text(counted_alone, text):
    assert [sign.id for sign in counted_alone if sign.pattern and sign.pattern.search(text)] == []


# What each sign that counts alone exists to catch: a line per branch of its check, so silence above can't come from a
# sign that finds nothing, or from a branch that stopped finding.
MACHINE = [
    ("any-assistant-closing-offer", "Would you like me to convert this into a table?"),
    ("any-assistant-closing-offer", "Let me know if you'd like me to adjust the tone."),
    ("any-assistant-closing-offer", "Is there anything else you'd like me to add?"),
    ("any-assistant-closing-offer", "Gibt es noch etwas, bei dem ich helfen kann?"),
    ("any-assistant-closing-offer", "Сообщите мне, если хотите, чтобы я сократил текст."),
    ("any-assistant-preamble", "Certainly! Here is a revised draft of your announcement:"),
    ("any-assistant-preamble", "Absolutely! Here's a rewrite:"),
    ("any-assistant-preamble", "Sure! Here's a more polished version:"),
    ("any-assistant-preamble", "Gerne! Hier ist eine überarbeitete Version Ihres Textes:"),
    ("any-assistant-preamble", "Безусловно! Вот более официальная версия:"),
    ("any-assistant-preamble", "当然可以\uff01以下是润色后的版本\uff1a"),
    ("any-assistant-preamble", "Sure! Here's a professional email you can send to your client:"),
    ("any-assistant-preamble", "Of course! Here is a shorter version of the post:"),
    # the German branch fires only when the line names the reader's text (#23's review, F2)
    ("any-assistant-preamble", "Natürlich! Hier ist eine kürzere Fassung Ihrer Notiz:"),
    ("any-assistant-preamble", "Конечно! Вот исправленный текст:"),
    ("any-assistant-preamble", "当然可以\uff01以下是修改后的版本\uff1a"),
    ("any-didactic-aside", "It's worth noting that results vary."),
    ("any-didactic-aside", "It is crucial to note the deadline."),
    ("any-emoji-markers", "- 🚀 Launch day"),
    ("any-emoji-markers", "## 📊 Results"),
    ("any-emoji-markers", "1. ✨ Faster pages"),
    ("any-emoji-markers", "- ⭐ Top pick"),
    ("any-source-gap-disclaimer", "No such figure appears in the provided sources."),
    ("en-stock-openers", "In today's digital age, firms must adapt."),
]


@pytest.mark.parametrize(("sign", "text"), MACHINE)
def test_the_signs_still_find_what_they_are_for(counted_alone, sign, text):
    pattern = {found.id: found.pattern for found in counted_alone}[sign]
    assert pattern is not None
    assert pattern.search(text), sign


def test_a_bold_list_is_weak_and_the_preamble_reads_mail():
    catalogue, _ = signs.load()
    bold = catalogue.signs["any-bold-lead-in-list"]
    assert bold.strength == "weak"
    assert bold.pattern is not None
    assert bold.pattern.search(OFFICE[-1])  # it fires, and counts only in a cluster
    assert "email" in catalogue.signs["any-assistant-preamble"].kinds
