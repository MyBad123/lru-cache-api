from pydantic import BaseSettings, Field


class AppConfig(BaseSettings):
    cache_size = Field(env="DB_PORT")
    
