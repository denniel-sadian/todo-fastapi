from pydantic import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    TOKEN_EXPIRES_IN_SECONDS: int = 3600
    APP_NAME: str = 'Todo App'
    APP: str = 'todo.main:app'
    PORT: int
    POSTGRES_DB_URL: str
    MONGODB_URL: str
    MONGO_DB: str


settings = Settings()
