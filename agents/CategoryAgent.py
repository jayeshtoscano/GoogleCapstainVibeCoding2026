class CategoryAgent:

    def classify(self, text: str):

        if "code" in text:
            return "coding"

        if "explain" in text:
            return "reasoning"

        return "general"
