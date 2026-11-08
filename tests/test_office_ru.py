"""Plain Russian work text, invented, against the real catalogue. A strong or usual sign counts alone, so one that
fires on any of these accuses a person of writing like a machine. Russian office register (в рамках, является, данный,
в целях, осуществлять) is how many people write mail, minutes, reports and official letters, and the тире and «ёлочки»
are standard punctuation: none of them is a sign. A weak sign may fire: it counts only in a cluster."""

import re

import pytest

from byhand import signs


def _text(*lines: str) -> str:
    """Lines of a text, joined: a newline escape written against a Cyrillic word reads to ruff as a mixed-script
    word."""
    return "\n".join(lines)


DASHES_AND_QUOTES = "Москва — столица. «Сдадим в срок», — сказал прораб. Встреча — в 10:00, отчёт — к пятнице."
TEMPLATE = _text(
    "Шаблон приглашения ниже, вместо [имя] подставьте имя гостя:",
    "",
    "Дорогой [имя], ждём вас на вечере выпускников.",
)
REPORT = _text(
    "Отчёт за октябрь",
    "",
    "Выручка составила 4,2 млн ₽, на 8% больше, чем в сентябре, в основном за счёт двух новых клиентов. "
    "Следует отметить, что дебиторская задолженность выросла до 900 тыс. ₽; работа по должникам ведётся "
    "в рамках утверждённого регламента. Отдел продаж по-прежнему является основным источником заявок.",
)
REPORT_PRICES = (
    "Закупочные цены в октябре выросли на 5%, отражая рост курса. Стоит отметить, что два поставщика уже прислали "
    "новые прайсы. Данный рост мы заложили в бюджет на ноябрь в рамках резерва."
)
# Report paragraphs that once made a weak cluster from everyday phrases (#22's review, F3).
REPORTS = [
    "Стоит отметить, что переход на электронный документооборот занял два месяца, способствуя снижению затрат "
    "на печать. Эксперты отмечают, что такие проекты окупаются за год.",
    "2025 год стал поворотным моментом для компании: мы открыли второй склад. Сейчас отрасль сталкивается "
    "\u0441 серьёзными вызовами из-за роста тарифов. По мнению экспертов, цены стабилизируются к осени.",
    "Стоит отметить, что план продаж выполнен на 104%. Нельзя не упомянуть работу склада, который отгрузил "
    "заказы без задержек. Эксперты отмечают рост спроса в регионе.",
    REPORT_PRICES + " По мнению экспертов, к весне цены выровняются.",
    # round 2 (#22's review, F11)
    "Нельзя не отметить работу отдела логистики: новые маршруты сократили расходы на 9%, способствуя росту "
    "прибыли. Ряд источников в отрасли подтверждает, что это лучший показатель по региону.",
    "Число заказов выросло на 11%, отражая приток новых покупателей. Ряд экспертов считает это началом подъёма "
    "рынка. Нельзя не отметить и работу службы поддержки.",
    "Запуск приложения стал поворотным моментом: продажи через него выросли вдвое, отражая интерес молодых "
    "клиентов. Нельзя не упомянуть команду разработки, которая уложилась в сроки.",
]
OFFICIAL_LETTER = _text(
    "Исх. № 112/4 от 05.11.2026",
    "",
    "Генеральному директору компании «Вектор»",
    "Д. Л. Смирнову",
    "",
    "Уважаемый Дмитрий Львович!",
    "",
    "Согласно пункту 4.2 договора поставки № 17 от 12.03.2026 уведомляем вас, что срок отгрузки переносится "
    "на 25 ноября 2026 года. Данное письмо является неотъемлемой частью договора.",
    "",
    "Приложение: график поставок на 1 л. в 1 экз.",
    "",
    "Коммерческий директор И. П. Орлова",
)
NOTICE = (
    "Настоящим сообщаем, что в целях исполнения требований законодательства в период 10-14 ноября будет осуществляться "
    "плановая проверка пожарной сигнализации. Просим обеспечить доступ в помещения. При возникновении вопросов "
    "обращайтесь к инженеру по охране труда."
)
MINUTES = _text(
    "Протокол планёрки 07.11",
    "Присутствовали: Иванов, Петрова, Ли",
    "1. Релиз переносим на 18.11 — не готов модуль оплаты.",
    "2. Петрова готовит письмо клиентам до 12.11.",
    "3. Было принято решение осуществлять сверку еженедельно.",
)
# Business chat in the words people use there, which the post-and-document signs leave alone.
CHAT = [
    "Кофемашина опять сломалась. Без кофе. Без печенья. Держимся.",
    "Ок, давайте разберёмся завтра на созвоне, кто отвечает за релиз. Если копнуть глубже, там и тесты падают.",
    "Новая сборка адресует главную боль саппорта, дедлайн встретим, если QA не завалит.",
    "Для меня удобство > цена, так что выбираю второй тариф. Надеюсь, это поможет тебе определиться.",
]

