from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from typing import List, Dict
from text_processing import process_text

# Define type aliases for better readability
MenuOptions = Dict[str, List[List[InlineKeyboardButton]]]

# Keyboard options for submenu
SUBMENU_OPTIONS: MenuOptions = {
    'digi': [
        [InlineKeyboardButton("Digi Booster", callback_data='digi_booster')],
        [InlineKeyboardButton("Digi X Langgan", callback_data='digi_x_langgan')]
    ],
    'maxis': [
        [InlineKeyboardButton("Maxis My", callback_data='maxis_my')],
        [InlineKeyboardButton("Maxis SG", callback_data='maxis_sg')]
    ],
    'booster5': [
        [InlineKeyboardButton("Method 1", callback_data='booster5_method1')],
        [InlineKeyboardButton("Method 2", callback_data='booster5_method2')]
    ],
    'umobile': [
        [InlineKeyboardButton("Umobile Option", callback_data='umobile')]  # Placeholder button
    ],
    'unifi': [
        [InlineKeyboardButton("Unifi Option", callback_data='unifi')]  # Placeholder button
    ],
    'celcom': [
        [InlineKeyboardButton("Celcom Option", callback_data='celcom')]  # Placeholder button
    ],
    'yes': [
        [InlineKeyboardButton("Yes Option", callback_data='yes')]  # Placeholder button
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

def get_submenu_keyboard(menu: str) -> InlineKeyboardMarkup:
    """Generate submenu keyboard based on the menu option."""
    keyboard = SUBMENU_OPTIONS.get(menu, [])
    return InlineKeyboardMarkup(keyboard)
