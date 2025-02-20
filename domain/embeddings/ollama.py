import logging
from typing import List

import ollama

from configs.ollama import configs
from domain.embeddings.base import BaseEmbedding


class OllamaEmbedding(BaseEmbedding):
    """Ollama embedding model"""

    logger: logging.Logger
    client: ollama.Client

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.client = ollama.Client(
            host=configs.ollama_base_url,
        )

        self.logger.info(f"{configs.ollama_model} initialized")

    @staticmethod
    def num_dim() -> int:
        """Get the number of dimensions of the embedding.

        Returns:
            int: The number of dimensions of the embedding.
        """
        return configs.ollama_num_dim

    def embed(self, text: str) -> List[float]:
        """Embed the text.

        Arguments:
            text (str): The text to embed.

        Returns:
            List[float]: The embedding of the text.
        """
        self.logger.debug(f"Embedding text: {text}")

        response = self.client.embed(model=configs.ollama_model, input=text)

        return response.embeddings[0]
