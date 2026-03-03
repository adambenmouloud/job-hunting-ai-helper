from abc import ABC, abstractmethod


class BaseProvider(ABC):
    model: str
    provider_name: str

    @abstractmethod
    def complete(
        self, system: str, user: str, max_tokens: int
    ) -> tuple[str, dict[str, int]]:
        """Send a completion request.

        Returns:
            (text, {"input": N, "output": N})
        """
        ...
