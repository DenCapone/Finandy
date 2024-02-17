import os
import telebot
import telethon
import time
import datetime

from binance.exceptions import BinanceAPIException
from views import plus_percent, minus_percent
from const import MONEY, TP, TP2, TP3, SL, QUAN
from binance.client import Client
from dotenv import load_dotenv
from telethon import TelegramClient, events

load_dotenv()

api_id = os.getenv('API_ID2')
api_hash = os.getenv('API_HASH2')
phone = '+79262132124'
api_key = os.getenv('KEY2')
api_secret = os.getenv('SECRET2')
# создаём клиента на бирже
client = Client(api_key, api_secret)
client_tg = TelegramClient(phone, api_id, api_hash)
client_tg.start()
# client_tg.get_entity(5930168941)


# Реакция при получении нового сообщения в группе
# Den chat
@client_tg.on(events.NewMessage(-1001519195868))
# Algo test chat
# @client_tg.on(events.NewMessage(-1002039000124))
# Elden test chat
# @client_tg.on(events.NewMessage(-733712583))
async def main(event):
    # Получаем текст нового сообщения
    message = event.message.text
    # await client_tg.send_message(client_tg.get_entity('5930168941'), message)
    try:
        caption = message.replace('#', '', 1).split()
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
            await client_tg.send_message(1002039000124, f'Нет нужной команды')
    except IndexError:
        print('list index out of range')
    mes = event.message
    await client_tg.send_message(-1002039000124, mes)

client_tg.run_until_disconnected()
