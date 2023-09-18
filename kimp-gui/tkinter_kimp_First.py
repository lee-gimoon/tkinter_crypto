import websockets
import asyncio
import json
from binance import AsyncClient, BinanceSocketManager
import tkinter as tk
from queue import Queue
import threading
import sys

# 업비트 클라이언트.
async def upbit_client(upbit_btc_queue):
    uri = "wss://api.upbit.com/websocket/v1"
    async with websockets.connect(uri, ping_interval=60) as websocket:
        subscribe = [{"ticket": "test"}, {"type": "ticker", "codes": ["KRW-BTC"], "isOnlyRealtime": True}, {"format": "SIMPLE"}]
        subscribe = json.dumps(subscribe)
        await websocket.send(subscribe)

        while True:
            data = await websocket.recv()
            data = json.loads(data)
            data = round(data['tp'])
            upbit_btc_queue.put_nowait(data)

# 바이낸스 클라이언트.
async def binance_client(binance_btc_queue):
    client = await AsyncClient.create()
    bm = BinanceSocketManager(client, user_timeout=60)
    ts = bm.trade_socket("BTCUSDT")
    async with ts as tscm:
        while True:
            data = await tscm.recv()
            data = round(float(data['p']))
            binance_btc_queue.put_nowait(data)

# 웹소켓 클라이언트들 실행.
async def main(upbit_btc_queue, binance_btc_queue):
    upbit_task = asyncio.create_task(upbit_client(upbit_btc_queue))
    binance_task = asyncio.create_task(binance_client(binance_btc_queue))
    await asyncio.gather(upbit_task, binance_task)

def start_async_task(upbit_btc_queue, binance_btc_queue):
    asyncio.run(main(upbit_btc_queue, binance_btc_queue))

# 종료 시 처리 함수
def on_closing():
    sys.exit(0)

# gui에 큐에서 가져온 데이터 업데이트.
def consumer(upbit_btc_queue, binance_btc_queue):
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

        if last_upbit_data is not None and last_binance_data is not None and updated:
            binance_krw = last_binance_data * 1329
            BTC_KIMP = round(((last_upbit_data - binance_krw) / binance_krw) * 100, 2)

            if BTC_KIMP != last_BTC_KIMP:
                BTC_KIMP_str.set(f"{BTC_KIMP} %") # 김프를 gui 화면에 업데이트.
                last_BTC_KIMP = BTC_KIMP

# tkinter gui 실행.
root = tk.Tk()
root.title("KIMP Monitor")
root.geometry("400x200")

BTC_KIMP_str = tk.StringVar()
BTC_KIMP_label = tk.Label(root, text="BTC_KIMP:")
BTC_KIMP_label.place(x=10, y=10)
BTC_KIMP_entry = tk.Entry(root, textvariable=BTC_KIMP_str)
BTC_KIMP_entry.place(x=100, y=10)

upbit_btc_queue = Queue()
binance_btc_queue = Queue()

async_thread = threading.Thread(target=start_async_task, args=(upbit_btc_queue, binance_btc_queue))
async_thread.daemon = True
async_thread.start()

consumer_thread = threading.Thread(target=consumer, args=(upbit_btc_queue, binance_btc_queue))
consumer_thread.daemon = True
consumer_thread.start()

root.mainloop()