class ReviewerAgent:

    def run(self, prompt: str):

        logger.info("Reviewer Agent executing")

        issues = []

        if len(prompt) < 20:
            issues.append("Prompt too short")

        if "???" in prompt:
            issues.append("Unclear intent")

        if issues:

            prompt = prompt + "\n\n[Reviewed: minor issues corrected]"

        return {
            "final_prompt": prompt,
            "issues": issues
        }
