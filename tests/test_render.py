"""The plugin's sign files: what goes where, the plain words, the check files, the budgets, and staleness."""

import datetime
import pathlib
import re
import tomllib
import unicodedata

import pytest

from byhand import cli, render, signs
from byhand.models import ModelRange, Version
from byhand.signs import Catalogue, Family, Language, Sign, Term

CLAUDE = Family("claude", "Claude")
GPT = Family("gpt", "GPT")


def sign(sign_id="en-a", language="en", **kept):
    fields = {
        "category": "structure",
        "kinds": ("any",),
        "models": (),
        "what": "Does a thing.",
        "instead": "Says it plainly.",
        "strength": "usual",
        "flags": "x",
        "passes": "y",
        "pattern": None,
    }
    return Sign(sign_id, language, **{**fields, **kept})


def catalogue(*found):
    return Catalogue(
        languages={
            "en": Language("en", "English", rank=1),
            "zh": Language("zh", "Chinese", rank=2, spaces=False),
            "zh-Hant": Language("zh-Hant", "Chinese, Traditional", of="zh", spaces=False),
        },
        families={"claude": CLAUDE, "gpt": GPT},
        signs={item.id: item for item in found},
    )


def lines(text):
    return [line for line in text.splitlines() if line.startswith("- ")]


def test_a_sign_goes_to_its_language_and_family():
    gpt = (ModelRange("gpt", Version(4), Version(4, 5)),)
    files = render.render(
        catalogue(sign("any-a", "any"), sign("en-b"), sign("en-c", models=gpt), sign("zh-d", "zh", models=gpt))
    )
    assert sorted(files) == [
        "any/any.short.md",
        "any/check.md",
        "en/any.short.md",
        "en/check.md",
        "en/gpt.short.md",
        "zh/check.md",
        "zh/gpt.short.md",
    ]
    assert "en-b" not in files["en/gpt.short.md"]
    assert "en-c" not in files["en/any.short.md"]
    assert files["en/gpt.short.md"].startswith("# Signs of AI writing: English, GPT, for every kind of writing\n")
    assert files["any/any.short.md"].startswith("# Signs of AI writing: every language, every model, for every kind")


@pytest.mark.parametrize(
    ("kinds", "part"),
    [
        (("any",), "short"),
        (("email",), "short"),
        (("message", "post"), "short"),  # a mail or a message reads it, so every draft does
        (("document",), "long"),
        (("document", "post"), "long"),
        (("deck",), "layout"),
        (("deck", "sheet"), "layout"),
        (("deck", "document"), "long"),
    ],
)
def test_a_sign_goes_to_short_long_or_layout_by_its_kinds(kinds, part):
    assert render.part(sign(kinds=kinds)) == part
    suffix = {"short": render.SHORT, "long": render.LONG, "layout": render.LAYOUT}[part]
    assert f"en/any{suffix}" in render.render(catalogue(sign(kinds=kinds)))


def test_a_sign_with_ranges_in_two_families_renders_in_both_and_once_in_its_check_file():
    both = (ModelRange("gpt", Version(5)), ModelRange("claude", Version(4), Version(4, 6)))
    files = render.render(catalogue(sign(models=both)))
    assert sorted(files) == ["en/check.md", "en/claude.short.md", "en/gpt.short.md"]
    assert "gpt 5 and later" in files["en/gpt.short.md"]
    assert "claude" not in files["en/gpt.short.md"].split("\n", 3)[3]
    assert "claude 4 to 4.6" in files["en/claude.short.md"]
    assert lines(files["en/check.md"]) == [
        "- en-a (usual; gpt 5 and later; claude 4 to 4.6): Does a thing. Instead: Says it plainly."
    ]


@pytest.mark.parametrize(
    ("span", "printed"),
    [
        (ModelRange("gpt", Version(5)), "gpt 5 and later"),  # a newer model is inside an open range
        (ModelRange("gpt", Version(4), Version(4, 5)), "gpt 4 to 4.5"),  # none past a closed `to`
        (ModelRange("gpt", Version(4), Version(5)), "gpt 4 to 5.x"),  # a `to` with no minor is its whole series
        (ModelRange("gpt", Version(4), Version(5, 0)), "gpt 4 to 5.0"),
    ],
)
def test_a_range_prints_what_the_model_applies(span, printed):
    assert f"(usual; {printed})" in render.render(catalogue(sign(models=(span,))))["en/gpt.short.md"]


