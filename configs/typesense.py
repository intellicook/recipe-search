from typing import Optional

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from configs.base import BaseConfigs


class TypesenseConfigs(BaseConfigs):
    """Typesense configuration"""

    host: Optional[str] = Field(None)
    api_key: Optional[str] = Field(None)

    model_config = SettingsConfigDict(
        env_prefix="TYPESENSE_",
        env_file=".env",
        extra="ignore",
    )


configs = TypesenseConfigs()
