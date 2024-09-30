from configs.base import BaseConfigs


class APIConfigs(BaseConfigs):
    """API server configuration"""

    port: str

    class Config:
        env_prefix = "API_"
        env_file = ".env"
        extra = "ignore"


configs = APIConfigs()
