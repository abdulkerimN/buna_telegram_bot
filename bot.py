from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes,MessageHandler, filters

from dotenv import load_dotenv
import os

load_dotenv()

TOKEN: Final = os.getenv("TOKEN")
BOT_USERNAME: Final = "@bunaet_bot"  # replace with your bot's username

# commands

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("selam! I am buna bot")
    
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("How can I help you today?")
    
async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("this is custom command")
    
# handle responses
def handle_response(text: str) -> str:
    text = text.lower()
  
    if "hello" in text:
        return "hey there!"
    if "how are you" in text:
        return "I'm good, thanks for asking!"
    if "bye" in text:
        return "see you later!"
    return "I don't understand you."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text
    
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == "group":
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
      response: str = handle_response(text)

    print("Bot:", response)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")
    

if __name__== "__main__":
    print("starting bot...")
    app = Application.builder().token(TOKEN).build()
    

    # commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))
    
    # messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    # errors
    app.add_error_handler(error)
    
    # polls the bot
    print("bot started")
    app.run_polling(poll_interval=3)