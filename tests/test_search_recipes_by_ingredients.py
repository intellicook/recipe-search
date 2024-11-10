import grpc
import pytest
import pytest_mock

from apis.servicer import RecipeSearchServicer
from configs.domain import configs
from infra import models
from protos.search_recipes_by_ingredients_pb2 import (
    SearchRecipesByIngredientsRecipe,
    SearchRecipesByIngredientsRecipeDetail,
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
    mock_get_recipes.assert_called_once_with(mocker.ANY)
    assert all(
        recipe.id in mock_get_recipes.call_args.args[0] for recipe in recipes
    )
    assert response == SearchRecipesByIngredientsResponse(
        recipes=[
            SearchRecipesByIngredientsRecipe(
                id=id,
                name=recipe.name,
            )
            for (id, _), recipe in zip(results, recipes)
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
    context.abort = mocker.MagicMock(side_effect=grpc.RpcError)

    servicer = RecipeSearchServicer()
    with pytest.raises(grpc.RpcError):
        servicer.SearchRecipesByIngredients(request, context)

    context.abort.assert_called_once_with(
        grpc.StatusCode.INVALID_ARGUMENT,
        "Ingredients cannot be empty",
    )


def test_search_recipes_by_ingredients_include_detail(
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
            id=1,
            name="Recipe 1",
            ingredients=["ingredient 1.1", "ingredient 1.2"],
            instructions=["instruction 1.1", "instruction 1.2"],
            raw="raw 1",
        ),
        models.RecipeModel(
            id=2,
            name="Recipe 2",
            ingredients=["ingredient 2.1", "ingredient 2.2"],
            instructions=["instruction 2.1", "instruction 2.2"],
            raw="raw 2",
        ),
        models.RecipeModel(
            id=3,
            name="Recipe 3",
            ingredients=["ingredient 3.1", "ingredient 3.2"],
            instructions=["instruction 3.1", "instruction 3.2"],
            raw="raw 3",
        ),
    ]
    request = SearchRecipesByIngredientsRequest(
        username=username,
        ingredients=ingredients,
        limit=limit,
        include_detail=True,
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
    mock_get_recipes.assert_called_once_with(mocker.ANY)
    assert all(
        recipe.id in mock_get_recipes.call_args.args[0] for recipe in recipes
    )
    assert response == SearchRecipesByIngredientsResponse(
        recipes=[
            SearchRecipesByIngredientsRecipe(
                id=id,
                name=recipe.name,
                detail=SearchRecipesByIngredientsRecipeDetail(
                    ingredients=recipe.ingredients,
                    instructions=recipe.instructions,
                    raw=recipe.raw,
                ),
            )
            for (id, _), recipe in zip(results, recipes)
        ]
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
    mock_get_recipes.assert_called_once_with(mocker.ANY)
    assert response == SearchRecipesByIngredientsResponse(
        recipes=[
            SearchRecipesByIngredientsRecipe(
                id=id,
                name=recipe.name,
            )
            for (id, _), recipe in zip(results, recipes)
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
    context.abort = mocker.MagicMock(side_effect=grpc.RpcError)

    servicer = RecipeSearchServicer()
    with pytest.raises(grpc.RpcError):
        servicer.SearchRecipesByIngredients(request, context)

    context.abort.assert_called_once_with(
        grpc.StatusCode.INVALID_ARGUMENT,
        "Limit must be a positive integer",
    )


def test_search_recipes_by_ingredients_search_not_initialized(
    mocker: pytest_mock.MockerFixture,
):
    username = "test_username"
    ingredients = ["apple", "banana"]
    limit = 3
    request = SearchRecipesByIngredientsRequest(
        username=username, ingredients=ingredients, limit=limit
    )

    mock_search = mocker.patch(
        "domain.controllers.search_recipes_by_ingredients",
        return_value=None,
    )

    context = mocker.MagicMock()
    context.abort = mocker.MagicMock(side_effect=grpc.RpcError)

    servicer = RecipeSearchServicer()
    with pytest.raises(grpc.RpcError):
        servicer.SearchRecipesByIngredients(request, context)

    mock_search.assert_called_once_with(ingredients=ingredients, limit=limit)
    context.abort.assert_called_once_with(
        grpc.StatusCode.FAILED_PRECONDITION,
        "Search model is not initialized",
    )
