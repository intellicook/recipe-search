import pytest_mock

from apis.servicer import RecipeSearchServicer
from protos.health_pb2 import HealthCheck, HealthRequest, HealthStatus


def test_get_health_healthy(mocker: pytest_mock.MockerFixture):
    mocker.patch("infra.db.check_health", return_value=True)

    servicer = RecipeSearchServicer()
    request = HealthRequest()
    context = mocker.MagicMock()
    response = servicer.GetHealth(request, context)

    assert response.status == HealthStatus.HEALTHY
    assert len(response.checks) == 2

    assert response.checks[0] == HealthCheck(
        name="RecipeSearch",
        status=HealthStatus.HEALTHY,
    )
    assert response.checks[1] == HealthCheck(
        name="PostgreSQL",
        status=HealthStatus.HEALTHY,
    )


def test_get_health_unhealthy(mocker: pytest_mock.MockerFixture):
    mocker.patch("infra.db.check_health", return_value=False)

    servicer = RecipeSearchServicer()
    request = HealthRequest()
    context = mocker.MagicMock()
    response = servicer.GetHealth(request, context)

    assert response.status == HealthStatus.UNHEALTHY
    assert len(response.checks) == 2

    assert response.checks[0] == HealthCheck(
        name="RecipeSearch",
        status=HealthStatus.HEALTHY,
    )
    assert response.checks[1] == HealthCheck(
        name="PostgreSQL",
        status=HealthStatus.UNHEALTHY,
    )
