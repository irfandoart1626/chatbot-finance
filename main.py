import asyncio
import logging
from app.bot_handler import run_telegram_bot, shutdown_telegram_bot
import uvicorn
from app import app
from app.keepalive_task import keep_alive_task

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

shutdown_event = asyncio.Event()

async def start_uvicorn():
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, loop="asyncio")
    server = uvicorn.Server(config)
    logger.info("🚀 FastAPI server dimulai...")
    await server.serve()

async def wait_for_shutdown_command():
    # Menunggu input Enter untuk memicu shutdown
    await asyncio.to_thread(input, "Tekan Enter untuk keluar dan hentikan layanan...\n")
    shutdown_event.set()

async def main():
    bot_task = asyncio.create_task(run_telegram_bot(), name="Telegram Bot Task")
    api_task = asyncio.create_task(start_uvicorn(), name="FastAPI Server Task")
    keepalive_task = asyncio.create_task(keep_alive_task(), name="Keep-Alive Checker")
    shutdown_wait_task = asyncio.create_task(wait_for_shutdown_command(), name="Shutdown Wait Task")

    logger.info("✅ Memulai layanan bot Telegram & FastAPI...")

    await shutdown_event.wait()

    logger.info("📴 Menerima perintah shutdown. Menghentikan semua layanan...")
    # Cancel semua task kecuali shutdown_wait_task yang sudah selesai
    for task in [bot_task, api_task, keepalive_task]:
        task.cancel()
    await asyncio.gather(bot_task, api_task, keepalive_task, return_exceptions=True)

    await shutdown_telegram_bot()
    logger.info("✅ Semua layanan berhasil dihentikan.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("✅ Shutdown manual selesai.")
