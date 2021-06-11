from logging import exception
import time
import json
import os
import time
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from binance.client import Client
from binance.enums import *
from loggerM import sendLog
from telegramHandler import sendTelegram

stop = {}
scheduler = BackgroundScheduler({
    'apscheduler.executors.default': {
        'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
        'max_workers': '9999999999999'
    },
    'apscheduler.job_defaults.max_instances': '999999999999'})
scheduler.start()

# Cancel position orders with type of "all" and "user". Requests comes from Telegram commands.


# {"type": "all / user", "userId": 0 / 10001, "coin": "ALGO/MKR/ADA", "orderId": "578678"}
def orderCancel(threadId, args):
    coin = str(args['coin']).lower()
    if args['type'] == "all":
        for dirs in os.walk("users"):
            usersArray = dirs[1]
            for x in usersArray:
                x = str(x)
                positionOrderJsonFile = open(
                    "users/{}/positionOrders.json".format(x), "r+")
                configJsonFile = open("users/{}/config.json".format(x), "r+")
                apiJsonFile = open(
                    "users/{}/binanceApiKeys.json".format(x), "r+")
                pnlJsonFile = open("users/{}/pnlHistory.json".format(x), "r+")
                positionHistoryJsonFile = open(
                    "users/{}/positionHistory.json".format(x), "r+")
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
                            api = [
                                x for x in userApis if x['apiKeyId'] == int(a)]
                            api = api[0]
                            apiKey = api['apiKey']
                            apiSecret = api['apiSecret']
                            apiName = api['apiName']
                            client = Client(apiKey, apiSecret)
                            for order in positionOrders:
                                if order['coin'] == coin.upper():
                                    coinx = str(coin.upper()) + "USDT"
                                    position = client.futures_account(
                                        recvWindow=50000, timestamp=round(time.time() * 1000))['positions']
                                    position = [
                                        y for y in position if y['symbol'] == coinx]
                                    pnl = float(
                                        position[0]['unrealizedProfit'])
                                    bougthQuantity = int(
                                        order['bougthQuantity'])
                                    spentMoney = float(order['spentMoney'])
                                    orderType = str(order['orderType'])
                                    roe = str(order['roe'])
                                    karzarar = "KÂR"
                                    if pnl < 0:
                                        karzarar = "ZARAR"
                                    orderId = str(order['orderId'])
                                    orderTypex = ""
                                    if orderType == "BUY":
                                        orderTypex = "SELL"
                                    elif orderType == "SELL":
                                        orderTypex = "BUY"
                                    cancelPosition = client.futures_create_order(
                                        symbol=coinx, side=orderTypex, type="MARKET", quantity=bougthQuantity, recvWindow=50000, timestamp=round(time.time() * 1000))
                                    sendTelegram(str(userConfig['telegramChatId']), "------İŞLEMDEN ÇIKILDI ({})------\nCoin Sembol: {}\nİşlem Tipi: {}\nİşlem Id: {}\nMiktar: {}\nHarcama: {}\nPNL: {}".format(
                                        karzarar, coinx, orderType, orderId, bougthQuantity, spentMoney, pnl))
                                    with open("users/{}/positionOrders.json".format(x), encoding='utf-8') as json_data:
                                        nations = json.load(json_data)
                                    nations_new = [
                                        x for x in nations if x['coin'] != coin.upper()]
                                    with open("users/{}/positionOrders.json".format(x), mode='w', encoding='utf-8') as json_data:
                                        json.dump(
                                            nations_new, json_data, indent=2)
            break
    elif type == "user":  # under construction
        x = str(args['userId'])
        positionOrderJsonFile = open(
            "users/{}/positionOrders.json".format(x), "r+")
        configJsonFile = open("users/{}/config.json".format(x), "r+")
        apiJsonFile = open("users/{}/binanceApiKeys.json".format(x), "r+")
        pnlJsonFile = open("users/{}/pnlHistory.json".format(x), "r+")
        positionHistoryJsonFile = open(
            "users/{}/positionHistory.json".format(x), "r+")
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
                        position = client.futures_account(
                            recvWindow=50000, timestamp=round(time.time() * 1000))['positions']
                        position = [
                            y for y in position if y['symbol'] == coinx]
                        pnl = float(position[0]['unrealizedProfit'])
                        bougthQuantity = int(order['bougthQuantity'])
                        spentMoney = float(order['spentMoney'])
                        orderType = str(order['orderType'])
                        roe = str(order['roe'])
                        karzarar = "KÂR"
                        if pnl < 0:
                            karzarar = "ZARAR"
                        orderId = str(order['orderId'])
                        orderTypex = ""
                        if orderType == "BUY":
                            orderTypex = "SELL"
                        elif orderType == "SELL":
                            orderTypex = "BUY"
                        cancelPosition = client.futures_create_order(
                            symbol=coinx, side=orderTypex, type="MARKET", quantity=bougthQuantity, recvWindow=50000, timestamp=round(time.time() * 1000))
                        sendTelegram(str(userConfig['telegramChatId']), "------İŞLEMDEN ÇIKILDI ({})------\nCoin Sembol: {}\nİşlem Tipi: {}\nİşlem Id: {}\nMiktar: {}\nHarcama: {}\nPNL: {}".format(
                            karzarar, coinx, orderType, orderId, bougthQuantity, spentMoney, pnl))

