import asyncio
from telegram.ext import Application
from config import TOKEN
from handlers import start, button, handle_message

async def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    try:
        await application.run_polling()
    except Exception as e:
        logger.error(f"Error during polling: {e}")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Error running the bot: {e}")
