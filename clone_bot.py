import os
import json
from typing import List
from telegram import Update
from telegram.ext import ContextTypes
from config import ALLOWED_USER_IDS, PAYING_USERS, TOYYIBPAY_API_KEY, TOYYIBPAY_MERCHANT_CODE, TOYYIBPAY_SECRET_KEY
import requests

# Define type alias for the payment status
PaymentStatus = Dict[str, str]

def is_user_paid(user_id: int) -> bool:
    """Check if the user has paid and is allowed to clone the bot."""
    return user_id in PAYING_USERS

async def clone_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id

    if is_user_paid(user_id):
        # Proceed with cloning the bot
        # Here, you would implement the actual cloning logic.
        await update.message.reply_text("Your bot is being cloned...")
    else:
        await update.message.reply_text("You need to be a paying user to clone the bot.")

def verify_payment(payment_data: Dict) -> PaymentStatus:
    """Verify the payment using ToyyibPay API."""
    payload = {
        "api_key": TOYYIBPAY_API_KEY,
        "merchant_code": TOYYIBPAY_MERCHANT_CODE,
        "secret_key": TOYYIBPAY_SECRET_KEY,
        "invoice_no": payment_data.get("invoice_no"),
    }
    response = requests.post("https://toyyibpay.com/verify_payment", json=payload)
    return response.json()

def handle_payment_return(request_data: Dict) -> None:
    """Handle payment return from ToyyibPay."""
    payment_status = verify_payment(request_data)
    if payment_status.get("status") == "success":
        user_id = int(payment_status.get("invoice_no").split('-')[1])
        PAYING_USERS.append(user_id)
        # Save or update the list of paying users
        with open('paying_users.json', 'w') as file:
            json.dump(PAYING_USERS, file)
    else:
        print("Payment verification failed.")

def load_paying_users() -> List[int]:
    """Load the list of paying users from a file."""
    if os.path.exists('paying_users.json'):
        with open('paying_users.json', 'r') as file:
            return json.load(file)
    return []

# Initialize the list of paying users
PAYING_USERS = load_paying_users()
