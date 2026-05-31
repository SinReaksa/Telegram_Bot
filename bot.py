import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from config import TOKEN
from handlers import start, reply, handle_pdf, send_pdf

# logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("pdf", send_pdf))
    app.add_handler(MessageHandler(filters.Document.PDF, handle_pdf))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

    print("Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()