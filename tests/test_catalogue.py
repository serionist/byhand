"""The catalogue: what ships is valid, and each kind of bad sign, source or language is refused with its reason."""

import datetime
import shutil

import pytest

from byhand import render, signs

SOURCES = """
[[source]]
id = "wiki-en"
url = "https://en.wikipedia.org/wiki/Example"
kind = "wiki"
languages = ["en"]
licence = "CC BY-SA 4.0"
due = "daily"
feed = { api = "mediawiki", site = "en.wikipedia.org", title = "Example" }
read_at = { revision = "123", date = 2026-11-07 }

[[source]]
id = "wiki-de"
url = "https://de.wikipedia.org/wiki/Beispiel"
kind = "wiki"
languages = ["de"]
licence = "CC BY-SA 4.0"
due = "weekly"
feed = { api = "mediawiki", site = "de.wikipedia.org", title = "Beispiel" }
read_at = { revision = "456", date = 2026-11-07 }

[[source]]
id = "wiki-zh"
url = "https://zh.wikipedia.org/wiki/Example"
kind = "wiki"
languages = ["zh"]
licence = "CC BY-SA 4.0"
due = "weekly"
feed = { api = "mediawiki", site = "zh.wikipedia.org", title = "Example" }
read_at = { revision = "789", date = 2026-11-07 }

[[source]]
id = "maintainer"
url = "https://github.com/serionist/byhand/issues/4"
kind = "review"
languages = ["hu"]
licence = "MIT"
due = "by-hand"
feed = { api = "none" }
read_at = { date = 2026-11-07 }
"""
SIGN = """
[[sign]]
id = "en-delve"
category = "word"
kinds = ["any"]
models = [{ family = "gpt", from = "4", to = "4.5" }]
what = "Reaches for a grand verb."
instead = "Says what the writer did."
strength = "usual"
terms = [{ term = "delv(?:e|es|ing)", instead = "look at" }]
flags = "Let us delve into the numbers."
passes = "The dog delved no holes; shelves delved nothing."
sources = [{ source = "wiki-en", where = "Language, revision 123", seen = 2026-11-07 }]
"""
STRUCTURE = """
[[sign]]
id = "any-rule-of-three"
category = "structure"
kinds = ["email", "document"]
models = "any"
what = "Lists three things for the rhythm."
instead = "Lists as many as there are."
strength = "weak"
flags = "Fast, simple and reliable."
passes = "It is fast."
sources = [
  { source = "wiki-en", where = "Style", seen = 2026-11-07 },
  { source = "wiki-de", where = "Stil", seen = 2026-11-07 },
]
until = 2030-01-01
"""
CJK = """
[[sign]]
id = "zh-not-but"
category = "phrase"
kinds = ["any"]
models = "any"
what = "Sets up a contrast nobody made."
instead = "States the point."
strength = "usual"
terms = [{ term = "不是.{1,10}而是", instead = "the point itself" }]
flags = "这不是工具而是伙伴。"
passes = "这是工具。"
sources = [{ source = "wiki-zh", where = "Style", seen = 2026-11-07 }]
"""


@pytest.fixture
def root(tmp_path):
    """A valid catalogue: the real languages and families, invented sources and signs."""
    (tmp_path / "signs").mkdir()
    for name in ("languages.toml", "models.toml"):
        shutil.copy(signs.CATALOGUE / name, tmp_path / name)
    (tmp_path / "sources.toml").write_text(SOURCES, encoding="utf-8")
    (tmp_path / "signs" / "en.toml").write_text(SIGN, encoding="utf-8")
    (tmp_path / "signs" / "any.toml").write_text(STRUCTURE, encoding="utf-8")
    (tmp_path / "signs" / "zh.toml").write_text(CJK, encoding="utf-8")
    return tmp_path


def problems_after(root, rel, old, new):
    path = root / rel
    text = path.read_text(encoding="utf-8")
    assert old in text, old
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    return signs.load(root)[1]


def test_what_ships_is_valid():
    catalogue, problems = signs.load()
    assert problems == []
    assert sum(1 for language in catalogue.languages.values() if language.rank) == signs.LANGUAGE_COUNT
    assert {"en", "zh", "de", "fr", "hu", "ko", "ja", "ru", "zh-Hant"} <= catalogue.languages.keys()
    assert catalogue.languages["zh-Hant"].of == "zh"
    assert not catalogue.languages["zh-Hant"].spaces
    assert not catalogue.languages["tts"].spaces
    assert not catalogue.languages["ja"].spaces
    assert catalogue.languages["hu"].spaces
    assert catalogue.languages["hu"].native == "magyar"
    assert {"claude", "gpt", "gemini"} <= catalogue.families.keys()


