from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.api.verify import verify_router

#  Create FastAPI app
app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Including routes
# app.include_router(upload_router)
# app.include_router()

# Including api
app.include_router(verify_router)
