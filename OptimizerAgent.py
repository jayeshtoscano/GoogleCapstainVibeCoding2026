class OptimizerAgent:

    def run(self, prompt: str):

        logger.info("Optimizer Agent executing")

        structured = AddArchitected(prompt)

        return {
            "optimized_prompt": structured
        }
