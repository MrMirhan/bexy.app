import config
import time
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException

client = Client(config.API_KEY, config.API_SECRET)

print(client.futures_account_balance(
    recvWindow=50000, timestamp=round(time.time() * 1000)))
