"""Plain Chinese work writing, invented, against the real catalogue: mail, WeChat and DingTalk messages, notes, replies
that end on a colon, and people handing over their own drafts. A strong or usual sign counts alone, so one that fires on
any of these accuses a person of writing like a machine. A weak sign may fire: it counts only in a cluster.

Full-width marks are written as escapes, as ruff refuses them in a string: \\uff0c is the comma, \\u3002 the full stop,
\\uff01 the exclamation mark, \\uff1f the question mark, \\uff1a the colon, \\u3001 the enumeration comma.
"""

import re

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
    # a person returning their own revision, which only 以下是 turns into a chatbot's line (review of #16, F1)
    "当然可以\uff01这是修改后的版本\uff1a",
    "当然可以\uff01附件是修改后的版本\uff1a",
    "當然可以\uff01這是修改後的版本\uff1a",
    "当然可以\uff01优化后的版本见附件\uff1a",
    "当然可以\uff01按您的意见改好了\uff0c修改后的文本如下\uff1a",
    # 接住 with a thing, not a person, as its object (F3)
    "服务器稳稳接住大家的访问\u3002",
    "系统稳稳接住这份流量\u3002",
    "门将稳稳接住你的传球\u3002",
    # a product or a team speaking as an AI assistant, not a model about itself (F4)
    "作为AI助手\uff0c我们的产品能自动排会\u3002",
    "作為AI助理\uff0c我們的系統會先整理紀要\u3002",
    "作为AI助手\uff0c我司产品可以自动整理会议纪要\u3002",
    "作為AI助理\uff0c我方系統支援繁體中文\u3002",
    "作为AI助手\uff0c我公司推出的产品可以自动排班\u3002",
    # reports and news that point at a fact, as people write them (round 3 of the review of #16, N1)
    "值得注意的是\uff0c三季度应收账款比上月多了一百万\uff0c两家大客户还没回款\u3002",
    "需要指出的是\uff0c本次调查样本只有二十人\u3002",
    "作为AI助手\uff0c我行推出的智能客服全天在线\u3002",
    "作为AI助手\uff0c我校的选课系统能自动排课\u3002",
    "作为新人\uff0c我可以先从整理文档做起\u3002",
    "作为AI助手的产品经理\uff0c我会先看用户反馈\u3002",
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


@pytest.mark.parametrize("text", OFFICE)
def test_no_sign_that_counts_alone_fires_on_plain_chinese_office_text(counted_alone, text):
    assert [sign.id for sign in counted_alone if sign.pattern and sign.pattern.search(text)] == []


