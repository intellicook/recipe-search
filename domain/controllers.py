import logging
from typing import Iterable, List, Optional, Tuple, Type

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from configs.domain import configs
from domain import embeddings
from domain.embeddings import faiss
from domain.embeddings.base import BaseEmbedding
from infra import models
from infra.db import engine

logger = logging.getLogger(__name__)


def init_embedding(cls: Type[BaseEmbedding]) -> Optional[BaseEmbedding]:
    """Initialize the embedding model.

    Arguments:
        cls (Type[BaseEmbedding]): The embedding class to initialize.

    Returns:
        Optional[BaseEmbedding]: The initialized embedding model.
    """
    with Session(engine) as session:
        stmt = select(func.count()).select_from(models.IndexFileModel)
        count = session.execute(stmt).scalar()

        if count == 0:
            logger.error(
                "Index file not found, please initialize an index first"
            )
            return None
        if count > 1:
            logger.warning(
                "Multiple index files currently not supported, using the"
                " first one"
            )

        stmt = select(models.IndexFileModel)
        index_file = session.execute(stmt).scalar_one()

    try:
        model = cls.load_from_file(index_file.path)
    except FileNotFoundError:
        logger.error(
            f"Index file at {index_file.path} not found, database is out of"
            " sync with file system, please reinitialize the index"
        )
        return None

    logger.info(f"{cls.__name__} initialized")

    return model


def reinit_embedding():
    """Reinitialize the embedding model in place."""
    global embedding
    embedding = init_embedding(embeddings.model)


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


def add_recipes(recipes: Iterable[models.RecipeModel]):
    """Add the recipes to the database.

    Arguments:
        recipes (Iterable[models.RecipeModel]): The recipes to add.
    """
    with Session(engine) as session:
        session.add_all(recipes)
        session.commit()


def search_recipes_by_ingredients(
    ingredients: Iterable[str],
    limit: int = configs.default_search_limit,
) -> Optional[List[Tuple[int, float]]]:
    """Search recipes by ingredients.

    Arguments:
        ingredients (Iterable[str]): The list of ingredients to search.
        limit (int): The limit of the number of recipes to return.
            Defaults to configs.domain.configs.default_search_limit.

    Returns:
        Optional[List[Tuple[int, float]]]: A series of recipe IDs and their
            corresponding similarity scores.
    """
    if embedding is None:
        return None

    distances, indices = embedding.search(ingredients, limit=limit)

    return sorted(list(zip(indices, distances)), key=lambda x: x[1])


def init_faiss_index(
    count: int = None,
    path: str = configs.default_faiss_index_path,
):
    """Initialize the Faiss index.

    Arguments:
        count (int): The number of recipes to index. Defaults to None.
        path (str): The path to save the index. Defaults to
            configs.domain.configs.default_faiss_index_path.
    """
    faiss.init_index(count, configs.embedding_model, path, reinit_embedding)


def get_faiss_index_thread() -> faiss.IndexThread:
    """Get the Faiss index thread.

    Returns:
        faiss.FaissIndexThread: The Faiss index thread.
    """
    return faiss.index_thread


embedding = init_embedding(embeddings.model)
