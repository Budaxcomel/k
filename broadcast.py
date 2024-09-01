import json
import os
from telegram import Update
from telegram.ext import ContextTypes

# Load user data from file
def load_user_data() -> dict:
    """Load user data from file."""
    if os.path.exists('user_data.json'):
        with open('user_data.json', 'r') as file:
            return json.load(file)
    return {}

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

def is_freemium(user_id: int) -> bool:
    """Check if the user is freemium."""
    user_data = load_user_data()
    return user_id not in user_data or user_data[user_id].get('subscription_end') is None

async def broadcast_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Broadcast message to all users, but only freemium users will receive it."""
    user_id = update.message.from_user.id
    message = ' '.join(context.args)
    user_data = load_user_data()
    
    # Broadcast to all users
    for uid in user_data.keys():
        if is_freemium(uid):
            await context.bot.send_message(chat_id=uid, text=message)

    # Confirm sending message
    await update.message.reply_text("Broadcast to freemium users completed.")

async def broadcast_to_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Broadcast message to groups."""
    user_id = update.message.from_user.id
    message = ' '.join(context.args)
    group_ids = load_group_ids()
    
    # Broadcast to all groups
    for group_id in group_ids:
        await context.bot.send_message(chat_id=group_id, text=message)

    # Confirm sending message
    await update.message.reply_text("Broadcast to groups completed.")

async def broadcast_to_channel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Broadcast message to channels."""
    user_id = update.message.from_user.id
    message = ' '.join(context.args)
    channel_ids = load_channel_ids()
    
    # Broadcast to all channels
    for channel_id in channel_ids:
        await context.bot.send_message(chat_id=channel_id, text=message)

    # Confirm sending message
    await update.message.reply_text("Broadcast to channels completed.")

async def auto_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Broadcast message to all users, groups, and channels."""
    user_id = update.message.from_user.id
    message = ' '.join(context.args)
    user_data = load_user_data()
    group_ids = load_group_ids()
    channel_ids = load_channel_ids()

    # Broadcast to all users
    for uid in user_data.keys():
        if is_freemium(uid):
            await context.bot.send_message(chat_id=uid, text=message)

    # Broadcast to all groups
    for group_id in group_ids:
        await context.bot.send_message(chat_id=group_id, text=message)

    # Broadcast to all channels
    for channel_id in channel_ids:
        await context.bot.send_message(chat_id=channel_id, text=message)

    # Confirm sending message
    await update.message.reply_text("Auto broadcast completed.")
