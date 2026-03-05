import logging
from urllib.parse import quote_plus

import requests
import telebot
from bs4 import BeautifulSoup

import config

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

ALIEXPRESS_SEARCH_URL = "https://www.aliexpress.com/wholesale?SearchText={}"
REQUEST_HEADERS = {"User-Agent": "Mozilla/5.0"}
REQUEST_TIMEOUT_SECONDS = 15

bot = telebot.TeleBot(config.BOT_TOKEN)


def fetch_first_product_url(query: str) -> str | None:
    """Fetch the first product URL from AliExpress search results."""
    search_url = ALIEXPRESS_SEARCH_URL.format(quote_plus(query))

    response = requests.get(
        search_url,
        headers=REQUEST_HEADERS,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # AliExpress frequently changes classes; scan candidate links and return first product-like URL.
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if "/item/" in href:
            if href.startswith("//"):
                return f"https:{href}"
            if href.startswith("/"):
                return f"https://www.aliexpress.com{href}"
            if href.startswith("http"):
                return href
    return None


@bot.message_handler(commands=["start"])
def welcome(message):
    bot.reply_to(
        message,
        "Welcome to the Dropshipping Bot! Send a product name, and I'll find deals for you.",
    )


@bot.message_handler(func=lambda message: message.text and message.text.lower().strip() == "buy")
def buy_product(message):
    bot.reply_to(message, "Processing your order... (Demo mode)")


@bot.message_handler(func=lambda message: bool(message.text and message.text.strip()))
def search_product(message):
    query = message.text.strip()

    if query.lower() == "buy":
        return

    try:
        product_url = fetch_first_product_url(query)
    except requests.RequestException as exc:
        logging.exception("Failed to fetch AliExpress products: %s", exc)
        bot.reply_to(message, "I couldn't reach AliExpress right now. Please try again in a moment.")
        return

    if product_url:
        bot.reply_to(
            message,
            f"I found this for you: {product_url}\n\nReply with 'Buy' to purchase!",
        )
    else:
        bot.reply_to(message, "No product found. Try another keyword.")


def main() -> None:
    logging.info("Bot is live...")
    bot.infinity_polling(skip_pending=True)


if __name__ == "__main__":
    main()
