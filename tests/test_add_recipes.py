import grpc
import pytest
import pytest_mock

from apis.servicer import RecipeSearchServicer
from infra.models import RecipeModel
from protos.add_recipes_pb2 import (
    AddRecipesRequest,
    AddRecipesRequestRecipe,
    AddRecipesResponse,
    AddRecipesResponseRecipe,
)


def test_add_recipes_success(
    mocker: pytest_mock.MockerFixture,
):
    recipes = [
        RecipeModel(
            id=1,
            name="test_name",
            ingredients=["apple", "banana"],
            instructions=["step 1", "step 2"],
            raw="raw recipe",
        ),
        RecipeModel(
            id=2,
            name="test_name",
            ingredients=["apple", "banana"],
            instructions=["step 1", "step 2"],
            raw="raw recipe",
        ),
    ]
    request_recipes = [
        AddRecipesRequestRecipe(
            name=recipe.name,
            ingredients=recipe.ingredients,
            instructions=recipe.instructions,
            raw=recipe.raw,
        )
        for recipe in recipes
    ]
    response_recipes = [
        AddRecipesResponseRecipe(
            id=recipe.id,
            name=recipe.name,
            ingredients=recipe.ingredients,
            instructions=recipe.instructions,
            raw=recipe.raw,
        )
        for recipe in recipes
    ]
    request = AddRecipesRequest(
        recipes=request_recipes,
    )
    expected_response = AddRecipesResponse(
        recipes=response_recipes,
    )

    mock_add_recipes = mocker.patch(
        "domain.controllers.add_recipes",
        return_value=recipes,
    )

    context = mocker.MagicMock()

    servicer = RecipeSearchServicer()
    response = servicer.AddRecipes(request, context)

    mock_add_recipes.assert_called_once_with(mocker.ANY)
    assert (recipe in mock_add_recipes.call_args.args[0] for recipe in recipes)
    assert response == expected_response


def test_add_recipes_no_recipe_raw(
    mocker: pytest_mock.MockerFixture,
):
    recipes = [
        RecipeModel(
            id=1,
            name="test_name",
            ingredients=["apple", "banana"],
            instructions=["step 1", "step 2"],
            raw="",
        ),
        RecipeModel(
            id=2,
            name="test_name",
            ingredients=["apple", "banana"],
            instructions=["step 1", "step 2"],
            raw="",
        ),
    ]
    request_recipes = [
        AddRecipesRequestRecipe(
            name=recipe.name,
            ingredients=recipe.ingredients,
            instructions=recipe.instructions,
        )
        for recipe in recipes
    ]
    response_recipes = [
        AddRecipesResponseRecipe(
            id=recipe.id,
            name=recipe.name,
            ingredients=recipe.ingredients,
            instructions=recipe.instructions,
            raw=recipe.raw,
        )
        for recipe in recipes
    ]
    request = AddRecipesRequest(
        recipes=request_recipes,
    )
    expected_response = AddRecipesResponse(
        recipes=response_recipes,
    )

    mock_add_recipes = mocker.patch(
        "domain.controllers.add_recipes",
        return_value=recipes,
    )

    context = mocker.MagicMock()

    servicer = RecipeSearchServicer()
    response = servicer.AddRecipes(request, context)

    mock_add_recipes.assert_called_once_with(mocker.ANY)
    assert (recipe in mock_add_recipes.call_args.args[0] for recipe in recipes)
    assert response == expected_response


def test_add_recipes_empty_recipes(
    mocker: pytest_mock.MockerFixture,
):
    recipes = []
    request = AddRecipesRequest(
        recipes=recipes,
    )

    mock_add_recipes = mocker.patch(
        "domain.controllers.add_recipes",
        return_value=recipes,
    )

    context = mocker.MagicMock()
    context.abort = mocker.MagicMock(side_effect=grpc.RpcError)

    servicer = RecipeSearchServicer()
    with pytest.raises(grpc.RpcError):
        servicer.AddRecipes(request, context)

    mock_add_recipes.assert_not_called()
    context.abort.assert_called_once_with(
        grpc.StatusCode.INVALID_ARGUMENT,
        "Recipes cannot be empty",
    )
