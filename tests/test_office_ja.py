"""Plain Japanese work text, invented, against the real catalogue. A strong or usual sign counts alone, so one that
fires on any of these accuses a person of writing like a machine. Japanese mail opens and closes on set phrases
(お世話になっております, よろしくお願いいたします): they are a person's, never a sign. A weak sign may fire: it counts
only in a cluster.

The full-width exclamation and question marks, colon, brackets, wave dash and ideographic zero are written as escapes,
as ruff refuses them in source; the first test holds that they are the real marks."""

import unicodedata

import pytest

from byhand import signs

COLON_REPLY = "了解です\uff01こちらが議事録の下書きです\uff1a"
SHORT_CHAT = "了解。OK。助かる。"

OFFICE = [
    # mail, with its set openers and closers
    "株式会社みどり商事\n営業部 佐藤様\n\nいつもお世話になっております。\nABC物流の田中です。\n\n"
    "先日ご依頼いただいた見積書を添付いたします。\nご確認のほど、よろしくお願いいたします。",
    "お世話になっております。\n明日の打ち合わせですが、15時からに変更していただくことは可能でしょうか。\n"
    "お手数をおかけしますが、よろしくお願いいたします。",
    "お疲れさまです。経理の中村です。\n10月分の経費精算は、今週金曜日までに提出をお願いします。\n"
    "不明点があれば、遠慮なくお声がけください。",
    "ご質問ありがとうございます。\n納期については、来週火曜日の出荷を予定しております。\n引き続きよろしくお願いいたします。",
    "先日はお忙しいところお時間をいただき、ありがとうございました。\nいただいたご意見をもとに、提案書を修正いたしました。\n"
    "ご査収のほど、よろしくお願い申し上げます。",
    "各位\n\nお疲れさまです。11月のシフト表を共有します。\n変更希望は20日までに、このメールに返信してください。",
    "お世話になっております。\n下記のとおり、会議の日程をご案内いたします。\n\n"
    "日時\uff1a11月12日\uff08水\uff0914時\uff5e15時\n場所\uff1a本社3階 第2会議室\n\n以上、よろしくお願いいたします。",
    "ご返信ありがとうございます。承知しました。\nそれでは、10日の10時にお伺いします。",
    "夜分に失礼いたします。\n明日は体調不良のため、お休みをいただきます。\n急ぎの件は鈴木さんにお願いしてあります。",
    "結論から申し上げますと、今回は見送らせていただきます。\nまたの機会がございましたら、ぜひお声がけください。",
    "ご参考になれば幸いです。\n何卒よろしくお願い申し上げます。",
    "お手すきの際にご確認いただけますと幸いです。",
    "お世話になっております。\n\nご依頼の件、承知いたしました。\n来週中にご提出いたします。\n\n"
    "――――――――――\n株式会社ABC 総務部\n山田 花子\nTEL 03-1234-5678\n――――――――――",
    "取り急ぎ、ご連絡まで。\n詳細は改めてお送りします。",
    # colon-ended replies, and a person handing over their own draft or version
    "お世話になっております。\n資料を拝見しました。2点だけ確認させてください\uff1a\n1. 単価は税込でしょうか。\n"
    "2. 納品場所は本社で問題ないでしょうか。",
    "承知しました\uff01修正版をお送りします\uff1a",
    COLON_REPLY,
    "もちろんです。以下が私の案です\uff1a",
    "お待たせしました\uff01修正した提案書です\uff1a",
    "はい\uff01こちらが短くしたバージョンです\uff1a",
    "かしこまりました。先ほどの企画書、少し短くしたものを添付します。",
    "承知しました。ご指摘の箇所を直した版を、共有ドライブに置きました。",
    "テンプレートを作りました。宛名の部分は各自で書き換えてください\uff1a\n\u3007\u3007様",
    # chat: Slack and Chatwork
    "@山田さん 了解です\uff01明日までに対応します🙏",
    "おつかれさまです。会議室Bって今空いてますか\uff1f",
    "[To:1234567]佐藤さん\nCC 経理チーム\n請求書の件、確認しました。問題ありません。",
    "[info][title]定例会議メモ[/title]次回は来週木曜です。[/info]",
    "すみません、5分ほど遅れます🙇",
    "共有ありがとうございます\uff01確認しておきます。",
    "このPR、レビューお願いできますか\uff1f急ぎではないです。",
    "明日の定例、リモート参加でも大丈夫そうです。",
    SHORT_CHAT,
    "✅ 会議室予約済み\n✅ 資料印刷済み",
    # notes
    "【議事録】11/7 定例\n・参加者\uff1a田中、佐藤、鈴木\n・決定事項\uff1a来月から週次報告をSlackに一本化\n"
    "・宿題\uff1a鈴木さんが手順書を作成\uff0811/14まで\uff09",
    "TODO\n- 見積もり再送\n- 請求書の宛名を確認\n- 来週の出張の新幹線を予約",
    "- **重要**\uff1a締め切りは金曜です",
    "保存する前に **「下書き」** を選んでください。",
    "**注意\uff1a** 金曜は全館停電です。",
    "念のため、先方の担当者名を【要確認】としています。",
    "差出人欄が\uff3b氏名\uff3dのままなので、送る前に直してください。",
    "ポイントは3つあります。価格、納期、保証です。",
    "以上です。よろしくお願いします。",
]


