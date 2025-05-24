# import asyncio
# import uvicorn
# from app import app
# from app.bot_handler import run_telegram_bot, shutdown_telegram_bot

# async def start_uvicorn():
#     config = uvicorn.Config(app, host="0.0.0.0", port=8000, loop="asyncio")
#     server = uvicorn.Server(config)
#     await server.serve()

# async def main():
#     bot_task = asyncio.create_task(run_telegram_bot())
#     api_task = asyncio.create_task(start_uvicorn())

#     try:
#         await asyncio.gather(bot_task, api_task)
#     except KeyboardInterrupt:
#         print("📴 CTRL+C diterima, menghentikan semua task...")
#         bot_task.cancel()
#         api_task.cancel()
#         await asyncio.gather(bot_task, api_task, return_exceptions=True)
#         await shutdown_telegram_bot()
#         print("✅ Semua layanan dihentikan.")
        
# if __name__ == "__main__":
#     try:
#         asyncio.run(main())
#     except KeyboardInterrupt:
#         print("✅ Shutdown selesai.")

# main.py
# import asyncio
# import logging
# import signal
# from contextlib import AsyncExitStack

# from app.bot_handler import run_telegram_bot, shutdown_telegram_bot
# import uvicorn
# from app import app  # FastAPI instance

# # Setup logging
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
# )
# logger = logging.getLogger(__name__)

# async def start_uvicorn():
#     """Mulai FastAPI server"""
#     config = uvicorn.Config(app, host="0.0.0.0", port=8000, loop="asyncio")
#     server = uvicorn.Server(config)
#     logger.info("🚀 FastAPI server dimulai...")
#     await server.serve()


# async def main():
#     # Handle SIGTERM/SIGINT untuk graceful shutdown
#     loop = asyncio.get_event_loop()

#     # Buat tasks
#     bot_task = asyncio.create_task(run_telegram_bot(), name="Telegram Bot Task")
#     api_task = asyncio.create_task(start_uvicorn(), name="FastAPI Server Task")

#     # Tangkap sinyal interupsi (Ctrl+C atau di cloud)
#     for sig in [signal.SIGTERM, signal.SIGINT]:
#         loop.add_signal_handler(sig, lambda: asyncio.create_task(shutdown_tasks(bot_task, api_task)))

#     logger.info("✅ Memulai layanan bot Telegram & FastAPI...")

#     try:
#         await asyncio.gather(bot_task, api_task)
#     except asyncio.CancelledError:
#         logger.info("🛑 Tasks dibatalkan, melanjutkan shutdown...")


# async def shutdown_tasks(bot_task, api_task):
#     """Gracefully shutdown semua task"""
#     logger.info("📴 Menerima sinyal shutdown. Menghentikan semua layanan...")
#     bot_task.cancel()
#     api_task.cancel()
    
#     try:
#         await asyncio.gather(bot_task, api_task, return_exceptions=True)
#     finally:
#         await shutdown_telegram_bot()
#         logger.info("✅ Semua layanan berhasil dihentikan.")


# if __name__ == "__main__":
#     try:
#         asyncio.run(main())
#     except KeyboardInterrupt:
#         logging.info("✅ Shutdown manual selesai.")













# main.py
import asyncio
import logging
import signal
from contextlib import AsyncExitStack

from app.bot_handler import run_telegram_bot, shutdown_telegram_bot
import uvicorn
from app import app  # FastAPI instance
from app.keepalive_task import keep_alive_task

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

async def start_uvicorn():
    """Mulai FastAPI server"""
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, loop="asyncio")
    server = uvicorn.Server(config)
    logger.info("🚀 FastAPI server dimulai...")
    await server.serve()


async def main():
    loop = asyncio.get_event_loop()

    # Buat tasks
    bot_task = asyncio.create_task(run_telegram_bot(), name="Telegram Bot Task")
    api_task = asyncio.create_task(start_uvicorn(), name="FastAPI Server Task")
    keepalive_task = asyncio.create_task(keep_alive_task(), name="Keep-Alive Checker")

    # Tangkap sinyal interupsi (Ctrl+C atau di cloud)
    for sig in [signal.SIGTERM, signal.SIGINT]:
        loop.add_signal_handler(sig, lambda: asyncio.create_task(shutdown_tasks(bot_task, api_task, keepalive_task)))

    logger.info("✅ Memulai layanan bot Telegram & FastAPI...")

    try:
        await asyncio.gather(bot_task, api_task, keepalive_task)
    except asyncio.CancelledError:
        logger.info("🛑 Tasks dibatalkan, melanjutkan shutdown...")


async def shutdown_tasks(*tasks):
    """Gracefully shutdown semua task"""
    logger.info("📴 Menerima sinyal shutdown. Menghentikan semua layanan...")
    for task in tasks:
        task.cancel()
    
    await asyncio.gather(*tasks, return_exceptions=True)
    await shutdown_telegram_bot()
    logger.info("✅ Semua layanan berhasil dihentikan.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("✅ Shutdown manual selesai.")