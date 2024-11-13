import logging
from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, Iterable, Optional

import openai
from openai.types.chat import (
    ChatCompletionAssistantMessageParam as OpenAIAssistantMessageParam,
)
from openai.types.chat import ChatCompletionMessage as OpenAICompletionMessage
from openai.types.chat import (
    ChatCompletionSystemMessageParam as OpenAISystemMessageParam,
)
from openai.types.chat import (
    ChatCompletionUserMessageParam as OpenAIUserMessageParam,
)
from openai.types.chat.chat_completion_chunk import (
    ChoiceDelta as OpenAIStreamChoiceDelta,
)

from configs.azure import configs
from domain.chats.base import BaseChat
from infra import models


class AzureOpenAIChat(BaseChat):
    """Chat class for Azure OpenAI chat model"""

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
            "You are a cooking assistant who helps users with their queries."
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
            "Do not chat about anything unrelated to the recipe or cooking in"
            " general. If the user tries to talk about something else, remind"
            " them that you are a cooking assistant and that you can only"
            " help with cooking-related queries."
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

    def get_system_payload(self) -> OpenAISystemMessageParam:
        """Get the OpenAI system message.

        Returns:
            OpenAISystemMessageParam: The system message.
        """
        return OpenAISystemMessageParam(
            role="system",
            content=self.get_system_prompt(),
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
        self, messages: Iterable[models.ChatMessageModel]
    ) -> models.ChatMessageModel:
        """Chat with the model.

        Arguments:
            messages (Iterable[models.ChatMessageModel]): The messages to chat
                with.

        Returns:
            models.ChatMessageModel: The response message.
        """
        response = self.client.chat.completions.create(
            model=self.configs.model,
            messages=[
                self.get_system_payload(),
                *(
                    self._message_model_to_openai_message_param(message)
                    for message in messages
                ),
            ],
        )

        self.logger.debug(f"Response: {response}")

        if not response.choices:
            raise Exception("Response choices is empty")

        choice = response.choices[0]

        if choice.finish_reason not in ("length", "stop"):
            raise Exception(f"Invalid finish reason: {choice.finish_reason}")

        response_message = self._openai_completion_message_to_model(
            response.choices[0].message
        )

        return response_message

    def chat_stream(
        self, messages: Iterable[models.ChatMessageModel]
    ) -> Iterable[models.ChatStreamModel]:
        """Chat with the model and return a stream of messages.

        Arguments:
            messages (Iterable[models.ChatMessageModel]): The messages to chat
                with.

        Returns:
            Iterable[models.ChatStreamModel]: The response stream of messages.
        """
        stream = self.client.chat.completions.create(
            model=self.configs.model,
            messages=[
                self.get_system_payload(),
                *(
                    self._message_model_to_openai_message_param(message)
                    for message in messages
                ),
            ],
            stream=True,
        )

        for chunk in stream:
            if not chunk.choices or not chunk.choices[0].delta:
                self.logger.debug(f"No delta in chunk: chunk={chunk}")
                continue

            delta = chunk.choices[0].delta
            stream_model = self._openai_stream_choice_delta_to_stream_model(
                delta
            )

            if stream_model is None:
                self.logger.debug(
                    f"Did not convert delta to stream model: delta={delta}"
                )
                continue

            yield stream_model

    def _openai_completion_message_to_model(
        self,
        message: OpenAICompletionMessage,
    ) -> models.ChatMessageModel:
        """Convert OpenAI completion message to message model.

        Arguments:
            message (OpenAICompletionMessage): The message from OpenAI.

        Returns:
            models.ChatMessageModel: The message model.
        """
        if not message.content:
            raise Exception("Content is empty")

        return models.ChatMessageModel(
            role=models.ChatRoleModel.ASSISTANT,
            text=message.content,
        )

    def _openai_stream_choice_delta_to_stream_model(
        self,
        delta: OpenAIStreamChoiceDelta,
    ) -> Optional[models.ChatStreamModel]:
        """Convert OpenAI stream choice delta to stream model.

        Arguments:
            delta (OpenAIStreamChoiceDelta): The message type from
                OpenAI.

        Returns:
            Optional[models.ChatStreamModel]: The stream model.
        """
        if delta.role is not None:
            if delta.role == "assistant":
                return models.ChatStreamHeaderModel(
                    role=models.ChatRoleModel.ASSISTANT,
                )
            else:
                self.logger.warning(f"Unexpected role: {delta.role}")
                return None

        if delta.content is not None:
            return models.ChatStreamContentModel(
                text=delta.content,
            )

        return None

    def _message_model_to_openai_message_param(
        self,
        message: models.ChatMessageModel,
    ) -> OpenAIUserMessageParam | OpenAIAssistantMessageParam:
        """Convert message model to OpenAI message parameter.

        Arguments:
            message (models.ChatMessageModel): The message model.

        Returns:
            OpenAIUserMessageParam | OpenAIAssistantMessageParam: The message
                payload.
        """
        is_user = message.role == models.ChatRoleModel.USER
        cls = (
            OpenAIUserMessageParam if is_user else OpenAIAssistantMessageParam
        )

        return cls(
            role=("user" if is_user else "assistant"),
            content=message.text,
        )