def test_a_newer_model_is_held_by_an_open_range_and_not_by_a_closed_one():
    assert ModelRange("gpt", Version(5)).holds(Version(9, 1))
    assert not ModelRange("gpt", Version(4), Version(4, 5)).holds(Version(4, 6))


def test_signs_sort_strongest_first_then_by_id():
    text = render.render(
        catalogue(
            sign("en-b", strength="weak"),
            sign("en-c", strength="strong"),
            sign("en-e", strength="usual"),
            sign("en-d", strength="usual"),
        )
    )["en/any.short.md"]
    assert [line.split()[1] for line in lines(text)] == ["en-c", "en-d", "en-e", "en-b"]


def test_a_line_holds_plain_words_and_no_regex():
    terms = (Term("delv(?:e|es)", "look at"), Term("tapestry", "mix"))
    pattern = re.compile(r"\b(?:delv(?:e|es)|tapestry)\b", re.IGNORECASE)
    files = render.render(
        catalogue(sign(kinds=("email", "post"), terms=terms, pattern=pattern, flags="FLAGS", passes="PASSES"))
    )
    assert lines(files["en/any.short.md"]) == [
        "- en-a (usual; email, post): Does a thing. Instead: Says it plainly. Words: delve: look at; tapestry: mix"
    ]
    assert "FLAGS" not in files["en/any.short.md"]
    assert "(?:" not in files["en/any.short.md"]


def test_a_check_line_adds_the_pattern_grep_runs():
    grep = r"\b(?:delv(?:e|es))\b"
    terms = (Term("delv(?:e|es)", "look at"),)
    files = render.render(catalogue(sign(terms=terms, pattern=signs.as_grep(grep), grep=grep)))
    assert lines(files["en/check.md"]) == [
        r"- en-a (usual): Does a thing. Instead: Says it plainly. Words: delve: look at Pattern: `\b(?:delv(?:e|es))\b`"
    ]
    assert "Grep runs on a file, case-insensitive and line by line" in files["en/check.md"]
    assert "Grep runs" not in files["en/any.short.md"]


@pytest.mark.parametrize(
    ("term", "printed"),
    [
        ("delv(?:e|es|ed|ing)", ["delve"]),
        ("verdeutlichend|widerspiegelnd|betonend", ["verdeutlichend", "widerspiegelnd", "betonend"]),
        (r"mark(?:s|ed|ing)? a (?:pivotal|significant) (?:moment|shift)", ["mark a pivotal shift"]),
        (r"in today['\u2019]?s (?:age|era)", ["in today's age"]),  # an optional apostrophe prints
        (r"\w+ként\s+szolgál\w*", ["\u2026ként szolgál\u2026"]),  # a required run: never a filler letter
        (r"kulcsfontosság\w*", ["kulcsfontosság\u2026"]),  # a stem shows its open end
        ("underscore a|underscore the", ["underscore a", "underscore the"]),  # a shared prefix keeps both
        (r"im (?:digitalen )?zeitalter", ["im zeitalter"]),  # an optional word is not the bare form
        (r"a[^.!?]b", ["a\u2026b"]),  # a negated class never prints a character it excludes
        ("至[关關]重要|[举舉]足[轻輕]重", ["至关重要", "举足轻重"]),
        (r"поворотн\w+ (?:момент|пункт)", ["поворотн\u2026 пункт"]),
    ],
)
def test_a_term_prints_one_plain_word_per_alternative(term, printed):
    assert render.words(term) == printed


def test_every_top_level_alternative_of_the_real_catalogue_has_its_word():
    # Python's parser folds a prefix two alternatives share; split on the term's own text, none is lost.
    found, problems = signs.load()
    assert problems == []
    lost = [
        (term.term, alternative)
        for item in found.signs.values()
        for term in item.terms
        for alternative in render.alternatives(term.term)
        if not any(
            re.fullmatch(alternative, word.replace(render.ELLIPSIS, "x"), re.IGNORECASE)
            for word in render.words(term.term)
        )
    ]
    assert lost == []


def test_alternatives_split_only_at_the_top_level():
    assert render.alternatives(r"a(?:b|c)|[|x]|d\|e") == ["a(?:b|c)", "[|x]", "d\\|e"]


