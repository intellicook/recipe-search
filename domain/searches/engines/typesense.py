import logging
from dataclasses import dataclass
from typing import ClassVar, Iterable, List

import typesense
import typesense.collection
import typesense.exceptions

from configs.domain import configs as domain_configs
from configs.typesense import configs
from infra import models


@dataclass
class Recipe:
    """Recipe class."""

    SCHEMA: ClassVar[dict] = {
        "name": "recipes",
        "fields": [
            {
                "name": "name",
                "type": "string",
            },
            {
                "name": "ingredients",
                "type": "string[]",
            },
        ],
    }

    id: int
    name: str
    ingredients: List[str]

    @classmethod
    def equal_schema(cls, json: dict) -> bool:
        """Check if the JSON object has the same schema as the recipe.

        Arguments:
            json (dict): The JSON object.

        Returns:
            bool: True if the JSON object has the same schema, False otherwise.
        """
        if cls.SCHEMA["name"] != json["name"]:
            return False

        return all(
            any(
                field["name"] == json_field["name"]
                and field["type"] == json_field["type"]
                for json_field in json["fields"]
            )
            for field in cls.SCHEMA["fields"]
        )

    def from_model(recipe: models.RecipeModel) -> "Recipe":
        """Create a recipe from a recipe model.

        Arguments:
            recipe (models.RecipeModel): The recipe model.

        Returns:
            Recipe: The recipe.
        """
        return Recipe(
            id=recipe.id,
            name=recipe.name,
            ingredients=recipe.ingredients,
        )

    def to_model(self) -> models.RecipeModel:
        """Convert the recipe to a recipe model.

        Returns:
            models.RecipeModel: The recipe model.
        """
        return models.RecipeModel(
            id=self.id,
            name=self.name,
            ingredients=self.ingredients,
        )

    def from_json(json: dict) -> "Recipe":
        """Create a recipe from a JSON object.

        Arguments:
            json (dict): The JSON object.

        Returns:
            Recipe: The recipe.
        """
        return Recipe(
            id=int(json["id"]),
            name=json["name"],
            ingredients=json["ingredients"],
        )

    def to_json(self) -> dict:
        """Convert the recipe to a JSON object.

        Returns:
            dict: The JSON object.
        """
        return {
            "id": str(self.id),
            "name": self.name,
            "ingredients": self.ingredients,
        }


class TypesenseSearchEngine:
    """Typesense search engine class."""

    logger: logging.Logger
    client: typesense.Client

    @property
    def recipes(self) -> typesense.collection.Collection:
        """Get the recipes collection.

        Returns:
            typesense.collection.Collection: The recipes collection.
        """
        return self.client.collections[Recipe.SCHEMA["name"]]

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.client = typesense.Client(
            {
                "nodes": [
                    {
                        "host": configs.host,
                        "port": "8108",
                        "protocol": "http",
                    }
                ],
                "api_key": configs.api_key,
                "connection_timeout_seconds": 5,
            }
        )

        try:
            recipe_schema = self.recipes.retrieve()
            if not Recipe.equal_schema(recipe_schema):
                self.logger.warning(
                    "Recipe collection schema is outdated, deleting and"
                    " recreating"
                )
                self.recipes.delete()
                self.create_recipe_collection()
        except typesense.exceptions.ObjectNotFound:
            self.create_recipe_collection()

        self.logger.info("Typesense search engine initialized")

    def is_healthy(self) -> bool:
        """Check if the search engine is healthy.

        Returns:
            bool: True if healthy, False otherwise.
        """
        try:
            response = self.client.api_call.get("/health")
            return response["ok"]
        except Exception as e:
            self.logger.error(f"Typesense health check failed: {e}")
            return False

    def create_recipe_collection(self):
        """Create the recipe collection."""
        self.client.collections.create(Recipe.SCHEMA)
        self.logger.info("Recipe collection created")

    def add_recipes(self, recipes: Iterable[models.RecipeModel]):
        """Add recipes to the collection.

        Arguments:
            recipes (Iterable[models.RecipeModel]): The recipes to add.
        """
        recipes: Iterable[Recipe] = (
            Recipe.from_model(recipe) for recipe in recipes
        )
        self.recipes.documents.import_(
            [recipe.to_json() for recipe in recipes]
        )
        self.logger.info("Recipes added to collection")

    def remove_all_recipes(self):
        """Remove all recipes from the collection."""
        try:
            self.recipes.documents.delete({"filter_by": "id:!=0"})
            self.logger.info("All recipes removed from collection")
        except typesense.exceptions.ObjectNotFound:
            self.logger.info("Recipe collection not found, skipping removal")

    def search_recipes(
        self,
        ingredients: Iterable[str],
        page: int = 1,
        per_page: int = domain_configs.default_search_per_page,
    ) -> List[models.TypesenseResult]:
        """Search for recipes.

        Arguments:
            ingredients (Iterable[str]): The ingredients to search for.
            page (int): The page number. Defaults to 1.
            per_page (int): The number of results per page. Defaults to
                domain_configs.default_search_per_page.

        Returns:
            List[models.TypesenseResult]: The list of recipe results.
        """
        recipes_documents = self.recipes.retrieve()
        recipes_count = recipes_documents["num_documents"]

        response = self.recipes.documents.search(
            {
                "q": " ".join(ingredients),
                "query_by_weights": "1,1",
                "query_by": "name,ingredients",
                "drop_tokens_threshold": recipes_count + 1,
                "drop_tokens_mode": "both_sides:3",
                "page": page,
                "per_page": per_page,
            }
        )

        return [
            models.TypesenseResult.from_json(hit) for hit in response["hits"]
        ]


search_engine = TypesenseSearchEngine()
