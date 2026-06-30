import yaml
from pymongo import MongoClient


def load_skill():

    with open("skill.md", "r") as f:
        return yaml.safe_load(f)


skill = load_skill()

client = MongoClient(
    skill["mongodb"]["connection_string"]
)

db = client[
    skill["mongodb"]["database"]
]


def load_collection(collection_name):

    collection = db[
        skill["mongodb"]["collections"][collection_name]
    ]

    return [x["value"] for x in collection.find()]
