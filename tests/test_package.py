"""The package's version is the one pyproject.toml sets, which the plugin's manifest and pins must equal."""

import tomllib
from pathlib import Path

import byhand

ROOT = Path(__file__).resolve().parents[1]


def test_version_is_pyprojects():
    with (ROOT / "pyproject.toml").open("rb") as f:
        assert byhand.__version__ == tomllib.load(f)["project"]["version"]
