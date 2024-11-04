import logging
from dataclasses import dataclass
from enum import Enum, StrEnum, auto
from typing import Any, Dict, Iterable, Optional, Type

import openai
from openai.types.chat.chat_completion_message import (
    ChatCompletionMessage as OpenAIChatCompletionMessage,
)

from configs.azure import configs
from domain.chats.base import BaseChat, BaseChatMessage
from infra import models
from protos.chat_by_recipe_pb2 import ChatByRecipeMessage, ChatByRecipeRole


@dataclass
class AzureOpenAIChatMessage(BaseChatMessage):
    """Message class for Azure OpenAI chat model"""

    class Role(StrEnum):
        """Message role enumeration"""

        SYSTEM = "system"
        USER = "user"
        ASSISTANT = "assistant"

        @classmethod
        def from_proto(
            cls, role: ChatByRecipeRole
        ) -> "AzureOpenAIChatMessage.Role":
            """Create a role from a protobuf role.

            Arguments:
                role (ChatByRecipeRole): The protobuf role.

            Returns:
                AzureOpenAIChatMessage.Role: The new role.
            """
            if role == ChatByRecipeRole.SYSTEM:
                return cls.SYSTEM
            if role == ChatByRecipeRole.USER:
                return cls.USER
            if role == ChatByRecipeRole.ASSISTANT:
                return cls.ASSISTANT

        def to_proto(self) -> ChatByRecipeRole:
            """Convert the role to a protobuf role.

            Returns:
                ChatByRecipeRole: The protobuf role.
            """
            if self == self.SYSTEM:
                return ChatByRecipeRole.SYSTEM
            if self == self.USER:
                return ChatByRecipeRole.USER
            if self == self.ASSISTANT:
                return ChatByRecipeRole.ASSISTANT

    @dataclass
    class Message:
        """Message class"""

        role: "AzureOpenAIChatMessage.Role"
        content: str

    message: Message

    @classmethod
    def from_proto(
        cls, proto: ChatByRecipeMessage
    ) -> "AzureOpenAIChatMessage":
        """Create a message from a protobuf message.

        Arguments:
            proto (ChatByRecipeMessage): The protobuf message.

        Returns:
            BaseChatMessage: The new message.
        """
        return cls(
            message=cls.Message(
                role=cls.Role.from_proto(proto.role),
                content=proto.text,
            )
        )

    def to_proto(self) -> ChatByRecipeMessage:
        """Convert the message to a protobuf message.

        Returns:
            ChatByRecipeMessage: The protobuf message.
        """
        return ChatByRecipeMessage(
            role=self.message.role.to_proto(),
            text=self.message.content,
        )

    def to_payload(self) -> Dict[str, Any]:
        """Convert to message payload.

        Returns:
            Dict[str, Any]: The message payload.
        """
        return {
            "role": self.message.role.value,
            "content": [
                {
                    "type": "text",
                    "text": self.message.content,
                },
            ],
        }

    @classmethod
    def from_payload(
        cls, message: OpenAIChatCompletionMessage
    ) -> "AzureOpenAIChatMessage":
        """Create from response message.

        Arguments:
            message (OpenAIChatCompletionMessage): The message type from
                OpenAI.

        Returns:
            AzureOpenAIChatMessage: The message.
        """
        if not message.content:
            raise Exception("Content is empty")

        return cls(
            message=cls.Message(
                role=cls.Role(message.role), content=message.content
            )
        )