OFFICE = [
    # mail, на вы and на ты, with its set openers and closers
    _text(
        "Добрый день, Ольга Викторовна!",
        "",
        "Направляю вам акт сверки за третий квартал. Если есть расхождения, напишите, пожалуйста, до пятницы.",
        "",
        "Хорошей недели,",
        "Анна Сергеевна Ковалёва",
        "главный бухгалтер компании «Север»",
    ),
    _text(
        "Здравствуйте, Игорь!",
        "",
        "Встречу переносим на вторник, 14:00 — директор будет на совещании. Переговорная та же.",
        "",
        "Спасибо!",
    ),
    _text(
        "Коллеги, добрый день.",
        "",
        "Напоминаю: до 20 ноября нужно сдать заявки на отпуск в январе. Форма во вложении.",
    ),
    _text(
        "Уважаемый Пётр Иванович!",
        "",
        "Благодарим за сотрудничество. Счёт № 418 от 3 ноября оплачен, платёжку прилагаем.",
    ),
    "Маш, привет! Скинь, пожалуйста, презентацию к завтрашнему созвону, хочу глянуть цифры.",
    "Дим, клиент опять просит скидку. Я считаю, больше 5% не даём — и так работаем в ноль.",
    "Сообщите мне, если хотите получить полную версию отчёта.",
    "Сообщите, пожалуйста, если хотите перенести встречу на четверг.",
    "Вы абсолютно правы, я перепутал даты. Исправлю сегодня.",
    _text("Мария Андреевна Белова", "Отдел Продаж И Маркетинга", "+7 912 000-00-00"),
    _text("Хорошего дня,", "", "**Мария Андреевна Белова**", "руководитель отдела продаж"),
    _text("## Нижний Новгород Сити Центр", "", "Адрес офиса и как проехать."),
    # official letters and notices, in their fixed wording
    OFFICIAL_LETTER,
    NOTICE,
    "Отвечая на ваш запрос от 28.10.2026 № 55, сообщаем, что запрашиваемые документы будут направлены в ваш адрес "
    "в установленный срок.",
    # colon-ended replies, and a person handing over or returning their own draft
    "Конечно! Вот ссылка на папку:",
    "Да, вот список участников:",
    "Готово, вот что получилось:",
    "Коротко по итогам:",
    "Конечно! Вот исправленный счёт:",
    "Конечно! Вот черновик письма, посмотри, пожалуйста:",
    "Безусловно! Вот обновлённый график дежурств:",
    "Вот мой вариант текста для рассылки, правь смело:",
    "Отправляю договор после моих правок, исправленная версия во вложении.",
    "Конечно! Вот исправленный вариант письма:",
    "Конечно! Вот исправленный вариант договора:",
    "Конечно! Вот исправленная версия презентации:",
    "Конечно! Вот исправленный текст объявления:",
    "Конечно! Вот более свежая версия прайса:",
    "Конечно! Вот более новая версия договора:",
    "Оплатить можно в [вашем личном кабинете](https://example.ru/lk).",
    # a teacher, a developer and a stock-keeper, in words a chatbot also uses
    "Курсовая в целом хорошая, но в предоставленных источниках не указаны страницы. Поправьте до 20 числа.",
    "Скрипт упал во время обновления моей базы данных, перезапущу ночью.",
    "По состоянию на 1 ноября остаток на складе — 120 штук.",
    # chat: Telegram and Slack
    "Ребят, кто сегодня в офисе? Привезли воду, надо помочь занести",
    "@Сергей глянь пр, пожалуйста, там мелочь — поправил опечатку в конфиге",
    "Ок, понял. Сделаю к вечеру 👍",
    "Созвон перенесли на 16:30, ссылка та же",
    _text("✅ Пропуск заказан", "✅ Переговорка свободна"),
    *CHAT,
    # notes, minutes and reports
    MINUTES,
    _text("TODO", "- оплатить аренду", "- отправить акт в «Вектор»", "- забронировать переговорку на среду"),
    _text("Ниже список задач на неделю:", "1. Сверка по «Вектору»", "2. Акт по аренде", "3. Отпуска"),
    REPORT,
    REPORT_PRICES,
    _text("## Итоги квартала", "", "Продажи выросли, расходы на логистику снизились."),
    "**Важно: пропуска теперь только электронные**",
    "## План на 2027 год",
    "## ПРАВА И ОБЯЗАННОСТИ ПОДРЯДЧИКА",
    "**ПОРЯДОК ОПЛАТЫ И ДОСТАВКИ**",
    "### СРОКИ И ПОРЯДОК ПРИЁМКИ",
    _text("Хорошей недели,", "", "**Отдел Продаж И Маркетинга**"),
    "## Поздравляем \u0421 Новым Годом",  # people capitalise the greeting whole (#22's review, F4)
    "## Анна Иванова и Пётр Смирнов",
    # plain Russian punctuation and plain contrasts
    DASHES_AND_QUOTES,
    "Мы не только закрыли долги, но и купили новый сервер.",
    "Это не ошибка: кнопку спрятали специально.",
    "Важно: возьмите паспорт, без него не пустят.",
    "Подводя итог: бюджет согласован, сроки прежние.",
]


