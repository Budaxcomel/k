from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext
from queue import Queue
import re

TOKEN = '7409687169:AAHYmbd5UwNLwzZQVnAKaUwCcue_7ddLarY'

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

    if query.data == 'digi':
        keyboard = [
            [InlineKeyboardButton("Digi Booster", callback_data='digi_booster')],
            [InlineKeyboardButton("Digi X Langgan", callback_data='digi_x_langgan')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Pilih submenu Digi:", reply_markup=reply_markup)
    elif query.data == 'maxis':
        keyboard = [
            [InlineKeyboardButton("my.budaxcomel.me", callback_data='maxis_my')],
            [InlineKeyboardButton("sg.budaxcomel.me", callback_data='maxis_sg')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Pilih submenu Maxis:", reply_markup=reply_markup)
    elif query.data == 'booster5':
        keyboard = [
            [InlineKeyboardButton("Method 1", callback_data='booster5_method1')],
            [InlineKeyboardButton("Method 2", callback_data='booster5_method2')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Pilih submenu Booster 5:", reply_markup=reply_markup)
    else:
        context.user_data['menu'] = query.data
        await query.edit_message_text(text="Sila hantar teks yang ingin ditukar:")

async def handle_message(update: Update, context: CallbackContext) -> None:
    user_text = update.message.text
    menu = context.user_data.get('menu')

    if menu:
        response = process_text(user_text, menu)
        await update.message.reply_text(response)
    else:
        await update.message.reply_text("Sila pilih menu terlebih dahulu menggunakan butang.")

def process_text(user_text: str, menu: str) -> str:
    result = user_text

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

    for pattern, replacement in patterns.get(menu, []):
        result = re.sub(pattern, replacement, result)

    return result

async def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
