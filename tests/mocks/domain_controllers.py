from typing import Any, Iterable, List, Type

from configs.domain import configs
from infra import models


def is_typesense_healthy() -> bool:
    pass


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


def search_recipes(
    ingredients: Iterable[str],
    page: int = 1,
    per_page: int = configs.default_search_per_page,
    include_detail: bool = False,
) -> List[models.RecipeModel]:
    pass


def init_faiss_index(
    count: int = None,
    path: str = configs.default_faiss_index_path,
):
    pass


def get_faiss_index_thread() -> Any:  # faiss.IndexThread
    pass


def get_chat_type() -> Type[Any]:  # Type[BaseChat]
    pass


def chat_by_recipe(
    name: str,
    recipe: models.RecipeModel,
    messages: Iterable[Any],  # Iterablep[BaseChatMessage]
) -> Any:  # BaseChatMessage
    pass
