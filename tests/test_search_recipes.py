import grpc
import pytest
import pytest_mock

from apis.servicer import RecipeSearchServicer
from configs.domain import configs
from infra import models
from protos.search_recipes_pb2 import (
    SearchRecipesRecipe,
    SearchRecipesRecipeDetail,
    SearchRecipesRequest,
    SearchRecipesResponse,
)


def test_search_recipes_success(
    mocker: pytest_mock.MockerFixture,
):
    username = "test_username"
    ingredients = ["apple", "banana"]
    page = 1
    per_page = 3
    recipes = [
        models.RecipeModel(id=1, name="Recipe 1", ingredients=[]),
        models.RecipeModel(id=2, name="Recipe 2", ingredients=[]),
        models.RecipeModel(id=3, name="Recipe 3", ingredients=[]),
    ]
    request = SearchRecipesRequest(
        username=username,
        ingredients=ingredients,
        page=page,
        per_page=per_page,
    )

    mock_search = mocker.patch(
        "domain.controllers.search_recipes",
        return_value=recipes,
    )

    context = mocker.MagicMock()

    servicer = RecipeSearchServicer()
    response = servicer.SearchRecipes(request, context)

    mock_search.assert_called_once_with(
        ingredients=ingredients,
        page=page,
        per_page=per_page,
        include_detail=False,
    )
    assert response == SearchRecipesResponse(
        recipes=[
            SearchRecipesRecipe(
                id=recipe.id,
                name=recipe.name,
                ingredients=recipe.ingredients,
            )
            for recipe in recipes
        ]
    )


def test_search_recipes_empty_ingredients(
    mocker: pytest_mock.MockerFixture,
):
    username = "test_username"
    ingredients = []
    page = 1
    per_page = 3
    request = SearchRecipesRequest(
        username=username,
        ingredients=ingredients,
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
    page = 1
    per_page = 3
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
    request = SearchRecipesRequest(
        username=username,
        ingredients=ingredients,
        page=page,
        per_page=per_page,
        include_detail=True,
    )

    mock_search = mocker.patch(
        "domain.controllers.search_recipes",
        return_value=recipes,
    )

    context = mocker.MagicMock()

    servicer = RecipeSearchServicer()
    response = servicer.SearchRecipes(request, context)

    mock_search.assert_called_once_with(
        ingredients=ingredients,
        page=page,
        per_page=per_page,
        include_detail=True,
    )
    assert response == SearchRecipesResponse(
        recipes=[
            SearchRecipesRecipe(
                id=recipe.id,
                name=recipe.name,
                ingredients=recipe.ingredients,
                detail=SearchRecipesRecipeDetail(
                    instructions=recipe.instructions,
                    raw=recipe.raw,
                ),
            )
            for recipe in recipes
        ]
    )


def test_search_recipes_page_and_per_page_null(
    mocker: pytest_mock.MockerFixture,
):
    username = "test_username"
    ingredients = ["apple", "banana"]
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
    request = SearchRecipesRequest(
        username=username,
        ingredients=ingredients,
    )

    mock_search = mocker.patch(
        "domain.controllers.search_recipes",
        return_value=recipes,
    )

    context = mocker.MagicMock()

    servicer = RecipeSearchServicer()
    response = servicer.SearchRecipes(request, context)

    mock_search.assert_called_once_with(
        ingredients=ingredients,
        page=1,
        per_page=configs.default_search_per_page,
        include_detail=False,
    )
    assert response == SearchRecipesResponse(
        recipes=[
            SearchRecipesRecipe(
                id=recipe.id,
                name=recipe.name,
                ingredients=recipe.ingredients,
            )
            for recipe in recipes
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
