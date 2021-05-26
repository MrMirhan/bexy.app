import json
import pprint
from pkg_resources import add_activation_listener
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
    elif type == "user":
                    x = str(args['userId'])
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
                                    print(position)
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

def createOrder(args):
    coin = str(args['coin']).lower()
    if args['type'] == "all":
        for dirs in os.walk("users"):
            usersArray = dirs[1]
            for x in usersArray:
                x = str(x)
                openOrdersJsonFile = open("users/{}/openOrders.json".format(x), "r+")
                configJsonFile = open("users/{}/config.json".format(x), "r+")
                apiJsonFile = open("users/{}/binanceApiKeys.json".format(x), "r+")
                pnlJsonFile = open("users/{}/pnlHistory.json".format(x), "r+")
                positionHistoryJsonFile = open("users/{}/positionHistory.json".format(x), "r+")
                coinsJsonFile = open("users/{}/coins.json".format(x), "r+")
                                
                openOrders = json.load(openOrdersJsonFile)
                userConfig = json.load(configJsonFile)
                userApis = json.load(apiJsonFile)
                pnlHistory = json.load(pnlJsonFile)
                positionHistory = json.load(positionHistoryJsonFile)
                userCoins = json.load(coinsJsonFile)
                TRADE_SYMBOL = str(coin.upper()) + "USDT"
                coinData = userCoins[coin]
                if coinData['active'] == 1:
                    for a in coinData['apiKeys']:
                        api = [x for x in userApis if x['apiKeyId'] == int(a)]
                        api = api[0]
                        apiKey = api['apiKey']
                        apiSecret = api['apiSecret']
                        apiName = api['apiName']
                        client = Client(apiKey, apiSecret)
                        side = args['side']
                        pres = int(args['pres'])
                        orders = client.futures_get_open_orders(symbol=TRADE_SYMBOL, recvWindow=50000, timestamp=round(time.time() * 1000))
                        budget = float(client.futures_account_balance()[1]['balance'])
                        open_orders = orders
                        minusBudget = float(0)
                        for x in open_orders:
                            minusBudget = float(minusBudget) + float((float(x['stopPrice']) * float(x['origQty'])) / float(10))
                        availableBalance = budget - minusBudget
                        orderBudgetLimit = int(userConfig['orderBudgetLimit'])
                        alimButce = float(float(availableBalance) * float(float(orderBudgetLimit) / float(100)))
                        price = float(args['coinAlimEmriDeger'])
                        qnt = int(round(float(alimButce / price)) * 10)
                        try:
                            print("sending order")
                            order = client.futures_create_order(symbol=TRADE_SYMBOL, side=side, type="STOP", timeInForce = "GTC", quantity = qnt, price=price, stopPrice=price, recvWindow=50000, timestamp=round(time.time() * 1000))
                            appendOrder = {"coin": coin.upper(), "orderId": order['orderId'], "entryPrice": price, "bougthQuantity": qnt, "spentMoney": alimButce, "orderType": side}
                            mesaj = "------EMİR KOYULDU------\nCoin Sembol: {}\nİşlem Tipi: {}\nİşlem Id: {}\nAlım Miktarı: {}\nAlım Yapılacak Değer: {}\nHarcanan Tutar: {}\nİşlem Öncesi Kullanılabilir Bakiye: {}".format(TRADE_SYMBOL, side, order['orderId'], qnt, price, alimButce, availableBalance)
                            print(mesaj)
                            main.sendTelegram(str(userConfig['telegramChatId']), mesaj)
                            return order
                        except Exception as e:
                            print("an exception occured - {}".format(e))
                            e = str(e)
                            if "2021" in e:
                                if side == "SELL":
                                    print("Activation price should be smaller than current price.")
                                elif side == "BUY":
                                    print("Activation price should be larger than current price.")
                                return "immediately"
                            elif "1111" in e:
                                return "pres"
            break
    
def alimYap(threadId, args):
        coinAlimEmriDeger = float(args['coinAlimEmriDeger'])
        orderType = str(args['orderType'])
        coin = str(args['coin'])
        pres = int(args['pres'])
        TRADE_SYMBOL = str(coin.upper()) + "USDT"
        price = requests.get("https://api.binance.com/api/v3/avgPrice?symbol={}".format(TRADE_SYMBOL)).json()['price']
        coinDeger = float(str(price).split('.')[0] + "." + str(price).split('.')[1][0:pres])
        orderTypex = ""
        if orderType == "al":
            orderTypex = "BUY"
        else:
            orderTypex = "SELL"
        print(orderTypex)
        order = createOrder({"coin": coin, "side": orderTypex, "coinAlimEmriDeger": coinAlimEmriDeger, "pres": pres, "type": str(args['type'])})
        print(order)
        if order == "immediately":
            while True:
                time.sleep(0.3)
                price = str(float(requests.get("https://api.binance.com/api/v3/avgPrice?symbol={}".format(TRADE_SYMBOL)).json()['price']))
                coinDeger = float(str(price).split('.')[0] + "." + str(price).split('.')[1][0:pres])
                orderType = str(orderType)
                coinAlimEmriDegerx = 0.00
                orderTypex = ""
                if orderTypex == "al":
                    orderType = "BUY"
                    coinAlimEmriDegerx = float(coinDeger - ((coinDeger / float(100)) * float(0.125)))
                else:
                    orderTypex = "SELL"
                    coinAlimEmriDegerx = float(coinDeger + ((coinDeger / float(100)) * float(0.125)))
                order = createOrder({"coin": coin, "side": orderTypex, "coinAlimEmriDeger": coinAlimEmriDegerx, "pres": pres, "type": str(args['type'])})
                if order == "immediately":
                        continue
                elif order == "pres":
                    break
                else:
                    break
        elif order == "pres":
            return
        else:
            return


def createThread(type, args):
    threadId = round(time.time() * 1000)
    if type == 'cancel':
        scheduler.add_job(func=orderCancel, args=[threadId, args], trigger=None, id=f"{threadId}")
    elif type == 'check':
        scheduler.add_job(func=orderCheck, args=[threadId, args], trigger="interval", id=f"{threadId}", seconds=1)
    elif type == 'create':
        scheduler.add_job(func=alimYap, args=[threadId, args], trigger=None, id=f"{threadId}")