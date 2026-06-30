class AgentOrchestrator:

    def __init__(self):

        self.gatekeeper = GatekeeperAgent()
        self.optimizer = OptimizerAgent()
        self.reviewer = ReviewerAgent()

    def run(self, text: str):

        logger.info("Orchestrator started")

        # 1. Gatekeeper
        gk_output = self.gatekeeper.run(text)

        # cache shortcut
        if isinstance(gk_output, dict) and gk_output.get("cached"):
            return gk_output

        prompt = gk_output["prompt"]

        # 2. Optimizer
        opt_output = self.optimizer.run(prompt)

        optimized = opt_output["optimized_prompt"]

        # 3. Reviewer
        rev_output = self.reviewer.run(optimized)

        final = rev_output["final_prompt"]

        # 4. Cache update
        UpdateCacheList(
            request=text,
            response=final,
            responsetime=0.0,
            cacheddatetime=datetime.utcnow()
        )

        return {
            "input": text,
            "gatekeeper": gk_output,
            "optimizer": opt_output,
            "reviewer": rev_output,
            "output": final
        }
