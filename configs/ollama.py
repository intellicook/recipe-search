from typing import Optional

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from configs.base import BaseConfigs


class OllamaConfigs(BaseConfigs):
    """Ollama configuration"""

    ollama_base_url: Optional[str] = Field("http://localhost:2607")
    ollama_model: Optional[str] = Field("nomic-embed-text")
    ollama_num_dim: Optional[int] = Field(768)

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


configs = OllamaConfigs()
