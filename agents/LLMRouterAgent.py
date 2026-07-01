from ConfigLoader import get_skill_config
from utils.logger import get_logger
from services.LLMClient import LLMClient


logger = get_logger("llm_policy_router")


class LLMRouterAgent:

    def __init__(self):

        self.skill = get_skill_config()

        # Policy engine config
        self.policies = self.skill.get("policies", {})

        self.llm_client = LLMClient()

    ########################################################
    # MAIN ENTRY
    ########################################################

    def run(self, prompt: str, category: str = "default"):

        logger.info(
            f"Policy routing started | category={category}"
        )

        category = (category or "default").lower()

        policy = self.policies.get(
            category,
            self.policies.get("default", {})
        )

        selected_provider = self._evaluate_policy(
            prompt,
            category,
            policy
        )

        logger.info(
            f"Selected provider={selected_provider} for category={category}"
        )

        return self.llm_client.call(
            prompt=prompt,
            category=category,
            provider_override=selected_provider
        )

    ########################################################
    # POLICY ENGINE CORE
    ########################################################

    def _evaluate_policy(self, prompt: str, category: str, policy: dict):

        providers = policy.get("providers", [])
        rules = policy.get("rules", {})
        fallback = policy.get("fallback", "gemini")

        prompt_lower = prompt.lower()

        ####################################################
        # 1. Keyword-based routing rules
        ####################################################

        keyword_rules = rules.get("keyword", {})

        for keyword, provider in keyword_rules.items():

            if keyword.lower() in prompt_lower:

                logger.info(
                    f"Keyword match '{keyword}' → {provider}"
                )

                return provider

        ####################################################
        # 2. Complexity-based routing
        ####################################################

        if len(prompt) > rules.get("complex_prompt_threshold", 2000):

            provider = rules.get(
                "complex_provider",
                "claude"
            )

            logger.info("Complex prompt detected")

            return provider

        ####################################################
        # 3. Category-based preferred provider order
        ####################################################

        if providers:

            for provider in providers:

                if self._is_provider_available(provider):

                    logger.info(
                        f"Selected preferred provider={provider}"
                    )

                    return provider

        ####################################################
        # 4. Fallback
        ####################################################

        logger.warning(
            f"No policy match found. Falling back to {fallback}"
        )

        return fallback

    ########################################################
    # Provider Health Check (simplified stub)
    ########################################################

    def _is_provider_available(self, provider: str) -> bool:

        llms = self.skill.get("llms", {})

        config = llms.get(provider, {})

        return config.get("enabled", True)
