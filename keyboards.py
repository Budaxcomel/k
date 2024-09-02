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
    """Generate the main keyboard with processed button labels."""
    keyboard = [
        [InlineKeyboardButton(process_text("Digi", 'digi'), callback_data='digi')],
        [InlineKeyboardButton(process_text("Maxis", 'maxis'), callback_data='maxis')],
        [InlineKeyboardButton(process_text("Umobile", 'umobile'), callback_data='umobile')],
        [InlineKeyboardButton(process_text("Unifi", 'unifi'), callback_data='unifi')],
        [InlineKeyboardButton(process_text("Celcom", 'celcom'), callback_data='celcom')],
        [InlineKeyboardButton(process_text("Yes", 'yes'), callback_data='yes')],
        [InlineKeyboardButton(process_text("Booster 5", 'booster5'), callback_data='booster5')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_submenu_keyboard(menu: str) -> InlineKeyboardMarkup:
    """Generate submenu keyboard based on the menu option with processed button labels."""
    submenu = SUBMENU_OPTIONS.get(menu, [])
    keyboard = [[InlineKeyboardButton(process_text(button.text, menu), callback_data=button.callback_data) for button in row] for row in submenu]
    return InlineKeyboardMarkup(keyboard)
