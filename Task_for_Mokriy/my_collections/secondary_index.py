class SecondaryIndex:
    def __init__(self, index_key):
        self.index_key = index_key
        self.index = {}

    def add(self, key, value):
        if value not in self.index:
            self.index[value] = set()
        self.index[value].add(key)

    def remove(self, key, value):
        if value in self.index and key in self.index[value]:
            self.index[value].remove(key)
            if len(self.index[value]) == 0:
                del self.index[value]

    def get_keys(self, value):
        return list(self.index.get(value, set()))

    def clear(self):
        self.index = {}


