# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from protos import add_recipes_pb2 as protos_dot_add__recipes__pb2
from protos import chat_by_recipe_pb2 as protos_dot_chat__by__recipe__pb2
from protos import health_pb2 as protos_dot_health__pb2
from protos import recipe_pb2 as protos_dot_recipe__pb2
from protos import reset_data_pb2 as protos_dot_reset__data__pb2
from protos import search_recipes_pb2 as protos_dot_search__recipes__pb2

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
        self.GetRecipe = channel.unary_unary(
                '/RecipeSearchService/GetRecipe',
                request_serializer=protos_dot_recipe__pb2.RecipeRequest.SerializeToString,
                response_deserializer=protos_dot_recipe__pb2.RecipeResponse.FromString,
                _registered_method=True)
        self.SearchRecipes = channel.unary_unary(
                '/RecipeSearchService/SearchRecipes',
                request_serializer=protos_dot_search__recipes__pb2.SearchRecipesRequest.SerializeToString,
                response_deserializer=protos_dot_search__recipes__pb2.SearchRecipesResponse.FromString,
                _registered_method=True)
        self.ChatByRecipe = channel.unary_unary(
                '/RecipeSearchService/ChatByRecipe',
                request_serializer=protos_dot_chat__by__recipe__pb2.ChatByRecipeRequest.SerializeToString,
                response_deserializer=protos_dot_chat__by__recipe__pb2.ChatByRecipeResponse.FromString,
                _registered_method=True)
        self.ChatByRecipeStream = channel.unary_stream(
                '/RecipeSearchService/ChatByRecipeStream',
                request_serializer=protos_dot_chat__by__recipe__pb2.ChatByRecipeRequest.SerializeToString,
                response_deserializer=protos_dot_chat__by__recipe__pb2.ChatByRecipeStreamResponse.FromString,
                _registered_method=True)
        self.AddRecipes = channel.unary_unary(
                '/RecipeSearchService/AddRecipes',
                request_serializer=protos_dot_add__recipes__pb2.AddRecipesRequest.SerializeToString,
                response_deserializer=protos_dot_add__recipes__pb2.AddRecipesResponse.FromString,
                _registered_method=True)
        self.ResetData = channel.unary_unary(
                '/RecipeSearchService/ResetData',
                request_serializer=protos_dot_reset__data__pb2.ResetDataRequest.SerializeToString,
                response_deserializer=protos_dot_reset__data__pb2.ResetDataResponse.FromString,
                _registered_method=True)


class RecipeSearchServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetHealth(self, request, context):
        """Core services

        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetRecipe(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SearchRecipes(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ChatByRecipe(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ChatByRecipeStream(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddRecipes(self, request, context):
        """Admin services

        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ResetData(self, request, context):
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
            'GetRecipe': grpc.unary_unary_rpc_method_handler(
                    servicer.GetRecipe,
                    request_deserializer=protos_dot_recipe__pb2.RecipeRequest.FromString,
                    response_serializer=protos_dot_recipe__pb2.RecipeResponse.SerializeToString,
            ),
            'SearchRecipes': grpc.unary_unary_rpc_method_handler(
                    servicer.SearchRecipes,
                    request_deserializer=protos_dot_search__recipes__pb2.SearchRecipesRequest.FromString,
                    response_serializer=protos_dot_search__recipes__pb2.SearchRecipesResponse.SerializeToString,
            ),
            'ChatByRecipe': grpc.unary_unary_rpc_method_handler(
                    servicer.ChatByRecipe,
                    request_deserializer=protos_dot_chat__by__recipe__pb2.ChatByRecipeRequest.FromString,
                    response_serializer=protos_dot_chat__by__recipe__pb2.ChatByRecipeResponse.SerializeToString,
            ),
            'ChatByRecipeStream': grpc.unary_stream_rpc_method_handler(
                    servicer.ChatByRecipeStream,
                    request_deserializer=protos_dot_chat__by__recipe__pb2.ChatByRecipeRequest.FromString,
                    response_serializer=protos_dot_chat__by__recipe__pb2.ChatByRecipeStreamResponse.SerializeToString,
            ),
            'AddRecipes': grpc.unary_unary_rpc_method_handler(
                    servicer.AddRecipes,
                    request_deserializer=protos_dot_add__recipes__pb2.AddRecipesRequest.FromString,
                    response_serializer=protos_dot_add__recipes__pb2.AddRecipesResponse.SerializeToString,
            ),
            'ResetData': grpc.unary_unary_rpc_method_handler(
                    servicer.ResetData,
                    request_deserializer=protos_dot_reset__data__pb2.ResetDataRequest.FromString,
                    response_serializer=protos_dot_reset__data__pb2.ResetDataResponse.SerializeToString,
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
    def GetRecipe(request,
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
            '/RecipeSearchService/GetRecipe',
            protos_dot_recipe__pb2.RecipeRequest.SerializeToString,
            protos_dot_recipe__pb2.RecipeResponse.FromString,
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
    def SearchRecipes(request,
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
            '/RecipeSearchService/SearchRecipes',
            protos_dot_search__recipes__pb2.SearchRecipesRequest.SerializeToString,
            protos_dot_search__recipes__pb2.SearchRecipesResponse.FromString,
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
    def ChatByRecipe(request,
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
            '/RecipeSearchService/ChatByRecipe',
            protos_dot_chat__by__recipe__pb2.ChatByRecipeRequest.SerializeToString,
            protos_dot_chat__by__recipe__pb2.ChatByRecipeResponse.FromString,
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
    def ChatByRecipeStream(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/RecipeSearchService/ChatByRecipeStream',
            protos_dot_chat__by__recipe__pb2.ChatByRecipeRequest.SerializeToString,
            protos_dot_chat__by__recipe__pb2.ChatByRecipeStreamResponse.FromString,
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
    def AddRecipes(request,
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
            '/RecipeSearchService/AddRecipes',
            protos_dot_add__recipes__pb2.AddRecipesRequest.SerializeToString,
            protos_dot_add__recipes__pb2.AddRecipesResponse.FromString,
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
    def ResetData(request,
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
            '/RecipeSearchService/ResetData',
            protos_dot_reset__data__pb2.ResetDataRequest.SerializeToString,
            protos_dot_reset__data__pb2.ResetDataResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
