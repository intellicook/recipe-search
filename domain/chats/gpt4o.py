from domain.chats.azure_openai import AzureOpenAIChat


class GPT4OChat(AzureOpenAIChat):
    """GPT-4 OpenAI chat model"""

    CONFIGS = AzureOpenAIChat.Configs(
        api_version="2024-02-15-preview",
        model="gpt-4o",
    )

    def __init__(self):
        super().__init__(self.CONFIGS)