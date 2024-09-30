from pydantic import Field

from configs.base import BaseConfigs


class LoggingConfigs(BaseConfigs):
    """Logging configuration"""

    level: str = Field("INFO")

    class Config:
        env_prefix = "LOGGING_"
        env_file = ".env"
        extra = "ignore"


configs = LoggingConfigs()
