"""The family and version a model's id names, for models that exist and for models that don't yet."""

import pytest

from byhand import models, signs
from byhand.models import ModelId, Version


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
    ],
)
def test_an_id_names_its_family_and_version(families, model_id, family, version):
    assert models.read_id(model_id, families) == ModelId(family, version)


@pytest.mark.parametrize("model_id", ["", "   ", "phi-4", "yandexgpt-5", "some-new-model-1"])
def test_an_unknown_family_or_an_empty_id_is_none(families, model_id):
    assert models.read_id(model_id, families) is None


def test_a_family_with_no_number_has_no_version(families):
    assert models.read_id("claude-latest", families) == ModelId("claude", None)


@pytest.mark.parametrize(
    ("text", "expected"), [("5", Version(5)), ("4.6", Version(4, 6)), ("4.6.1", None), ("x", None)]
)
def test_a_written_version(text, expected):
    assert models.parse_version(text) == expected


def test_versions_order_by_number_not_by_text():
    assert Version(4, 10) > Version(4, 9)
    assert Version(5) > Version(4, 99)
    assert Version(4) == Version(4, 0)
    assert hash(Version(4)) == hash(Version(4, 0))
    assert Version(4) != "4"
    assert str(Version(4)) == "4"
    assert str(Version(4, 6)) == "4.6"
