from abc import ABC, abstractmethod
from typing import List, Dict


class Repository(ABC):
    @abstractmethod
    def add_user(self, category: str, user_id: int) -> None:
        pass

    @abstractmethod
    def remove_user(self, category: str, user_id: int) -> None:
        pass

    @abstractmethod
    def save(self) -> None:
        pass

    @abstractmethod
    def load(self) -> None:
        pass

