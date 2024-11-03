import grpc
import pytest
import pytest_mock

from apis.servicer import RecipeSearchServicer
from protos.add_recipes_pb2 import AddRecipesRecipe, AddRecipesRequest


def test_add_recipes_success(
    mocker: pytest_mock.MockerFixture,
):
    recipes = [
        AddRecipesRecipe(
            name="Recipe 1",
            ingredients=["Ingredient 1", "Ingredient 2"],
            instructions=["Instruction 1", "Instruction 2"],
            raw="Raw 1",
        ),
        AddRecipesRecipe(
            name="Recipe 2",
            ingredients=["Ingredient 3", "Ingredient 4"],
            instructions=["Instruction 3", "Instruction 4"],
            raw="Raw 2",
        ),
    ]
    request = AddRecipesRequest(
        recipes=recipes,
    )

    mock_add_recipes = mocker.patch(
        "domain.controllers.add_recipes",
    )

    context = mocker.MagicMock()

    servicer = RecipeSearchServicer()
    servicer.AddRecipes(request, context)

    mock_add_recipes.assert_called_once_with(mocker.ANY)
    assert (recipe in mock_add_recipes.call_args.args[0] for recipe in recipes)


def test_add_recipes_empty_recipes(
    mocker: pytest_mock.MockerFixture,
):
    recipes = []
    request = AddRecipesRequest(
        recipes=recipes,
    )

    mock_add_recipes = mocker.patch(
        "domain.controllers.add_recipes",
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
