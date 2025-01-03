from typing import Iterable, List, Tuple

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
from protos.chat_by_recipe_pb2 import (
    ChatByRecipeMessage,
    ChatByRecipeRequest,
    ChatByRecipeResponse,
    ChatByRecipeStreamContent,
    ChatByRecipeStreamHeader,
    ChatByRecipeStreamResponse,
)
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
from protos.reset_data_pb2 import ResetDataRequest, ResetDataResponse
from protos.search_recipes_by_ingredients_pb2 import (
    SearchRecipesByIngredientsRecipe,
    SearchRecipesByIngredientsRecipeDetail,
    SearchRecipesByIngredientsRequest,
    SearchRecipesByIngredientsResponse,
)
from protos.search_recipes_pb2 import (
    SearchRecipesMatch,
    SearchRecipesRecipe,
    SearchRecipesRecipeDetail,
    SearchRecipesRequest,
    SearchRecipesResponse,
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

        checks.append(
            HealthCheck(
                name="Typesense",
                status=(
                    HealthStatus.HEALTHY
                    if controllers.is_typesense_healthy()
                    else HealthStatus.UNHEALTHY
                ),
            )
        )

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
                "Search model is not initialized",
            )

        results: List[Tuple[int, float]]

        recipes = controllers.get_recipes(id for id, _ in results)

        id_to_recipes = {recipe.id: recipe for recipe in recipes}
        ordered_recipes = [id_to_recipes[id] for id, _ in results]

        include_detail = (
            request.HasField("include_detail") and request.include_detail
        )

        return SearchRecipesByIngredientsResponse(
            recipes=[
                SearchRecipesByIngredientsRecipe(
                    id=id,
                    name=recipe.name,
                    detail=(
                        SearchRecipesByIngredientsRecipeDetail(
                            ingredients=recipe.ingredients,
                            instructions=recipe.instructions,
                            raw=recipe.raw,
                        )
                        if include_detail
                        else None
                    ),
                )
                for (id, _), recipe in zip(results, ordered_recipes)
            ],
        )

    def SearchRecipes(
        self,
        request: SearchRecipesRequest,
        context: grpc.ServicerContext,
    ) -> SearchRecipesResponse:
        """Search for recipes given the query"""
        if not request.ingredients:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Ingredients cannot be empty",
            )

        if not request.HasField("page"):
            request.page = 1

        if request.page <= 0:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Page must be a positive integer",
            )

        if not request.HasField("per_page"):
            request.per_page = domain_configs.default_search_per_page

        if request.per_page <= 0:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Per page must be a positive integer",
            )

        if not request.HasField("include_detail"):
            request.include_detail = False

        results = controllers.search_recipes(
            ingredients=request.ingredients,
            page=request.page,
            per_page=request.per_page,
            include_detail=request.include_detail,
        )

        return SearchRecipesResponse(
            recipes=[
                SearchRecipesRecipe(
                    id=result.recipe.id,
                    name=result.recipe.name,
                    ingredients=result.recipe.ingredients,
                    matches=[
                        SearchRecipesMatch(
                            field=highlight.field.to_proto(),
                            tokens=highlight.tokens,
                            index=highlight.index,
                        )
                        for highlight in result.highlights
                    ],
                    detail=(
                        SearchRecipesRecipeDetail(
                            instructions=result.recipe.instructions,
                            raw=result.recipe.raw,
                        )
                        if request.include_detail
                        else None
                    ),
                )
                for result in results
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
                    raw=recipe.raw if recipe.HasField("raw") else "",
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
            models.ChatMessageModel(
                role=models.ChatRoleModel.from_proto(message.role),
                text=message.text,
            )
            for message in request.messages
        ]

        message = controllers.chat_by_recipe(request.name, recipe, messages)

        return ChatByRecipeResponse(
            message=ChatByRecipeMessage(
                role=message.role.to_proto(),
                text=message.text,
            ),
        )

    def ChatByRecipeStream(
        self,
        request: ChatByRecipeRequest,
        context: grpc.ServicerContext,
    ) -> Iterable[ChatByRecipeStreamResponse]:
        """Chat with the model by recipe and return a stream of messages"""
        try:
            recipe = controllers.get_recipe(request.id)
        except NoResultFound:
            context.abort(
                grpc.StatusCode.NOT_FOUND,
                f"Recipe with ID {request.id} not found",
            )

        messages = [
            models.ChatMessageModel(
                role=models.ChatRoleModel.from_proto(message.role),
                text=message.text,
            )
            for message in request.messages
        ]

        for message in controllers.chat_by_recipe_stream(
            request.name, recipe, messages
        ):
            if isinstance(message, models.ChatStreamHeaderModel):
                yield ChatByRecipeStreamResponse(
                    header=ChatByRecipeStreamHeader(
                        role=message.role.to_proto(),
                    ),
                )
            elif isinstance(message, models.ChatStreamContentModel):
                yield ChatByRecipeStreamResponse(
                    content=ChatByRecipeStreamContent(
                        text=message.text,
                    ),
                )

    def ResetData(
        self,
        request: ResetDataRequest,
        context: grpc.ServicerContext,
    ) -> ResetDataResponse:
        """Reset the data in the database"""
        controllers.reset_data()

        return ResetDataResponse()
