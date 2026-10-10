"""Telegram product-search bot. Order placement is intentionally not implemented."""
import logging
from urllib.parse import quote_plus, urljoin, urlparse

import requests
import telebot
from bs4 import BeautifulSoup

import config

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
ALIEXPRESS_SEARCH_URL = "https://www.aliexpress.com/wholesale?SearchText={}"
REQUEST_HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; DropshipBot/1.0)"}
REQUEST_TIMEOUT_SECONDS = 15
MAX_QUERY_LENGTH = 120
bot = telebot.TeleBot(config.BOT_TOKEN)


def fetch_first_product_url(query: str) -> str | None:
    """Return the first valid AliExpress item URL or None."""
    query = " ".join(query.split())
    if not query:
        raise ValueError("Please enter a product name.")
    if len(query) > MAX_QUERY_LENGTH:
        raise ValueError(f"Search must be {MAX_QUERY_LENGTH} characters or fewer.")

    response = requests.get(
        ALIEXPRESS_SEARCH_URL.format(quote_plus(query)),
        headers=REQUEST_HEADERS,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    for link in soup.find_all("a", href=True):
        href = urljoin("https://www.aliexpress.com", link["href"])
        parsed = urlparse(href)
        if (
            parsed.scheme == "https"
            and (parsed.hostname or "").lower() in {"aliexpress.com", "www.aliexpress.com"}
            and "/item/" in parsed.path
        ):
            return href
    return None


@bot.message_handler(commands=["start", "help"])
def welcome(message):
    bot.reply_to(
        message,
        "Send a product name and I'll look for an AliExpress listing. "
        "This bot only finds links; it does not place orders or process payments.",
    )


@bot.message_handler(func=lambda message: bool(message.text and message.text.strip()))
def search_product(message):
    try:
        product_url = fetch_first_product_url(message.text.strip())
    except ValueError as exc:
        bot.reply_to(message, str(exc))
        return
    except requests.RequestException:
        logging.warning("AliExpress request failed", exc_info=True)
        bot.reply_to(message, "I couldn't reach AliExpress right now. Please try again later.")
        return
    except Exception:
        logging.exception("Unexpected product-search failure")
        bot.reply_to(message, "Something went wrong while searching. Please try again later.")
        return

    if product_url:
        bot.reply_to(message, f"Possible listing: {product_url}\n\nCheck seller, price, shipping, and returns before buying.")
    else:
        bot.reply_to(message, "No product listing found. Try a more specific product name.")


def main() -> None:
    logging.info("Dropship product-search bot is starting")
    bot.infinity_polling(skip_pending=True, timeout=30, long_polling_timeout=20)


if __name__ == "__main__":
    main()
