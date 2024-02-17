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
symbol = "BTCUSDT"
#price_now = float(client.futures_symbol_ticker(symbol=symbol, requests_params={'timeout': 1})['price'])
#latest_price = client.futures_symbol_ticker(symbol=symbol)['price']
#print("Время запроса цены монет командой: price_now = float(client.futures_symbol_ticker(symbol=symbol, requests_params={'timeout': 1})['price'])")
#print(price_now)
#i = 0
#while i < 10:
#    start_time = time.time()
#    price_now = float(client.futures_symbol_ticker(symbol=symbol, requests_params={'timeout': 1})['price'])
#    end_time = time.time()
#    elapsed_time = round(end_time - start_time, 3)
#    print('Время запроса: ' + str(elapsed_time) + 'сек')
#    time.sleep(1)
#    i = i + 1

#print("Время запроса цены монет командой: latest_price = client.futures_symbol_ticker(symbol=symbol)['price']")
#print(latest_price)
#i = 0
#while i < 10:
#    start_time = time.time()
#    latest_price = client.futures_symbol_ticker(symbol=symbol)['price']
#    end_time = time.time()
#    elapsed_time = round(end_time - start_time, 3)
#    print('Время запроса: ' + str(elapsed_time) + 'сек')
#    time.sleep(1)
#    i = i + 1

# Чекаем цену входа открытой позиции
orders = client.futures_position_information(symbol=symbol)
print(orders[0]['entryPrice'])

# Чекаем баланс кошелька
balance = client.futures_account_balance()
wallet = balance[5]['balance']
print(int(float(wallet)))
