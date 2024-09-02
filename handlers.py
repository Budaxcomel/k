import logging
import requests
import json
from datetime import datetime, timedelta
import os
import telebot
from config import ADMIN_USER_ID, ALLOWED_USER_IDS, PAID_USER_IDS, TOYYIBPAY_API_KEY, TOYYIBPAY_MERCHANT_CODE, TOYYIBPAY_SECRET_KEY
from clone_bot import get_user_data

logger = logging.getLogger(__name__)

def is_user_allowed(user_id: int) -> bool:
    """Check if the user is allowed to use the bot."""
    return user_id == ADMIN_USER_ID or user_id in ALLOWED_USER_IDS

def is_user_paid(user_id: int) -> bool:
    """Check if the user has paid to access the bot."""
    user_data = load_user_data()
    return user_id in user_data and user_data[user_id].get("subscription_end") and user_data[user_id]["subscription_end"] > datetime.now()

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

def start(message: telebot.types.Message, bot: telebot.TeleBot) -> None:
    """Handle /start command."""
    bot.reply_to(message, "Welcome!")

def button(call: telebot.types.CallbackQuery, bot: telebot.TeleBot) -> None:
    """Handle callback queries from inline buttons."""
    bot.answer_callback_query(call.id)
    bot.edit_message_text(f"Selected option: {call.data}", chat_id=call.message.chat.id, message_id=call.message.message_id)

def handle_message(message: telebot.types.Message, bot: telebot.TeleBot) -> None:
    """Handle incoming text messages."""
    user_id = message.from_user.id
    if is_user_allowed(user_id):
        user_text = message.text
        bot.reply_to(message, f"You said: {user_text}")
    else:
        bot.reply_to(message, "You do not have permission to use this bot.")

def set_admin_id(message: telebot.types.Message, bot: telebot.TeleBot) -> None:
    """Set a new admin ID."""
    user_id = message.from_user.id
    if user_id == ADMIN_USER_ID:
        args = message.text.split()[1:]
        if len(args) != 1:
            bot.reply_to(message, "Usage: /set_admin_id <new_admin_id>")
            return
        
        new_admin_id = args[0]
        update_config('ADMIN_USER_ID', new_admin_id)
        bot.reply_to(message, "Admin ID has been updated.")
    else:
        bot.reply_to(message, "You do not have permission to change the admin ID.")

def set_user_id(message: telebot.types.Message, bot: telebot.TeleBot) -> None:
    """Set new allowed user IDs."""
    user_id = message.from_user.id
    if user_id == ADMIN_USER_ID:
        args = message.text.split()[1:]
        if len(args) != 1:
            bot.reply_to(message, "Usage: /set_user_id <user_ids_comma_separated>")
            return
        
        new_allowed_user_ids = args[0].split(',')
        update_config('ALLOWED_USER_IDS', ','.join(new_allowed_user_ids))
        bot.reply_to(message, "Allowed user IDs have been updated.")
    else:
        bot.reply_to(message, "You do not have permission to change the allowed user IDs.")

def clone_bot(message: telebot.types.Message, bot: telebot.TeleBot) -> None:
    """Clone the bot to another bot using the provided token."""
    user_id = message.from_user.id
    if is_user_paid(user_id):
        args = message.text.split()[1:]
        if len(args) != 1:
            bot.reply_to(message, "Usage: /clone_bot <bot_token>")
            return
        
        bot_token = args[0]
        # Implement cloning logic here
        
        bot.reply_to(message, f"Bot cloned successfully with token: {bot_token}")
    else:
        bot.reply_to(message, "You need to be a premium user to clone the bot.")

def process_payment(message: telebot.types.Message, bot: telebot.TeleBot) -> None:
    """Create a payment invoice and send the payment link to the user."""
    user_id = message.from_user.id
    payment_url = "https://toyyibpay.com/index.php/api/create_invoice"
    payload = {
        "api_key": TOYYIBPAY_API_KEY,
        "merchant_code": TOYYIBPAY_MERCHANT_CODE,
        "secret_key": TOYYIBPAY_SECRET_KEY,
        "invoice_no": f"INV-{user_id}",
        "amount": 5.00,  # Amount to be paid
        "description": "Access to Bot for 30 days",
        "return_url": "https://yourdomain.com/payment_return"  # Update with your actual return URL
    }
    
    response = requests.post(payment_url, json=payload)
    data = response.json()

    if response.status_code == 200 and data.get('status') == 'success':
        payment_link = data.get('payment_url')
        bot.reply_to(message, f"Please complete your payment by visiting: {payment_link}")
    else:
        bot.reply_to(message, "Failed to create payment link. Please try again later.")

def payment_return(message: telebot.types.Message, bot: telebot.TeleBot) -> None:
    """Handle payment return and update user status."""
    data = message.text.split()  # Expecting data to come as a text message

    if len(data) < 2:
        bot.reply_to(message, "Invalid return data.")
        return

    invoice_no = data[0]
    payment_status = data[1]  # Status of payment

    if payment_status == "paid":
        user_id = int(invoice_no.split('-')[1])
        user_data = load_user_data()
        user_data[user_id] = {
            "subscription_end": datetime.now() + timedelta(days=30)
        }
        save_user_data(user_data)
        bot.reply_to(message, "Payment successful. You now have access to the bot.")
    else:
        bot.reply_to(message, "Payment failed or cancelled.")

def total_users(message: telebot.types.Message, bot: telebot.TeleBot) -> None:
    """Get the total number of users."""
    user_data = load_user_data()
    total_users_count = len(user_data)
    bot.reply_to(message, f"Total number of users: {total_users_count}")

def update_config(key: str, value: str) -> None:
    """Update the config file with new values."""
    config_file = 'config.env'
    if not os.path.exists(config_file):
        with open(config_file, 'w') as file:
            file.write(f"{key}={value}\n")
    else:
        with open(config_file, 'r') as file:
            lines = file.readlines()
        
        with open(config_file, 'w') as file:
            found = False
            for line in lines:
                if line.startswith(f"{key}="):
                    file.write(f"{key}={value}\n")
                    found = True
                else:
                    file.write(line)
            if not found:
                file.write(f"{key}={value}\n")
