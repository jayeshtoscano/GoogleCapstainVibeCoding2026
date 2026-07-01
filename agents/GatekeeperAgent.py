from utils.logger import get_logger

logger = get_logger("gatekeeper_agent")


class GatekeeperAgent:

    def __init__(
        self,
        observability_agent,
        cache_agent,
        lean_content_fn,
        constraint_fn,
        explicit_fn
    ):

        self.observability_agent = observability_agent
        self.cache_agent = cache_agent

        self.lean_content = lean_content_fn
        self.add_constraint = constraint_fn
        self.add_explicit = explicit_fn

    ########################################################
    # MAIN EXECUTION
    ########################################################

    def run(self, text: str):

        logger.info("GatekeeperAgent started")

        ####################################################
        # 1. SYSTEM HEALTH CHECK (NEW)
        ####################################################

        scores = self.observability_agent.project_scores()

        diligence = scores["diligence_score"]

        logger.info(f"Diligence Score = {diligence}")

        # If system is unhealthy → fallback mode
        if diligence < 60:

            logger.warning("System in degraded mode")

            return {
                "status": "degraded_system",
                "message": "Low system diligence detected",
                "diligence": scores,
                "fallback_response": text
            }

        ####################################################
        # 2. CACHE CHECK (FIXED: only once)
        ####################################################

        cache_result = self.cache_agent.check(text)

        if cache_result.get("cached"):

            logger.info("Cache hit")

            return cache_result

        ####################################################
        # 3. LEAN CONTENT PROCESSING
        ####################################################

        cleaned = self.lean_content(text)

        ####################################################
        # 4. CONSTRAINT ENRICHMENT
        ####################################################

        constraint = self.add_constraint(cleaned)

        prompt = constraint["updated_prompt"]

        ####################################################
        # 5. EXPLICIT ENRICHMENT
        ####################################################

        explicit = self.add_explicit(prompt)

        prompt = explicit["updated_prompt"]

        ####################################################
        # 6. RETURN FINAL PROMPT + METADATA
        ####################################################

        logger.info("GatekeeperAgent completed successfully")

        return {

            "prompt": prompt,

            "system_health": {

                "diligence": scores["diligence_score"],

                "status": scores["status"],

                "metrics": scores["metrics"]
            },

            "meta": {

                "constraint": constraint,

                "explicit": explicit
            }
        }
