"""The family and version a model's id names, for models that exist and for models that don't yet."""

import pytest

from byhand import models, signs
from byhand.models import ModelId, ModelRange, Version


@pytest.fixture(scope="module")
def families():
    return signs.load()[0].families.values()


@pytest.mark.parametrize(
    ("model_id", "family", "version"),
    [
        ("claude-opus-5-5", "claude", Version(5, 5)),
        ("claude-sonnet-5-5", "claude", Version(5, 5)),
        ("claude-haiku-5-5", "claude", Version(5, 5)),
        ("claude-fable-5-1", "claude", Version(5, 1)),
        ("claude-opus-9-1", "claude", Version(9, 1)),  # newer than any model the catalogue has seen
        ("claude-opus-4", "claude", Version(4)),
        ("claude-sonnet-4-5-20250929", "claude", Version(4, 5)),
        ("claude-opus-4-20250514", "claude", Version(4)),
        ("claude-3-5-sonnet-20241022", "claude", Version(3, 5)),
        ("claude-3-opus-20240229", "claude", Version(3)),
        ("us.anthropic.claude-opus-4-6-v1:0", "claude", Version(4, 6)),
        ("global.anthropic.claude-sonnet-4-5-20250929-v1:0", "claude", Version(4, 5)),
        ("claude-opus-4-6@20250514", "claude", Version(4, 6)),
        ("anthropic/claude-opus-5.5", "claude", Version(5, 5)),
        ("Claude-Opus-5-5", "claude", Version(5, 5)),
        ("gpt-5.6-sol", "gpt", Version(5, 6)),
        ("gpt-7", "gpt", Version(7)),
        ("gpt-4o", "gpt", Version(4)),
        ("gpt-4-0314", "gpt", Version(4)),
        ("gpt-3.5-turbo-0125", "gpt", Version(3, 5)),
        ("chatgpt-4o-latest", "gpt", Version(4)),
        ("gemini-3.1-pro", "gemini", Version(3, 1)),
        ("grok-3-mini", "grok", Version(3)),
        ("llama-3-70b", "llama", Version(3)),
        ("llama3.1", "llama", Version(3, 1)),
        ("deepseek-v4-pro", "deepseek", Version(4)),
        ("qwen2.5-vl", "qwen", Version(2, 5)),
        ("kimi-k3", "kimi", Version(3)),
        ("gpt-4.1", "gpt", Version(4, 1)),
        ("claude-instant-1.2", "claude", Version(1, 2)),
        ("gemini-1.5-pro-002", "gemini", Version(1, 5)),
        ("grok-4.1-fast", "grok", Version(4, 1)),
        ("llama-4-scout-17b", "llama", Version(4)),
        ("meta.llama3-1-70b", "llama", Version(3, 1)),
        ("kimi-k2.5", "kimi", Version(2, 5)),
        ("deepseek-r1", "deepseek", Version(1)),
        ("deepseek-r1-distill-llama-70b", "deepseek", Version(1)),  # the family named first, wherever the file has it
        ("deepseek-r1-distill-qwen-32b", "deepseek", Version(1)),
    ],
)
def test_an_id_names_its_family_and_version(families, model_id, family, version):
    assert models.read_id(model_id, families) == ModelId(family, version)


@pytest.mark.parametrize("model_id", ["", "   ", "phi-4", "yandexgpt-5", "some-new-model-1"])
def test_an_unknown_family_or_an_empty_id_is_none(families, model_id):
    assert models.read_id(model_id, families) is None


@pytest.mark.parametrize(
    ("model_id", "family"),
    [
        ("claude-latest", "claude"),
        ("mistral-large-2411", "mistral"),  # a date
        ("mistral-small-2503", "mistral"),
        ("gemini-exp-1206", "gemini"),
        ("qwen-max-2025-01-25", "qwen"),
        ("qwen-max-0428", "qwen"),
        ("gpt-realtime-2025-08-28", "gpt"),
        ("mistral-7b", "mistral"),  # a size
        ("mistral.mixtral-8x7b-instruct-v0:1", "mistral"),
        ("gpt-oss-120b", "gpt"),
        ("doubao-pro-32k-240828", "doubao"),
    ],
)
def test_a_number_that_is_no_version_is_not_read_as_one(families, model_id, family):
    assert models.read_id(model_id, families) == ModelId(family, None)


@pytest.mark.parametrize(
    ("text", "expected"), [("5", Version(5)), ("4.6", Version(4, 6)), ("4.6.1", None), ("x", None)]
)
def test_a_written_version(text, expected):
    assert models.parse_version(text) == expected


def test_versions_order_by_number_not_by_text():
    assert Version(4, 9) < Version(4, 10)
    assert Version(4, 10) > Version(4, 9)
    assert Version(5) > Version(4, 99)
    assert Version(4) == Version(4, 0)
    assert hash(Version(4)) == hash(Version(4, 0))
    assert Version(4) != "4"
    assert str(Version(4)) == "4"
    assert str(Version(4, 6)) == "4.6"


@pytest.mark.parametrize(
    ("since", "to", "version", "expected"),
    [
        (Version(4), None, Version(9, 1), True),  # no `to`: a model newer than the catalogue is covered
        (Version(4), None, Version(3, 9), False),
        (Version(4, 6), Version(5), Version(5, 6), True),  # a `to` with no minor holds its whole major
        (Version(4, 6), Version(5), Version(6), False),
        (Version(4, 6), Version(5, 0), Version(5), True),
        (Version(4, 6), Version(5, 0), Version(5, 6), False),  # `to = "5.0"` stops at 5.0
        (Version(4, 6), Version(4, 6), Version(4, 6), True),
        (Version(4, 6), Version(4), Version(4, 7), True),
    ],
)
def test_a_range_holds_a_version(since, to, version, expected):
    assert ModelRange("gpt", since, to).holds(version) is expected
