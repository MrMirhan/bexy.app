import json
import pprint
from pkg_resources import add_activation_listener
from requests.api import request
import talib
import numpy
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
                                    cancelPosition = client.futures_create_order(symbol=coinx, side=orderTypex, type="MARKET", quantity=bougthQuantity, recvWindow=50000, timestamp=round(time.time() * 1000))
                                    main.sendTelegram(str(userConfig['telegramChatId']), "------İŞLEMDEN ÇIKILDI ({})------\nCoin Sembol: {}\nİşlem Tipi: {}\nİşlem Id: {}\nMiktar: {}\nHarcama: {}\nPNL: {}".format(karzarar, coinx, orderType, orderId, bougthQuantity, spentMoney, pnl))
                                    with open("users/{}/positionOrders.json".format(x), encoding='utf-8') as json_data:
                                        nations = json.load(json_data)
                                    nations_new = [x for x in nations if x['coin'] != coin.upper()]
                                    with open("users/{}/positionOrders.json".format(x), mode='w', encoding='utf-8') as json_data:
                                        json.dump(nations_new, json_data, indent=2)
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
                                    cancelPosition =  client.futures_create_order(symbol=coinx, side=orderTypex, type="MARKET", quantity=bougthQuantity, recvWindow=50000, timestamp=round(time.time() * 1000))
                                    main.sendTelegram(str(userConfig['telegramChatId']), "------İŞLEMDEN ÇIKILDI ({})------\nCoin Sembol: {}\nİşlem Tipi: {}\nİşlem Id: {}\nMiktar: {}\nHarcama: {}\nPNL: {}".format(karzarar, coinx, orderType, orderId, bougthQuantity, spentMoney, pnl))
def getOrder(id, symbol, apiKey, apiSecret):
    try:
        client = Client(apiKey, apiSecret)
        order = client.futures_get_order(symbol=symbol, orderId=id, recvWindow=50000, timestamp=round(time.time() * 1000))
        return order
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

def checkPnl(threadId, args):
    orderId = str(args['orderId'])
    symbol = str(args['symbol'])
    coin = str(args['coin']).upper()
    orderType = str(args['orderType'])
    coinAlimEmriDeger = float(args['coinAlimEmriDeger'])
    quantity = int(args['quantity'])
    userId = str(args['userId'])
    beforeBudget = float(args['beforeBudget'])
    spent = float(args['spent'])
    apiId = int(args['apiId'])
    islemBaslamaTime = int(round(int(threadId)))
    anlikTime = int(round(time.time() * 1000))

    positionOrderJsonFile = open("users/{}/positionOrders.json".format(userId), "r+")
    configJsonFile = open("users/{}/config.json".format(userId), "r+")
    apiJsonFile = open("users/{}/binanceApiKeys.json".format(userId), "r+")
    pnlJsonFile = open("users/{}/pnlHistory.json".format(userId), "r+")
    positionHistoryJsonFile = open("users/{}/positionHistory.json".format(userId), "r+")
    coinsJsonFile = open("users/{}/coins.json".format(userId), "r+")
                
    positionOrders = json.load(positionOrderJsonFile)
    userConfig = json.load(configJsonFile)
    userApis = json.load(apiJsonFile)
    pnlHistory = json.load(pnlJsonFile)
    positionHistory = json.load(positionHistoryJsonFile)
    userCoins = json.load(coinsJsonFile)

    api = [x for x in userApis if x['apiKeyId'] == int(apiId)]
    api = api[0]
    apiKey = api['apiKey']
    apiSecret = api['apiSecret']
    apiName = api['apiName']
    client = Client(apiKey, apiSecret)
    order = getOrder(orderId, symbol, apiKey, apiSecret)
    status = order['status']
    positions = client.futures_account(recvWindow=50000, timestamp=round(time.time() * 1000))['positions']
    position = [y for y in positions if y['symbol'] == symbol]
    pnl = float(position[0]['unrealizedProfit'])
    positionAmount = float(position[0]['positionAmt'])
    if positionAmount == 0:
        scheduler.remove_job(f"{threadId}", jobstore=None)
        openPositions = [z for z in positions if z['coin'] == coin]
        print(openPositions, len(openPositions))
        if len(openPositions) >= 1:
            mesaj = "------İŞLEM KAPATILDI (MANUEL)------\nCoin Sembol: {}\nİşlem Id: {}".format(symbol, orderId)
            main.sendTelegram(str(userConfig['telegramChatId']), mesaj)
            with open("users/{}/positionOrders.json".format(userId), encoding='utf-8') as json_data:
                nations = json.load(json_data)
            nations_new = [x for x in nations if x['coin'] != coin]
            with open("users/{}/positionOrders.json".format(userId), mode='w', encoding='utf-8') as json_data:
                json.dump(nations_new, json_data, indent=2)

