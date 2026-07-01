from utils.logger import get_logger
from services.prompt_service import PromptService


logger = get_logger("gatekeeper_agent")


class GatekeeperAgent:

    def __init__(
        self,
        observability_agent,
        cache_agent,
        prompt_service: PromptService
    ):

        self.observability_agent = observability_agent
        self.cache_agent = cache_agent
        self.prompt_service = prompt_service

    ########################################################
    # MAIN FLOW
    ########################################################

    def run(self, text: str):

        logger.info("GatekeeperAgent started")

        ####################################################
        # 1. SYSTEM HEALTH CHECK
        ####################################################

        scores = self.observability_agent.project_scores()

        if scores["diligence_score"] < 60:

            return {
                "status": "degraded_system",
                "message": "Low system diligence detected",
                "diligence": scores
            }

        ####################################################
        # 2. CACHE CHECK
        ####################################################

        cache_result = self.cache_agent.check(text)

        if cache_result.get("cached"):

            return cache_result

        ####################################################
        # 3. PROMPT PROCESSING (NOW CLEAN & CENTRALIZED)
        ####################################################

        cleaned = self.prompt_service.lean_content(text)

        constraint = self.prompt_service.add_constraint(cleaned)

        explicit = self.prompt_service.add_explicit(
            constraint["updated_prompt"]
        )

        final_prompt = explicit["updated_prompt"]

        ####################################################
        # 4. RETURN RESPONSE
        ####################################################

        return {

            "prompt": final_prompt,

            "system_health": scores,

            "meta": {

                "constraint": constraint,

                "explicit": explicit
            }
        }
