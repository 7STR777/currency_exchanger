from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_NAME: str
    DB_PORT: int
    DB_PASS: str
    DB_HOST: str
    DB_USER: str
    ALGORITHM: str
    SECRET_KEY: str
    BASE_URL: str
    API_KEY: str

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    model_config = SettingsConfigDict(env_file="C:\\Users\\igorm\\OneDrive\\Desktop\\etc\\currencyexchange\src\\.env")
    

settings = Settings()