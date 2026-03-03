from unittest.mock import MagicMock, patch

import pytest

from src.providers.openai_compatible_provider import OpenAICompatibleProvider


@pytest.fixture
def mock_openai_client():
    with patch("src.providers.openai_compatible_provider.OpenAI") as mock_cls:
        mock_client = MagicMock()
        mock_cls.return_value = mock_client
        yield mock_client


def _make_response(text: str | None, input_tokens: int = 10, output_tokens: int = 5):
    resp = MagicMock()
    resp.choices[0].message.content = text
    resp.usage.prompt_tokens = input_tokens
    resp.usage.completion_tokens = output_tokens
    return resp


def test_complete_returns_text_and_tokens(mock_openai_client):
    mock_openai_client.chat.completions.create.return_value = _make_response("hello")
    provider = OpenAICompatibleProvider(api_key="sk-test", model="gpt-4o")
    text, tokens = provider.complete("sys", "user", 100)
    assert text == "hello"
    assert tokens == {"input": 10, "output": 5}


def test_provider_name_default(mock_openai_client):
    provider = OpenAICompatibleProvider(api_key="sk-test", model="gpt-4o")
    assert provider.provider_name == "openai"


def test_provider_name_custom(mock_openai_client):
    provider = OpenAICompatibleProvider(
        api_key="sk-test", model="mistral-small", provider_name="mistral"
    )
    assert provider.provider_name == "mistral"


def test_base_url_passed_to_client():
    with patch("src.providers.openai_compatible_provider.OpenAI") as mock_cls:
        OpenAICompatibleProvider(
            api_key="key",
            model="some-model",
            base_url="https://openrouter.ai/api/v1",
            provider_name="openrouter",
        )
    mock_cls.assert_called_once_with(
        api_key="key", base_url="https://openrouter.ai/api/v1"
    )


def test_complete_raises_on_none_content(mock_openai_client):
    resp = _make_response(None)
    mock_openai_client.chat.completions.create.return_value = resp
    provider = OpenAICompatibleProvider(api_key="sk-test", model="gpt-4o")
    with pytest.raises(ValueError, match="No text content"):
        provider.complete("sys", "user", 100)
