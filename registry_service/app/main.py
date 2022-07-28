from fastapi import FastAPI
from app.api import secure

app = FastAPI(
    version='1.0.0',
    openapi_url='/api/v1/registry/openapi.json',
    docs_url='/api/v1/registry/docs',
    redoc_url='/api/v1/registry/redoc'
)

app.include_router(
    secure.secure,
    prefix='/api/v1/authenticate',
    tags=['Authenticate']
)
