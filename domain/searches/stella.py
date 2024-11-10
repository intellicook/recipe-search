from typing import Optional

import faiss

from domain.searches.sentence_transformer import SentenceTransformerSearch


class StellaEn15BV5Search(SentenceTransformerSearch):
    """Search class for the stella_en_1.5B_v5 model"""

    CONFIGS = SentenceTransformerSearch.Configs(
        model="dunzhang/stella_en_1.5B_v5",
        prompt=(
            "Instruct: Retrieve semantically similar food ingredient"
            " text.\nQuery: "
        ),
    )

    def __init__(self, index: Optional[faiss.IndexIDMap] = None):
        super().__init__(self.CONFIGS, index)

    @classmethod
    def load_from_file(cls, path: str) -> "StellaEn15BV5Search":
        """Load the index from a file.

        Arguments:
            path (str): The path to load the index from.

        Returns:
            StellaEn15BV5Search: The loaded search model.
        """
        return super().load_from_file(cls.CONFIGS, path)
