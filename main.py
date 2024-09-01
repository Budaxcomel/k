import sys
import os
import asyncio
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config import TOKEN, logger
from handlers import start, button, handle_message, set_admin_id, set_user_id

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def main() -> None:
    application = Application.builder().token(TOKEN).build()

    # Add handlers for new commands
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CommandHandler('set_admin_id', set_admin_id))
    application.add_handler(CommandHandler('set_user_id', set_user_id))

    try:
        await application.initialize()
        await application.run_polling()
    except Exception as e:
        logger.error(f"Error during polling: {e}")
    finally:
        try:
            await application.shutdown()
        except Exception as shutdown_error:
            logger.error(f"Error during shutdown: {shutdown_error}")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Error running the bot: {e}")
