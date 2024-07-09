class AssociativeContainer:
    def __init__(self):
        pass

    def add(self, key, value):
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError

    def update(self, key, value):
        raise NotImplementedError

    def delete(self, key):
        raise NotImplementedError