# Get information about order by order id from Binance


def getOrder(id, symbol, apiKey, apiSecret):
    try:
        client = Client(apiKey, apiSecret)
        order = client.futures_get_order(
            symbol=symbol, orderId=id, recvWindow=50000, timestamp=round(time.time() * 1000))
        return order
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

# When order is goes to Position checkPnl function starts to work for check position status.


def checkPnl(threadId, args):
    orderId = str(args['orderId'])
    symbol = str(args['symbol'])
    orderType = str(args['orderType'])
    quantity = str(args['quantity'])
    userId = str(args['userId'])
    spent = str(args['spent'])
    positionOrderJsonFile = open(
        "users/{}/positionOrders.json".format(userId), "r+")
    configJsonFile = open("users/{}/config.json".format(userId), "r+")
    apiJsonFile = open("users/{}/binanceApiKeys.json".format(userId), "r+")
    pnlJsonFile = open("users/{}/pnlHistory.json".format(userId), "r+")
    positionExitJsonFile = open("users/{}/positionExit.json".format(userId), "r+")

    positionOrders = json.load(positionOrderJsonFile)
    userConfig = json.load(configJsonFile)
    userApis = json.load(apiJsonFile)
    pnlHistory = json.load(pnlJsonFile)
    positionExit = json.load(positionExitJsonFile)
    apiId = str([y for y in positionOrders if str(y['orderId']) == str(orderId)][0]['apiId'])

    api = [x for x in userApis if int(x['apiKeyId']) == int(apiId)]
    api = api[0]
    apiKey = api['apiKey']
    apiSecret = api['apiSecret']
    client = Client(apiKey, apiSecret)
    positions = client.futures_account(
        recvWindow=50000, timestamp=round(time.time() * 1000))['positions']
    position = [y for y in positions if str(y['symbol']) == str(symbol)]
    pnl = float(position[0]['unrealizedProfit'])
    karzarar = "KÂR"
    if pnl < 0:
        karzarar = "ZARAR"
    positionAmount = float(position[0]['positionAmt'])
    if positionAmount == 0:
        scheduler.remove_job(f"{threadId}", jobstore=None)
        openPositions = [z for z in positionOrders if str(
            z['orderId']) == str(orderId)]
        if openPositions:
            mesaj = "------İŞLEMDEN  MANUEL ÇIKILDI ({})------\nCoin Sembol: {}\nİşlem Tipi: {}\nİşlem Id: {}\nMiktar: {}\nHarcama: {}\nPNL: {}".format(
                karzarar, symbol, orderType, orderId, quantity, spent, pnl)
            sendTelegram(str(userConfig['telegramChatId']), mesaj)
            sendLog(mesaj)
            with open("users/{}/positionOrders.json".format(userId), encoding='utf-8') as json_data:
                nations = json.load(json_data)
            nations_new = [x for x in nations if x['orderId'] != orderId]
            with open("users/{}/positionOrders.json".format(userId), mode='w', encoding='utf-8') as json_data:
                json.dump(nations_new, json_data, indent=2)
    else:
        yuzdePnl = float(float((abs(pnl) * 100)) / float(spent))
        if pnl < 0: yuzdePnl = float("-" + str(yuzdePnl))
        orderTypex = ""
        if orderType == "BUY":
            orderTypex = "SELL"
        elif orderType == "SELL":
            orderTypex = "BUY"

        if positionExit['automaticExit'] == 1:
            if yuzdePnl > positionExit['profitExitPercent']:
                try:
                    cancelPosition = client.futures_create_order(symbol=symbol, side=orderTypex, type="MARKET", quantity=quantity, recvWindow=50000, timestamp=round(time.time() * 1000))
                    scheduler.remove_job(f"{threadId}", jobstore=None)
                except:
                    sendLog("While cancelling position got an error.")
                    return
                yuzdePnl = round(yuzdePnl, 3)
                pnl = round(pnl, 3)
                mesaj = "------İŞLEMDEN ÇIKILDI ({})------\nCoin Sembol: {}\nİşlem Tipi: {}\nİşlem Id: {}\nMiktar: {}\nHarcama: {}\nPNL: {}(% {})".format(karzarar, symbol, orderType, orderId, quantity, spent, pnl, yuzdePnl)
                sendTelegram(str(userConfig['telegramChatId']), mesaj)
                sendLog(mesaj)
                with open("users/{}/positionOrders.json".format(userId), encoding='utf-8') as json_data:
                    nations = json.load(json_data)
                nations_new = [x for x in nations if x['orderId'] != orderId]
                with open("users/{}/positionOrders.json".format(userId), mode='w', encoding='utf-8') as json_data:
                    json.dump(nations_new, json_data, indent=2)
                return
            elif yuzdePnl < float("-" + str(positionExit['lossNotifyPercent'])):
                if yuzdePnl < float("-" + str(positionExit['lossExitPercent'])):
                    try:
                        cancelPosition = client.futures_create_order(symbol=symbol, side=orderTypex, type="MARKET", quantity=quantity, recvWindow=50000, timestamp=round(time.time() * 1000))
                        scheduler.remove_job(f"{threadId}", jobstore=None)
                    except:
                        sendLog("While cancelling position got an error.")
                        return
                    yuzdePnl = round(yuzdePnl, 3)
                    pnl = round(pnl, 3)
                    mesaj = "------İŞLEMDEN ÇIKILDI ({})------\nCoin Sembol: {}\nİşlem Tipi: {}\nİşlem Id: {}\nMiktar: {}\nHarcama: {}\nPNL: {}(% {})".format(karzarar, symbol, orderType, orderId, quantity, spent, pnl, yuzdePnl)
                    sendTelegram(str(userConfig['telegramChatId']), mesaj)
                    sendLog(mesaj)
                    with open("users/{}/positionOrders.json".format(userId), encoding='utf-8') as json_data:
                        nations = json.load(json_data)
                    nations_new = [x for x in nations if x['orderId'] != orderId]
                    with open("users/{}/positionOrders.json".format(userId), mode='w', encoding='utf-8') as json_data:
                        json.dump(nations_new, json_data, indent=2)
                    return
                yuzdePnl = round(yuzdePnl, 3)
                pnl = round(pnl, 3)
                mesaj = "------ZARAR {}$------\nCoin Sembol: {}\nİşlem Tipi: {}\nİşlem Id: {}\nMiktar: {}\nHarcama: {}\nPNL: {}(% {})\nDaha fazla risk almak ve zarar etmemek için işlemden çıkmanızı öneriyoruz.".format(
                    pnl, symbol, orderType, orderId, quantity, spent, pnl, yuzdePnl)
                sendTelegram(str(userConfig['telegramChatId']), mesaj)
            sendLog(mesaj)

