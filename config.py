from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # 指定讀取 .env
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    PROJECT_NAME: str = "Music API"
    VERSION: str = "1.0.0"
    API_STR: str = "/api"

    # 從 .env 讀取
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str

    # PostgreSQL
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str = "music_database"

    # Qdrant 
    VECTOR_DATABASE_URL: str = "http://localhost:6333"
    COLLECTION_NAME_SONG: str = "song_features"
    COLLECTION_NAME_USER_HISTORY: str = "user_song_vectors"

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql://"
            f"{self.DATABASE_USERNAME}:"
            f"{self.DATABASE_PASSWORD}@"
            f"{self.DATABASE_HOST}:"
            f"{self.DATABASE_PORT}/"
            f"{self.DATABASE_NAME}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

