import logging
import requests
import json
from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_USER_ID, ALLOWED_USER_IDS, PAID_USER_IDS, TOYYIBPAY_API_KEY, TOYYIBPAY_MERCHANT_CODE, TOYYIBPAY_SECRET_KEY
from clone_bot import PAYING_USERS
from datetime import datetime, timedelta
import os

logger = logging.getLogger(__name__)

def is_user_allowed(user_id: int) -> bool:
    """Check if the user is allowed to use the bot."""
    return user_id == ADMIN_USER_ID or user_id in ALLOWED_USER_IDS

def is_user_paid(user_id: int) -> bool:
    """Check if the user has paid to access the bot."""
    user_data = load_user_data()
    return user_id in user_data and user_data[user_id]["subscription_end"] > datetime.now()

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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    await update.message.reply_text("Welcome!")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle callback queries from inline buttons."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=f"Selected option: {query.data}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming text messages."""
    user_id = update.message.from_user.id
    if is_user_allowed(user_id):
        user_text = update.message.text
        await update.message.reply_text(f"You said: {user_text}")
    else:
        await update.message.reply_text("You do not have permission to use this bot.")

async def set_admin_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Set a new admin ID."""
    user_id = update.message.from_user.id
    if user_id == ADMIN_USER_ID:
        if len(context.args) != 1:
            await update.message.reply_text("Usage: /set_admin_id <new_admin_id>")
            return
        
        new_admin_id = context.args[0]
        update_config('ADMIN_USER_ID', new_admin_id)
        await update.message.reply_text("Admin ID has been updated.")
    else:
        await update.message.reply_text("You do not have permission to change the admin ID.")

async def set_user_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Set new allowed user IDs."""
    user_id = update.message.from_user.id
    if user_id == ADMIN_USER_ID:
        if len(context.args) != 1:
            await update.message.reply_text("Usage: /set_user_id <user_ids_comma_separated>")
            return
        
        new_allowed_user_ids = context.args[0].split(',')
        update_config('ALLOWED_USER_IDS', ','.join(new_allowed_user_ids))
        await update.message.reply_text("Allowed user IDs have been updated.")
    else:
        await update.message.reply_text("You do not have permission to change the allowed user IDs.")

async def clone_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Clone the bot to another bot using the provided token."""
    user_id = update.message.from_user.id
    if is_user_paid(user_id):
        if len(context.args) != 1:
            await update.message.reply_text("Usage: /clone_bot <bot_token>")
            return
        
        bot_token = context.args[0]
        # Here you would implement the actual cloning logic
        # For example, you might use the Telegram API to create a new bot instance with the given token
        
        await update.message.reply_text(f"Bot cloned successfully with token: {bot_token}")
    else:
        await update.message.reply_text("You need to be a premium user to clone the bot.")

async def process_payment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Create a payment invoice and send the payment link to the user."""
    user_id = update.message.from_user.id
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
        await update.message.reply_text(f"Please complete your payment by visiting: {payment_link}")
    else:
        await update.message.reply_text("Failed to create payment link. Please try again later.")

async def payment_return(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle payment return and update user status."""
    data = update.message.text.split()  # Expecting data to come as a text message

    if len(data) < 2:
        await update.message.reply_text("Invalid return data.")
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
        await update.message.reply_text("Payment successful. You now have access to the bot.")
    else:
        await update.message.reply_text("Payment failed or cancelled.")

async def broadcast_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Broadcast message to all freemium users."""
    message = ' '.join(context.args)
    user_data = load_user_data()
    for user_id, data in user_data.items():
        if data.get("subscription_end") is None or data["subscription_end"] <= datetime.now():
            await context.bot.send_message(chat_id=user_id, text=message)
    await update.message.reply_text("Broadcast to freemium users completed.")

async def broadcast_to_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Broadcast message to all groups."""
    message = ' '.join(context.args)
    group_ids = load_group_ids()
    for group_id in group_ids:
        await context.bot.send_message(chat_id=group_id, text=message)
    await update.message.reply_text("Broadcast to groups completed.")

async def broadcast_to_channel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Broadcast message to all channels."""
    message = ' '.join(context.args)
    channel_ids = load_channel_ids()
    for channel_id in channel_ids:
        await context.bot.send_message(chat_id=channel_id, text=message)
    await update.message.reply_text("Broadcast to channels completed.")

async def broadcast_to_all(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Broadcast message to all users, groups, and channels."""
    message = ' '.join(context.args)
    
    # Broadcast to freemium users
    user_data = load_user_data()
    for user_id, data in user_data.items():
        if data.get("subscription_end") is None or data["subscription_end"] <= datetime.now():
            await context.bot.send_message(chat_id=user_id, text=message)

    # Broadcast to groups
    group_ids = load_group_ids()
    for group_id in group_ids:
        await context.bot.send_message(chat_id=group_id, text=message)

    # Broadcast to channels
    channel_ids = load_channel_ids()
    for channel_id in channel_ids:
        await context.bot.send_message(chat_id=channel_id, text=message)
    
    await update.message.reply_text("Broadcast to all users, groups, and channels completed.")

async def total_users(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Get the total number of users."""
    user_data = load_user_data()
    total_users_count = len(user_data)
    await update.message.reply_text(f"Total number of users: {total_users_count}")

def load_group_ids() -> list:
    """Load group IDs from file."""
    if os.path.exists('group_ids.json'):
        with open('group_ids.json', 'r') as file:
            return json.load(file)
    return []

def load_channel_ids() -> list:
    """Load channel IDs from file."""
    if os.path.exists('channel_ids.json'):
        with open('channel_ids.json', 'r') as file:
            return json.load(file)
    return []

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
