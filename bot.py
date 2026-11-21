import logging
import os
import re
from typing import Final

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)


# Load environment variables from the .env file
load_dotenv()

TOKEN: Final[str | None] = os.getenv("TOKEN")
BOT_USERNAME: Final[str] = os.getenv(
    "BOT_USERNAME", "@bunaet_bot"
).strip()


# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


# -------------------------
# COMMAND HANDLERS
# -------------------------

async def start_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    message = update.effective_message

    if message is None:
        return

    await message.reply_text(
        "Selam! 👋\n"
        "I'm Buna, your student academic assistant.\n\n"
        "I'm being developed to help students organize "
        "their academic activities.\n\n"
        "Use /help to see the available commands."
    )


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    message = update.effective_message

    if message is None:
        return

    await message.reply_text(
        "Here are my available commands:\n\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/custom - Test a custom command\n\n"
        "You can also send me simple messages."
    )


async def custom_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    message = update.effective_message

    if message is None:
        return

    await message.reply_text("This is a custom command!")


# -------------------------
# TEXT RESPONSE LOGIC
# -------------------------

def handle_response(text: str) -> str:
    text = text.lower()

    if "hello" in text:
        return "Hey there!"

    if "how are you" in text:
        return "I'm good, thanks for asking!"

    if "bye" in text:
        return "See you later!"

    return "I don't understand you yet."


# -------------------------
# MESSAGE HANDLER
# -------------------------

async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    message = update.effective_message
    chat = update.effective_chat

    if message is None or chat is None or message.text is None:
        return

    text = message.text

    logger.info(
        'User %s in %s: "%s"',
        update.effective_user.id if update.effective_user else "Unknown",
        chat.type,
        text,
    )

    # In groups, respond only when the bot is mentioned
    # or someone replies directly to one of its messages.
    if chat.type in ("group", "supergroup"):

        is_mentioned = BOT_USERNAME.lower() in text.lower()

        is_reply_to_bot = (
            message.reply_to_message is not None
            and message.reply_to_message.from_user is not None
            and message.reply_to_message.from_user.id == context.bot.id
        )

        if not is_mentioned and not is_reply_to_bot:
            return

        # Remove the bot's username before processing the message.
        if is_mentioned:
            text = re.sub(
                re.escape(BOT_USERNAME),
                "",
                text,
                flags=re.IGNORECASE,
            ).strip()

    response = handle_response(text)

    logger.info("Bot response: %s", response)

    await message.reply_text(response)


# -------------------------
# ERROR HANDLER
# -------------------------

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    logger.error(
        "An error occurred while processing an update: %s",
        context.error,
    )


# -------------------------
# MAIN APPLICATION
# -------------------------

def main() -> None:

    # Make sure the Telegram token exists.
    if not TOKEN:
        raise RuntimeError(
            "TOKEN is missing. Add TOKEN=your_bot_token "
            "to your .env file."
        )

    application = Application.builder().token(TOKEN).build()

    # Register commands
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("custom", custom_command))

    # Register text messages, excluding commands.
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message,
        )
    )

    # Register error handler
    application.add_error_handler(error_handler)

    logger.info("Starting Buna bot...")

    # Start polling Telegram for updates.
    application.run_polling(poll_interval=3)


if __name__ == "__main__":
    main()