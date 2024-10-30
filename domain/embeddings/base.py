from abc import ABC, abstractmethod
from typing import Iterable, Tuple

import numpy as np
import numpy.typing as npt

from infra import models


class BaseEmbedding(ABC):
    """Base class for embedding models"""

    @classmethod
    @abstractmethod
    def load_from_file(cls, path: str) -> "BaseEmbedding":
        """Load the index from a file.

        Arguments:
            path (str): The path to load the index from.

        Returns:
            BaseEmbedding: The loaded embedding model.
        """

    @abstractmethod
    def save_to_file(self, path: str):
        """Save the index to a file.

        Arguments:
            path (str): The path to save the index.
        """

    @abstractmethod
    def add(self, recipe: models.RecipeModel) -> npt.NDArray[np.float32]:
        """Add a recipe entry to the index.

        Arguments:
            recipe (RecipeModel): The recipe to add.

        Returns:
            npt.NDArray[np.float32]: The encoded vector.
        """

    @abstractmethod
    def remove(self, id: int):
        """Remove a recipe entry from the index.

        Arguments:
            id (int): The id of the recipe to remove.
        """

    @abstractmethod
    def search(
        self, ingredients: Iterable[str], k: int = 1
    ) -> Tuple[npt.NDArray[np.float32], npt.NDArray[np.int64]]:
        """Perform similarity search to search recipe by ingredients.

        Arguments:
            ingredients (Iterable[str]): The ingredients to search.
            limit (int): The number of recipes to return. Defaults to 1.

        Returns:
            npt.NDArray[np.float32]: The distances of shape (limit,).
            npt.NDArray[np.int64]: The ids of the recipes of shape (limit,).
        """