# Checking new orders before goes position.


def orderCheck(threadId, args):
    orderId = str(args['orderId'])
    symbol = str(args['symbol'])
    coin = str(args['coin']).upper()
    orderType = str(args['orderType'])
    coinAlimEmriDeger = float(args['coinAlimEmriDeger'])
    side = str(args['side'])
    quantity = int(args['quantity'])
    spent = float(args['spent'])
    apiId = int(args['apiId'])
    islemBaslamaTime = int(round(int(threadId)))
    anlikTime = int(round(time.time() * 1000))

    userId = str(args['userId'])

    positionOrderJsonFile = open(
        "users/{}/positionOrders.json".format(userId), "r+")
    configJsonFile = open("users/{}/config.json".format(userId), "r+")
    apiJsonFile = open("users/{}/binanceApiKeys.json".format(userId), "r+")
    pnlJsonFile = open("users/{}/pnlHistory.json".format(userId), "r+")
    positionHistoryJsonFile = open(
        "users/{}/positionHistory.json".format(userId), "r+")
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
        # Removes order if not goes position in 5 and half minutes.
        if (anlikTime - islemBaslamaTime) > (330 * 1000):
            scheduler.remove_job(f"{threadId}", jobstore=None)
            cancel = client.futures_cancel_order(
                symbol=symbol, orderId=orderId, recvWindow=50000, timestamp=round(time.time() * 1000))
            mesaj = "------İŞLEM EMRİ KALDIRILDI------\nCoin Sembol: {}\nİşlem Id: {}\nİşlem 5 Dakika İçerisinde Pozisyona Girmediği İçin Kaldırıldı.".format(
                symbol, orderId)
            sendLog(str(mesaj) + " " + str(userId))
            sendTelegram(str(userConfig['telegramChatId']), mesaj)
            with open("users/{}/openOrders.json".format(userId), encoding='utf-8') as json_data:
                nations = json.load(json_data)
            nations_new = [x for x in nations if str(
                x['orderId']) != str(orderId)]
            with open("users/{}/openOrders.json".format(userId), mode='w', encoding='utf-8') as json_data:
                json.dump(nations_new, json_data, indent=2)
    elif status == "CANCELED":
        scheduler.remove_job(f"{threadId}", jobstore=None)
        mesaj = "------İŞLEM İPTAL EDİLDİ------\nCoin Sembol: {}\nİşlem Id: {}\nİşlem Manuel Olarak Kapatıldı".format(
            symbol, orderId)
        sendLog(str(mesaj) + " " + str(userId))
        sendTelegram(str(userConfig['telegramChatId']), mesaj)
        with open("users/{}/openOrders.json".format(userId), encoding='utf-8') as json_data:
            nations = json.load(json_data)
        nations_new = [x for x in nations if str(x['orderId']) != str(orderId)]
        with open("users/{}/openOrders.json".format(userId), mode='w', encoding='utf-8') as json_data:
            json.dump(nations_new, json_data, indent=2)
    elif status != "NEW":
        scheduler.remove_job(f"{threadId}", jobstore=None)
        mesaj = "------İŞLEM BAŞLADI------\nCoin Sembol: {}\nİşlem Tipi: {}\nİşlem Id: {}\nMiktar: {}\nHarcama: {}\nCoin Giriş Değer: {}".format(
            symbol, orderType, order['orderId'], quantity, spent, coinAlimEmriDeger)
        sendLog(str(mesaj) + " " + str(userId))
        sendTelegram(str(userConfig['telegramChatId']), mesaj)
        appendCoin = {"coin": coin, "orderId": str(order['orderId']), "entryPrice": float(coinAlimEmriDeger), "markPrice": 0.00, "bougthQuantity": float(
            quantity), "spentMoney": float(spent), "orderType": str(side), "pnl": 0.00, "roe": "0", "apiId": int(apiId)}
        createThread("pnl", args)
        with open("users/{}/openOrders.json".format(userId), encoding='utf-8') as json_data:
            nations = json.load(json_data)
        nations_new = [x for x in nations if str(x['orderId']) != str(orderId)]
        with open("users/{}/openOrders.json".format(userId), mode='w', encoding='utf-8') as json_data:
            json.dump(nations_new, json_data, indent=2)
        sendLog("Order successfully deleted from opened orders json." + " - ignore")
        with open("users/{}/positionOrders.json".format(userId), encoding='utf-8') as feedssjson:
            feedss = json.load(feedssjson)
        with open("users/{}/positionOrders.json".format(userId), mode='w', encoding='utf-8') as feedssjson:
            feedss.append(appendCoin)
            json.dump(feedss, feedssjson, indent=2)
        sendLog("Order successfully added to opened positions json." + " - ignore")
        with open("users/{}/positionHistory.json".format(userId), mode='r', encoding='utf-8') as feedsjson:
            feeds = json.load(feedsjson)
        with open("users/{}/positionHistory.json".format(userId), mode='w', encoding='utf-8') as feedsjson:
            feeds.append(appendCoin)
            json.dump(feeds, feedsjson, indent=2)
        sendLog("Order successfully added to positions history json." + " - ignore")

