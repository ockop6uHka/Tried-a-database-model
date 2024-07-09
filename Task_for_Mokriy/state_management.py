import pickle


class StateManager:
    def __init__(self, data_storage_system):
        self.data_storage_system = data_storage_system

    def save_state(self, filename):
        state_to_save = {
            'pools': self.data_storage_system.pools,
            'secondary_indexes': self.data_storage_system.secondary_indexes,
            'schemas': self.serialize_schemas(),
            'collections': self.serialize_collections()
        }
        with open(filename, 'wb') as f:
            pickle.dump(state_to_save, f)

    def load_state(self, filename):
        with open(filename, 'rb') as f:
            saved_state = pickle.load(f)
            self.data_storage_system.pools = saved_state.get('pools', {})
            self.data_storage_system.secondary_indexes = saved_state.get('secondary_indexes', {})
            self.deserialize_schemas(saved_state.get('schemas', {}))
            self.deserialize_collections(saved_state.get('collections', {}))

    def serialize_schemas(self):
        serialized_schemas = {}
        for pool_name, pool in self.data_storage_system.pools.items():
            serialized_schemas[pool_name] = {}
            for schema_name, schema in pool.items():
                serialized_schemas[pool_name][schema_name] = list(schema.keys())
        return serialized_schemas

    def deserialize_schemas(self, serialized_schemas):
        for pool_name, schemas in serialized_schemas.items():
            if pool_name in self.data_storage_system.pools:
                for schema_name, collections in schemas.items():
                    self.data_storage_system.pools[pool_name][schema_name] = {}
                    for collection_name in collections:
                        self.data_storage_system.pools[pool_name][schema_name][collection_name] = {}

    def serialize_collections(self):
        serialized_collections = {}
        for pool_name, pool in self.data_storage_system.pools.items():
            serialized_collections[pool_name] = {}
            for schema_name, schema in pool.items():
                serialized_collections[pool_name][schema_name] = {}
                for collection_name, collection in schema.items():
                    serialized_collections[pool_name][schema_name][collection_name] = list(collection.keys())
        return serialized_collections

    def deserialize_collections(self, serialized_collections):
        for pool_name, schemas in serialized_collections.items():
            if pool_name in self.data_storage_system.pools:
                for schema_name, collections in schemas.items():
                    if schema_name in self.data_storage_system.pools[pool_name]:
                        self.data_storage_system.pools[pool_name][schema_name] = {}
                        for collection_name in collections:
                            self.data_storage_system.pools[pool_name][schema_name][collection_name] = {}
