from openai import OpenAI

from src.providers.base import BaseProvider


class OpenAICompatibleProvider(BaseProvider):
    def __init__(
        self,
        api_key: str,
        model: str,
        base_url: str | None = None,
        provider_name: str = "openai",
    ):
        self.model = model
        self.provider_name = provider_name
        self._client = OpenAI(api_key=api_key, base_url=base_url)

    def complete(
        self, system: str, user: str, max_tokens: int
    ) -> tuple[str, dict[str, int]]:
        resp = self._client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            max_tokens=max_tokens,
        )
        text = resp.choices[0].message.content
        if text is None:
            raise ValueError(f"No text content in response: {resp}")
        if resp.usage is None:
            raise ValueError(f"No usage data in response: {resp}")
        tokens = {
            "input": resp.usage.prompt_tokens,
            "output": resp.usage.completion_tokens,
        }
        return text, tokens
