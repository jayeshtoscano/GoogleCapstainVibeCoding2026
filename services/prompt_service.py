import re
from typing import Dict, Any

from app.utils.logger import get_logger
from app.db.mongodb import get_collection


logger = get_logger("prompt_service")


class PromptService:

    def __init__(self):

        ########################################################
        # MongoDB collections
        ########################################################

        self.constraints_col = get_collection("constraints")
        self.explicit_col = get_collection("explicits")

        ########################################################
        # Static cleaning rules (can later move to MongoDB)
        ########################################################

        self.fillers = [
            "um", "uh", "like", "you know", "actually"
        ]

        self.hedges = [
            "maybe", "perhaps", "sort of", "kind of", "i think"
        ]

        self.courtesies = [
            "please", "thank you", "thanks", "appreciate it"
        ]

        self.gestures = [
            "🙂", "😊", "👍", "👋"
        ]

    ########################################################
    # 1. LEAN CONTENT
    ########################################################

    def lean_content(self, text: str) -> str:

        logger.info("Executing LeanContent")

        original = text

        text = self._remove_patterns(text, self.fillers)
        text = self._remove_patterns(text, self.hedges)
        text = self._remove_patterns(text, self.courtesies)
        text = self._remove_patterns(text, self.gestures)

        text = re.sub(r"\s+", " ", text).strip()

        logger.info("LeanContent completed")

        return text

    ########################################################
    # 2. ADD CONSTRAINT
    ########################################################

    def add_constraint(self, text: str) -> Dict[str, Any]:

        logger.info("Executing AddConstraint")

        match = self.constraints_col.find_one(
            {
                "keyword": {
                    "$regex": text,
                    "$options": "i"
                }
            }
        )

        if not match:

            logger.info("No constraint match found")

            return {
                "updated_prompt": text,
                "audience": None,
                "length": None,
                "format": None
            }

        updated_prompt = self._apply_constraint(text, match)

        return {
            "updated_prompt": updated_prompt,
            "audience": match.get("audience"),
            "length": match.get("length"),
            "format": match.get("format")
        }

    ########################################################
    # 3. ADD EXPLICIT
    ########################################################

    def add_explicit(self, text: str) -> Dict[str, Any]:

        logger.info("Executing AddExplicit")

        match = self.explicit_col.find_one(
            {
                "keyword": {
                    "$regex": text,
                    "$options": "i"
                }
            }
        )

        if not match:

            logger.info("No explicit match found")

            return {
                "updated_prompt": text,
                "role": None,
                "tasks": None,
                "tools": None
            }

        updated_prompt = self._apply_explicit(text, match)

        return {
            "updated_prompt": updated_prompt,
            "role": match.get("role"),
            "tasks": match.get("tasks"),
            "tools": match.get("tools")
        }

    ########################################################
    # INTERNAL HELPERS
    ########################################################

    def _remove_patterns(self, text: str, patterns: list) -> str:

        for p in patterns:

            text = re.sub(
                rf"\b{re.escape(p)}\b",
                "",
                text,
                flags=re.IGNORECASE
            )

        return text

    ########################################################

    def _apply_constraint(self, text: str, rule: dict) -> str:

        return (
            f"{text}\n\n"
            f"[Audience: {rule.get('audience')}]\n"
            f"[Length: {rule.get('length')}]\n"
            f"[Format: {rule.get('format')}]"
        )

    ########################################################

    def _apply_explicit(self, text: str, rule: dict) -> str:

        return (
            f"{text}\n\n"
            f"[Role: {rule.get('role')}]\n"
            f"[Tasks: {rule.get('tasks')}]\n"
            f"[Tools: {rule.get('tools')}]"
        )
