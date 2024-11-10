from typing import Dict, Type

from configs.domain import configs
from domain.chats.base import BaseChat
from domain.chats.gpt4o import GPT4OChat
from domain.chats.gpt4o_mini import GPT4OMiniChat

mapping: Dict[str, Type[BaseChat]] = {
    "gpt4o": GPT4OChat,
    "gpt4o_mini": GPT4OMiniChat,
}

model = mapping[configs.chat_model]
