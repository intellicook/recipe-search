import grpc
import pytest
import pytest_mock

from apis.servicer import RecipeSearchServicer
from configs.domain import configs
from infra import models
from protos.search_recipes_pb2 import (
    SearchRecipesMatch,
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
    results = [
        models.TypesenseResult(
            recipe=models.RecipeModel(id=1, name="Recipe 1", ingredients=[]),
            highlights=[
                models.TypesenseResultHighlight(
                    field=models.TypesenseResultHighlight.Field.NAME,
                    tokens=["apple"],
                )
            ],
        ),
        models.TypesenseResult(
            recipe=models.RecipeModel(id=2, name="Recipe 2", ingredients=[]),
            highlights=[
                models.TypesenseResultHighlight(
                    field=models.TypesenseResultHighlight.Field.NAME,
                    tokens=["banana"],
                )
            ],
        ),
        models.TypesenseResult(
            recipe=models.RecipeModel(id=3, name="Recipe 3", ingredients=[]),
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
        page=page,
        per_page=per_page,
        include_detail=False,
    )
    assert response == SearchRecipesResponse(
        recipes=[
            SearchRecipesRecipe(
                id=result.recipe.id,
                name=result.recipe.name,
                ingredients=result.recipe.ingredients,
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
    results = [
        models.TypesenseResult(
            recipe=models.RecipeModel(
                id=1,
                name="Recipe 1",
                ingredients=["ingredient 1.1", "ingredient 1.2"],
                instructions=["instruction 1.1", "instruction 1.2"],
                raw="raw 1",
            ),
            highlights=[
                models.TypesenseResultHighlight(
                    field=models.TypesenseResultHighlight.Field.NAME,
                    tokens=["apple"],
                )
            ],
        ),
        models.TypesenseResult(
            recipe=models.RecipeModel(
                id=2,
                name="Recipe 2",
                ingredients=["ingredient 2.1", "ingredient 2.2"],
                instructions=["instruction 2.1", "instruction 2.2"],
                raw="raw 2",
            ),
            highlights=[
                models.TypesenseResultHighlight(
                    field=models.TypesenseResultHighlight.Field.NAME,
                    tokens=["banana"],
                )
            ],
        ),
        models.TypesenseResult(
            recipe=models.RecipeModel(
                id=3,
                name="Recipe 3",
                ingredients=["ingredient 3.1", "ingredient 3.2"],
                instructions=["instruction 3.1", "instruction 3.2"],
                raw="raw 3",
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
        page=page,
        per_page=per_page,
        include_detail=True,
    )
    assert response == SearchRecipesResponse(
        recipes=[
            SearchRecipesRecipe(
                id=result.recipe.id,
                name=result.recipe.name,
                ingredients=result.recipe.ingredients,
                matches=[
                    SearchRecipesMatch(
                        field=match.field.to_proto(),
                        tokens=match.tokens,
                        index=match.index,
                    )
                    for match in result.highlights
                ],
                detail=SearchRecipesRecipeDetail(
                    instructions=result.recipe.instructions,
                    raw=result.recipe.raw,
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
            recipe=models.RecipeModel(id=1, name="Recipe 1", ingredients=[]),
            highlights=[
                models.TypesenseResultHighlight(
                    field=models.TypesenseResultHighlight.Field.NAME,
                    tokens=["apple"],
                )
            ],
        ),
        models.TypesenseResult(
            recipe=models.RecipeModel(id=2, name="Recipe 2", ingredients=[]),
            highlights=[
                models.TypesenseResultHighlight(
                    field=models.TypesenseResultHighlight.Field.NAME,
                    tokens=["banana"],
                )
            ],
        ),
        models.TypesenseResult(
            recipe=models.RecipeModel(id=3, name="Recipe 3", ingredients=[]),
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
        page=1,
        per_page=configs.default_search_per_page,
        include_detail=False,
    )
    assert response == SearchRecipesResponse(
        recipes=[
            SearchRecipesRecipe(
                id=result.recipe.id,
                name=result.recipe.name,
                ingredients=result.recipe.ingredients,
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
