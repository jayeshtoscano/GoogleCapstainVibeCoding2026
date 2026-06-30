from pymongo import MongoClient
import yaml
import logging

logger = logging.getLogger("mongodb")


##########################################################
# Load skill.md configuration
##########################################################

def load_skill():
    with open("config/skill.md", "r") as f:
        return yaml.safe_load(f)


SKILL = load_skill()


##########################################################
# MongoDB Singleton Client
##########################################################

class MongoDBClient:

    _client = None
    _db = None

    def __init__(self):

        if MongoDBClient._client is None:

            config = SKILL["mongodb"]

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

        raise Exception("MongoDB not initialized")

    return db[name]
