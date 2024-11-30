from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.api.lottery import lottery_router
from src.api.verify import verify_router

from src.routes.table import table_router

#  Create FastAPI app
app = FastAPI(
      title="Lottery API",
    description="API for managing lottery tickets.",
    version="1.0.0"
    )

templates = Jinja2Templates(directory="templates")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Including routes
app.include_router(table_router, prefix="")

# Including api
app.include_router(lottery_router, prefix="/api", tags=["Lottery"])
app.include_router(verify_router, prefix="/api", tags=["Verify"])
