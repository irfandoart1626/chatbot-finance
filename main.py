# import asyncio
# import uvicorn
# from app import app
# from app.bot_handler import run_telegram_bot

# async def start_uvicorn():
#     config = uvicorn.Config(app, host="0.0.0.0", port=8000, loop="asyncio")
#     server = uvicorn.Server(config)
#     await server.serve()

# async def main():
#     await asyncio.gather(
#         run_telegram_bot(),
#         start_uvicorn()
#     )

# if __name__ == "__main__":
#     asyncio.run(main())

# import asyncio
# import uvicorn
# from app import app
# from app.bot_handler import run_telegram_bot

# async def start_uvicorn():
#     config = uvicorn.Config(app, host="0.0.0.0", port=8000, loop="asyncio")
#     server = uvicorn.Server(config)
#     await server.serve()

# async def main():
#     bot_task = asyncio.create_task(run_telegram_bot())
#     api_task = asyncio.create_task(start_uvicorn())

#     try:
#         await asyncio.gather(bot_task, api_task)
#     except asyncio.CancelledError:
#         print("❗️ Task dibatalkan")
#     except KeyboardInterrupt:
#         print("📴 CTRL+C diterima, menghentikan semua task...")
#         bot_task.cancel()
#         api_task.cancel()
#         await asyncio.gather(bot_task, api_task, return_exceptions=True)
#         print("✅ Semua layanan dihentikan.")

# if __name__ == "__main__":
#     try:
#         asyncio.run(main())
#     except KeyboardInterrupt:
#         print("✅ Shutdown selesai.")



import asyncio
import uvicorn
from app import app
from app.bot_handler import run_telegram_bot, shutdown_telegram_bot

async def start_uvicorn():
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, loop="asyncio")
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    bot_task = asyncio.create_task(run_telegram_bot())
    api_task = asyncio.create_task(start_uvicorn())

    try:
        await asyncio.gather(bot_task, api_task)
    except KeyboardInterrupt:
        print("📴 CTRL+C diterima, menghentikan semua task...")
        bot_task.cancel()
        api_task.cancel()
        await asyncio.gather(bot_task, api_task, return_exceptions=True)
        await shutdown_telegram_bot()
        print("✅ Semua layanan dihentikan.")
        
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("✅ Shutdown selesai.")
