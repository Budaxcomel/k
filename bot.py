from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
import re

TOKEN = '7409687169:AAHYmbd5UwNLwzZQVnAKaUwCcue_7ddLarY'

def start(update: Update, context: CallbackContext) -> None:
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
    update.message.reply_text('Pilih pilihan:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == 'digi':
        keyboard = [
            [InlineKeyboardButton("Digi Booster", callback_data='digi_booster')],
            [InlineKeyboardButton("Digi X Langgan", callback_data='digi_x_langgan')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text="Pilih submenu Digi:", reply_markup=reply_markup)
    elif query.data == 'maxis':
        keyboard = [
            [InlineKeyboardButton("my.budaxcomel.me", callback_data='maxis_my')],
            [InlineKeyboardButton("sg.budaxcomel.me", callback_data='maxis_sg')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text="Pilih submenu Maxis:", reply_markup=reply_markup)
    elif query.data == 'booster5':
        keyboard = [
            [InlineKeyboardButton("Method 1", callback_data='booster5_method1')],
            [InlineKeyboardButton("Method 2", callback_data='booster5_method2')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text="Pilih submenu Booster 5:", reply_markup=reply_markup)
    else:
        context.user_data['menu'] = query.data
        query.edit_message_text(text="Sila hantar teks yang ingin ditukar:")

def handle_message(update: Update, context: CallbackContext) -> None:
    user_text = update.message.text
    menu = context.user_data.get('menu')

    if menu:
        response = process_text(user_text, menu)
        update.message.reply_text(response)

def process_text(user_text: str, menu: str) -> str:
    result = user_text
    
    if menu == 'digi_booster':
        result = re.sub(r'@(\S+):', '@162.159.134.61:', user_text)
        result = re.sub(r'&host=(\S+)', '&host=sg8.immanvpn.xyz', result)
    elif menu == 'digi_x_langgan':
        result = re.sub(r'@(\S+):', '@app.optimizely.com:', user_text)
    elif menu == 'maxis_my':
        result = re.sub(r'@(\S+):', '@speedtest.net:', user_text)
        result = re.sub(r'&host=(\S+)', '&host=imman.budaxcomel.me&sni=speedtest.net', result)
    elif menu == 'maxis_sg':
        result = re.sub(r'@(\S+):', '@speedtest.net:', user_text)
        result = re.sub(r'&host=(\S+)', '&host=sg.imman.budaxcomel.me&sni=speedtest.net', result)
    elif menu == 'umobile':
        result = re.sub(r'@(\S+):', '@sg8.immanvpn.xyz:', user_text)
        result = re.sub(r'&host=(\S+)', '&host=m.pubgmobile.com', result)
    elif menu == 'unifi':
        result = re.sub(r'@(\S+):', '@104.17.10.12:', user_text)
    elif menu == 'celcom':
        result = re.sub(r'@(\S+):', '@104.17.147.22:', user_text)
        result = re.sub(r'&host=(\S+)', '&host=opensignal.com.sg8.immanvpn.xyz', result)
    elif menu == 'yes':
        result = re.sub(r'@(\S+):', '@104.17.113.188:', user_text)
        result = re.sub(r'&host=(\S+)', '&host=tap-database.who.int.sg8.immanvpn.xyz', result)
    elif menu == 'booster5_method1':
        result = re.sub(r'@(\S+):', '@www.speedtest.net:', user_text)
    elif menu == 'booster5_method2':
        result = re.sub(r'@(\S+):', '@104.17.148.22:', user_text)

    return result

def main() -> None:
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
