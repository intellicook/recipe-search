from typing import Optional

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from configs.base import BaseConfigs


class DBConfigs(BaseConfigs):
    """Database configuration"""

    host: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    user: Optional[str] = Field(None)
    password: Optional[str] = Field(None)

    @property
    def connection_string(self) -> str:
        """Get the connection string"""
        if all(v is None for v in self.model_dump().values()):
            return "sqlite+pysqlite:///:memory:"
        return (
            f"postgresql+psycopg://{self.user}:{self.password}"
            f"@{self.host}:5432/{self.name}"
        )

    model_config = SettingsConfigDict(
        env_prefix="DB_",
        env_file=".env",
        extra="ignore",
    )


configs = DBConfigs()
