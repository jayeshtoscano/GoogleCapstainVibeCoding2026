"""
------------------------------------------------------------
Agent Card Module (Secure Agent Discovery Layer)
------------------------------------------------------------

Purpose:
- Define agent identity
- Expose capabilities safely
- Control tool exposure
- Support partner onboarding (B2B integration)
- Enable MCP-compatible discovery
------------------------------------------------------------
"""

from typing import Dict, Any
import yaml
import json
from utils.logger import get_logger

logger = get_logger("agent_card")


##########################################################
# Load Agent Metadata (agent.md / config)
##########################################################

def load_agent_config():

    """
    Loads agent definition from file system.
    """

    try:

        with open("config/agent_card.json", "r") as f:

            return json.load(f)

    except Exception as e:

        logger.error(f"Failed to load agent card: {e}")

        return {}


##########################################################
# Agent Card Core Class
##########################################################

class AgentCard:

    """
    Secure representation of the Gatekeeper Agent
    exposed to external organizations.
    """

    def __init__(self):

        self.config = load_agent_config()

        self.name = self.config.get(
            "name",
            "Gatekeeper AI Agent"
        )

        self.visibility = self.config.get(
            "visibility",
            "private"
        )

        self.capabilities = self.config.get(
            "capabilities",
            []
        )

        self.tools = self.config.get(
            "capabilities",
            []
        )

        self.version = self.config.get(
            "version",
            "1.0"
        )

        self.security = self.config.get(
            "security",
            {
                "auth": "none",
                "rate_limit": "unlimited"
            }
        )

    ######################################################
    # Public Agent Card (Safe Exposure)
    ######################################################

    def get_public_card(self) -> Dict[str, Any]:

        """
        Returns sanitized agent information
        for external organizations.
        """

        logger.info("Generating public agent card")

        return {

            "agent_name": self.name,

            "version": self.version,

            "visibility": self.visibility,

            "capabilities": self.capabilities,

            "exposed_tools": self.tools,

            "security_model": {

                "auth": self.security.get("auth"),

                "rate_limit": self.security.get("rate_limit")

            }

        }

    ######################################################
    # Internal Full Card (Admin Use Only)
    ######################################################

    def get_internal_card(self) -> Dict[str, Any]:

        """
        Full internal metadata view.
        """

        logger.info("Generating internal agent card")

        return {

            "agent_name": self.name,

            "version": self.version,

            "visibility": self.visibility,

            "capabilities": self.capabilities,

            "tools": self.tools,

            "security": self.security,

            "raw_config": self.config

        }


##########################################################
# Global Instance
##########################################################

agent_card = AgentCard()


##########################################################
# Helper Functions (FastAPI Integration)
##########################################################

def get_agent_card(public: bool = True):

    """
    Returns agent card based on access level.
    """

    if public:

        return agent_card.get_public_card()

    return agent_card.get_internal_card()
