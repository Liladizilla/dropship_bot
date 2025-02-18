import telebot
import requests
from bs4 import BeautifulSoup
import config

bot = telebot.TeleBot(config.BOT_TOKEN)

ALIEXPRESS_SEARCH_URL = "https://www.aliexpress.com/wholesale?SearchText={}"

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Welcome to the Dropshipping Bot! Send a product name, and I'll find the best deals for you.")

@bot.message_handler(func=lambda message: True)
def search_product(message):
    query = message.text
    search_url = ALIEXPRESS_SEARCH_URL.format(query.replace(" ", "+"))
    
    # Scrape AliExpress for the first product
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)
    print(response.status_code)
print(response.text[:500])  # Print first 500 characters of response
    soup = BeautifulSoup(response.text, 'html.parser')
    
    product = soup.find("a", class_="manhattan--container--3lP0P")
    
    if product:
        product_url = "https:" + product['href']
        bot.reply_to(message, f"I found this for you: {product_url}\n\nReply with 'Buy' to purchase!")
    else:
        bot.reply_to(message, "No product found. Try another keyword.")

@bot.message_handler(func=lambda message: message.text.lower() == "buy")
def buy_product(message):
    bot.reply_to(message, "Processing your order... (Just a demo 😆)")

print("Bot is live...")
bot.infinity_polling()