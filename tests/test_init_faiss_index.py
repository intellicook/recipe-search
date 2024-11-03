import grpc
import pytest
import pytest_mock

from apis.servicer import RecipeSearchServicer
from configs.domain import configs
from protos.init_faiss_index_pb2 import InitFaissIndexRequest


def test_init_faiss_index_success(
    mocker: pytest_mock.MockerFixture,
):
    count = 100
    path = "test_path"
    request = InitFaissIndexRequest(
        count=count,
        path=path,
    )

    mocker.patch(
        "domain.controllers.get_faiss_index_thread",
        return_value=mocker.MagicMock(is_in_progress=False),
    )
    mock_init = mocker.patch(
        "domain.controllers.init_faiss_index",
        return_value=None,
    )

    context = mocker.MagicMock()

    servicer = RecipeSearchServicer()
    servicer.InitFaissIndex(request, context)

    mock_init.assert_called_once_with(count=count, path=path)


def test_init_faiss_index_no_count(
    mocker: pytest_mock.MockerFixture,
):
    path = "test_path"
    request = InitFaissIndexRequest(
        path=path,
    )

    mocker.patch(
        "domain.controllers.get_faiss_index_thread",
        return_value=mocker.MagicMock(is_in_progress=False),
    )
    mock_init = mocker.patch(
        "domain.controllers.init_faiss_index",
        return_value=None,
    )

    context = mocker.MagicMock()

    servicer = RecipeSearchServicer()
    servicer.InitFaissIndex(request, context)

    mock_init.assert_called_once_with(count=None, path=path)


def test_init_faiss_index_no_path(
    mocker: pytest_mock.MockerFixture,
):
    count = 100
    request = InitFaissIndexRequest(
        count=count,
    )

    mocker.patch(
        "domain.controllers.get_faiss_index_thread",
        return_value=mocker.MagicMock(is_in_progress=False),
    )
    mock_init = mocker.patch(
        "domain.controllers.init_faiss_index",
        return_value=None,
    )

    context = mocker.MagicMock()

    servicer = RecipeSearchServicer()
    servicer.InitFaissIndex(request, context)

    mock_init.assert_called_once_with(
        count=count, path=configs.default_faiss_index_path
    )


def test_init_faiss_index_thread_in_progress(
    mocker: pytest_mock.MockerFixture,
):
    request = InitFaissIndexRequest()

    mocker.patch(
        "domain.controllers.get_faiss_index_thread",
        return_value=mocker.MagicMock(is_in_progress=True),
    )

    context = mocker.MagicMock()
    context.abort = mocker.MagicMock(side_effect=grpc.RpcError)

    servicer = RecipeSearchServicer()
    with pytest.raises(grpc.RpcError):
        servicer.InitFaissIndex(request, context)

    context.abort.assert_called_once_with(
        grpc.StatusCode.FAILED_PRECONDITION,
        "Faiss index thread is already in progress",
    )
