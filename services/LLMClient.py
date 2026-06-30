import requests
import yaml
import logging

logger = logging.getLogger("llm_client")


##########################################################
# Load skill.md
##########################################################

def load_skill():
    with open("config/skill.md", "r") as f:
        return yaml.safe_load(f)


SKILL = load_skill()


##########################################################
# LLM Client Class
##########################################################

class LLMClient:

    def __init__(self):

        self.llms = SKILL.get("llms", {})
        self.routing = SKILL.get("routing", {})
        self.fallback = self.routing.get("default", "gemini")

    ######################################################
    # Select Model Based on Category
    ######################################################

    def select_llm(self, category: str):

        return self.routing.get(
            category,
            self.fallback
        )

    ######################################################
    # Call LLM Provider
    ######################################################

    def call(self, prompt: str, category: str = "default"):

        provider = self.select_llm(category)

        config = self.llms.get(provider)

        if not config:

            raise Exception(
                f"LLM config not found for {provider}"
            )

        model = config.get("model")

        logger.info(
            f"Using LLM: {provider} | Model: {model}"
        )

        # -----------------------------
        # OpenAI-style generic request
        # -----------------------------

        if provider == "openai":

            return self._call_openai(model, prompt)

        elif provider == "gemini":

            return self._call_gemini(model, prompt)

        elif provider == "claude":

            return self._call_claude(model, prompt)

        else:

            raise Exception(
                f"Unsupported provider: {provider}"
            )

    ######################################################
    # OpenAI
    ######################################################

    def _call_openai(self, model, prompt):

        # placeholder for real API key integration
        return f"[OpenAI:{model}] {prompt}"

    ######################################################
    # Gemini
    ######################################################

    def _call_gemini(self, model, prompt):

        return f"[Gemini:{model}] {prompt}"

    ######################################################
    # Claude
    ######################################################

    def _call_claude(self, model, prompt):

        return f"[Claude:{model}] {prompt}"
