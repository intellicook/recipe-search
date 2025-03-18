import grpc
import pytest
import pytest_mock
from sqlalchemy.exc import NoResultFound

from apis.servicer import RecipeSearchServicer
from infra import models
from protos.chat_by_recipe_pb2 import (
    ChatByRecipeMessage,
    ChatByRecipeRequest,
    ChatByRecipeRole,
    ChatByRecipeStreamContent,
    ChatByRecipeStreamHeader,
    ChatByRecipeStreamResponse,
)


def test_chat_by_recipe_stream_success(mocker: pytest_mock.MockerFixture):
    id = 1
    username = "test_username"
    name = "test_name"
    messages = [
        {
            "role": "USER",
            "text": "user text",
        },
        {
            "role": "ASSISTANT",
            "text": "assistant text",
        },
    ]
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
    request = ChatByRecipeRequest(
        id=id,
        username=username,
        name=name,
        messages=(
            ChatByRecipeMessage(
                role=(
                    ChatByRecipeRole.USER
                    if message["role"] == "USER"
                    else ChatByRecipeRole.ASSISTANT
                ),
                text=message["text"],
            )
            for message in messages
        ),
    )
    expected_responses = [
        ChatByRecipeStreamResponse(
            header=ChatByRecipeStreamHeader(
                role=ChatByRecipeRole.ASSISTANT,
            ),
        ),
        ChatByRecipeStreamResponse(
            content=ChatByRecipeStreamContent(
                text="assistant",
            ),
        ),
        ChatByRecipeStreamResponse(
            content=ChatByRecipeStreamContent(
                text=" response",
            ),
        ),
    ]

    mocker.patch(
        "domain.controllers.get_recipe",
        return_value=recipe,
    )
    mock_chat = mocker.patch(
        "domain.controllers.chat_by_recipe_stream",
        return_value=(
            models.ChatStreamHeaderModel(
                role=models.ChatRoleModel.from_proto(
                    expected_responses[0].header.role
                ),
            ),
            models.ChatStreamContentModel(
                text=expected_responses[1].content.text,
            ),
            models.ChatStreamContentModel(
                text=expected_responses[2].content.text,
            ),
        ),
    )

    context = mocker.MagicMock()

    servicer = RecipeSearchServicer()
    for response in servicer.ChatByRecipeStream(request, context):
        expected_response = expected_responses.pop(0)

        if response.WhichOneof("response") == "header":
            assert response.header.role == expected_response.header.role
        elif response.WhichOneof("response") == "content":
            assert response.content.text == expected_response.content.text

    mock_chat.assert_called_once_with(
        name,
        username,
        recipe,
        mocker.ANY,
    )
    assert all(
        req == arg for req, arg in zip(request.messages, mock_chat.args[2])
    )


def test_chat_by_recipe_stream_recipe_not_found(
    mocker: pytest_mock.MockerFixture,
):
    id = 1
    username = "test_username"
    name = "test_name"
    messages = [
        {
            "role": "USER",
            "text": "user text",
        },
        {
            "role": "ASSISTANT",
            "text": "assistant text",
        },
    ]
    request = ChatByRecipeRequest(
        id=id,
        username=username,
        name=name,
        messages=(
            ChatByRecipeMessage(
                role=(
                    ChatByRecipeRole.USER
                    if message["role"] == "USER"
                    else ChatByRecipeRole.ASSISTANT
                ),
                text=message["text"],
            )
            for message in messages
        ),
    )

    mock_get_recipe = mocker.patch(
        "domain.controllers.get_recipe",
        side_effect=NoResultFound(),
    )

    context = mocker.MagicMock()
    context.abort = mocker.MagicMock(side_effect=grpc.RpcError)

    servicer = RecipeSearchServicer()
    with pytest.raises(grpc.RpcError):
        next(servicer.ChatByRecipeStream(request, context))

    mock_get_recipe.assert_called_once_with(id)
    context.abort.assert_called_once_with(
        grpc.StatusCode.NOT_FOUND,
        f"Recipe with ID {id} not found",
    )
