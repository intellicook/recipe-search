from abc import ABC, abstractmethod
from typing import List, Optional

from infra import models


class BaseEmbedding(ABC):
    """Base class for embeddings"""

    @staticmethod
    @abstractmethod
    def num_dim() -> int:
        """Get the number of dimensions of the embedding.

        Returns:
            int: The number of dimensions of the embedding.
        """
        pass

    @abstractmethod
    def embed(self, text: str) -> List[float]:
        """Embed the text.

        Arguments:
            text (str): The text to embed.

        Returns:
            List[float]: The embedding of the text.
        """
        pass

    def embed_recipe(self, recipe: models.RecipeModel) -> List[float]:
        """Embed the recipe.

        Arguments:
            recipe (models.RecipeModel): The recipe to embed.

        Returns:
            List[float]: The embedding of the recipe.
        """
        text = ", ".join(
            [
                f"Title of recipe: {recipe.title}",
                recipe.description,
                (
                    "ingredients: "
                    f"{' '.join(
                        ingredient.name
                        for ingredient in recipe.ingredients
                    )}"
                ),
            ]
        )
        return self.embed(text)

    def embed_user_profile(
        self,
        profile: models.UserProfileModel,
        extra_terms: Optional[str] = None,
    ) -> List[float]:
        """Embed the user profile.

        Arguments:
            profile (models.UserProfileModel): The user profile to embed.
            extra_terms (Optional[str]): Extra terms to include in the
                embedding. Defaults to None.

        Returns:
            List[float]: The embedding of the user profile.
        """
        has_prefer = bool(profile.prefer)
        has_dislike = bool(profile.dislike)

        if not has_prefer and not has_dislike:
            return []

        if has_prefer and has_dislike:
            query = (
                "Find the best recipes given the above preferences and"
                " dislikes."
            )
        elif has_prefer:
            query = "Find the best recipes given the above preferences."
        else:
            query = "Find the best recipes given the above dislikes."

        text = "".join(
            [
                (
                    f"{', '.join(f"PREFER {x}" for x in profile.prefer)}.\n"
                    if has_prefer
                    else ""
                ),
                (
                    f"{', '.join(f"AVOID {x}" for x in profile.dislike)}.\n"
                    if has_dislike
                    else ""
                ),
                (f"Additionally: {extra_terms}.\n" if extra_terms else ""),
                query,
            ]
        )
        return self.embed(text)
