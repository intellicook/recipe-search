from pydantic import Field
from pydantic_settings import SettingsConfigDict

from configs.base import BaseConfigs
from domain.model_types import ChatModelType


class DomainConfigs(BaseConfigs):
    """Domain configuration"""

    domain_default_faiss_index_path: str = Field("index.faiss")
    domain_default_search_limit: int = Field(10)
    domain_default_search_per_page: int = Field(10)
    domain_chat_message_limit: int = Field(10)
    domain_chat_model: ChatModelType

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


configs = DomainConfigs()
