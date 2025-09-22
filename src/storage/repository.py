from abc import ABC, abstractmethod
from typing import List, Dict


class Repository(ABC):
    @abstractmethod
    def add_user(self, category: str, user_id: int) -> None:
        pass

    @abstractmethod
    def get_user_categories(self, user_id: int) -> List[str]:
        pass

    @abstractmethod
    def get_category_users(self, category: str) -> List[int]:
        pass

    @abstractmethod
    def remove_user(self, category: str, user_id: int) -> None:
        pass

    @abstractmethod
    def get_all_categories(self) -> List[str]:
        pass

    @abstractmethod
    def save(self) -> None:
        pass

    @abstractmethod
    def load(self) -> None:
        pass

