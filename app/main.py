from fastapi import FastAPI
from .router import router as user_router

app = FastAPI(title="sample-performance-automation performance automation testing")
app.include_router(user_router)

@app.get("/")
def root():
    return {"message": "sample-performance-automation performance automation testing"}