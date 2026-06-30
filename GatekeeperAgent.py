class GatekeeperAgent:

    def run(self, text: str):

        if CheckReusability(text)["cached"]:
            return CheckReusability(text)

        cleaned = LeanContent(text)

        constraint = AddConstraint(cleaned)
        prompt = constraint["updated_prompt"]

        explicit = AddExplicit(prompt)
        prompt = explicit["updated_prompt"]

        return {
            "prompt": prompt,
            "meta": {
                "constraint": constraint,
                "explicit": explicit
            }
        }
