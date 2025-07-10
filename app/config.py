from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    telegram_bot_token: str
    openai_api_key: str
    webhook_url: str

    class Config:
        env_file = ".env"

settings = Settings()