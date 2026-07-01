import re

from ConfigLoader import get_agent_config
from utils.logger import logger


class ReviewerAgent:

    def __init__(self):

        config = get_agent_config()

        reviewer = config.get("reviewer", {})

        self.min_length = reviewer.get("min_prompt_length", 20)
        self.max_length = reviewer.get("max_prompt_length", 4000)

        self.blocked_patterns = reviewer.get(
            "blocked_patterns",
            [
                r"ignore\s+previous\s+instructions",
                r"system\s+prompt",
                r"developer\s+instructions",
                r"<script.*?>",
                r"javascript:",
                r"drop\s+table",
                r"union\s+select",
                r"rm\s+-rf",
                r"shutdown",
                r"format\s+c:",
                r"sudo\s+rm"
            ]
        )

    def run(self, prompt: str):

        logger.info("Reviewer Agent executing")

        issues = []

        review_status = "approved"

        prompt = prompt.strip()

        ####################################################
        # Minimum length
        ####################################################

        if len(prompt) < self.min_length:

            issues.append(
                f"Prompt must contain at least {self.min_length} characters."
            )

        ####################################################
        # Maximum length
        ####################################################

        if len(prompt) > self.max_length:

            issues.append(
                f"Prompt exceeds maximum allowed length ({self.max_length})."
            )

        ####################################################
        # Unclear prompt detection
        ####################################################

        if "???" in prompt:

            issues.append("Prompt contains ambiguous content.")

        ####################################################
        # Malicious content detection
        ####################################################

        for pattern in self.blocked_patterns:

            if re.search(pattern, prompt, re.IGNORECASE):

                issues.append(
                    f"Potential malicious content detected ({pattern})."
                )

                review_status = "blocked"

        ####################################################
        # Return result
        ####################################################

        return {

            "status": review_status,

            "approved": review_status == "approved",

            "final_prompt": prompt,

            "issues": issues
        }
