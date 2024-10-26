import logging
from typing import Iterable, List, Tuple

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from configs.domain import configs
from domain.stella import Stella
from infra import models
from infra.db import engine

logger = logging.getLogger(__name__)


def init_stella() -> Stella:
    """Initialize the Stella model.

    Returns:
        Stella: The Stella model.
    """
    with Session(engine) as session:
        stmt = select(func.count()).select_from(models.IndexFileModel)
        count = session.execute(stmt).scalar()

        if count == 0:
            logger.error(
                "Index file not found, please initialize an index file by"
                " running `python -m domain.init_index <path> [<count>]`"
            )
            raise FileNotFoundError
        if count > 1:
            logger.warning(
                "Multiple index files currently not supported, using the"
                " first one"
            )

        stmt = select(models.IndexFileModel)
        index_file = session.execute(stmt).scalar_one()

    try:
        stella = Stella.load_from_file(index_file.path)
    except FileNotFoundError:
        logger.error(
            f"Index file at {index_file.path} not found, database is out of"
            " sync with file system"
        )

    return stella


def get_recipe(id: int) -> models.RecipeModel:
    """Get the recipe details.

    Arguments:
        id (int): The ID of the recipe.

    Returns:
        models.RecipeModel: The recipe details.
    """
    with Session(engine) as session:
        stmt = select(models.RecipeModel).where(models.RecipeModel.id == id)
        recipe = session.execute(stmt).scalar_one()

    return recipe


def get_recipes(ids: Iterable[int]) -> List[models.RecipeModel]:
    """Get the recipe details.

    Arguments:
        ids (Iterable[int]): The IDs of the recipes.

    Returns:
        List[models.RecipeModel]: The recipe details.
    """
    with Session(engine) as session:
        stmt = select(models.RecipeModel).where(models.RecipeModel.id.in_(ids))
        recipes = session.execute(stmt).scalars().all()

    return recipes


def search_recipes_by_ingredients(
    ingredients: Iterable[str],
    limit: int = configs.default_search_limit,
) -> List[Tuple[int, float]]:
    """Search recipes by ingredients.

    Arguments:
        ingredients (Iterable[str]): The list of ingredients to search.
        limit (int): The limit of the number of recipes to return.
            Defaults to configs.domain.configs.default_search_limit.

    Returns:
        List[Tuple[int, float]]: A series of recipe IDs and their
            corresponding similarity scores.
    """
    distances, indices = stella.search(ingredients, limit=limit)

    return sorted(list(zip(indices, distances)), key=lambda x: x[1])


stella = init_stella()
