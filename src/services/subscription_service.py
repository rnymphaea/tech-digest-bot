from typing import List

from src.storage.repository import Repository


class SubscriptionService:
    def __init__(self, repo: Repository):
        self.repo = repo

    def subscribe(self, category: str, user_id: int) -> None:
        self.repo.add_user(category, user_id)
        self.repo.save()

    def unsubscribe(self, category: str, user_id: int) -> None:
        self.repo.remove_user(category, user_id)
        self.repo.save()

    def save(self) -> None:
        self.repo.save()
