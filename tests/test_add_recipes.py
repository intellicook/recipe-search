import grpc
import pytest
import pytest_mock

from apis.servicer import RecipeSearchServicer
from infra.models import (
    RecipeModel,
    RecipeModelIngredient,
    RecipeModelNutrition,
    RecipeModelNutritionValue,
)
from protos.add_recipes_pb2 import (
    AddRecipesRecipeIngredient,
    AddRecipesRequest,
    AddRecipesRequestRecipe,
    AddRecipesResponse,
    AddRecipesResponseRecipe,
)
from protos.recipe_nutrition_pb2 import RecipeNutrition


def test_add_recipes_success(
    mocker: pytest_mock.MockerFixture,
):
    recipes = [
        RecipeModel(
            id=1,
            title="test_title",
            description="test_description",
            ingredients=[
                RecipeModelIngredient(name="apple", quantity=1, unit="unit"),
                RecipeModelIngredient(name="banana", quantity=2, unit="unit"),
            ],
            directions=["step 1", "step 2"],
            tips=["tip 1", "tip 2"],
            utensils=["knife", "spoon"],
            nutrition=RecipeModelNutrition(
                calories=RecipeModelNutritionValue.high,
                fat=RecipeModelNutritionValue.low,
                protein=RecipeModelNutritionValue.medium,
                carbs=RecipeModelNutritionValue.none,
            ),
        ),
        RecipeModel(
            id=2,
            title="test_title",
            description="test_description",
            ingredients=[
                RecipeModelIngredient(name="apple", quantity=1, unit="unit"),
                RecipeModelIngredient(name="banana", quantity=2, unit="unit"),
            ],
            directions=["step 1", "step 2"],
            tips=["tip 1", "tip 2"],
            utensils=["knife", "spoon"],
            nutrition=RecipeModelNutrition(
                calories=RecipeModelNutritionValue.high,
                fat=RecipeModelNutritionValue.low,
                protein=RecipeModelNutritionValue.medium,
                carbs=RecipeModelNutritionValue.none,
            ),
        ),
    ]
    request_recipes = [
        AddRecipesRequestRecipe(
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
    response_recipes = [
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
            title="test_title",
            description="test_description",
            ingredients=[
                RecipeModelIngredient(name="apple", quantity=1, unit="unit"),
                RecipeModelIngredient(name="banana", quantity=2, unit="unit"),
            ],
            directions=["step 1", "step 2"],
            tips=["tip 1", "tip 2"],
            utensils=["knife", "spoon"],
            nutrition=RecipeModelNutrition(
                calories=RecipeModelNutritionValue.high,
                fat=RecipeModelNutritionValue.low,
                protein=RecipeModelNutritionValue.medium,
                carbs=RecipeModelNutritionValue.none,
            ),
        ),
        RecipeModel(
            id=2,
            title="test_title",
            description="test_description",
            ingredients=[
                RecipeModelIngredient(name="apple", quantity=1, unit="unit"),
                RecipeModelIngredient(name="banana", quantity=2, unit="unit"),
            ],
            directions=["step 1", "step 2"],
            tips=["tip 1", "tip 2"],
            utensils=["knife", "spoon"],
            nutrition=RecipeModelNutrition(
                calories=RecipeModelNutritionValue.high,
                fat=RecipeModelNutritionValue.low,
                protein=RecipeModelNutritionValue.medium,
                carbs=RecipeModelNutritionValue.none,
            ),
        ),
    ]
    request_recipes = [
        AddRecipesRequestRecipe(
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
    response_recipes = [
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
