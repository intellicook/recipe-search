from typing import Optional

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from configs.base import BaseConfigs


class AzureConfigs(BaseConfigs):
    """Azure configuration"""

    openai_api_key: Optional[str] = Field(None)
    openai_base_url: Optional[str] = Field(None)

    model_config = SettingsConfigDict(
        env_prefix="AZURE_",
        env_file=".env",
        extra="ignore",
    )


configs = AzureConfigs()
