import json, numpy, requests
import talib as ta
import config
from loggerM import sendLog

client = config.client

class Controller():
    def __init__(self, symbol):
        jsonFile = open("coins.json", "r")
        coind = json.load(jsonFile)
        jsonFile.close()
        self.symbol = str(symbol).lower()
        self.coind = coind
        self.kusur = int(self.coind[self.symbol]['pres'])
        self.bildirimGonderildi = self.coind[self.symbol]['bildirimGonderildi']

        self.TRADE_SYMBOL = self.symbol.upper() + "USDT"

        klines = client.get_klines(symbol=self.TRADE_SYMBOL, interval='5m', limit=500)

        close = [float(entry[4]) for entry in klines]
        high = [float(entry[2]) for entry in klines]
        low = [float(entry[3]) for entry in klines]

        self.close_array = numpy.asarray(close)
        self.high_array = numpy.asarray(high)
        self.low_array = numpy.asarray(low)

        self.close_finished = str(float(requests.get("https://api.binance.com/api/v3/avgPrice?symbol={}".format(self.TRADE_SYMBOL)).json()['price']))
        self.close_finished = float(str(self.close_finished).split('.')[0] + "." + str(self.close_finished).split('.')[1][0:self.kusur])

    def coinBuyPriceCheck(self, side):
        side = str(side)
        self.coinDeger = float(self.close_finished)
        value = float((float(self.coinDeger) / float(100)) * float(0.185))
        if side == "sat":
            self.coinAlimEmriDeger = float(float(self.coinDeger) - (value))
        elif side == "al":
            self.coinAlimEmriDeger = float(float(self.coinDeger) + (value))
        self.coinAlimEmriDeger = float(self.coinAlimEmriDeger)
        self.coinAlimEmriDeger = float(str(self.coinAlimEmriDeger).split('.')[0] + "." + str(self.coinAlimEmriDeger).split('.')[1][0:self.kusur])
        return str(self.coinAlimEmriDeger)

    def tillsonCheck(self):
        volume_factor = 0.7
        t3Length = 8
        high_array = self.high_array
        low_array = self.low_array
        close_array = self.close_array

        ema_first_input = (high_array + low_array + 2 * close_array) / 4

        e1 = ta.EMA(ema_first_input, t3Length)

        e2 = ta.EMA(e1, t3Length)

        e3 = ta.EMA(e2, t3Length)

        e4 = ta.EMA(e3, t3Length)

        e5 = ta.EMA(e4, t3Length)

        e6 = ta.EMA(e5, t3Length)

        c1 = -1 * volume_factor * volume_factor * volume_factor

        c2 = 3 * volume_factor * volume_factor + 3 * \
            volume_factor * volume_factor * volume_factor

        c3 = -6 * volume_factor * volume_factor - 3 * volume_factor - \
            3 * volume_factor * volume_factor * volume_factor

        c4 = 1 + 3 * volume_factor + volume_factor * volume_factor * \
            volume_factor + 3 * volume_factor * volume_factor

        T3 = c1 * e6 + c2 * e5 + c3 * e4 + c4 * e3
        return T3

    def tillsonSignal(self, tillson):
        t3_last = tillson[-1]
        t3_previous = tillson[-2]

        self.t3side = "a"

        # kırmızıdan yeşile dönüyor
        if t3_last > t3_previous:
            self.coind[self.symbol]['t3']['sinyal'] = "al"
            self.coind[self.symbol]['t3']['eskiSinyal'] = "sat"
            self.t3side = "al"

        # yeşilden kırmızıya dönüyor
        elif t3_last < t3_previous:
            self.coind[self.symbol]['t3']['sinyal'] = "sat"
            self.coind[self.symbol]['t3']['eskiSinyal'] = "al"
            self.t3side = "sat"
        else:
            self.t3side = False

        jsonFile = open("coins.json", "w+")
        jsonFile.write(json.dumps(self.coind, indent=4, sort_keys=True))
        jsonFile.close()
        return self.t3side

    def stochCheck(self):
        timeperiod = 14
        rsi = ta.RSI(self.close_array, timeperiod)
        rsi = rsi[~numpy.isnan(rsi)]
        stochrsif, stochrsis = ta.STOCH(rsi, rsi, rsi, fastk_period=14, slowk_period=3, slowd_period=3)
        return stochrsif, stochrsis

    def blueRedCheck(self, redi, bluei):
        self.bluei = bluei[~numpy.isnan(bluei)]
        self.redi = redi[~numpy.isnan(redi)]
        self.bluei = bluei[-1]
        self.redi = redi[-1]
        self.red = float(round(self.bluei, 2))
        self.blue = float(round(self.redi, 2))
        self.aradakiFark = float(abs(self.red - self.blue))
        self.stside = "a"
        if self.red > self.blue:
            self.ustte = 1
            self.coind[self.symbol]['stochRSI']['ustte'] = self.ustte
            self.eskiUstte = 2
            self.coind[self.symbol]['stochRSI']['eskiUstte'] = self.eskiUstte
            self.stside = "sat"
        else:
            self.ustte = 2
            self.coind[self.symbol]['stochRSI']['ustte'] = self.ustte
            self.eskiUstte = 1
            self.coind[self.symbol]['stochRSI']['eskiUstte'] = self.eskiUstte
            self.stside = "al"

        sendLog(str(self.symbol) + " " + str(self.ustte) + " " + str(self.eskiUstte))
        jsonFile = open("coins.json", "w+")
        jsonFile.write(json.dumps(self.coind, indent=4, sort_keys=True))
        jsonFile.close()
        return self.stside

    def stochRSIControl(self):
        self.srside = "a"
        if (self.red > 88.6 or self.red == 88.6) and (self.blue > 88.6 or self.blue == 88.6):
            sendLog("İkisi de 90 Üstünde")
            if self.eskiUstte != 0:
                if (self.ustte == 1 and self.eskiUstte == 2) or (self.ustte == 2 and self.eskiUstte == 1):
                    sendLog("KESİŞME OLMUŞ")
                    if self.aradakiFark > 2:
                        self.stochkesisti = 1
                        self.coind[self.symbol]['stochRSI']['kesisti'] = self.stochkesisti
                        self.srside = "sat"
                    else:
                        self.srside = False
                        sendLog("Aradaki fark 2 den büyük değil, işlem kesin değil. İşlem açmadım.")
                else:
                    self.srside = False
            else:
                self.srside = False
        elif (self.red < 11.4 or self.red == 11.4) and (self.blue < 11.4 or self.blue == 11.4):
            sendLog("İkisi de 10 Altında")
            if self.eskiUstte != 0:
                if (self.ustte == 1 and self.eskiUstte == 2) or (self.ustte == 2 and self.eskiUstte == 1):
                    sendLog("KESİŞME OLMUŞ")
                    if self.aradakiFark > 2:
                        self.stochkesisti = 1
                        self.coind[self.symbol]['stochRSI']['kesisti'] = self.stochkesisti
                        self.srside = "al"
                    else:
                        self.srside = False
                        sendLog("Aradaki fark 2 den büyük değil, işlem kesin değil. İşlem açmadım.")
                else:
                    self.srside = False
            else:
                self.srside = False
        else:
            self.srside = False
        jsonFile = open("coins.json", "w+")
        jsonFile.write(json.dumps(self.coind, indent=4, sort_keys=True))
        jsonFile.close()
        return self.srside

    def macdCheck(self):
        macd, macdsignal, macdhist = ta.MACD(self.close_array, fastperiod=12, slowperiod=26, signalperiod=9)
        rsi = ta.RSI(self.close_array
        , timeperiod=14)

        if len(macd) > 0:
            last_macd = macd[-1]
            last_macd_signal = macdsignal[-1]
            rsi_last = rsi[-1]

            macd_cross_up = last_macd > last_macd_signal
            macd_cross_down = last_macd < last_macd_signal

            if macd_cross_up and rsi_last > 50:
                self.macdside = "al"
                self.coind[self.symbol]['macd']['sinyal'] = self.macdside
                self.coind[self.symbol]['macd']['eskiSinyal'] = "sat"
            elif macd_cross_down and rsi_last < 50:
                self.macdside = "sat"
                self.coind[self.symbol]['macd']['sinyal'] = self.macdside
                self.coind[self.symbol]['macd']['eskiSinyal'] = "al"
            else:
                self.macdside = False
            jsonFile = open("coins.json", "w+")
            jsonFile.write(json.dumps(self.coind, indent=4, sort_keys=True))
            jsonFile.close()
            return self.macdside

    def controlNotify(self):
        if self.bildirimGonderildi > 0:
            if ((self.coind[self.symbol]['t3']['sinyal'] == 1 and self.coind[self.symbol]['t3']['eskiSinyal'] == 2) or (self.coind[self.symbol]['t3']['sinyal'] == 2 and self.coind[self.symbol]['t3']['eskiSinyal'] == 1)):
                self.bildirimGonderildi = 0
                self.coind[self.symbol]['bildirimGonderildi'] = self.bildirimGonderildi
                jsonFile = open("coins.json", "w+")
                jsonFile.write(json.dumps(self.coind, indent=4, sort_keys=True))
                jsonFile.close()
            elif self.coind[self.symbol]['stochRSI']['kesisti'] == 1:
                if (self.red < 77 and self.blue < 77) and (self.red > 23 and self.blue > 23):
                    self.bildirimGonderildi = 0
                    self.coind[self.symbol]['bildirimGonderildi'] = self.bildirimGonderildi
                    jsonFile = open("coins.json", "w+")
                    jsonFile.write(json.dumps(self.coind, indent=4, sort_keys=True))
                    jsonFile.close()

    def end(self):
        message = f"\n------COIN DETAILS------\nsymbol: {self.TRADE_SYMBOL}\nperiod: 5m\nclose: {self.close_finished}\n\n------STOCHASTIC RSI------\nblue: {self.blue}\nred: {self.red}\ndifference: {self.aradakiFark}\n\n-----CONTROL-----\nT3 Signal Check: {str(self.t3side)}\nRed and Blue Side Check: {str(self.stside)}\nStoch RSI Control: {str(self.srside)}\nMACD Side Control: {str(self.macdside)}\nCoin Price Check: {str(self.coinAlimEmriDeger)}\nNotify Check: {str(self.bildirimGonderildi)}\n"
        sendLog(message)
