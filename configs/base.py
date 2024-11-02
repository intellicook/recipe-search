import os

from pydantic_settings import BaseSettings


class BaseConfigs(BaseSettings, env_parse_none_str="None"):
    """Base configuration"""

    def __init__(self, **kwargs):
        if os.getenv("_TESTING"):
            kwargs["_env_file"] = ".env.test"
        super().__init__(**kwargs)
