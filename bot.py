import json
import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from config import TOKEN

logging.basicConfig(level=logging.INFO)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "faq.json")

with open(FILE_PATH, "r", encoding="utf-8") as f:
    QA_DATA = json.load(f)


def find_answer(text: str):
    text = text.strip().lower()

    for item in QA_DATA:
        question = item["question"].strip().lower()
        keywords = [k.lower() for k in item.get("keywords", [])]

        if text == question:
            return item["answer"]

        for kw in keywords:
            if kw in text:
                return item["answer"]

    return None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is running ✅")


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    answer = find_answer(text)

    if answer:
        await update.message.reply_text(answer)
    else:
        await update.message.reply_text("❌ No answer found")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()