def test_a_good_catalogue_passes(root):
    catalogue, problems = signs.load(root)
    assert problems == []
    assert catalogue.signs.keys() == {"en-delve", "any-rule-of-three", "zh-not-but"}
    delve = catalogue.signs["en-delve"]
    assert delve.pattern is not None
    assert delve.pattern.search("DELVING deeper")
    assert delve.models[0].family == "gpt"
    assert catalogue.signs["any-rule-of-three"].models == ()
    assert catalogue.signs["any-rule-of-three"].pattern is None


def test_a_term_stands_as_a_word_only_in_a_language_written_with_spaces(root):
    catalogue, _ = signs.load(root)
    delve, cjk = catalogue.signs["en-delve"], catalogue.signs["zh-not-but"]
    assert delve.pattern is not None
    assert not delve.pattern.search("undelvedly")
    assert not delve.pattern.search("undelve")
    assert not delve.pattern.search("delveful")
    assert cjk.pattern is not None
    assert cjk.pattern.search("这不是工具而是伙伴")


def test_an_open_range_has_no_to(root):
    problems_after(root, "signs/en.toml", ', to = "4.5"', "")
    assert signs.load(root)[0].signs["en-delve"].models[0].to is None


def test_a_signs_own_check_wins_over_its_terms(root):
    new = 'strength = "usual"\ncheck = "numbers"'
    assert problems_after(root, "signs/en.toml", 'strength = "usual"', new) == []
    pattern = signs.load(root)[0].signs["en-delve"].pattern
    assert pattern is not None
    assert pattern.pattern == "numbers"


def test_a_check_runs_line_by_line(root):
    new = 'strength = "usual"\ncheck = "^- bold"\n'
    problems_after(root, "signs/en.toml", 'strength = "usual"\n', new)
    problems_after(root, "signs/en.toml", '"Let us delve into the numbers."', '"""Two lines:\n- bold lead-in"""')
    assert signs.load(root)[1] == []


def test_a_check_compares_in_nfc(root):
    decomposed = "fontossa\u0301g"
    new = f'strength = "usual"\ncheck = "{decomposed}"\n'
    problems_after(root, "signs/en.toml", 'strength = "usual"\n', new)
    assert problems_after(root, "signs/en.toml", '"Let us delve into the numbers."', '"Ez fontosság."') == []


def test_a_sign_from_a_source_in_its_base_language_passes(root):
    sign = CJK.replace("zh-not-but", "zh-Hant-not-but")
    (root / "signs" / "zh-Hant.toml").write_text(sign, encoding="utf-8")
    assert signs.load(root)[1] == []


def test_a_model_scoped_range_may_end_in_a_major_below_its_minor(root):
    # `to = "4"` holds the whole 4 series, so it can follow `from = "4.5"`.
    assert problems_after(root, "signs/en.toml", 'from = "4", to = "4.5"', 'from = "4.5", to = "4"') == []


def test_text_compares_in_nfc(root):
    # A Hungarian word in combining accents is the same word as in composed ones.
    decomposed = "kulcsfontosságú"
    sign = SIGN.replace("delv(?:e|es|ing)", "kulcsfontosság\\\\w*").replace(
        "Let us delve into the numbers.", f"Ez {decomposed}."
    )
    sign = sign.replace("The dog delved no holes; shelves delved nothing.", "Ez fontos.")
    (root / "signs" / "en.toml").write_text(sign, encoding="utf-8")
    assert signs.load(root)[1] == []


