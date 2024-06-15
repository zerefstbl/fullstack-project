import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DB_URI: str
    ECHO_SQL: bool
    print(Path(__file__).parent / f"config")

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / f"config/{os.environ['APP_CONFIG_FILE']}.env",
        case_sensitive=True,
    )

settings = Settings.model_validate({})
