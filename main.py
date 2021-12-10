
from time import time
import requests
import threading
import telegram

bot = telegram.Bot(token='5095136537:AAEIFF9EQp1iyGzpfYuI1Ouf6QLJlMFxmSI')

prices = []
roc:float = None
print("initializing in 20 seconds")
bot.sendMessage(chat_id='-522727272', text="initializing in 30 seconds")
def get_bitcoin_price_binance():
    """Returns bitcoin price from Binance API every 3 seconds
    """

    threading.Timer(3, get_bitcoin_price_binance).start()
    r = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT').json()
    bitcoin_price = float(r["price"])
    prices.append(bitcoin_price)
    if len(prices) > 10:
        prices.pop(0)
        roc = ((prices[9] / prices[0]) - 1) * 100 #roc is price`s rate of change
        roc = round(roc, 2)
        roc_threshold:float = 0.2
        if abs(roc) > roc_threshold:
            message = f"last price: {prices[0]} \nprice now:  {prices[9]} \nROC = {roc}% \n"
            bot.sendMessage(chat_id='-522727272', text=message)         
            
get_bitcoin_price_binance()
