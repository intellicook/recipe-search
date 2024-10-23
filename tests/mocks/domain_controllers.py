from typing import Iterable, List

from configs.domain import configs


def search_recipes_by_ingredients(
    ingredients: Iterable[str],
    limit: int = configs.default_search_limit,
) -> List[int]:
    pass
