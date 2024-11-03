import pytest_mock

from apis.servicer import RecipeSearchServicer
from protos.faiss_index_thread_pb2 import FaissIndexThreadRequest


def test_get_faiss_index_thread_success(
    mocker: pytest_mock.MockerFixture,
):
    count = 100
    model = "test_model"
    path = "test_path"
    is_in_progress = False
    is_complete = True
    is_successful = True
    mocker.patch(
        "domain.controllers.get_faiss_index_thread",
        return_value=mocker.MagicMock(
            count=count,
            model=model,
            path=path,
            is_in_progress=is_in_progress,
            is_complete=is_complete,
            is_successful=is_successful,
        ),
    )

    context = mocker.MagicMock()

    servicer = RecipeSearchServicer()
    request = FaissIndexThreadRequest()
    response = servicer.GetFaissIndexThread(request, context)

    assert response.args.count == count
    assert response.args.model == model
    assert response.args.path == path
    assert response.is_in_progress == is_in_progress
    assert response.is_complete == is_complete
    assert response.is_successful == is_successful


def test_get_faiss_index_thread_no_args(
    mocker: pytest_mock.MockerFixture,
):
    is_in_progress = False
    is_complete = False
    is_successful = False
    mocker.patch(
        "domain.controllers.get_faiss_index_thread",
        return_value=mocker.MagicMock(
            is_in_progress=is_in_progress,
            is_complete=is_complete,
            is_successful=is_successful,
        ),
    )

    context = mocker.MagicMock()

    servicer = RecipeSearchServicer()
    request = FaissIndexThreadRequest()
    response = servicer.GetFaissIndexThread(request, context)

    assert not response.HasField("args")
    assert response.is_in_progress == is_in_progress
    assert response.is_complete == is_complete
    assert response.is_successful == is_successful
