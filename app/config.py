from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    ECHO: bool

    #for JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SECRET_KEY: str
    ALGORITHM: str

    #for PWD CONTEXT
    SCHEME_FOR_PWD: str = "brcypt"

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: str
    MAIL_SERVER: str
    MAIL_FROM_NAME: str


    @property
    def DATABASE_URL(self): 
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    
 

    HASHING_SCHEME: str = "bcrypt"
    
    api_prefix: str = "/api/v1"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()