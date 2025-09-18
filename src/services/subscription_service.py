from typing import List
import logging

from src.storage.repository import Repository


class SubscriptionService:
    def __init__(self, repo: Repository):
        self.repo = repo
        self.logger = logging.getLogger(__name__)

    def subscribe(self, category: str, user_id: int) -> None:
        self.repo.add_user(category, user_id)
        self.repo.save()

    def unsubscribe(self, category: str, user_id: int) -> None:
        self.repo.remove_user(category, user_id)
        self.repo.save()

    def unsubscribe_all(self, user_id: int) -> None:
        func_name = "unsubscribe_all"

        categories = list(self.repo.get_user_categories(user_id))
        self.logger.debug(f"{func_name}: {user_id}: {categories}")

        for category in categories:
            self.repo.remove_user(category, user_id)
        self.repo.save()

    def get_user_categories(self, user_id: int) -> List[str]:
        return self.repo.get_user_categories(user_id)

    def get_category_users(self, category: str) -> List[int]:
        return self.repo.get_category_users(category)

    def save(self) -> None:
        self.repo.save()
