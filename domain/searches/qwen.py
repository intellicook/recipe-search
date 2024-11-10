from typing import Optional

import faiss

from domain.searches.sentence_transformer import SentenceTransformerSearch


class QWen215BInstructSearch(SentenceTransformerSearch):
    """Search class for the gtw-Qwen2-1.5B-instruct model"""

    CONFIGS = SentenceTransformerSearch.Configs(
        model="Alibaba-NLP/gte-Qwen2-1.5B-instruct",
        prompt=(
            "Instruct: Given a web search query, retrieve relevant passages"
            " that answer the query\nQuery: "
        ),
    )

    def __init__(self, index: Optional[faiss.IndexIDMap] = None):
        super().__init__(self.CONFIGS, index)

    @classmethod
    def load_from_file(cls, path: str) -> "QWen215BInstructSearch":
        """Load the index from a file.

        Arguments:
            path (str): The path to load the index from.

        Returns:
            QWen215BInstructSearch: The loaded search model.
        """
        return super().load_from_file(cls.CONFIGS, path)
