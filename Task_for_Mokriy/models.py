from pydantic import BaseModel

class PoolRequest(BaseModel):
    name: str

class SchemaRequest(BaseModel):
    pool_name: str
    schema_name: str

class CollectionRequest(BaseModel):
    pool_name: str
    schema_name: str
    collection_name: str
    container_type: str

class RecordRequest(BaseModel):
    pool_name: str
    key: str
    value: str

class UserIn(BaseModel):
    username: str
    password: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str
