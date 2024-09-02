import os
import json
import requests
from typing import Dict
import telebot
from config import ALLOWED_USER_IDS, PAID_USER_IDS, TOYYIBPAY_API_KEY, TOYYIBPAY_MERCHANT_CODE, TOYYIBPAY_SECRET_KEY

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

def clone_bot(message, bot: telebot.TeleBot) -> None:
    user_id = message.from_user.id
    user_data = get_user_data(user_id)
    
    if is_user_paid(user_id):
        bot_count = user_data.get('bot_count', 0)
        if bot_count < 5:
            # Proceed with cloning the bot
            user_data['bot_count'] = bot_count + 1
            save_user_data({user_id: user_data})
            bot.reply_to(message, "Your bot is being cloned...")
        else:
            bot.reply_to(message, "You have reached the maximum number of bot clones allowed.")
    else:
        if user_data.get('bot_count', 0) < 1:
            # Proceed with cloning the bot
            user_data['bot_count'] = 1
            save_user_data({user_id: user_data})
            bot.reply_to(message, "Your bot is being cloned...")
        else:
            bot.reply_to(message, "You have reached the maximum number of bot clones allowed.")

# Example function using requests to fetch additional data
def fetch_additional_data(api_url: str) -> dict:
    """Fetch additional data from an external API."""
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data"}
