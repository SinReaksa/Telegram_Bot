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
    text = text.lower().strip()
    logging.info("find_answer: text=%s", text)

    for item in QA_DATA:
        q = item["question"].lower().strip()
        if text == q:
            logging.info("find_answer: exact match question=%s", item["question"])
            return item["answer"]

    for item in QA_DATA:
        q = item["question"].lower().strip()
        if q in text or text in q:
            logging.info("find_answer: substring match question=%s", item["question"])
            return item["answer"]

    for item in QA_DATA:
        keywords = [k.lower() for k in item.get("keywords", [])]
        if keywords and all(kw in text for kw in keywords):
            logging.info("find_answer: keyword match question=%s keywords=%s", item["question"], keywords)
            return item["answer"]

    logging.info("find_answer: no match")
    return None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is running ✅")


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    logging.info("Incoming message: %s", text)
    answer = find_answer(text)

    if answer:
        logging.info("Replying with answer: %s", answer)
        await update.message.reply_text(answer)
    else:
        logging.info("No matching answer found for: %s", text)
        await update.message.reply_text("❌ No answer found")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()