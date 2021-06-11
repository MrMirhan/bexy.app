if (kesisti == 1 and aradakiFark > 2.2) and ((red > 83 or red == 83) and (blue > 83 or blue == 83) or (red < 17 or red == 17) and (blue < 17 or blue == 17)):
                kesisti = 0
                coind[xd]['stochRSI']['kesisti'] = kesisti
                if (red < 17 or red == 17) and (blue < 17 or blue == 17):
                    sendLog("KESİŞME OLMUŞ")
                    coinDeger = float(close)
                    coinAlimEmriDeger = float(
                        coinDeger + ((coinDeger / float(100)) * float(0.185)))
                    coinAlimEmriDeger = float(coinAlimEmriDeger)
                    coinAlimEmriDeger = float(str(coinAlimEmriDeger).split(
                        '.')[0] + "." + str(coinAlimEmriDeger).split('.')[1][0:kusur])
                    if bildirimGonderildi == 0:
                        if aradakiFark > 2:
                            bildirimGonderildi = 2
                            coind[xd]['bildirimGonderildi'] = bildirimGonderildi
                            sendLog(
                                f"trying to send notification for buy {TRADE_SYMBOL} from {coinAlimEmriDeger} USDT")
                            sent = sendTelegram(
                                channelId, f"------ALIŞ EMRI------\nCoin Sembol: {TRADE_SYMBOL}\nMum Kapanışı: {coinDeger}\nEmir Koyulacak Fiyat: {coinAlimEmriDeger}")
                            if sent['ok'] == True:
                                sendLog(
                                    f"------BUY ORDER------\nCoin Sembol: {TRADE_SYMBOL}\nCandle Close: {coinDeger}\nOrder Price: {coinAlimEmriDeger}")
                                orderAc(str(xd), coinAlimEmriDeger,
                                        kusur, "al")
                            else:
                                sendLog("Error while sending message to channel\n{}".format(
                                    sent['description']))
                        else:
                            sendLog(
                                "Aradaki fark 2 den büyük değil, işlem kesin değil. İşlem açmadım.")
                    elif bildirimGonderildi == 1:
                        if aradakiFark > 2:
                            bildirimGonderildi = 2
                            coind[xd]['bildirimGonderildi'] = bildirimGonderildi
                            sendLog(
                                f"trying to send notification for buy {TRADE_SYMBOL} from {coinAlimEmriDeger} USDT")
                            sent = sendTelegram(
                                channelId, f"------ALIŞ EMRI------\nCoin Sembol: {TRADE_SYMBOL}\nMum Kapanışı: {coinDeger}\nEmir Koyulacak Fiyat: {coinAlimEmriDeger}")
                            if sent['ok'] == True:
                                sendLog(
                                    f"------BUY ORDER------\nCoin Sembol: {TRADE_SYMBOL}\nCandle Close: {coinDeger}\nOrder Price: {coinAlimEmriDeger}")
                                orderAc(str(xd), coinAlimEmriDeger,
                                        kusur, "al")
                            else:
                                sendLog("Error while sending message to channel\n{}".format(
                                    sent['description']))
                        else:
                            sendLog(
                                "Aradaki fark 2 den büyük değil, işlem kesin değil. İşlem açmadım.")
                elif (red > 83 or red == 83) and (blue > 83 or blue == 83):
                    sendLog("KESİŞME OLMUŞ")
                    coinDeger = float(close)
                    coinAlimEmriDeger = float(
                        coinDeger - ((coinDeger / float(100)) * float(0.185)))
                    coinAlimEmriDeger = float(coinAlimEmriDeger)
                    coinAlimEmriDeger = float(str(coinAlimEmriDeger).split(
                        '.')[0] + "." + str(coinAlimEmriDeger).split('.')[1][0:kusur])
                    if bildirimGonderildi == 0:
                        if aradakiFark > 2:
                            bildirimGonderildi = 1
                            coind[xd]['bildirimGonderildi'] = bildirimGonderildi
                            sendLog(
                                f"trying to send notification for sell {TRADE_SYMBOL} from {coinAlimEmriDeger} USDT")
                            sent = sendTelegram(
                                channelId, f"------SATIŞ EMRI------\nCoin Sembol: {TRADE_SYMBOL}\nMum Kapanışı: {coinDeger}\nEmir Koyulacak Fiyat: {coinAlimEmriDeger}")
                            if sent['ok'] == True:
                                sendLog(
                                    f"------SELL ORDER------\nCoin Symbol: {TRADE_SYMBOL}\nCandle Close: {coinDeger}\nOrder Price: {coinAlimEmriDeger}")
                                orderAc(str(xd), coinAlimEmriDeger,
                                        kusur, "sat")
                            else:
                                sendLog("Error while sending message to channel\n{}".format(
                                    sent['description']))
                        else:
                            sendLog(
                                "Aradaki fark 2 den büyük değil, işlem kesin değil. İşlem açmadım.")
                    elif bildirimGonderildi == 2:
                        if aradakiFark > 2:
                            bildirimGonderildi = 1
                            coind[xd]['bildirimGonderildi'] = bildirimGonderildi
                            sendLog(
                                f"trying to send notification for sell {TRADE_SYMBOL} from {coinAlimEmriDeger} USDT")
                            sent = sendTelegram(
                                channelId, f"------SATIŞ EMRI------\nCoin Sembol: {TRADE_SYMBOL}\nMum Kapanışı: {coinDeger}\nEmir Koyulacak Fiyat: {coinAlimEmriDeger}")
                            if sent['ok'] == True:
                                sendLog(
                                    f"------SELL ORDER------\nCoin Symbol: {TRADE_SYMBOL}\nCandle Close: {coinDeger}\nOrder Price: {coinAlimEmriDeger}")
                                orderAc(str(xd), coinAlimEmriDeger,
                                        kusur, "sat")
                            else:
                                sendLog("Error while sending message to channel\n{}".format(
                                    sent['description']))
                        else:
                            sendLog(
                                "Aradaki fark 2 den büyük değil, işlem kesin değil. İşlem açmadım.")
                return True