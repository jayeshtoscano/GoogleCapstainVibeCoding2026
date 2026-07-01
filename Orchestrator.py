from agents.gatekeeper import GatekeeperAgent
from agents.cache_agent import CacheAgent
from agents.prompt_refiner import PromptRefinerAgent
from agents.category_agent import CategoryAgent
from agents.llm_router import LLMRouterAgent
from agents.observability_agent import ObservabilityAgent


class Orchestrator:

    def __init__(self):

        self.gatekeeper = GatekeeperAgent()
        self.cache = CacheAgent()
        self.refiner = PromptRefinerAgent()
        self.category = CategoryAgent()
        self.router = LLMRouterAgent()
        self.obs = ObservabilityAgent()

    def run(self, prompt: str):

        start = self.obs.start_timer()

        # 1. Gatekeeper
        cleaned = self.gatekeeper.process(prompt)

        # 2. Cache check
        cached = self.cache.check(prompt)
        if cached:
            return cached

        # 3. Refiner
        refined = self.refiner.process(cleaned)

        # 4. Category detection
        category = self.category.classify(refined)

        # 5. LLM routing
        response = self.router.run(refined, category)

        # 6. Cache update
        self.cache.store(prompt, response)

        # 7. Observability
        self.obs.log(prompt, response, start)

        return {
            "input": prompt,
            "output": response,
            "category": category
        }
