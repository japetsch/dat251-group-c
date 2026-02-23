from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Defines the application's configuration settings,
    read from .env file using pydantic-settings
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    DB_PATH: str
    TEST_DB_PATH: str

    @property
    def database_url(self) -> str:
        return f"sqlite+aiosqlite:///./{self.DB_PATH}"

    @property
    def test_database_url(self) -> str:
        return f"sqlite+aiosqlite:///./{self.TEST_DB_PATH}"

    @classmethod
    @lru_cache
    def get_settings(cls) -> Settings:
        """
        Returns a Settings instance (might be cached)
        """
        print("Loading application settings...")
        settings = Settings()
        return settings
