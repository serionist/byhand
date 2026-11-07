"""Plain Chinese work writing, invented, against the real catalogue: mail, WeChat and DingTalk messages, notes, replies
that end on a colon, and people handing over their own drafts. A strong or usual sign counts alone, so one that fires on
any of these accuses a person of writing like a machine. A weak sign may fire: it counts only in a cluster.

Full-width marks are written as escapes, as ruff refuses them in a string: \\uff0c is the comma, \\u3002 the full stop,
\\uff01 the exclamation mark, \\uff1f the question mark, \\uff1a the colon, \\u3001 the enumeration comma.
"""

import pytest

from byhand import signs

OFFICE = [
    # mail
    "王经理您好\uff0c附件是三月的对账单\uff0c请查收\u3002如有问题请随时联系我\u3002",
    "各位同事\uff1a本周五下午三点在三楼会议室开季度会\uff0c请准时参加\u3002",
    "张老师\uff0c报名表已经填好\uff0c麻烦您签个字\uff0c明天交到教务处\u3002",
    "李总\uff0c合同第五条的付款期限我们希望改成六十天\uff0c您看是否可行\uff1f",
    "随着业务的发展\uff0c我们打算下个月再招两名客服\u3002",
    "需要注意的是\uff0c报销截止到本月二十五号\u3002",
    "总的来说这次活动还不错\uff0c下次早点订场地\u3002",
    "首先\uff0c确认人数\uff1b其次\uff0c订餐\uff1b最后\uff0c发通知\u3002",
    # WeChat and DingTalk
    "收到\uff01我下午发给你\u3002",
    "好的\uff0c明天上午十点见\u3002",
    "当然可以\uff01我晚点发你\u3002",
    "要不要我帮你把会议纪要整理一下\uff1f",
    "如果你愿意\uff0c我可以帮你约一下王总\u3002",
    "这事说句实话我也拿不准\uff0c等老板定吧\u3002",
    "希望对你有帮助\uff0c有问题再找我\u3002",
    "如果你还有其他问题\uff0c直接在群里问就行\u3002",
    "辛苦了\uff01这个版本没问题\uff0c可以发给客户了\u3002",
    "球传过来\uff0c我稳稳接住\u3002",
    "新网关周五晚高峰也稳稳接住了所有请求\u3002",
    "作为AI产品经理\uff0c我想先确认一下需求范围\u3002",
    "作为人工智能专业的学生\uff0c我对这个实习很感兴趣\u3002",
    "作为AI助手\uff0c这款产品能自动排会\u3001记纪要\u3002",
    "这段内容我用工具翻译过\uff0c你再帮我看看\u3002",
    "数据库我已经备份好了\uff0c周日凌晨停机维护\u3002",
    "1. 合同已盖章\n2. 发票已寄出\n3. 尾款下周到账",
    # replies that end on a colon
    "好的\uff0c附件如下\uff1a",
    "收到\uff01文件在这里\uff1a",
    "当然可以\uff01链接如下\uff1a",
    # a person handing over their own draft or revision
    "当然可以\uff01这是修改后的方案\uff1a",
    "当然可以\uff01这是我修改后的版本\uff1a",
    "当然可以\uff01这是更新后的版本\uff1a",
    "当然可以\uff01这是改过的初稿\uff1a",
    "当然可以\uff01这是修改后的稿子\uff1a",
    "當然可以\uff01這是我修改後的版本\uff1a",
    "我把初稿放在共享文件夹了\uff0c你看一下哪里要改\u3002",
    "这是我写的周报初稿\uff0c帮忙看看数字对不对\uff1a",
    # notes
    "周三\uff1a跟供应商对账\u3001催发票\u3001订下周的会议室\u3002",
    "待办\uff1a续签房租合同\uff0c问物业能不能便宜点\u3002",
    "老王说预算批了\uff0c下周一开始招人\u3002",
    # Traditional, as in Taiwan
    "王經理您好\uff0c附件是三月的對帳單\uff0c請查收\u3002",
    "主管說\u300c下週再談\u300d\uff0c所以先別寄報價單\u3002",
]


def test_the_marks_are_real():
    """An escaped backslash would leave `\\uff01` as six characters, and no test could fail on it."""
    assert "\uff01" in OFFICE[8]
    assert "\\" not in "".join(OFFICE)
    assert len("\uff0c") == 1


@pytest.fixture(scope="module")
def counted_alone():
    catalogue, problems = signs.load()
    assert problems == []
    found = [sign for sign in catalogue.signs.values() if sign.pattern and sign.strength != "weak"]
    assert found
    return found


@pytest.mark.parametrize("text", OFFICE)
def test_no_sign_that_counts_alone_fires_on_plain_chinese_office_text(counted_alone, text):
    assert [sign.id for sign in counted_alone if sign.pattern and sign.pattern.search(text)] == []


# What each sign that counts alone exists to catch in Chinese: a line per branch of its check, so silence above can't
# come from a sign that finds nothing, or from a branch that stopped finding.
MACHINE = [
    ("any-assistant-preamble", "当然可以\uff01以下是润色后的版本\uff1a"),
    ("any-assistant-preamble", "当然可以\uff01以下是为你改写后的文本\uff1a"),
    ("any-assistant-preamble", "當然可以\uff01以下是優化後的版本\uff1a"),
    ("any-ai-self-reference", "作为一个AI语言模型\uff0c我无法预测股价\u3002"),
    ("any-ai-self-reference", "作為AI助手\uff0c我沒有個人立場\u3002"),
    ("any-ai-self-reference", "作为一位机器人\uff0c我不能替你做决定\u3002"),
    ("any-ai-self-reference", "\uff08内容由豆包生成\uff09"),
    ("any-ai-self-reference", "\uff08內容由豆包產生\uff09"),
    ("zh-holding-space", "别怕\uff0c我会稳稳接住你\u3002"),
    ("zh-holding-space", "我们会稳稳地接住所有人\u3002"),
    ("zh-holding-space", "讓我穩穩接住這份不安\u3002"),
    ("zh-holding-space", "这里会稳稳接住大家\u3002"),
]


@pytest.mark.parametrize(("sign", "text"), MACHINE)
def test_the_signs_still_find_what_they_are_for(counted_alone, sign, text):
    pattern = {found.id: found.pattern for found in counted_alone}[sign]
    assert pattern is not None
    assert pattern.search(text), sign


def test_chinese_word_signs_are_weak():
    """Chinese office writing shares these phrases: a Chinese word list counts only in a cluster."""
    catalogue, _ = signs.load()
    lists = [sign for sign in catalogue.signs.values() if sign.language in ("zh", "zh-Hant") and sign.terms]
    assert lists
    assert {sign.strength for sign in lists} == {"weak"}
