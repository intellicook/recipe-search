from pydantic import Field
from pydantic_settings import SettingsConfigDict

from configs.base import BaseConfigs


class LoggingConfigs(BaseConfigs):
    """Logging configuration"""

    level: str = Field("INFO")

    model_config = SettingsConfigDict(
        env_prefix="LOGGING_",
        env_file=".env",
        extra="ignore",
    )


configs = LoggingConfigs()
