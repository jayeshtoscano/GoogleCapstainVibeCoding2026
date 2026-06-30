class LLMRouterAgent:

    def run(self, prompt, category):

        if category == "coding":
            return "OpenAI GPT response"

        if category == "reasoning":
            return "Claude response"

        return "Gemini response"
