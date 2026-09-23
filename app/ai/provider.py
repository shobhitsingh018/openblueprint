from abc import ABC, abstractmethod
from typing import Any


class AIProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, response_schema: dict[str, Any] | None = None) -> str:
        raise NotImplementedError
