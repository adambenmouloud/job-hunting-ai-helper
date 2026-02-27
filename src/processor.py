import os
from typing import Literal, TypedDict, cast

from anthropic import Anthropic
from anthropic.types import TextBlock
from dotenv import load_dotenv

from src.loader import load_prompt

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
    def __init__(self, model: str = "claude-sonnet-4-6"):
        load_dotenv(".env")
        api_key = os.getenv("ANTHROPIC_API_KEY")
        self.client = Anthropic(api_key=api_key) if api_key else None
        self.model = model

    def analyze(
        self, resume: str, job_desc: str, mode: AnalysisMode = "full"
    ) -> AnalysisResult:
        """Analyze a resume against a job description. mode='full' for full analysis, 'score' for score + quick fixes."""
        if not self.client:
            raise ValueError("Missing ANTHROPIC_API_KEY in .env")

        sys_prompt_name, tpl_prompt_name = _PROMPTS[mode]
        sys_prompt = load_prompt(sys_prompt_name)
        tpl_prompt = load_prompt(tpl_prompt_name)

        if not sys_prompt or not tpl_prompt:
            raise ValueError(f"Missing prompt files for mode '{mode}'.")

        resp = self.client.messages.create(
            model=self.model,
            system=sys_prompt,
            max_tokens=_MAX_TOKENS[mode],
            messages=[
                {
                    "role": "user",
                    "content": f"{tpl_prompt}\n\nRESUME:\n{resume}\n\nJD:\n{job_desc}",
                }
            ],
        )

        return {
            "content": cast(TextBlock, resp.content[0]).text,
            "tokens": {
                "input": resp.usage.input_tokens,
                "output": resp.usage.output_tokens,
            },
        }
