from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from typing import List, Dict

# Define type aliases for better readability
MenuOptions = Dict[str, List[List[InlineKeyboardButton]]]

# Keyboard options for submenu
SUBMENU_OPTIONS: MenuOptions = {
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

def get_main_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("Digi", callback_data='digi')],
        [InlineKeyboardButton("Maxis", callback_data='maxis')],
        [InlineKeyboardButton("Umobile", callback_data='umobile')],
        [InlineKeyboardButton("Unifi", callback_data='unifi')],
        [InlineKeyboardButton("Celcom", callback_data='celcom')],
        [InlineKeyboardButton("Yes", callback_data='yes')],
        [InlineKeyboardButton("Booster 5", callback_data='booster5')]
    ]
    return InlineKeyboardMarkup(keyboard)
