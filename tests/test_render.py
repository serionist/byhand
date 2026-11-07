"""The plugin's sign files: what goes where, what a draft reads, the budgets, and staleness."""

import datetime
import pathlib

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


def test_a_sign_goes_to_its_language_and_family():
    gpt = (ModelRange("gpt", Version(4), Version(4, 5)),)
    files = render.render(
        catalogue(sign("any-a", "any"), sign("en-b"), sign("en-c", models=gpt), sign("zh-d", "zh", models=gpt))
    )
    assert sorted(files) == ["any/any.signs.md", "en/any.signs.md", "en/gpt.signs.md", "zh/gpt.signs.md"]
    assert "en-b" not in files["en/gpt.signs.md"]
    assert "en-c" not in files["en/any.signs.md"]
    assert files["en/gpt.signs.md"].startswith("# Signs of AI writing: English, GPT\n")
    assert files["any/any.signs.md"].startswith("# Signs of AI writing: every language, every model\n")


def test_a_sign_with_ranges_in_two_families_renders_in_both():
    both = (ModelRange("gpt", Version(5)), ModelRange("claude", Version(4), Version(4, 6)))
    files = render.render(catalogue(sign(models=both)))
    assert sorted(files) == ["en/claude.signs.md", "en/gpt.signs.md"]
    assert "gpt 5 and later" in files["en/gpt.signs.md"]
    assert "claude" not in files["en/gpt.signs.md"].split("\n", 3)[3]
    assert "claude 4 to 4.6" in files["en/claude.signs.md"]


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
    assert f"(usual; {printed})" in render.render(catalogue(sign(models=(span,))))["en/gpt.signs.md"]


def test_a_newer_model_is_held_by_an_open_range_and_not_by_a_closed_one():
    assert ModelRange("gpt", Version(5)).holds(Version(9, 1))
    assert not ModelRange("gpt", Version(4), Version(4, 5)).holds(Version(4, 6))


@pytest.mark.parametrize(
    ("kept", "layout"),
    [
        ({"category": "layout", "kinds": ("deck",)}, True),
        ({"kinds": ("deck", "sheet")}, True),
        ({"kinds": ("sheet",)}, True),
        ({"kinds": ("deck", "email")}, False),
        ({"kinds": ("any",)}, False),
    ],
)
def test_the_layout_signs_of_decks_and_sheets_are_apart(kept, layout):
    files = render.render(catalogue(sign(**kept)))
    assert list(files) == (["en/any.layout.md"] if layout else ["en/any.signs.md"])
    assert files[next(iter(files))].splitlines()[0].endswith("decks and sheets") is layout


def test_signs_sort_strongest_first_then_by_id():
    text = render.render(
        catalogue(
            sign("en-b", strength="weak"),
            sign("en-c", strength="strong"),
            sign("en-e", strength="usual"),
            sign("en-d", strength="usual"),
        )
    )["en/any.signs.md"]
    assert [line.split()[1] for line in text.splitlines() if line.startswith("- ")] == ["en-c", "en-d", "en-e", "en-b"]


def test_a_line_holds_what_the_model_acts_on_and_nothing_else():
    terms = (Term("delv(?:e|es)", "look at"), Term("tapestry", "mix"))
    text = render.render(catalogue(sign(kinds=("email", "post"), terms=terms, flags="FLAGS", passes="PASSES")))
    line = text["en/any.signs.md"].splitlines()[-1]
    assert line == (
        "- en-a (usual; email, post): Does a thing. Instead: Says it plainly. "
        "Terms: `delv(?:e|es)`: look at; `tapestry`: mix"
    )
    assert "FLAGS" not in text["en/any.signs.md"]


def test_the_range_rule_prints_only_where_a_range_is():
    ranged = render.render(catalogue(sign(models=(ModelRange("gpt", Version(5)),))))["en/gpt.signs.md"]
    assert "`5.x` is the whole 5 series" in ranged
    assert "5 series" not in render.render(catalogue(sign()))["en/any.signs.md"]


def test_a_rendered_file_says_it_is_generated():
    assert "Generated by `byhand render`" in render.render(catalogue(sign()))["en/any.signs.md"]


def test_the_cluster_rule_prints_only_where_a_weak_sign_is():
    weak = render.render(catalogue(sign(strength="weak")))["en/any.signs.md"]
    assert f"with {signs.WEAK_CLUSTER} or more hits of weak signs in a paragraph or section" in weak
    assert "or section" not in render.render(catalogue(sign()))["en/any.signs.md"]


