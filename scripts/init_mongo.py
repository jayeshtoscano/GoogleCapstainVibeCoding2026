"""
------------------------------------------------------------
MongoDB Initialization Script
Gatekeeper AI Platform
------------------------------------------------------------

Purpose:
- Create required collections
- Create indexes
- Prepare schema structure for AI platform
------------------------------------------------------------
"""

from services.mongodb import db
from utils.logger import logger


##########################################################
# Required Collections
##########################################################

COLLECTIONS = [

    "cachelist",
    "constraints",
    "explicits",
    "llm_registry",
    "observability_metrics",
    "agent_cards",
    "mcp_tools",
    "skill_config"

]


##########################################################
# Index Setup
##########################################################

def create_indexes():

    logger.info("Creating MongoDB indexes...")

    # Cache optimization index
    db.cachelist.create_index("request")

    # Constraints lookup index
    db.constraints.create_index("keyword")

    # Explicit rules index
    db.explicits.create_index("keyword")

    # Observability index
    db.observability_metrics.create_index("timestamp")

    logger.info("Indexes created successfully")


##########################################################
# Collection Initialization
##########################################################

def init_collections():

    logger.info("Initializing MongoDB collections...")

    existing = db.list_collection_names()

    for col in COLLECTIONS:

        if col not in existing:

            db.create_collection(col)

            logger.info(f"Created collection: {col}")

        else:

            logger.info(f"Collection exists: {col}")


##########################################################
# Main Execution
##########################################################

if __name__ == "__main__":

    logger.info("Starting MongoDB initialization...")

    init_collections()

    create_indexes()

    logger.info("MongoDB initialization completed.")
