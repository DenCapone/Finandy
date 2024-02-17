import os
import telebot
import telethon
import time
import datetime

from views import plus_percent, minus_percent
from const_den import MONEY, TP, TP2, TP3, SL
from binance.client import Client
from dotenv import load_dotenv
from telethon import TelegramClient, events

load_dotenv()

api_id = os.getenv('API_ID2')
api_hash = os.getenv('API_HASH2')
phone = '+79262132124'
api_key = os.getenv('KEY4')
api_secret = os.getenv('SECRET4')
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
    start_time = time.time()
    try:
        caption = event.message.text.replace('#', '', 1).split()
        coin = caption[0] + 'USDT'
        end_time5 = time.time()
        elapsed_time5 = end_time5 - start_time
        print('Время обработки сообщения:', round(elapsed_time5, 3))
    except AttributeError:
        print('NoneType')
        return
    try:
        if caption[1].lower() == 'buy':
            try:
                # получаем таблицу с текущей стоимостью монеты
                price_now = float(client.futures_symbol_ticker(symbol=coin, requests_params={'timeout': 1})['price'])
                end_time2 = time.time()
                elapsed_time2 = end_time2 - start_time
                print('Время запроса цены:', elapsed_time2)
            except:
                print('не смог получить текущий курс, пробую ещё раз')
                time.sleep(1)
                price_now = float(client.futures_symbol_ticker(symbol=coin, requests_params={'timeout': 1})['price'])
            # умножаем сумму, которую хотим потратить на текущую стоимость
            quan = float(round((MONEY / price_now), 3))
            # print(quan)
            # округляем количество монет до целого числа
            if quan < 1:
                try:
                    # пытаемся купить монеты
                    buy_futures = client.futures_create_order(symbol=coin, side='BUY', type='market', quantity=quan)
                    end_time1 = time.time()
                    elapsed_time1 = end_time1 - start_time
                    print('Время покупки quan < 1:', elapsed_time1)
                except:
                    time.sleep(1)
                    buy_futures = client.futures_create_order(symbol=coin, side='BUY', type='market', quantity=quan)
                quan1 = float(round((quan * 0.5), 4))
                quan2 = quan - quan1
                take1 = float(round(plus_percent(price_now, 2), 2))
                stop = float(round(minus_percent(price_now, 0.5), 2))
                sl_order = client.futures_create_order(symbol=coin,
                                                       side='SELL',
                                                       type='STOP_MARKET',
                                                       quantity=quan,
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
                take2 = float(round(plus_percent(price_now, 3), 2))
                tp_order2 = client.futures_create_order(symbol=coin,
                                                        side='SELL',
                                                        type='LIMIT',
                                                        quantity=quan2,
                                                        price=take2,
                                                        timeInForce='GTC'
                                                        )
            else:
                quan = round(quan)
                try:
                    # пытаемся купить монеты
                    buy_futures = client.futures_create_order(symbol=coin, side='BUY', type='market', quantity=quan)
                    end_time1 = time.time()
                    elapsed_time1 = end_time1 - start_time
                    print('Время покупки quan < 1(else):', elapsed_time1)
                except:
                    time.sleep(1)
                    buy_futures = client.futures_create_order(symbol=coin, side='BUY', type='market', quantity=quan)
                quan1 = round(quan * 0.5)
                quan2 = round(quan * 0.25)
                quan3 = quan - quan1 - quan2
                take1 = plus_percent(price_now, TP)
                stop = minus_percent(price_now, SL)
                sl_order = client.futures_create_order(symbol=coin,
                                                       side='SELL',
                                                       type='STOP_MARKET',
                                                       quantity=quan,
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
        elif caption[1].lower() == 'short':
            try:
                # получаем таблицу с текущей стоимостью монеты
                price_now = float(client.futures_symbol_ticker(symbol=coin, requests_params={'timeout': 1})['price'])
                end_time6 = time.time()
                elapsed_time6 = end_time6 - start_time
                print('Время распознования шорта:', elapsed_time6)
            except:
                print('не смог получить текущий курс, пробую ещё раз')
                time.sleep(1)
                price_now = float(client.futures_symbol_ticker(symbol=coin, requests_params={'timeout': 1})['price'])
            # умножаем сумму, которую хотим потратить на текущую стоимость
            quan = float(round((MONEY / price_now), 3))
            print(quan)
            # округляем количество монет до целого числа
            if quan < 1:
                try:
                    # пытаемся купить монеты
                    buy_futures = client.futures_create_order(symbol=coin, side='SELL', type='market', quantity=quan)
                    end_time7 = time.time()
                    elapsed_time7 = end_time7 - start_time
                    print('Время открытия шорта:', elapsed_time7)
                except:
                    time.sleep(1)
                    buy_futures = client.futures_create_order(symbol=coin, side='SELL', type='market', quantity=quan)
                quan1 = float(round((quan * 0.5), 4))
                quan2 = quan - quan1
                take1 = float(round(minus_percent(price_now, 2), 2))
                stop = float(round(plus_percent(price_now, 0.5), 2))
                sl_order = client.futures_create_order(symbol=coin,
                                                       side='BUY',
                                                       type='STOP_MARKET',
                                                       quantity=quan,
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
                take2 = float(round(minus_percent(price_now, 3), 2))
                tp_order2 = client.futures_create_order(symbol=coin,
                                                        side='BUY',
                                                        type='LIMIT',
                                                        quantity=quan2,
                                                        price=take2,
                                                        timeInForce='GTC'
                                                        )
            else:
                quan = round(quan)
                try:
                    # пытаемся купить монеты
                    buy_futures = client.futures_create_order(symbol=coin, side='SELL', type='market', quantity=quan)
                    end_time8 = time.time()
                    elapsed_time8 = end_time8 - start_time
                    print('Время открытия шорта 2:', elapsed_time8)
                except:
                    time.sleep(1)
                    buy_futures = client.futures_create_order(symbol=coin, side='SELL', type='market', quantity=quan)
                quan1 = round(quan * 0.5)
                quan2 = round(quan * 0.25)
                quan3 = quan - quan1 - quan2
                take1 = minus_percent(price_now, TP)
                stop = plus_percent(price_now, SL)
                sl_order = client.futures_create_order(symbol=coin,
                                                       side='BUY',
                                                       type='STOP_MARKET',
                                                       quantity=quan,
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
        else:
            # нихуя не вышло
            await client_tg.send_message(-1002039000124, f'Нет нужной команды')
    except IndexError:
        print('list index out of range')
    end_time = time.time()
    elapsed_time = end_time - start_time
    print('Время выполнения кода:', elapsed_time)
    mes = event.message
    await client_tg.send_message(-1002039000124, mes)


client_tg.run_until_disconnected()