def test_a_retired_sign_renders_nowhere_whatever_the_date():
    retired = sign("en-b", until=datetime.date(2999, 1, 1))
    assert list(render.render(catalogue(retired))) == []
    assert "en-b" not in render.render(catalogue(retired, sign()))["en/any.signs.md"]


def test_what_a_draft_reads():
    found = catalogue()
    assert render.draft_files(found, "en", "gpt") == [
        "any/any.signs.md",
        "any/gpt.signs.md",
        "en/any.signs.md",
        "en/gpt.signs.md",
    ]
    assert render.draft_files(found, "en", "any") == ["any/any.signs.md", "en/any.signs.md"]
    assert render.draft_files(found, "zh-Hant", "claude") == [
        "any/any.signs.md",
        "any/claude.signs.md",
        "zh/any.signs.md",
        "zh/claude.signs.md",
        "zh-Hant/any.signs.md",
        "zh-Hant/claude.signs.md",
    ]


def files_of(sizes):
    return {path: "x" * size for path, size in sizes.items()}


def test_a_draft_within_its_budget_passes():
    files = files_of({"any/any.signs.md": 40, "en/any.signs.md": 30, "en/gpt.signs.md": 30})
    assert render.budget_problems(files, catalogue(), draft=100) == []


def test_a_draft_over_its_budget_fails():
    files = files_of({"any/any.signs.md": 40, "en/any.signs.md": 30, "en/gpt.signs.md": 31})
    assert render.budget_problems(files, catalogue(), draft=100) == [
        "a draft reads 101 bytes, over its 100: any/any.signs.md, en/any.signs.md, en/gpt.signs.md"
    ]


def test_a_shared_file_over_budget_is_named_once():
    # Every language and family reads it: the gate shows 40 lines, and 1,111 would hide the cause.
    assert render.budget_problems(files_of({"any/any.signs.md": 101}), catalogue(), draft=100) == [
        "a draft reads 101 bytes, over its 100: any/any.signs.md"
    ]


def test_a_draft_at_its_budget_passes():
    assert render.budget_problems(files_of({"any/any.signs.md": 100}), catalogue(), draft=100, unknown=100) == []


def test_the_budget_counts_a_variant_with_its_base_language():
    files = files_of({"zh/any.signs.md": 60, "zh-Hant/any.signs.md": 60})
    problems = render.budget_problems(files, catalogue(), draft=100)
    assert problems == ["a draft reads 120 bytes, over its 100: zh-Hant/any.signs.md, zh/any.signs.md"]


def test_the_budget_counts_bytes_not_characters():
    assert render.budget_problems({"zh/any.signs.md": "字" * 40}, catalogue(), draft=100)


def test_a_layout_file_counts_in_no_prose_budget():
    assert render.budget_problems(files_of({"en/any.layout.md": 500}), catalogue(), draft=100, unknown=600) == []


def test_a_deck_of_unknown_author_reads_every_family_within_its_budget():
    files = files_of({"en/any.layout.md": 60, "en/gpt.layout.md": 60, "en/claude.layout.md": 60})
    assert render.budget_problems(files, catalogue(), unknown=100) == [
        "a deck of unknown author reads 180 bytes, over its 100: "
        "en/any.layout.md, en/claude.layout.md, en/gpt.layout.md"
    ]


def test_a_deck_has_a_budget_of_its_own():
    files = files_of({"any/any.layout.md": 60, "en/any.layout.md": 60})
    assert render.budget_problems(files, catalogue(), layout=100) == [
        "a deck or a sheet reads 120 bytes, over its 100: any/any.layout.md, en/any.layout.md"
    ]


def test_a_text_of_unknown_author_reads_every_family_within_its_budget():
    # No one draft reads more than 80 bytes here, but a text of unknown author reads all three.
    files = files_of({"en/any.signs.md": 40, "en/gpt.signs.md": 40, "en/claude.signs.md": 40})
    problems = render.budget_problems(files, catalogue(), draft=100, unknown=100)
    assert problems == [
        "a text of unknown author reads 120 bytes, over its 100: en/any.signs.md, en/claude.signs.md, en/gpt.signs.md"
    ]


