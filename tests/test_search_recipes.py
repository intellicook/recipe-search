import grpc
import pytest
import pytest_mock

from apis.servicer import RecipeSearchServicer
from configs.domain import configs
from infra import models
from protos.recipe_nutrition_pb2 import RecipeNutrition
from protos.search_recipes_pb2 import (
    SearchRecipesMatch,
    SearchRecipesRecipe,
    SearchRecipesRecipeDetail,
    SearchRecipesRecipeIngredient,
    SearchRecipesRequest,
    SearchRecipesResponse,
)


def test_search_recipes_success(
    mocker: pytest_mock.MockerFixture,
):
    username = "test_username"
    ingredients = ["apple", "banana"]
    extra_terms = "extra_terms"
    page = 1
    per_page = 3
    results = [
        models.TypesenseResult(
            recipe=models.RecipeModel(
                id=1,
                title="test_title 1",
                description="test_description 1",
                ingredients=[
                    models.RecipeModelIngredient(name="apple"),
                    models.RecipeModelIngredient(name="banana"),
                ],
            ),
            highlights=[
                models.TypesenseResultHighlight(
                    field=models.TypesenseResultHighlight.Field.TITLE,
                    tokens=["apple"],
                )
            ],
        ),
        models.TypesenseResult(
            recipe=models.RecipeModel(
                id=2,
                title="test_title 2",
                description="test_description 2",
                ingredients=[
                    models.RecipeModelIngredient(name="apple"),
                    models.RecipeModelIngredient(name="banana"),
                ],
            ),
            highlights=[
                models.TypesenseResultHighlight(
                    field=models.TypesenseResultHighlight.Field.DESCRIPTION,
                    tokens=["banana"],
                )
            ],
        ),
        models.TypesenseResult(
            recipe=models.RecipeModel(
                id=3,
                title="test_title 3",
                description="test_description 3",
                ingredients=[
                    models.RecipeModelIngredient(name="apple"),
                    models.RecipeModelIngredient(name="banana"),
                ],
            ),
            highlights=[
                models.TypesenseResultHighlight(
                    field=models.TypesenseResultHighlight.Field.INGREDIENTS,
                    tokens=["banana"],
                    index=1,
                )
            ],
        ),
    ]
    request = SearchRecipesRequest(
        username=username,
        ingredients=ingredients,
        extra_terms=extra_terms,
        page=page,
        per_page=per_page,
    )

    mock_search = mocker.patch(
        "domain.controllers.search_recipes",
        return_value=results,
    )

    context = mocker.MagicMock()

    servicer = RecipeSearchServicer()
    response = servicer.SearchRecipes(request, context)

    mock_search.assert_called_once_with(
        ingredients=ingredients,
        username=username,
        extra_terms=extra_terms,
        page=page,
        per_page=per_page,
        include_detail=False,
    )
    assert response == SearchRecipesResponse(
        recipes=[
            SearchRecipesRecipe(
                id=result.recipe.id,
                title=result.recipe.title,
                description=result.recipe.description,
                ingredients=[
                    SearchRecipesRecipeIngredient(name=ingredient.name)
                    for ingredient in result.recipe.ingredients
                ],
                matches=[
                    SearchRecipesMatch(
                        field=match.field.to_proto(),
                        tokens=match.tokens,
                        index=match.index,
                    )
                    for match in result.highlights
                ],
            )
            for result in results
        ]
    )


def test_search_recipes_empty_ingredients(
    mocker: pytest_mock.MockerFixture,
):
    username = "test_username"
    ingredients = []
    extra_terms = "extra_terms"
    page = 1
    per_page = 3
    request = SearchRecipesRequest(
        username=username,
        ingredients=ingredients,
        extra_terms=extra_terms,
        page=page,
        per_page=per_page,
    )

    context = mocker.MagicMock()
    context.abort = mocker.MagicMock(side_effect=grpc.RpcError)

    servicer = RecipeSearchServicer()
    with pytest.raises(grpc.RpcError):
        servicer.SearchRecipes(request, context)

    context.abort.assert_called_once_with(
        grpc.StatusCode.INVALID_ARGUMENT,
        "Ingredients cannot be empty",
    )


