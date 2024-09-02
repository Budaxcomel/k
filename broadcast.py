import json
import os
import telebot
from typing import List
from config import TOKEN as TELEGRAM_BOT_TOKEN

# Load configuration from environment variables or a config file
API_TOKEN = TELEGRAM_BOT_TOKEN  # Directly use imported token
bot = telebot.TeleBot(API_TOKEN)

def load_user_data() -> dict:
    """Load user data from file."""
    if os.path.exists('user_data.json'):
        with open('user_data.json', 'r') as file:
            return json.load(file)
    return {}

def load_group_ids() -> List[int]:
    """Load group IDs from file."""
    if os.path.exists('group_ids.json'):
        with open('group_ids.json', 'r') as file:
            return json.load(file)
    return []

def load_channel_ids() -> List[int]:
    """Load channel IDs from file."""
    if os.path.exists('channel_ids.json'):
        with open('channel_ids.json', 'r') as file:
            return json.load(file)
    return []

def is_freemium(user_id: int) -> bool:
    """Check if the user is freemium."""
    user_data = load_user_data()
    return user_id not in user_data or user_data[user_id].get('subscription_end') is None

@bot.message_handler(commands=['broadcast_user'])
def broadcast_to_user(message: telebot.types.Message) -> None:
    """Broadcast message to all users, but only freemium users will receive it."""
    user_id = message.from_user.id
    message_text = ' '.join(message.text.split()[1:])  # Get message text after the command
    user_data = load_user_data()
    
    # Broadcast to all freemium users
    for uid in user_data.keys():
        if is_freemium(uid):
            try:
                bot.send_message(chat_id=uid, text=message_text)
            except Exception as e:
                print(f"Failed to send message to user {uid}: {e}")

    # Confirm sending message
    bot.reply_to(message, "Broadcast to all freemium users completed.")

@bot.message_handler(commands=['broadcast_group'])
def broadcast_to_group(message: telebot.types.Message) -> None:
    """Broadcast message to groups."""
    user_id = message.from_user.id
    message_text = ' '.join(message.text.split()[1:])  # Get message text after the command
    group_ids = load_group_ids()
    
    # Broadcast to all groups
    for group_id in group_ids:
        try:
            bot.send_message(chat_id=group_id, text=message_text)
        except Exception as e:
            print(f"Failed to send message to group {group_id}: {e}")

    # Confirm sending message
    bot.reply_to(message, "Broadcast to all groups completed.")

@bot.message_handler(commands=['broadcast_channel'])
def broadcast_to_channel(message: telebot.types.Message) -> None:
    """Broadcast message to channels."""
    user_id = message.from_user.id
    message_text = ' '.join(message.text.split()[1:])  # Get message text after the command
    channel_ids = load_channel_ids()
    
    # Broadcast to all channels
    for channel_id in channel_ids:
        try:
            bot.send_message(chat_id=channel_id, text=message_text)
        except Exception as e:
            print(f"Failed to send message to channel {channel_id}: {e}")

    # Confirm sending message
    bot.reply_to(message, "Broadcast to all channels completed.")

@bot.message_handler(commands=['broadcast_all'])
def broadcast_to_all(message: telebot.types.Message) -> None:
    """Broadcast message to all users, groups, and channels."""
    user_id = message.from_user.id
    message_text = ' '.join(message.text.split()[1:])  # Get message text after the command
    user_data = load_user_data()
    group_ids = load_group_ids()
    channel_ids = load_channel_ids()

    # Broadcast to all freemium users
    for uid in user_data.keys():
        if is_freemium(uid):
            try:
                bot.send_message(chat_id=uid, text=message_text)
            except Exception as e:
                print(f"Failed to send message to user {uid}: {e}")

    # Broadcast to all groups
    for group_id in group_ids:
        try:
            bot.send_message(chat_id=group_id, text=message_text)
        except Exception as e:
            print(f"Failed to send message to group {group_id}: {e}")

    # Broadcast to all channels
    for channel_id in channel_ids:
        try:
            bot.send_message(chat_id=channel_id, text=message_text)
        except Exception as e:
            print(f"Failed to send message to channel {channel_id}: {e}")

    # Confirm sending message
    bot.reply_to(message, "Broadcast to all users, groups, and channels completed.")

if __name__ == "__main__":
    bot.polling(none_stop=True)