# Works when program stops. Reset coins.json for new start.


def socketClose():
    jsonFile = open("coins.json", "r+")
    coins = json.load(jsonFile)
    jsonFile.close()
    coinList = coins.keys()
    for coin in coinList:
        coins[coin]['bildirimGonderildi'] = 0
        coins[coin]['stochRSI']['eskiUstte'] = 0
        coins[coin]['stochRSI']['ustte'] = 0
        coins[coin]['stochRSI']['kesisti'] = 0
        coins[coin]['t3']['sinyal'] = False
        coins[coin]['t3']['eskiSinyal'] = False
        coins[coin]['macd']['sinyal'] = False
        coins[coin]['macd']['eskiSinyal'] = False
    jsonFile = open("coins.json", "w+")
    jsonFile.write(json.dumps(coins, indent=4, sort_keys=True))
    jsonFile.close()
    sendLog('All coins datas resetted successfully.')

# Closes wathcing coin for spesific user. Turns coins status active 1 to 0


def closeCoin(threadId, args):
    userId = str(args['userId'])
    chatId = str(args['chatId'])
    if str(args['type']) == "all":
        jsonFile = open("users/{}/coins.json".format(userId), "r+")
        coins = json.load(jsonFile)
        jsonFile.close()
        coinList = coins.keys()
        for coin in coinList:
            if coins[coin]['active'] == 0:
                mesaj = f"{coin} zaten deaktif olarak ayarlı."
                sendTelegram(chatId, mesaj)
            coins[coin]['active'] = 0
        jsonFile = open("users/{}/coins.json".format(userId), "w+")
        jsonFile.write(json.dumps(coins, indent=4, sort_keys=True))
        jsonFile.close()
    else:
        coin = str(args['coin']).lower()
        jsonFile = open("users/{}/coins.json".format(userId), "r+")
        coins = json.load(jsonFile)
        jsonFile.close()
        if coins[coin]['active'] == 0:
            mesaj = f"{coin} zaten deaktif olarak ayarlı."
            sendTelegram(chatId, mesaj)
        coins[coin]['active'] = 0
        jsonFile = open("users/{}/coins.json".format(userId), "w+")
        jsonFile.write(json.dumps(coins, indent=4, sort_keys=True))
        jsonFile.close()

# Allows wathcing coin for spesific user. Turns coins status active 0 to 1


def openCoin(threadId, args):
    userId = str(args['userId'])
    chatId = str(args['chatId'])
    if str(args['type']) == "all":
        jsonFile = open("users/{}/coins.json".format(userId), "r+")
        coins = json.load(jsonFile)
        jsonFile.close()
        coinList = coins.keys()
        for coin in coinList:
            if coins[coin]['active'] == 1:
                mesaj = f"{coin} zaten aktif olarak ayarlı."
                sendTelegram(chatId, mesaj)
            coins[coin]['active'] = 1
        jsonFile = open("users/{}/coins.json".format(userId), "w+")
        jsonFile.write(json.dumps(coins, indent=4, sort_keys=True))
        jsonFile.close()
    else:
        coin = str(args['coin']).lower()
        jsonFile = open("users/{}/coins.json".format(userId), "r+")
        coins = json.load(jsonFile)
        jsonFile.close()
        if coins[coin]['active'] == 1:
            mesaj = f"{coin} zaten aktif olarak ayarlı."
            sendTelegram(chatId, mesaj)
        coins[coin]['active'] = 1
        jsonFile = open("users/{}/coins.json".format(userId), "w+")
        jsonFile.write(json.dumps(coins, indent=4, sort_keys=True))
        jsonFile.close()

# Allows wathcing order sides like long or short (buy and sell) for spesific user. Turns side status "false" to "true"


