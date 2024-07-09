from datetime import datetime

class Command:
    def execute(self):
        raise NotImplementedError

class AddCommand(Command):
    def __init__(self, collection, key, value):
        self.collection = collection
        self.key = key
        self.value = value

    def execute(self):
        self.collection.data[self.key] = self.value

    def undo(self):
        del self.collection.data[self.key]

class UpdateCommand(Command):
    def __init__(self, collection, key, value):
        self.collection = collection
        self.key = key
        self.new_value = value
        self.old_value = None

    def execute(self):
        if self.key in self.collection.data:
            self.old_value = self.collection.data[self.key]
            self.collection.data[self.key] = self.new_value
        else:
            raise KeyError("Key does not exist.")

    def undo(self):
        if self.old_value is not None:
            self.collection.data[self.key] = self.old_value
        else:
            raise RuntimeError("Cannot undo operation without previous state.")

class DeleteCommand(Command):
    def __init__(self, collection, key):
        self.collection = collection
        self.key = key
        self.deleted_value = None

    def execute(self):
        if self.key in self.collection.data:
            self.deleted_value = self.collection.data[self.key]
            del self.collection.data[self.key]
        else:
            raise KeyError("Key does not exist.")

    def undo(self):
        if self.deleted_value is not None:
            self.collection.data[self.key] = self.deleted_value
        else:
            raise RuntimeError("Cannot undo operation without previous state.")

class PersistenceManager:
    def __init__(self):
        self.history = []

    def execute_command(self, command):
        command.execute()
        self.history.append((datetime.now(), command))

    def get_state_at(self, timestamp):
        state = {}
        for time, command in self.history:
            if time > timestamp:
                break
            if isinstance(command, AddCommand):
                state[command.key] = command.value
            elif isinstance(command, UpdateCommand):
                state[command.key] = command.new_value
            elif isinstance(command, DeleteCommand):
                if command.key in state:
                    del state[command.key]
        return state

    def rollback_to(self, timestamp):
        new_history = []
        for time, command in self.history:
            if time <= timestamp:
                command.undo()
            else:
                new_history.append((time, command))
        self.history = new_history
