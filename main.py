import logging
import os
import asyncio
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from handlers import start, button, handle_message, set_admin_id, set_user_id, clone_bot, process_payment, payment_return, broadcast_to_user, broadcast_to_group, broadcast_to_channel, broadcast_to_all, total_users

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def main() -> None:
    """Start the bot."""
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        logger.error("Telegram bot token is not set in environment variables.")
        return

    application = Application.builder().token(token).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("set_admin_id", set_admin_id))
    application.add_handler(CommandHandler("set_user_id", set_user_id))
    application.add_handler(CommandHandler("clone_bot", clone_bot))
    application.add_handler(CommandHandler("process_payment", process_payment))
    application.add_handler(CommandHandler("payment_return", payment_return))
    application.add_handler(CommandHandler("broadcast_to_user", broadcast_to_user))
    application.add_handler(CommandHandler("broadcast_to_group", broadcast_to_group))
    application.add_handler(CommandHandler("broadcast_to_channel", broadcast_to_channel))
    application.add_handler(CommandHandler("broadcast_to_all", broadcast_to_all))
    application.add_handler(CommandHandler("total_users", total_users))

    # Register message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Register callback query handler
    application.add_handler(CallbackQueryHandler(button))

    # Start the bot
    try:
        logger.info("Starting bot...")
        await application.initialize()
        await application.run_polling()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        if not application.is_closed:  # Check if application is already closed
            try:
                await application.shutdown()
            except Exception as shutdown_error:
                logger.error(f"Error during shutdown: {shutdown_error}")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
