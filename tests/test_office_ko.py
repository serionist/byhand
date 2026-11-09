"""Plain Korean work mail, chat and notes, invented, against the real catalogue. A strong or usual sign counts alone, so
one that fires on any of these accuses a person of writing like a machine. A weak sign may fire, but these must not add
up to a cluster: three hits of weak signs in one paragraph count as one strong sign."""

import pytest

from byhand import signs

OFFICE = [
    # mail, in the polite registers people use at work
    "안녕하세요, 김 과장님.\n\n"
    "내일 회의는 3시가 아니라 4시로 옮겼습니다. 장소는 그대로 2층 회의실입니다.\n\n"
    "감사합니다.\n이수진 드림",
    "요청하신 견적서 보내드립니다. 검토 부탁드립니다.",
    "팀장님, 휴가 신청서 올렸습니다. 확인 부탁드립니다.",
    "서버 점검 때문에 오늘 밤 11시부터 1시간 동안 접속이 안 됩니다. 양해 부탁드립니다.",
    "결론부터 말씀드리면 이번 분기 목표는 달성했습니다. 자세한 수치는 첨부 파일에 있습니다.",
    "작년 대비 매출이 12% 늘었고 신규 고객도 크게 증가했습니다.",
    "이번 일로 고객 신뢰를 잃으면 안 됩니다. 오늘 안에 사과 메일 보내겠습니다.",
    "다들 고생 많으셨습니다. 이번 프로젝트는 여기서 마무리하겠습니다.",
    "늦어질 수도 있을 것 같습니다. 죄송합니다. 내일 오전까지는 꼭 드리겠습니다.",
    "요약하면 다음 주 화요일까지 2차 시안을 보내 주시면 됩니다.",
    # chat: KakaoTalk and Slack
    "넵 확인했습니다! 오늘 중으로 공유드릴게요.",
    "오늘 점심 같이 하실 분? 12시에 1층 로비에서 봬요 ㅎㅎ",
    "자료 잘 받았습니다. 감사합니다!",
    "혹시 내일 오전에 10분만 통화 가능하실까요?",
    "고객사에서 회신이 왔는데 계약서 3조만 다시 보자고 하네요.",
    "이건 제 실수가 아니라 시스템 오류 같아요. 로그 확인해 볼게요.",
    "솔직히 이번 일정은 좀 빠듯해요. 하루만 더 주실 수 있을까요?",
    "회의실 예약은 제가 해 둘게요. 혹시 바뀌면 말씀 주세요.",
    "새 기능이 아직 작동하지 않아요. 확인 부탁드립니다.",
    "입금 확인되었습니다. 감사합니다.",
    "중요한 건 금요일까지 견적서를 보내는 거예요.",
    "그건 단순한 문제가 아니라서 내일 다시 얘기해요.",
    "상태는 '검토 중'으로 바꿔 놨어요.",
    # near the one Korean sign that counts alone: 단순한 and 넘어 apart, or in another sense
    "단순한 오타였어요. 바로 수정해서 다시 올렸습니다.",
    "마감 시간을 넘어서 죄송합니다. 내일 오전까지 꼭 보낼게요.",
    "단순히 날짜만 바꾸면 돼요. 나머지는 그대로 두세요.",
    "단순히 기한을 넘어서 생긴 문제라 큰일은 아니에요.",
    "예산을 넘어서면 다시 결재를 받아야 해요.",
    "단순한 실수니까 그냥 넘어가셔도 됩니다.",
    "단순한 오타라서 예산을 넘어선 건 아니에요.",
    "단순한 실수지만 기한을 넘어서 죄송해요.",
    "단순한 확인 요청이 오후를 넘어서까지 이어졌어요.",
    "단순한 표기 오류를 넘어서는 문제는 없었습니다.",
    "단순한 질문을 넘어서면 별도 견적이 필요합니다.",
    "단순한 오타 수준을 넘어서는 오류는 발견되지 않았다.",
    "단순한 계산을 넘어가는 문제라서 엑셀로는 어려워요.",
    "이번 요청은 단순한 유지보수 범위를 넘어선 작업이라 별도 계약이 필요합니다.",
    "단순한 업무 범위를 넘어 추가 인력이 필요한 상황입니다.",
    "이번 결과가 시사하는 점이 있어서 회의 때 얘기해 봐요.",
    # notes and lists
    "회의 메모: 디자인 시안 B로 결정, 개발은 다음 주 월요일 착수.",
    "회의록 공유드립니다.\n\n1) 다음 주 일정 확정\n2) 예산 재검토\n3) 신규 채용 논의",
    "첫째, 출장비는 영수증이 있어야 하고 둘째, 이번 달 25일까지 올려 주세요.",
    "## 3분기 일정\n- 7월: 기획\n- 8월: 개발\n- 9월: 출시",
    "이 문서에서는 신규 입사자 온보딩 절차를 설명합니다.",
    # replies ending on a colon, before the link, the file or the text
    "자료 첨부합니다:",
    "다음과 같이 변경되었습니다:\n- 회의실: 3층에서 5층\n- 시간: 2시에서 3시",
    "물론이죠! 수정한 파일 여기 있어요:",
    # a person handing over their own draft
    "제가 쓴 초안입니다. 편하게 고쳐 주세요:",
    "네, 제가 다시 정리한 버전입니다:",
    "제가 쓴 공지 초안입니다. 이상한 부분 있으면 알려 주세요:\n\n"
    "다음 주 월요일은 사내 체육대회로 오후 업무가 없습니다.",
]


