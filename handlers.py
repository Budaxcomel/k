import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the token from an environment variable for security
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not TOKEN:
    logger.error("Telegram bot token not found. Please set the TELEGRAM_BOT_TOKEN environment variable.")
    exit(1)