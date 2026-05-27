from abc import ABC, abstractmethod
from typing import Any, Dict
from pydantic import BaseModel

class Tool(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    @abstractmethod
    def parameters_schema(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def execute(self, session_id: str, **kwargs) -> Any:
        pass