@pytest.mark.parametrize("text", OFFICE)
def test_no_sign_that_counts_alone_fires_on_plain_korean_work_text(counted_alone, text):
    assert [sign.id for sign in counted_alone if sign.pattern and sign.pattern.search(text)] == []


# A person's 단순한 X를 넘어, in the sense of going past a limit (round 3 of #17). The limit nouns are an open set, so
# ko-beyond-mere is weak: alone, these must not make a cluster.
LIMIT = [
    "단순한 실수의 선을 넘어선 일이라 공식적으로 보고하겠습니다.",
    "단순한 조회 권한을 넘어 수정 권한까지 필요하시면 말씀해 주세요.",
    "단순한 자문 역할을 넘어 실무까지 맡기는 건 계약상 어렵습니다.",
    "단순한 문의 건수를 넘어서 민원으로 번지고 있어요.",
    "단순한 견적 금액을 넘어 세금까지 포함하면 예산이 모자라요.",
    "단순한 사내 공지를 넘어 외부 발표까지 하려면 홍보팀 확인이 필요합니다.",
]


def _weak_hits(catalogue: signs.Catalogue, paragraph: str) -> list[str]:
    weak = [sign for sign in catalogue.signs.values() if sign.pattern and sign.strength == "weak"]
    return [sign.id for sign in weak if sign.pattern and sign.pattern.search(paragraph)]


@pytest.mark.parametrize("text", OFFICE + LIMIT)
def test_plain_korean_work_text_makes_no_weak_cluster(catalogue, text):
    for paragraph in text.split("\n\n"):
        hits = _weak_hits(catalogue, paragraph)
        assert len(hits) < signs.WEAK_CLUSTER, hits


def test_no_korean_check_counts_alone(counted_alone):
    # ko-beyond-mere was the last (round 3 of #17). A Korean sign with a pattern that counts alone needs a MACHINE list
    # here, a line per branch of its check, as tests/test_office.py has for the others.
    assert [sign.id for sign in counted_alone if sign.language == "ko"] == []


# Korean inflects: the forms a weak check must still find, beyond its own `flags`, and what it must leave alone.
FORMS = [
    ("ko-beyond-mere", "이번 행사는 단순한 친목 모임을 넘어 협업의 출발점이 됩니다."),
    ("ko-beyond-mere", "고객 응대는 단순한 업무를 넘어서 브랜드 경험이 되었다."),
    ("ko-beyond-mere", "이번 투자는 단순한 지원을 넘어선 약속입니다."),
    ("ko-beyond-mere", "단순한 기록을 넘어, 팀의 기억을 남기는 일입니다."),
    ("ko-beyond-mere", "이번 프로젝트는 단순한 개편을 넘어"),  # a line ending on 넘어, as Grep reads it
    ("ko-beyond-mere", "이 서비스는 단순한 도구를 넘어서는 가치를 제공합니다."),
    ("ko-beyond-mere", "이 행사는 단순한 제도를 넘어 문화가 되었다."),
    ("ko-wrap-up-words", "합리적인 선택이라고 할 수 있습니다."),
    ("ko-wrap-up-words", "비용이 줄었음을 알 수 있습니다."),
    ("ko-wrap-up-words", "이번 결정은 매우 중요하다고 할 수 있습니다."),
    ("ko-wrap-up-words", "이것이 이번 개편의 핵심이라고 할 수 있을 것입니다."),
    ("ko-slogan-close", "이제 방향을 다시 정할 때다."),
    ("ko-slogan-close", "이는 고객 이탈로 이어질 수 있다."),
    ("ko-slogan-close", "결국 매출 감소로 이어질 것이다."),
    ("ko-enumeration-preamble", "변화는 크게 세 가지로 나누어 볼 수 있다."),
    ("ko-enumeration-preamble", "크게 두 가지로 나눠 설명하겠습니다."),
    ("ko-heading-summary-line", "이번 장에서는 예산을 다룬다."),
    ("ko-heading-summary-line", "이 절에서는 일정을 정리한다."),
    ("ko-double-hedge", "지연될 가능성도 있을 수 있습니다."),
    ("ko-comma-after-ending", "확인했지만, 답이 없었다."),
    ("ko-comma-after-ending", "검토하지만, 결론은 다음 주에 낸다."),
    ("ko-register-shift-vocabulary", "이 보고서는 현장의 변화를 조명한다."),
]

LEFT_ALONE = [
    ("ko-beyond-mere", "단순한 오타라서 예산을 넘어선 건 아니에요."),
    ("ko-beyond-mere", "단순한 질문을 넘어서면 별도 견적이 필요합니다."),
    ("ko-beyond-mere", "단순한 계산을 넘어가는 문제라서 엑셀로는 어려워요."),
    ("ko-comma-after-ending", "하지만, 일정은 그대로예요."),
    ("ko-comma-after-ending", "그렇지만, 비용은 줄었어요."),
    ("ko-comma-after-ending", "그러면서, 다음 회의를 잡았어요."),
]


@pytest.mark.parametrize(("sign", "text"), FORMS)
def test_a_weak_korean_check_finds_its_inflected_forms(catalogue, sign, text):
    pattern = catalogue.signs[sign].pattern
    assert pattern is not None
    assert pattern.search(text), sign


@pytest.mark.parametrize(("sign", "text"), LEFT_ALONE)
def test_a_weak_korean_check_leaves_plain_forms_alone(catalogue, sign, text):
    pattern = catalogue.signs[sign].pattern
    assert pattern is not None
    assert not pattern.search(text), sign
