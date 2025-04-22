from telegram import Update
from telegram.ext import (
    Application,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters
)
from telegram.error import TelegramError

import os
from dotenv import load_dotenv
import re

from collector import fetch_articles
from aggregator import summarize_news


load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_BOT_NAME = os.getenv("TELEGRAM_BOT_NAME")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

import logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def command_start(update, context):
    """
    Handle /start command.
    """
    await update.message.reply_text("Tag me with keywords (e.g., @Bot_Username News Keywords) to get a news summary!")

async def post_to_channel(context: ContextTypes.DEFAULT_TYPE, message: str):
    """
    Post a message to the Newsroom Telegram Channel
    """
    try:
        # bot = Bot(TELEGRAM_BOT_TOKEN) 
        if len(message) <= 4096:
            await context.bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=message, parse_mode="HTML")
            logger.info(f"Message posted sucessfully to channel {TELEGRAM_CHANNEL_ID}")
        else:
            # Split message into chunks of 4096 character or less
            message_chunks = [message[i:i+4096] for i in range(0, len(message), 4096)]

            for chunk in message_chunks:
                await context.bot.send_message(TELEGRAM_BOT_TOKEN, text=chunk, parse_mode="HTML")
                logger.info(f"Message posted sucessfully to channel {TELEGRAM_CHANNEL_ID}")
            
            logger.info(f"Long message posted as {len(message_chunks)} chunks to channel {TELEGRAM_CHANNEL_ID}")

    except TelegramError as e:
        logger.error(f"Error posting to channel: {e}")


# [backlog]: notify functin <effective_chat.id>

async def query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Extract query keywords from messages tagging @BotName.
    Return the query string or None if no valid query.
    """
    message_text = update.message.text
    bot_username = context.bot.username
    pattern = rf"^@{bot_username}\s+(.+)$"
    match = re.match(pattern, message_text)
    if not match:
        logger.error(f"No found any topic from input: {message_text} \nMatching Result: {pattern} \nBot_Username: {bot_username}")
        return
    topic = match.group(1)
    logger.info(f"User is searching for '{topic}'")

    articles = fetch_articles(topic)
    if not articles:
        logger.info(f"No articles found for '{topic}'.")
        return
    summary = summarize_news(articles)
    await post_to_channel(context, message=summary)

def run_bot():
    """
    """
    # Initialize Telegram application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    # Add handlers
    application.add_handler(CommandHandler("start", command_start))
    # app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), receive_query_request))
    application.add_handler(
        MessageHandler(filters.Mention(TELEGRAM_BOT_NAME), query_handler)
    )

    application.run_polling(poll_interval=1010, allowed_updates=Update.ALL_TYPES)
        

if __name__ == "__main__":
    run_bot()