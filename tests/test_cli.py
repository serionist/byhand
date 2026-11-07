"""The `byhand` command, in-process, and once through a real pipe with text cp1252 can't hold."""

import sys

import gate
import pytest

from byhand import cli, signs


def test_validate_reports_what_ships(capsys):
    assert cli.main(["validate"]) == 0
    assert "the catalogue is valid: 101 languages" in capsys.readouterr().out


def test_validate_lists_every_problem_and_fails(capsys, monkeypatch):
    monkeypatch.setattr(signs, "load", lambda: (signs.Catalogue(), ["one", "two"]))
    assert cli.main(["validate"]) == 1
    out = capsys.readouterr().out
    assert "one\ntwo\n" in out
    assert "2 problem(s)" in out


@pytest.mark.parametrize(
    ("model_id", "expected"),
    [
        ("claude-opus-5-5", "claude 5.5\n"),
        ("gpt-7", "gpt 7\n"),
        ("claude-latest", "claude: no version in the id\n"),
        ("phi-4", "any: no family the catalogue knows, so the any signs alone\n"),
    ],
)
def test_models_reads_an_id(capsys, model_id, expected):
    assert cli.main(["models", model_id]) == 0
    assert capsys.readouterr().out == expected


def test_models_fails_on_a_broken_models_file(capsys, monkeypatch, tmp_path):
    (tmp_path / "models.toml").write_text("[[family", encoding="utf-8")
    monkeypatch.setattr(signs, "CATALOGUE", tmp_path)
    assert cli.main(["models", "claude-opus-5-5"]) == 1
    assert "models.toml: not valid TOML" in capsys.readouterr().out


def test_models_reads_only_the_families(capsys, monkeypatch):
    # A bad sign is validate's to report: it doesn't stop `byhand models`.
    monkeypatch.setattr(signs, "load", lambda: pytest.fail("models loads the whole catalogue"))
    assert cli.main(["models", "gpt-7"]) == 0
    assert capsys.readouterr().out == "gpt 7\n"


def test_a_command_is_required():
    with pytest.raises(SystemExit):
        cli.main([])


def test_the_command_writes_utf8_through_a_pipe():
    # On Windows a pipe is cp1252 unless the command says otherwise, and these characters can't be written in it.
    code = (
        "import sys; from byhand import cli, signs; "
        "signs.load = lambda: (signs.Catalogue(), ['不是而是 ő']); sys.exit(cli.main(['validate']))"
    )
    done = gate.run([sys.executable, "-c", code])
    assert done.returncode == 1, done.stderr
    assert "不是而是 ő" in done.stdout
