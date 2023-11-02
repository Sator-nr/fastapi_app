from pydantic_settings import BaseSettings
from pydantic import root_validator


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    @root_validator(skip_on_failure=True)
    def get_database_url(self, v):
        v['DATABASE_URL'] = f"postgresql+asyncpg://{v['DB_USER']}:{v['DB_PASS']}@{v['DB_HOST']}:{v['DB_PORT']}/{v['DB_NAME']}"
        return v

    class Config:
        env_file = '.env'


settings = Settings()
