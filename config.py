from binance.client import Client
import time

# Informations

API_KEY = 'VzJYaYBn2w0aNkavvlCG1o2LwuOUQyBEjjnM0TPZAGBIwZge0hsejAnxV3pf2J2L'
API_SECRET = 'XGoSn1gxfL6eoDA8WlEBinbNUmGXNneeBCCbHpXaE6BxWNIvHvWMXYziZTFjZjFa'
SOCKETS = 'wss://stream.binance.com:9443/ws/adausdt@kline_5m'

# Version

branch = "Beta"
version = "1.1.6"

# Run Dependency

run = True

try:
    client = Client(API_KEY, API_SECRET)
    budget = client.futures_account(recvWindow=50000, timestamp=round(time.time() * 1000))
    print("Client successfully connected.")
except:
    print("While connection to client an error occured.")
    run = False

#print(client.get_deposit_address(coin="BTC", recvWindow=50000, timestamp=round(time.time() * 1000)))

# Telegram

channelId = "-1001347995174"
TOKEN = "1776589751:AAH3HQRXe7tEJf5C-HnfBVeOBWta72Gbd_E"