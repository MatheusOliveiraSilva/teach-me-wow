from apps.common.settings import AZURE_OPENAI_BASE_URL, AZURE_OPENAI_API_KEY, OPENAI_API_VERSION

class LLMConfig:
    """
    LLMConfig is a class that configures the LLM for the application.
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

    def get_llm(self):
        """
        Returns the LLM based on the provider.
        """
        if self.provider == "azure":
            return self.get_azure_llm(**self.kwargs)
        else:
            raise ValueError(f"Provider {self.provider} not supported")

    def get_azure_llm(self, **kwargs):
        """Configures and returns an AzureOpenAI instance."""
        from langchain_openai import AzureChatOpenAI

        params = {
            "openai_api_key": self.AZURE_OPENAI_API_KEY,
            "openai_api_version": self.OPENAI_API_VERSION,
            "azure_endpoint": self.AZURE_OPENAI_BASE_URL,
        }

        kwargs = self.manage_openai_kwargs(kwargs)

        return AzureChatOpenAI(**params, **kwargs)

    def manage_openai_kwargs(self, kwargs):
        """
        Manages the OpenAI kwargs.

        This function is used to handle some cases, like:
            - Pydantic requires to add disabled_params to the kwargs, so we pop it from kwargs if are not using o1 or o3.
            - the reasoning_effort (only supported by o1, o3 and o4 family models, so we pop it from kwargs if are not using o1 or o3)
            - the think_mode (only supported by anthropic models, so we pop it from kwargs)
            - the temperature (if we are using o1 and o3 family models, we set the temperature to 1, because it's the only temperature supported by the models)
        """
        if kwargs.get("model", None) is None: kwargs["model"] = self.DEFAULT_OPENAI_MODEL

        if kwargs.get("model").startswith("o"):
            # constraints of o1, o3 and o4 family
            kwargs["temperature"] = 1
            kwargs["disabled_params"] = {"parallel_tool_calls": None}
        else:
            kwargs.pop("reasoning_effort", None)

        kwargs.pop("think_mode", None)
        return kwargs