@pytest.fixture(scope="module")
def counted_alone():
    catalogue, problems = signs.load()
    assert problems == []
    found = [sign for sign in catalogue.signs.values() if sign.pattern and sign.strength != "weak"]
    assert any(sign.language == "ja" for sign in found)
    return found


def test_the_marks_are_the_real_ones():
    # an escape that lost its backslash would leave the lines holding ASCII, and the test passing on nothing
    assert unicodedata.name("\uff01") == "FULLWIDTH EXCLAMATION MARK"
    assert unicodedata.name(COLON_REPLY[-1]) == "FULLWIDTH COLON"
    assert sum("\uff1a" in text for text in OFFICE) >= 5
    assert len(OFFICE) >= 30


@pytest.mark.parametrize("text", OFFICE)
def test_no_sign_that_counts_alone_fires_on_plain_japanese_work_text(counted_alone, text):
    assert [sign.id for sign in counted_alone if sign.pattern and sign.pattern.search(text)] == []


# What each sign that counts alone exists to catch, inside Japanese text: a line per branch of its check, so silence
# above can't come from a sign that finds nothing, or from a branch that stopped finding. Branches that only read
# English, German, Russian or Chinese words have their lines in test_office.py.
MACHINE = [
    ("ja-bold-not-rendered", "**「保存」**を押してから閉じてください。"),
    ("ja-bold-not-rendered", "必ず**「保存」**、それから終了。"),
    ("any-unfilled-placeholder", "お世話になっております。\uff3bここに会社名を入れる\uff3dの山田です。"),
    ("any-unfilled-placeholder", "【ここに本文を貼り付け】"),
    ("any-unfilled-placeholder", "お世話になっております。[Your Name]です。"),
    ("any-unfilled-placeholder", "詳細は insert_link_here をご覧ください。"),
    ("any-unfilled-placeholder", "締め切りは2026-xx-xxです。"),
    ("any-emoji-markers", "- 🚀 新機能のお知らせ"),
    ("any-emoji-markers", "## 📊 今月の数字"),
    ("any-emoji-markers", "1. ✨ 表示が速くなりました"),
    ("any-chatgpt-citation-markup", "売上は前年より伸びた。:contentReference[oaicite:0]{index=0}"),
    ("any-chatgpt-citation-markup", "売上は前年より伸びた。oaicite:3"),
    ("any-chatgpt-citation-markup", "売上は前年より伸びた。oai_citation:1"),
    ("any-chatgpt-citation-markup", "売上は前年より伸びた。attributableIndex"),
    ("any-chatgpt-citation-markup", "売上は前年より伸びた。turn0search3"),
    ("any-chatbot-url-tag", "詳しくは https://example.jp/guide?utm_source=chatgpt.com を見てください。"),
    ("any-chatbot-url-tag", "詳しくは https://example.jp/guide?referrer=grok.com を見てください。"),
    ("any-gemini-citation-markup", "導入は2019年です。[span_0](start_span)"),
    ("any-gemini-citation-markup", "導入は2019年です。[cite: 2]"),
    ("any-grok-citation-markup", "導入は2019年です。grok_render_citation_card_json"),
    ("any-grok-citation-markup", "導入は2019年です。grok_card"),
    ("any-grok-citation-markup", "導入は2019年です。<grok-card id=1>"),
    ("any-deepseek-citation-markup", "導入は2019年です【1†source】。"),
    ("any-chat-tool-markup", "添付の資料によると[attached_file:1]、来期は増収です。"),
    ("any-chat-tool-markup", "公式サイトによると[web:2]、来期は増収です。"),
    ("any-chat-tool-markup", "ppl-ai-file-upload の資料を参照。"),
    ("any-chat-tool-markup", ":::writing{variant=standard}"),
]


@pytest.mark.parametrize(("sign", "text"), MACHINE)
def test_the_signs_still_find_what_they_are_for_in_japanese(counted_alone, sign, text):
    pattern = {found.id: found.pattern for found in counted_alone}[sign]
    assert pattern is not None
    assert pattern.search(text), sign


def test_colon_replies_and_short_chat_meet_only_weak_signs():
    catalogue, _ = signs.load()
    for sign, text in (("ja-trailing-colon", COLON_REPLY), ("ja-copy-fragments", SHORT_CHAT)):
        found = catalogue.signs[sign]
        assert found.strength == "weak"
        assert found.pattern is not None
        assert found.pattern.search(text)  # it fires, and counts only in a cluster
    # and a colon before a pasted draft is a person's in mail and chat: the sign reads only posts and documents
    assert set(catalogue.signs["ja-trailing-colon"].kinds) == {"post", "document"}
