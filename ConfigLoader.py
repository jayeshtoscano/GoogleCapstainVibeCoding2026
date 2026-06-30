"""
------------------------------------------------------------
Configuration Loader (Central Config Hub)
------------------------------------------------------------

Purpose:
- Load skill.md (LLM routing + Mongo config)
- Load agent.md (agent behavior rules)
- Provide unified config access for all agents
- Validate required fields at startup
- Support runtime config access
------------------------------------------------------------
"""

import yaml
import logging
from typing import Dict, Any

logger = logging.getLogger("config_loader")


##########################################################
# Config Loader Class
##########################################################

class ConfigLoader:

    def __init__(self):

        self._skill_config = None
        self._agent_config = None

        self.load_all_configs()

    ######################################################
    # Load YAML/MD configs
    ######################################################

    def _load_yaml_file(self, path: str) -> Dict[str, Any]:

        try:

            with open(path, "r") as f:

                return yaml.safe_load(f)

        except Exception as e:

            logger.error(f"Failed to load config {path}: {e}")
            return {}

    ######################################################
    # Load all configs
    ######################################################

    def load_all_configs(self):

        logger.info("Loading Gatekeeper configuration files...")

        self._skill_config = self._load_yaml_file(
            "config/skill.md"
        )

        self._agent_config = self._load_yaml_file(
            "config/agent.md"
        )

        self._validate_configs()

        logger.info("Configuration loading completed")

    ######################################################
    # Validation Layer
    ######################################################

    def _validate_configs(self):

        logger.info("Validating configuration integrity...")

        # Validate skill.md
        if not self._skill_config:

            raise Exception("skill.md is missing or invalid")

        if "llms" not in self._skill_config:

            raise Exception("skill.md must contain 'llms' section")

        if "mongodb" not in self._skill_config:

            raise Exception("skill.md must contain 'mongodb' section")

        # Validate agent.md
        if not self._agent_config:

            logger.warning("agent.md is missing or empty")

        logger.info("Configuration validation successful")

    ######################################################
    # Public Accessors
    ######################################################

    def get_skill(self) -> Dict[str, Any]:

        return self._skill_config

    def get_agent(self) -> Dict[str, Any]:

        return self._agent_config

    ######################################################
    # LLM Config Helpers
    ######################################################

    def get_llm_config(self) -> Dict[str, Any]:

        return self._skill_config.get("llms", {})

    def get_routing_config(self) -> Dict[str, Any]:

        return self._skill_config.get("routing", {})

    def get_mongodb_config(self) -> Dict[str, Any]:

        return self._skill_config.get("mongodb", {})

    ######################################################
    # Agent Rules Helper
    ######################################################

    def get_agent_rules(self) -> str:

        """
        Returns raw agent.md content as string
        (used by Gatekeeper reasoning layer)
        """

        return str(self._agent_config)

    ######################################################
    # Reload Support (Hot Reload Capability)
    ######################################################

    def reload(self):

        logger.info("Reloading configuration files...")

        self.load_all_configs()


##########################################################
# Global Singleton
##########################################################

config_loader = ConfigLoader()


##########################################################
# Convenience Functions
##########################################################

def get_skill_config():

    return config_loader.get_skill()


def get_agent_config():

    return config_loader.get_agent()


def get_llm_config():

    return config_loader.get_llm_config()


def get_mongodb_config():

    return config_loader.get_mongodb_config()


def get_agent_rules():

    return config_loader.get_agent_rules()


def reload_config():

    config_loader.reload()
