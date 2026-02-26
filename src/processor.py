import os
from anthropic import Anthropic
from dotenv import load_dotenv


class Processor:
    def __init__(self, model: str = "claude-sonnet-4-6"):
        """
        Initializes the AI processor.
        Loads environment variables and sets up the Anthropic client.
        """
        # Load .env
        load_dotenv(".env")
        api_key = os.getenv("ANTHROPIC_API_KEY")
        self.client = Anthropic(api_key=api_key) if api_key else None
        self.model = model

    def process(
        self,
        resume: str,
        job_desc: str,
        template_prompt: str,
        system_prompt: str = "",
        max_tokens: int = 1500,
    ) -> dict[str, str | dict[str, int]]:
        if not self.client:
            raise ValueError("Missing ANTHROPIC_API_KEY in .env")

        resp = self.client.messages.create(
            model=self.model,
            system=system_prompt,
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "user",
                    "content": f"{template_prompt}\n\nRESUME:\n{resume}\n\nJD:\n{job_desc}",
                }
            ],
        )

        input_tokens = resp.usage.input_tokens
        output_tokens = resp.usage.output_tokens

        return {
            "content": resp.content[0].text,
            "tokens": {"input": input_tokens, "output": output_tokens},
        }

    def score_only(
        self,
        resume: str,
        job_desc: str,
        template_prompt: str,
        system_prompt: str = "",
    ) -> dict[str, str | dict[str, int]]:
        if not self.client:
            raise ValueError("Missing ANTHROPIC_API_KEY in .env")

        resp = self.client.messages.create(
            model=self.model,
            system=system_prompt,
            max_tokens=400,
            messages=[
                {
                    "role": "user",
                    "content": f"{template_prompt}\n\nRESUME:\n{resume}\n\nJD:\n{job_desc}",
                }
            ],
        )

        input_tokens = resp.usage.input_tokens
        output_tokens = resp.usage.output_tokens

        return {
            "content": resp.content[0].text,
            "tokens": {"input": input_tokens, "output": output_tokens},
        }
