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
import sys, re, optparse
from threading import Thread
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

stop = {}
scheduler = BackgroundScheduler()

def orderCheck(threadId, args):
    global stop
    print("Thread started.")
    print(args)
    scheduler.remove_job(f"{threadId}", jobstore=None)

def orderCancel(threadId, args):
    jsonFile = open("coinsTest.json", "r+")
    coins = json.load(jsonFile)
def createThread(type, args):
    threadId = round(time.time() * 1000)
    if type == 'cancel':
        scheduler.add_job(func=orderCancel, args=[threadId, args], trigger=None, id=f"{threadId}")
    elif type == 'check':
        scheduler.add_job(func=orderCheck, args=[threadId, args], trigger="interval", id=f"{threadId}", seconds=1)
    scheduler.start()