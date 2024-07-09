class SecondaryIndex:
    def __init__(self):
        self.index = {}

    def add(self, key, value):
        self.index[key] = value

    def update(self, key, value):
        if key in self.index:
            self.index[key] = value

    def delete(self, key):
        if key in self.index:
            del self.index[key]

    def search(self, key):
        return self.index.get(key, None)

    def search_range(self, min_key, max_key):
        return {k: v for k, v in self.index.items() if min_key <= k <= max_key}

class IndexManager:
    def __init__(self):
        self.indices = {}

    def create_index(self, index_name):
        if index_name in self.indices:
            raise KeyError("Index already exists.")
        self.indices[index_name] = SecondaryIndex()

    def get_index(self, index_name):
        return self.indices.get(index_name, None)
