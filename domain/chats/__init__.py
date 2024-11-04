from typing import Dict, Type

from configs.domain import configs
from domain.chats.base import BaseChat
from domain.chats.gpt4o import GPT4OChat

mapping: Dict[str, Type[BaseChat]] = {
    "gpt4o": GPT4OChat,
}

model = mapping[configs.chat_model]
