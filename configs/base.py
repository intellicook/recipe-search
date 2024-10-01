import os
from typing import Tuple, Type

from pydantic_settings import BaseSettings, PydanticBaseSettingsSource


class BaseConfigs(BaseSettings, env_parse_none_str="None"):
    """Base configuration"""

    def __init__(self, **kwargs):
        if os.getenv("_TESTING"):
            kwargs["_env_file"] = ".env.test"
        super().__init__(**kwargs)

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        """Change source priority order so .env file is loaded first"""
        return (
            init_settings,
            dotenv_settings,
            env_settings,
            file_secret_settings,
        )