class AzureOpenAIChat(BaseChat):
    """Chat class for Azure OpenAI chat model"""

    @classmethod
    def get_message_type(cls) -> Type[AzureOpenAIChatMessage]:
        """Get the message type of the chat model.

        Returns:
            Type[AzureOpenAIChatMessage]: The message type of the chat model.
        """
        return AzureOpenAIChatMessage

    @dataclass
    class Configs:
        """Initial configuration for the chat model"""

        api_version: str
        model: str

    class SystemPromptKey(Enum):
        """System prompt format key enumeration"""

        INTRO = auto()
        USER = auto()
        RECIPE = auto()
        END = auto()

    SYSTEM_PROMPT_ORDER = [
        SystemPromptKey.INTRO,
        SystemPromptKey.USER,
        SystemPromptKey.RECIPE,
        SystemPromptKey.END,
    ]

    SYSTEM_PROMPT_FORMATS = {
        SystemPromptKey.INTRO: (
            "You are a cooking professional who helps users with their"
            " queries."
        ),
        SystemPromptKey.USER: (
            "You are chatting with the user who's name is {name}."
        ),
        SystemPromptKey.RECIPE: (
            "You are chatting with the user about a recipe. The recipe is"
            " '{name}'. The recipe's ingredients are: {ingredients}. The"
            " recipe's instructions are: {instructions}."
        ),
        SystemPromptKey.END: (
            "Do not make up any information not provided here, only reply with"
            " the information provided here. State that you do not have the"
            " information if it is not provided here."
        ),
    }

    logger: logging.Logger
    configs: Configs
    system_prompts: Dict[SystemPromptKey, Optional[str]]
    client: openai.AzureOpenAI

    def __init__(self, init_configs: Configs):
        self.logger = logging.getLogger(__name__)
        self.configs = init_configs

        self.system_prompts = {key: None for key in self.SystemPromptKey}
        self.system_prompts[self.SystemPromptKey.INTRO] = (
            self.SYSTEM_PROMPT_FORMATS[self.SystemPromptKey.INTRO]
        )
        self.system_prompts[self.SystemPromptKey.END] = (
            self.SYSTEM_PROMPT_FORMATS[self.SystemPromptKey.END]
        )

        self.client = openai.AzureOpenAI(
            api_version=self.configs.api_version,
            azure_endpoint=configs.openai_base_url,
        )

        self.logger.info(f"{self.configs.model} initialized")

    def get_system_prompt(self) -> str:
        """Get the system prompt.

        Returns:
            str: The system prompt.
        """
        return " ".join(
            prompt
            for key in self.SYSTEM_PROMPT_ORDER
            if (prompt := self.system_prompts[key])
        )

    def get_system_message(self) -> AzureOpenAIChatMessage:
        """Get the system message.

        Returns:
            AzureOpenAIChatMessage: The system message.
        """
        return AzureOpenAIChatMessage(
            message=AzureOpenAIChatMessage.Message(
                role=AzureOpenAIChatMessage.Role.SYSTEM,
                content=self.get_system_prompt(),
            )
        )

    def set_user(self, user: str):
        """Prepare the chat model for a user.

        Arguments:
            user (str): The user to prepare.
        """
        self.system_prompts[self.SystemPromptKey.USER] = (
            self.SYSTEM_PROMPT_FORMATS[self.SystemPromptKey.USER].format(
                name=user
            )
        )

    def set_recipe(self, recipe: models.RecipeModel):
        """Prepare the chat model for a recipe.

        Arguments:
            recipe (RecipeModel): The recipe to prepare.
        """
        self.system_prompts[
            self.SystemPromptKey.RECIPE
        ] = self.SYSTEM_PROMPT_FORMATS[self.SystemPromptKey.RECIPE].format(
            name=recipe.name,
            ingredients=", ".join(recipe.ingredients),
            instructions=" ".join(
                f"{i}. {instruction}"
                for i, instruction in enumerate(recipe.instructions)
            ),
        )

    def chat(
        self, messages: Iterable[AzureOpenAIChatMessage]
    ) -> AzureOpenAIChatMessage:
        """Chat with the model.

        Arguments:
            messages (Iterable[AzureOpenAIChatMessage]): The messages to chat
                with.

        Returns:
            AzureOpenAIChatMessage: The response message.
        """
        response = self.client.chat.completions.create(
            model=self.configs.model,
            messages=[
                self.get_system_message().to_payload(),
                *(message.to_payload() for message in messages),
            ],
        )

        self.logger.debug(f"Response: {response}")

        if not response.choices:
            raise Exception("Response choices is empty")

        choice = response.choices[0]

        if choice.finish_reason not in ("length", "stop"):
            raise Exception(f"Invalid finish reason: {choice.finish_reason}")

        response_message = AzureOpenAIChatMessage.from_payload(
            response.choices[0].message
        )

        return response_message
