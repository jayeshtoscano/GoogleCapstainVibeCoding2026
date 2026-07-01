"""
------------------------------------------------------------
LLM Client
------------------------------------------------------------

Responsibilities
- Read LLM configuration from config_loader
- Route requests to appropriate provider
- Handle fallback providers
- Log execution details
------------------------------------------------------------
"""

from typing import Dict, Callable

from ConfigLoader import get_skill_config
from utils.logger import logger


class LLMClient:

    def __init__(self):

        skill = get_skill_config()

        self.llms = skill.get("llms", {})
        self.routing = skill.get("routing", {})

        self.default_provider = self.routing.get(
            "default",
            "gemini"
        )

        self.providers: Dict[str, Callable] = {
            "openai": self._call_openai,
            "gemini": self._call_gemini,
            "claude": self._call_claude
        }

    ########################################################
    # Select Provider
    ########################################################

    def select_provider(self, category: str) -> str:

        provider = self.routing.get(
            category,
            self.default_provider
        )

        logger.info(
            f"Category [{category}] routed to provider [{provider}]"
        )

        return provider

    ########################################################
    # Public Method
    ########################################################

    def call(
        self,
        prompt: str,
        category: str = "default"
    ) -> str:

        provider = self.select_provider(category)

        try:

            return self._invoke(
                provider,
                prompt
            )

        except Exception as ex:

            logger.error(
                f"LLM [{provider}] failed. Error: {str(ex)}"
            )

            if provider != self.default_provider:

                logger.info(
                    f"Falling back to [{self.default_provider}]"
                )

                return self._invoke(
                    self.default_provider,
                    prompt
                )

            raise

    ########################################################
    # Internal Invocation
    ########################################################

    def _invoke(
        self,
        provider: str,
        prompt: str
    ) -> str:

        config = self.llms.get(provider)

        if config is None:

            raise ValueError(
                f"Configuration missing for provider [{provider}]"
            )

        model = config.get("model")

        logger.info(
            f"Invoking Provider={provider} Model={model}"
        )

        handler = self.providers.get(provider)

        if handler is None:

            raise ValueError(
                f"Provider [{provider}] not supported"
            )

        return handler(
            model=model,
            prompt=prompt,
            config=config
        )

    ########################################################
    # OpenAI
    ########################################################

    def _call_openai(
        self,
        model: str,
        prompt: str,
        config: dict
    ) -> str:

        logger.info(
            f"Calling OpenAI Model [{model}]"
        )

        # TODO:
        # Replace with OpenAI SDK

        return f"[OpenAI:{model}] {prompt}"

    ########################################################
    # Gemini
    ########################################################

    def _call_gemini(
        self,
        model: str,
        prompt: str,
        config: dict
    ) -> str:

        logger.info(
            f"Calling Gemini Model [{model}]"
        )

        # TODO:
        # Replace with Gemini SDK

        return f"[Gemini:{model}] {prompt}"

    ########################################################
    # Claude
    ########################################################

    def _call_claude(
        self,
        model: str,
        prompt: str,
        config: dict
    ) -> str:

        logger.info(
            f"Calling Claude Model [{model}]"
        )

        # TODO:
        # Replace with Anthropic SDK

        return f"[Claude:{model}] {prompt}"

    ########################################################
    # Health Check
    ########################################################

    def available_models(self):

        models = {}

        for provider, config in self.llms.items():

            models[provider] = {

                "model": config.get("model"),

                "enabled": config.get(
                    "enabled",
                    True
                )

            }

        return models
