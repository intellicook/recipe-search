from typing import Optional

import faiss

from domain.embeddings.sentence_transformer import SentenceTransformerEmbedding


class QWen215BInstructEmbedding(SentenceTransformerEmbedding):
    """Embedding class for the gtw-Qwen2-1.5B-instruct model"""

    CONFIGS = SentenceTransformerEmbedding.Configs(
        model="Alibaba-NLP/gte-Qwen2-1.5B-instruct",
        prompt=(
            "Instruct: Given a web search query, retrieve relevant passages"
            " that answer the query\nQuery: "
        ),
    )

    def __init__(self, index: Optional[faiss.IndexIDMap] = None):
        super().__init__(self.CONFIGS, index)

    @classmethod
    def load_from_file(cls, path: str) -> "QWen215BInstructEmbedding":
        """Load the index from a file.

        Arguments:
            path (str): The path to load the index from.

        Returns:
            QWen215BInstructEmbedding: The loaded embedding
        """
        return super().load_from_file(cls.CONFIGS, path)