def test_a_term_with_syntax_no_word_can_show_is_refused():
    with pytest.raises(ValueError, match="no word for"):
        render.words(r"(?>atomic)")


def test_every_word_of_the_real_catalogue_matches_its_term():
    found, problems = signs.load()
    assert problems == []
    printed = [
        (term.term, word) for item in found.signs.values() for term in item.terms for word in render.words(term.term)
    ]
    assert len(printed) > 300  # every term of every language, so the test can fail
    wrong = [
        (term, word)
        for term, word in printed
        if not word or not re.search(term, word.replace(render.ELLIPSIS, "x"), re.IGNORECASE)
    ]
    assert wrong == []


def test_every_pattern_prints_as_written_in_nfc():
    # Grep runs the text as written, never Python's reading of it: Grep refuses the look-around `\b` becomes (#13).
    found, problems = signs.load()
    assert problems == []
    printed = {
        match[1]: match[2]
        for text in render.render(found).values()
        for match in re.finditer(r"^- (\S+) .* Pattern: `(.*)`$", text, re.MULTILINE)
    }
    written = {}
    for path in (signs.CATALOGUE / "signs").glob("*.toml"):
        language = found.languages.get(path.stem)
        for row in tomllib.loads(path.read_text(encoding="utf-8"))["sign"]:
            body = "|".join(f"(?:{term['term']})" for term in row.get("terms", ()))
            text = row.get("check") or (rf"\b(?:{body})\b" if language and language.spaces else body)
            if ("check" in row or body) and "until" not in row:
                written[row["id"]] = unicodedata.normalize("NFC", text)
    assert len(printed) > 100
    assert printed == written


def test_no_pattern_breaks_its_code_span_in_a_check_file():
    # A backtick in a pattern would end the span the check file prints it in, and scan would run half of it.
    found, problems = signs.load()
    assert problems == []
    assert [item.id for item in found.signs.values() if "`" in item.grep] == []


def test_the_range_rule_prints_only_where_a_range_is():
    ranged = render.render(catalogue(sign(models=(ModelRange("gpt", Version(5)),))))["en/gpt.short.md"]
    assert "`5.x` is the whole 5 series" in ranged
    assert "5 series" not in render.render(catalogue(sign()))["en/any.short.md"]


def test_a_rendered_file_says_it_is_generated():
    assert "Generated by `byhand render`" in render.render(catalogue(sign()))["en/any.short.md"]


def test_the_cluster_rule_prints_only_where_a_weak_sign_is():
    weak = render.render(catalogue(sign(strength="weak")))["en/any.short.md"]
    assert f"with {signs.WEAK_CLUSTER} or more hits of weak signs in a paragraph or section" in weak
    assert "each a different word or phrase, even two from one sign: the same one repeated, a mark" in weak
    assert "or section" not in render.render(catalogue(sign()))["en/any.short.md"]


def test_a_retired_sign_renders_nowhere_whatever_the_date():
    retired = sign("en-b", until=datetime.date(2999, 1, 1))
    assert list(render.render(catalogue(retired))) == []
    files = render.render(catalogue(retired, sign()))
    assert "en-b" not in files["en/any.short.md"]
    assert "en-b" not in files["en/check.md"]


def test_a_layout_sign_waits_for_decks_and_sheets_outside_the_check_file():
    files = render.render(catalogue(sign(kinds=("deck",)), sign("en-b")))
    assert "en-a" in files["en/any.layout.md"]
    assert "en-a" not in files["en/check.md"]


def test_what_a_draft_reads():
    found = catalogue()
    assert render.draft_files(found, "en", "gpt", "email") == [
        "any/any.short.md",
        "any/gpt.short.md",
        "en/any.short.md",
        "en/gpt.short.md",
    ]
    assert render.draft_files(found, "en", "any", "message") == ["any/any.short.md", "en/any.short.md"]
    assert render.draft_files(found, "en", "any", "document") == [
        "any/any.short.md",
        "en/any.short.md",
        "any/any.long.md",
        "en/any.long.md",
    ]
    assert render.draft_files(found, "en", "any", "deck") == ["any/any.layout.md", "en/any.layout.md"]
    assert render.draft_files(found, "zh-Hant", "claude", "email") == [
        "any/any.short.md",
        "any/claude.short.md",
        "zh/any.short.md",
        "zh/claude.short.md",
        "zh-Hant/any.short.md",
        "zh-Hant/claude.short.md",
    ]


