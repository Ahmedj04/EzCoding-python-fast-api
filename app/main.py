from fastapi import FastAPI
from app.routes import run_code

app = FastAPI()

app.include_router(run_code.router)
