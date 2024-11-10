from domain.chats.azure_openai import AzureOpenAIChat


class GPT4OMiniChat(AzureOpenAIChat):
    """GPT-4 mini OpenAI chat model"""

    CONFIGS = AzureOpenAIChat.Configs(
        api_version="2024-08-01-preview",
        model="gpt-4o-mini",
    )

    def __init__(self):
        super().__init__(self.CONFIGS)
