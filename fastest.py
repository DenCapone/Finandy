import os
import telebot
import time
# import unicorn_binance_websocket_api

from binance.exceptions import BinanceAPIException
from views import plus_percent, minus_percent
from const import MONEY, TP, TP2, TP3, SL, QUAN
from dotenv import load_dotenv
from binance.client import Client

# подгружаем ключи
load_dotenv()
# anemiaabot
# secret_token = os.getenv('TOKEN2')
# oldrat
secret_token = os.getenv('TOKEN')
api_key = os.getenv('KEY2')
api_secret = os.getenv('SECRET2')
# создаём клиента на бирже
client = Client(api_key, api_secret)
# вызываем своего бота
bot = telebot.TeleBot(secret_token)


@bot.message_handler(content_types=['text', 'photo'])
def get_mess(message):
    try:
        caption = message.text.replace('#', '', 1).split()
    except AttributeError:
        print('NoneType')
        return
    try:
        coin = caption[0] + 'USDT'
    except AttributeError:
        print('NightMode')
        return
    try:
        if caption[1].lower() == 'buy':
            try:
                # пытаемся купить монеты
                buy_futures = client.futures_create_order(symbol=coin, side='BUY', type='market', quantity=QUAN)
            except BinanceAPIException as e:
                print(e)
            quan1 = round(QUAN * 0.5)
            quan2 = round(QUAN * 0.25)
            quan3 = QUAN - quan1 - quan2
            try:
                # получаем таблицу с текущей стоимостью монеты
                price_now = float(client.futures_symbol_ticker(symbol=coin, requests_params={'timeout': 1})['price'])
            except:
                print('не смог получить текущий курс, пробую ещё раз')
                time.sleep(1)
                price_now = float(client.futures_symbol_ticker(symbol=coin, requests_params={'timeout': 1})['price'])
            take1 = plus_percent(price_now, TP)
            stop = minus_percent(price_now, SL)
            try:
                sl_order = client.futures_create_order(symbol=coin,
                                                       side='SELL',
                                                       type='STOP_MARKET',
                                                       quantity=QUAN,
                                                       stopPrice=stop,
                                                       closePosition='true',
                                                       )
                tp_order = client.futures_create_order(symbol=coin,
                                                       side='SELL',
                                                       type='LIMIT',
                                                       quantity=quan1,
                                                       price=take1,
                                                       timeInForce='GTC'
                                                       )
                take2 = plus_percent(price_now, TP2)
                tp_order2 = client.futures_create_order(symbol=coin,
                                                        side='SELL',
                                                        type='LIMIT',
                                                        quantity=quan2,
                                                        price=take2,
                                                        timeInForce='GTC'
                                                        )
                take3 = plus_percent(price_now, TP3)
                tp_order3 = client.futures_create_order(symbol=coin,
                                                        side='SELL',
                                                        type='LIMIT',
                                                        quantity=quan3,
                                                        price=take3,
                                                        timeInForce='GTC'
                                                        )
            except BinanceAPIException as e:
                print(e)
        elif caption[1].lower() == 'short':
            try:
                # пытаемся купить монеты
                buy_futures = client.futures_create_order(symbol=coin, side='SELL', type='market', quantity=QUAN)
            except BinanceAPIException as e:
                print(e)
            quan1 = round(QUAN * 0.5)
            quan2 = round(QUAN * 0.25)
            quan3 = QUAN - quan1 - quan2
            try:
                # получаем таблицу с текущей стоимостью монеты
                price_now = float(client.futures_symbol_ticker(symbol=coin, requests_params={'timeout': 1})['price'])
            except:
                print('не смог получить текущий курс, пробую ещё раз')
                time.sleep(1)
                price_now = float(client.futures_symbol_ticker(symbol=coin, requests_params={'timeout': 1})['price'])
            take1 = minus_percent(price_now, TP)
            stop = plus_percent(price_now, SL)
            try:
                sl_order = client.futures_create_order(symbol=coin,
                                                       side='BUY',
                                                       type='STOP_MARKET',
                                                       quantity=QUAN,
                                                       stopPrice=stop,
                                                       closePosition='true',
                                                       )
                tp_order = client.futures_create_order(symbol=coin,
                                                       side='BUY',
                                                       type='LIMIT',
                                                       quantity=quan1,
                                                       price=take1,
                                                       timeInForce='GTC'
                                                       )
                take2 = minus_percent(price_now, TP2)
                tp_order2 = client.futures_create_order(symbol=coin,
                                                        side='BUY',
                                                        type='LIMIT',
                                                        quantity=quan2,
                                                        price=take2,
                                                        timeInForce='GTC'
                                                        )
                take3 = minus_percent(price_now, TP3)
                tp_order3 = client.futures_create_order(symbol=coin,
                                                        side='BUY',
                                                        type='LIMIT',
                                                        quantity=quan3,
                                                        price=take3,
                                                        timeInForce='GTC'
                                                        )
            except BinanceAPIException as e:
                print(e)
        else:
            # нихуя не вышло
            bot.send_message(message.from_user.id, f'Нет нужной команды')
    except IndexError:
        print('list index out of range')


# проверяем входящие сообщения в ТГ у бота нонстоп
bot.polling(none_stop=True, interval=0)