def openSide(threadId, args):
    userId = str(args['userId'])
    chatId = str(args['chatId'])
    if str(args['type']) == "all":
        jsonFile = open("users/{}/config.json".format(userId), "r+")
        config = json.load(jsonFile)
        jsonFile.close()
        if config['long'] == "true":
            mesaj = "Long işlem ayarınız zaten açık."
            sendTelegram(chatId, mesaj)
        config['long'] = "true"
        if config['short'] == "true":
            mesaj = "Short işlem ayarınız zaten açık."
            sendTelegram(chatId, mesaj)
        config['short'] = "true"
        jsonFile = open("users/{}/config.json".format(userId), "w+")
        jsonFile.write(json.dumps(config, indent=4, sort_keys=True))
        jsonFile.close()
        mesaj = "Short ve Long işleminiz açılmıştır."
        sendTelegram(chatId, mesaj)
    elif str(args['type']) == "long":
        jsonFile = open("users/{}/config.json".format(userId), "r+")
        config = json.load(jsonFile)
        jsonFile.close()
        if config['long'] == "true":
            mesaj = "Long işlem ayarınız zaten açık."
            sendTelegram(chatId, mesaj)
        config['long'] = "true"
        jsonFile = open("users/{}/config.json".format(userId), "w+")
        jsonFile.write(json.dumps(config, indent=4, sort_keys=True))
        jsonFile.close()
        mesaj = "Long işleminiz açılmıştır."
        sendTelegram(chatId, mesaj)
    else:
        jsonFile = open("users/{}/config.json".format(userId), "r+")
        config = json.load(jsonFile)
        jsonFile.close()
        if config['short'] == "true":
            mesaj = "Short işlem ayarınız zaten açık."
            sendTelegram(chatId, mesaj)
        config['short'] = "true"
        jsonFile = open("users/{}/config.json".format(userId), "w+")
        jsonFile.write(json.dumps(config, indent=4, sort_keys=True))
        jsonFile.close()
        mesaj = "Short işleminiz açılmıştır."
        sendTelegram(chatId, mesaj)

# Closes wathcing order sides like long or short (buy and sell) for spesific user. Turns side status "true" to "false"


def closeSide(threadId, args):
    userId = str(args['userId'])
    chatId = str(args['chatId'])
    if str(args['type']) == "all":
        jsonFile = open("users/{}/config.json".format(userId), "r+")
        config = json.load(jsonFile)
        jsonFile.close()
        if config['long'] == "false":
            mesaj = "Long işlem ayarınız zaten kapalı."
            sendTelegram(chatId, mesaj)
        config['long'] = "false"
        if config['short'] == "false":
            mesaj = "Short işlem ayarınız zaten kapalı."
            sendTelegram(chatId, mesaj)
        config['short'] = "false"
        jsonFile = open("users/{}/config.json".format(userId), "w+")
        jsonFile.write(json.dumps(config, indent=4, sort_keys=True))
        jsonFile.close()
        mesaj = "Short ve Long işleminiz kapatılmıştır."
        sendTelegram(chatId, mesaj)
    elif str(args['type']) == "long":
        jsonFile = open("users/{}/config.json".format(userId), "r+")
        config = json.load(jsonFile)
        jsonFile.close()
        if config['long'] == "false":
            mesaj = "Long işlem ayarınız zaten kapalı."
            sendTelegram(chatId, mesaj)
        config['long'] = "false"
        jsonFile = open("users/{}/config.json".format(userId), "w+")
        jsonFile.write(json.dumps(config, indent=4, sort_keys=True))
        jsonFile.close()
        mesaj = "Long işleminiz kapatılmıştır."
        sendTelegram(chatId, mesaj)
    else:
        jsonFile = open("users/{}/config.json".format(userId), "r+")
        config = json.load(jsonFile)
        jsonFile.close()
        if config['short'] == "false":
            mesaj = "Short işlem ayarınız zaten kapalı."
            sendTelegram(chatId, mesaj)
        config['short'] = "false"
        jsonFile = open("users/{}/config.json".format(userId), "w+")
        jsonFile.write(json.dumps(config, indent=4, sort_keys=True))
        jsonFile.close()
        mesaj = "Short işleminiz kapatılmıştır."
        sendTelegram(chatId, mesaj)


def clientControl(apiKey, apiSecret, TRADE_SYMBOL):
    time.sleep(0.15)
    try:
        client = Client(apiKey, apiSecret)
        budget = client.futures_account(recvWindow=50000, timestamp=round(time.time() * 1000))
        return client
    except:
        return False