# Each case: the file, the text replaced in it, its replacement, what the problem says.
BREAKS = [
    ("signs/en.toml", 'id = "en-delve"', 'id = "de-delve"', "an id is en-<slug>"),
    ("signs/en.toml", 'id = "en-delve"', 'id = "en-Delve"', "an id is en-<slug>"),
    ("signs/en.toml", 'category = "word"', 'category = "vibe"', "`category` is 'vibe'"),
    ("signs/en.toml", 'kinds = ["any"]', 'kinds = ["tweet"]', "`kinds` is 'tweet'"),
    ("signs/en.toml", 'kinds = ["any"]', "kinds = []", "`kinds` must list"),
    ("signs/en.toml", 'strength = "usual"', 'strength = "loud"', "`strength` is 'loud'"),
    ("signs/en.toml", 'what = "Reaches for a grand verb."', 'what = "  "', "`what` must be text"),
    ("signs/en.toml", 'instead = "Says what the writer did."\n', "", "`instead` is missing"),
    ("signs/en.toml", 'strength = "usual"', 'strength = "usual"\nuntill = 2030-01-01', "unknown key `untill`"),
    ("signs/en.toml", 'family = "gpt"', 'family = "bard"', "names no family 'bard'"),
    ("signs/en.toml", 'from = "4"', 'from = "four"', "`from` must be a version"),
    ("signs/en.toml", 'to = "4.5"', 'to = "soon"', "`to` must be a version"),
    ("signs/en.toml", 'to = "4.5"', 'to = "3"', "`to` 3 comes before `from` 4"),
    ("signs/en.toml", 'models = [{ family = "gpt", from = "4", to = "4.5" }]', "models = []", "`models` must be"),
    ("signs/en.toml", 'term = "delv(?:e|es|ing)"', 'term = "delv("', "not a regular expression"),
    ("signs/en.toml", 'category = "word"', 'category = "structure"', "only a word or phrase sign holds `terms`"),
    (
        "signs/en.toml",
        'terms = [{ term = "delv(?:e|es|ing)", instead = "look at" }]',
        "terms = []",
        "`terms` must list",
    ),
    ("signs/en.toml", ', instead = "look at" }', " }", "terms: `instead` is missing"),
    ("signs/en.toml", 'flags = "Let us delve into the numbers."', 'flags = "No such word."', "doesn't find `flags`"),
    (
        "signs/en.toml",
        'passes = "The dog delved no holes; shelves delved nothing."',
        'passes = "We delve."',
        "finds `passes`",
    ),
    (
        "signs/en.toml",
        'passes = "The dog delved no holes; shelves delved nothing."',
        'passes = "  "',
        "`passes` must be",
    ),
    ("signs/en.toml", 'source = "wiki-en"', 'source = "nowhere"', "cites no source 'nowhere'"),
    ("signs/en.toml", "seen = 2026-11-07", 'seen = "today"', "`seen` must be a date"),
    (
        "signs/en.toml",
        'sources = [{ source = "wiki-en", where = "Language, revision 123", seen = 2026-11-07 }]',
        "sources = []",
        "must cite at least one",
    ),
    ("signs/en.toml", 'strength = "usual"', 'strength = "usual"\nuntil = 2030-01-01', "retires by its range's `to`"),
    ("signs/en.toml", 'strength = "usual"', 'strength = "usual"\ncheck = 3', "`check` must be text"),
    ("signs/en.toml", 'strength = "usual"', 'strength = "usual"\ncheck = "delv("', "not a regular expression"),
    ("signs/en.toml", "[[sign]]", "[[sign", "not valid TOML"),
    (
        "signs/any.toml",
        'flags = "Fast, simple and reliable."',
        'flags = "It is fast."',
        "`flags` and `passes` must differ",
    ),
    ("signs/any.toml", "until = 2030-01-01", 'until = "later"', "`until` must be a date"),
    (
        "signs/any.toml",
        '  { source = "wiki-de", where = "Stil", seen = 2026-11-07 },\n',
        "",
        "sources in at least two languages",
    ),
    ("sources.toml", 'id = "wiki-de"', 'id = "wiki-en"', "wiki-en: repeated"),
    ("sources.toml", 'kind = "wiki"', 'kind = "blog"', "`kind` is 'blog'"),
    ("sources.toml", 'due = "daily"', 'due = "hourly"', "`due` is 'hourly'"),
    ("sources.toml", 'licence = "CC BY-SA 4.0"', 'licence = ""', "`licence` must be text"),
    ("sources.toml", 'languages = ["en"]', 'languages = ["klingon"]', "the language 'klingon' isn't one"),
    (
        "sources.toml",
        'feed = { api = "mediawiki", site = "en.wikipedia.org", title = "Example" }',
        'feed = "wiki"',
        "`feed` must be a table",
    ),
    (
        "sources.toml",
        'feed = { api = "mediawiki", site = "en.wikipedia.org", title = "Example" }',
        'feed = { api = "rss" }',
        "`feed.api` is 'rss'",
    ),
    ("sources.toml", ', title = "Example" }', " }", "feed: `title` is missing"),
    ("sources.toml", 'read_at = { revision = "123", date = 2026-11-07 }\n', "", "`read_at` is missing"),
    (
        "sources.toml",
        'read_at = { revision = "123", date = 2026-11-07 }',
        'read_at = "yesterday"',
        "`read_at` must be a table",
    ),
    (
        "sources.toml",
        'read_at = { revision = "123", date = 2026-11-07 }',
        "read_at = { date = 2026-11-07 }",
        "needs the `revision` or `commit`",
    ),
    (
        "sources.toml",
        'read_at = { revision = "123", date = 2026-11-07 }',
        'read_at = { revision = "123", date = "today" }',
        "`read_at.date` must be a date",
    ),
    ("models.toml", 'id = "gpt"', 'id = "claude"', "claude: repeated"),
    ("models.toml", 'id = "gpt"', 'id = "G P T"', "an id takes lowercase letters"),
    ("languages.toml", 'code = "de"', 'code = "en"', "en: repeated"),
    ("languages.toml", 'of = "zh"', 'of = "klingon"', "`of` names no language"),
    ("languages.toml", "rank = 1\n", "rank = 200\n", "the ranks must run from 1"),
    ("languages.toml", "rank = 1\n", 'rank = "one"\n', "the ranks must run from 1"),
    ("languages.toml", 'code = "zh-Hant"', 'code = "ja"', "ja: repeated"),
    ("languages.toml", "1325\nspaces = false", '1325\nspaces = "false"', "`spaces` must be true or false"),
    ("languages.toml", 'code = "en"', "code = 3", "`code` must be text"),
    ("languages.toml", "[[language]]", "[[lang]]", "unknown key `lang`"),
    ("sources.toml", "[[source]]", "[[sources]]", "unknown key `sources`"),
    ("sources.toml", 'languages = ["en"]', "languages = []", "`languages` must list"),
    (
        "sources.toml",
        'feed = { api = "mediawiki", site = "en.wikipedia.org", title = "Example" }',
        'feed = { api = ["x"] }',
        "`feed.api` is",
    ),
    ("signs/en.toml", "[[sign]]", "[[signs]]", "unknown key `signs`"),
    ("signs/en.toml", "[[sign]]", "[sign]", "`sign` must be [[sign]]"),
    ("signs/en.toml", 'id = "en-delve"', "id = 3", "`id` must be text"),
    ("signs/en.toml", 'kinds = ["any"]', 'kinds = ["any", "deck"]', "`kinds` is any or a list of kinds"),
    ("signs/en.toml", 'kinds = ["any"]', 'kinds = ["email", "email"]', "`kinds` repeats a kind"),
    (
        "signs/en.toml",
        'models = [{ family = "gpt", from = "4", to = "4.5" }]',
        'models = ["gpt"]',
        "a `models` range must be a table",
    ),
    ("signs/en.toml", 'family = "gpt"', 'family = ["gpt"]', "names no family"),
    ("signs/en.toml", 'from = "4"', "from = 4.10", "`from` must be a version in quotes"),
    (
        "signs/en.toml",
        'terms = [{ term = "delv(?:e|es|ing)", instead = "look at" }]\n',
        "",
        "a word sign needs `terms` or a `check`",
    ),
    (
        "signs/en.toml",
        'terms = [{ term = "delv(?:e|es|ing)", instead = "look at" }]',
        'terms = ["delve"]',
        "every term must be a table",
    ),
    ("signs/en.toml", 'term = "delv(?:e|es|ing)"', "term = 3", "`term` must be text"),
    ("signs/en.toml", 'instead = "look at"', 'instead = ""', "terms: `instead` must be text"),
    ("signs/en.toml", 'category = "word"', 'category = "artefact"', "only a word or phrase sign holds `terms`"),
    (
        "signs/en.toml",
        'sources = [{ source = "wiki-en", where = "Language, revision 123", seen = 2026-11-07 }]',
        'sources = ["wiki-en"]',
        "every entry of `sources` must be a table",
    ),
    ("signs/en.toml", 'where = "Language, revision 123"', 'where = ""', "`where` must be text"),
    ("signs/en.toml", 'source = "wiki-en"', 'source = ["wiki-en"]', "cites no source"),
    ("signs/en.toml", 'source = "wiki-en"', 'source = "wiki-de"', "no source it cites covers en"),
    ("signs/any.toml", 'category = "structure"', 'category = "artefact"', "an artefact sign needs a `check`"),
    ("signs/any.toml", 'category = "structure"', 'category = "layout"', "a layout sign is for deck and sheet"),
    (
        "signs/any.toml",
        'category = "structure"',
        'category = "word"\nterms = [{ term = "x", instead = "y" }]',
        "an any sign writes its `check`",
    ),
    ("signs/any.toml", "until = 2030-01-01", "until = 2030-01-01T10:00:00", "`until` must be a date"),
    ("signs/any.toml", 'category = "structure"', 'category = "structure"\nsince = 2030-01-01', "unknown key `since`"),
    ("signs/en.toml", 'strength = "usual"', "strength = \"usual\"\ncheck = '(?<!x)delve'", "Grep can't run"),
    ("signs/en.toml", 'strength = "usual"', "strength = \"usual\"\ncheck = 'delve(?=s)'", "Grep can't run"),
    ("signs/en.toml", 'strength = "usual"', "strength = \"usual\"\ncheck = '(d)elve\\1'", "Grep can't run"),
    ("signs/en.toml", 'term = "delv(?:e|es|ing)"', "term = '(?<!un)delve'", "Grep can't run"),
]


