import grpc
import pytest
import pytest_mock
from sqlalchemy.exc import NoResultFound

from apis.servicer import RecipeSearchServicer
from infra import models
from protos.chat_by_recipe_pb2 import (
    ChatByRecipeMessage,
    ChatByRecipeRequest,
    ChatByRecipeResponse,
    ChatByRecipeRole,
)


def test_chat_by_recipe_success(mocker: pytest_mock.MockerFixture):
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
        id=id,
        name=name,
        ingredients=["apple", "banana"],
        instructions=["step 1", "step 2"],
        raw="raw recipe",
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
    expected_response = ChatByRecipeResponse(
        message=ChatByRecipeMessage(
            role=ChatByRecipeRole.ASSISTANT,
            text="assistant response",
        )
    )

    mocker.patch(
        "domain.controllers.get_recipe",
        return_value=recipe,
    )
    mock_chat = mocker.patch(
        "domain.controllers.chat_by_recipe",
        return_value=models.ChatMessageModel(
            role=models.ChatRoleModel.from_proto(
                expected_response.message.role
            ),
            text=expected_response.message.text,
        ),
    )

    context = mocker.MagicMock()

    servicer = RecipeSearchServicer()
    response = servicer.ChatByRecipe(request, context)

    mock_chat.assert_called_once_with(
        name,
        recipe,
        mocker.ANY,
    )
    assert all(
        req == arg for req, arg in zip(request.messages, mock_chat.args[2])
    )
    assert response == expected_response


def test_chat_by_recipe_recipe_not_found(
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
        servicer.ChatByRecipe(request, context)

    mock_get_recipe.assert_called_once_with(id)
    context.abort.assert_called_once_with(
        grpc.StatusCode.NOT_FOUND,
        f"Recipe with ID {id} not found",
    )
