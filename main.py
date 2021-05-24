from socket import SIO_LOOPBACK_FAST_PATH
import websocket
import json
import pprint
import talib
import numpy
import config
import requests
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException
import time
import json
from tradingview_ta import TA_Handler, Interval, Exchange
from decimal import Decimal
import math
import telebot
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC1, wait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import decimal
import random   
import sys, re, optparse 
import json
from threading import Thread

SOCKETS = f"wss://stream.binance.com:9443/ws/adausdt@kline_5m"

channelId = "-1001347995174"
token = "1776589751:AAH3HQRXe7tEJf5C-HnfBVeOBWta72Gbd_E"

def on_open(ws):
    print('Socket connection started.')

def on_close(ws):
    print('Socket connection ended.')

def generateStochasticRSI(close_array, timeperiod=14):
    rsi = talib.RSI(close_array, timeperiod)
    rsi = rsi[~numpy.isnan(rsi)]
    stochrsif, stochrsis = talib.STOCH(
        rsi, rsi, rsi, fastk_period=14, slowk_period=3, slowd_period=3)
    return stochrsif, stochrsis

def sendTelegram(cid, message):
    send_text = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={cid}&text={message}"
    response = requests.post(send_text)
    return response.json()

def format_number(num):
    try:
        dec = decimal.Decimal(num)
    except:
        return 'bad'
    tup = dec.as_tuple()
    delta = len(tup.digits) + tup.exponent
    digits = ''.join(str(d) for d in tup.digits)
    if delta <= 0:
        zeros = abs(tup.exponent) - len(tup.digits)
        val = '0.' + ('0'*zeros) + digits
    else:
        val = digits[:delta] + ('0'*tup.exponent) + '.' + digits[delta:]
    val = val.rstrip('0')
    if val[-1] == '.':
        val = val[:-1]
    if tup.sign:
        return '-' + val
    return val