@pytest.mark.parametrize("case", BREAKS, ids=[f"{n:02d} {case[3]}" for n, case in enumerate(BREAKS)])
def test_a_broken_catalogue_says_why(root, case):
    rel, old, new, expected = case
    problems = problems_after(root, rel, old, new)
    assert any(expected in problem for problem in problems), problems


def test_a_sign_id_used_twice_is_refused(root):
    german = SIGN.replace("en-delve", "de-delve").replace('source = "wiki-en"', 'source = "wiki-de"')
    (root / "signs" / "de.toml").write_text(german, encoding="utf-8")
    assert signs.load(root)[1] == []
    (root / "signs" / "en.toml").write_text(SIGN + SIGN, encoding="utf-8")
    assert any("en-delve: repeated" in problem for problem in signs.load(root)[1])


def test_a_signs_file_named_for_no_language_is_refused(root):
    (root / "signs" / "klingon.toml").write_text("", encoding="utf-8")
    assert "signs/klingon.toml: the file's name is no language" in signs.load(root)[1]


def test_a_catalogue_short_of_a_hundred_languages_is_refused(root):
    path = root / "languages.toml"
    text = path.read_text(encoding="utf-8")
    path.write_text(text[: text.rindex("[[language]]")] + text[text.index("[[variant]]") :], encoding="utf-8")
    assert any("99 languages" in problem for problem in signs.load(root)[1])


