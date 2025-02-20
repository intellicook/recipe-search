import grpc
import pytest
import pytest_mock

from apis.servicer import RecipeSearchServicer
from infra.models import UserProfileModel, UserProfileModelVeggieIdentity
from protos.user_profile_pb2 import UserProfileRequest, UserProfileResponse


def test_get_user_profile_success(
    mocker: pytest_mock.MockerFixture,
):
    username = "test_user"
    profile = UserProfileModel(
        username=username,
        veggie_identity=UserProfileModelVeggieIdentity.VEGETARIAN,
        prefer=["apple", "banana"],
        dislike=["orange", "grape"],
        embedding=[0.1, 0.2, 0.3],
    )
    request = UserProfileRequest(
        username=profile.username,
    )
    expected_response = UserProfileResponse(
        username=profile.username,
        veggie_identity=profile.veggie_identity.to_proto(),
        prefer=profile.prefer,
        dislike=profile.dislike,
    )

    mock_get_user_profile = mocker.patch(
        "domain.controllers.get_user_profile",
        return_value=profile,
    )

    context = mocker.MagicMock()

    servicer = RecipeSearchServicer()
    response = servicer.GetUserProfile(request, context)

    mock_get_user_profile.assert_called_once_with(username)
    assert response == expected_response


def test_get_user_profile_not_found(
    mocker: pytest_mock.MockerFixture,
):
    username = "test_user"
    request = UserProfileRequest(
        username=username,
    )

    mock_get_user_profile = mocker.patch(
        "domain.controllers.get_user_profile",
        return_value=None,
    )

    context = mocker.MagicMock()
    context.abort = mocker.MagicMock(side_effect=grpc.RpcError)

    servicer = RecipeSearchServicer()
    with pytest.raises(grpc.RpcError):
        servicer.GetUserProfile(request, context)

    mock_get_user_profile.assert_called_once_with(username)
    context.abort.assert_called_once_with(
        grpc.StatusCode.NOT_FOUND,
        f"User profile with username {username} not found",
    )
