import websocket, json, datetime, telepot, time, random
from binance.enums import *
from telepot.loop import MessageLoop
import handlerOrder as oh
from telegramHandler import on_chat_message, on_callback_query, on_chosen_inline_result
from loggerM import sendLog
from telegramHandler import sendTelegram
import coinControl as cc
import config

bot = telepot.Bot(config.TOKEN)
answerer = telepot.helper.Answerer(bot)

def on_open(ws):
    sendLog("Bexy started to working. Version is: " + config.branch + " " + config.version)
    if config.run != True:
        sendLog("Config'den gelen yanıt çalışmamam gerektiğini söylüyor.")
        on_close("s")
    sendLog('Socket connection started.')
    MessageLoop(bot, {'chat': on_chat_message, 'callback_query': on_callback_query, 'chosen_inline_result': on_chosen_inline_result}).run_as_thread()
    sendLog('Listening ...')
    oh.startCheck()
    oh.socketClose()

def on_close(ws):
    sendLog('Socket connection ended.')
    sendLog('Process stopped.')
    oh.stopJobs()
    oh.socketClose()
    quit()

channelId = config.channelId

def orderAc(coin, coinAlimEmriDeger, pres, type):
    sleepTime = random.uniform(0.2, 0.8)
    time.sleep(sleepTime)
    oh.createThread("create", {"orderType": str(type), "coinAlimEmriDeger": float(coinAlimEmriDeger), "pres": int(pres), "coin": str(coin).lower(), "type": "all"})

def orderCreate(symbol, TRADE_SYMBOL, coinAlimEmriDeger, coinDeger, side):
    coinsJsonFile = open("coins.json", "r+")
    coind = json.load(coinsJsonFile)
    coin = coind[symbol]
    kusur = coin['pres']
    bildirimGonderildi = coind[symbol]['bildirimGonderildi']

    if side == "al":
        if bildirimGonderildi == 0:
            bildirimGonderildi = 2
            coind[symbol]['bildirimGonderildi'] = bildirimGonderildi
            sendLog(f"trying to send notification for buy {TRADE_SYMBOL} from {coinAlimEmriDeger} USDT")
            sent = sendTelegram(
            channelId, f"------ALIŞ EMRI------\nCoin Sembol: {TRADE_SYMBOL}\nMum Kapanışı: {coinDeger}\nEmir Koyulacak Fiyat: {coinAlimEmriDeger}")
            if sent['ok'] == True:
                sendLog(f"------BUY ORDER------\nCoin Symbol: {TRADE_SYMBOL}\nCandle Close: {coinDeger}\nOrder Price: {coinAlimEmriDeger}")
                orderAc(str(symbol), coinAlimEmriDeger, kusur, side)
            else:
                sendLog("Error while sending message to channel\n{}".format(sent['description']))
        elif bildirimGonderildi == 2:
            bildirimGonderildi = 1
            coind[symbol]['bildirimGonderildi'] = bildirimGonderildi
            sendLog(f"trying to send notification for sell {TRADE_SYMBOL} from {coinAlimEmriDeger} USDT")
            sent = sendTelegram(channelId, f"------SATIŞ EMRI------\nCoin Sembol: {TRADE_SYMBOL}\nMum Kapanışı: {coinDeger}\nEmir Koyulacak Fiyat: {coinAlimEmriDeger}")
            if sent['ok'] == True:
                sendLog(f"------SELL ORDER------\nCoin Symbol: {TRADE_SYMBOL}\nCandle Close: {coinDeger}\nOrder Price: {coinAlimEmriDeger}")
                orderAc(str(symbol), coinAlimEmriDeger, kusur, side)
            else:
                sendLog("Error while sending message to channel\n{}".format(sent['description']))
    elif side == "sat":
        if bildirimGonderildi == 0:
            bildirimGonderildi = 1
            coind[symbol]['bildirimGonderildi'] = bildirimGonderildi
            sendLog(f"trying to send notification for sell {TRADE_SYMBOL} from {coinAlimEmriDeger} USDT")
            sent = sendTelegram(
            channelId, f"------SATIŞ EMRI------\nCoin Sembol: {TRADE_SYMBOL}\nMum Kapanışı: {coinDeger}\nEmir Koyulacak Fiyat: {coinAlimEmriDeger}")
            if sent['ok'] == True:
                sendLog(f"------SELL ORDER------\nCoin Symbol: {TRADE_SYMBOL}\nCandle Close: {coinDeger}\nOrder Price: {coinAlimEmriDeger}")
                orderAc(str(symbol), coinAlimEmriDeger, kusur, side)
            else:
                sendLog("Error while sending message to channel\n{}".format(sent['description']))
        elif bildirimGonderildi == 2:
            bildirimGonderildi = 1
            coind[symbol]['bildirimGonderildi'] = bildirimGonderildi
            sendLog(f"trying to send notification for sell {TRADE_SYMBOL} from {coinAlimEmriDeger} USDT")
            sent = sendTelegram(channelId, f"------SATIŞ EMRI------\nCoin Sembol: {TRADE_SYMBOL}\nMum Kapanışı: {coinDeger}\nEmir Koyulacak Fiyat: {coinAlimEmriDeger}")
            if sent['ok'] == True:
                sendLog(f"------SELL ORDER------\nCoin Symbol: {TRADE_SYMBOL}\nCandle Close: {coinDeger}\nOrder Price: {coinAlimEmriDeger}")
                orderAc(str(symbol), coinAlimEmriDeger, kusur, side)
            else:
                sendLog("Error while sending message to channel\n{}".format(sent['description']))
    coinsJsonFile.close()
    jsonFile = open("coins.json", "w+")
    jsonFile.write(json.dumps(coind, indent=4, sort_keys=True))
    jsonFile.close()

