from pydantic import Field

from configs.base import BaseConfigs


class DBConfigs(BaseConfigs):
    """Database configuration"""

    host: str
    port: str
    name: str
    user: str
    password: str
    use_in_memory: bool = Field(False)

    @property
    def connection_string(self) -> str:
        """Get the connection string"""
        if self.use_in_memory:
            return "sqlite+pysqlite:///:memory:"
        return (
            f"postgresql+psycopg://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.name}"
        )

    class Config:
        env_prefix = "DB_"
        env_file = ".env"
        extra = "ignore"


configs = DBConfigs()
