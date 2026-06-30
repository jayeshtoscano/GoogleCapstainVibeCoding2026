"""
------------------------------------------------------------
MongoDB Seed Script
Gatekeeper AI Platform
------------------------------------------------------------

Purpose:
- Insert baseline configuration data
- Enable immediate system usability
------------------------------------------------------------
"""

from datetime import datetime
from app.services.mongodb import db
from app.utils.logger import logger


##########################################################
# Seed Constraints Collection
##########################################################

def seed_constraints():

    db.constraints.delete_many({})

    db.constraints.insert_many([

        {
            "keyword": "summary",
            "audience": "general",
            "length": "short",
            "format": "paragraph"
        },

        {
            "keyword": "code",
            "audience": "developer",
            "length": "medium",
            "format": "structured"
        }

    ])

    logger.info("Seeded constraints")


##########################################################
# Seed Explicits Collection
##########################################################

def seed_explicits():

    db.explicits.delete_many({})

    db.explicits.insert_many([

        {
            "keyword": "api",
            "role": "developer assistant",
            "tasks": ["design", "document", "optimize"],
            "tools": ["fastapi", "mongodb", "llm"]
        }

    ])

    logger.info("Seeded explicits")


##########################################################
# Seed Cache Sample
##########################################################

def seed_cache():

    db.cachelist.delete_many({})

    db.cachelist.insert_one({

        "request": "hello world",

        "response": "Hello! How can I help you?",

        "responsetime": 120,

        "cacheddatetime": datetime.utcnow()

    })

    logger.info("Seeded cache list")


##########################################################
# Seed LLM Registry
##########################################################

def seed_llm_registry():

    db.llm_registry.delete_many({})

    db.llm_registry.insert_many([

        {
            "provider": "openai",
            "model": "gpt-4.1-mini",
            "cost": "low",
            "latency": "medium"
        },

        {
            "provider": "gemini",
            "model": "gemini-2.5-flash",
            "cost": "low",
            "latency": "low"
        },

        {
            "provider": "claude",
            "model": "claude-3-haiku",
            "cost": "medium",
            "latency": "low"
        }

    ])

    logger.info("Seeded LLM registry")


##########################################################
# Seed MCP Tools
##########################################################

def seed_mcp_tools():

    db.mcp_tools.delete_many({})

    db.mcp_tools.insert_many([

        {
            "tool": "LeanContent",
            "description": "Removes filler words and noise"
        },

        {
            "tool": "AddConstraint",
            "description": "Adds audience/format/length constraints"
        }

    ])

    logger.info("Seeded MCP tools")


##########################################################
# Seed Agent Card
##########################################################

def seed_agent_card():

    db.agent_cards.delete_many({})

    db.agent_cards.insert_one({

        "agent_name": "Gatekeeper",

        "version": "1.0",

        "capabilities": [
            "leaning",
            "routing",
            "cache",
            "observability"
        ],

        "created_at": datetime.utcnow()

    })

    logger.info("Seeded agent card")


##########################################################
# Main Seeder
##########################################################

if __name__ == "__main__":

    logger.info("Starting MongoDB seeding...")

    seed_constraints()
    seed_explicits()
    seed_cache()
    seed_llm_registry()
    seed_mcp_tools()
    seed_agent_card()

    logger.info("MongoDB seeding completed.")
