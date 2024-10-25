from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from pydantic import (
    AnyUrl,
    BeforeValidator,
    HttpUrl,
    PostgresDsn,
    computed_field,
    model_validator,
)
from pydantic_core import MultiHostUrl
from typing import Annotated, Any, Literal
import secrets

def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Use top level .env file (one level above ./backend/)
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
        env_file_encoding = 'utf-8'  # 指定编码
    )

    FIRST_SUPERUSER: str = "wumignhui@qq.com"
    FIRST_SUPERUSER_PASSWORD: str = "123456789"

    ##千问模型配置
    QWEN_MODEL:str
    QWEN_KEY:str
    QWEN_URL:str
    QWEN_MAX_TOKEN:int

    OPENAI_ENABLE:bool
    OPENAI_MODEL:str
    OPENAI_KEY:str
    OPENAI_URL:str = "https://api.openai.com/v1"
    OPENAI_MAX_TOKEN:int

    ##音乐配置
    MUSIC_URL: str
    MUSIC_COOKIE:str

    WEATGER_API_KEY:str

    XIMALAYA_API_KEY: str
    XIMALAYA_API_SECRET: str
    XIMALAYA_API_URL: str

    app_name: str = Field(default="My FastAPI App", description="The name of the application")
    admin_email: str = Field(..., description="Admin email address")
    items_per_page: int = Field(default=10, ge=1, description="Number of items per page")
    
    PROJECT_NAME: str
    SENTRY_DSN: HttpUrl | None = None
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""

    SECRET_KEY: str = secrets.token_urlsafe(32)
    
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    FRONTEND_HOST: str = "http://localhost:5173"

    BACKEND_CORS_ORIGINS: Annotated[
            list[AnyUrl] | str, BeforeValidator(parse_cors)
        ] = []

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [
            self.FRONTEND_HOST
        ]
    
settings = Settings()