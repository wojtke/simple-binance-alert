fromb binance.websockets import BinanceSocketManager
from binance.client import Client
from time import sleep
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import datetime
import time
import winsound


lines = []


def get_time(arr, now):
    timezone=now/1000-(int)(time.time())
    dt = datetime.datetime(2020, arr[0], arr[1], arr[2], arr[3])
    return 1000*(time.mktime(dt.timetuple())-timezone)

def linear(line, now):
    return (line[1][0]-line[0][0])*(now-get_time(line[0][1], now))/(get_time(line[1][1], now)-get_time(line[0][1], now)) + line[0][0]

def process_message(msg):
   # print(msg)

    price=float(msg['c'])
    now=msg['E']

    print("----------", datetime.datetime.fromtimestamp(round(now/1000)), "----------")
    print("  Latest price:", price)
    for line in lines:
        lin_price =linear(line, now) 
        print("  Price triggering alarm", round(lin_price,2), "+-",line[2])
        if abs(price-lin_price)<line[2]:
            winsound.PlaySound('alarm.wav', winsound.SND_FILENAME)
            print("RUAUAUAUAUAUAU")

def add_line(p1, p2, buf):
    lines.append([p1,p2, buf])

def show_lines():
    candles = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_15MINUTE, limit=1000)
    df = pd.DataFrame(candles)
    df = df[[0,1,2,3,4]]
    fig = go.Figure(data=[go.Candlestick(x=df[0],
                open=df[1],
                high=df[2],
                low=df[3],
                close=df[4])])

    now = candles[-1][0]

    for line in lines:
        fig.add_trace(go.Scatter(x=[get_time(line[0][1], now), get_time(line[1][1], now)], y=[line[0][0], line[1][0]], name="linear", line_shape='linear'))

    fig.show()
    time.sleep(3)

    czy = "y"#input("Czy tak ma byc? (y/n)\n>")

    if czy.lower()=='y'or czy.lower()=="yes":
        print("Zatwierdzone zostalo!")
        return True
    else: 
        print("Nie zostalo zatwierdzone!")
        return False


client = Client("","")
add_line([6826, [3, 24, 20, 45]], [4160, [3, 15, 12, 30]], 100)


if show_lines():
    bm = BinanceSocketManager(client)
    conn_key = bm.start_symbol_ticker_socket('BTCUSDT', process_message)
    bm.start()