def coinControl(symbol):
    time.sleep(1)
    coinsJsonFile = open("coins.json", "r+")
    coind = json.load(coinsJsonFile)
    symbol = str(symbol).lower()
    TRADE_SYMBOL = symbol.upper() + "USDT"
    control = cc.Controller(symbol)
    t3 = control.tillsonCheck()
    redi, bluei = control.stochCheck()
    t3side = control.tillsonSignal(t3)
    rbside = control.blueRedCheck(redi, bluei)
    stochside = control.stochRSIControl()
    macdside = control.macdCheck()
    control.controlNotify()
    if t3side == False: t3side = coind[symbol]['t3']['sinyal']
    if macdside == False: macdside = coind[symbol]['macd']['sinyal']
    if stochside == "al" or stochside == "sat":
        if t3side == "al" or t3side == "sat":
            coinAlimDeger = control.coinBuyPriceCheck(stochside)
            coinDeger = control.coinDeger
            control.end()
            coinsJsonFile.close()
            if macdside != "al" or macdside != "sat": macdside = False
            if t3side == stochside and t3side == macdside and macdside == stochside:
                orderCreate(symbol, TRADE_SYMBOL, coinAlimDeger, coinDeger, stochside)
            else:
                sendLog("Order Isn't Created. T3 and Stoch and MACD isn't equal.\n" + "Stock Side: " + str(stochside) + "\nT3 Side: " + str(t3side) + "\nMACD Side: " + str(macdside))

def check(ws, message):
    coins = ["ada", "btc", "eth", "ltc", "dent", "storj", "btt", "vet", "doge", "hot", "sxp", "xlm", "algo", "mtl", "trx", "reef", "one", "xrp"]
    json_message = json.loads(message)
    candle = json_message['k']
    is_candle_closed = candle['x']
    if is_candle_closed:
        for xd in coins:
            sleepTime = random.uniform(1.05, 1.45)
            time.sleep(sleepTime)
            oh.scheduler.add_job(func=coinControl, args=[str(xd)], trigger=None, id=f"{round(time.time() * 1000)}")
        sendLog("Date: " + str(datetime.datetime.now()) + " sent!")

wss = websocket.WebSocketApp(config.SOCKETS, on_open=on_open, on_close=on_close, on_message=check)
wss.run_forever()