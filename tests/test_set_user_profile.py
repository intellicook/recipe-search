import pytest_mock

from apis.servicer import RecipeSearchServicer
from infra.models import UserProfileModel, UserProfileModelVeggieIdentity
from protos.set_user_profile_pb2 import (
    SetUserProfileRequest,
    SetUserProfileResponse,
)


def test_set_user_profile_success(
    mocker: pytest_mock.MockerFixture,
):
    profile = UserProfileModel(
        username="test_user",
        veggie_identity=UserProfileModelVeggieIdentity.VEGETARIAN,
        prefer=["apple", "banana"],
        dislike=["orange", "grape"],
        embedding=[0.1, 0.2, 0.3],
    )
    request = SetUserProfileRequest(
        username=profile.username,
        veggie_identity=profile.veggie_identity.to_proto(),
        prefer=profile.prefer,
        dislike=profile.dislike,
    )
    expected_response = SetUserProfileResponse(
        username=profile.username,
        veggie_identity=profile.veggie_identity.to_proto(),
        prefer=profile.prefer,
        dislike=profile.dislike,
    )

    mock_set_user_profile = mocker.patch(
        "domain.controllers.set_user_profile",
    )

    context = mocker.MagicMock()

    servicer = RecipeSearchServicer()
    response = servicer.SetUserProfile(request, context)

    mock_set_user_profile.assert_called_once_with(mocker.ANY)
    assert mock_set_user_profile.call_args.args[0].username == profile.username
    assert (
        mock_set_user_profile.call_args.args[0].veggie_identity
        == profile.veggie_identity
    )
    assert mock_set_user_profile.call_args.args[0].prefer == profile.prefer
    assert mock_set_user_profile.call_args.args[0].dislike == profile.dislike
    assert response == expected_response
