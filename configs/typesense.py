from typing import Optional

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from configs.base import BaseConfigs


class TypesenseConfigs(BaseConfigs):
    """Typesense configuration"""

    typesense_host: Optional[str] = Field(None)
    typesense_api_key: Optional[str] = Field(None)

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


configs = TypesenseConfigs()