def test_what_a_check_reads():
    found = catalogue()
    assert render.check_files(found, "en") == ["any/check.md", "en/check.md"]
    assert render.check_files(found, "zh-Hant") == ["any/check.md", "zh/check.md", "zh-Hant/check.md"]


def files_of(sizes):
    return {path: "x" * size for path, size in sizes.items()}


def budgets(**kept):
    return render.Budgets(**{"mail": 10**9, "document": 10**9, "layout": 10**9, "check": 10**9, **kept})


def test_a_mail_within_its_budget_passes():
    files = files_of({"any/any.short.md": 40, "en/any.short.md": 30, "en/gpt.short.md": 30})
    assert render.budget_problems(files, catalogue(), budgets(mail=100)) == []


def test_a_mail_over_its_budget_fails_and_a_long_file_is_no_part_of_it():
    files = files_of({"any/any.short.md": 40, "en/any.short.md": 30, "en/gpt.short.md": 31, "en/any.long.md": 500})
    assert render.budget_problems(files, catalogue(), budgets(mail=100)) == [
        "a mail or a message reads 101 bytes, over its 100: any/any.short.md, en/any.short.md, en/gpt.short.md"
    ]


def test_a_document_reads_the_short_and_long_files_together():
    files = files_of({"en/any.short.md": 60, "en/any.long.md": 60})
    assert render.budget_problems(files, catalogue(), budgets(document=100)) == [
        "a post or a document reads 120 bytes, over its 100: en/any.long.md, en/any.short.md"
    ]


def test_a_shared_file_over_budget_is_named_once():
    # Every language and family reads it: the gate shows 40 lines, and 1,111 would hide the cause.
    assert render.budget_problems(files_of({"any/any.short.md": 101}), catalogue(), budgets(mail=100)) == [
        "a mail or a message reads 101 bytes, over its 100: any/any.short.md"
    ]


def test_a_mail_at_its_budget_passes():
    assert render.budget_problems(files_of({"any/any.short.md": 100}), catalogue(), budgets(mail=100)) == []


def test_the_budget_counts_a_variant_with_its_base_language():
    files = files_of({"zh/any.short.md": 60, "zh-Hant/any.short.md": 60})
    assert render.budget_problems(files, catalogue(), budgets(mail=100)) == [
        "a mail or a message reads 120 bytes, over its 100: zh-Hant/any.short.md, zh/any.short.md"
    ]


def test_the_budget_counts_bytes_not_characters():
    assert render.budget_problems({"zh/any.short.md": "字" * 40}, catalogue(), budgets(mail=100))


def test_a_deck_has_a_budget_of_its_own():
    files = files_of({"any/any.layout.md": 60, "en/any.layout.md": 60})
    assert render.budget_problems(files, catalogue(), budgets(layout=100)) == [
        "a deck or a sheet reads 120 bytes, over its 100: any/any.layout.md, en/any.layout.md"
    ]


def test_a_check_reads_its_scopes_check_files_together():
    files = files_of({"any/check.md": 40, "zh/check.md": 40, "zh-Hant/check.md": 40})
    assert render.budget_problems(files, catalogue(), budgets(check=100)) == [
        "a check reads 120 bytes, over its 100: any/check.md, zh-Hant/check.md, zh/check.md"
    ]


def test_a_check_at_its_budget_passes():
    files = files_of({"any/check.md": 50, "en/check.md": 50})
    assert render.budget_problems(files, catalogue(), budgets(check=100)) == []


def test_a_file_of_too_many_lines_fails():
    problems = render.budget_problems({"en/any.short.md": "x\n" * render.MAX_LINES}, catalogue(), budgets())
    size = render.MAX_LINES
    assert problems == [f"en/any.short.md: {size} lines; a file stays under {size}, Claude Code's `Read` default"]


def test_the_budgets_are_the_plans():
    assert render.Budgets(mail=14 * 1024, document=16 * 1024, layout=16 * 1024, check=32 * 1024) == render.BUDGETS


def test_write_then_stale_says_nothing(tmp_path):
    out = tmp_path / "signs"
    files = {"en/any.short.md": "a\n", "any/check.md": "字\n"}
    render.write(files, out)
    assert render.stale(files, out) == []
    assert (out / "en" / "any.short.md").read_bytes() == b"a\n"  # LF on every platform


