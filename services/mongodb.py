from pymongo import MongoClient
import yaml

from utils.logger import get_logger
from ConfigLoader import get_mongodb_config


##########################################################
# Logger (Centralized)
##########################################################

logger = get_logger("mongodb")


##########################################################
# Load configuration (NO direct file access)
##########################################################

def load_skill():

    # Prefer config_loader instead of reading file directly
    return get_mongodb_config()


SKILL = load_skill()


##########################################################
# MongoDB Singleton Client
##########################################################

class MongoDBClient:

    _client = None
    _db = None

    def __init__(self):

        if MongoDBClient._client is None:

            config = SKILL

            logger.info("Connecting to MongoDB...")

            MongoDBClient._client = MongoClient(
                config["connection_string"]
            )

            MongoDBClient._db = MongoDBClient._client[
                config["database"]
            ]

            logger.info(
                f"Connected to DB: {config['database']}"
            )

    def get_db(self):

        return MongoDBClient._db


##########################################################
# Global DB Instance
##########################################################

db_client = MongoDBClient()
db = db_client.get_db()


##########################################################
# Helper Functions
##########################################################

def get_collection(name: str):

    """
    Returns MongoDB collection safely.
    """

    if db is None:

        logger.error("MongoDB not initialized")

        raise Exception("MongoDB not initialized")

    return db[name]
