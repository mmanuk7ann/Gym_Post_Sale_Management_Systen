from pydantic import EmailStr
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    SMTP_SERVER: str
    SMTP_PORT: int = 587
    # SMTP_USERNAME: EmailStr
    # SMTP_PASSWORD: str

    class Config:
        env_file = ".env"

settings = Settings()