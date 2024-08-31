from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext
import asyncio
import re
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the token from an environment variable for security
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not TOKEN:
    logger.error("Telegram bot token not found. Please set the TELEGRAM_BOT_TOKEN environment variable.")
    exit(1)

async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Digi", callback_data='digi')],
        [InlineKeyboardButton("Maxis", callback_data='maxis')],
        [InlineKeyboardButton("Umobile", callback_data='umobile')],
        [InlineKeyboardButton("Unifi", callback_data='unifi')],
        [InlineKeyboardButton("Celcom", callback_data='celcom')],
        [InlineKeyboardButton("Yes", callback_data='yes')],
        [InlineKeyboardButton("Booster 5", callback_data='booster5')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Pilih pilihan:', reply_markup=reply_markup)

async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    submenu_options = {
        'digi': [
            [InlineKeyboardButton("Digi Booster", callback_data='digi_booster')],
            [InlineKeyboardButton("Digi X Langgan", callback_data='digi_x_langgan')]
        ],
        'maxis': [
            [InlineKeyboardButton("my.budaxcomel.me", callback_data='maxis_my')],
            [InlineKeyboardButton("sg.budaxcomel.me", callback_data='maxis_sg')]
        ],
        'booster5': [
            [InlineKeyboardButton("Method 1", callback_data='booster5_method1')],
            [InlineKeyboardButton("Method 2", callback_data='booster5_method2')]
        ]
    }

    if query.data in submenu_options:
        keyboard = submenu_options[query.data]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=f"Pilih submenu {query.data.capitalize()}:", reply_markup=reply_markup)
    else:
        context.user_data['menu'] = query.data
        await query.edit_message_text(text="Sila hantar teks yang ingin ditukar:")

async def handle_message(update: Update, context: CallbackContext) -> None:
    user_text = update.message.text
    menu = context.user_data.get('menu')

    if menu:
        try:
            response = process_text(user_text, menu)
            await update.message.reply_text(response)
        except Exception as e:
            logger.error(f"Error processing text: {e}")
            await update.message.reply_text("Terjadi ralat semasa memproses teks.")
    else:
        await update.message.reply_text("Sila pilih menu terlebih dahulu menggunakan butang.")

def process_text(user_text: str, menu: str) -> str:
    patterns = {
        'digi_booster': [
            (r'@(\S+):(\d+)', '@162.159.134.61:\2'),
            (r'&host=(\S+)', '&host=sg8.immanvpn.xyz')
        ],
        'digi_x_langgan': [
            (r'@(\S+):(\d+)', '@app.optimizely.com:\2')
        ],
        'maxis_my': [
            (r'@(\S+):(\d+)', '@speedtest.net:\2'),
            (r'&host=(\S+)', '&host=imman.budaxcomel.me&sni=speedtest.net')
        ],
        'maxis_sg': [
            (r'@(\S+):(\d+)', '@speedtest.net:\2'),
            (r'&host=(\S+)', '&host=sg.imman.budaxcomel.me&sni=speedtest.net')
        ],
        'umobile': [
            (r'@(\S+):(\d+)', '@sg8.immanvpn.xyz:\2'),
            (r'&host=(\S+)', '&host=m.pubgmobile.com')
        ],
        'unifi': [
            (r'@(\S+):(\d+)', '@104.17.10.12:\2')
        ],
        'celcom': [
            (r'@(\S+):(\d+)', '@104.17.147.22:\2'),
            (r'&host=(\S+)', '&host=opensignal.com.sg8.immanvpn.xyz')
        ],
        'yes': [
            (r'@(\S+):(\d+)', '@104.17.113.188:\2'),
            (r'&host=(\S+)', '&host=tap-database.who.int.sg8.immanvpn.xyz')
        ],
        'booster5_method1': [
            (r'@(\S+):(\d+)', '@www.speedtest.net:\2')
        ],
        'booster5_method2': [
            (r'@(\S+):(\d+)', '@104.17.148.22:\2')
        ]
    }

    replacements = patterns.get(menu, [])
    result = user_text

    for pattern, replacement in replacements:
        result = re.sub(pattern, replacement, result)

    return result

async def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start polling
    await application.run_polling()

if __name__ == '__main__':
    # Obtain the current event loop
    loop = asyncio.get_event_loop()
    
    # Run the main function in the event loop
    loop.run_until_complete(main())
