import pytest
from unittest.mock import MagicMock, patch

from src.processor import Processor
from tests.conftest import SAMPLE_JD, SAMPLE_RESUME

_MOCK_RESPONSE = '{"score": 85, "missing_keywords": [], "improvements": [], "hard_filter_risk": "low"}'


@pytest.fixture
def mock_provider():
    provider = MagicMock()
    provider.model = "claude-sonnet-4-6"
    provider.complete.return_value = (_MOCK_RESPONSE, {"input": 100, "output": 50})
    return provider


@pytest.fixture
def mock_prompts():
    with patch("src.processor.load_prompt", return_value="fake prompt"):
        yield


def test_analyze_raises_on_missing_prompts(mock_provider):
    with patch("src.processor.load_prompt", return_value=""):
        with pytest.raises(ValueError, match="Missing prompt files"):
            Processor(mock_provider).analyze(resume=SAMPLE_RESUME, job_desc=SAMPLE_JD)


def test_analyze_returns_correct_shape(mock_provider, mock_prompts):
    with patch("src.processor.log_llm_call"):
        result = Processor(mock_provider).analyze(
            resume=SAMPLE_RESUME, job_desc=SAMPLE_JD
        )
    assert "content" in result
    assert "tokens" in result
    assert "input" in result["tokens"]
    assert "output" in result["tokens"]


def test_analyze_logs_success(mock_provider, mock_prompts):
    with patch("src.processor.log_llm_call") as mock_log:
        Processor(mock_provider).analyze(resume=SAMPLE_RESUME, job_desc=SAMPLE_JD)
    mock_log.assert_called_once()
    assert mock_log.call_args.kwargs["status"] == "success"


def test_analyze_logs_error_and_reraises(mock_provider, mock_prompts):
    mock_provider.complete.side_effect = Exception("API error")
    with patch("src.processor.log_llm_call") as mock_log:
        with pytest.raises(Exception, match="API error"):
            Processor(mock_provider).analyze(resume=SAMPLE_RESUME, job_desc=SAMPLE_JD)
    mock_log.assert_called_once()
    assert mock_log.call_args.kwargs["status"] == "error"


def test_analyze_score_mode_uses_score_prompts(mock_provider):
    with (
        patch("src.processor.log_llm_call"),
        patch("src.processor.load_prompt", return_value="fake prompt") as mock_load,
    ):
        Processor(mock_provider).analyze(
            resume=SAMPLE_RESUME, job_desc=SAMPLE_JD, mode="score"
        )
    called_with = [c.args[0] for c in mock_load.call_args_list]
    assert "score_instruction_prompt" in called_with
    assert "score_template_prompt" in called_with


def test_analyze_score_mode_uses_400_max_tokens(mock_provider, mock_prompts):
    with patch("src.processor.log_llm_call"):
        Processor(mock_provider).analyze(
            resume=SAMPLE_RESUME, job_desc=SAMPLE_JD, mode="score"
        )
    assert mock_provider.complete.call_args.args[2] == 400
