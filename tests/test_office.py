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
    # a progress list's ticks, in each language with a test file (#19)
    "1. ✅ 合同已盖章",
    "- ✅ 会议室已订",
    "- ✅ 合同已盖章\n- ✅ 会议室已订\n- ❌ 发票还没开",
    "1. ✅ Contract signed\n2. ✅ Room booked\n3. ❌ Caterer not confirmed yet",
    "* ✅ Slides sent\n* ❌ Name badges",
    "• ✅ Visa paid\n• ❌ Hotel still open",
    "1) ✅ Invoice paid\n2) ❌ Receipt missing",
    "  - ✅ Tickets booked\n  - ❌ Taxi to the airport",
    "- ✅ Vertrag unterschrieben\n- ✅ Raum gebucht\n- ❌ Catering noch offen",
    "- ✅ Contrat signé\n- ✅ Salle réservée\n- ❌ Traiteur à confirmer",
    "1. ✅ Szerződés aláírva\n2. ✅ Terem lefoglalva\n3. ❌ Az ebéd még nincs megrendelve",
    "- ✅ 会議室予約済み\n- ✅ 資料印刷済み\n- ❌ 名札はまだ",
    "- ✅ 계약서 서명 완료\n- ✅ 회의실 예약 완료\n- ❌ 다과 주문은 아직",
    "1. ✅ Договор подписан\n2. ✅ Переговорка забронирована\n3. ❌ Пропуска ещё не заказаны",
    "10. ✅ Contract signed\n11. ✅ Keys handed over",
    "\u2013 ✅ Raum gebucht\n\u2013 ❌ Catering noch offen",
    # a person bolding the item they ticked, with no label (#34's review, F2)
    "- ✅ **Contract** signed\n- ❌ **Caterer** not confirmed",
    # Markdown link text is no slot (#22's review, F8)
    "Update your details in [your account](https://example.com/account).",
    "[ここに入力した例](https://example.jp/sample)を見てください。",
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
    # a person's newer, shorter or reworked file that names no reader's text, or a text that is no one's writing to
    # rework (#26): only the reader's text or a register word after more or less is a chatbot's, in English too
    "Of course! Here is a more recent version of the deck:",
    "Sure! Here's a shorter version:",
    "Sure! Here's a newer version of the price list:",
    "Certainly! Here is a more up-to-date version of the price list:",
    "Of course! Here's a longer version of the contract, with the annexes:",
    "Absolutely! Here's a more detailed version of the budget:",
    "Sure! Here's a less cluttered version of the slides:",
    "Of course! Here's a more polished version of the deck:",
    "Of course! Here's a more recent draft of the contract:",
    "Sure! Here's a shorter draft of the minutes:",
    "Certainly! Here is a cleaner version of the spreadsheet:",
    "Sure! Here's a revised version of the contract:",
    "Of course! Here's a revised draft of the lease:",
    "Sure! Here's a revised version of her email:",
    "Sure! Here's a shorter version of the email to the landlord:",
    "Of course! Here's a revised version of your contract:",
    "Sure! Here's an updated version of your timesheet:",
    "Sure! Here's your revised invoice:",
    "Of course! Here is your revised offer letter:",
    "Sure! Here's a rewrite of the second paragraph:",
    "Sure! Here's an email you can send to the landlord:",
    "Sure! Here's a short message you can post in the team channel:",
    # the reader's text only as the head noun, a register word only about text (#35's review, F1 and F2)
    "Of course! Here's your revised email signature:",
    "Of course! Here's a revised version of your email policy:",
    "Sure! Here's a revised version of your incident response plan:",
    "Sure! Here's a shorter version of your email list:",
    "Sure! Here's an improved version of your intro deck:",
    "Sure! Here's your revised message template for the helpdesk:",
    "Sure! Here's a more neutral version of the logo:",
    "Of course! Here's a less formal version of the dress code:",
    "Sure! Here's a more professional version of the deck:",
    "Of course! Here's your revised valuation report:",
    "Sure! Here's a revised version of your email to-do list:",
    "Sure! Here's a more neutral version of this banner:",
    "Sure! Here's a revised version of your email marketing plan:",
    "Sure! Here's a shorter version, as requested:",
    # the other openers chatbots use, on a person's own file (#37)
    "Below is the revised quote, as agreed:",
    "Below is a more detailed version of the budget:",
    "Certainly! Below is a revised version of the lease:",
    "Happy to help! Here's a shorter version of the contract:",
    "Sure - here's the agenda for Monday:",
    "Sure thing! Here's the link to the folder:",
    "Sure \u2013 here's your revised invoice:",
    "Sure, below is a more formal version of the dress code:",
    "Below is a friendly message you can share with your team:",
    "Happy to help! Here's a polite reply you can use if a customer asks for a refund:",
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


