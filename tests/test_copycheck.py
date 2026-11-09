"""Finding sign text that shares a run of words with a source. All text here is invented."""

import copycheck
import pytest

SOURCE = "Pale gulls circle the old harbour wall at dusk, and nobody on the quay looks up from the nets."


def sign(**kept):
    row = {
        "id": "en-a",
        "what": "A short note in our own words.",
        "instead": "Say it plainly.",
        "flags": "Something else entirely.",
        "passes": "A plain line.",
    }
    return {**row, **kept}


def shared(row, source=SOURCE, run=6):
    return copycheck.hits(copycheck.fields([row]), [("page.txt", source)], run)


def test_a_shared_run_is_found_with_both_texts():
    found = shared(sign(flags="We saw pale gulls circle the old harbour wall last night."))
    assert [(hit.sign, hit.key, hit.path) for hit in found] == [("en-a", "flags", "page.txt")]
    assert found[0].shared == "pale gulls circle the old harbour"
    assert "at dusk" in found[0].around


def test_a_shorter_run_is_not():
    assert shared(sign(flags="We saw pale gulls circle the old pier.")) == []


def test_case_and_punctuation_hide_nothing():
    assert shared(sign(what="PALE gulls, circle: the old 'harbour' wall."))


def test_each_field_and_each_terms_instead_is_read():
    text = "pale gulls circle the old harbour"
    for row, key in (
        (sign(what=text), "what"),
        (sign(instead=text), "instead"),
        (sign(passes=text), "passes"),
        (sign(terms=[{"term": "zebra", "instead": text}]), "terms"),
    ):
        assert [hit.key for hit in shared(row)] == [key]


def test_a_fixed_string_a_check_needs_is_left_out_of_flags():
    # A fixed string a check needs has to sit in `flags`: only the words around it count.
    terms = sign(
        flags="We saw pale gulls circle the old harbour wall.", terms=[{"term": "gulls circle", "instead": "x"}]
    )
    assert shared(terms) == []  # the run is broken where the term stood
    six = sign(flags="We saw pale gulls circle the old harbour.", check="pale gulls circle the old harbour")
    assert shared(six) == []  # a check's fixed string may be a run long


def test_a_match_longer_than_a_run_is_no_fixed_string():
    row = sign(flags="We saw pale gulls circle the old harbour wall.", check="pale gulls circle the old harbour wall")
    assert [hit.key for hit in shared(row)] == ["flags"]


def test_only_flags_lose_what_the_check_finds():
    # A term in `what` doesn't break a copied run there: `what` holds no fixed string.
    row = sign(what="Pale gulls circle the old harbour wall.", terms=[{"term": "gulls", "instead": "x"}])
    assert [hit.key for hit in shared(row)] == ["what"]


def test_a_copied_sentence_without_spaces_is_found():
    source = "老港口的墙边\uff0c苍白的海鸥在黄昏时盘旋。"  # a full-width comma, as Chinese writes it
    assert [hit.key for hit in shared(sign(flags="苍白的海鸥在黄昏时盘旋。"), source)] == ["flags"]
    assert shared(sign(flags="海鸥盘旋。"), source) == []


def test_a_word_keeps_its_combining_marks():
    assert copycheck.words("महत्वाकांक्षी योजना") == ["महत्वाकांक्षी", "योजना"]
    source = "नई योजना से शहर के लोगों को बहुत लाभ होगा और काम जल्दी पूरा होगा"
    assert shared(sign(flags="योजना से शहर के लोगों को बहुत लाभ होगा"), source)


def test_a_check_that_wont_compile_leaves_the_text_whole():
    assert shared(sign(flags="pale gulls circle the old harbour", check="(unclosed"))


def test_a_sign_with_no_check_or_terms_has_no_pattern():
    assert copycheck.pattern(sign()) is None


def test_a_check_s_forms_by_language_find_together():
    found = copycheck.pattern(sign(check={"en": "pale gulls", "de": "blasse möwen"}))
    assert found is not None
    assert found.search("Pale gulls")
    assert found.search("Blasse Möwen")
    assert not found.search("old harbour")


@pytest.mark.parametrize(
    ("text", "suffix", "expected"),
    [
        ("the [[harbour|old harbour]] wall", ".wikitext", "the old harbour wall"),
        ("'''pale''' gulls", ".wikitext", "pale gulls"),
        ("{{lang|quay}} side", ".wikitext", "quay side"),
        ("<b>pale</b> gulls", ".html", " pale  gulls"),
        ("<b>pale</b> gulls", ".txt", "<b>pale</b> gulls"),
    ],
)
def test_markup_comes_out_of_a_source(text, suffix, expected):
    assert copycheck.plain(text, suffix) == expected


def test_only_source_text_files_are_read_and_the_baseline_is_skipped(tmp_path):
    (tmp_path / "wiki").mkdir()
    (tmp_path / "human-baseline").mkdir()
    (tmp_path / "wiki" / "page.md").write_text("x", encoding="utf-8")
    (tmp_path / "wiki" / "image.png").write_bytes(b"x")
    (tmp_path / "human-baseline" / "book.txt").write_text("x", encoding="utf-8")
    assert [path.name for path in copycheck.source_files(tmp_path)] == ["page.md"]


def signs_folder(path, flags):
    path.mkdir()
    (path / "en.toml").write_text(
        f'[[sign]]\nid = "en-a"\nwhat = "A note."\ninstead = "Say it."\nflags = "{flags}"\npasses = "A line."\n',
        encoding="utf-8",
    )
    return path


def test_the_command_exits_1_on_a_hit_and_prints_both_texts(tmp_path, monkeypatch, capsys):
    folder = signs_folder(tmp_path / "signs", "pale gulls circle the old harbour")
    rows = copycheck.load_signs(folder)
    monkeypatch.setattr(copycheck, "load_signs", lambda: rows)
    sources = tmp_path / "sources"
    sources.mkdir()
    (sources / "page.txt").write_text(SOURCE, encoding="utf-8")
    assert copycheck.main(["--sources", str(sources)]) == 1
    out = capsys.readouterr().out
    assert "en-a flags: 'pale gulls circle the old harbour'" in out
    assert "page.txt: ...pale gulls circle" in out
    assert "1 hit(s)" in out


def test_the_command_exits_0_with_no_hit(tmp_path, monkeypatch, capsys):
    rows = copycheck.load_signs(signs_folder(tmp_path / "signs", "something else"))
    monkeypatch.setattr(copycheck, "load_signs", lambda: rows)
    sources = tmp_path / "sources"
    sources.mkdir()
    (sources / "page.txt").write_text(SOURCE, encoding="utf-8")
    assert copycheck.main(["--sources", str(sources)]) == 0
    assert "0 hit(s)" in capsys.readouterr().out


def test_the_command_says_when_there_are_no_downloads(tmp_path, capsys):
    assert copycheck.main(["--sources", str(tmp_path / "none")]) == 1
    assert "no such folder" in capsys.readouterr().out
