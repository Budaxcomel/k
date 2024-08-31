from dotenv import load_dotenv
import os
import logging

# Load environment variables from a specific .env file
load_dotenv('config.env')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the token from an environment variable for security
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not TOKEN:
    logger.error("Telegram bot token not found. Please set the TELEGRAM_BOT_TOKEN environment variable.")
    exit(1)

# Optionally, you can add more configuration settings here
# For example:
# API_KEY = os.getenv('API_KEY')
# DATABASE_URL = os.getenv('DATABASE_URL')
# DEBUG = os.getenv('DEBUG', 'False').lower() in ['true', '1', 't']