@pytest.fixture(scope="module")
def catalogue():
    found, problems = signs.load()
    assert problems == []
    return found


@pytest.fixture(scope="module")
def counted_alone(catalogue):
    found = [sign for sign in catalogue.signs.values() if sign.pattern and sign.strength != "weak"]
    assert any(sign.language == "ru" for sign in found)
    return found


def test_the_lists_hold_enough():
    assert len(OFFICE) >= 40
    assert "—" in DASHES_AND_QUOTES
    assert "«" in DASHES_AND_QUOTES
    assert "»" in DASHES_AND_QUOTES


@pytest.mark.parametrize("text", OFFICE)
def test_no_sign_that_counts_alone_fires_on_plain_russian_work_text(counted_alone, text):
    assert [sign.id for sign in counted_alone if sign.pattern and sign.pattern.search(text)] == []


# What each sign that counts alone exists to catch, inside Russian text: a line per branch of its check, so silence
# above can't come from a sign that finds nothing, or from a branch that stopped finding.
MACHINE = [
    ("ru-title-case-headings", "## Сроки И Бюджет Проекта"),
    ("ru-title-case-headings", "# Права И Обязанности Подрядчика"),
    ("ru-title-case-headings", "### Итоги Года Для Отдела Продаж"),
    ("any-assistant-preamble", "Конечно! Вот исправленный вариант вашего письма:"),
    ("any-assistant-preamble", "Безусловно! Вот более официальная версия:"),
    ("any-assistant-preamble", "Конечно! Вот сокращенная редакция твоего поста:"),
    ("any-assistant-preamble", "Конечно! Вот ваш отредактированный текст:"),
    ("any-assistant-closing-offer", "Сообщите мне, если хотите, чтобы я дополнил таблицу."),
    ("any-assistant-closing-offer", "Сообщите мне, если хотите, чтобы текст был сокращён."),
    ("any-knowledge-cutoff", "Компания, на момент моего обучения, не объявляла слияния."),
    ("any-knowledge-cutoff", "По состоянию на момент последнего обновления моей базы данных офис был в Казани."),
    ("any-knowledge-cutoff", "По состоянию на моё последнее обновление знаний сделка не закрыта."),
    ("any-source-gap-disclaimer", "Сведения про фирму ограничены в предоставленных результатах поиска."),
    (
        "any-source-gap-disclaimer",
        "Данные про её детство скудны в предоставленных источниках, но она, вероятно, росла в Туле.",
    ),
    ("any-unfilled-placeholder", "Спасибо,\n[Ваше имя]"),
    ("any-unfilled-placeholder", "Я пишу по поводу [опишите проблему]."),
    ("any-unfilled-placeholder", "Срок сдачи — [укажите дату]."),
    # a slot left in a person's own template fires on purpose: it is unfilled (#22's review, F8)
    ("any-unfilled-placeholder", TEMPLATE),
    ("any-unfilled-placeholder", "Подробности: [вставьте ссылку]"),
    ("any-unfilled-placeholder", "Срок сдачи — 2026-xx-xx."),
    ("any-emoji-markers", "- 🚀 Запуск в понедельник"),
    ("any-emoji-markers", "## 📊 Цифры месяца"),
    ("any-chatgpt-citation-markup", "Склад открыли в 2019 году. :contentReference[oaicite:0]{index=0}"),
    ("any-chatgpt-citation-markup", "Склад открыли в 2019 году. turn0search3"),
    ("any-chatbot-url-tag", "Подробнее: https://example.ru/guide?utm_source=chatgpt.com"),
    ("any-gemini-citation-markup", "Склад открыли в 2019 году.[cite: 2]"),
    ("any-grok-citation-markup", "Склад открыли в 2019 году. grok_card"),
    ("any-deepseek-citation-markup", "Склад открыли в 2019 году【1†source】."),
    ("any-chat-tool-markup", "Судя по файлу[attached_file:1], план выполнен."),
]


