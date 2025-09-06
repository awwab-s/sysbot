import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
PREFIX = os.getenv("PREFIX")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))
CHAT_API_KEY = os.getenv("CHAT_API_KEY")
CHAT_MODEL = os.getenv("CHAT_MODEL")

