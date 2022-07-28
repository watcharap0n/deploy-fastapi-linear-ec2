from fastapi import FastAPI
from app.api import model

app = FastAPI(
    version='1.0.0',
    openapi_url='/api/v1/ml/openapi.json',
    docs_url='/api/v1/ml/docs',
    redoc_url='/api/v1/ml/redoc'
)

app.include_router(
    model.router,
    prefix='/api/v1/ml',
    tags=['Model Linear Regression']
)


@app.get('/')
async def index():
    return 'hello my first page machine learning.'
