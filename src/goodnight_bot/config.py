from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: str
    reply_strategy: str = "predefined"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


def get_settings() -> Settings:
    return Settings()