def orderMake(qnt, userId, price, apiId, alimButce, TRADE_SYMBOL, side, coin, availableBalance, coinDeger, userConfig, client, a):
                                try:
                                    qnt = str(float(round(qnt)))
                                    if "." in qnt:
                                        qnt = qnt.split(".")[0]
                                    sendLog("Order Request Sending to Binance for user: " + str(userId) + "\nAPI Key Id: " + str(apiId) + " - ignore")
                                    order = client.futures_create_order(symbol=TRADE_SYMBOL, side=side, type="STOP", timeInForce="GTC",
                                                                        quantity=qnt, price=price, stopPrice=price, recvWindow=50000, timestamp=round(time.time() * 1000))
                                    appendOrder = {"coin": coin.upper(), "orderId": order['orderId'], "entryPrice": price, "bougthQuantity": qnt,
                                                "spentMoney": alimButce, "orderType": side, "userId": userId, "apiId": int(apiId)}
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
                                    mesaj = "------EMİR KOYULDU------\nCoin Sembol: {}\nİşlem Tipi: {}\nİşlem Id: {}\nAlım Miktarı: {}\nAlım Yapılacak Değer: {}\nHarcanan Tutar: {}\nİşlem Öncesi Kullanılabilir Bakiye: {}".format(
                                        TRADE_SYMBOL, side, order['orderId'], qnt, price, alimButce, availableBalance)
                                    sendTelegram(
                                        str(userConfig['telegramChatId']), mesaj)
                                    createThread("check", {"orderId": order['orderId'], "symbol": TRADE_SYMBOL, "side": side, "coin": coin,
                                                "orderType": side, "coinAlimEmriDeger": price, "quantity": qnt, "spent": alimButce, "userId": userId, "apiId": a})
                                    return order
                                except Exception as e:
                                    mesaj = "an exception occured - {}\nCoin: {}".format(e, TRADE_SYMBOL) + " - ignore"
                                    sendLog(mesaj)
                                    e = str(e)
                                    if "2021" in e:
                                        if side == "SELL":
                                            sendLog(
                                                "ERROR: Activation price should be smaller than current price." + " - ignore")
                                        elif side == "BUY":
                                            sendLog(
                                                "ERROR: Activation price should be larger than current price." + " - ignore")
                                        return "immediately"
                                    elif "1111" in e:
                                        sendLog("Coin: {} | Quantity: {} | Mark: {} | Limit: {}".format(TRADE_SYMBOL, qnt, coinDeger, price)  + " - ignore")
                                        return "pres"

# Creating order function. Creates order from datas which cam from "alimYap" function.

