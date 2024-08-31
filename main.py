import sys
import os
import asyncio
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config import TOKEN, logger
from handlers import start, button, handle_message

# Menambah direktori semasa ke Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    try:
        await application.initialize()
        await application.run_polling()
    except Exception as e:
        logger.error(f"Error during polling: {e}")
    finally:
        await application.shutdown()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Error running the bot: {e}")