@pytest.mark.parametrize(("sign", "text"), MACHINE)
def test_the_signs_still_find_what_they_are_for_in_russian(counted_alone, sign, text):
    pattern = {found.id: found.pattern for found in counted_alone}[sign]
    assert pattern is not None
    assert pattern.search(text), sign


# What the weak checks are for, a line each, so a check that stops finding is caught.
WEAK_MACHINE = [
    ("ru-chopped-fragments", "Новая касса. Без очередей. Без чеков."),
    ("ru-chopped-fragments", "Ни одной ошибки. Никаких жалоб."),
    ("ru-math-signs", "Опыт = деньги, и скорость > качество."),
    ("ru-math-signs", "Москва vs Питер: где дешевле офис."),
    ("ru-significance-phrases", "Переезд стал поворотным этапом и символизирует новый курс."),
    ("ru-significance-phrases", "Старая проходная служит напоминанием для ветеранов завода."),
    ("ru-tacked-on-participles", "Продажи выросли, демонстрируя силу бренда."),
    ("ru-calques", "Обновление адресует эту проблему."),
    ("ru-chat-residue", "Надеюсь, мой ответ был полезен."),
]


@pytest.mark.parametrize(("sign", "text"), WEAK_MACHINE)
def test_the_weak_signs_find_what_they_are_for(catalogue, sign, text):
    found = catalogue.signs[sign]
    assert found.strength == "weak"
    assert found.pattern is not None
    assert found.pattern.search(text), sign


# Terms are stems: each must still find its case and verb forms behind the word edge `render` gives it.
FORMS = [
    ("ru-significance-phrases", "Это был поворотный момент."),
    ("ru-significance-phrases", "Решение знаменовало конец эпохи."),
    ("ru-significance-phrases", "Башня являлась символом города."),
    ("ru-significance-phrases", "Он оставил неизгладимый след в истории цеха."),
    ("ru-tacked-on-participles", "Цены выросли, подчеркивая дефицит."),
    ("ru-didactic-phrases", "Крайне важно подчеркнуть, что сроки прежние."),
    ("ru-didactic-phrases", "Стоит обратить внимание на то, что склад закрыт."),
    ("ru-vague-authority", "Исследователи утверждают обратное."),
    ("ru-challenges-formula", "Компания столкнулась \u0441 целым рядом вызовов."),
    ("ru-challenges-formula", "Будущее выглядит многообещающе."),
    ("ru-significance-phrases", "Это символизировало перемены."),
    ("ru-challenges-formula", "Магазин продолжал процветать."),
    ("ru-throat-clearing", "Давайте разберемся, кто платит за тариф."),
    ("ru-throat-clearing", "Вот в чем фокус."),
    ("ru-calques", "Мы адресовали главную боль клиентов."),
    ("ru-calques", "Команда доставляет ценность каждую неделю."),
    ("ru-calques", "Мы встретили дедлайн."),
    ("ru-promotional-words", "Город богат историческим наследием."),
    ("ru-promotional-words", "Музеи могут похвастаться коллекцией."),
    ("ru-chat-residue", "Буду рада помочь!"),
    ("ru-chat-residue", "Если вы хотите узнать что-нибудь еще, пишите."),
]


@pytest.mark.parametrize(("sign", "text"), FORMS)
def test_each_term_finds_its_forms(catalogue, sign, text):
    found = catalogue.signs[sign]
    assert found.pattern is not None
    assert found.pattern.search(text), sign


