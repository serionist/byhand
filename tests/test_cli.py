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
