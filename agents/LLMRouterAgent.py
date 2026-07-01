from ConfigLoader import get_skill_config
from utils.logger import get_logger
from services.llm_client import LLMClient


logger = get_logger("llm_router")


class LLMRouterAgent:

    def __init__(self):

        self.skill = get_skill_config()

        # Routing policy from configuration
        self.routing_map = self.skill.get("routing", {})

        self.llm_client = LLMClient()

        # Default fallback category/provider
        self.default_category = self.routing_map.get(
            "default",
            "general"
        )

    ########################################################
    # MAIN ENTRY
    ########################################################

    def run(self, prompt: str, category: str):

        logger.info(
            f"Routing request | category={category}"
        )

        # Normalize category
        category = (category or "").lower()

        match category:

            ################################################
            # CODING CATEGORY
            ################################################
            case "coding":

                provider = self.routing_map.get(
                    "coding",
                    "openai"
                )

                return self.llm_client.call(
                    prompt=prompt,
                    category="coding"
                )

            ################################################
            # REASONING CATEGORY
            ################################################
            case "reasoning":

                provider = self.routing_map.get(
                    "reasoning",
                    "claude"
                )

                return self.llm_client.call(
                    prompt=prompt,
                    category="reasoning"
                )

            ################################################
            # ANALYSIS CATEGORY (NEW)
            ################################################
            case "analysis":

                provider = self.routing_map.get(
                    "analysis",
                    "gemini"
                )

                return self.llm_client.call(
                    prompt=prompt,
                    category="analysis"
                )

            ################################################
            # SUMMARIZATION CATEGORY (optional extension)
            ################################################
            case "summarization":

                provider = self.routing_map.get(
                    "summarization",
                    "gemini"
                )

                return self.llm_client.call(
                    prompt=prompt,
                    category="summarization"
                )

            ################################################
            # DEFAULT CATEGORY
            ################################################
            case _:

                logger.warning(
                    f"Unknown category '{category}', using default"
                )

                return self.llm_client.call(
                    prompt=prompt,
                    category=self.default_category
                )
