import pytest
from unittest.mock import MagicMock, patch

from src.processor import Processor
from tests.conftest import SAMPLE_JD, SAMPLE_RESUME


@pytest.fixture
def mock_anthropic():
    with patch("src.processor.Anthropic") as mock_cls:
        mock_client = MagicMock()
        mock_cls.return_value = mock_client
        mock_resp = MagicMock()
        mock_resp.content = [MagicMock(text='{"score": 85, "missing_keywords": [], "improvements": [], "hard_filter_risk": "low"}')]
        mock_resp.usage.input_tokens = 100
        mock_resp.usage.output_tokens = 50
        mock_client.messages.create.return_value = mock_resp
        yield mock_client


@pytest.fixture
def mock_prompts():
    with patch("src.processor.load_prompt", return_value="fake prompt"):
        yield


def test_analyze_raises_without_api_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    with patch("src.processor.load_dotenv"):
        p = Processor()
    with pytest.raises(ValueError, match="Missing ANTHROPIC_API_KEY"):
        p.analyze(resume=SAMPLE_RESUME, job_desc=SAMPLE_JD)


def test_analyze_raises_on_missing_prompts(mock_anthropic, monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test")
    with patch("src.processor.load_prompt", return_value=""):
        p = Processor()
        with pytest.raises(ValueError, match="Missing prompt files"):
            p.analyze(resume=SAMPLE_RESUME, job_desc=SAMPLE_JD)


def test_analyze_returns_correct_shape(mock_anthropic, mock_prompts, monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test")
    with patch("src.processor.log_llm_call"):
        p = Processor()
        result = p.analyze(resume=SAMPLE_RESUME, job_desc=SAMPLE_JD)
    assert "content" in result
    assert "tokens" in result
    assert "input" in result["tokens"]
    assert "output" in result["tokens"]


def test_analyze_logs_success(mock_anthropic, mock_prompts, monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test")
    with patch("src.processor.log_llm_call") as mock_log:
        p = Processor()
        p.analyze(resume=SAMPLE_RESUME, job_desc=SAMPLE_JD)
    mock_log.assert_called_once()
    assert mock_log.call_args.kwargs["status"] == "success"


def test_analyze_logs_error_and_reraises(mock_anthropic, mock_prompts, monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test")
    mock_anthropic.messages.create.side_effect = Exception("API error")
    with patch("src.processor.log_llm_call") as mock_log:
        p = Processor()
        with pytest.raises(Exception, match="API error"):
            p.analyze(resume=SAMPLE_RESUME, job_desc=SAMPLE_JD)
    mock_log.assert_called_once()
    assert mock_log.call_args.kwargs["status"] == "error"


def test_analyze_score_mode_uses_score_prompts(mock_anthropic, monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test")
    with patch("src.processor.log_llm_call"), patch("src.processor.load_prompt", return_value="fake prompt") as mock_load:
        p = Processor()
        p.analyze(resume=SAMPLE_RESUME, job_desc=SAMPLE_JD, mode="score")
    called_with = [c.args[0] for c in mock_load.call_args_list]
    assert "score_instruction_prompt" in called_with
    assert "score_template_prompt" in called_with


def test_analyze_score_mode_uses_400_max_tokens(mock_anthropic, mock_prompts, monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test")
    with patch("src.processor.log_llm_call"):
        p = Processor()
        p.analyze(resume=SAMPLE_RESUME, job_desc=SAMPLE_JD, mode="score")
    assert mock_anthropic.messages.create.call_args.kwargs["max_tokens"] == 400
