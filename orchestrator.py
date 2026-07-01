from agents.gatekeeper import GatekeeperAgent
from agents.cache_agent import CacheAgent
from agents.prompt_refiner import PromptRefinerAgent
from agents.category_agent import CategoryAgent
from agents.llm_router import LLMRouterAgent
from agents.observability_agent import ObservabilityAgent
from services.lean_content import LeanContent
from services.constraints import AddConstraint
from services.explicit import AddExplicit
from services.prompt_service import PromptService

class Orchestrator:

    def __init__(self):

        self.cache = CacheAgent()
        self.refiner = PromptRefinerAgent()
        self.category = CategoryAgent()
        self.router = LLMRouterAgent()
        self.obs = ObservabilityAgent()
        self.reviewer = ReviewerAgent()
        self.prompt_service = PromptService()
        self.gatekeeper = GatekeeperAgent(observability_agent=self.observability_agent,cache_agent=self.cache_agent,prompt_service=self.prompt_service)
        
    def run(self, prompt: str):

        start = self.obs.start_timer()

        # 1. Gatekeeper
        
        # Gatekeeper calls review agent to check rules and security acting as structured as well as semantic gating
        review = self.reviewer.run(prompt)

        if not review["approved"]:

            return {
                "status": "rejected",
                "issues": review["issues"]
            }

        prompt = review["final_prompt"]

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
