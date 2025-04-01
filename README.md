# Telegram Translation Bot

## Overview

This is a Telegram bot specialized in translation, leveraging Large Language Models (LLMs) for high-quality text translation. The bot is built using Python and integrates the **Gemini** LLM, an easy to use google AI model, to provide accurate translations across multiple languages.

## Features

- Supports multiple languages
- Uses **Gemini** for advanced translation
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

### 2. Obtain an API Key for Gemini

You need an API key from **Gemini** to access its translation model. Visit the [Gemini API portal](https://ai.google.dev/gemini-api/docs/api-key) and generate a key.

### 3. Configure Environment Variables

Create a `.env` file in the project root and add:

```ini
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
Gemini_API_KEY=your_gemini_api_key
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
   heroku config:set GEMINI_API_KEY=your_gemini_api_key
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

The bot interacts with gemini API as follows:

```python
import requests

import requests

def translate_text(text, source_lang, target_lang):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    
    headers = {"Content-Type": "application/json"}
    params = {"key": os.getenv("GEMINI_API_KEY")}
    
    payload = {
        "contents": [{
            "parts": [{
                "text": f"Translate the following text from {source_lang} to {target_lang}: {text}"
            }]
        }]
    }
    
    response = requests.post(url, json=payload, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Translation failed")
    else:
        return f"Error {response.status_code}: {response.text}"

```

## Contributing

Feel free to open issues and submit pull requests to improve the bot.

##

