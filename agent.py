from pathlib import Path

import yaml

from lean_content import LeanContent


class GatekeeperAgent:

    def __init__(self):

        self.agent_context = Path("agent.md").read_text()

        self.skill = yaml.safe_load(
            Path("skill.md").read_text()
        )

    def execute(self, prompt):

        context = {
            "role": "Gatekeeper",
            "rules": self.agent_context,
            "skill": self.skill
        }

        cleaned = LeanContent(prompt)

        return {
            "context": context,
            "response": cleaned
        }
