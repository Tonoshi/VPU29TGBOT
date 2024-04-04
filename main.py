import logging
import os


from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [KeyboardButton('/start'), KeyboardButton('/hello')],
        [KeyboardButton('Share my location', request_location=True)],
        [KeyboardButton('Share my contact', request_contact=True)]

    ]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"Hello {update.effective_user.first_name}, I'm a bot!",
        reply_markup=reply_markup
    )


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}', )


async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lat = update.message.location.latitude
    lon = update.message.location.longitude

    await update.message.reply_text(f"lat = {lat}, lon = {lon}, Ось ваша висота та ширина. ")

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.contact.user_id
    first_name = update.message.contact.first_name
    last_name = update.message.contact.last_name
    await update.message.reply_text(
        f"""        user_id = {user_id}
        first_name = {first_name}        last_name = {last_name}
        """
    )



if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    hello_handler = CommandHandler("hello", hello)
    application.add_handler(hello_handler)

    location_handler = MessageHandler(filters.LOCATION, location)
    application.add_handler(location_handler)

    contact_handler = MessageHandler(filters.LOCATION, location)
    application.add_handler(location_handler)

    application.run_polling()
