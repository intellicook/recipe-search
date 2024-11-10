import logging
from dataclasses import dataclass
from enum import Enum, auto
from typing import ClassVar, Iterable, Optional, Tuple

import faiss
import numpy as np
import numpy.typing as npt
import torch
from sentence_transformers import SentenceTransformer

from domain.searches.base import BaseSearch
from infra import models


class SentenceTransformerSearch(BaseSearch):
    """Search class for sentence transformer embedding with Faiss index"""

    class EncodeMethod(Enum):
        """Methods to encode ingredient list"""

        COMMA_JOINED_STR = auto()
        QUERIED_COMMA_JOINED_STR = auto()
        AVERAGE_VEC = auto()
        AVERAGE_QUERIED_VEC = auto()

    @dataclass
    class Configs:
        """Initial configuration for the search model"""

        model: str
        prompt: str

    DEFAULT_ENCODE_NON_QUERY_METHOD: ClassVar[EncodeMethod] = (
        EncodeMethod.COMMA_JOINED_STR
    )
    DEFAULT_ENCODE_QUERY_METHOD: ClassVar[EncodeMethod] = (
        EncodeMethod.QUERIED_COMMA_JOINED_STR
    )
    DEFAULT_ENCODE_QUERY: ClassVar[str] = (
        "Which food ingredient lists contain {ingredient}?"
    )

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
    ) -> "SentenceTransformerSearch":
        """Load the index from a file.

        Arguments:
            init_configs (InitConfigs): The initial configuration for the
                search model.
            path (str): The path to load the index from.

        Returns:
            SentenceTransformerSearch: The loaded search model.
        """
        index = faiss.read_index(path)
        return SentenceTransformerSearch(init_configs, index=index)

    def save_to_file(self, path: str):
        """Save the index to a file.

        Arguments:
            path (str): The path to save the index.
        """
        faiss.write_index(self.index, path)
        self.logger.debug(f"Index written to {path}")

    def encode(
        self,
        ingredients: Iterable[str],
        is_query: bool = False,
        method: Optional[EncodeMethod] = None,
        query: str = DEFAULT_ENCODE_QUERY,
    ) -> npt.NDArray[np.float32]:
        """Encode ingredients into a single vector.

        Arguments:
            ingredients (Iterable[str]): The ingredients to encode.
            is_query (bool): Whether the ingredients are a query or not.
            method (EncodeMethod): The method to encode the ingredients.
                If None, the method will be DEFAULT_ENCODE_NON_QUERY_METHOD
                if is_query is False, otherwise DEFAULT_ENCODE_QUERY_METHOD.
            query (str): The query to format for AVERAGE_QUERIED_VEC.
                Defaults to DEFAULT_ENCODE_QUERY.

        Returns:
            npt.NDArray[np.float32]: The encoded vector.
        """
        if method is None:
            method = (
                self.DEFAULT_ENCODE_QUERY_METHOD
                if is_query
                else self.DEFAULT_ENCODE_NON_QUERY_METHOD
            )

        if method == self.EncodeMethod.COMMA_JOINED_STR:
            return self._encode_comma_joined_str(ingredients, is_query)
        elif method == self.EncodeMethod.QUERIED_COMMA_JOINED_STR:
            return self._encode_queried_comma_joined_str(
                query, ingredients, is_query
            )
        elif method == self.EncodeMethod.AVERAGE_VEC:
            return self._encode_average_vec(ingredients, is_query)
        elif method == self.EncodeMethod.AVERAGE_QUERIED_VEC:
            return self._encode_average_queried_vec(
                query, ingredients, is_query
            )
        else:
            raise ValueError(f"Invalid method: {method}")

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

    def _encode_comma_joined_str(
        self, ingredients: Iterable[str], is_query: bool = False
    ) -> npt.NDArray[np.float32]:
        """Encode ingredients by first joining them with a comma.

        Arguments:
            ingredients (Iterable[str]): The ingredients to encode.
            is_query (bool): Whether the ingredients are a query or not.

        Returns:
            npt.NDArray[np.float32]: The encoded vector.
        """
        vec = self.model.encode(
            ", ".join(ingredients),
            prompt=self.configs.prompt if is_query else None,
            normalize_embeddings=True,
        )
        return vec

    def _encode_queried_comma_joined_str(
        self, query: str, ingredients: Iterable[str], is_query: bool = False
    ) -> npt.NDArray[np.float32]:
        """Encode ingredients by first formatting the query and joining them
        with a comma.

        Arguments:
            query (str): The query to format.
            ingredients (Iterable[str]): The ingredients to encode.
            is_query (bool): Whether the ingredients are a query or not.

        Returns:
            npt.NDArray[np.float32]: The encoded vector.
        """
        if not is_query:
            self.logger.warning(
                "QUERIED_COMMA_JOINED_STR method should be used for queries,"
                " defaulting to COMMA_JOINED_STR"
            )
            return self._encode_comma_joined_str(ingredients, is_query)

        query = query.format(ingredient=", ".join(ingredients))
        vec = self.model.encode(
            query, prompt=self.configs.prompt, normalize_embeddings=True
        )
        return vec

    def _encode_average_vec(
        self, ingredients: Iterable[str], is_query: bool = False
    ) -> npt.NDArray[np.float32]:
        """Encode ingredients into a single vector by averaging the vectors.

        Arguments:
            ingredients (Iterable[str]): The ingredients to encode.
            is_query (bool): Whether the ingredients are a query or not.

        Returns:
            npt.NDArray[np.float32]: The encoded vector.
        """
        vecs = self.model.encode(
            list(ingredients),
            prompt=self.configs.prompt if is_query else None,
            normalize_embeddings=True,
        )
        vec = np.mean(vecs, axis=0)
        return vec

    def _encode_average_queried_vec(
        self, query: str, ingredients: Iterable[str], is_query: bool = False
    ) -> npt.NDArray[np.float32]:
        """Encode ingredients by first formatting the query and averaging
        the vectors.

        Arguments:
            query (str): The query to format.
            ingredients (Iterable[str]): The ingredients to encode.
            is_query (bool): Whether the ingredients are a query or not.

        Returns:
            npt.NDArray[np.float32]: The encoded vector.
        """
        if not is_query:
            self.logger.warning(
                "AVERAGE_QUERIED_VEC method should be used for queries,"
                " defaulting to AVERAGE_VEC"
            )
            return self._encode_average_vec(ingredients, is_query)

        queries = (
            query.format(ingredient=ingredient) for ingredient in ingredients
        )
        return self._encode_average_vec(queries, is_query)
