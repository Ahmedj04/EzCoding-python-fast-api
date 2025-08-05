from fastapi import FastAPI
from app.routes import run_code

app = FastAPI()

app.include_router(run_code.router)


@app.get("/")
async def root():
    return {"EzCoding FastAPI Python API"}


# Render expects host=0.0.0.0 and port=$PORT
if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
