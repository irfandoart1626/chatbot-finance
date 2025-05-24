# app/keepalive_task.py
import asyncio
import httpx
from app.config import Config

KEEP_ALIVE_URL = "https://chatbot-finance-production.up.railway.app/api/keep-alive"
INTERVAL = 10  # Detik

async def keep_alive_task():
    """
    Task async yang terus memanggil /keep-alive setiap INTERVAL detik
    """
    async with httpx.AsyncClient() as client:
        while True:
            try:
                response = await client.get(KEEP_ALIVE_URL)
                if response.status_code == 200:
                    print("🟢 Keep-alive berhasil:", response.json())
                else:
                    print("🔴 Keep-alive gagal:", response.status_code)
            except Exception as e:
                print("⚠️ Error saat keep-alive:", str(e))
            
            await asyncio.sleep(INTERVAL)