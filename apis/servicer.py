from typing import List

import grpc
from sqlalchemy.exc import NoResultFound

from configs.domain import configs as domain_configs
from domain import controllers
from infra import db, models
from protos.add_recipes_pb2 import (
    AddRecipesRequest,
    AddRecipesResponse,
    AddRecipesResponseRecipe,
)
from protos.chat_by_recipe_pb2 import ChatByRecipeRequest, ChatByRecipeResponse
from protos.faiss_index_thread_pb2 import (
    FaissIndexThreadRequest,
    FaissIndexThreadResponse,
    FaissIndexThreadStatus,
)
from protos.health_pb2 import (
    HealthCheck,
    HealthRequest,
    HealthResponse,
    HealthStatus,
)
from protos.init_faiss_index_pb2 import (
    InitFaissIndexRequest,
    InitFaissIndexResponse,
)
from protos.recipe_pb2 import RecipeRequest, RecipeResponse
from protos.search_recipes_by_ingredients_pb2 import (
    SearchRecipesByIngredientsRecipe,
    SearchRecipesByIngredientsRequest,
    SearchRecipesByIngredientsResponse,
)
from protos.service_pb2_grpc import RecipeSearchServiceServicer


class RecipeSearchServicer(RecipeSearchServiceServicer):
    """Service class to implement the recipe search service"""

    def GetHealth(
        self,
        request: HealthRequest,
        context: grpc.ServicerContext,
    ) -> HealthResponse:
        """Get the health status of the service"""
        status = HealthStatus.HEALTHY
        checks: List[HealthCheck] = []

        # Database
        checks.append(
            HealthCheck(
                name="PostgreSQL",
                status=(
                    HealthStatus.HEALTHY
                    if db.check_health()
                    else HealthStatus.UNHEALTHY
                ),
            )
        )

        # Overall status
        if any(check.status == HealthStatus.UNHEALTHY for check in checks):
            status = HealthStatus.UNHEALTHY
        elif any(check.status == HealthStatus.DEGRADED for check in checks):
            status = HealthStatus.DEGRADED

        return HealthResponse(status=status, checks=checks)

    def GetRecipe(
        self,
        request: RecipeRequest,
        context: grpc.ServicerContext,
    ) -> RecipeResponse:
        """Get the recipe details"""
        try:
            recipe = controllers.get_recipe(request.id)
        except NoResultFound:
            context.abort(
                grpc.StatusCode.NOT_FOUND,
                f"Recipe with ID {request.id} not found",
            )

        return RecipeResponse(
            id=recipe.id,
            name=recipe.name,
            ingredients=recipe.ingredients,
            instructions=recipe.instructions,
            raw=recipe.raw,
        )

    def SearchRecipesByIngredients(
        self,
        request: SearchRecipesByIngredientsRequest,
        context: grpc.ServicerContext,
    ) -> SearchRecipesByIngredientsResponse:
        """Search for recipes given the ingredients"""
        if not request.ingredients:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Ingredients cannot be empty",
            )

        if not request.HasField("limit"):
            request.limit = domain_configs.default_search_limit

        if request.limit <= 0:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Limit must be a positive integer",
            )

        results = controllers.search_recipes_by_ingredients(
            ingredients=request.ingredients,
            limit=request.limit,
        )

        if results is None:
            context.abort(
                grpc.StatusCode.FAILED_PRECONDITION,
                "Embedding model is not initialized",
            )

        recipes = controllers.get_recipes(id for id, _ in results)

        return SearchRecipesByIngredientsResponse(
            recipes=[
                SearchRecipesByIngredientsRecipe(
                    id=id,
                    distance=distance,
                    name=recipe.name,
                )
                for (id, distance), recipe in zip(results, recipes)
            ],
        )

    def AddRecipes(
        self,
        request: AddRecipesRequest,
        context: grpc.ServicerContext,
    ) -> AddRecipesResponse:
        """Add the recipes to the database"""
        if not request.recipes:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Recipes cannot be empty",
            )

        recipes = controllers.add_recipes(
            [
                models.RecipeModel(
                    name=recipe.name,
                    ingredients=list(recipe.ingredients),
                    instructions=list(recipe.instructions),
                    raw=recipe.raw,
                )
                for recipe in request.recipes
            ],
        )

        return AddRecipesResponse(
            recipes=[
                AddRecipesResponseRecipe(
                    id=recipe.id,
                    name=recipe.name,
                    ingredients=recipe.ingredients,
                    instructions=recipe.instructions,
                    raw=recipe.raw,
                )
                for recipe in recipes
            ],
        )

    def InitFaissIndex(
        self,
        request: InitFaissIndexRequest,
        context: grpc.ServicerContext,
    ) -> InitFaissIndexResponse:
        """Initialize the Faiss index"""
        if (
            controllers.get_faiss_index_thread().to_proto().status
            == FaissIndexThreadStatus.IN_PROGRESS
        ):
            context.abort(
                grpc.StatusCode.FAILED_PRECONDITION,
                "Faiss index thread is already in progress",
            )

        count = request.count
        if not request.HasField("count"):
            count = None

        path = request.path
        if not request.HasField("path"):
            path = domain_configs.default_faiss_index_path

        controllers.init_faiss_index(
            count=count,
            path=path,
        )

        return InitFaissIndexResponse()

    def GetFaissIndexThread(
        self,
        request: FaissIndexThreadRequest,
        context: grpc.ServicerContext,
    ) -> FaissIndexThreadResponse:
        """Get the Faiss index thread status"""
        thread = controllers.get_faiss_index_thread()

        return thread.to_proto()

    def ChatByRecipe(
        self,
        request: ChatByRecipeRequest,
        context: grpc.ServicerContext,
    ) -> ChatByRecipeResponse:
        """Chat with the model by recipe"""
        try:
            recipe = controllers.get_recipe(request.id)
        except NoResultFound:
            context.abort(
                grpc.StatusCode.NOT_FOUND,
                f"Recipe with ID {request.id} not found",
            )

        messages = [
            controllers.get_chat_type().get_message_type().from_proto(message)
            for message in request.messages
        ]

        message = controllers.chat_by_recipe(request.name, recipe, messages)

        response_message = message.to_proto()

        return ChatByRecipeResponse(
            message=response_message,
        )
