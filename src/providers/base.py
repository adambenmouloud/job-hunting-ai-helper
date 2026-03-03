from typing import Protocol


class BaseProvider(Protocol):
    model: str

    def complete(
        self, system: str, user: str, max_tokens: int
    ) -> tuple[str, dict[str, int]]:
        """Send a completion request.

        Returns:
            (text, {"input": N, "output": N})
        """
        ...
