"""The plugin's sign files: what goes where, what a draft reads, the budgets, and staleness."""

import datetime

import pytest

from byhand import cli, render, signs
from byhand.models import ModelRange, Version
from byhand.signs import Catalogue, Family, Language, Sign, Term

CLAUDE = Family("claude", "Claude", ("claude",))
GPT = Family("gpt", "GPT", ("gpt",))


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
    assert sorted(files) == ["any/any.md", "en/any.md", "en/gpt.md", "zh/gpt.md"]
    assert "en-b" not in files["en/gpt.md"]
    assert "en-c" not in files["en/any.md"]
    assert files["en/gpt.md"].startswith("# Signs of AI writing: English, GPT\n")
    assert files["any/any.md"].startswith("# Signs of AI writing: every language, every model\n")


def test_a_sign_with_ranges_in_two_families_renders_in_both():
    both = (ModelRange("gpt", Version(5)), ModelRange("claude", Version(4), Version(4, 6)))
    files = render.render(catalogue(sign(models=both)))
    assert sorted(files) == ["en/claude.md", "en/gpt.md"]
    assert "gpt 5 and later" in files["en/gpt.md"]
    assert "claude" not in files["en/gpt.md"].split("\n", 3)[3]
    assert "claude 4 to 4.6" in files["en/claude.md"]


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
    assert f"(usual; {printed})" in render.render(catalogue(sign(models=(span,))))["en/gpt.md"]


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
    assert list(files) == (["en/any.layout.md"] if layout else ["en/any.md"])
    assert files[next(iter(files))].splitlines()[0].endswith("decks and sheets") is layout


def test_signs_sort_strongest_first_then_by_id():
    text = render.render(
        catalogue(
            sign("en-b", strength="weak"),
            sign("en-c", strength="strong"),
            sign("en-e", strength="usual"),
            sign("en-d", strength="usual"),
        )
    )["en/any.md"]
    assert [line.split()[1] for line in text.splitlines() if line.startswith("- ")] == ["en-c", "en-d", "en-e", "en-b"]


def test_a_line_holds_what_the_model_acts_on_and_nothing_else():
    terms = (Term("delv(?:e|es)", "look at"), Term("tapestry", "mix"))
    text = render.render(catalogue(sign(kinds=("email", "post"), terms=terms, flags="FLAGS", passes="PASSES")))
    line = text["en/any.md"].splitlines()[-1]
    assert line == (
        "- en-a (usual; email, post): Does a thing. Instead: Says it plainly. "
        "Terms: `delv(?:e|es)`: look at; `tapestry`: mix"
    )
    assert "FLAGS" not in text["en/any.md"]


def test_the_cluster_rule_prints_only_where_a_weak_sign_is():
    weak = render.render(catalogue(sign(strength="weak")))["en/any.md"]
    assert f"with {signs.WEAK_CLUSTER} or more in one paragraph" in weak
    assert "paragraph" not in render.render(catalogue(sign()))["en/any.md"]


def test_a_retired_sign_renders_nowhere_whatever_the_date():
    retired = sign("en-b", until=datetime.date(2999, 1, 1))
    assert list(render.render(catalogue(retired))) == []
    assert "en-b" not in render.render(catalogue(retired, sign()))["en/any.md"]


def test_what_a_draft_reads():
    found = catalogue()
    assert render.draft_files(found, "en", "gpt") == ["any/any.md", "any/gpt.md", "en/any.md", "en/gpt.md"]
    assert render.draft_files(found, "en", "any") == ["any/any.md", "en/any.md"]
    assert render.draft_files(found, "zh-Hant", "claude") == [
        "any/any.md",
        "any/claude.md",
        "zh/any.md",
        "zh/claude.md",
        "zh-Hant/any.md",
        "zh-Hant/claude.md",
    ]


def files_of(sizes):
    return {path: "x" * size for path, size in sizes.items()}


def test_a_draft_within_its_budget_passes():
    files = files_of({"any/any.md": 40, "en/any.md": 30, "en/gpt.md": 30})
    assert render.budget_problems(files, catalogue(), draft=100) == []


def test_a_draft_over_its_budget_fails():
    files = files_of({"any/any.md": 40, "en/any.md": 30, "en/gpt.md": 31})
    assert render.budget_problems(files, catalogue(), draft=100) == [
        "a en draft by gpt reads 101 bytes; the budget is 100"
    ]


