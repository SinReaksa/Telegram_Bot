import json
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from config import TOKEN

logging.basicConfig(level=logging.INFO)

# Load JSON data once
with open("data.json", "r", encoding="utf-8") as f:
    QA_DATA = json.load(f)


def find_answer(user_text: str):
    user_text = user_text.lower()

    for item in QA_DATA:
        question = item["question"].lower()
        keywords = [k.lower() for k in item.get("keywords", [])]

        # match by exact question OR keyword
        if user_text in question:
            return item["answer"]

        for kw in keywords:
            if kw in user_text:
                return item["answer"]

    return None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot ready ✅")


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    answer = find_answer(text)

    if answer:
        await update.message.reply_text(answer)
    else:
        await update.message.reply_text("❌ ខ្ញុំមិនមានចម្លើយសម្រាប់សំណួរនេះទេ")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()