def orderCheck(threadId, args):
    orderId = str(args['orderId'])
    symbol = str(args['symbol'])
    coin = str(args['coin']).upper()
    orderType = str(args['orderType'])
    coinAlimEmriDeger = float(args['coinAlimEmriDeger'])
    side = str(args['side'])
    quantity = int(args['quantity'])
    beforeBudget = float(args['beforeBudget'])
    spent = float(args['spent'])
    apiId = int(args['apiId'])
    islemBaslamaTime = int(round(int(threadId)))
    anlikTime = int(round(time.time() * 1000)) 

    userId = str(args['userId'])

    positionOrderJsonFile = open("users/{}/positionOrders.json".format(userId), "r+")
    configJsonFile = open("users/{}/config.json".format(userId), "r+")
    apiJsonFile = open("users/{}/binanceApiKeys.json".format(userId), "r+")
    pnlJsonFile = open("users/{}/pnlHistory.json".format(userId), "r+")
    positionHistoryJsonFile = open("users/{}/positionHistory.json".format(userId), "r+")
    coinsJsonFile = open("users/{}/coins.json".format(userId), "r+")
                
    positionOrders = json.load(positionOrderJsonFile)
    userConfig = json.load(configJsonFile)
    userApis = json.load(apiJsonFile)
    pnlHistory = json.load(pnlJsonFile)
    positionHistory = json.load(positionHistoryJsonFile)
    userCoins = json.load(coinsJsonFile)

    api = [x for x in userApis if x['apiKeyId'] == int(apiId)]
    api = api[0]
    apiKey = api['apiKey']
    apiSecret = api['apiSecret']
    apiName = api['apiName']
    client = Client(apiKey, apiSecret)
    order = getOrder(orderId, symbol, apiKey, apiSecret)
    status = order['status']
    if status == "NEW":
        if (anlikTime - islemBaslamaTime) > (60 * 1000) * 2:
            scheduler.remove_job(f"{threadId}", jobstore=None)
            print('20 Saniyedir işleme giremedi.')
            cancel = client.futures_cancel_order(symbol=symbol, orderId=orderId, recvWindow=50000, timestamp=round(time.time() * 1000))
            mesaj = "------İŞLEM EMRİ KALDIRILDI------\nCoin Sembol: {}\nİşlem Id: {}\nİşlem 2 Dakika İçerisinde Pozisyona Girmediği İçin Kaldırıldı.".format(symbol, orderId)
            main.sendTelegram(str(userConfig['telegramChatId']), mesaj)
            with open("users/{}/openOrders.json".format(userId), encoding='utf-8') as json_data:
                nations = json.load(json_data)
            nations_new = [x for x in nations if x['coin'] != coin]
            with open("users/{}/openOrders.json".format(userId), mode='w', encoding='utf-8') as json_data:
                json.dump(nations_new, json_data, indent=2)
    elif status == "CANCELED":
        scheduler.remove_job(f"{threadId}", jobstore=None)
        mesaj = "------İŞLEM İPTAL EDİLDİ------\nCoin Sembol: {}\nİşlem Id: {}\nİşlem Manuel Olarak Kapatıldı".format(symbol, orderId)
        main.sendTelegram(str(userConfig['telegramChatId']), mesaj)
        with open("users/{}/openOrders.json".format(userId), encoding='utf-8') as json_data:
            nations = json.load(json_data)
        nations_new = [x for x in nations if x['coin'] != coin]
        with open("users/{}/openOrders.json".format(userId), mode='w', encoding='utf-8') as json_data:
            json.dump(nations_new, json_data, indent=2)
    elif status != "NEW":
        scheduler.remove_job(f"{threadId}", jobstore=None)
        mesaj = "------İŞLEM BAŞLADI------\nCoin Sembol: {}\nİşlem Tipi: {}\nİşlem Id: {}\nMiktar: {}\nHarcama: {}\nCoin Giriş Değer: {}".format(symbol, orderType, order['orderId'], quantity, spent, coinAlimEmriDeger)
        main.sendTelegram(str(userConfig['telegramChatId']), mesaj)
    
        appendCoin = {"coin": coin, "orderId": str(order['orderId']), "entryPrice": float(coinAlimEmriDeger), "markPrice": 0.00, "bougthQuantity": float(quantity), "spentMoney": float(spent), "orderType": str(side), "pnl": 0.00, "roe": "0"}
        createThread("pnl", args)
        with open("users/{}/openOrders.json".format(userId), encoding='utf-8') as json_data:
            nations = json.load(json_data)
        nations_new = [x for x in nations if x['coin'] != coin]
        with open("users/{}/openOrders.json".format(userId), mode='w', encoding='utf-8') as json_data:
            json.dump(nations_new, json_data, indent=2)
        print("orders ok")
        with open("users/{}/positionOrders.json".format(userId), encoding='utf-8') as feedssjson:
            feedss = json.load(feedssjson)
        with open("users/{}/positionOrders.json".format(userId), mode='w', encoding='utf-8') as feedssjson:
            feedss.append(appendCoin)
            json.dump(feedss, feedssjson, indent=2)
        print("position ok")
        with open("users/{}/positionHistory.json".format(userId), mode='r', encoding='utf-8') as feedsjson:
            feeds = json.load(feedsjson)
        with open("users/{}/positionHistory.json".format(userId), mode='w', encoding='utf-8') as feedsjson:
            feeds.append(appendCoin)
            json.dump(feeds, feedsjson, indent=2)
        print("history ok")

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
                userId = str(userConfig['userId'])
                TRADE_SYMBOL = str(coin.upper()) + "USDT"
                coinData = userCoins[coin]
                if len(openOrders) == int(userConfig['maxActiveOrders']):
                    mesaj = "------MAKS İŞLEM LİMİTİ------\nKoyulan Maks İşlem Limiti: {}\nBelirlemiş olduğunuz aynı anda maksimum işlem limiti aşılacak olduğu için yeni işleme girilemedi.".format(int(userConfig['maxActiveOrders']))
                    main.sendTelegram(str(userConfig['telegramChatId']), mesaj)
                    return
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
                        if availableBalance < alimButce:
                            mesaj = "------YETERSİZ BAKİYE------\nİşlem İçin Gereken Tutar: {}\nHesabınızdaki Kullanılabilir Bakiye: {}\nİşleme bakiyeniz yetersiz olduğu için girilemedi.".format(availableBalance, alimButce)
                            main.sendTelegram(str(userConfig['telegramChatId']), mesaj)
                            return
                        try:
                            print("sending order")
                            order = client.futures_create_order(symbol=TRADE_SYMBOL, side=side, type="STOP", timeInForce = "GTC", quantity = qnt, price=price, stopPrice=price, recvWindow=50000, timestamp=round(time.time() * 1000))
                            appendOrder = {"coin": coin.upper(), "orderId": order['orderId'], "entryPrice": price, "bougthQuantity": qnt, "spentMoney": alimButce, "orderType": side}
                            with open("users/{}/openOrders.json".format(userId), mode='r', encoding='utf-8') as feedsjson:
                                feeds = json.load(feedsjson)
                            with open("users/{}/openOrders.json".format(userId), mode='w', encoding='utf-8') as feedsjson:
                                feeds.append(appendOrder)
                                json.dump(feeds, feedsjson, indent=2)
                            with open("users/{}/orderHistory.json".format(userId), mode='r', encoding='utf-8') as feedsjson:
                                feeds = json.load(feedsjson)
                            with open("users/{}/orderHistory.json".format(userId), mode='w', encoding='utf-8') as feedsjson:
                                feeds.append(appendOrder)
                                json.dump(feeds, feedsjson, indent=2)
                            mesaj = "------EMİR KOYULDU------\nCoin Sembol: {}\nİşlem Tipi: {}\nİşlem Id: {}\nAlım Miktarı: {}\nAlım Yapılacak Değer: {}\nHarcanan Tutar: {}\nİşlem Öncesi Kullanılabilir Bakiye: {}".format(TRADE_SYMBOL, side, order['orderId'], qnt, price, alimButce, availableBalance)
                            main.sendTelegram(str(userConfig['telegramChatId']), mesaj)
                            print(getOrder(order['orderId'], TRADE_SYMBOL, apiKey, apiSecret))
                            createThread("check", {"orderId": order['orderId'], "symbol": TRADE_SYMBOL, "side": side, "coin": coin, "orderType": side, "coinAlimEmriDeger": price, "quantity": qnt, "beforeBudget": availableBalance, "spent": alimButce, "userId": userId, "apiId": a})
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
        order = createOrder({"coin": coin, "side": orderTypex, "coinAlimEmriDeger": coinAlimEmriDeger, "pres": pres, "type": str(args['type'])})
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
    elif type == 'pnl':
        scheduler.add_job(func=checkPnl, args=[threadId, args], trigger="interval", id=f"{threadId}", seconds=1)
    elif type == 'create':
        scheduler.add_job(func=alimYap, args=[threadId, args], trigger=None, id=f"{threadId}")