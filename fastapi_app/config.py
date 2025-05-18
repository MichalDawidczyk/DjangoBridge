from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "mysql://user:password@localhost/db_name"

settings = Settings()