def createOrder(args):
    coin = str(args['coin']).lower()
    sendLog('Creating order..' + " - ignore")
    if args['type'] == "all":
        for dirs in os.walk("users"):
            usersArray = dirs[1]
            for x in usersArray:
                x = str(x)
                sendLog("Starting to check json files for user." + " - ignore")
                openOrdersJsonFile = open(
                    "users/{}/openOrders.json".format(x), "r+")
                positionOrderJsonFile = open(
                    "users/{}/positionOrders.json".format(x), "r+")
                configJsonFile = open("users/{}/config.json".format(x), "r+")
                apiJsonFile = open(
                    "users/{}/binanceApiKeys.json".format(x), "r+")
                coinsJsonFile = open("users/{}/coins.json".format(x), "r+")
                openOrders = json.load(openOrdersJsonFile)
                positionOrders = json.load(positionOrderJsonFile)
                userConfig = json.load(configJsonFile)
                userApis = json.load(apiJsonFile)
                userCoins = json.load(coinsJsonFile)
                sendLog("Finished to get json files for user." + " - ignore")
                userId = str(userConfig['userId'])
                TRADE_SYMBOL = str(coin.upper()) + "USDT"
                coinData = userCoins[coin]
                if coinData['active'] == 1:
                    for a in coinData['apiKeys']:
                        api = [x for x in userApis if x['apiKeyId'] == int(a)]
                        api = api[0]
                        apiKey = api['apiKey']
                        apiSecret = api['apiSecret']
                        apiName = api['apiName']
                        apiId = api['apiKeyId']
                        time.sleep(0.2)
                        client = clientControl(apiKey, apiSecret, apiName, apiId, TRADE_SYMBOL)
                        if client == False:
                            sendLog("While connecting client error occured.\nApi Id: {} | Api Name: {} | Coin: {}".format(apiId, apiName, TRADE_SYMBOL))
                            return
                        side = args['side']
                        pres = args['pres']
                        budget = float(
                            client.futures_account_balance()[1]['balance'])
                        sendLog("Got the budget from api key." + " - ignore")
                        minusBudget = float(0)
                        for x in openOrders:
                            minusBudget = float(
                                minusBudget) + float((float(x['entryPrice']) * float(x['bougthQuantity'])) / float(10))
                        for x in positionOrders:
                            minusBudget = float(
                                minusBudget) + float((float(x['entryPrice']) * float(x['bougthQuantity'])) / float(10))
                        availableBalance = budget - minusBudget
                        orderBudgetLimit = int(userConfig['orderBudgetLimit'])
                        alimButce = float(
                            float(availableBalance) * float(float(orderBudgetLimit) / float(100)))
                        price = float(args['coinAlimEmriDeger'])
                        coinDeger = float(args['coinDeger'])
                        qnt = float(float(float(alimButce) / float(price)) * 10)
                        sendLog('Finished to check availible balance to use.' + " - ignore")
                        if str(side).lower() == "BUY".lower():
                            if str(userConfig['long']) == "false":
                                mesaj = "------LONG İŞLEM KAPALI------\nCoin Sembol: {}\nLong işlem ayarınız kapalı olduğundan bu işleme girilmedi.".format(
                                    TRADE_SYMBOL)
                                sendLog(str(mesaj) + " " + str(userId))
                                sendTelegram(
                                    str(userConfig['telegramChatId']), mesaj)
                                return
                        elif str(side).lower() == "SELL".lower():
                            if str(userConfig['short']) == "false":
                                mesaj = "------SHORT İŞLEM KAPALI------\nCoin Sembol: {}\nShort işlem ayarınız kapalı olduğundan bu işleme girilmedi.".format(
                                    TRADE_SYMBOL)
                                sendLog(str(mesaj) + " " + str(userId))
                                sendTelegram(
                                    str(userConfig['telegramChatId']), mesaj)
                                return
                        sendLog(
                            'Finished to check long and short trade settings.' + " - ignore")
                        if availableBalance < alimButce:
                            mesaj = "------YETERSİZ BAKİYE------\nİşlem İçin Gereken Tutar: {}\nHesabınızdaki Kullanılabilir Bakiye: {}\nİşleme bakiyeniz yetersiz olduğu için girilemedi.".format(
                                availableBalance, alimButce)
                            sendLog(str(mesaj) + " " + str(userId))
                            sendTelegram(
                                str(userConfig['telegramChatId']), mesaj)
                            return
                        sendLog(
                            'Finished to check availible budget is enough for trade.' + " - ignore")
                        sameOrderCoin = [x for x in openOrders if x['coin'] == str(coin).upper()]
                        sameOrder = [x for x in sameOrderCoin if x['apiId'] == int(apiId)]
                        sameCoin = [x for x in positionOrders if x['coin'] == str(coin).upper()]
                        samePosition = [x for x in sameCoin if x['apiId'] == int(apiId)]
                        if len(samePosition) > 0 or len(sameOrder) > 0:
                            if (samePosition['apiId'] == apiId) or (sameOrder['apiId'] == apiId):
                                mesaj = "------AKTİF İŞLEM VAR------\nCoin Sembol: {}\nApi ID: {}\nİşlem açılmak istenen coinde aktif bir işlem olduğu için yeni işlem açılmadı.".format(
                                    TRADE_SYMBOL, apiId)
                                sendLog(str(mesaj) + " " + str(userId))
                                sendTelegram(str(userConfig['telegramChatId']), mesaj)
                                return
                        sendLog(
                            'Finished to check any open or position order with same coin.' + " - ignore")
                        apiOpenOrders = [x for x in openOrders if x['apiId'] == int(apiId)]
                        apiPositionOrders =  [x for x in positionOrders if x['apiId'] == int(apiId)]
                        if (len(apiOpenOrders) + len(apiPositionOrders)) >= int(userConfig['maxActiveOrders']):
                            mesaj = "------MAKS İŞLEM LİMİTİ------\nKoyulan Maks İşlem Limiti: {}\nApi Adı: {}\nApi ID: {}\nBelirlemiş olduğunuz aynı anda maksimum işlem limiti aşılacak olduğu için yeni işleme girilemedi.".format(
                                int(userConfig['maxActiveOrders']), apiName, apiId)
                            sendLog(str(mesaj) + " " + str(userId))
                            sendTelegram(
                                str(userConfig['telegramChatId']), mesaj)
                            return
                        sendLog(
                            'Finished to check order count is higher than setted maximum order count.' + " - ignore")
                        if qnt < float(1):
                            mesaj = "------YETERSİZ BAKİYE------\nAlınacak Coin Miktarı: {}\nHesabınızdaki Kullanılabilir Bakiye: {}\nİşleme bakiyenizin bu coinden 1 tane alamayacak kadar az olması sebebiyle girilemedi.".format(
                                qnt, alimButce)
                            sendLog(str(mesaj) + " " + str(userId))
                            sendTelegram(
                                str(userConfig['telegramChatId']), mesaj)
                            return
                        order = orderMake(qnt, userId, price, apiId, alimButce, TRADE_SYMBOL, side, coin, availableBalance, coinDeger, userConfig, client, apiId)
            break

# The function for creates order. Starts from main.py by order side.


def alimYap(threadId, args):
    coinAlimEmriDeger = float(args['coinAlimEmriDeger'])
    orderType = str(args['orderType'])
    coin = str(args['coin'])
    pres = int(args['pres'])
    TRADE_SYMBOL = str(coin.upper()) + "USDT"
    price = str(float(requests.get("https://api.binance.com/api/v3/avgPrice?symbol={}".format(TRADE_SYMBOL)).json()['price']))
    coinDeger = float(str(price).split('.')[0] + "." + str(price).split('.')[1][0:pres])
    orderTypex = ""
    if orderType == "al":
        orderTypex = "BUY"
    else:
        orderTypex = "SELL"
    mesaj = "{} order request for {} came. Sending to orderCreate function.".format(
        str(orderTypex), str(coin))
    sendLog(mesaj)
    order = createOrder({"coin": coin, "side": orderTypex, "coinAlimEmriDeger": coinAlimEmriDeger, "pres": pres, "type": str(args['type']), "coinDeger": coinDeger, "type": "all"})
    islemBaslamaTime = int(round(time.time() * 1000))
    if order:
        if order == "immediately":
            while True:
                time.sleep(0.3)
                anlikTime = int(round(time.time() * 1000))
                price = str(float(requests.get(
                    "https://api.binance.com/api/v3/avgPrice?symbol={}".format(TRADE_SYMBOL)).json()['price']))
                coinDeger = float(str(price).split(
                    '.')[0] + "." + str(price).split('.')[1][0:pres])
                orderType = str(orderType)
                coinAlimEmriDegerx = 0.00
                orderTypex = ""
                if orderTypex == "al":
                    orderType = "BUY"
                    coinAlimEmriDegerx = float(
                        coinDeger + ((coinDeger / float(100)) * float(0.125)))
                else:
                    orderTypex = "SELL"
                    coinAlimEmriDegerx = float(
                        coinDeger - ((coinDeger / float(100)) * float(0.125)))
                coinAlimEmriDegerx = float(str(coinAlimEmriDegerx).split('.')[0] + "." + str(coinAlimEmriDegerx).split('.')[1][0:pres])
                order = createOrder({"coin": coin, "side": orderTypex, "coinAlimEmriDeger": coinAlimEmriDegerx,
                                    "pres": pres, "type": str(args['type']), "coinDeger": coinDeger, "type": "all"})
                if order:
                    if order == "immediately":
                        if (anlikTime - islemBaslamaTime) > (45 * 1000):
                            sendLog("Denemeler 30 saniyeyi geçtiği için işlem emri talebini kapattım.")
                            break
                        else:
                            continue
                    elif order == "pres":
                        break
                    else:
                        break
        elif order == "pres":
            return
        else:
            return

