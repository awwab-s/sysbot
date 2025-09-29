import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
APPLICATION_ID = os.getenv("APPLICATION_ID")
PREFIX = os.getenv("PREFIX")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))
CHAT_API_KEY = os.getenv("CHAT_API_KEY")
CHAT_MODEL = os.getenv("CHAT_MODEL")

QURAN_CLIENT_ID = os.getenv("QURAN_CLIENT_ID")
QURAN_CLIENT_SECRET = os.getenv("QURAN_CLIENT_SECRET")
QURAN_TOKEN_URL = os.getenv("QURAN_TOKEN_URL")
QURAN_BASE_URL = os.getenv("QURAN_BASE_URL")