import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TOKEN:
    raise Exception("Missing TELEGRAM_BOT_TOKEN")

if not OPENAI_API_KEY:
    raise Exception("Missing OPENAI_API_KEY")