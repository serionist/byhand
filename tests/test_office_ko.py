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


@pytest.fixture(scope="module")
def catalogue():
    found, problems = signs.load()
    assert problems == []
    return found


@pytest.fixture(scope="module")
def counted_alone(catalogue):
    found = [sign for sign in catalogue.signs.values() if sign.pattern and sign.strength != "weak"]
    assert found
    return found


@pytest.mark.parametrize("text", OFFICE)
def test_no_sign_that_counts_alone_fires_on_plain_korean_work_text(counted_alone, text):
    assert [sign.id for sign in counted_alone if sign.pattern and sign.pattern.search(text)] == []


@pytest.mark.parametrize("text", OFFICE)
def test_plain_korean_work_text_makes_no_weak_cluster(catalogue, text):
    weak = [sign for sign in catalogue.signs.values() if sign.pattern and sign.strength == "weak"]
    for paragraph in text.split("\n\n"):
        hits = [sign.id for sign in weak if sign.pattern and sign.pattern.search(paragraph)]
        assert len(hits) < signs.WEAK_CLUSTER, hits


# What each Korean sign that counts alone exists to catch: a line per branch of its check, so the silence above can't
# come from a sign that finds nothing.
MACHINE = [
    ("ko-beyond-mere", "이번 행사는 단순한 친목 모임을 넘어 협업의 출발점이 됩니다."),
    ("ko-beyond-mere", "고객 응대는 단순한 업무를 넘어서 브랜드 경험이 되었다."),
    ("ko-beyond-mere", "이번 투자는 단순한 지원을 넘어선 약속입니다."),
    ("ko-beyond-mere", "단순한 기록을 넘어, 팀의 기억을 남기는 일입니다."),
]


@pytest.mark.parametrize(("sign", "text"), MACHINE)
def test_the_korean_signs_still_find_what_they_are_for(counted_alone, sign, text):
    pattern = {found.id: found.pattern for found in counted_alone}[sign]
    assert pattern is not None
    assert pattern.search(text), sign


def test_every_korean_sign_that_counts_alone_has_its_machine_lines(counted_alone):
    assert {sign.id for sign in counted_alone if sign.language == "ko"} == {sign for sign, _ in MACHINE}
