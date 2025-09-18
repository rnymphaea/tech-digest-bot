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
        self._data: Dict[str, List[int]] = {}

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.StreamHandler(),
            ]
        )

        self.logger = logging.getLogger(__name__)
        self.load()

    def add_user(self, category: str, user_id: int) -> None:
        self.logger.debug(f"{category}: {user_id}")

        with self._lock:
            if category not in self._data:
                self._data[category] = []
            if user_id not in self._data[category]:
                self._data[category].append(user_id)

        self.logger.debug(self._data)

    def remove_user(self, category: str, user_id: int) -> None:
        self.logger.debug(f"{category}: {user_id}")

        with self._lock:
            if category in self._data and user_id in self._data[category]:
                self._data[category].remove(user_id)
                if not self._data[category]:
                    del self._data[category]

        self.logger.debug(self._data)


    def save(self) -> None:
        with self._lock:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self._data, f, ensure_ascii=False, indent=2)
        
        self.logger.debug(f"data saved to {filepath}")

    def load(self) -> None:
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if not content:
                        self._data = {}
                    else:
                        self._data = json.loads(content)
            except (json.JSONDecodeError, OSError):
                self._data = {}
        else:
            self._data = {}

        self.logger.info(f"loaded data:\n{self._data}")
