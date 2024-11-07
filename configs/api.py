from pydantic import Field
from pydantic_settings import SettingsConfigDict

from configs.base import BaseConfigs


class APIConfigs(BaseConfigs):
    """API server configuration"""

    port: str = Field("2505")

    model_config = SettingsConfigDict(
        env_prefix="API_",
        env_file=".env",
        extra="ignore",
    )


configs = APIConfigs()
