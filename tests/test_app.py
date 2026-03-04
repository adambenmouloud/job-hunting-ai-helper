import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# app.py has Streamlit/typst calls and a logging file handler at module level
sys.modules.setdefault("streamlit", MagicMock())
sys.modules.setdefault("typst", MagicMock())
Path("data/logs").mkdir(parents=True, exist_ok=True)

from app import extract_json, get_api_key  # noqa: E402


@pytest.fixture(autouse=True)
def reset_st_mocks():
    """Reset streamlit mock state between tests."""
    st = sys.modules["streamlit"]
    st.secrets.__getitem__.side_effect = None
    st.session_state.get.side_effect = lambda key, default=None: default
    yield
    st.secrets.__getitem__.side_effect = None
    st.session_state.get.side_effect = None


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


# get_api_key resolution chain


def test_get_api_key_falls_back_to_env(monkeypatch):
    sys.modules["streamlit"].secrets.__getitem__.side_effect = KeyError
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-from-env")
    with patch("app.load_dotenv"):
        assert get_api_key() == "sk-from-env"


def test_get_api_key_falls_back_to_session(monkeypatch):
    st = sys.modules["streamlit"]
    st.secrets.__getitem__.side_effect = KeyError
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    state = {"provider_name": "anthropic", "api_key": "sk-from-session"}
    st.session_state.get.side_effect = lambda key, default=None: state.get(key, default)
    with patch("app.load_dotenv"):
        assert get_api_key() == "sk-from-session"


def test_get_api_key_returns_none_when_nothing_configured(monkeypatch):
    sys.modules["streamlit"].secrets.__getitem__.side_effect = KeyError
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    with patch("app.load_dotenv"):
        assert get_api_key() is None
