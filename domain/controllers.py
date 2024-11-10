import logging
from typing import Iterable, List, Optional, Tuple, Type

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from configs.domain import configs
from domain import chats, searches
from domain.chats.base import BaseChat, BaseChatMessage
from domain.searches import faiss
from domain.searches.base import BaseSearch
from infra import models
from infra.db import engine

logger = logging.getLogger(__name__)


def init_search(cls: Type[BaseSearch]) -> Optional[BaseSearch]:
    """Initialize the search model.

    Arguments:
        cls (Type[BaseSearch]): The search class to initialize.

    Returns:
        Optional[BaseSearch]: The initialized search model.
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

    if index_file.model not in searches.mapping:
        logger.info(
            f"Search model not found, using {configs.search_model} from"
            " configs"
        )
    else:
        logger.info(
            f"Using the {index_file.model} search model, as specified in"
            " the 'model' field of the index file"
        )
        cls = searches.mapping[index_file.model]

        if index_file.model != configs.search_model:
            logger.warning(
                f"Using the {index_file.model} search model, which is"
                f" different from {configs.search_model} in configs"
            )

    try:
        search = cls.load_from_file(index_file.path)
    except FileNotFoundError:
        logger.error(
            f"Index file at {index_file.path} not found, database is out of"
            " sync with file system, please reinitialize the index"
        )
        return None

    faiss.index_thread = faiss.IndexThread(
        count=index_file.count,
        model=index_file.model,
        path=index_file.path,
        exception=None,
        thread="Database",
    )

    logger.info(f"{cls.__name__} initialized")

    return search


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


def add_recipes(
    recipes: List[models.RecipeModel],
) -> List[models.RecipeModel]:
    """Add the recipes to the database.

    Arguments:
        recipes (List[models.RecipeModel]): The recipes to add.

    Returns:
        List[models.RecipeModel]: The added recipes.
    """
    with Session(engine, expire_on_commit=False) as session:
        session.add_all(recipes)
        session.commit()

    return recipes


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
    logger.debug(
        f"Searching for recipes by ingredients {ingredients} with limit"
        f" {limit}"
    )

    if search is None:
        logger.debug("Search model is not initialized")
        return None

    distances, indices = search.search(ingredients, limit=limit)

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
    logger.debug(
        f"Initializing Faiss index with count {count} and path {path}"
    )

    def _reinit_search():
        global search
        search = init_search(searches.model)

    faiss.init_index(count, configs.search_model, path, _reinit_search)


def get_faiss_index_thread() -> faiss.IndexThread:
    """Get the Faiss index thread.

    Returns:
        faiss.FaissIndexThread: The Faiss index thread.
    """
    return faiss.index_thread


def get_chat_type() -> Type[BaseChat]:
    """Get the chat model.

    Returns:
        Type[BaseChat]: The chat model.
    """
    return chats.model


def chat_by_recipe(
    name: str,
    recipe: models.RecipeModel,
    messages: Iterable[BaseChatMessage],
) -> BaseChatMessage:
    """Chat with the model by recipe.

    Arguments:
        name (str): The name of the user.
        recipe (models.RecipeModel): The recipe to chat with.
        messages (Iterable[BaseChatMessage]): The messages to chat with.

    Returns:
        BaseChatMessage: The response message.
    """
    logger.debug(f"Chatting with {name} by recipe {recipe.name}")

    chat = chats.model()
    chat.set_user(name)
    chat.set_recipe(recipe)

    logger.debug(f"Messages: {messages}")

    return chat.chat(messages)


search = init_search(searches.model)
