import logging
import requests
from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_USER_ID, ALLOWED_USER_IDS, PAID_USER_IDS, TOYYIBPAY_API_KEY, TOYYIBPAY_MERCHANT_CODE, TOYYIBPAY_SECRET_KEY
import os

logger = logging.getLogger(__name__)

def is_user_allowed(user_id: int) -> bool:
    """Check if the user is allowed to use the bot."""
    return user_id == ADMIN_USER_ID or user_id in ALLOWED_USER_IDS

def is_user_paid(user_id: int) -> bool:
    """Check if the user has paid to access the bot."""
    return user_id in PAID_USER_IDS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    await update.message.reply_text("Welcome!")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle callback queries from inline buttons."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=f"Selected option: {query.data}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming text messages."""
    user_id = update.message.from_user.id
    if is_user_allowed(user_id):
        user_text = update.message.text
        await update.message.reply_text(f"You said: {user_text}")
    else:
        await update.message.reply_text("You do not have permission to use this bot.")

async def set_admin_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Set a new admin ID."""
    user_id = update.message.from_user.id
    if user_id == ADMIN_USER_ID:
        if len(context.args) != 1:
            await update.message.reply_text("Usage: /set_admin_id <new_admin_id>")
            return
        
        new_admin_id = context.args[0]

        # Update the config file with the new admin ID
        update_config('ADMIN_USER_ID', new_admin_id)

        await update.message.reply_text("Admin ID has been updated.")
    else:
        await update.message.reply_text("You do not have permission to change the admin ID.")

async def set_user_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Set new allowed user IDs."""
    user_id = update.message.from_user.id
    if user_id == ADMIN_USER_ID:
        if len(context.args) != 1:
            await update.message.reply_text("Usage: /set_user_id <user_ids_comma_separated>")
            return
        
        new_allowed_user_ids = context.args[0].split(',')

        # Update the config file with the new allowed user IDs
        update_config('ALLOWED_USER_IDS', ','.join(new_allowed_user_ids))

        await update.message.reply_text("Allowed user IDs have been updated.")
    else:
        await update.message.reply_text("You do not have permission to change the allowed user IDs.")

async def process_payment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Create a payment invoice and send the payment link to the user."""
    user_id = update.message.from_user.id

    # Create payment invoice using ToyyibPay
    payment_url = "https://toyyibpay.com/index.php/api/create_invoice"
    payload = {
        "api_key": TOYYIBPAY_API_KEY,
        "merchant_code": TOYYIBPAY_MERCHANT_CODE,
        "secret_key": TOYYIBPAY_SECRET_KEY,
        "invoice_no": f"INV-{user_id}",
        "amount": 10.00,  # Amount to be paid
        "description": "Access to Bot",
        "return_url": "https://yourdomain.com/payment_return"  # Update with your actual return URL
    }
    
    response = requests.post(payment_url, json=payload)
    data = response.json()

    if response.status_code == 200 and data.get('status') == 'success':
        payment_link = data.get('payment_url')
        await update.message.reply_text(f"Please complete your payment by visiting: {payment_link}")
    else:
        await update.message.reply_text("Failed to create payment link. Please try again later.")

async def payment_return(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle payment return and update user status."""
    data = update.message.text.split()  # Expecting data to come as a text message

    if len(data) < 2:
        await update.message.reply_text("Invalid return data.")
        return

    invoice_no = data[0]
    payment_status = data[1]  # Status of payment

    if payment_status == "paid":
        user_id = int(invoice_no.split('-')[1])
        PAID_USER_IDS.add(user_id)  # Add user to the paid user list

        # Save the update to the config file
        update_config('PAID_USER_IDS', ','.join(map(str, PAID_USER_IDS)))
        
        await update.message.reply_text("Payment successful. You now have access to the bot.")
    else:
        await update.message.reply_text("Payment failed or cancelled.")

def update_config(key: str, value: str) -> None:
    """Update the config file with new values."""
    config_file = 'config.env'
    if not os.path.exists(config_file):
        with open(config_file, 'w') as file:
            pass  # Create the file if it does not exist

    with open(config_file, 'r') as file:
        lines = file.readlines()

    with open(config_file, 'w') as file:
        key_found = False
        for line in lines:
            if line.startswith(f'{key}='):
                file.write(f'{key}={value}\n')
                key_found = True
            else:
                file.write(line)
        if not key_found:
            file.write(f'{key}={value}\n')
