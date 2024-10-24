// <auto-generated>
//     Generated by the protocol buffer compiler.  DO NOT EDIT!
//     source: Protos/service.proto
// </auto-generated>
#pragma warning disable 0414, 1591, 8981, 0612
#region Designer generated code

using grpc = global::Grpc.Core;

namespace IntelliCook.RecipeSearch.Client {
  public static partial class RecipeSearchService
  {
    static readonly string __ServiceName = "RecipeSearchService";

    [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
    static void __Helper_SerializeMessage(global::Google.Protobuf.IMessage message, grpc::SerializationContext context)
    {
      #if !GRPC_DISABLE_PROTOBUF_BUFFER_SERIALIZATION
      if (message is global::Google.Protobuf.IBufferMessage)
      {
        context.SetPayloadLength(message.CalculateSize());
        global::Google.Protobuf.MessageExtensions.WriteTo(message, context.GetBufferWriter());
        context.Complete();
        return;
      }
      #endif
      context.Complete(global::Google.Protobuf.MessageExtensions.ToByteArray(message));
    }

    [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
    static class __Helper_MessageCache<T>
    {
      public static readonly bool IsBufferMessage = global::System.Reflection.IntrospectionExtensions.GetTypeInfo(typeof(global::Google.Protobuf.IBufferMessage)).IsAssignableFrom(typeof(T));
    }

    [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
    static T __Helper_DeserializeMessage<T>(grpc::DeserializationContext context, global::Google.Protobuf.MessageParser<T> parser) where T : global::Google.Protobuf.IMessage<T>
    {
      #if !GRPC_DISABLE_PROTOBUF_BUFFER_SERIALIZATION
      if (__Helper_MessageCache<T>.IsBufferMessage)
      {
        return parser.ParseFrom(context.PayloadAsReadOnlySequence());
      }
      #endif
      return parser.ParseFrom(context.PayloadAsNewBuffer());
    }

    [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
    static readonly grpc::Marshaller<global::IntelliCook.RecipeSearch.Client.HealthRequest> __Marshaller_HealthRequest = grpc::Marshallers.Create(__Helper_SerializeMessage, context => __Helper_DeserializeMessage(context, global::IntelliCook.RecipeSearch.Client.HealthRequest.Parser));
    [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
    static readonly grpc::Marshaller<global::IntelliCook.RecipeSearch.Client.HealthResponse> __Marshaller_HealthResponse = grpc::Marshallers.Create(__Helper_SerializeMessage, context => __Helper_DeserializeMessage(context, global::IntelliCook.RecipeSearch.Client.HealthResponse.Parser));
    [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
    static readonly grpc::Marshaller<global::IntelliCook.RecipeSearch.Client.SearchRecipesByIngredientsRequest> __Marshaller_SearchRecipesByIngredientsRequest = grpc::Marshallers.Create(__Helper_SerializeMessage, context => __Helper_DeserializeMessage(context, global::IntelliCook.RecipeSearch.Client.SearchRecipesByIngredientsRequest.Parser));
    [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
    static readonly grpc::Marshaller<global::IntelliCook.RecipeSearch.Client.SearchRecipesByIngredientsResponse> __Marshaller_SearchRecipesByIngredientsResponse = grpc::Marshallers.Create(__Helper_SerializeMessage, context => __Helper_DeserializeMessage(context, global::IntelliCook.RecipeSearch.Client.SearchRecipesByIngredientsResponse.Parser));

    [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
    static readonly grpc::Method<global::IntelliCook.RecipeSearch.Client.HealthRequest, global::IntelliCook.RecipeSearch.Client.HealthResponse> __Method_GetHealth = new grpc::Method<global::IntelliCook.RecipeSearch.Client.HealthRequest, global::IntelliCook.RecipeSearch.Client.HealthResponse>(
        grpc::MethodType.Unary,
        __ServiceName,
        "GetHealth",
        __Marshaller_HealthRequest,
        __Marshaller_HealthResponse);

    [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
    static readonly grpc::Method<global::IntelliCook.RecipeSearch.Client.SearchRecipesByIngredientsRequest, global::IntelliCook.RecipeSearch.Client.SearchRecipesByIngredientsResponse> __Method_SearchRecipesByIngredients = new grpc::Method<global::IntelliCook.RecipeSearch.Client.SearchRecipesByIngredientsRequest, global::IntelliCook.RecipeSearch.Client.SearchRecipesByIngredientsResponse>(
        grpc::MethodType.Unary,
        __ServiceName,
        "SearchRecipesByIngredients",
        __Marshaller_SearchRecipesByIngredientsRequest,
        __Marshaller_SearchRecipesByIngredientsResponse);

    /// <summary>Service descriptor</summary>
    public static global::Google.Protobuf.Reflection.ServiceDescriptor Descriptor
    {
      get { return global::IntelliCook.RecipeSearch.Client.ServiceReflection.Descriptor.Services[0]; }
    }

    /// <summary>Client for RecipeSearchService</summary>
    public partial class RecipeSearchServiceClient : grpc::ClientBase<RecipeSearchServiceClient>
    {
      /// <summary>Creates a new client for RecipeSearchService</summary>
      /// <param name="channel">The channel to use to make remote calls.</param>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      public RecipeSearchServiceClient(grpc::ChannelBase channel) : base(channel)
      {
      }
      /// <summary>Creates a new client for RecipeSearchService that uses a custom <c>CallInvoker</c>.</summary>
      /// <param name="callInvoker">The callInvoker to use to make remote calls.</param>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      public RecipeSearchServiceClient(grpc::CallInvoker callInvoker) : base(callInvoker)
      {
      }
      /// <summary>Protected parameterless constructor to allow creation of test doubles.</summary>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      protected RecipeSearchServiceClient() : base()
      {
      }
      /// <summary>Protected constructor to allow creation of configured clients.</summary>
      /// <param name="configuration">The client configuration.</param>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      protected RecipeSearchServiceClient(ClientBaseConfiguration configuration) : base(configuration)
      {
      }

      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      public virtual global::IntelliCook.RecipeSearch.Client.HealthResponse GetHealth(global::IntelliCook.RecipeSearch.Client.HealthRequest request, grpc::Metadata headers = null, global::System.DateTime? deadline = null, global::System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken))
      {
        return GetHealth(request, new grpc::CallOptions(headers, deadline, cancellationToken));
      }
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      public virtual global::IntelliCook.RecipeSearch.Client.HealthResponse GetHealth(global::IntelliCook.RecipeSearch.Client.HealthRequest request, grpc::CallOptions options)
      {
        return CallInvoker.BlockingUnaryCall(__Method_GetHealth, null, options, request);
      }
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      public virtual grpc::AsyncUnaryCall<global::IntelliCook.RecipeSearch.Client.HealthResponse> GetHealthAsync(global::IntelliCook.RecipeSearch.Client.HealthRequest request, grpc::Metadata headers = null, global::System.DateTime? deadline = null, global::System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken))
      {
        return GetHealthAsync(request, new grpc::CallOptions(headers, deadline, cancellationToken));
      }
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      public virtual grpc::AsyncUnaryCall<global::IntelliCook.RecipeSearch.Client.HealthResponse> GetHealthAsync(global::IntelliCook.RecipeSearch.Client.HealthRequest request, grpc::CallOptions options)
      {
        return CallInvoker.AsyncUnaryCall(__Method_GetHealth, null, options, request);
      }
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      public virtual global::IntelliCook.RecipeSearch.Client.SearchRecipesByIngredientsResponse SearchRecipesByIngredients(global::IntelliCook.RecipeSearch.Client.SearchRecipesByIngredientsRequest request, grpc::Metadata headers = null, global::System.DateTime? deadline = null, global::System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken))
      {
        return SearchRecipesByIngredients(request, new grpc::CallOptions(headers, deadline, cancellationToken));
      }
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      public virtual global::IntelliCook.RecipeSearch.Client.SearchRecipesByIngredientsResponse SearchRecipesByIngredients(global::IntelliCook.RecipeSearch.Client.SearchRecipesByIngredientsRequest request, grpc::CallOptions options)
      {
        return CallInvoker.BlockingUnaryCall(__Method_SearchRecipesByIngredients, null, options, request);
      }
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      public virtual grpc::AsyncUnaryCall<global::IntelliCook.RecipeSearch.Client.SearchRecipesByIngredientsResponse> SearchRecipesByIngredientsAsync(global::IntelliCook.RecipeSearch.Client.SearchRecipesByIngredientsRequest request, grpc::Metadata headers = null, global::System.DateTime? deadline = null, global::System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken))
      {
        return SearchRecipesByIngredientsAsync(request, new grpc::CallOptions(headers, deadline, cancellationToken));
      }
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      public virtual grpc::AsyncUnaryCall<global::IntelliCook.RecipeSearch.Client.SearchRecipesByIngredientsResponse> SearchRecipesByIngredientsAsync(global::IntelliCook.RecipeSearch.Client.SearchRecipesByIngredientsRequest request, grpc::CallOptions options)
      {
        return CallInvoker.AsyncUnaryCall(__Method_SearchRecipesByIngredients, null, options, request);
      }
      /// <summary>Creates a new instance of client from given <c>ClientBaseConfiguration</c>.</summary>
      [global::System.CodeDom.Compiler.GeneratedCode("grpc_csharp_plugin", null)]
      protected override RecipeSearchServiceClient NewInstance(ClientBaseConfiguration configuration)
      {
        return new RecipeSearchServiceClient(configuration);
      }
    }

  }
}
#endregion
