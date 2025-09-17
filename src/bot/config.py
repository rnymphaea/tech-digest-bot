import logging

from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from aiogram import Bot


class Settings(BaseSettings):
    bot_token_file: SecretStr

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


settings = Settings()
bot = Bot(token=settings.bot_token) 

logging.basicConfig(
   level=logging.INFO,
   format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
   handlers=[
       logging.StreamHandler(),
   ]
)

logger = logging.getLogger(__name__)
