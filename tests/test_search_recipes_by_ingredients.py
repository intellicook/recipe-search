from unittest import mock

import grpc
import pytest
import pytest_mock

from apis.servicer import RecipeSearchServicer
from configs.domain import configs
from infra import models
from protos.search_recipes_by_ingredients_pb2 import (
    SearchRecipesByIngredientsRecipe,
    SearchRecipesByIngredientsRequest,
    SearchRecipesByIngredientsResponse,
)


def test_search_recipes_by_ingredients_success(
    mocker: pytest_mock.MockerFixture,
):
    username = "test_username"
    ingredients = ["apple", "banana"]
    limit = 3
    results = [
        (1, 0.5),
        (2, 0.4),
        (3, 0.3),
    ]
    recipes = [
        models.RecipeModel(
            id=1, name="Recipe 1", ingredients=[], instructions=[]
        ),
        models.RecipeModel(
            id=2, name="Recipe 2", ingredients=[], instructions=[]
        ),
        models.RecipeModel(
            id=3, name="Recipe 3", ingredients=[], instructions=[]
        ),
    ]
    request = SearchRecipesByIngredientsRequest(
        username=username, ingredients=ingredients, limit=limit
    )

    mock_search = mocker.patch(
        "domain.controllers.search_recipes_by_ingredients",
        return_value=results,
    )

    mock_get_recipes = mocker.patch(
        "domain.controllers.get_recipes",
        return_value=recipes,
    )

    context = mocker.MagicMock()

    servicer = RecipeSearchServicer()
    response = servicer.SearchRecipesByIngredients(request, context)

    mock_search.assert_called_once_with(ingredients=ingredients, limit=limit)
    mock_get_recipes.assert_called_once_with(mock.ANY)
    assert all(
        recipe.id in mock_get_recipes.call_args.args[0] for recipe in recipes
    )
    assert response == SearchRecipesByIngredientsResponse(
        recipes=[
            SearchRecipesByIngredientsRecipe(
                id=id,
                distance=distance,
                name=recipe.name,
            )
            for (id, distance), recipe in zip(results, recipes)
        ]
    )


def test_search_recipes_by_ingredients_empty_ingredients(
    mocker: pytest_mock.MockerFixture,
):
    username = "test_username"
    ingredients = []
    limit = 3
    request = SearchRecipesByIngredientsRequest(
        username=username, ingredients=ingredients, limit=limit
    )

    context = mocker.MagicMock()
    context.abort = mock.MagicMock(side_effect=grpc.RpcError)

    servicer = RecipeSearchServicer()
    with pytest.raises(grpc.RpcError):
        servicer.SearchRecipesByIngredients(request, context)

    context.abort.assert_called_once_with(
        grpc.StatusCode.INVALID_ARGUMENT,
        "Ingredients cannot be empty",
    )


def test_search_recipes_by_ingredients_limit_null(
    mocker: pytest_mock.MockerFixture,
):
    username = "test_username"
    ingredients = ["apple", "banana"]
    limit = None
    results = [
        (1, 0.5),
        (2, 0.4),
        (3, 0.3),
    ]
    recipes = [
        models.RecipeModel(
            id=1, name="Recipe 1", ingredients=[], instructions=[]
        ),
        models.RecipeModel(
            id=2, name="Recipe 2", ingredients=[], instructions=[]
        ),
        models.RecipeModel(
            id=3, name="Recipe 3", ingredients=[], instructions=[]
        ),
    ]
    request = SearchRecipesByIngredientsRequest(
        username=username, ingredients=ingredients, limit=limit
    )

    mock_search = mocker.patch(
        "domain.controllers.search_recipes_by_ingredients",
        return_value=results,
    )

    mock_get_recipes = mocker.patch(
        "domain.controllers.get_recipes",
        return_value=recipes,
    )

    context = mocker.MagicMock()

    servicer = RecipeSearchServicer()
    response = servicer.SearchRecipesByIngredients(request, context)

    mock_search.assert_called_once_with(
        ingredients=ingredients, limit=configs.default_search_limit
    )
    mock_get_recipes.assert_called_once_with(mock.ANY)
    assert response == SearchRecipesByIngredientsResponse(
        recipes=[
            SearchRecipesByIngredientsRecipe(
                id=id,
                distance=distance,
                name=recipe.name,
            )
            for (id, distance), recipe in zip(results, recipes)
        ]
    )


def test_search_recipes_by_ingredients_limit_zero(
    mocker: pytest_mock.MockerFixture,
):
    username = "test_username"
    ingredients = ["apple", "banana"]
    limit = 0
    request = SearchRecipesByIngredientsRequest(
        username=username, ingredients=ingredients, limit=limit
    )

    context = mocker.MagicMock()
    context.abort = mock.MagicMock(side_effect=grpc.RpcError)

    servicer = RecipeSearchServicer()
    with pytest.raises(grpc.RpcError):
        servicer.SearchRecipesByIngredients(request, context)

    context.abort.assert_called_once_with(
        grpc.StatusCode.INVALID_ARGUMENT,
        "Limit must be a positive integer",
    )
