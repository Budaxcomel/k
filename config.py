# config.py
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

# Admin user ID
ADMIN_USER_ID = int(os.getenv('ADMIN_USER_ID', 123456789))  # Replace with your actual admin user ID

# List of allowed user IDs
ALLOWED_USER_IDS = list(map(int, os.getenv('ALLOWED_USER_IDS', '123456789,987654321').split(',')))  # Replace with allowed user IDs

# List of paid user IDs
PAID_USER_IDS = set(map(int, os.getenv('PAID_USER_IDS', '').split(',')))  # Replace with IDs of users who have paid

# ToyyibPay API configuration
TOYYIBPAY_API_KEY = os.getenv('TOYYIBPAY_API_KEY')
TOYYIBPAY_MERCHANT_CODE = os.getenv('TOYYIBPAY_MERCHANT_CODE')
TOYYIBPAY_SECRET_KEY = os.getenv('TOYYIBPAY_SECRET_KEY')

if not TOKEN:
    logger.error("Telegram bot token not found. Please set the TELEGRAM_BOT_TOKEN environment variable.")
    exit(1)

# Ensure that ToyyibPay configurations are set
if not all([TOYYIBPAY_API_KEY, TOYYIBPAY_MERCHANT_CODE, TOYYIBPAY_SECRET_KEY]):
    logger.error("ToyyibPay configuration missing. Please set the TOYYIBPAY_API_KEY, TOYYIBPAY_MERCHANT_CODE, and TOYYIBPAY_SECRET_KEY environment variables.")
    exit(1)
