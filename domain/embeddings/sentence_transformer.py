import logging
from dataclasses import dataclass
from typing import Iterable, Optional, Tuple

import faiss
import numpy as np
import numpy.typing as npt
import torch
from sentence_transformers import SentenceTransformer

from domain.embeddings.base import BaseEmbedding
from infra import models


class SentenceTransformerEmbedding(BaseEmbedding):
    """Embedding class for sentence transformer with Faiss index"""

    @dataclass
    class Configs:
        """Initial configuration for the embedding model"""

        model: str
        prompt: str

    logger: logging.Logger
    configs: Configs
    model: SentenceTransformer
    index: faiss.IndexIDMap

    def __init__(
        self,
        init_configs: Configs,
        index: Optional[faiss.IndexIDMap] = None,
    ):
        self.logger = logging.getLogger(__name__)
        self.configs = init_configs
        self.model = SentenceTransformer(
            self.configs.model, trust_remote_code=True
        )

        if torch.cuda.is_available():
            self.model = self.model.cuda()

        self.index = index or faiss.IndexIDMap(
            faiss.IndexFlatIP(self.model.get_sentence_embedding_dimension())
        )

        self.logger.info(f"{self.configs.model} initialized")

    @classmethod
    def load_from_file(
        cls, init_configs: Configs, path: str
    ) -> "SentenceTransformerEmbedding":
        """Load the index from a file.

        Arguments:
            init_configs (InitConfigs): The initial configuration for the
                embedding model.
            path (str): The path to load the index from.

        Returns:
            SentenceTransformerEmbedding: The loaded embedding model.
        """
        index = faiss.read_index(path)
        return SentenceTransformerEmbedding(init_configs, index)

    def save_to_file(self, path: str):
        """Save the index to a file.

        Arguments:
            path (str): The path to save the index.
        """
        faiss.write_index(self.index, path)
        self.logger.debug(f"Index written to {path}")

    def encode(
        self, ingredients: Iterable[str], is_query: bool = False
    ) -> npt.NDArray[np.float32]:
        """Encode ingredients into a single vector.

        Arguments:
            ingredients (Iterable[str]): The ingredients to encode.
            is_query (bool): Whether the ingredients are a query or not.

        Returns:
            npt.NDArray[np.float32]: The encoded vector.
        """
        test = self.model.encode(
            ", ".join(ingredients),
            prompt=self.configs.prompt if is_query else None,
            normalize_embeddings=True,
        )
        return test

    def add(self, recipe: models.RecipeModel) -> npt.NDArray[np.float32]:
        """Add a recipe entry to the index.

        Arguments:
            recipe (models.RecipeModel): The recipe to add.

        Returns:
            npt.NDArray[np.float32]: The encoded vector.
        """
        vec: npt.NDArray[np.float32] = self.encode(recipe.ingredients)
        self.index.add_with_ids(vec.reshape(1, -1), recipe.id)
        return vec

    def remove(self, id: int):
        """Remove a recipe entry from the index.

        Arguments:
            id (int): The id of the recipe to remove.
        """
        self.index.remove_ids(np.array([id]))

    def search(
        self, ingredients: Iterable[str], limit: int = 1
    ) -> Tuple[npt.NDArray[np.float32], npt.NDArray[np.int64]]:
        """Perform similarity search to search recipe by ingredients.

        Arguments:
            ingredients (Iterable[str]): The ingredients to search.
            limit (int): The number of recipes to return. Defaults to 1.

        Returns:
            npt.NDArray[np.float32]: The distances of shape (limit,).
            npt.NDArray[np.int64]: The ids of the recipes of shape (limit,).
        """
        self.logger.debug(f"Searching for {ingredients}")
        vec = self.encode(ingredients, is_query=True)

        distances: np.ndarray
        ids: np.ndarray
        distances, ids = self.index.search(vec.reshape(1, -1), limit)

        self.logger.debug(f"Found {ids} with distances {distances}")

        return distances.flatten(), ids.flatten()
