from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

import os
from dotenv import load_dotenv

# Loading data from .env
load_dotenv()

# Retreiving secret key from env
RECAPTCHA_PUBLIC_KEY = os.getenv("RECAPTCHA_PUBLIC_KEY")

table_router = APIRouter()
templates = Jinja2Templates(directory="src/templates")

@table_router.get("/", response_class=HTMLResponse)
def show_table(request: Request):
    """
    Returning index page HTML
    """
    return templates.TemplateResponse("table.html", {"request": request, "recaptcha_public_key": RECAPTCHA_PUBLIC_KEY})
