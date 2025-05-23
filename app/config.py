import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_CONFIG = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'chatbot_ai'),
        'port': int(os.getenv('DB_PORT', 3306)),
    }

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# import os
# from dotenv import load_dotenv

# load_dotenv()

# class Config:
#     DB_CONFIG = {
#         'host': os.getenv('DB_HOST'),
#         'user': os.getenv('DB_USER'),
#         'password': os.getenv('DB_PASSWORD'),
#         'database': os.getenv('DB_NAME'),
#         'port': int(os.getenv('DB_PORT', 5432)),
#     }

#     GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
#     TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