# Threading system.

def createThread(type, args):
    threadId = round(time.time() * 1000)
    if str(type) == "cancel":
        return scheduler.add_job(func=orderCancel, args=[threadId, args], trigger=None, id=f"{threadId}")
    elif str(type) == "check":
        return scheduler.add_job(func=orderCheck, args=[threadId, args], trigger="interval", id=f"{threadId}", seconds=1)
    elif str(type) == "pnl":
        return scheduler.add_job(func=checkPnl, args=[threadId, args], trigger="interval", id=f"{threadId}", seconds=1)
    elif str(type) == "create":
        return scheduler.add_job(func=alimYap, args=[threadId, args], trigger=None, id=f"{threadId}")
    elif str(type) == "close":
        return scheduler.add_job(func=closeCoin, args=[threadId, args], trigger=None, id=f"{threadId}")
    elif str(type) == "open":
        return scheduler.add_job(func=openCoin, args=[threadId, args], trigger=None, id=f"{threadId}")
    elif str(type) == "sideClose":
        return scheduler.add_job(func=closeSide, args=[threadId, args], trigger=None, id=f"{threadId}")
    elif str(type) == "sideOpen":
        return scheduler.add_job(func=openSide, args=[threadId, args], trigger=None, id=f"{threadId}")

# Wen program stops runs this function to remove all past jobs and shutdowns threading system.


def stopJobs():
    scheduler.remove_all_jobs(jobstore=None)
    scheduler.shutdown(wait=False)

# When program starts it runs this function first. Program starts to check if any open orders there or any position orders and starts to checking positions and orders function.


def startCheck():
    sendLog("Started to check open and position orders.")
    orders = 0
    for dirs in os.walk("users"):
        usersArray = dirs[1]
        for user in usersArray:
            user = str(user)
            openOrdersJsonFile = open(
                "users/{}/openOrders.json".format(user), "r+")
            positionOrderJsonFile = open(
                "users/{}/positionOrders.json".format(user), "r+")
            configJsonFile = open("users/{}/config.json".format(user), "r+")

            openOrders = json.load(openOrdersJsonFile)
            positionOrders = json.load(positionOrderJsonFile)
            userConfig = json.load(configJsonFile)
            for position in positionOrders:
                time.sleep(0.2)
                orders = orders + 1
                orderId = str(position['orderId'])
                symbol = str(position['coin']).upper() + "USDT"
                side = str(position['orderType'])
                coin = str(position['coin']).lower()
                orderType = str(position['orderType'])
                coinAlimEmriDeger = str(position['entryPrice'])
                quantity = str(position['bougthQuantity'])
                spent = str(position['spentMoney'])
                userId = str(userConfig['userId'])
                apiId = str(position['apiId'])
                createThread("pnl", {"orderId": orderId, "symbol": symbol, "side": side, "coin": coin, "orderType": orderType, "coinAlimEmriDeger": coinAlimEmriDeger, "quantity": quantity, "spent": spent, "userId": userId, "apiId": apiId})
                sendLog(f"checking position {orderId}")
            for order in openOrders:
                time.sleep(0.2)
                orders = orders + 1
                orderId = str(order['orderId'])
                symbol = str(order['coin']).upper() + "USDT"
                side = str(order['orderType'])
                coin = str(order['coin']).lower()
                orderType = str(order['orderType'])
                coinAlimEmriDeger = str(order['entryPrice'])
                quantity = str(order['bougthQuantity'])
                spent = str(order['spentMoney'])
                userId = str(userConfig['userId'])
                apiId = str(order['apiId'])
                createThread("check", {"orderId": orderId, "symbol": symbol, "side": side, "coin": coin, "orderType": orderType, "coinAlimEmriDeger": coinAlimEmriDeger, "quantity": quantity, "spent": spent, "userId": userId, "apiId": apiId})
                sendLog(f"checking order {orderId}")
    sendLog('Old orders and positions checking finished. Total checked positions and order is: ' + str(orders))
