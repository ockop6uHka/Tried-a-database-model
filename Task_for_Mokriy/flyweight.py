class StringFlyweight:
    _instances = {}

    @classmethod
    def get_instance(cls, string):
        if string not in cls._instances:
            cls._instances[string] = string
        return cls._instances[string]

class StringPool:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StringPool, cls).__new__(cls)
            cls._instance._pool = StringFlyweight()
        return cls._instance

    def get_string(self, string):
        return self._instance._pool.get_instance(string)
