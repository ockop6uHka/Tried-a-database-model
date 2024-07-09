from persistence import PersistenceManager, AddCommand, UpdateCommand, DeleteCommand
from flyweight import StringPool
from index import IndexManager
from avl_tree import AVLTree
from red_black_tree import RedBlackTree
from btree import BTree
from my_collections.secondary_index import SecondaryIndex

class AssociativeContainer:
    def add(self, key, value):
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError

    def get_range(self, min_bound, max_bound):
        raise NotImplementedError

    def update(self, key, value):
        raise NotImplementedError

    def delete(self, key):
        raise NotImplementedError

class DataCollection(AssociativeContainer):
    def __init__(self, name):
        self.name = name
        self.data = {}
        self.persistence_manager = PersistenceManager()
        self.string_pool = StringPool()
        self.index_manager = IndexManager()

    def add(self, key, value):
        if key in self.data:
            raise KeyError("Key already exists.")
        value = self.string_pool.get_string(value)
        self.persistence_manager.execute_command(AddCommand(self, key, value))
        self.data[key] = value

    def get(self, key):
        return self.data.get(key, None)

    def get_range(self, min_bound, max_bound):
        return {k: v for k, v in self.data.items() if min_bound <= k <= max_bound}

    def update(self, key, value):
        if key not in self.data:
            raise KeyError("Key does not exist.")
        value = self.string_pool.get_string(value)
        self.persistence_manager.execute_command(UpdateCommand(self, key, value))
        self.data[key] = value

    def delete(self, key):
        if key in self.data:
            self.persistence_manager.execute_command(DeleteCommand(self, key))
            del self.data[key]
        else:
            raise KeyError("Key does not exist.")

    def get_state_at(self, timestamp):
        return self.persistence_manager.get_state_at(timestamp)

    def create_index(self, index_name):
        self.index_manager.create_index(index_name)

    def search_index(self, index_name, key):
        index = self.index_manager.get_index(index_name)
        if index:
            return index.search(key)
        else:
            raise KeyError("Index does not exist.")

    def search_index_range(self, index_name, min_key, max_key):
        index = self.index_manager.get_index(index_name)
        if index:
            return index.search_range(min_key, max_key)
        else:
            raise KeyError("Index does not exist.")

class DataSchema:
    def __init__(self, name):
        self.name = name
        self.collections = {}

    def add_collection(self, collection_name):
        if collection_name in self.collections:
            raise KeyError(f"Collection '{collection_name}' already exists in schema '{self.name}'.")
        self.collections[collection_name] = DataCollection(collection_name)

    def remove_collection(self, collection_name):
        if collection_name in self.collections:
            del self.collections[collection_name]
        else:
            raise KeyError(f"Collection '{collection_name}' does not exist in schema '{self.name}'.")

    def get_collection(self, collection_name):
        return self.collections.get(collection_name, None)

    def __repr__(self):
        return f"DataSchema(name='{self.name}', collections={self.collections})"

class DataPool:
    def __init__(self):
        self.schemas = {}

    def add_schema(self, schema_name):
        if schema_name in self.schemas:
            raise KeyError(f"Schema '{schema_name}' already exists in the data pool.")
        self.schemas[schema_name] = DataSchema(schema_name)

    def remove_schema(self, schema_name):
        if schema_name in self.schemas:
            del self.schemas[schema_name]
        else:
            raise KeyError(f"Schema '{schema_name}' does not exist in the data pool.")

    def get_schema(self, schema_name):
        return self.schemas.get(schema_name, None)

    def __repr__(self):
        return f"DataPool(schemas={self.schemas})"



class DataStorageSystem:
    def __init__(self):
        self.pools = {}
        self.secondary_indexes = {}  # Добавляем и инициализируем secondary_indexes

    def add_pool(self, pool_name):
        if pool_name not in self.pools:
            self.pools[pool_name] = {}

    def remove_pool(self, pool_name):
        if pool_name in self.pools:
            del self.pools[pool_name]

    def get_pool(self, pool_name):
        return self.pools.get(pool_name, None)

    def add_schema(self, pool_name, schema_name):
        pool = self.get_pool(pool_name)
        if pool:
            pool[schema_name] = {}

    def remove_schema(self, pool_name, schema_name):
        pool = self.get_pool(pool_name)
        if pool and schema_name in pool:
            del pool[schema_name]

    def get_schema(self, pool_name, schema_name):
        pool = self.get_pool(pool_name)
        if pool:
            return pool.get(schema_name, None)
        return None

    def add_collection(self, pool_name, schema_name, collection_name, container_type):
        schema = self.get_schema(pool_name, schema_name)
        if schema:
            if container_type == "AVL":
                container = AVLTree()
            elif container_type == "RED_BLACK":
                container = RedBlackTree()
            elif container_type == "BTREE":
                container = BTree()
            else:
                raise ValueError(f"Unsupported container type: {container_type}")

            schema[collection_name] = container
            self.create_secondary_index(pool_name, schema_name, collection_name)

    def remove_collection(self, pool_name, schema_name, collection_name):
        schema = self.get_schema(pool_name, schema_name)
        if schema and collection_name in schema:
            del schema[collection_name]
            self.remove_secondary_index(pool_name, schema_name, collection_name)

    def get_collection(self, pool_name, schema_name, collection_name):
        schema = self.get_schema(pool_name, schema_name)
        if schema:
            return schema.get(collection_name, None)
        return None

    def create_secondary_index(self, pool_name, schema_name, collection_name):
        if (pool_name, schema_name, collection_name) not in self.secondary_indexes:
            self.secondary_indexes[(pool_name, schema_name, collection_name)] = {}

    def get_secondary_index(self, pool_name, schema_name, collection_name):
        return self.secondary_indexes.get((pool_name, schema_name, collection_name), {})

    def add_secondary_index(self, pool_name, schema_name, collection_name, index_key):
        pool = self.get_pool(pool_name)
        if pool:
            schema = pool.get(schema_name)
            if schema:
                collection = schema.get(collection_name)
                if collection:
                    index = SecondaryIndex(index_key)
                    collection.set_secondary_index(index)
                    print(
                        f"Secondary index '{index_key}' added to collection '{collection_name}' in schema '{schema_name}' in pool '{pool_name}'.")
                else:
                    print(
                        f"Collection '{collection_name}' does not exist in schema '{schema_name}' in pool '{pool_name}'.")
            else:
                print(f"Schema '{schema_name}' does not exist in pool '{pool_name}'.")
        else:
            print(f"Pool '{pool_name}' does not exist.")

    def remove_secondary_index(self, pool_name, schema_name, collection_name):
        pool = self.get_pool(pool_name)
        if pool:
            schema = pool.get(schema_name)
            if schema:
                collection = schema.get(collection_name)
                if collection:
                    collection.remove_secondary_index()
                    print(
                        f"Secondary index removed from collection '{collection_name}' in schema '{schema_name}' in pool '{pool_name}'.")
                else:
                    print(
                        f"Collection '{collection_name}' does not exist in schema '{schema_name}' in pool '{pool_name}'.")
            else:
                print(f"Schema '{schema_name}' does not exist in pool '{pool_name}'.")
        else:
            print(f"Pool '{pool_name}' does not exist.")

    def print_pools(self):
        print("Current pools:")
        for pool_name, schemas in self.pools.items():
            print(f"- Pool: {pool_name}")
            for schema_name in schemas:
                print(f"  - Schema: {schema_name}")


