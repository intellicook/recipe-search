from typing import Dict, Type

from configs.domain import configs
from domain.chats.base import BaseChat
from domain.chats.gpt4o import GPT4OChat
from domain.chats.gpt4o_mini import GPT4OMiniChat
from domain.model_types import ChatModelType

mapping: Dict[ChatModelType, Type[BaseChat]] = {
    ChatModelType.GPT4O: GPT4OChat,
    ChatModelType.GPT4O_MINI: GPT4OMiniChat,
}

model = mapping[configs.domain_chat_model]
