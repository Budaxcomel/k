import os
import json
from typing import List, Dict
from telegram import Update
from telegram.ext import ContextTypes
from config import ALLOWED_USER_IDS, PAID_USER_IDS, TOYYIBPAY_API_KEY, TOYYIBPAY_MERCHANT_CODE, TOYYIBPAY_SECRET_KEY
import requests

# Define type alias for the payment status
PaymentStatus = Dict[str, str]

def is_user_paid(user_id: int) -> bool:
    """Check if the user has paid and is allowed to clone the bot."""
    return user_id in PAID_USER_IDS

def get_user_data(user_id: int) -> dict:
    """Load user data from file."""
    user_data = load_user_data()
    return user_data.get(user_id, {})

def load_user_data() -> dict:
    """Load user data from file."""
    if os.path.exists('user_data.json'):
        with open('user_data.json', 'r') as file:
            return json.load(file)
    return {}

def save_user_data(user_data: dict) -> None:
    """Save user data to file."""
    with open('user_data.json', 'w') as file:
        json.dump(user_data, file, indent=4)

async def clone_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    user_data = get_user_data(user_id)
    
    if is_user_paid(user_id):
        bot_count = user_data.get('bot_count', 0)
        if bot_count < 5:
            # Proceed with cloning the bot
            user_data['bot_count'] = bot_count + 1
            save_user_data({user_id: user_data})
            await update.message.reply_text("Your bot is being cloned...")
        else:
            await update.message.reply_text("You have reached the maximum number of bot clones allowed.")
    else:
        if user_data.get('bot_count', 0) < 1:
            # Proceed with cloning the bot
            user_data['bot_count'] = 1
            save_user_data({user_id: user_data})
            await update.message.reply_text("Your bot is being cloned...")
        else:
            await update.message.reply_text("You have reached the maximum number of bot clones allowed.")
