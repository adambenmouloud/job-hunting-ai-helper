from src.providers.anthropic_provider import AnthropicProvider
from src.providers.base import BaseProvider
from src.providers.openai_compatible_provider import OpenAICompatibleProvider
from src.providers.registry import PROVIDERS


def create_provider(provider_name: str, api_key: str, model: str) -> BaseProvider:
    if provider_name == "anthropic":
        return AnthropicProvider(api_key=api_key, model=model)
    config = PROVIDERS[provider_name]
    return OpenAICompatibleProvider(
        api_key=api_key,
        model=model,
        base_url=config.base_url,
        provider_name=provider_name,
    )
