
import os
from fastapi import APIRouter, Form, HTTPException
from dotenv import load_dotenv
import httpx

# Loading data from .env
load_dotenv()

# Retreiving secret key from env

verify_router = APIRouter()

RECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY")

@verify_router.post("/verify-captcha")
async def verify_captcha(captcha_response: str = Form(...)):
    """
    Проверяет Google reCAPTCHA ответ пользователя.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={
                "secret": RECAPTCHA_SECRET_KEY,
                "response": captcha_response
            }
        )
        result = response.json()

    if not result.get("success"):
        raise HTTPException(status_code=400, detail="Ошибка верификации reCAPTCHA")

    return {"message": "reCAPTCHA верифицирована успешно"}