# What each sign exists to catch: a line per branch of its check, so silence above can't come from a sign that finds
# nothing, or from a branch that stopped finding. A weak sign's term may have a line too (#38).
MACHINE = [
    ("any-assistant-closing-offer", "Would you like me to convert this into a table?"),
    ("any-assistant-closing-offer", "Let me know if you'd like me to adjust the tone."),
    ("any-assistant-closing-offer", "Is there anything else you'd like me to add?"),
    ("any-assistant-closing-offer", "Gibt es noch etwas, bei dem ich helfen kann?"),
    ("any-assistant-closing-offer", "Сообщите мне, если хотите, чтобы я сократил текст."),
    # the English branch fires only on the reader's text, or a register word after more or less (#26)
    ("any-assistant-preamble", "Certainly! Here is a revised draft of your announcement:"),
    ("any-assistant-preamble", "Absolutely! Here's a rewrite of your bio:"),
    ("any-assistant-preamble", "Sure! Here's a more polished version of your email:"),
    ("any-assistant-preamble", "Of course! Here's a revised version of your email:"),
    ("any-assistant-preamble", "Certainly! Here's a polished draft of your cover letter:"),
    ("any-assistant-preamble", "Absolutely! Here's a clearer version of your résumé:"),
    ("any-assistant-preamble", "Certainly! Here is a tightened version of your essay, cut to 500 words:"),
    ("any-assistant-preamble", "Sure! Here's the shorter version of your LinkedIn post:"),
    ("any-assistant-preamble", "Sure! Here's a rewrite of your cover letter that sounds more confident:"),
    ("any-assistant-preamble", "Sure! Here's your rewritten post:"),
    ("any-assistant-preamble", "Of course! Here's your improved LinkedIn post:"),
    ("any-assistant-preamble", "Of course! Here is your polished thank-you email:"),
    ("any-assistant-preamble", "Sure! Here's a more formal version:"),
    ("any-assistant-preamble", "Absolutely! Here's a less formal version:"),
    ("any-assistant-preamble", "Of course! Here's a slightly more casual version:"),
    ("any-assistant-preamble", "Sure! Here's a shorter, more professional version:"),
    ("any-assistant-preamble", "Certainly! Here is a more concise and friendly version:"),
    ("any-assistant-preamble", "Sure! Here's a more polite draft:"),
    ("any-assistant-preamble", "Sure! Here's a friendly message you can post in the team chat:"),
    ("any-assistant-preamble", "Certainly! Here's an edited version of your email:"),
    ("any-assistant-preamble", "Sure! Here's a proofread version of your article:"),
    ("any-assistant-preamble", "Of course! Here's a streamlined version of your personal statement:"),
    ("any-assistant-preamble", "Sure! Here's a professional version of your email to the landlord:"),
    ("any-assistant-preamble", "Certainly! Here's a revised version of the text you provided:"),
    ("any-assistant-preamble", "Sure! Here's your reworked caption, with the hashtags at the end:"),
    ("any-assistant-preamble", "Sure! Here's a revised version of your email so it sounds warmer:"),
    ("any-assistant-preamble", "Sure! Here's a more formal version of the email:"),
    ("any-assistant-preamble", "Sure! Here's a more formal version for your manager:"),
    ("any-assistant-preamble", "Certainly! Here's a revised version of your email incorporating your feedback:"),
    ("any-assistant-preamble", "Sure! Here's an improved version of your cover letter tailored to the role:"),
    ("any-assistant-preamble", "Sure! Here's a revised version of your message without the jargon:"),
    ("any-assistant-preamble", "Sure! Here's a revised version of your email \u2014 more concise and direct:"),
    ("any-assistant-preamble", "Sure! Here's a rephrased version of your intro (shorter and warmer):"),
    ("any-assistant-preamble", "Sure! Here's a revised version of your reply that's more concise:"),
    ("any-assistant-preamble", "Of course! Here's a corrected version of your essay below:"),
    ("any-assistant-preamble", "Sure! Here's your enhanced bio based on your notes:"),
    ("any-assistant-preamble", "Certainly! Here's a revised version of the email you wrote:"),
    ("any-assistant-preamble", "Sure! Here's a more professional version you can send:"),
    ("any-assistant-preamble", "Sure! Here's a more formal version, keeping your main points:"),
    ("any-assistant-preamble", "Sure! Here's a more formal version of it:"),
    ("any-assistant-preamble", "Certainly! Here's a more polite version in a friendly tone:"),
    ("any-assistant-preamble", "Sure! Here's a more conversational version suitable for a client:"),
    ("any-assistant-preamble", "Sure! Here's a more formal version of the paragraph above:"),
    ("any-assistant-preamble", "Sure! Here's a more professional version \u2014 clear, polite and to the point:"),
    ("any-assistant-preamble", "Sure! Here's a more casual version (great for Slack):"),
    ("any-assistant-preamble", "Sure! Here's a more professional version to send to your manager:"),
    ("any-assistant-preamble", "Sure! Here's a more concise version without losing the key points:"),
    ("any-assistant-preamble", "Sure! Here's a more polite version you could use:"),
    ("any-assistant-preamble", "Sure! Here's a more formal version of the above:"),
    ("any-assistant-preamble", "Sure! Here's a revised version of your email - shorter and warmer:"),
    ("any-assistant-preamble", "Sure! Here's a revised version of your email as requested:"),
    ("any-assistant-preamble", "Sure! Here's a polished version of your text while keeping the key points:"),
    ("any-assistant-preamble", "Sure! Here's a shorter version of your email you can send:"),
    ("any-assistant-preamble", "Sure! Here's a revised version of your email aimed at a senior audience:"),
    ("any-assistant-preamble", "Sure! Here's a revised version of your email focusing on clarity:"),
    ("any-assistant-preamble", "Sure! Here's a more concise version focusing on the key points:"),
    ("any-assistant-preamble", "Sure! Here's a more professional version ready to send:"),
    ("any-assistant-preamble", "Sure! Here's a more formal version addressed to the board:"),
    ("any-assistant-preamble", "Sure! Here's a more polite version on the same lines:"),
    ("any-assistant-preamble", "Gerne! Hier ist eine überarbeitete Version Ihres Textes:"),
    ("any-assistant-preamble", "Безусловно! Вот более официальная версия:"),
    ("any-assistant-preamble", "当然可以\uff01以下是润色后的版本\uff1a"),
    ("any-assistant-preamble", "Sure! Here's a professional email you can send to your client:"),
    ("any-assistant-preamble", "Of course! Here is a shorter version of your post:"),
    # the other openers, held to the same rule (#37)
    ("any-assistant-preamble", "Below is a revised version of your email:"),
    ("any-assistant-preamble", "Certainly! Below is a more concise version of your post:"),
    ("any-assistant-preamble", "Happy to help! Here's a rewrite of your bio:"),
    ("any-assistant-preamble", "I'd be happy to help! Here's a more polished version of your email:"),
    ("any-assistant-preamble", "Sure - here's a more polished version of your email:"),
    ("any-assistant-preamble", "Sure \u2014 here's a revised version of your cover letter:"),
    ("any-assistant-preamble", "Sure\u2013here's a less formal version:"),
    ("any-assistant-preamble", "Sure thing! Here's a more formal version:"),
    ("any-assistant-preamble", "Sure, below is your rewritten intro:"),
    # the German branch fires only when the line names the reader's text (#23's review, F2)
    ("any-assistant-preamble", "Natürlich! Hier ist eine kürzere Fassung Ihrer Notiz:"),
    ("any-assistant-preamble", "Конечно! Вот исправленный текст вашего письма:"),
    ("any-assistant-preamble", "当然可以\uff01以下是修改后的版本\uff1a"),
    ("any-didactic-aside", "It's worth noting that results vary."),
    ("any-didactic-aside", "It is crucial to note the deadline."),
    ("any-emoji-markers", "- 🚀 Launch day"),
    ("any-emoji-markers", "## 📊 Results"),
    ("any-emoji-markers", "1. ✨ Faster pages"),
    ("any-emoji-markers", "- ⭐ Top pick"),
    ("any-emoji-markers", "- 💡 Tip: book early"),
    ("any-emoji-markers", "* 🔥 Hot right now"),
    # a tick still counts opening a heading, or leading a bold label (#19)
    ("any-emoji-markers", "## ✅ Done this week"),
    ("any-emoji-markers", "# ❌ Blocked"),
    ("any-emoji-markers", "- ✅ **Faster builds:** they take half the time"),
    ("any-emoji-markers", "1. ❌ **Old flow**: no longer supported"),
    ("any-emoji-markers", "\u2013 ✅ **Speed:** pages load in half the time"),
    ("any-emoji-markers", "\u2013 🚀 Launch day"),
    ("any-emoji-markers", "- ✅ **合同**\uff1a已盖章"),
    ("any-source-gap-disclaimer", "No such figure appears in the provided sources."),
    ("en-ai-vocabulary", "We want to foster collaboration across the teams."),
    ("en-stock-openers", "In today's digital age, firms must adapt."),
]


@pytest.fixture(scope="module")
def every_sign():
    catalogue, problems = signs.load()
    assert problems == []
    return catalogue.signs


@pytest.mark.parametrize(("sign", "text"), MACHINE)
def test_the_signs_still_find_what_they_are_for(every_sign, sign, text):
    pattern = every_sign[sign].pattern
    assert pattern is not None
    assert pattern.search(text), sign


def test_a_bold_list_is_weak_and_the_preamble_reads_mail():
    catalogue, _ = signs.load()
    bold = catalogue.signs["any-bold-lead-in-list"]
    assert bold.strength == "weak"
    assert bold.pattern is not None
    assert bold.pattern.search(OFFICE[-1])  # it fires, and counts only in a cluster
    assert "email" in catalogue.signs["any-assistant-preamble"].kinds
