from app.services.mongodb import db

class CacheService:

    def __init__(self):
        self.col = db["cachelist"]

    def get(self, prompt):
        return self.col.find_one({"request": prompt})

    def set(self, prompt, response):
        self.col.insert_one({
            "request": prompt,
            "response": response
        })
