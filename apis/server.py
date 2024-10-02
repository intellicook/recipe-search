import logging
from concurrent import futures

import grpc
from grpc_reflection.v1alpha import reflection

from apis.servicer import RecipeSearchServicer
from configs import api
from protos import service_pb2, service_pb2_grpc

logger = logging.getLogger(__name__)


def start():
    """Start the API server."""
    port = api.configs.port
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_RecipeSearchServicer_to_server(
        RecipeSearchServicer(), server
    )

    # Reflection
    SERVICE_NAMES = (
        service_pb2.DESCRIPTOR.services_by_name["RecipeSearch"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    # Start the server
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    logger.info(f"Server started, listening on {port}")
    server.wait_for_termination()
