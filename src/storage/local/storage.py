import json
import os
import threading
import logging
from typing import Dict, List


from src.storage.repository import Repository


class LocalStorage(Repository):
    def __init__(self, filepath: str):
        if not filepath:
            raise ValueError("filepath is empty")

        self.filepath = filepath
        self._lock = threading.Lock()
        self._category_to_users: Dict[str, List[int]] = {}
        self._user_to_categories: Dict[int, List[str]] = {}

        self.logger = logging.getLogger(__name__)
        self.load()

    def add_user(self, category: str, user_id: int) -> None:
        self.logger.debug(f"{category}: {user_id}")

        with self._lock:
            if category not in self._category_to_users:
                self._category_to_users[category] = []
            if user_id not in self._category_to_users[category]:
                self._category_to_users[category].append(user_id)

            if user_id not in self._user_to_categories:
                self._user_to_categories[user_id] = []
            if category not in self._user_to_categories[user_id]:
                self._user_to_categories[user_id].append(category)

        self.logger.debug(self._category_to_users)
        self.logger.debug(self._user_to_categories)

    def get_user_categories(self, user_id: int) -> List[str]:
        func_name = "get_user_categories"

        categories = self._user_to_categories.get(user_id, [])

        self.logger.debug(f"{func_name}: {user_id}: {categories}")
        return categories

    def get_category_users(self, category: str) -> List[int]:
        func_name = "get_category_users"

        users = self._category_to_users.get(category, [])

        self.logger.debug(f"{func_name}: {category}: {users}")
        return users

    def remove_user(self, category: str, user_id: int) -> None:
        func_name = "remove_user"

        self.logger.debug(f"{func_name}: {category}: {user_id}")

        with self._lock:
            if category in self._category_to_users and user_id in self._category_to_users[category]:
                self._category_to_users[category].remove(user_id)
                if not self._category_to_users[category]:
                    del self._category_to_users[category]

            if user_id in self._user_to_categories and category in self._user_to_categories[user_id]:
                self._user_to_categories[user_id].remove(category)
                if not self._user_to_categories[user_id]:
                    del self._user_to_categories[user_id]

        self.logger.debug(f"{func_name}: {self._category_to_users}")
        self.logger.debug(f"{func_name}: {self._user_to_categories}")

    def get_all_categories(self) -> List[str]:
        func_name = "get_all_categories"

        categories = list(self._category_to_users.keys())

        self.logger.debug(f"{func_name}: {categories}")
        return categories

    def save(self) -> None:
        with self._lock:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self._category_to_users, f, ensure_ascii=False, indent=2)
        
        self.logger.debug(f"data saved to {self.filepath}")

    def load(self) -> None:
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if not content:
                        self._category_to_users = {}
                    else:
                        self._category_to_users = json.loads(content)
            except (json.JSONDecodeError, OSError):
                self._category_to_users = {}
        else:
            self._category_to_users = {}

        self._user_to_categories = {}
        for category, users in self._category_to_users.items():
            for user in users:
                if user not in self._user_to_categories:
                    self._user_to_categories[user] = []
                if category not in self._user_to_categories[user]:
                    self._user_to_categories[user].append(category)

        self.logger.info(f"loaded data:\n{self._category_to_users}")
        self.logger.debug(f"reconstructed user_to_categories:\n{self._user_to_categories}")
