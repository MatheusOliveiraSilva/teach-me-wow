from apps.common.settings import AZURE_OPENAI_BASE_URL, AZURE_OPENAI_API_KEY, OPENAI_API_VERSION

class EmbeddingConfig:
    """
    EmbeddingConfig is a class that configures the embedding for the application.
    """

    def __init__(self, **kwargs):
        # Store config from environment
        self.AZURE_OPENAI_BASE_URL = AZURE_OPENAI_BASE_URL
        self.AZURE_OPENAI_API_KEY = AZURE_OPENAI_API_KEY
        self.OPENAI_API_VERSION = OPENAI_API_VERSION

        self.provider = kwargs.pop("provider", "azure")
        self.DEFAULT_OPENAI_MODEL = "gpt-4o"
        self.DEFAULT_TEMPERATURE = 0

        # Store provider and kwargs
        self.kwargs = kwargs

    def get_embedding(self):
        """
        Returns the embedding based on the provider.
        """
        if self.provider == "azure":
            return self.get_azure_embedding(**self.kwargs)
        else:
            raise ValueError(f"Provider {self.provider} not supported")

    def get_azure_embedding(self, **kwargs):
        """Configures and returns an AzureOpenAI instance."""
        from langchain_openai import AzureOpenAIEmbeddings

        params = {
            "openai_api_key": self.AZURE_OPENAI_API_KEY,
            "openai_api_version": self.OPENAI_API_VERSION,
            "azure_endpoint": self.AZURE_OPENAI_BASE_URL,
        }
        
        return AzureOpenAIEmbeddings(**params, **kwargs)

