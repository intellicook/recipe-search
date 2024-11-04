from abc import ABC, abstractmethod
from typing import Iterable, Type

from infra import models
from protos.chat_by_recipe_pb2 import ChatByRecipeMessage


class BaseChatMessage(ABC):
    """Base class for message used and returned by chat models"""

    @classmethod
    @abstractmethod
    def from_proto(cls, proto: ChatByRecipeMessage) -> "BaseChatMessage":
        """Create a message from a protobuf message.

        Arguments:
            proto (ChatByRecipeMessage): The protobuf message.

        Returns:
            BaseChatMessage: The new message.
        """

    @abstractmethod
    def to_proto(self) -> ChatByRecipeMessage:
        """Convert the message to a protobuf message.

        Returns:
            ChatByRecipeMessage: The protobuf message.
        """


class BaseChat(ABC):
    """Base class for chat models"""

    @classmethod
    @abstractmethod
    def get_message_type(cls) -> Type[BaseChatMessage]:
        """Get the message type of the chat model.

        Returns:
            Type[BaseChatMessage]: The message type of the chat model.
        """

    @abstractmethod
    def set_user(self, user: str):
        """Prepare the chat model for a user.

        Arguments:
            user (str): The user to prepare.
        """

    @abstractmethod
    def set_recipe(self, recipe: models.RecipeModel):
        """Prepare the chat model for a recipe.

        Arguments:
            recipe (RecipeModel): The recipe to prepare.
        """

    @abstractmethod
    def chat(self, messages: Iterable[BaseChatMessage]) -> BaseChatMessage:
        """Chat with the model.

        Arguments:
            messages (Iterable[BaseChatMessage]): The messages to chat with.

        Returns:
            BaseChatMessage: The response message.
        """
