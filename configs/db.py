from typing import Optional

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from configs.base import BaseConfigs


class DBConfigs(BaseConfigs):
    """Database configuration"""

    db_host: Optional[str] = Field(None)
    db_name: Optional[str] = Field(None)
    db_user: Optional[str] = Field(None)
    db_password: Optional[str] = Field(None)
    db_override_connection_string: Optional[str] = Field(None)

    @property
    def connection_string(self) -> str:
        """Get the connection string"""
        if self.db_override_connection_string:
            return self.db_override_connection_string

        if all(v is None for v in self.model_dump().values()):
            return "sqlite+pysqlite:///:memory:"
        return (
            f"postgresql+psycopg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:5432/{self.db_name}"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


configs = DBConfigs()
