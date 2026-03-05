# Telegram Dropshipping Bot

A Telegram bot that searches AliExpress products from user messages and returns the first matching product link.

## Features

- Search AliExpress by keyword.
- Return a product URL in chat.
- Simple `Buy` command flow (demo response).
- Script-style startup via `scripts/run.sh`.

## Project Structure

- `dropship_bot.py` - main bot script.
- `config.py` - environment-based settings loader.
- `scripts/run.sh` - one-command run script.
- `.env.example` - environment template.

## Setup

1. Clone repository.
2. Create your env file:

   ```bash
   cp .env.example .env
   ```

3. Add your Telegram token to `.env`:

   ```env
   BOT_TOKEN=your_actual_bot_token
   ```

4. Run the bot as a script:

   ```bash
   ./scripts/run.sh
   ```

## Alternative Manual Run

```bash
python3 -m pip install -r requirements.txt
python3 dropship_bot.py
```

## Notes

- AliExpress HTML changes frequently, so scraping selectors may need future updates.
- This project provides demo order messaging only and does not process payments.
