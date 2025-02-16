from pydantic import Field
from pydantic_settings import SettingsConfigDict

from configs.base import BaseConfigs
from domain.model_types import ChatModelType


class DomainConfigs(BaseConfigs):
    """Domain configuration"""

    default_faiss_index_path: str = Field("index.faiss")
    default_search_limit: int = Field(10)
    default_search_per_page: int = Field(10)
    chat_message_limit: int = Field(10)
    chat_model: ChatModelType

    model_config = SettingsConfigDict(
        env_prefix="DOMAIN_",
        env_file=".env",
        extra="ignore",
    )


configs = DomainConfigs()
