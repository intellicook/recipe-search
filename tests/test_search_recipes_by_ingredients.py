import pytest_mock

from apis.servicer import RecipeSearchServicer
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
