from fastapi import FastAPI
from app.api.books import router

app = FastAPI(title="Library API")

app.include_router(router)