
import logging
import os
import random

from dotenv import load_dotenv
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from messages import STUDY_TIPS, MOTIVATIONS


load_dotenv()
TOKEN = os.getenv("TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

KEYBOARD = ReplyKeyboardMarkup(
    [
        ["📚 Study Tip", "🌟 Motivate Me"],
        ["ℹ️ Help", "🏠 Main Menu"],
    ],
    resize_keyboard=True,
    input_field_placeholder="Choose an option...",
)

def inline_keyboard(callback_data):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔄 Another",
                callback_data=callback_data,
            )
        ]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "Selam! 👋\n\n"
        "Welcome to Buna Mini Bot! ☕\n"
        "Choose an option below to get started.",
        reply_markup=KEYBOARD,
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "☕ Buna Mini Bot Commands\n\n"
        "/start - Start the bot\n"
        "/help - Show help\n"
        "/tip - Get a study tip\n"
        "/motivate - Get motivation\n\n"
        "You can also use the buttons below!"
    )


async def send_random_message(update, messages, title, callback_data):
    message = random.choice(messages)

    await update.effective_message.reply_text(
        f"{title}\n\n{message}",
        reply_markup=inline_keyboard(callback_data),
    )

async def tip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_random_message(
        update,
        STUDY_TIPS,
        "📚 Study Tip",
        "another_tip",
    )


async def motivate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_random_message(
        update,
        MOTIVATIONS,
        "🌟 Motivation",
        "another_motivation",
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.effective_message.text

    if text == "📚 Study Tip":
        await tip(update, context)

    elif text == "🌟 Motivate Me":
        await motivate(update, context)

    elif text == "ℹ️ Help":
        await help_command(update, context)

    elif text == "🏠 Main Menu":
        await start(update, context)
        
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Update error: %s", context.error)

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()

    if query.data == "another_tip":
        messages = STUDY_TIPS
        title = "📚 Study Tip"
        callback_data = "another_tip"

    elif query.data == "another_motivation":
        messages = MOTIVATIONS
        title = "🌟 Motivation"
        callback_data = "another_motivation"

    else:
        return

    message = random.choice(messages)

    await query.edit_message_text(
        f"{title}\n\n{message}",
        reply_markup=inline_keyboard(callback_data),
    )
def main():
    if not TOKEN:
        raise RuntimeError("TOKEN is missing from your .env file.")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("tip", tip))
    app.add_handler(CommandHandler("motivate", motivate))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button_handler))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_error_handler(error_handler)

    logger.info("Starting Buna Mini Bot...")
    app.run_polling(poll_interval=3)


if __name__ == "__main__":
    main()
