import logging
from typing import Iterable, List, Optional

from sqlalchemy import delete, select, text
from sqlalchemy.orm import Session

from configs.domain import configs
from domain import chats, embeddings
from domain.searches import typesense
from infra import models
from infra.db import engine

logger = logging.getLogger(__name__)


def is_typesense_healthy() -> bool:
    """Check if the Typesense search engine is healthy.

    Returns:
        bool: True if healthy, False otherwise.
    """
    return typesense.search_engine.is_healthy()


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

    This function does not guarantee the order of the recipes.

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
    # chat = chats.model()
    for recipe in recipes:
        if not recipe.veggie_identity:
            # recipe.veggie_identity = chat.identify_recipe_veggie_identity(
            #     recipe
            # )
            recipe.veggie_identity = models.UserProfileModelVeggieIdentity.NONE

    with Session(engine, expire_on_commit=False) as session:
        session.add_all(recipes)
        session.commit()

    typesense.search_engine.add_recipes(recipes)

    return recipes


def search_recipes(
    ingredients: Iterable[str],
    username: str,
    extra_terms: Optional[str] = None,
    page: int = 1,
    per_page: int = configs.domain_default_search_per_page,
    include_detail: bool = False,
) -> List[models.TypesenseResult]:
    """Search recipes by ingredients.

    Results are ordered by relevance.

    Arguments:
        ingredients (Iterable[str]): The list of ingredients to search.
        username (str): The username of the user profile to use.
        extra_terms (Optional[str]): Extra terms to search for. Defaults to
            None.
        page (int): The page number to return. Defaults to 1.
        per_page (int): The number of recipes to return per page. Defaults to
            configs.domain.configs.default_search_per_page.
        include_detail (bool): Whether to include the recipe details. Defaults
            to False. If False, only the recipe ID, name, and ingredients are
            assigned to the returned recipes.

    Returns:
        List[models.TypesenseResult]: The list of results.
    """
    logger.debug(
        f"Searching for recipes with: ingredients={ingredients},"
        f" username={username}, extra_terms={extra_terms}, page={page},"
        f" per_page={per_page}, include_detail={include_detail}"
    )

    profile = get_user_profile(username)

    if profile:
        embedding = profile.embedding
        logger.debug("User profile used")

        if extra_terms:
            embedding = embeddings.model().embed_user_profile(
                profile, extra_terms
            )
            logger.debug("Extra terms used")
    else:
        embedding = None
        logger.debug("User profile not used")

        if extra_terms:
            embedding = embeddings.model().embed(extra_terms)
            logger.debug("Extra terms used")

    results = typesense.search_engine.search_recipes(
        ingredients,
        embedding,
        page=page,
        per_page=per_page,
    )

    if not include_detail:
        return results

    result_ids = [result.recipe.id for result in results]

    recipes = sorted(
        get_recipes(result.recipe.id for result in results),
        key=lambda recipe: result_ids.index(recipe.id),
    )

    return [
        models.TypesenseResult(recipe=recipe, highlights=result.highlights)
        for recipe, result in zip(recipes, results)
    ]


def chat_by_recipe(
    name: str,
    username: str,
    recipe: models.RecipeModel,
    messages: Iterable[models.ChatMessageModel],
) -> models.ChatResponseModel:
    """Chat with the model by recipe.

    Arguments:
        name (str): The name of the user.
        username (str): The username of the user profile to use.
        recipe (models.RecipeModel): The recipe to chat with.
        messages (Iterable[models.ChatMessageModel]): The messages to chat
            with.

    Returns:
        models.ChatResponseModel: The response.
    """
    logger.debug(f"Chatting with {name} by recipe {recipe.title}")

    chat = chats.model()
    chat.set_user(name, username)
    chat.set_recipe(recipe)

    messages = messages[-configs.domain_chat_message_limit :]

    logger.debug(f"Messages: {messages}")

    return chat.chat(messages)


def chat_by_recipe_stream(
    name: str,
    username: str,
    recipe: models.RecipeModel,
    messages: Iterable[models.ChatMessageModel],
) -> Iterable[models.ChatStreamModel]:
    """Chat with the model by recipe and return a stream of messages.

    Arguments:
        name (str): The name of the user.
        username (str): The username of the user profile to use.
        recipe (models.RecipeModel): The recipe to chat with.
        messages (Iterable[models.ChatMessageModel]): The messages to chat
            with.

    Returns:
        Iterable[models.ChatStreamModel]: The response stream of messages.
    """
    logger.debug(f"Chatting with {name} by recipe {recipe.title}")

    chat = chats.model()
    chat.set_user(name, username)
    chat.set_recipe(recipe)

    messages = messages[-configs.domain_chat_message_limit :]

    logger.debug(f"Messages: {messages}")

    return chat.chat_stream(messages)


def reset_data():
    """Reset the data."""
    with Session(engine) as session:
        session.execute(delete(models.RecipeModel))
        session.execute(
            text(
                f"ALTER SEQUENCE {models.RecipeModel.__tablename__}_id_seq"
                " RESTART WITH 1"
            )
        )

        session.commit()

    typesense.search_engine.remove_all_recipes()


def set_user_profile(profile: models.UserProfileModel):
    """Set the user profile.

    Arguments:
        profile (models.UserProfileModel): The user profile.
    """
    if not profile.embedding:
        profile.embedding = embeddings.model().embed_user_profile(profile)

    with Session(engine) as session:
        stmt = select(models.UserProfileModel).where(
            models.UserProfileModel.username == profile.username
        )
        existing_profile = session.execute(stmt).scalar_one_or_none()

        if existing_profile:
            existing_profile.veggie_identity = profile.veggie_identity
            existing_profile.prefer = profile.prefer
            existing_profile.dislike = profile.dislike
            existing_profile.embedding = profile.embedding
        else:
            session.add(profile)

        session.commit()


def get_user_profile(username: str) -> Optional[models.UserProfileModel]:
    """Get the user profile.

    Arguments:
        username (str): The username.

    Returns:
        Optional[models.UserProfileModel]: The user profile.
    """
    with Session(engine) as session:
        stmt = select(models.UserProfileModel).where(
            models.UserProfileModel.username == username
        )
        profile = session.execute(stmt).scalar_one_or_none()

    return profile
