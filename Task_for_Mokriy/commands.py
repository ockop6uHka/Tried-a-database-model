import os
from state_management import StateManager

class CommandProcessor:
    def __init__(self, data_storage_system):
        self.data_storage_system = data_storage_system
        self.state_manager = StateManager(data_storage_system)

        self.command_mapping = {
            "ADD_POOL": self.add_pool,
            "REMOVE_POOL": self.remove_pool,
            "ADD_SCHEMA": self.add_schema,
            "REMOVE_SCHEMA": self.remove_schema,
            "ADD_COLLECTION": self.add_collection,
            "REMOVE_COLLECTION": self.remove_collection,
            "ADD_RECORD_AVL": self.add_record_avl,
            "ADD_RECORD_RED_BLACK": self.add_record_red_black,
            "GET_RECORD_AVL": self.get_record_avl,
            "GET_RECORD_RED_BLACK": self.get_record_red_black,
            "GET_RECORD_BTREE": self.get_record_btree,
            "ADD_RECORD_BTREE": self.add_record_btree,
            "SAVE_STATE": self.save_state,
            "LOAD_STATE": self.load_state
        }

    def process_command(self, command):
        parts = command.strip().split()
        cmd_type = parts[0]

        try:
            if cmd_type in self.command_mapping:
                self.command_mapping[cmd_type](*parts[1:])
            else:
                print(f"Unknown command: {cmd_type}")

        except Exception as e:
            print(f"Error processing command: {e}")

    def add_pool(self, pool_name):
        if self.data_storage_system.get_pool(pool_name):
            print(f"Pool {pool_name} already exists.")
        else:
            self.data_storage_system.add_pool(pool_name)
            print(f"Pool {pool_name} added.")

    def remove_pool(self, pool_name):
        if self.data_storage_system.get_pool(pool_name):
            self.data_storage_system.remove_pool(pool_name)
            print(f"Pool {pool_name} removed.")
        else:
            print(f"Pool {pool_name} does not exist.")

    def add_schema(self, pool_name, schema_name):
        pool = self.data_storage_system.get_pool(pool_name)
        if pool:
            pool.add_schema(schema_name)
            print(f"Schema {schema_name} added to pool {pool_name}.")
        else:
            print(f"Pool {pool_name} does not exist.")

    def remove_schema(self, pool_name, schema_name):
        pool = self.data_storage_system.get_pool(pool_name)
        if pool:
            pool.remove_schema(schema_name)
            print(f"Schema {schema_name} removed from pool {pool_name}.")
        else:
            print(f"Pool {pool_name} does not exist.")

    def add_collection(self, pool_name, schema_name, collection_name, collection_type="default"):
        pool = self.data_storage_system.get_pool(pool_name)
        if pool:
            schema = pool.get_schema(schema_name)
            if schema:
                schema.add_collection(collection_name, collection_type)
                print(f"Collection {collection_name} added to schema {schema_name} in pool {pool_name}.")
            else:
                print(f"Schema {schema_name} does not exist in pool {pool_name}.")
        else:
            print(f"Pool {pool_name} does not exist.")

    def remove_collection(self, pool_name, schema_name, collection_name):
        pool = self.data_storage_system.get_pool(pool_name)
        if pool:
            schema = pool.get_schema(schema_name)
            if schema:
                schema.remove_collection(collection_name)
                print(f"Collection {collection_name} removed from schema {schema_name} in pool {pool_name}.")
            else:
                print(f"Schema {schema_name} does not exist in pool {pool_name}.")
        else:
            print(f"Pool {pool_name} does not exist.")

    def add_record_avl(self, pool_name, key, *value_parts):
        value = ' '.join(value_parts)
        pool = self.data_storage_system.get_pool(pool_name)
        if pool:
            schema = pool.get_schema("avl_schema")  # Assuming schema name for AVL
            if schema:
                collection = schema.get_collection("avl_collection")  # Assuming collection name for AVL
                if collection:
                    collection.add(key, value)
                    print(f"Record added to AVL collection in pool {pool_name}.")
                else:
                    print("AVL collection does not exist.")
            else:
                print("AVL schema does not exist.")
        else:
            print(f"Pool {pool_name} does not exist.")

    def add_record_red_black(self, pool_name, key, *value_parts):
        value = ' '.join(value_parts)
        pool = self.data_storage_system.get_pool(pool_name)
        if pool:
            schema = pool.get_schema("red_black_schema")  # Assuming schema name for Red-Black
            if schema:
                collection = schema.get_collection("red_black_collection")  # Assuming collection name for Red-Black
                if collection:
                    collection.add(key, value)
                    print(f"Record added to Red-Black collection in pool {pool_name}.")
                else:
                    print("Red-Black collection does not exist.")
            else:
                print("Red-Black schema does not exist.")
        else:
            print(f"Pool {pool_name} does not exist.")

    def add_record_btree(self, pool_name, key, *value_parts):
        value = ' '.join(value_parts)
        pool = self.data_storage_system.get_pool(pool_name)
        if pool:
            schema = pool.get_schema("btree")  # Assuming schema name for Red-Black
            if schema:
                collection = schema.get_collection("btree")  # Assuming collection name for Red-Black
                if collection:
                    collection.add(key, value)
                    print(f"Record added to btree collection in pool {pool_name}.")
                else:
                    print("btree collection does not exist.")
            else:
                print("btree schema does not exist.")
        else:
            print(f"Pool {pool_name} does not exist.")

    def get_record_btree(self, pool_name, key):
        pool = self.data_storage_system.get_pool(pool_name)
        if pool:
            schema = pool.get_schema("btree")
            if schema:
                collection = schema.get_collection("btree_collection")
                if collection:
                    value = collection.get(key)
                    print(f"Record from AVL collection in pool {pool_name}: {value}")
                else:
                    print("btree collection does not exist.")
            else:
                print("btree schema does not exist.")
        else:
            print(f"Pool {pool_name} does not exist.")

    def get_record_avl(self, pool_name, key):
        pool = self.data_storage_system.get_pool(pool_name)
        if pool:
            schema = pool.get_schema("avl_schema")
            if schema:
                collection = schema.get_collection("avl_collection")
                if collection:
                    value = collection.get(key)
                    print(f"Record from AVL collection in pool {pool_name}: {value}")
                else:
                    print("AVL collection does not exist.")
            else:
                print("AVL schema does not exist.")
        else:
            print(f"Pool {pool_name} does not exist.")

    def get_record_red_black(self, pool_name, key):
        pool = self.data_storage_system.get_pool(pool_name)
        if pool:
            schema = pool.get_schema("red_black_schema")
            if schema:
                collection = schema.get_collection("red_black_collection")
                if collection:
                    value = collection.get(key)
                    print(f"Record from Red-Black collection in pool {pool_name}: {value}")
                else:
                    print("Red-Black collection does not exist.")
            else:
                print("Red-Black schema does not exist.")
        else:
            print(f"Pool {pool_name} does not exist.")

    def save_state(self, filename):
        self.state_manager.save_state(filename)
        print(f"State saved to {filename}.")

    def load_state(self, filename):
        self.state_manager.load_state(filename)
        print(f"State loaded from {filename}.")
        print("Current state restored.")
        print("Note: Current state in memory will be replaced with the loaded state.")

    def process_commands_from_file(self, filepath):
        if not os.path.exists(filepath):
            print(f"File {filepath} does not exist.")
            return

        with open(filepath, 'r') as file:
            for line in file:
                self.process_command(line)

    def interactive_mode(self):
        print("Entering interactive mode. Type 'exit' to quit.")
        while True:
            command = input("Enter command: ")
            if command.lower() == 'exit':
                break
            self.process_command(command)
