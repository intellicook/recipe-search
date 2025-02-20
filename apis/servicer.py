from typing import Iterable, List

import grpc
from sqlalchemy.exc import NoResultFound

from configs.domain import configs as domain_configs
from domain import controllers
from infra import db, models
from protos.add_recipes_pb2 import (
    AddRecipesRecipeIngredient,
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
from protos.health_pb2 import (
    HealthCheck,
    HealthRequest,
    HealthResponse,
    HealthStatus,
)
from protos.recipe_nutrition_pb2 import RecipeNutrition
from protos.recipe_pb2 import (
    RecipeRecipeIngredient,
    RecipeRequest,
    RecipeResponse,
)
from protos.reset_data_pb2 import ResetDataRequest, ResetDataResponse
from protos.search_recipes_pb2 import (
    SearchRecipesMatch,
    SearchRecipesRecipe,
    SearchRecipesRecipeDetail,
    SearchRecipesRecipeIngredient,
    SearchRecipesRequest,
    SearchRecipesResponse,
)
from protos.service_pb2_grpc import RecipeSearchServiceServicer
from protos.set_user_profile_pb2 import (
    SetUserProfileRequest,
    SetUserProfileResponse,
)
from protos.user_profile_pb2 import UserProfileRequest, UserProfileResponse


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
            title=recipe.title,
            description=recipe.description,
            ingredients=[
                RecipeRecipeIngredient(
                    name=ingredient.name,
                    quantity=ingredient.quantity,
                    unit=ingredient.unit,
                )
                for ingredient in recipe.ingredients
            ],
            directions=recipe.directions,
            tips=recipe.tips,
            utensils=recipe.utensils,
            nutrition=RecipeNutrition(
                calories=recipe.nutrition.calories.to_proto(),
                fat=recipe.nutrition.fat.to_proto(),
                protein=recipe.nutrition.protein.to_proto(),
                carbs=recipe.nutrition.carbs.to_proto(),
            ),
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
            request.per_page = domain_configs.domain_default_search_per_page

        if request.per_page <= 0:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Per page must be a positive integer",
            )

        if not request.HasField("include_detail"):
            request.include_detail = False

        results = controllers.search_recipes(
            ingredients=request.ingredients,
            username=request.username,
            page=request.page,
            per_page=request.per_page,
            include_detail=request.include_detail,
        )

        return SearchRecipesResponse(
            recipes=[
                SearchRecipesRecipe(
                    id=result.recipe.id,
                    title=result.recipe.title,
                    description=result.recipe.description,
                    ingredients=[
                        SearchRecipesRecipeIngredient(
                            name=ingredient.name,
                            quantity=ingredient.quantity,
                            unit=ingredient.unit,
                        )
                        for ingredient in result.recipe.ingredients
                    ],
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
                            directions=result.recipe.directions,
                            tips=result.recipe.tips,
                            utensils=result.recipe.utensils,
                            nutrition=RecipeNutrition(
                                calories=(
                                    result.recipe.nutrition.calories.to_proto()
                                ),
                                fat=result.recipe.nutrition.fat.to_proto(),
                                protein=(
                                    result.recipe.nutrition.protein.to_proto()
                                ),
                                carbs=(
                                    result.recipe.nutrition.carbs.to_proto()
                                ),
                            ),
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
                    title=recipe.title,
                    description=recipe.description,
                    ingredients=[
                        models.RecipeModelIngredient(
                            name=ingredient.name,
                            quantity=ingredient.quantity,
                            unit=ingredient.unit,
                        )
                        for ingredient in recipe.ingredients
                    ],
                    directions=list(recipe.directions),
                    tips=list(recipe.tips),
                    utensils=list(recipe.utensils),
                    nutrition=models.RecipeModelNutrition(
                        calories=models.RecipeModelNutritionValue.from_proto(
                            recipe.nutrition.calories
                        ),
                        fat=models.RecipeModelNutritionValue.from_proto(
                            recipe.nutrition.fat
                        ),
                        protein=models.RecipeModelNutritionValue.from_proto(
                            recipe.nutrition.protein
                        ),
                        carbs=models.RecipeModelNutritionValue.from_proto(
                            recipe.nutrition.carbs
                        ),
                    ),
                )
                for recipe in request.recipes
            ],
        )

        return AddRecipesResponse(
            recipes=[
                AddRecipesResponseRecipe(
                    id=recipe.id,
                    title=recipe.title,
                    description=recipe.description,
                    ingredients=[
                        AddRecipesRecipeIngredient(
                            name=ingredient.name,
                            quantity=ingredient.quantity,
                            unit=ingredient.unit,
                        )
                        for ingredient in recipe.ingredients
                    ],
                    directions=recipe.directions,
                    tips=recipe.tips,
                    utensils=recipe.utensils,
                    nutrition=RecipeNutrition(
                        calories=recipe.nutrition.calories.to_proto(),
                        fat=recipe.nutrition.fat.to_proto(),
                        protein=recipe.nutrition.protein.to_proto(),
                        carbs=recipe.nutrition.carbs.to_proto(),
                    ),
                )
                for recipe in recipes
            ]
        )

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

    def SetUserProfile(
        self,
        request: SetUserProfileRequest,
        context: grpc.ServicerContext,
    ) -> SetUserProfileResponse:
        """Set the user profile"""
        controllers.set_user_profile(
            models.UserProfileModel(
                username=request.username,
                veggie_identity=(
                    models.UserProfileModelVeggieIdentity.from_proto(
                        request.veggie_identity
                    )
                ),
                prefer=list(request.prefer),
                dislike=list(request.dislike),
            )
        )

        return SetUserProfileResponse(
            username=request.username,
            veggie_identity=request.veggie_identity,
            prefer=request.prefer,
            dislike=request.dislike,
        )

    def GetUserProfile(
        self,
        request: UserProfileRequest,
        context: grpc.ServicerContext,
    ) -> UserProfileResponse:
        """Get the user profile"""
        profile = controllers.get_user_profile(request.username)

        if not profile:
            context.abort(
                grpc.StatusCode.NOT_FOUND,
                f"User profile with username {request.username} not found",
            )

        return UserProfileResponse(
            username=profile.username,
            veggie_identity=profile.veggie_identity.to_proto(),
            prefer=profile.prefer,
            dislike=profile.dislike,
        )
