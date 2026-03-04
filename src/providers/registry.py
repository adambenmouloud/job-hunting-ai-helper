from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderConfig:
    base_url: str | None
    models: list[str]


DEFAULT_PROVIDER = "anthropic"
DEFAULT_MODEL = "claude-sonnet-4-6"

PROVIDERS: dict[str, ProviderConfig] = {
    "anthropic": ProviderConfig(
        base_url=None,
        models=[
            "claude-sonnet-4-6",
            "claude-opus-4-6",
            "claude-haiku-4-5-20251001",
        ],
    ),
    "openai": ProviderConfig(
        base_url=None,
        models=[
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-4.1",
            "gpt-4.1-mini",
            "o3",
            "o4-mini",
        ],
    ),
    "mistral": ProviderConfig(
        base_url="https://api.mistral.ai/v1",
        models=["mistral-large-latest", "mistral-medium-latest", "mistral-tiny-latest"],
    ),
    "mammouth": ProviderConfig(
        base_url="https://api.mammouth.ai/v1",
        models=[
            "claude-sonnet-4-6",
            "claude-opus-4-6",
            "gpt-4.1",
            "gpt-4.1-mini",
            "gemini-2.5-pro",
            "gemini-2.5-flash",
            "mistral-large-3",
            "deepseek-v3.2",
        ],
    ),
    "openrouter": ProviderConfig(
        base_url="https://openrouter.ai/api/v1",
        models=[
            "anthropic/claude-4.5-sonnet-20250929",
            "anthropic/claude-4-sonnet-20250522",
            "google/gemini-2.5-pro",
            "google/gemini-2.5-flash",
            "google/gemini-2.0-flash-001",
            "deepseek/deepseek-chat-v3-0324",
            "openai/gpt-4.1-mini-2025-04-14",
            "x-ai/grok-4-fast",
        ],
    ),
}
