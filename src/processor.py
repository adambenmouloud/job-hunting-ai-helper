import logging
import time
from typing import Literal, TypedDict

from src.loader import load_prompt
from src.llm_logger import log_llm_call
from src.providers.base import BaseProvider

logger = logging.getLogger(__name__)

AnalysisMode = Literal["full", "score"]

_PROMPTS: dict[AnalysisMode, tuple[str, str]] = {
    "full": ("instruction_prompt", "template_prompt"),
    "score": ("score_instruction_prompt", "score_template_prompt"),
}

_MAX_TOKENS: dict[AnalysisMode, int] = {
    "full": 1500,
    "score": 400,
}


class AnalysisResult(TypedDict):
    content: str
    tokens: dict[str, int]


class Processor:
    def __init__(self, provider: BaseProvider):
        self.provider = provider

    def analyze(
        self,
        resume: str,
        job_desc: str,
        mode: AnalysisMode = "full",
        resume_filename: str | None = None,
    ) -> AnalysisResult:
        """Analyze a resume against a job description. mode='full' for full analysis, 'score' for score + quick fixes."""
        sys_prompt_name, tpl_prompt_name = _PROMPTS[mode]
        sys_prompt = load_prompt(sys_prompt_name)
        tpl_prompt = load_prompt(tpl_prompt_name)

        if not sys_prompt or not tpl_prompt:
            raise ValueError(f"Missing prompt files for mode '{mode}'.")

        user_content = f"{tpl_prompt}\n\nRESUME:\n{resume}\n\nJD:\n{job_desc}"

        logger.info(f"Starting LLM call: mode={mode} resume={resume_filename}")
        start = time.monotonic()
        try:
            text, tokens = self.provider.complete(
                sys_prompt, user_content, _MAX_TOKENS[mode]
            )
            duration_ms = int((time.monotonic() - start) * 1000)
            log_llm_call(
                feature=mode,
                model=self.provider.model,
                duration_ms=duration_ms,
                status="success",
                resume_filename=resume_filename,
                input_tokens=tokens["input"],
                output_tokens=tokens["output"],
            )
        except Exception as e:
            duration_ms = int((time.monotonic() - start) * 1000)
            log_llm_call(
                feature=mode,
                model=self.provider.model,
                duration_ms=duration_ms,
                status="error",
                resume_filename=resume_filename,
                error_message=str(e),
            )
            logger.error(f"LLM call failed: {e}", exc_info=True)
            raise

        return {"content": text, "tokens": tokens}
