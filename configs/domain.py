from pydantic import Field
from pydantic_settings import SettingsConfigDict

from configs.base import BaseConfigs


class DomainConfigs(BaseConfigs):
    """Domain configuration"""

    default_search_limit: int = Field(10)

    model_config = SettingsConfigDict(
        env_prefix="DOMAIN_",
        env_file=".env",
        extra="ignore",
    )


configs = DomainConfigs()