def test_search_recipes_include_detail(
    mocker: pytest_mock.MockerFixture,
):
    username = "test_username"
    ingredients = ["apple", "banana"]
    extra_terms = "extra_terms"
    page = 1
    per_page = 3
    results = [
        models.TypesenseResult(
            recipe=models.RecipeModel(
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
                directions=["step 1.1", "step 1.2"],
                tips=["tip 1.1", "tip 1.2"],
                utensils=["knife", "spoon"],
                nutrition=models.RecipeModelNutrition(
                    calories=models.RecipeModelNutritionValue.high,
                    fat=models.RecipeModelNutritionValue.low,
                    protein=models.RecipeModelNutritionValue.medium,
                    carbs=models.RecipeModelNutritionValue.none,
                ),
            ),
            highlights=[
                models.TypesenseResultHighlight(
                    field=models.TypesenseResultHighlight.Field.TITLE,
                    tokens=["apple"],
                )
            ],
        ),
        models.TypesenseResult(
            recipe=models.RecipeModel(
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
                directions=["step 2.1", "step 2.2"],
                tips=["tip 2.1", "tip 2.2"],
                utensils=["knife", "spoon"],
                nutrition=models.RecipeModelNutrition(
                    calories=models.RecipeModelNutritionValue.high,
                    fat=models.RecipeModelNutritionValue.low,
                    protein=models.RecipeModelNutritionValue.medium,
                    carbs=models.RecipeModelNutritionValue.none,
                ),
            ),
            highlights=[
                models.TypesenseResultHighlight(
                    field=models.TypesenseResultHighlight.Field.DESCRIPTION,
                    tokens=["banana"],
                )
            ],
        ),
        models.TypesenseResult(
            recipe=models.RecipeModel(
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
                directions=["step 3.1", "step 3.2"],
                tips=["tip 3.1", "tip 3.2"],
                utensils=["knife", "spoon"],
                nutrition=models.RecipeModelNutrition(
                    calories=models.RecipeModelNutritionValue.high,
                    fat=models.RecipeModelNutritionValue.low,
                    protein=models.RecipeModelNutritionValue.medium,
                    carbs=models.RecipeModelNutritionValue.none,
                ),
            ),
            highlights=[
                models.TypesenseResultHighlight(
                    field=models.TypesenseResultHighlight.Field.INGREDIENTS,
                    tokens=["banana"],
                )
            ],
        ),
    ]
    request = SearchRecipesRequest(
        username=username,
        ingredients=ingredients,
        extra_terms=extra_terms,
        page=page,
        per_page=per_page,
        include_detail=True,
    )

    mock_search = mocker.patch(
        "domain.controllers.search_recipes",
        return_value=results,
    )

    context = mocker.MagicMock()

    servicer = RecipeSearchServicer()
    response = servicer.SearchRecipes(request, context)

    mock_search.assert_called_once_with(
        ingredients=ingredients,
        username=username,
        extra_terms=extra_terms,
        page=page,
        per_page=per_page,
        include_detail=True,
    )
    assert response == SearchRecipesResponse(
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
                        field=match.field.to_proto(),
                        tokens=match.tokens,
                        index=match.index,
                    )
                    for match in result.highlights
                ],
                detail=SearchRecipesRecipeDetail(
                    directions=result.recipe.directions,
                    tips=result.recipe.tips,
                    utensils=result.recipe.utensils,
                    nutrition=RecipeNutrition(
                        calories=result.recipe.nutrition.calories.to_proto(),
                        fat=result.recipe.nutrition.fat.to_proto(),
                        protein=result.recipe.nutrition.protein.to_proto(),
                        carbs=result.recipe.nutrition.carbs.to_proto(),
                    ),
                ),
            )
            for result in results
        ]
    )