def test_a_missing_file_is_a_problem_not_a_crash(root):
    (root / "sources.toml").unlink()
    assert any(problem.startswith("sources.toml: ") for problem in signs.load(root)[1])


def test_a_file_not_in_utf8_is_a_problem_not_a_crash(root):
    (root / "signs" / "hu.toml").write_bytes("# kulcsfontosságú\n".encode("cp1250"))
    assert any(problem == "hu.toml: not UTF-8; save it as UTF-8" for problem in signs.load(root)[1])


def test_a_sign_in_a_language_of_no_catalogue_has_no_edge_to_read(root):
    (root / "signs" / "klingon.toml").write_text(SIGN.replace("en-delve", "klingon-delve"), encoding="utf-8")
    problems = signs.load(root)[1]
    assert "signs/klingon.toml: the file's name is no language" in problems
    assert any("no source it cites covers klingon" in problem for problem in problems)


def test_a_table_where_a_list_of_tables_belongs_is_refused(root):
    (root / "models.toml").write_text('[family]\nid = "x"\n', encoding="utf-8")
    assert "models.toml: `family` must be [[family]], a list of tables" in signs.load(root)[1]


def test_a_row_that_is_no_table_is_refused(root):
    (root / "models.toml").write_text('family = ["x"]\n', encoding="utf-8")
    assert "models.toml: every `family` must be a table" in signs.load(root)[1]


def test_terms_and_until_reach_the_rendered_files(root):
    found, problems = signs.load(root)
    assert problems == []
    files = render.render(found)
    assert sorted(files) == ["en/gpt.signs.md", "zh/any.signs.md"]  # any-rule-of-three has an `until`, so it is retired
    assert "Terms: `delv(?:e|es|ing)`: look at" in files["en/gpt.signs.md"]
    assert found.signs["any-rule-of-three"].until == datetime.date(2030, 1, 1)
    assert found.signs["en-delve"].until is None
