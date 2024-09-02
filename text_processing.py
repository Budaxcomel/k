import re
import logging
from typing import Dict, List, Tuple

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define type aliases for better readability
Patterns = Dict[str, List[Tuple[str, str]]]

# Define patterns for text replacement
PATTERNS: Patterns = {
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

def process_text(user_text: str, menu: str) -> str:
    """
    Processes the provided text based on the selected menu's patterns.

    Args:
        user_text (str): The text to be processed.
        menu (str): The menu key to determine which patterns to apply.

    Returns:
        str: The processed text with applied replacements.
    """
    replacements = PATTERNS.get(menu, [])
    result = user_text

    for pattern, replacement in replacements:
        try:
            result = re.sub(pattern, replacement, result)
        except re.error as e:
            logger.error(f"Regex error for pattern '{pattern}': {e}")

    return result