# What each sign that counts alone exists to catch in Chinese: a line per branch of its check, so silence above can't
# come from a sign that finds nothing, or from a branch that stopped finding.
MACHINE = [
    ("any-assistant-preamble", "当然可以\uff01以下是修改后的版本\uff1a"),
    # weak, so it counts only in a cluster; one form reads both scripts
    ("any-flattering-agreement", "这是很好的观察\uff0c我们先看数据。"),
    ("any-flattering-agreement", "這是很好的觀察\uff0c我們先看數據。"),
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


MACHINE += [  # round 4 of the review of #16: a model's own disclaimers
    ("any-ai-self-reference", "作为一个AI语言模型\uff0c我不具备个人情感\u3002"),
    ("any-ai-self-reference", "作为AI语言模型\uff0c我的知识截止到2023年\u3002"),
    ("any-ai-self-reference", "作为一个AI语言模型\uff0c我并没有自己的立场\u3002"),
    ("any-ai-self-reference", "作为一个AI语言模型\uff0c我只能提供一般性信息\u3002"),
    ("any-ai-self-reference", "作为AI助手\uff0c我建议您咨询专业律师\u3002"),
    ("any-ai-self-reference", "作为AI助手\uff0c我需要提醒您注意风险\u3002"),
    ("any-ai-self-reference", "作为AI助手\uff0c我很乐意帮您修改\u3002"),
    ("any-ai-self-reference", "作为人工智能助手\uff0c我理解您的担忧\u3002"),
]
MACHINE += [  # round 2 of the review of #16
    ("zh-holding-space", "我会一直在这里\uff0c稳稳接住你的情绪\u3002"),
    ("any-assistant-preamble", "当然可以\uff01下面是根据您的要求修改后的版本\uff1a"),
    ("any-assistant-preamble", "当然\uff01以下是优化后的文本\uff1a"),
]


@pytest.mark.parametrize(("sign", "text"), MACHINE)
def test_the_signs_still_find_what_they_are_for(catalogue, read_in, sign, text):
    # as a Chinese check runs it: the forms under zh and any, never another language's
    pattern = read_in(catalogue.signs[sign], "zh")
    assert pattern is not None
    assert pattern.search(text), sign


def test_every_chinese_form_of_a_shared_sign_has_a_machine_line(unproven):
    assert unproven(MACHINE, "zh") == []


def test_chinese_word_signs_are_weak():
    """Chinese office writing shares these phrases: a Chinese word list counts only in a cluster."""
    catalogue, _ = signs.load()
    lists = [sign for sign in catalogue.signs.values() if sign.language in ("zh", "zh-Hant") and sign.terms]
    assert lists
    assert {sign.strength for sign in lists} == {"weak"}


# Plain official notices, invented, in the fixed wording people use for them: 按照规定, 进行审核, 予以, 相关部门,
# 起到\u2026\u2026作用. shuorenhua's rule 21 leaves such wording alone, so the weak signs
# must not make a cluster of it (review of #16, F2).
NOTICES = [
    "关于春节放假的通知\n\n各部门\uff1a按照规定\uff0c春节假期为二月十日至十七日\uff0c共八天\u3002请各部门在放假前对办公区进行安全检查\uff0c关好门窗电源\u3002假期如有急事\uff0c请联系值班人员\u3002\n\n行政部\n二月三日",
    "关于报销材料提交的通知\n\n各位同事\uff1a本月报销材料请于二十五日前交到财务部\uff0c财务部将对单据进行审核\uff0c不符合要求的予以退回\uff0c审核结果对下月付款起到参考作用\u3002如有疑问\uff0c请联系财务部小刘\u3002",
    "停水通知\n\n各位住户\uff1a因管道维修\uff0c本楼将于周六上午九点至下午三点停水\u3002物业已提前通知相关部门\uff0c维修完成后会在群里告知\uff0c请提前储水\u3002",
    "关于消防培训的通知\n\n全体员工\uff1a公司定于本周四下午两点在一楼大厅开展消防培训\uff0c培训对日常防火起到重要作用\uff0c请各部门安排人员准时参加\uff0c无故缺席者由人事部进行处理并予以通报\u3002",
]


def _weak_hits(paragraph: str, weak: list[signs.Sign]) -> int:
    """Hits of weak signs in a paragraph as the rendered files count them, each a different word or phrase: one phrase
    two signs find (overlapping matches) counts once, and so does the same phrase repeated."""
    spans = sorted(
        (match.start(), match.end()) for sign in weak if sign.pattern for match in sign.pattern.finditer(paragraph)
    )
    phrases: list[list[int]] = []
    for start, stop in spans:
        if phrases and start < phrases[-1][1]:
            phrases[-1][1] = max(phrases[-1][1], stop)
        else:
            phrases.append([start, stop])
    return len({paragraph[start:stop].casefold() for start, stop in phrases})


def test_weak_hits_count_as_the_rendered_files_say():
    catalogue, _ = signs.load()
    weak = [sign for sign in catalogue.signs.values() if sign.strength == "weak" and sign.language in ("any", "zh")]
    assert _weak_hits("总的来说还行\u3002总的来说还行\u3002总的来说还行\u3002", weak) == 1
    assert _weak_hits("众所周知\uff0c总的来说\uff0c说到底\u3002", weak) == 3


@pytest.mark.parametrize("notice", NOTICES)
def test_a_plain_official_notice_makes_no_cluster(notice):
    catalogue, _ = signs.load()
    weak = [sign for sign in catalogue.signs.values() if sign.strength == "weak" and sign.language in ("any", "zh")]
    for paragraph in notice.split("\n\n"):
        assert _weak_hits(paragraph, weak) < signs.WEAK_CLUSTER, paragraph


@pytest.mark.parametrize("wording", ["对单据进行审核", "由人事部进行处理", "予以退回", "对付款起到参考作用"])
def test_officialese_leaves_fixed_official_wording(wording):
    catalogue, _ = signs.load()
    pattern = catalogue.signs["zh-officialese"].pattern
    assert pattern is not None
    assert not pattern.search(wording)


def test_the_notices_hold_the_official_wording():
    """Each notice holds wording zh-officialese or slop-gate once found, so the test above has something to hold."""
    official = re.compile(r"[进進]行[审審]核|予以|起到[^\u3002\uff0c\n]{1,10}作用|按照规定|相关部门")
    assert all(official.search(notice) for notice in NOTICES)


# Plain report paragraphs, a year's summary or a look back, in the words people use for them (round 2 of the review
# of #16, F8: 关键在于, 核心在于 and 实现了\u2026\u2026的增长 are how such reports are written).
REPORTS = [
    "今年销售额实现了百分之二十的增长\uff0c主要来自华东区\u3002团队对客户结构进行了全面分析\uff0c发现大客户占比过高\u3002明年的核心在于降低对大客户的依赖\u3002",
    "市场部对投放数据进行了深入分析\u3002总的来说\uff0c短视频的转化不如预期\u3002下季度的关键在于把预算从抖音挪到私域\u3002",
    "复盘\uff1a这次大促备货偏多\uff0c库存周转拉长到四十天\u3002我们对去年的数据进行了系统梳理\uff0c却没算上今年新开的两个渠道\u3002下次备货前先跟渠道负责人对一遍预估\u3002",
    "年度总结\uff1a全年交付项目十二个\uff0c延期三个\u3002总的来说\uff0c人手是最大的瓶颈\u3002本质上是接的单子超出了团队能做的量\uff0c明年先把招聘提上来\u3002",
]


@pytest.mark.parametrize("report", REPORTS)
def test_a_plain_report_paragraph_makes_no_cluster(report):
    catalogue, _ = signs.load()
    weak = [sign for sign in catalogue.signs.values() if sign.strength == "weak" and sign.language in ("any", "zh")]
    assert _weak_hits(report, weak) < signs.WEAK_CLUSTER


@pytest.mark.parametrize(
    "wording", ["实现了百分之二十的增长", "效率实现了明显的提升", "明年的核心在于", "下季度的关键在于"]
)
def test_a_report_s_own_wording_is_no_sign(wording):
    catalogue, _ = signs.load()
    assert [sign.id for sign in catalogue.signs.values() if sign.pattern and sign.pattern.search(wording)] == []


@pytest.mark.parametrize("text", ["值得注意的是\uff0c合同下月到期\u3002", "需要指出的是\uff0c预算还没批\u3002"])
def test_a_signpost_that_people_write_too_is_weak(text):
    """People write these in reports and news, so they count only in a cluster (round 3 of the review of #16, N1)."""
    catalogue, _ = signs.load()
    openers = catalogue.signs["zh-stock-openers"]
    assert openers.strength == "weak"
    assert openers.pattern is not None
    assert openers.pattern.search(text)
