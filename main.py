import os
import logging

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [KeyboardButton('/hello')],
        [KeyboardButton('Share my location', request_location = True)]
    ]
    reply_text = ReplyKeyboardMarkup(keyboard, one_time_keyboard = True)
    await update.message.reply_text(f"How can i help you {update.effective_user.first_name}?", reply_markup=reply_text)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message.text.lower()
    last_name = update.effective_user.last_name

    if "hello" in message:
        if last_name:
            await update.message.reply_text(f"Hi {update.effective_user.first_name} {update.effective_user.last_name}")
        else:
            await update.message.reply_text(f"Hi {update.effective_user.first_name}")

    elif "bye" in message:
        if last_name:
            await update.message.reply_text(f"Bye {update.effective_user.first_name} {update.effective_user.last_name}")
        else:
            await update.message.reply_text(f"Bye {update.effective_user.first_name}")

    else:
        await update.message.reply_text(f"I don't know how to read this")


async def location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lat = update.message.location.latitude
    lon = update.message.location.longitude
    await update.message.reply_text(f"lat = {lat}, lon = {lon}")


app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("hello", hello))
location_handler = MessageHandler(filters.LOCATION, location)
app.add_handler(location_handler)
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
app.run_polling()