from telegram import Update
from telegram.ext import ContextTypes
from data import PDF_TEXT
from ai import ask_ai


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 AI Bot Ready!\nAsk me anything."
    )


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower()

    # 1. PDF search first
    if user_text in PDF_TEXT:
        await update.message.reply_text("📄 Found in document")
        return

    # 2. AI fallback
    try:
        answer = ask_ai(user_text)
        await update.message.reply_text(answer)
    except Exception as e:
        await update.message.reply_text("⚠️ AI error, try again later")