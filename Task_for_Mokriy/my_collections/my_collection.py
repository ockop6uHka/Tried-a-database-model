class Collection:
    def __init__(self, name):
        self.name = name
        self.data = {}
        self.secondary_index = None

    def set_secondary_index(self, index):
        self.secondary_index = index

    def get_secondary_index(self):
        return self.secondary_index

    def remove_secondary_index(self):
        self.secondary_index = None

    def add(self, key, value):
        self.data[key] = value

        if self.secondary_index:
            self.secondary_index.add(key, value)

    def get(self, key):
        return self.data.get(key, None)

    def remove(self, key):
        if key in self.data:
            del self.data[key]