def test_the_budget_counts_a_variant_with_its_base_language():
    files = files_of({"zh/any.md": 60, "zh-Hant/any.md": 60})
    problems = render.budget_problems(files, catalogue(), draft=100)
    assert any(problem.startswith("a zh-Hant draft by any") for problem in problems)
    assert not any(problem.startswith("a zh draft") for problem in problems)


def test_the_budget_counts_bytes_not_characters():
    assert render.budget_problems({"zh/any.md": "字" * 40}, catalogue(), draft=100)


def test_a_layout_file_counts_in_no_prose_budget():
    assert render.budget_problems(files_of({"en/any.layout.md": 500}), catalogue(), draft=100, unknown=100) == []


def test_a_text_of_unknown_author_reads_every_family_within_its_budget():
    # No one draft reads more than 80 bytes here, but a text of unknown author reads all three.
    files = files_of({"en/any.md": 40, "en/gpt.md": 40, "en/claude.md": 40})
    problems = render.budget_problems(files, catalogue(), draft=100, unknown=100)
    assert problems == ["a en text of unknown author reads 120 bytes; the budget is 100"]


def test_a_file_of_too_many_lines_fails():
    problems = render.budget_problems({"en/any.md": "x\n" * render.MAX_LINES}, catalogue(), draft=10**9, unknown=10**9)
    assert problems == [
        f"en/any.md: {render.MAX_LINES} lines; a file stays under {render.MAX_LINES}, Claude Code's `Read` default"
    ]


def test_the_budgets_are_the_plans():
    assert render.DRAFT_BUDGET == 16 * 1024
    assert render.UNKNOWN_BUDGET == 48 * 1024


def test_write_then_stale_says_nothing(tmp_path):
    out = tmp_path / "signs"
    files = {"en/any.md": "a\n", "any/any.md": "字\n"}
    render.write(files, out)
    assert render.stale(files, out) == []
    assert (out / "en" / "any.md").read_bytes() == b"a\n"  # LF on every platform


def test_stale_names_a_changed_a_missing_and_a_left_over_file(tmp_path):
    render.write({"en/any.md": "a\n", "de/any.md": "b\n", "fr/any.md": "c\n"}, tmp_path)
    (tmp_path / "en" / "any.md").write_bytes(b"edited by hand\n")
    assert render.stale({"en/any.md": "a\n", "hu/any.md": "d\n", "fr/any.md": "c\n"}, tmp_path) == [
        "de/any.md: left over; `byhand render` removes it",
        "en/any.md: differs from the catalogue; run `byhand render`",
        "hu/any.md: missing; run `byhand render`",
    ]


def test_stale_with_no_folder_and_no_files_says_nothing(tmp_path):
    assert render.stale({}, tmp_path / "none") == []


def test_write_removes_what_the_catalogue_no_longer_holds(tmp_path):
    render.write({"en/any.md": "a\n", "de/gpt.md": "b\n"}, tmp_path)
    render.write({"en/any.md": "a\n"}, tmp_path)
    assert not (tmp_path / "de").exists()
    assert (tmp_path / "en" / "any.md").is_file()


def test_the_command_writes_and_checks(tmp_path, monkeypatch, capsys):
    found = catalogue(sign())
    monkeypatch.setattr(signs, "load", lambda: (found, []))
    out = tmp_path / "signs"
    assert cli.main(["render", "--check", "--out", str(out)]) == 1
    assert "en/any.md: missing" in capsys.readouterr().out
    assert not out.exists()
    assert cli.main(["render", "--out", str(out)]) == 0
    assert "1 sign files written to" in capsys.readouterr().out
    assert cli.main(["render", "--check", "--out", str(out)]) == 0
    assert "1 sign files match the catalogue" in capsys.readouterr().out


def test_the_command_writes_nothing_from_a_bad_catalogue(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(signs, "load", lambda: (catalogue(sign()), ["a problem"]))
    assert cli.main(["render", "--out", str(tmp_path / "signs")]) == 1
    assert "a problem" in capsys.readouterr().out
    assert not (tmp_path / "signs").exists()


def test_the_command_writes_nothing_over_budget(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(signs, "load", lambda: (catalogue(sign(what="x" * 20000)), []))
    assert cli.main(["render", "--out", str(tmp_path / "signs")]) == 1
    assert "the budget is" in capsys.readouterr().out
    assert not (tmp_path / "signs").exists()


def test_the_real_catalogue_renders_within_its_budgets():
    found, problems = signs.load()
    assert problems == []
    assert render.budget_problems(render.render(found), found) == []
