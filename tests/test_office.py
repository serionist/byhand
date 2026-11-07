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


def test_the_signs_still_find_what_they_are_for(counted_alone):
    # The same signs, on what they exist to catch: silence above must not come from signs that find nothing.
    machine = {
        "any-assistant-closing-offer": "Would you like me to convert this into a table?",
        "any-assistant-preamble": "Certainly! Here is your announcement:",
        "any-didactic-aside": "It's worth noting that results vary.",
        "any-emoji-markers": "- 🚀 Launch day",
        "any-source-gap-disclaimer": "No such figure appears in the provided sources.",
        "en-stock-openers": "In today's digital age, firms must adapt.",
    }
    by_id = {sign.id: sign for sign in counted_alone}
    for sign, text in machine.items():
        pattern = by_id[sign].pattern
        assert pattern is not None
        assert pattern.search(text), sign
