import logging

from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from aiogram import Bot

from src.storage.repository import Repository
from src.storage.local.storage import LocalStorage

from src.services.subscription_service import SubscriptionService

from src.parsers.habr_rss import HabrRSSParser

class Settings(BaseSettings):
    bot_token_file: SecretStr
    dump_file: str = "/app/dump.json"
    storage_type: str = "local"
    logging_level: str = "info"
    timeout_minutes: int = 1

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
        
    @property
    def bot_token(self) -> str:
        token_path = Path(self.bot_token_file.get_secret_value())
        if not token_path.exists():
            raise FileNotFoundError(f"Bot token file not found: {token_path}")
        
        token = token_path.read_text().strip()
        if not token:
            raise ValueError("empty token")

        return token

    @property 
    def repo(self) -> Repository:
        if self.storage_type == "local":
            return LocalStorage(self.dump_file)
        else:
            raise ValueError("storage type is not supported")

    @property
    def log_level(self) -> int:
        levels = {"debug": logging.DEBUG, "info": logging.INFO}
        level = self.logging_level.lower().strip()

        if level not in levels:
            raise ValueError(f"logging level {self.logging_level} is not supported")

        return levels[level]


settings = Settings()
bot = Bot(token=settings.bot_token) 

logging.basicConfig(
   level=settings.log_level,
   format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
   handlers=[
       logging.StreamHandler(),
   ]
)

logger = logging.getLogger(__name__)

sub_service = SubscriptionService(settings.repo)

parser = HabrRSSParser()
