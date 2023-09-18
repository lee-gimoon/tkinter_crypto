# 코인 2개 이상의 김프를 계산하여 tkinter gui 화면에 출력하자.
import websockets
import asyncio
import json
from binance import AsyncClient, BinanceSocketManager
import sys
import tkinter as tk
from queue import Queue
import threading
import time

async def upbit_client(upbit_btc_queue, upbit_neo_queue):
    uri = "wss://api.upbit.com/websocket/v1"
    async with websockets.connect(uri, ping_interval=60) as websocket:
        subscribe = [{"ticket":"test"}, 
                     {"type":"ticker", "codes":["KRW-BTC", "KRW-NEO"], "isOnlyRealtime": True},
                     {"format":"SIMPLE"}]
        subscribe = json.dumps(subscribe)
        await websocket.send(subscribe)

        while True:
            data = await websocket.recv()
            data = json.loads(data)
            price = round(data['tp'])
            if data['cd'] == 'KRW-BTC':
                upbit_btc_queue.put_nowait(price)
            elif data['cd'] == 'KRW-NEO':
                upbit_neo_queue.put_nowait(price)

import logging

logging.basicConfig(level=logging.INFO)

async def handle_socket(ts, q, coin_type):
    try:
        async with ts as tscm:
            while True:
                res = await tscm.recv()
                if coin_type == 'BTC': # 조건1(BTC)이 참일 때 실행될 코드
                    # Handle BTC case
                    q.put(round(float(res['p'])))
                elif coin_type == 'NEO': # 조건1이 거짓이고 조건2(NEO)가 참일 때 실행될 코드
                    # Handle NEO case
                    q.put(float(res['p']))
    except Exception as e:
        logging.error(f"Error in handle_socket: {e}")

async def binance_client(binance_btc_queue, binance_neo_queue):
    client = await AsyncClient.create()
    bm = BinanceSocketManager(client, user_timeout=60)

    ts_btc = bm.trade_socket('BTCUSDT')
    ts_neo = bm.trade_socket('NEOUSDT')

    await asyncio.gather(
        handle_socket(ts_btc, binance_btc_queue, 'BTC'),
        handle_socket(ts_neo, binance_neo_queue, 'NEO'),
    )


# 웹소켓 클라이언트들 실행.
async def main(upbit_btc_queue, upbit_neo_queue, binance_btc_queue, binance_neo_queue):
    upbit_task = asyncio.create_task(upbit_client(upbit_btc_queue, upbit_neo_queue))
    binance_task = asyncio.create_task(binance_client(binance_btc_queue, binance_neo_queue))
    await asyncio.gather(upbit_task, binance_task)

def start_async_task(upbit_btc_queue, upbit_neo_queue, binance_btc_queue, binance_neo_queue):
    asyncio.run(main(upbit_btc_queue, upbit_neo_queue, binance_btc_queue, binance_neo_queue))

# 종료 시 처리 함수
def on_closing():
    sys.exit(0)


def btc_kimp_consumer(upbit_btc_queue, binance_btc_queue):
    last_upbit_data = None
    last_binance_data = None
    last_BTC_KIMP = None
    
    while True:
        updated = False

        if not upbit_btc_queue.empty():
            last_upbit_data = upbit_btc_queue.get()
            updated = True

        if not binance_btc_queue.empty():
            last_binance_data = binance_btc_queue.get()
            updated = True

        if last_upbit_data is not None and last_binance_data is not None and updated: # 이 조건문은 세 가지 조건이 모두 참일 때만 코드 블록 내의 로직을 실행합니다.
            binance_krw = last_binance_data * 1325 # Convert USD to KRW
            BTC_KIMP = round(((last_upbit_data - binance_krw) / binance_krw) * 100, 2)

            if BTC_KIMP != last_BTC_KIMP:
                BTC_KIMP_str.set(f"{BTC_KIMP} %") # 김프를 gui 화면에 업데이트.
                last_BTC_KIMP = BTC_KIMP
        # Rate Limiting: GUI 업데이트 빈도를 제한할 수 있습니다. 너무 빠른 업데이트는 GUI를 느리게 만들 수 있습니다.
        time.sleep(0.1)  # 0.1초 대기 (Rate Limiting)


def neo_kimp_consumer(upbit_neo_queue, binance_neo_queue): 
    last_upbit_neo_data = None # 마지막으로 알려진 데이터 사용(if not). (실시간 시스템에서 사용하는 패턴.)
    last_binance_neo_data = None
    last_NEO_KIMP = None
    
    while True:
        updated = False

        if not upbit_neo_queue.empty(): # 업비트 네오 큐가 비어있지 않으면 가격을 가져와 업데이트.
            last_upbit_neo_data = upbit_neo_queue.get()
            updated = True

        if not binance_neo_queue.empty(): # 바이낸스 네오 큐가 비어있지 않으면 가격을 가져와 업데이트.
            last_binance_neo_data = binance_neo_queue.get()
            updated = True

        if last_upbit_neo_data is not None and last_binance_neo_data is not None and updated: # 이 조건문은 세 가지 조건이 모두 참일 때만 코드 블록 내의 로직을 실행합니다.
            binance_neo_krw = last_binance_neo_data * 1325 # Convert USD to KRW
            NEO_KIMP = round(((last_upbit_neo_data - binance_neo_krw) / binance_neo_krw) * 100, 2)

            if NEO_KIMP != last_NEO_KIMP:
                NEO_KIMP_str.set(f"{NEO_KIMP} %")
                last_NEO_KIMP = NEO_KIMP
                
        time.sleep(0.1)  # 0.1초 대기 (Rate Limiting)


# tkinter gui 실행.
root = tk.Tk()
root.title("KIMP Monitor")
root.geometry("400x200")

BTC_KIMP_str = tk.StringVar()
BTC_KIMP_label = tk.Label(root, text="BTC_KIMP:")
BTC_KIMP_label.place(x=10, y=10)
BTC_KIMP_entry = tk.Entry(root, textvariable=BTC_KIMP_str)
BTC_KIMP_entry.place(x=100, y=10)

NEO_KIMP_str = tk.StringVar()
NEO_KIMP_label = tk.Label(root, text="NEO_KIMP:")
NEO_KIMP_label.place(x=10, y=40)
NEO_KIMP_entry = tk.Entry(root, textvariable=NEO_KIMP_str)
NEO_KIMP_entry.place(x=100, y=40)

upbit_btc_queue = Queue()
binance_btc_queue = Queue()
upbit_neo_queue = Queue()
binance_neo_queue = Queue()

async_thread = threading.Thread(target=start_async_task, args=(upbit_btc_queue, upbit_neo_queue, binance_btc_queue, binance_neo_queue))
async_thread.daemon = True
async_thread.start()

btc_consumer_thread = threading.Thread(target=btc_kimp_consumer, args=(upbit_btc_queue, binance_btc_queue))
btc_consumer_thread.daemon = True
btc_consumer_thread.start()

neo_consumer_thread = threading.Thread(target=neo_kimp_consumer, args=(upbit_neo_queue, binance_neo_queue))
neo_consumer_thread.daemon = True
neo_consumer_thread.start()

root.mainloop()