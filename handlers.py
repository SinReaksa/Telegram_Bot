import logging
from telegram import Update
from telegram.ext import ContextTypes
from utils import find_answer


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "សូមស្វាគមន៍!\n\n"
        "សួរអំពី KPI, AL, ច្បាប់ឈប់សម្រាក..."
    )


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text
    logging.info("Incoming message: %s", text)

    answer = find_answer(text)

    if answer:
        logging.info("Replying with answer: %s", answer)
        await update.message.reply_text(answer)
    else:
        logging.info("No matching answer found")
        await update.message.reply_text(
            "សូមទោស ខ្ញុំមិនស្គាល់សំណួរនេះទេ។"
        )