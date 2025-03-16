from pydantic import Field
from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    cache_size: int = Field(..., validation_alias="CACHE_CAPACITY")


app_config = AppConfig()
