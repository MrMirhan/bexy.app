from binance.client import Client
import time

# Informations

API_KEY = 'KEY'
API_SECRET = 'SECRET'
TIME = "30m"
SOCKETS = f'wss://stream.binance.com:9443/ws/adausdt@kline_{TIME}'

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

channelId = "CHANNEL ID"
TOKEN = "TOKEN TELEGRAM"