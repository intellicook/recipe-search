# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from protos import health_pb2 as protos_dot_health__pb2
from protos import search_recipes_by_ingredients_pb2 as protos_dot_search__recipes__by__ingredients__pb2

GRPC_GENERATED_VERSION = '1.66.2'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in protos/service_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class RecipeSearchServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetHealth = channel.unary_unary(
                '/RecipeSearchService/GetHealth',
                request_serializer=protos_dot_health__pb2.HealthRequest.SerializeToString,
                response_deserializer=protos_dot_health__pb2.HealthResponse.FromString,
                _registered_method=True)
        self.SearchRecipesByIngredients = channel.unary_unary(
                '/RecipeSearchService/SearchRecipesByIngredients',
                request_serializer=protos_dot_search__recipes__by__ingredients__pb2.SearchRecipesByIngredientsRequest.SerializeToString,
                response_deserializer=protos_dot_search__recipes__by__ingredients__pb2.SearchRecipesByIngredientsResponse.FromString,
                _registered_method=True)


class RecipeSearchServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetHealth(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SearchRecipesByIngredients(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RecipeSearchServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetHealth': grpc.unary_unary_rpc_method_handler(
                    servicer.GetHealth,
                    request_deserializer=protos_dot_health__pb2.HealthRequest.FromString,
                    response_serializer=protos_dot_health__pb2.HealthResponse.SerializeToString,
            ),
            'SearchRecipesByIngredients': grpc.unary_unary_rpc_method_handler(
                    servicer.SearchRecipesByIngredients,
                    request_deserializer=protos_dot_search__recipes__by__ingredients__pb2.SearchRecipesByIngredientsRequest.FromString,
                    response_serializer=protos_dot_search__recipes__by__ingredients__pb2.SearchRecipesByIngredientsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'RecipeSearchService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('RecipeSearchService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class RecipeSearchService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetHealth(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/RecipeSearchService/GetHealth',
            protos_dot_health__pb2.HealthRequest.SerializeToString,
            protos_dot_health__pb2.HealthResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def SearchRecipesByIngredients(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/RecipeSearchService/SearchRecipesByIngredients',
            protos_dot_search__recipes__by__ingredients__pb2.SearchRecipesByIngredientsRequest.SerializeToString,
            protos_dot_search__recipes__by__ingredients__pb2.SearchRecipesByIngredientsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
