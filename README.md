# Telegram Translation Bot

## Overview

This is a Telegram bot specialized in translation, leveraging Large Language Models (LLMs) for high-quality text translation. The bot is built using Python and integrates the **Deepseek** LLM, a powerful Chinese AI model, to provide accurate translations across multiple languages.

## Features

- Supports multiple languages
- Uses **Deepseek** for advanced translation
- Works with Telegram Bot API
- Can be deployed on a server for 24/7 operation

## Prerequisites

Before running the bot, ensure you have the following installed:

- Python 3.8+
- `requests`, `python-telegram-bot`, and `dotenv` libraries

Install dependencies using:

```bash
pip install -r requirements.txt
```

## Setup and Configuration

### 1. Get a Telegram Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/BotFather).
2. Start a chat and use the command:
   ```
   /newbot
   ```
3. Follow the instructions and copy the generated bot token.

### 2. Obtain an API Key for Deepseek

You need an API key from **Deepseek** to access its translation model. Visit the [Deepseek API portal](https://www.deepseek.com) and generate a key.

### 3. Configure Environment Variables

Create a `.env` file in the project root and add:

```ini
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
DEEPSEEK_API_KEY=your_deepseek_api_key
```

## Running the Bot

Run the bot with:

```bash
python bot.py
```

If deploying on a VPS, consider using `nohup` or `tmux` to keep it running:

```bash
nohup python bot.py
```

## Deployment

### Option 1: Heroku

1. Install Heroku CLI and log in:
   ```bash
   heroku login
   ```
2. Create a new Heroku app:
   ```bash
   heroku create your-bot-name
   ```
3. Set environment variables:
   ```bash
   heroku config:set TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   heroku config:set DEEPSEEK_API_KEY=your_deepseek_api_key
   ```
4. Deploy the bot:
   ```bash
   git push heroku main
   ```

### Option 2: VPS (Recommended for 24/7 availability)

1. Set up a VPS on DigitalOcean, AWS, or another provider.
2. Install Python and required libraries.
3. Use `screen` or `tmux` to keep the bot running persistently.

## API Integration

The bot interacts with Deepseek API as follows:

```python
import requests

def translate_text(text, source_lang, target_lang):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Act as a professional translation assistant specializing in English-Persian and Persian-English translations."},
            {"role": "user", "content": text}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json().get("choices", [{}])[0].get("message", {}).get("content", "Translation failed")
```

## Contributing

Feel free to open issues and submit pull requests to improve the bot.

##

