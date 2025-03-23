import json
import logging
from dataclasses import dataclass
from enum import Enum, StrEnum, auto
from typing import Dict, Iterable, Optional, Union

import openai
from openai.types.chat import (
    ChatCompletionAssistantMessageParam as OpenAIAssistantMessageParam,
)
from openai.types.chat import ChatCompletionMessage as OpenAICompletionMessage
from openai.types.chat import (
    ChatCompletionMessageToolCall as OpenAIChatCompletionMessageToolCall,
)
from openai.types.chat import (
    ChatCompletionSystemMessageParam as OpenAISystemMessageParam,
)
from openai.types.chat import (
    ChatCompletionToolParam as OpenAIChatCompletionToolParam,
)
from openai.types.chat import (
    ChatCompletionUserMessageParam as OpenAIUserMessageParam,
)
from openai.types.chat.chat_completion_chunk import (
    ChoiceDelta as OpenAIStreamChoiceDelta,
)
from openai.types.shared.function_definition import (
    FunctionDefinition as OpenAIFuncDef,
)
from pydantic import BaseModel

from configs.azure import configs
from domain import controllers
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
        FUNCTION_CALL = auto()
        END = auto()
        FUNCTION_ENUM_END = auto()
        FUNCTION_CALL_END = auto()

    class SystemPromptType(Enum):
        """System prompt type enumeration"""

        PROMPT = auto()
        FUNCTION_ENUM_PROMPT = auto()
        FUNCTION_CALL_PROMPT = auto()

    SYSTEM_PROMPT_ORDER = [
        SystemPromptKey.INTRO,
        SystemPromptKey.USER,
        SystemPromptKey.RECIPE,
        SystemPromptKey.FUNCTION_CALL,
        SystemPromptKey.END,
    ]

    SYSTEM_FUNCTION_ENUM_PROMPT_ORDER = [
        SystemPromptKey.INTRO,
        SystemPromptKey.USER,
        SystemPromptKey.RECIPE,
        SystemPromptKey.FUNCTION_ENUM_END,
    ]

    SYSTEM_FUNCTION_CALL_PROMPT_ORDER = [
        SystemPromptKey.INTRO,
        SystemPromptKey.USER,
        SystemPromptKey.RECIPE,
        SystemPromptKey.FUNCTION_CALL_END,
    ]

    SYSTEM_PROMPT_FORMATS = {
        SystemPromptKey.INTRO: (
            "You are a cooking assistant who helps users with their queries."
            " Talk and act like a normal human with a friendly and helpful"
            " tone, but remember that you are a cooking assistant AI."
        ),
        SystemPromptKey.USER: (
            "You are chatting with the user who's name is {name}."
        ),
        SystemPromptKey.RECIPE: (
            "You are chatting with the user about a recipe. The recipe is"
            " {title}. The recipe's details are {json}."
        ),
        SystemPromptKey.FUNCTION_CALL: (
            "You may ask whether the user want to use any of the following"
            " functions that you can provide: set or update user profile,"
            " serach recipes. Only ask if the user's latest message is related"
            " to any of the functions."
        ),
        SystemPromptKey.END: (
            "You will only talk about things related to the above recipe or"
            " cooking in general. If the user tries to talk about something"
            " else, remind them that you are a cooking assistant and that you"
            " can only help with cooking-related queries."
        ),
        SystemPromptKey.FUNCTION_ENUM_END: (
            "You should decide which function to use based on the user's"
            " latest message, only use the function if the user explicitly"
            " requested it, explicitly stated that they want to do what the"
            " function does, or directly responded to your request of using"
            " certain function call. Do not use any function if the user's"
            " query is not related to any function."
        ),
        SystemPromptKey.FUNCTION_CALL_END: (
            "You should use the function call based on the user's latest"
            " message, provide the appropriate arguments for the function"
            " call. Do not do anything that the user did not ask to."
        ),
    }

    FUNCTION_CALLS = {
        models.ChatResponseFunctionCallModel.SET_USER_PROFILE: OpenAIFuncDef(
            name="set_user_profile",
            description=(
                "Set the user profile, this replaces the entire profile with"
                " the new one. Update the profile by providing the new value,"
                " with all the other old values."
            ),
            strict=True,
            parameters={
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "veggie_identity": {
                        "type": "string",
                        "enum": [
                            "none",
                            "vegetarian",
                            "vegan",
                        ],
                        "description": (
                            "The vegetarian/vegan identity of the user, none"
                            " indicates omnivore"
                        ),
                    },
                    "prefer": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": (
                            "List of ingredients or foods that the user"
                            " prefers"
                        ),
                    },
                    "dislike": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": (
                            "List of ingredients or foods that the user"
                            " dislikes"
                        ),
                    },
                },
                "required": ["veggie_identity", "prefer", "dislike"],
            },
        ),
        models.ChatResponseFunctionCallModel.SEARCH_RECIPES: OpenAIFuncDef(
            name="search_recipes",
            description="Search for recipes.",
            strict=True,
            parameters={
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "ingredients": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": (
                            "List of ingredients to search for in recipes"
                        ),
                    },
                    "extra_terms": {
                        "type": "string",
                        "description": (
                            "Additional search terms/words/sentences to"
                            " refine recipe search"
                        ),
                    },
                },
                "required": ["ingredients", "extra_terms"],
            },
        ),
    }

    logger: logging.Logger
    configs: Configs
    username: Optional[str]
    system_prompts: Dict[SystemPromptKey, Optional[str]]
    system_function_enum_prompts: Dict[SystemPromptKey, Optional[str]]
    system_function_call_prompt: Dict[SystemPromptKey, Optional[str]]
    client: openai.AzureOpenAI

    def __init__(self, init_configs: Configs):
        self.logger = logging.getLogger(__name__)
        self.configs = init_configs

        self.system_prompts = {key: None for key in self.SystemPromptKey}
        self.system_prompts[self.SystemPromptKey.INTRO] = (
            self.SYSTEM_PROMPT_FORMATS[self.SystemPromptKey.INTRO]
        )
        self.system_prompts[self.SystemPromptKey.FUNCTION_CALL] = (
            self.SYSTEM_PROMPT_FORMATS[self.SystemPromptKey.FUNCTION_CALL]
        )
        self.system_prompts[self.SystemPromptKey.END] = (
            self.SYSTEM_PROMPT_FORMATS[self.SystemPromptKey.END]
        )

        self.system_function_enum_prompts = {
            key: None for key in self.SystemPromptKey
        }
        self.system_function_enum_prompts[self.SystemPromptKey.INTRO] = (
            self.SYSTEM_PROMPT_FORMATS[self.SystemPromptKey.INTRO]
        )
        self.system_function_enum_prompts[self.SystemPromptKey.USER] = (
            self.SYSTEM_PROMPT_FORMATS[self.SystemPromptKey.USER]
        )
        self.system_function_enum_prompts[self.SystemPromptKey.RECIPE] = (
            self.SYSTEM_PROMPT_FORMATS[self.SystemPromptKey.RECIPE]
        )
        self.system_function_enum_prompts[
            self.SystemPromptKey.FUNCTION_ENUM_END
        ] = self.SYSTEM_PROMPT_FORMATS[self.SystemPromptKey.FUNCTION_ENUM_END]

        self.system_function_call_prompts = {
            key: None for key in self.SystemPromptKey
        }
        self.system_function_call_prompts[self.SystemPromptKey.INTRO] = (
            self.SYSTEM_PROMPT_FORMATS[self.SystemPromptKey.INTRO]
        )
        self.system_function_call_prompts[
            self.SystemPromptKey.FUNCTION_CALL_END
        ] = self.SYSTEM_PROMPT_FORMATS[self.SystemPromptKey.FUNCTION_CALL_END]

        self.client = openai.AzureOpenAI(
            api_version=self.configs.api_version,
            azure_endpoint=configs.azure_openai_base_url,
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

    def get_system_function_enum_prompt(self) -> str:
        """Get the system function enum prompt.

        Returns:
            str: The system function enum prompt.
        """
        return " ".join(
            prompt
            for key in self.SYSTEM_FUNCTION_ENUM_PROMPT_ORDER
            if (prompt := self.system_function_enum_prompts[key])
        )

    def get_system_function_call_prompt(self) -> str:
        """Get the system function call prompt.

        Returns:
            str: The system function call prompt.
        """
        return " ".join(
            prompt
            for key in self.SYSTEM_FUNCTION_CALL_PROMPT_ORDER
            if (prompt := self.system_function_call_prompts[key])
        )

    def get_system_payload(
        self,
        type: SystemPromptType = SystemPromptType.PROMPT,
        additional: str = "",
    ) -> OpenAISystemMessageParam:
        """Get the OpenAI system message.

        Arguments:
            type (SystemPromptType): The system prompt type.
            additional (str): Additional prompt to add.

        Returns:
            OpenAISystemMessageParam: The system message.
        """
        get_system_prompts = {
            self.SystemPromptType.PROMPT: self.get_system_prompt,
            self.SystemPromptType.FUNCTION_ENUM_PROMPT: (
                self.get_system_function_enum_prompt
            ),
            self.SystemPromptType.FUNCTION_CALL_PROMPT: (
                self.get_system_function_call_prompt
            ),
        }

        return OpenAISystemMessageParam(
            role="system",
            content=get_system_prompts[type]() + additional,
        )

    def set_user(self, user: str, username: Optional[str] = None):
        """Prepare the chat model for a user.

        Arguments:
            user (str): The user to prepare.
            username (Optional[str]): The username to prepare.
        """
        self.system_prompts[self.SystemPromptKey.USER] = (
            self.SYSTEM_PROMPT_FORMATS[self.SystemPromptKey.USER].format(
                name=user
            )
        )
        self.system_function_call_prompts[self.SystemPromptKey.USER] = (
            self.SYSTEM_PROMPT_FORMATS[self.SystemPromptKey.USER].format(
                name=user
            )
        )

        self.username = username

    def set_recipe(self, recipe: models.RecipeModel):
        """Prepare the chat model for a recipe.

        Arguments:
            recipe (RecipeModel): The recipe to prepare.
        """
        self.system_prompts[self.SystemPromptKey.RECIPE] = (
            self.SYSTEM_PROMPT_FORMATS[self.SystemPromptKey.RECIPE].format(
                title=recipe.title, json=json.dumps(recipe.as_dict())
            )
        )
        self.system_function_call_prompts[self.SystemPromptKey.RECIPE] = (
            self.SYSTEM_PROMPT_FORMATS[self.SystemPromptKey.RECIPE].format(
                title=recipe.title, json=json.dumps(recipe.as_dict())
            )
        )

    def get_user_profile_prompt(self) -> str:
        """Get the user profile prompt.

        Returns:
            str: The user profile prompt.
        """
        if self.username is None:
            raise Exception("Username is not set")

        profile = controllers.get_user_profile(self.username)

        return (
            "If the user wants to change their identity to vegan or"
            " vegetarian, or remove them, set the veggie identity parameter."
            " If they want to remove or add any preferred food or disliked"
            " food, remove or add them on top of existing profile. The user's"
            f" profile is: {profile}"
        )

    def chat(
        self, messages: Iterable[models.ChatMessageModel]
    ) -> models.ChatResponseModel:
        """Chat with the model.

        Arguments:
            messages (Iterable[models.ChatMessageModel]): The messages to chat
                with.

        Returns:
            models.ChatResponseModel: The response.
        """
        openai_messages = [
            self._message_model_to_openai_message_param(message)
            for message in messages
        ]

        class FunctionFormat(BaseModel):
            """The function to call."""

            function: Optional[models.ChatResponseFunctionCallModel]
            """
            The function to use for user's query,
            or None if no function is required.
            """

        function_enum_response = self.client.beta.chat.completions.parse(
            model=self.configs.model,
            messages=[
                self.get_system_payload(
                    type=self.SystemPromptType.FUNCTION_ENUM_PROMPT
                ),
                *openai_messages,
            ],
            response_format=FunctionFormat,
        )

        self.logger.debug(f"Function enum response: {function_enum_response}")

        function_enum = function_enum_response.choices[0].message
        if function_enum.parsed and function_enum.parsed.function is not None:
            function_schema = self.FUNCTION_CALLS[
                function_enum.parsed.function
            ]

            additional_prompt = ""
            if (
                function_enum.parsed.function
                == models.ChatResponseFunctionCallModel.SET_USER_PROFILE
            ):
                additional_prompt = " " + self.get_user_profile_prompt()

            function_call_response = self.client.chat.completions.create(
                model=self.configs.model,
                messages=[
                    self.get_system_payload(
                        type=self.SystemPromptType.FUNCTION_CALL_PROMPT,
                        additional=additional_prompt,
                    ),
                    *openai_messages,
                ],
                tools=[
                    OpenAIChatCompletionToolParam(
                        function=function_schema,
                        type="function",
                    )
                ],
                tool_choice="required",
            )

            self.logger.debug(
                f"Function call response: {function_call_response}"
            )

            if not function_call_response.choices:
                raise Exception("Function call response choices is empty")

            function_call_choice = function_call_response.choices[0]

            if function_call_choice.finish_reason not in (
                "length",
                "stop",
                "tool_calls",
            ):
                raise Exception(
                    "Invalid function call finish reason:"
                    f" {function_call_choice.finish_reason}"
                )

            tool_calls = function_call_choice.message.tool_calls

            if tool_calls:
                tool_call = tool_calls[0]

                return models.ChatResponseModel(
                    message=models.ChatMessageModel(
                        role=models.ChatRoleModel.ASSISTANT,
                        text=(
                            "I can help you with it. Are the following options"
                            " okay?"
                        ),
                    ),
                    function_call=self._openai_function_call_to_model(
                        tool_call
                    ),
                )

        response = self.client.chat.completions.create(
            model=self.configs.model,
            messages=[
                self.get_system_payload(),
                *openai_messages,
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

        return models.ChatResponseModel(
            message=response_message,
        )

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

    def identify_recipe_veggie_identity(
        self, recipe: models.RecipeModel
    ) -> models.UserProfileModelVeggieIdentity:
        """Identify the recipe's veggie identity.

        Arguments:
            recipe (models.RecipeModel): The recipe to identify.

        Returns:
            models.UserProfileModelVeggieIdentity: The recipe's veggie
                identity.
        """

        class RecipeVeggieIdentity(StrEnum):
            """Recipe veggie identity enumeration"""

            NON_VEGETARIAN = "non-vegetarian"
            VEGETARIAN = "vegetarian"
            VEGAN = "vegan"

        response = self.client.beta.chat.completions.parse(
            model=self.configs.model,
            messages=[
                OpenAISystemMessageParam(
                    role="system",
                    content=(
                        "You are a menu assistant to determine whether the"
                        " provided recipe is vegetarian, vegan, or"
                        " non-vegetarian. Vegetarian is defined as not"
                        " containing meat, fish, or poultry. Vegan is defined"
                        " as not containing any animal products or"
                        " by-products. Non-vegetarian is defined as"
                        " containing meat, fish, or poultry. The recipe to"
                        f" determine is: {json.dumps(recipe.as_dict())}"
                    ),
                ),
            ],
            temperature=0.2,
            response_format=RecipeVeggieIdentity,
        )

        self.logger.debug(f"Response: {response}")

        if not response.choices:
            raise Exception("Response choices is empty")

        choice = response.choices[0]

        if choice.finish_reason not in ("stop",):
            raise Exception(f"Invalid finish reason: {choice.finish_reason}")

        identity = choice.message.parsed

        return {
            None: models.UserProfileModelVeggieIdentity.NONE,
            RecipeVeggieIdentity.NON_VEGETARIAN: (
                models.UserProfileModelVeggieIdentity.NONE
            ),
            RecipeVeggieIdentity.VEGETARIAN: (
                models.UserProfileModelVeggieIdentity.VEGETARIAN
            ),
            RecipeVeggieIdentity.VEGAN: (
                models.UserProfileModelVeggieIdentity.VEGAN
            ),
        }[identity]

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

    def _openai_function_call_to_model(
        self,
        call: OpenAIChatCompletionMessageToolCall,
    ) -> Union[
        models.ChatSetUserProfileFunctionCallModel,
        models.ChatSearchRecipeFunctionCallModel,
    ]:
        """Convert OpenAI function arguments to function args model.

        Arguments:
            call (OpenAIChatCompletionMessageToolCall): The function call.

        Returns:
            Union[
                models.ChatSetUserProfileFunctionArgsModel,
                models.ChatSearchRecipeFunctionArgsModel,
            ]: The function arguments model.
        """
        args = json.loads(call.function.arguments)

        if (
            call.function.name
            == models.ChatResponseFunctionCallModel.SET_USER_PROFILE
        ):
            return models.ChatSetUserProfileFunctionCallModel(
                veggie_identity=models.UserProfileModelVeggieIdentity(
                    args["veggie_identity"]
                ),
                prefer=args["prefer"],
                dislike=args["dislike"],
            )

        if (
            call.function.name
            == models.ChatResponseFunctionCallModel.SEARCH_RECIPES
        ):
            return models.ChatSearchRecipeFunctionCallModel(
                ingredients=args["ingredients"],
                extra_terms=args["extra_terms"],
            )

        raise Exception(f"Invalid function name: {call.function.name}")
