from enum import StrEnum


class SearchModelType(StrEnum):
    """Type of search model"""

    QWEN = "qwen"
    STELLA = "stella"


class ChatModelType(StrEnum):
    """Type of chat model"""

    GPT4O = "gpt4o"
    GPT4O_MINI = "gpt4o_mini"
