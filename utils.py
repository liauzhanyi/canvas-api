import pickle

CACHE_FILENAME = "cache.pkl"

class Cacher:
    def __init__(self, cache={}):
        self.cache = cache

    def update(self, key, value):
        self.cache[key] = value
        print(f"Updated cache with {key} = {value}\n")
        return self

    def read(self, key):
        try:
            return self.cache[key]
        except KeyError:
            print(f"Key {key} not found in cache\n")
            return None
    
    def store(self):
        print("Writing cache to file...")
        with open(CACHE_FILENAME, "wb") as f:
            pickle.dump(self.cache, f)
        print("Done\n")
        return self
    
    def load(self):
        print("Loading cache from file...")
        try:
            with open(CACHE_FILENAME, "rb") as f:
                self.cache = pickle.load(f)
            print("Done\n")
        except FileNotFoundError:
            self.cache = {}
        return self