def check(ws, message):
    coins = ["ada", "dent", "storj", "btt", "vet", "doge", "hot", "sxp", "xlm", "algo", "mtl", "trx", "reef", "one", "xrp"]
    json_message = json.loads(message)
    candle = json_message['k']
    is_candle_closed = candle['x']
    if is_candle_closed:
        for xd in coins:
                jsonFile = open("coins.json", "r")
                coind = json.load(jsonFile)
                jsonFile.close()

                coin = coind[xd]
                kusur = coin['pres']
                clientInfo = coin['apiCredentials']
                walletName = clientInfo[0]['walletName']
                bildirimGonderildi = coind[xd]['bildirimGonderildi']
                ustte = coin['ustte']
                kesisti = coin['kesisti']
                eskiUstte = coin['eskiUstte']
                
                client = Client(clientInfo[0]['apiKey'], clientInfo[0]['apiSecret'])
                TRADE_SYMBOL = xd.upper() + "USDT"

                close = str(float(requests.get("https://api.binance.com/api/v3/avgPrice?symbol={}".format(TRADE_SYMBOL)).json()['price']))
                close = float(str(close).split('.')[0] + "." + str(close).split('.')[1][0:kusur])
                klines = client.get_klines(symbol=TRADE_SYMBOL, interval='5m', limit=200)
                closec = [float(entry[4]) for entry in klines]
                close_array = numpy.asarray(closec)
                redi, bluei = generateStochasticRSI(close_array, timeperiod=14)
                bluei = bluei[~numpy.isnan(bluei)]
                redi = redi[~numpy.isnan(redi)]
                bluei = bluei[-1]
                redi = redi[-1]

                red = round(bluei, 2)
                blue = round(redi, 2)
                aradakiFark = abs(red - blue)
                print(f"------COIN DETAILS------\nsymbol: {TRADE_SYMBOL}\nperiod: 5m\nclose: {candle['c']}\n------STOCHASTIC RSI------\nblue: {blue}\nred: {red}\ndifference: {aradakiFark}")
                if red > blue:
                    ustte = 1
                    coind[xd]['ustte'] = ustte
                    eskiUstte = 2
                    coind[xd]['eskiUstte'] = eskiUstte
                else:
                    ustte = 2
                    coind[xd]['ustte'] = ustte
                    eskiUstte = 1
                    coind[xd]['eskiUstte'] = eskiUstte

                print(xd, ustte, eskiUstte, kesisti)

                if (kesisti == 1 and aradakiFark > 2.2) and ((red > 83 or red == 83) and (blue > 83 or blue == 83) or (red < 17 or red == 17) and (blue < 17 or blue == 17)):
                    kesisti = 0
                    coind[xd]['kesisti'] = kesisti
                    if (red < 17 or red == 17) and (blue < 17 or blue == 17):
                            print("KESİŞME OLMUŞ")
                            coinDeger = float(close)
                            coinAlimEmriDeger = float(coinDeger + ((coinDeger / float(100)) * float(0.185)))
                            coinAlimEmriDeger = float(coinAlimEmriDeger)
                            coinAlimEmriDeger = float(str(coinAlimEmriDeger).split('.')[0] + "." + str(coinAlimEmriDeger).split('.')[1][0:kusur])
                            if bildirimGonderildi == 0:
                                if aradakiFark > 2:
                                    bildirimGonderildi = 2
                                    coind[xd]['bildirimGonderildi'] = bildirimGonderildi
                                    print(f"trying to send notification for buy {TRADE_SYMBOL} from {coinAlimEmriDeger} USDT")
                                    sent = sendTelegram(channelId, f"------ALIŞ EMRI------\nCoin Sembol: {TRADE_SYMBOL}\nMum Kapanışı: {coinDeger}\nEmir Koyulacak Fiyat: {coinAlimEmriDeger}")
                                    if sent['ok'] == True:
                                        print(f"------BUY ORDER------\nCoin Sembol: {TRADE_SYMBOL}\nCandle Close: {coinDeger}\nOrder Price: {coinAlimEmriDeger}")
                                    else:
                                        print("Error while sending message to channel\n", sent['description'])
                                else:
                                    print("Aradaki fark 2 den büyük değil, işlem kesin değil. İşlem açmadım.")
                            elif bildirimGonderildi == 1:
                                if aradakiFark > 2:
                                    bildirimGonderildi = 2
                                    coind[xd]['bildirimGonderildi'] = bildirimGonderildi
                                    print(f"trying to send notification for buy {TRADE_SYMBOL} from {coinAlimEmriDeger} USDT")
                                    sent = sendTelegram(channelId, f"------ALIŞ EMRI------\nCoin Sembol: {TRADE_SYMBOL}\nMum Kapanışı: {coinDeger}\nEmir Koyulacak Fiyat: {coinAlimEmriDeger}")
                                    if sent['ok'] == True:
                                        print(f"------BUY ORDER------\nCoin Sembol: {TRADE_SYMBOL}\nCandle Close: {coinDeger}\nOrder Price: {coinAlimEmriDeger}")
                                    else:
                                        print("Error while sending message to channel\n", sent['description'])
                                else:
                                    print("Aradaki fark 2 den büyük değil, işlem kesin değil. İşlem açmadım.")
                    elif (red > 83 or red == 83) and (blue > 83 or blue == 83):
                            print("KESİŞME OLMUŞ")
                            coinDeger = float(close)
                            coinAlimEmriDeger = float(coinDeger - ((coinDeger / float(100)) * float(0.185)))
                            coinAlimEmriDeger = float(coinAlimEmriDeger)
                            coinAlimEmriDeger = float(str(coinAlimEmriDeger).split('.')[0] + "." + str(coinAlimEmriDeger).split('.')[1][0:kusur])
                            if bildirimGonderildi == 0:
                                if aradakiFark > 2:
                                    bildirimGonderildi = 1
                                    coind[xd]['bildirimGonderildi'] = bildirimGonderildi
                                    print(f"trying to send notification for sell {TRADE_SYMBOL} from {coinAlimEmriDeger} USDT")
                                    sent = sendTelegram(channelId, f"------SATIŞ EMRI------\nCoin Sembol: {TRADE_SYMBOL}\nMum Kapanışı: {coinDeger}\nEmir Koyulacak Fiyat: {coinAlimEmriDeger}")
                                    if sent['ok'] == True:
                                        print(f"------SELL ORDER------\nCoin Symbol: {TRADE_SYMBOL}\nCandle Close: {coinDeger}\nOrder Price: {coinAlimEmriDeger}")
                                    else:
                                        print("Error while sending message to channel\n", sent['description'])
                                else:
                                    print("Aradaki fark 2 den büyük değil, işlem kesin değil. İşlem açmadım.")
                            elif bildirimGonderildi == 2:
                                if aradakiFark > 2:
                                    bildirimGonderildi = 1
                                    coind[xd]['bildirimGonderildi'] = bildirimGonderildi
                                    print(f"trying to send notification for sell {TRADE_SYMBOL} from {coinAlimEmriDeger} USDT")
                                    sent = sendTelegram(channelId, f"------SATIŞ EMRI------\nCoin Sembol: {TRADE_SYMBOL}\nMum Kapanışı: {coinDeger}\nEmir Koyulacak Fiyat: {coinAlimEmriDeger}")
                                    if sent['ok'] == True:
                                        print(f"------SELL ORDER------\nCoin Symbol: {TRADE_SYMBOL}\nCandle Close: {coinDeger}\nOrder Price: {coinAlimEmriDeger}")
                                    else:
                                        print("Error while sending message to channel\n", sent['description'])
                                else:
                                    print("Aradaki fark 2 den büyük değil, işlem kesin değil. İşlem açmadım.")
                    return True
                if bildirimGonderildi > 0:
                    if (red < 80 and blue < 80) and (red > 20 and blue > 20):
                        bildirimGonderildi = 0
                        coind[xd]['bildirimGonderildi'] = bildirimGonderildi
                if (red > 88 or red == 88) and (blue > 88 or blue == 88):
                    print("İkisi de 90 Üstünde")
                    coinDeger = float(close)
                    coinAlimEmriDeger = float(coinDeger - ((coinDeger / float(100)) * float(0.185)))
                    coinAlimEmriDeger = float(coinAlimEmriDeger)
                    coinAlimEmriDeger = float(str(coinAlimEmriDeger).split('.')[0] + "." + str(coinAlimEmriDeger).split('.')[1][0:kusur])
                    if eskiUstte != 0:
                        if (ustte == 1 and eskiUstte == 2) or (ustte == 2 and eskiUstte == 1):
                            print("KESİŞME OLMUŞ")
                            if bildirimGonderildi == 0:
                                if aradakiFark > 2:
                                    bildirimGonderildi = 1
                                    coind[xd]['bildirimGonderildi'] = bildirimGonderildi
                                    kesisti = 1
                                    coind[xd]['kesisti'] = kesisti
                                    print(f"trying to send notification for sell {TRADE_SYMBOL} from {coinAlimEmriDeger} USDT")
                                    sent = sendTelegram(channelId, f"------SATIŞ EMRI------\nCoin Sembol: {TRADE_SYMBOL}\nMum Kapanışı: {coinDeger}\nEmir Koyulacak Fiyat: {coinAlimEmriDeger}")
                                    if sent['ok'] == True:
                                        print(f"------SELL ORDER------\nCoin Symbol: {TRADE_SYMBOL}\nCandle Close: {coinDeger}\nOrder Price: {coinAlimEmriDeger}")
                                        kesisti = 0
                                        coind[xd]['kesisti'] = kesisti
                                    else:
                                        print("Error while sending message to channel\n", sent['description'])
                                else:
                                    print("Aradaki fark 2 den büyük değil, işlem kesin değil. İşlem açmadım.")
                            elif bildirimGonderildi == 2:
                                if aradakiFark > 2:
                                    bildirimGonderildi = 1
                                    coind[xd]['bildirimGonderildi'] = bildirimGonderildi
                                    kesisti = 1
                                    coind[xd]['kesisti'] = kesisti
                                    print(f"trying to send notification for sell {TRADE_SYMBOL} from {coinAlimEmriDeger} USDT")
                                    sent = sendTelegram(channelId, f"------SATIŞ EMRI------\nCoin Sembol: {TRADE_SYMBOL}\nMum Kapanışı: {coinDeger}\nEmir Koyulacak Fiyat: {coinAlimEmriDeger}")
                                    if sent['ok'] == True:
                                        print(f"------SELL ORDER------\nCoin Symbol: {TRADE_SYMBOL}\nCandle Close: {coinDeger}\nOrder Price: {coinAlimEmriDeger}")
                                        kesisti = 0
                                        coind[xd]['kesisti'] = kesisti
                                    else:
                                        print("Error while sending message to channel\n", sent['description'])
                                else:
                                    print("Aradaki fark 2 den büyük değil, işlem kesin değil. İşlem açmadım.")
                        else:
                            print("Kesişme yok.")
                            kesisme = 0
                            coind[xd]['kesisti'] = kesisti
                elif (red < 12 or red == 12) and (blue < 12 or blue == 12):
                    print("İkisi de 10 Altında")
                    coinDeger = float(close)
                    coinAlimEmriDeger = float(coinDeger + ((coinDeger / float(100)) * float(0.185)))
                    coinAlimEmriDeger = float(coinAlimEmriDeger)
                    coinAlimEmriDeger = float(str(coinAlimEmriDeger).split('.')[0] + "." + str(coinAlimEmriDeger).split('.')[1][0:kusur])
                    if eskiUstte != 0:
                        if (ustte == 1 and eskiUstte == 2) or (ustte == 2 and eskiUstte == 1):
                            print("KESİŞME OLMUŞ")
                            if bildirimGonderildi == 0:
                                if aradakiFark > 2:
                                    bildirimGonderildi = 2
                                    coind[xd]['bildirimGonderildi'] = bildirimGonderildi
                                    kesisti = 1
                                    coind[xd]['kesisti'] = kesisti
                                    sent = sendTelegram(channelId, f"------ALIŞ EMRI------\nCoin Sembol: {TRADE_SYMBOL}\nMum Kapanışı: {coinDeger}\nEmir Koyulması Gereken Fiyat: {coinAlimEmriDeger}")
                                    if sent['ok'] == True:
                                        print(f"------BUY ORDER------\nCoin Sembol: {TRADE_SYMBOL}\nCandle Close: {coinDeger}")
                                        kesisti = 0
                                        coind[xd]['kesisti'] = kesisti
                                    else:
                                        print("Error while sending message to channel\n", sent['description'])
                                else:
                                    print("Aradaki fark 2 den büyük değil, işlem kesin değil. İşlem açmadım.")
                            elif bildirimGonderildi == 1:
                                if aradakiFark > 2:
                                    bildirimGonderildi = 2
                                    coind[xd]['bildirimGonderildi'] = bildirimGonderildi
                                    kesisti = 1
                                    coind[xd]['kesisti'] = kesisti
                                    print(f"trying to send notification for buy {TRADE_SYMBOL} from {coinAlimEmriDeger} USDT")
                                    sent = sendTelegram(channelId, f"------ALIŞ EMRI------\nCoin Sembol: {TRADE_SYMBOL}\nMum Kapanışı: {coinDeger}\nEmir Koyulacak Fiyat: {coinAlimEmriDeger}")
                                    if sent['ok'] == True:
                                        print(f"------BUY ORDER------\nCoin Symbol: {TRADE_SYMBOL}\nCandle Close: {coinDeger}\nOrder Price: {coinAlimEmriDeger}")
                                        kesisti = 0
                                        coind[xd]['kesisti'] = kesisti
                                    else:
                                        print("Error while sending message to channel\n", sent['description'])
                                    kesisme = 1
                                    coind[xd]['kesisti'] = kesisti
                                else:
                                    print("Aradaki fark 2 den büyük değil, işlem kesin değil. İşlem açmadım.")
                        else:
                            print("Kesişme yok.")
                            kesisme = 0
                            coind[xd]['kesisti'] = kesisti
            
                jsonFile = open("coins.json", "w+")
                jsonFile.write(json.dumps(coind, indent = 4, sort_keys=True))
                jsonFile.close()

        

wss = websocket.WebSocketApp(SOCKETS, on_open=on_open, on_close=on_close, on_message=check)
wss.run_forever()