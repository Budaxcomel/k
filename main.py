import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import TOKEN

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define command handlers
async def start(update, context):
    await update.message.reply_text('Hello!')

# Main function
async def main():
    # Create the Application and pass it your bot's token
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler('start', start))

    # Run the bot until you send a signal to stop
    try:
        await application.run_polling()
    except Exception as e:
        logger.error(f"Error during polling: {e}")
    finally:
        # Ensure the application shuts down properly
        await application.shutdown()

if __name__ == '__main__':
    # Assuming you have Python 3.7 or later
    asyncio.run(main())

    # For older Python versions (if necessary):
    # import asyncio
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.close()