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

## Where to Edit

- Main bot logic: `dropship_bot.py`
- Environment/token settings: `.env` (copy from `.env.example`)
- Dependency list: `requirements.txt`
- Startup script: `scripts/run.sh`
- Documentation: `README.md`

## Sync This Project to Your GitHub

If this folder is already a git repo, run:

```bash
git status
git add .
git commit -m "Your update message"
git push origin <your-branch>
```

If you want to connect this local project to a new GitHub repository:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

Then open your repository on GitHub and create a Pull Request from your branch.
