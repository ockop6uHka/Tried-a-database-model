from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import FileResponse
from commands import CommandProcessor
from data_storage import DataStorageSystem
from models import PoolRequest, SchemaRequest, CollectionRequest, RecordRequest
from auth import get_current_active_user, User
from users import router as user_router
import logging
import uuid

app = FastAPI()

command_processor = CommandProcessor(DataStorageSystem())

app.include_router(user_router)

logging.basicConfig(filename='logs/app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logging.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logging.info(f"Request processed with status code {response.status_code}")
    return response

def generate_request_id() -> str:
    return str(uuid.uuid4())


@app.post("/add_pool/")
async def add_pool(request: PoolRequest, current_user: User = Depends(get_current_active_user)):
    print(f"Current user: {current_user.username}, Role: {current_user.role}")
    if current_user.role not in ["administrator", "editor"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    command_processor.process_command(f"ADD_POOL {request.name}")
    logging.info(f"Pool {request.name} added by {current_user.username}")
    return {"message": f"Pool {request.name} added."}

@app.post("/remove_pool/")
async def remove_pool(request: PoolRequest, current_user: User = Depends(get_current_active_user)):
    if current_user.role not in ["administrator", "editor"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    command_processor.process_command(f"REMOVE_POOL {request.name}")
    logging.info(f"Pool {request.name} removed by {current_user.username}")
    return {"message": f"Pool {request.name} removed."}

@app.post("/add_schema/")
async def add_schema(request: SchemaRequest, current_user: User = Depends(get_current_active_user)):
    if current_user.role not in ["administrator", "editor"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    command_processor.process_command(f"ADD_SCHEMA {request.pool_name} {request.schema_name}")
    logging.info(f"Schema {request.schema_name} added to pool {request.pool_name} by {current_user.username}")
    return {"message": f"Schema {request.schema_name} added to pool {request.pool_name}."}

@app.post("/remove_schema/")
async def remove_schema(request: SchemaRequest, current_user: User = Depends(get_current_active_user)):
    if current_user.role not in ["administrator", "editor"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    command_processor.process_command(f"REMOVE_SCHEMA {request.pool_name} {request.schema_name}")
    logging.info(f"Schema {request.schema_name} removed from pool {request.pool_name} by {current_user.username}")
    return {"message": f"Schema {request.schema_name} removed from pool {request.pool_name}."}

@app.post("/add_collection/")
async def add_collection(request: CollectionRequest, current_user: User = Depends(get_current_active_user)):
    if current_user.role not in ["administrator", "editor"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    command_processor.process_command(f"ADD_COLLECTION {request.pool_name} {request.schema_name} {request.collection_name} {request.container_type}")
    logging.info(f"Collection {request.collection_name} added to schema {request.schema_name} in pool {request.pool_name} by {current_user.username}")
    return {"message": f"Collection {request.collection_name} added to schema {request.schema_name} in pool {request.pool_name}."}

@app.post("/remove_collection/")
async def remove_collection(request: CollectionRequest, current_user: User = Depends(get_current_active_user)):
    if current_user.role not in ["administrator", "editor"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    command_processor.process_command(f"REMOVE_COLLECTION {request.pool_name} {request.schema_name} {request.collection_name}")
    logging.info(f"Collection {request.collection_name} removed from schema {request.schema_name} in pool {request.pool_name} by {current_user.username}")
    return {"message": f"Collection {request.collection_name} removed from schema {request.schema_name}."}

@app.post("/add_record_avl/")
async def add_record_avl(request: RecordRequest, current_user: User = Depends(get_current_active_user)):
    if current_user.role not in ["administrator", "editor", "user"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    command_processor.process_command(f"ADD_RECORD_AVL {request.pool_name} {request.key} {request.value}")
    logging.info(f"Record added to AVL collection in pool {request.pool_name} by {current_user.username}")
    return {"message": f"Record added to AVL collection in pool {request.pool_name}."}

@app.post("/add_record_red_black/")
async def add_record_red_black(request: RecordRequest, current_user: User = Depends(get_current_active_user)):
    if current_user.role not in ["administrator", "editor", "user"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    command_processor.process_command(f"ADD_RECORD_RED_BLACK {request.pool_name} {request.key} {request.value}")
    logging.info(f"Record added to Red-Black collection in pool {request.pool_name} by {current_user.username}")
    return {"message": f"Record added to Red-Black collection in pool {request.pool_name}."}

@app.get("/get_record_avl/")
async def get_record_avl(pool_name: str, key: str, current_user: User = Depends(get_current_active_user)):
    if current_user.role not in ["administrator", "editor", "user"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    command_processor.process_command(f"GET_RECORD_AVL {pool_name} {key}")
    logging.info(f"Record retrieved from AVL collection in pool {pool_name} by {current_user.username}")
    return {"message": f"Record from AVL collection in pool {pool_name} retrieved."}

@app.get("/get_record_red_black/")
async def get_record_red_black(pool_name: str, key: str, current_user: User = Depends(get_current_active_user)):
    if current_user.role not in ["administrator", "editor", "user"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    command_processor.process_command(f"GET_RECORD_RED_BLACK {pool_name} {key}")
    logging.info(f"Record retrieved from Red-Black collection in pool {pool_name} by {current_user.username}")
    return {"message": f"Record from Red-Black collection in pool {pool_name} retrieved."}

@app.get("/get_record_btree/")
async def get_record_btree(pool_name: str, key: str, current_user: User = Depends(get_current_active_user)):
    if current_user.role not in ["administrator", "editor", "user"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    command_processor.process_command(f"GET_RECORD_BTREE {pool_name} {key}")
    logging.info(f"Record retrieved from B-Tree collection in pool {pool_name} by {current_user.username}")
    return {"message": f"Record from B-Tree collection in pool {pool_name} retrieved."}

@app.get("/")
async def read_index():
    return FileResponse("static/index.html")

@app.get("/register")
async def read_register():
    return FileResponse("static/register.html")

@app.get("/login")
async def read_login():
    return FileResponse("static/login.html")

@app.get("/storage")
async def read_storage():
    return FileResponse("static/storage.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
