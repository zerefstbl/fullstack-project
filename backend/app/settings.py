import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DB_URI: str
    ECHO_SQL: bool

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / ".env",
        case_sensitive=True,
    )

settings = Settings.model_validate({})