def test_a_text_of_unknown_author_at_its_budget_passes():
    files = files_of({"en/any.signs.md": 50, "en/gpt.signs.md": 25, "en/claude.signs.md": 25})
    assert render.budget_problems(files, catalogue(), draft=100, unknown=100) == []


def test_a_variants_unknown_read_counts_its_base_language():
    files = files_of({"zh/gpt.signs.md": 60, "zh-Hant/claude.signs.md": 60})
    assert render.budget_problems(files, catalogue(), draft=100, unknown=100) == [
        "a text of unknown author reads 120 bytes, over its 100: zh-Hant/claude.signs.md, zh/gpt.signs.md"
    ]


def test_a_file_of_too_many_lines_fails():
    problems = render.budget_problems(
        {"en/any.signs.md": "x\n" * render.MAX_LINES}, catalogue(), draft=10**9, unknown=10**9
    )
    size = render.MAX_LINES
    assert problems == [f"en/any.signs.md: {size} lines; a file stays under {size}, Claude Code's `Read` default"]


def test_the_budgets_are_the_plans():
    assert render.DRAFT_BUDGET == 16 * 1024
    assert render.LAYOUT_BUDGET == 16 * 1024
    assert render.UNKNOWN_BUDGET == 48 * 1024


def test_write_then_stale_says_nothing(tmp_path):
    out = tmp_path / "signs"
    files = {"en/any.signs.md": "a\n", "any/any.signs.md": "字\n"}
    render.write(files, out)
    assert render.stale(files, out) == []
    assert (out / "en" / "any.signs.md").read_bytes() == b"a\n"  # LF on every platform


def test_stale_names_a_changed_a_missing_and_a_left_over_file(tmp_path):
    render.write({"en/any.signs.md": "a\n", "de/any.signs.md": "b\n", "fr/any.signs.md": "c\n"}, tmp_path)
    (tmp_path / "en" / "any.signs.md").write_bytes(b"edited by hand\n")
    assert render.stale({"en/any.signs.md": "a\n", "hu/any.signs.md": "d\n", "fr/any.signs.md": "c\n"}, tmp_path) == [
        "de/any.signs.md: left over; `byhand render` removes it",
        "en/any.signs.md: differs from the catalogue; run `byhand render`",
        "hu/any.signs.md: missing; run `byhand render`",
    ]


def test_stale_with_no_folder_and_no_files_says_nothing(tmp_path):
    assert render.stale({}, tmp_path / "none") == []


def test_write_removes_what_the_catalogue_no_longer_holds(tmp_path):
    render.write({"en/any.signs.md": "a\n", "de/gpt.signs.md": "b\n"}, tmp_path)
    render.write({"en/any.signs.md": "a\n"}, tmp_path)
    assert not (tmp_path / "de").exists()
    assert (tmp_path / "en" / "any.signs.md").is_file()


def test_the_folder_is_the_repos_wherever_the_command_runs():
    assert pathlib.Path(signs.__file__).resolve().parents[2] / "plugin" / "signs" == render.OUT


def test_the_command_writes_and_checks(tmp_path, monkeypatch, capsys):
    found = catalogue(sign())
    out = tmp_path / "signs"
    monkeypatch.setattr(signs, "load", lambda: (found, []))
    monkeypatch.setattr(render, "OUT", out)
    assert cli.main(["render", "--check"]) == 1
    assert "en/any.signs.md: missing" in capsys.readouterr().out
    assert not out.exists()
    assert cli.main(["render"]) == 0
    assert "1 sign files written" in capsys.readouterr().out
    assert cli.main(["render", "--check"]) == 0
    assert "1 sign files match the catalogue" in capsys.readouterr().out


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
    assert "a draft reads 20161 bytes, over its 16384" in capsys.readouterr().out
    assert not (tmp_path / "signs").exists()


def test_the_real_catalogue_renders_within_its_budgets():
    found, problems = signs.load()
    assert problems == []
    assert render.budget_problems(render.render(found), found) == []


def test_no_rendered_file_can_be_read_as_a_claude_md():
    # On Windows and macOS `claude.md` is a CLAUDE.md, which Claude Code loads as project instructions.
    claude = (ModelRange("claude", Version(4)),)
    files = render.render(catalogue(sign(models=claude), sign("en-b", kinds=("deck",), models=claude)))
    assert sorted(files) == ["en/claude.layout.md", "en/claude.signs.md"]
    assert not any(path.rsplit("/", 1)[-1].casefold() == "claude.md" for path in files)
