import logging
import os
import telebot
from broadcast import broadcast_to_user, broadcast_to_group, broadcast_to_channel, broadcast_to_all
from handlers import start, button, handle_message, set_admin_id, set_user_id, clone_bot, process_payment, payment_return, total_users
from keyboards import get_main_keyboard, get_submenu_keyboard, SUBMENU_OPTIONS

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the bot token from environment variables
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TOKEN:
    logger.error("Telegram bot token is not set in environment variables.")
    exit(1)

# Create the bot instance
bot = telebot.TeleBot(TOKEN)

# Command handlers
@bot.message_handler(commands=['start'])
def handle_start(message)

@bot.message_handler(commands=['set_admin_id'])
def handle_set_admin_id(message):
    set_admin_id(message, bot)

@bot.message_handler(commands=['set_user_id'])
def handle_set_user_id(message):
    set_user_id(message, bot)

@bot.message_handler(commands=['clone_bot'])
def handle_clone_bot(message):
    clone_bot(message, bot)

@bot.message_handler(commands=['process_payment'])
def handle_process_payment(message):
    process_payment(message, bot)

@bot.message_handler(commands=['payment_return'])
def handle_payment_return(message):
    payment_return(message, bot)

@bot.message_handler(commands=['total_users'])
def handle_total_users(message):
    total_users(message, bot)

@bot.message_handler(commands=['broadcast_user'])
def broadcast_to_user(message: telebot.types.Message)

@bot.message_handler(commands=['broadcast_group'])
def broadcast_to_group(message: telebot.types.Message)

@bot.message_handler(commands=['broadcast_channel'])
def broadcast_to_channel(message: telebot.types.Message)

# Message handler
@bot.message_handler(func=lambda message: not message.text.startswith('/'))
def handle_text_message(message):
    handle_message(message, bot)

def main():
    try:
        logger.info("Starting bot...")
        bot.polling()
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
