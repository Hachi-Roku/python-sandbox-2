from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# from src.api.verify import verify_router
from src.api.lottery import lottery_router

#  Create FastAPI app
app = FastAPI(
      title="Lottery API",
    description="API for managing lottery tickets.",
    version="1.0.0"
    )

# Mount static files
# app.mount("/static", StaticFiles(directory="static"), name="static")

# Including routes
# app.include_router(upload_router)
# app.include_router()

# Including api
app.include_router(lottery_router, prefix="/api", tags=["Lottery"])
