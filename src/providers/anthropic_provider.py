import os

from anthropic import Anthropic
from anthropic.types import TextBlock
from dotenv import load_dotenv


class AnthropicProvider:
    def __init__(self, api_key: str | None = None, model: str = "claude-sonnet-4-6"):
        if api_key is None:
            load_dotenv(".env")
            api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("Missing ANTHROPIC_API_KEY")
        self.model = model
        self._client = Anthropic(api_key=api_key)

    def complete(
        self, system: str, user: str, max_tokens: int
    ) -> tuple[str, dict[str, int]]:
        resp = self._client.messages.create(
            model=self.model,
            system=system,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": user}],
        )

        # Extraction of text content
        text = next(
            (block.text for block in resp.content if isinstance(block, TextBlock)),
            None,
        )
        if text is None:
            raise ValueError(f"No text content in response: {resp.content}")

        tokens = {
            "input": resp.usage.input_tokens,
            "output": resp.usage.output_tokens,
        }
        return text, tokens
