from typing import Iterable, List, Optional

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


def search_recipes(
    ingredients: Iterable[str],
    page: int = 1,
    per_page: int = configs.domain_default_search_per_page,
    include_detail: bool = False,
) -> List[models.TypesenseResult]:
    pass


def chat_by_recipe(
    name: str,
    recipe: models.RecipeModel,
    messages: Iterable[models.ChatMessageModel],
) -> models.ChatResponseModel:
    pass


def chat_by_recipe_stream(
    name: str,
    recipe: models.RecipeModel,
    messages: Iterable[models.ChatMessageModel],
) -> Iterable[models.ChatStreamModel]:
    pass


def set_user_profile(profile: models.UserProfileModel):
    pass


def get_user_profile(username: str) -> Optional[models.UserProfileModel]:
    pass
