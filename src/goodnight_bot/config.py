from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: str
    reply_strategy: str = "template"
    detection_strategy: str = "fasttext"
    model_path: str = "model/goodnight.bin"
    detection_threshold: float = 0.5
    goodnight_ttl: int = 3600

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


def get_settings() -> Settings:
    return Settings()
