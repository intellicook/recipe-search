import grpc
import pytest
import pytest_mock
from sqlalchemy.exc import NoResultFound

from apis.servicer import RecipeSearchServicer
from infra import models
from protos.recipe_pb2 import RecipeRequest


def test_get_recipe_success(
    mocker: pytest_mock.MockerFixture,
):
    id = 1
    recipe = models.RecipeModel(
        id=id,
        name="Recipe 1",
        ingredients=["apple", "banana"],
        instructions=["step 1", "step 2"],
        raw="raw recipe",
    )
    request = RecipeRequest(
        id=id,
    )

    mock_get_recipe = mocker.patch(
        "domain.controllers.get_recipe",
        return_value=recipe,
    )

    context = mocker.MagicMock()

    servicer = RecipeSearchServicer()
    response = servicer.GetRecipe(request, context)

    mock_get_recipe.assert_called_once_with(id)
    assert response.name == recipe.name
    assert all(
        x == y for x, y in zip(response.ingredients, recipe.ingredients)
    )
    assert all(
        x == y for x, y in zip(response.instructions, recipe.instructions)
    )
    assert response.raw == recipe.raw


def test_get_recipe_not_found(
    mocker: pytest_mock.MockerFixture,
):
    id = 1
    request = RecipeRequest(
        id=id,
    )

    mock_get_recipe = mocker.patch(
        "domain.controllers.get_recipe",
        side_effect=NoResultFound(),
    )

    context = mocker.MagicMock()
    context.abort = mocker.MagicMock(side_effect=grpc.RpcError)

    servicer = RecipeSearchServicer()
    with pytest.raises(grpc.RpcError):
        servicer.GetRecipe(request, context)

    mock_get_recipe.assert_called_once_with(id)
    context.abort.assert_called_once_with(
        grpc.StatusCode.NOT_FOUND,
        f"Recipe with ID {id} not found",
    )
