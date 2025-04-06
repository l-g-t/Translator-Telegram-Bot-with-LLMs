import sys, io, os, time, logging, asyncio
import aiohttp, telebot
from dotenv import load_dotenv
from functools import wraps
from aiohttp import ClientTimeout

# Set the standard output encoding to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
load_dotenv()  # Load environment variables from a .env file

# Retrieve the Telegram bot token and Gemini API key from environment variables
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not all([TELEGRAM_TOKEN, GEMINI_API_KEY]):
    raise ValueError("Missing required environment variables")

# Set default timeout for HTTP requests and rate limit for bot responses
DEFAULT_TIMEOUT = ClientTimeout(total=30)
RATE_LIMIT = 1

# Configure logging to output to both console and a file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(), logging.FileHandler('bot.log')]
)
logger = logging.getLogger(__name__)

# Decorator to enforce rate limiting on bot functions
def rate_limit(func):
    last_call = 0
    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal last_call
        now = time.time()
        if now - last_call < RATE_LIMIT:
            time.sleep(RATE_LIMIT - (now - last_call))
        last_call = time.time()
        return func(*args, **kwargs)
    return wrapper

# Initialize the Telegram bot with the provided token
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Asynchronous function to call the Gemini language model API
async def call_language_model(prompt, session):
    try:
        async with session.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
            headers={"Content-Type": "application/json"},
            params={"key": os.getenv("GEMINI_API_KEY")},
            json={
                "contents": [
                    {
                        "parts": [
                            {
                                "text": "Translate between English and Persian (Farsi) with accuracy and cultural awareness. "
                                        "Ensure contextually appropriate translations, maintaining a formal tone. "
                                        "If multiple translations exist, choose the most suitable one. "
                                        "Keep responses clear, concise, and professional.\n\n"
                                        "Text: " + prompt
                            }
                        ]
                    }
                ],
                "temperature": 0.7,
                "max_output_tokens": 500,
            }
        ) as response:
            if response.status == 200:
                response_json = await response.json()
                return response_json["candidates"][0]["content"]["parts"][0]["text"].strip()
            else:
                logger.error(f"API error: {response.status} - {await response.text()}")
                return "Translation service error"
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return "An error occurred during translation"

# Handler for incoming messages to the bot
@bot.message_handler(func=lambda _: True)
def handle_message(message):
    try:
        # Process the translation asynchronously and send the response back to the user
        response = asyncio.run(process_translation(message.text))
        bot.reply_to(message, response[:4000] + "\n[...]" if len(response) > 4000 else response)
    except Exception as e:
        logger.error(f"Translation Error: {str(e)}")
        bot.reply_to(message, "Error in translation process")

# Asynchronous function to process the translation request
async def process_translation(text):
    async with aiohttp.ClientSession(timeout=DEFAULT_TIMEOUT) as session:
        response = await call_language_model(text, session)
        return response.encode('utf-8', 'ignore').decode('utf-8')

# Main entry point of the script
if __name__ == "__main__":
    try:
        logger.info("Starting Telegram Bot...")
        bot.infinity_polling(timeout=60)  # Start polling for new messages
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")