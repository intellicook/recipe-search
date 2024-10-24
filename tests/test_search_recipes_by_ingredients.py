from unittest import mock

import grpc
import pytest
import pytest_mock

from apis.servicer import RecipeSearchServicer
from configs.domain import configs
from protos.search_recipes_by_ingredients_pb2 import (
    SearchRecipesByIngredientsRecipe,
    SearchRecipesByIngredientsRequest,
    SearchRecipesByIngredientsResponse,
)


def context_abort_mock(code: grpc.StatusCode, message: str):
    raise grpc.RpcError(code, message)


def test_search_recipes_by_ingredients_success(
    mocker: pytest_mock.MockerFixture,
):
    username = "test_username"
    ingredients = ["apple", "banana"]
    limit = 3
    recipes = [1, 2, 3]
    request = SearchRecipesByIngredientsRequest(
        username=username, ingredients=ingredients, limit=limit
    )

    mock_search = mocker.patch(
        "domain.controllers.search_recipes_by_ingredients",
        return_value=recipes,
    )

    context = mocker.MagicMock()

    servicer = RecipeSearchServicer()
    response = servicer.SearchRecipesByIngredients(request, context)

    mock_search.assert_called_once_with(ingredients=ingredients, limit=limit)
    assert response == SearchRecipesByIngredientsResponse(
        recipes=[SearchRecipesByIngredientsRecipe(id=id) for id in recipes]
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
    context.abort = mock.MagicMock(side_effect=context_abort_mock)

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
    recipes = [1, 2, 3]
    request = SearchRecipesByIngredientsRequest(
        username=username, ingredients=ingredients, limit=limit
    )

    mock_search = mocker.patch(
        "domain.controllers.search_recipes_by_ingredients",
        return_value=recipes,
    )

    context = mocker.MagicMock()

    servicer = RecipeSearchServicer()
    response = servicer.SearchRecipesByIngredients(request, context)

    mock_search.assert_called_once_with(
        ingredients=ingredients, limit=configs.default_search_limit
    )
    assert response == SearchRecipesByIngredientsResponse(
        recipes=[SearchRecipesByIngredientsRecipe(id=id) for id in recipes]
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
    context.abort = mock.MagicMock(side_effect=context_abort_mock)

    servicer = RecipeSearchServicer()
    with pytest.raises(grpc.RpcError):
        servicer.SearchRecipesByIngredients(request, context)

    context.abort.assert_called_once_with(
        grpc.StatusCode.INVALID_ARGUMENT,
        "Limit must be a positive integer",
    )