def test_search_recipes_page_and_per_page_null(
    mocker: pytest_mock.MockerFixture,
):
    username = "test_username"
    ingredients = ["apple", "banana"]
    results = [
        models.TypesenseResult(
            recipe=models.RecipeModel(
                id=1,
                title="test_title 1",
                description="test_description 1",
                ingredients=[
                    models.RecipeModelIngredient(name="apple"),
                    models.RecipeModelIngredient(name="banana"),
                ],
            ),
            highlights=[
                models.TypesenseResultHighlight(
                    field=models.TypesenseResultHighlight.Field.TITLE,
                    tokens=["apple"],
                )
            ],
        ),
        models.TypesenseResult(
            recipe=models.RecipeModel(
                id=2,
                title="test_title 2",
                description="test_description 2",
                ingredients=[
                    models.RecipeModelIngredient(name="apple"),
                    models.RecipeModelIngredient(name="banana"),
                ],
            ),
            highlights=[
                models.TypesenseResultHighlight(
                    field=models.TypesenseResultHighlight.Field.DESCRIPTION,
                    tokens=["banana"],
                )
            ],
        ),
        models.TypesenseResult(
            recipe=models.RecipeModel(
                id=3,
                title="test_title 3",
                description="test_description 3",
                ingredients=[
                    models.RecipeModelIngredient(name="apple"),
                    models.RecipeModelIngredient(name="banana"),
                ],
            ),
            highlights=[
                models.TypesenseResultHighlight(
                    field=models.TypesenseResultHighlight.Field.INGREDIENTS,
                    tokens=["banana"],
                    index=1,
                )
            ],
        ),
    ]
    request = SearchRecipesRequest(
        username=username,
        ingredients=ingredients,
    )

    mock_search = mocker.patch(
        "domain.controllers.search_recipes",
        return_value=results,
    )

    context = mocker.MagicMock()

    servicer = RecipeSearchServicer()
    response = servicer.SearchRecipes(request, context)

    mock_search.assert_called_once_with(
        ingredients=ingredients,
        username=username,
        extra_terms=None,
        page=1,
        per_page=configs.domain_default_search_per_page,
        include_detail=False,
    )
    assert response == SearchRecipesResponse(
        recipes=[
            SearchRecipesRecipe(
                id=result.recipe.id,
                title=result.recipe.title,
                description=result.recipe.description,
                ingredients=[
                    SearchRecipesRecipeIngredient(name=ingredient.name)
                    for ingredient in result.recipe.ingredients
                ],
                matches=[
                    SearchRecipesMatch(
                        field=match.field.to_proto(),
                        tokens=match.tokens,
                        index=match.index,
                    )
                    for match in result.highlights
                ],
            )
            for result in results
        ]
    )


def test_search_recipes_page_zero(
    mocker: pytest_mock.MockerFixture,
):
    username = "test_username"
    ingredients = ["apple", "banana"]
    page = 0
    request = SearchRecipesRequest(
        username=username, ingredients=ingredients, page=page
    )

    context = mocker.MagicMock()
    context.abort = mocker.MagicMock(side_effect=grpc.RpcError)

    servicer = RecipeSearchServicer()
    with pytest.raises(grpc.RpcError):
        servicer.SearchRecipes(request, context)

    context.abort.assert_called_once_with(
        grpc.StatusCode.INVALID_ARGUMENT,
        "Page must be a positive integer",
    )


def test_search_recipes_per_page_zero(
    mocker: pytest_mock.MockerFixture,
):
    username = "test_username"
    ingredients = ["apple", "banana"]
    per_page = 0
    request = SearchRecipesRequest(
        username=username, ingredients=ingredients, per_page=per_page
    )

    context = mocker.MagicMock()
    context.abort = mocker.MagicMock(side_effect=grpc.RpcError)

    servicer = RecipeSearchServicer()
    with pytest.raises(grpc.RpcError):
        servicer.SearchRecipes(request, context)

    context.abort.assert_called_once_with(
        grpc.StatusCode.INVALID_ARGUMENT,
        "Per page must be a positive integer",
    )
