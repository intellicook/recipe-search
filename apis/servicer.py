from typing import List

import grpc
from sqlalchemy.exc import NoResultFound

from configs.domain import configs as domain_configs
from domain import controllers
from infra import db
from protos.health_pb2 import (
    HealthCheck,
    HealthRequest,
    HealthResponse,
    HealthStatus,
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
            name=recipe.name,
            ingredients=recipe.ingredients,
            instructions=recipe.instructions,
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
