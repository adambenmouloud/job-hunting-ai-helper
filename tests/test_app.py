import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

# app.py has Streamlit/typst calls and a logging file handler at module level
sys.modules.setdefault("streamlit", MagicMock())
sys.modules.setdefault("typst", MagicMock())
Path("data/logs").mkdir(parents=True, exist_ok=True)

from app import extract_json  # noqa: E402


def test_extract_json_valid_json():
    assert extract_json('{"score": 85, "keywords": []}') == {
        "score": 85,
        "keywords": [],
    }


def test_extract_json_embedded_in_prose():
    raw = 'Here is the result: {"score": 72, "improvements": []} Hope that helps.'
    assert extract_json(raw) == {"score": 72, "improvements": []}


def test_extract_json_invalid_raises():
    with pytest.raises(ValueError, match="Failed to extract valid JSON"):
        extract_json("no json here at all")
