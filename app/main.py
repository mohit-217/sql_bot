from fastapi import FastAPI, HTTPException,Form,Depends, Security
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from classes.db_ops import db_operations
from fastapi.security import APIKeyHeader
from fastapi.security.api_key import APIKey
import os
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, replace with specific domains if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

project_key = os.getenv("project_key")
API_KEY_NAME = os.getenv("API_KEY")
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)
def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header==project_key:
        return api_key_header
    else:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    
@app.get("/")
async def read_root(api_key: APIKey = Depends(get_api_key)):
    return {"message": "Welcome!"}


# Standard API: Health check
@app.get("/health")
async def health_check(api_key: APIKey = Depends(get_api_key)):
    return {"status": "healthy"}


# Standard API: Version
@app.get("/version")
async def get_version(api_key: APIKey = Depends(get_api_key)):
    return {"version": "1.0.0"}

@app.post("/perform_db_operation")
async def perform_db_ops(user_query: str = Form(...), api_key: APIKey = Depends(get_api_key)):
    try:
        obj=db_operations(user_query)
        return {"Response":obj.perform_db_operation()}
    except Exception as e:
        print(e)
        return "Error Encounterd View stacktrace for detailed Explanation"
@app.post("/check_database_table")
async def check_latest_query_record(api_key: APIKey = Depends(get_api_key)):
    try:
        response=db_operations.get_latest_record()
        return {"Latest record":response}
    except Exception as e:
        print(e)
        return "Error Encounterd View stacktrace for detailed Explanation"