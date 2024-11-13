from abc import ABC, abstractmethod
from typing import Iterable

from infra import models


class BaseChat(ABC):
    """Base class for chat models"""

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
    def chat(
        self, messages: Iterable[models.ChatMessageModel]
    ) -> models.ChatMessageModel:
        """Chat with the model.

        Arguments:
            messages (Iterable[models.ChatMessageModel]): The messages to chat
                with.

        Returns:
            models.ChatMessageModel: The response message.
        """

    @abstractmethod
    def chat_stream(
        self, messages: Iterable[models.ChatMessageModel]
    ) -> models.ChatStreamModel:
        """Chat with the model and return a stream of messages.

        Arguments:
            messages (Iterable[models.ChatMessageModel]): The messages to chat
                with.

        Returns:
            Iterable[models.ChatStreamModel]: The response stream of messages.
        """
