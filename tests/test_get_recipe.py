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
        id=1,
        title="test_title",
        description="test_description",
        ingredients=[
            models.RecipeModelIngredient(
                name="apple", quantity=1, unit="unit"
            ),
            models.RecipeModelIngredient(
                name="banana", quantity=2, unit="unit"
            ),
        ],
        directions=["step 1", "step 2"],
        tips=["tip 1", "tip 2"],
        utensils=["knife", "spoon"],
        nutrition=models.RecipeModelNutrition(
            calories=models.RecipeModelNutritionValue.high,
            fat=models.RecipeModelNutritionValue.low,
            protein=models.RecipeModelNutritionValue.medium,
            carbs=models.RecipeModelNutritionValue.none,
        ),
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
    assert response.title == recipe.title
    assert response.description == recipe.description
    assert all(
        x.name == y.name and x.quantity == y.quantity and x.unit == y.unit
        for x, y in zip(response.ingredients, recipe.ingredients)
    )
    assert all(x == y for x, y in zip(response.directions, recipe.directions))
    assert all(x == y for x, y in zip(response.tips, recipe.tips))
    assert all(x == y for x, y in zip(response.utensils, recipe.utensils))
    assert response.nutrition.calories == recipe.nutrition.calories.to_proto()
    assert response.nutrition.fat == recipe.nutrition.fat.to_proto()
    assert response.nutrition.protein == recipe.nutrition.protein.to_proto()
    assert response.nutrition.carbs == recipe.nutrition.carbs.to_proto()


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
