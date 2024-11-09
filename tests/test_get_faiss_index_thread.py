import pytest_mock

from apis.servicer import RecipeSearchServicer
from protos.faiss_index_thread_pb2 import (
    FaissIndexThreadArgs,
    FaissIndexThreadRequest,
    FaissIndexThreadResponse,
    FaissIndexThreadStatus,
)


def test_get_faiss_index_thread_success(
    mocker: pytest_mock.MockerFixture,
):
    count = 100
    model = "test_model"
    path = "test_path"
    status = FaissIndexThreadStatus.COMPLETED
    mocker.patch(
        "domain.controllers.get_faiss_index_thread",
        return_value=mocker.MagicMock(
            to_proto=mocker.MagicMock(
                return_value=FaissIndexThreadResponse(
                    args=FaissIndexThreadArgs(
                        count=count,
                        model=model,
                        path=path,
                    ),
                    status=status,
                ),
            ),
        ),
    )

    context = mocker.MagicMock()

    servicer = RecipeSearchServicer()
    request = FaissIndexThreadRequest()
    response = servicer.GetFaissIndexThread(request, context)

    assert response.args.count == count
    assert response.args.model == model
    assert response.args.path == path
    assert response.status == status


def test_get_faiss_index_thread_no_args(
    mocker: pytest_mock.MockerFixture,
):
    status = FaissIndexThreadStatus.UNINITIALIZED
    mocker.patch(
        "domain.controllers.get_faiss_index_thread",
        return_value=mocker.MagicMock(
            to_proto=mocker.MagicMock(
                return_value=FaissIndexThreadResponse(
                    status=status,
                ),
            ),
        ),
    )

    context = mocker.MagicMock()

    servicer = RecipeSearchServicer()
    request = FaissIndexThreadRequest()
    response = servicer.GetFaissIndexThread(request, context)

    assert not response.HasField("args")
    assert response.status == status