# Plain Russian that a term's stem would reach if it were wider (#22's review, F5 and F6).
PLAIN = [
    ("ru-calques", "Предлагаю адресовать этот вопрос юристам."),
    ("ru-calques", "Договор на доставку ценностей продлили до марта."),
    ("ru-promotional-words", "Наш офис пока не может похвастаться парковкой."),
    ("ru-didactic-phrases", "Важно отметить: оплата до пятницы."),
    ("ru-vague-authority", "Эксперты отмечают рост спроса."),
    ("ru-vague-authority", "По мнению экспертов, цены стабилизируются."),
    ("ru-didactic-phrases", "Стоит отметить, что план выполнен."),
    ("ru-challenges-formula", "Отрасль сталкивается \u0441 серьёзными вызовами."),
    ("ru-didactic-phrases", "Нельзя не отметить работу склада."),
    ("ru-vague-authority", "Ряд экспертов считает иначе."),
]


@pytest.mark.parametrize(("sign", "text"), PLAIN)
def test_the_terms_leave_plain_russian_alone(catalogue, sign, text):
    found = catalogue.signs[sign]
    assert found.pattern is not None
    assert not found.pattern.search(text), sign


def _reads(sign: signs.Sign, kind: str) -> bool:
    """A sign a Russian draft of this kind loads: the `any` signs and Russian's, never another language's."""
    return sign.language in ("any", "ru") and bool({"any", kind} & set(sign.kinds))


def _weak_hits(catalogue: signs.Catalogue, text: str, kind: str) -> int:
    """Hits of the weak signs a kind of writing reads, as the cluster rule counts them: each a different word or phrase.
    A term is one phrase however its endings vary, and a check one habit however often it fires; one phrase two signs
    find counts once."""
    counted: set[str] = set()
    spans: list[tuple[int, int]] = []
    for sign in catalogue.signs.values():
        if not sign.pattern or sign.strength != "weak" or not _reads(sign, kind):
            continue
        phrases = [
            (term.term, re.compile(rf"\b(?:{term.term})\b", re.IGNORECASE | re.MULTILINE)) for term in sign.terms
        ]
        for phrase, pattern in phrases or [(sign.id, sign.pattern)]:
            for found in pattern.finditer(text):
                if phrase not in counted and any(found.start() < end and start < found.end() for start, end in spans):
                    continue
                counted.add(phrase)
                spans.append(found.span())
    return len(counted)


WEAK_CASES = [
    (REPORT, "document"),
    *((report, "document") for report in REPORTS),
    (REPORT_PRICES, "document"),
    (OFFICIAL_LETTER, "document"),
    (OFFICIAL_LETTER, "email"),
    (NOTICE, "document"),
    (NOTICE, "email"),
    (MINUTES, "document"),
    (DASHES_AND_QUOTES, "post"),
    *((line, "message") for line in CHAT),
]


@pytest.mark.parametrize(("text", "kind"), WEAK_CASES)
def test_plain_mail_reports_and_letters_are_no_weak_cluster(catalogue, text, kind):
    assert _weak_hits(catalogue, text, kind) < signs.WEAK_CLUSTER


@pytest.mark.parametrize("text", CHAT)
def test_no_weak_sign_that_reads_chat_fires_on_business_chat(catalogue, text):
    fired = [
        sign.id
        for sign in catalogue.signs.values()
        if sign.pattern and sign.strength == "weak" and _reads(sign, "message") and sign.pattern.search(text)
    ]
    assert fired == []


def test_no_sign_reads_the_dash_or_the_quotes(catalogue):
    # the тире and «ёлочки» are Russian punctuation: not even a weak sign may count them
    for kind in signs.KINDS:
        assert _weak_hits(catalogue, DASHES_AND_QUOTES, kind) == 0, kind


def test_office_register_is_for_the_models_read_of_posts_and_documents(catalogue):
    # people write it in mail, minutes, reports and letters: no script counts it, and mail and chat don't read it
    register = catalogue.signs["ru-office-register"]
    assert register.pattern is None
    assert register.strength == "weak"
    assert set(register.kinds) == {"post", "document"}


def test_the_chat_words_are_read_in_posts_and_documents_only(catalogue):
    for sign in ("ru-chopped-fragments", "ru-math-signs", "ru-throat-clearing", "ru-calques", "ru-chat-residue"):
        assert set(catalogue.signs[sign].kinds) == {"post", "document"}, sign
