from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env.local",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="forbid",
    )
    db_url: str = Field(min_length=1, max_length=128, title="url базы данных")
    db_echo: bool = Field(default=False, title="Режим echo при исполнении команд")


settings = Settings()