def test_stale_names_a_changed_a_missing_and_a_left_over_file(tmp_path):
    render.write({"en/any.short.md": "a\n", "de/any.short.md": "b\n", "fr/any.short.md": "c\n"}, tmp_path)
    (tmp_path / "en" / "any.short.md").write_bytes(b"edited by hand\n")
    assert render.stale({"en/any.short.md": "a\n", "hu/any.short.md": "d\n", "fr/any.short.md": "c\n"}, tmp_path) == [
        "de/any.short.md: left over; `byhand render` removes it",
        "en/any.short.md: differs from the catalogue; run `byhand render`",
        "hu/any.short.md: missing; run `byhand render`",
    ]


def test_stale_with_no_folder_and_no_files_says_nothing(tmp_path):
    assert render.stale({}, tmp_path / "none") == []


def test_write_removes_what_the_catalogue_no_longer_holds(tmp_path):
    render.write({"en/any.short.md": "a\n", "de/gpt.short.md": "b\n"}, tmp_path)
    render.write({"en/any.short.md": "a\n"}, tmp_path)
    assert not (tmp_path / "de").exists()
    assert (tmp_path / "en" / "any.short.md").is_file()


def test_the_folder_is_the_repos_wherever_the_command_runs():
    assert pathlib.Path(signs.__file__).resolve().parents[2] / "plugin" / "signs" == render.OUT


def test_the_command_writes_and_checks(tmp_path, monkeypatch, capsys):
    found = catalogue(sign())
    out = tmp_path / "signs"
    monkeypatch.setattr(signs, "load", lambda: (found, []))
    monkeypatch.setattr(render, "OUT", out)
    assert cli.main(["render", "--check"]) == 1
    assert "en/any.short.md: missing" in capsys.readouterr().out
    assert not out.exists()
    assert cli.main(["render"]) == 0
    assert "2 sign files written" in capsys.readouterr().out
    assert cli.main(["render", "--check"]) == 0
    assert "2 sign files match the catalogue" in capsys.readouterr().out


def test_the_command_writes_nothing_from_a_bad_catalogue(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(signs, "load", lambda: (catalogue(sign()), ["a problem"]))
    monkeypatch.setattr(render, "OUT", tmp_path / "signs")
    assert cli.main(["render"]) == 1
    assert "a problem" in capsys.readouterr().out
    assert not (tmp_path / "signs").exists()


def test_the_command_writes_nothing_over_budget(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(signs, "load", lambda: (catalogue(sign(what="x" * 20000)), []))
    monkeypatch.setattr(render, "OUT", tmp_path / "signs")
    assert cli.main(["render"]) == 1
    assert "a mail or a message reads 20188 bytes, over its 14336" in capsys.readouterr().out
    assert not (tmp_path / "signs").exists()


def test_the_real_catalogue_renders_within_its_budgets():
    found, problems = signs.load()
    assert problems == []
    assert render.budget_problems(render.render(found), found) == []


def test_every_sign_file_a_plugin_skill_names_is_one_render_writes():
    # The rendered names changed twice (`.signs.md`, then `.short.md` and `.long.md`): a skill naming an old one would
    # read nothing, and no test of render would see it.
    plugin = pathlib.Path(signs.__file__).resolve().parents[2] / "plugin"
    texts = [
        path.read_text(encoding="utf-8") for path in [*plugin.glob("skills/*/SKILL.md"), *plugin.glob("agents/*.md")]
    ]
    named = [name for text in texts for name in re.findall(r"(?:any|<language>)/[\w<>-]+(?:\.[a-z]+)?\.md", text)]
    assert len(named) >= 5  # the skills name their sign files, so the test can fail
    suffixes = (render.SHORT, render.LONG, render.LAYOUT, "/" + render.CHECK)
    assert [name for name in named if not name.endswith(suffixes)] == []


def test_no_rendered_file_can_be_read_as_a_claude_md():
    # On Windows and macOS `claude.md` is a CLAUDE.md, which Claude Code loads as project instructions.
    claude = (ModelRange("claude", Version(4)),)
    files = render.render(catalogue(sign(models=claude), sign("en-b", kinds=("deck",), models=claude)))
    assert sorted(files) == ["en/check.md", "en/claude.layout.md", "en/claude.short.md"]
    assert not any(path.rsplit("/", 1)[-1].casefold() == "claude.md" for path in files)
