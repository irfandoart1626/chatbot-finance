from fastapi import FastAPI
from .api import router as api_router

app = FastAPI(
    title="Personal Finance API",
    description="API untuk pencatatan keuangan harian via Telegram Bot dan REST",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Personal Finance Chatbot API",
        "docs": "/docs",
        "telegram": "Bot is running..."
    }