import time
import requests
import threading

import telegram

bot = telegram.Bot(token='5095136537:AAEIFF9EQp1iyGzpfYuI1Ouf6QLJlMFxmSI')
prices = []
roc:float = None
print("initializing in 30 seconds")
bot.sendMessage(chat_id='667370488', text="initializing in 30 seconds")
def get_bitcoin_price_binance(request_time_interval:int = 3, roc_threshold:float = 1):
    """
    Returns bitcoin price from Binance API, 
    calculates price`s rate of change (roc),
    sends telegram message if absolute roc is too high.
    """
    process = threading.Timer(request_time_interval, get_bitcoin_price_binance)
    process.start()
    r = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT', timeout=5)

    if r.status_code != 200: #catches errors and tries again
        bot.sendMessage(chat_id='667370488', text=f"Binance API server responded with '{r.status_code}' code, instead of '200'. Trying agian in 60 seconds. \nClick for more info on response code: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/{r.status_code}")
        process.cancel()
        time.sleep(60)
        get_bitcoin_price_binance()

    r = r.json()
    bitcoin_price = float(r["price"])
    prices.append(bitcoin_price)
    if len(prices) > 10:
        prices.pop(0)
        roc = ((prices[9] / prices[0]) - 1) * 100 #roc is price`s rate of change
        roc = round(roc, 2)
        if abs(roc) > roc_threshold:
            message = f"last price: {prices[0]} \nprice now:  {prices[9]} \nROC = {roc}% \n"
            bot.sendMessage(chat_id="667370488", text=message)         
            
get_bitcoin_price_binance()
