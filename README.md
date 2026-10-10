# Telegram Dropship Product Finder

A Telegram bot that searches AliExpress and returns a candidate product listing. It is a **product discovery tool**, not an order-processing system.

## Features
- Search by product name.
- Request timeout and useful network error handling.
- Validate search length and reject non-AliExpress or non-item links.
- Telegram polling with `/start` and `/help`.
- Automated offline unit tests through GitHub Actions.

## Setup
1. Install Python 3.11 or newer.
2. Create a Telegram bot with Telegram's official BotFather.
3. Copy `.env.example` to `.env` and set `BOT_TOKEN`.
4. Install dependencies and run:

```bash
python -m pip install -r requirements.txt
python dropship_bot.py
```

## Scope and safety
The current bot does **not** place orders, accept payments, collect customer payment details, or guarantee prices/availability. Its HTML-based search may break when AliExpress changes its page structure. Treat results as links to inspect manually.

Never commit `.env` or expose the Telegram token.
