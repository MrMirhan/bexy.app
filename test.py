from socket import SIO_LOOPBACK_FAST_PATH
from sys import int_info
import websocket
import threading
import time
import random
from telethon.sync import TelegramClient, events
import continuous_threading
from continuous_threading import CommandProcess
import traceback
import telepot
from telepot.loop import MessageLoop
from telepot.delegate import per_chat_id, create_open, pave_event_space, per_inline_from_id
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent
import json
import orderHandler as oh

TOKEN = "1776589751:AAH3HQRXe7tEJf5C-HnfBVeOBWta72Gbd_E"

SOCKETS = f"wss://stream.binance.com:9443/ws/adausdt@kline_5m"

message_with_inline_keyboard = None

coins = ["ada", "dent", "storj", "btt", "vet", "doge", "hot", "sxp", "xlm", "algo", "mtl", "trx", "reef", "one", "xrp"]

def on_chat_message(msg):
    global coins, message_with_inline_keyboard
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(msg)
    if content_type == 'text':
        message = str(msg['text'])
        if message.startswith("/"):
            args = message.split(" ")
            command = args[0].replace("/", "").lower();
            del args[0]
            if command == "hi":
                bot.sendMessage(chat_id, "xd")
                print(args)
            elif command == "coin":
                print(len(args))
                if len(args) > 0:
                    if args[0] == "bak":
                        if len(args) > 1:
                            jsonFile = open('coins.json', "r+")
                            coin = json.load(jsonFile)
                            coin = coin[args[1]]
                            bot.sendMessagechat_id, (str(coin))
                        else:
                            bot.sendMessage(chat_id, 'Bir coin adı belirtin.')
                    else:
                        bot.sendMessage(chat_id, 'Kullanılabilir argümanlar: "bak"')
                else:
                    bot.sendMessage(chat_id, 'Kullanılabilir argümanlar: "bak"')
            elif command == 'c':
                markup = ReplyKeyboardMarkup(keyboard=[
                            ["Plain Text", KeyboardButton(text='Text only')],
                            [dict(text='Phone', request_contact=True), KeyboardButton(text='Location', request_location=True)],
                        ])
                bot.sendMessage(chat_id, 'Custom keyboard with various buttons', reply_markup=markup)
            elif command == 'i':
                markup = InlineKeyboardMarkup(inline_keyboard=[
                            [dict(text='Telegram URL', url='https://core.telegram.org/')],
                            [InlineKeyboardButton(text='Callback - show notification', callback_data='notification')],
                            [dict(text='Callback - show alert', callback_data='alert')],
                            [InlineKeyboardButton(text='Callback - edit message', callback_data='edit')],
                            [dict(text='Switch to using bot inline', switch_inline_query='initial query')],
                        ])
                message_with_inline_keyboard = bot.sendMessage(chat_id, 'Inline keyboard with various buttons', reply_markup=markup)
            elif command == 'h':
                markup = ReplyKeyboardRemove()
                bot.sendMessage(chat_id, 'Hide custom keyboard', reply_markup=markup)
            elif command == 'f':
                markup = ForceReply()
                bot.sendMessage(chat_id, 'Force reply', reply_markup=markup)
            elif command == "kapat":
                xd = []
                for x in coins:
                    x = x.upper()
                    xd.append([InlineKeyboardButton(text=f'{x} Kapatılsın', callback_data=f'kapat {x}')])
                markup = InlineKeyboardMarkup(inline_keyboard=xd)
                message_with_inline_keyboard = bot.sendMessage(chat_id, 'Hangi Coinin Açık İşlemleri Kapatılsın?', reply_markup=markup)
            elif command == "start":
                if msg['chat']['type'] != "private":
                    return
                jsonFile = open("users.json", "r+")
                users = json.load(jsonFile)
                user = [x for x in users if x['telegramId'] == chat_id]
                if user:
                    bot.sendMessage(chat_id, 'Kullanıcı kaydınız zaten bulunmakta.')
                else:
                    markup = ReplyKeyboardMarkup(keyboard=[
                            [dict(text='İletişim Bilgilerini Paylaş', request_contact=True)]
                        ])
                    bot.sendMessage(chat_id, 'Kayıt işlemleri başlıyor..')
                    time.sleep(1.2)
                    bot.sendMessage(chat_id, 'Lütfen iletişim bilgilerini paylaşır mısın?', reply_markup=markup)
    elif content_type == "contact":
        jsonFile = open("users.json", "r+")
        users = json.load(jsonFile)
        bot.sendMessage(chat_id, "Başarılı")


def on_callback_query(msg):
    query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
    print('Callback query:', query_id, from_id, data)
    global message_with_inline_keyboard
    if data == 'notification':
        bot.answerCallbackQuery(query_id, text='Notification at top of screen')
    elif data == 'alert':
        bot.answerCallbackQuery(query_id, text='Alert!', show_alert=True)
    elif data == 'edit':

        if message_with_inline_keyboard:
            msg_idf = telepot.message_identifier(message_with_inline_keyboard)
            bot.editMessageText(msg_idf, 'NEW MESSAGE HERE!!!!!')
        else:
            bot.answerCallbackQuery(query_id, text='No previous message to edit')
    elif data.startswith("kapat"):
        coin = data.split(" ")[1]
        msg_idf = telepot.message_identifier(message_with_inline_keyboard)
        bot.answerCallbackQuery(query_id, text=f'{coin} kapatılıyor.')
        bot.sendMessage(from_id, f'{coin} kapatılıyor.')
        bot.deleteMessage(msg_idf)
        oh.createThread("cancel", {'test': 'sjsjsj'})


def on_inline_query(msg):
    def compute():
        query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
        print('%s: Computing for: %s' % (threading.current_thread().name, query_string))

        articles = [InlineQueryResultArticle(
                        id='abcde', title='Telegram', input_message_content=InputTextMessageContent(message_text='Telegram is a messaging app')),
                    dict(type='article',
                        id='fghij', title='Google', input_message_content=dict(message_text='Google is a search engine'))]

        photo1_url = 'https://core.telegram.org/file/811140934/1/tbDSLHSaijc/fdcc7b6d5fb3354adf'
        photo2_url = 'https://www.telegram.org/img/t_logo.png'
        photos = [InlineQueryResultPhoto(
                      id='12345', photo_url=photo1_url, thumb_url=photo1_url),
                  dict(type='photo',
                      id='67890', photo_url=photo2_url, thumb_url=photo2_url)]

        result_type = query_string[-1:].lower()

        if result_type == 'a':
            return articles
        elif result_type == 'p':
            return photos
        else:
            results = articles if random.randint(0,1) else photos
            if result_type == 'b':
                return dict(results=results, switch_pm_text='Back to Bot', switch_pm_parameter='Optional_start_parameter')
            else:
                return dict(results=results)

    answerer.answer(msg, compute)


def on_chosen_inline_result(msg):
    result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
    print('Chosen Inline Result:', result_id, from_id, query_string)


bot = telepot.Bot(TOKEN)
answerer = telepot.helper.Answerer(bot)
def on_open(ws):
    print('Socket connection started.')
    MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query,
                  'inline_query': on_inline_query,
                  'chosen_inline_result': on_chosen_inline_result}).run_as_thread()
    print('Listening ...')
    oh.createThread(10001)

def on_close(ws):
    print('Socket connection ended.')

def check(ws, message):
    print("xd")

wss = websocket.WebSocketApp(SOCKETS, on_open=on_open, on_close=on_close, on_message=check)
wss.run_forever()

while True:
    pass