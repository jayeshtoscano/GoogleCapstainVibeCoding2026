from services.cache_service import CacheService

class CacheAgent:

    def __init__(self):
        self.cache = CacheService()

    def check(self, prompt):
        return self.cache.get(prompt)

    def store(self, prompt, response):
        self.cache.set(prompt, response)
