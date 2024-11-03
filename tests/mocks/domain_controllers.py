from typing import Iterable, List

from configs.domain import configs
from domain.embeddings import faiss
from infra import models


def get_recipe(id: int) -> models.RecipeModel:
    pass


def get_recipes(ids: Iterable[int]) -> List[models.RecipeModel]:
    pass


def add_recipes(recipes: Iterable[models.RecipeModel]):
    pass


def search_recipes_by_ingredients(
    ingredients: Iterable[str],
    limit: int = configs.default_search_limit,
) -> List[int]:
    pass


def init_faiss_index(
    count: int = None,
    path: str = configs.default_faiss_index_path,
):
    pass


def get_faiss_index_thread() -> faiss.IndexThread:
    pass
