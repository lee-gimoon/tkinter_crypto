import websockets
import asyncio
import json
from binance import AsyncClient, BinanceSocketManager
import tkinter as tk
from queue import Queue
import threading
import sys
import logging

logging.basicConfig(level=logging.INFO)

# 업비트 클라이언트.
async def upbit_client(upbit_btc_queue, upbit_neo_queue):
    uri = "wss://api.upbit.com/websocket/v1"
    async with websockets.connect(uri, ping_interval=60) as websocket:
        subscribe = [
            {"ticket": "test"},
            {"type": "ticker", "codes": ["KRW-BTC", "KRW-NEO"], "isOnlyRealtime": True},
            {"format": "SIMPLE"}
        ]
        subscribe = json.dumps(subscribe)
        await websocket.send(subscribe)

        while True:
            data = await websocket.recv()
            data = json.loads(data)
            if data['cd'] == 'KRW-BTC':
                upbit_btc_queue.put_nowait(round(data['tp']))
            elif data['cd'] == 'KRW-NEO':
                upbit_neo_queue.put_nowait(round(data['tp']))

# 바이낸스 클라이언트.
async def handle_socket(ts, q):
    try:
        async with ts as tscm:
            while True:
                res = await tscm.recv()
                q.put(res)
    except Exception as e:
        logging.error(f"Error in handle_socket: {e}")

async def binance_client(binance_btc_queue, binance_neo_queue):
    client = await AsyncClient.create()
    bm = BinanceSocketManager(client, user_timeout=60)

    ts_btc = bm.trade_socket('BTCUSDT')
    ts_neo = bm.trade_socket('NEOUSDT')

    await asyncio.gather(
        handle_socket(ts_btc, binance_btc_queue),
        handle_socket(ts_neo, binance_neo_queue),
    )

# 웹소켓 클라이언트들 실행.
async def main(upbit_btc_queue, binance_btc_queue, upbit_neo_queue, binance_neo_queue):
    upbit_task = asyncio.create_task(upbit_client(upbit_btc_queue, upbit_neo_queue))
    binance_task = asyncio.create_task(binance_client(binance_btc_queue, binance_neo_queue))
    await asyncio.gather(upbit_task, binance_task)

def start_async_task(upbit_btc_queue, binance_btc_queue, upbit_neo_queue, binance_neo_queue):
    asyncio.run(main(upbit_btc_queue, binance_btc_queue, upbit_neo_queue, binance_neo_queue))

# 종료 시 처리 함수
def on_closing():
    sys.exit(0)

# gui에 큐에서 가져온 데이터 업데이트.
def consumer(upbit_btc_queue, binance_btc_queue, upbit_neo_queue, binance_neo_queue):
    last_upbit_neo_data = None
    last_BTC_KIMP = None
    last_NEO_KIMP = None

    while True:
        updated = False

        if not upbit_btc_queue.empty():
            last_upbit_btc_data = upbit_btc_queue.get()
            updated = True

        if not binance_btc_queue.empty():
            last_binance_btc_data = binance_btc_queue.get()
            updated = True

        if not upbit_neo_queue.empty():
            last_upbit_neo_data = upbit_neo_queue.get()
            updated = True

        if not binance_neo_queue.empty():
            last_binance_neo_data = binance_neo_queue.get()
            updated = True

        if last_upbit_neo_data is not None and last_binance_neo_data is not None and updated:
            # NEO 김프 계산 로직
            neo_krw = last_binance_neo_data * 1329  # 예시 환율
            NEO_KIMP = round(((last_upbit_neo_data - neo_krw) / neo_krw) * 100, 2)

            NEO_KIMP_str.set(f"{NEO_KIMP} %")  # 김프를 gui 화면에 업데이트.

        # ... (BTC에 대한 김프 계산 로직이 여기에 추가되어야 함)

# tkinter gui 실행.
root = tk.Tk()
root.title("KIMP Monitor")
root.geometry("400x200")

BTC_KIMP_str = tk.StringVar()
NEO_KIMP_str = tk.StringVar()

BTC_KIMP_label = tk.Label(root, text="BTC_KIMP:")
BTC_KIMP_label.place(x=10, y=10)
BTC_KIMP_entry = tk.Entry(root, textvariable=BTC_KIMP_str)
BTC_KIMP_entry.place(x=100, y=10)

NEO_KIMP_label = tk.Label(root, text="NEO_KIMP:")
NEO_KIMP_label.place(x=10, y=40)
NEO_KIMP_entry = tk.Entry(root, textvariable=NEO_KIMP_str)
NEO_KIMP_entry.place(x=100, y=40)

upbit_btc_queue = Queue()
binance_btc_queue = Queue()
upbit_neo_queue = Queue()
binance_neo_queue = Queue()

async_thread = threading.Thread(target=start_async_task, args=(upbit_btc_queue, binance_btc_queue, upbit_neo_queue, binance_neo_queue))
async_thread.daemon = True
async_thread.start()

consumer_thread = threading.Thread(target=consumer, args=(upbit_btc_queue, binance_btc_queue, upbit_neo_queue, binance_neo_queue))
consumer_thread.daemon = True
consumer_thread.start()

root.mainloop()
