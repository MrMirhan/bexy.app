import json
import pprint
import talib
import numpy
import requests
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException
import time
import json
from tradingview_ta import TA_Handler, Interval, Exchange
from decimal import Decimal
import math
import decimal
import random   
import sys, re, optparse, os
from threading import Thread
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException
import main

stop = {}
scheduler = BackgroundScheduler()
scheduler.start()

def orderCheck(threadId, args):
    global stop
    print("Thread started.")
    print(args)
    scheduler.remove_job(f"{threadId}", jobstore=None)

def orderCancel(threadId, args): # {"type": "all / user", "userId": 0 / 10001, "coin": "ALGO/MKR/ADA", "orderId": "578678"}
    coin = str(args['coin']).lower()
    if args['type'] == "all":
        for dirs in os.walk("users"):
            usersArray = dirs[1]
            for x in usersArray:
                x = str(x)
                print(x)
                positionOrderJsonFile = open("users/{}/positionOrders.json".format(x), "r+")
                configJsonFile = open("users/{}/config.json".format(x), "r+")
                apiJsonFile = open("users/{}/binanceApiKeys.json".format(x), "r+")
                pnlJsonFile = open("users/{}/pnlHistory.json".format(x), "r+")
                positionHistoryJsonFile = open("users/{}/positionHistory.json".format(x), "r+")
                coinsJsonFile = open("users/{}/coins.json".format(x), "r+")
                
                positionOrders = json.load(positionOrderJsonFile)
                userConfig = json.load(configJsonFile)
                userApis = json.load(apiJsonFile)
                pnlHistory = json.load(pnlJsonFile)
                positionHistory = json.load(positionHistoryJsonFile)
                userCoins = json.load(coinsJsonFile)

                if userConfig['automaticClose'] == "true":
                    coinData = userCoins[coin]
                    if coinData['active'] == 1:
                        for a in coinData['apiKeys']:
                            api = [x for x in userApis if x['apiKeyId'] == int(a)]
                            api = api[0]
                            apiKey = api['apiKey']
                            apiSecret = api['apiSecret']
                            apiName = api['apiName']
                            client = Client(apiKey, apiSecret)
                            for order in positionOrders:
                                if order['coin'] == coin.upper():
                                    coinx = str(coin.upper()) + "USDT"
                                    position = client.futures_account(recvWindow=50000, timestamp=round(time.time() * 1000))['positions']
                                    position = [y for y in position if y['symbol'] == coinx]
                                    pnl = float(position[0]['unrealizedProfit'])
                                    bougthQuantity = int(order['bougthQuantity'])
                                    spentMoney = float(order['spentMoney'])
                                    orderType = str(order['orderType'])
                                    roe = str(order['roe'])
                                    karzarar = "KÂR"
                                    if pnl < 0: karzarar = "ZARAR"
                                    orderId = str(order['orderId'])
                                    orderTypex = ""
                                    if orderType == "BUY":
                                        orderTypex = "SELL"
                                    elif orderType == "SELL":
                                        orderTypex = "BUY"
                                    print(client.futures_create_order(symbol=coinx, side=orderTypex, type="MARKET", quantity=bougthQuantity, recvWindow=50000, timestamp=round(time.time() * 1000)))
                                    main.sendTelegram(str(userConfig['telegramChatId']), "------İŞLEMDEN ÇIKILDI ({})------\nCoin Sembol: {}\nİşlem Tipi: {}\nİşlem Id: {}\nMiktar: {}\nHarcama: {}\nPNL: {}".format(karzarar, coinx, orderType, orderId, bougthQuantity, spentMoney, pnl))
            break

def createThread(type, args):
    threadId = round(time.time() * 1000)
    if type == 'cancel':
        scheduler.add_job(func=orderCancel, args=[threadId, args], trigger=None, id=f"{threadId}")
    elif type == 'check':
        scheduler.add_job(func=orderCheck, args=[threadId, args], trigger="interval", id=f"{threadId}", seconds=1)