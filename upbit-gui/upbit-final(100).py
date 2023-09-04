import json
import tkinter as tk
import websockets
from queue import Queue
import threading
import sys
import asyncio

# 웹소켓 클라이언트
async def upbit_client(q):
    uri = "wss://api.upbit.com/websocket/v1"
    subscribe = [
        {"ticket": "test"},
        {"type": "trade", "codes": [
            'KRW-BTC', 'KRW-XRP', 'KRW-SEI', 'KRW-XLM', 'KRW-BCH', 'KRW-SUI', 'KRW-STORJ', 'KRW-ETH', 'KRW-STX', 'KRW-ZRX',
            'KRW-FLOW', 'KRW-ETC', 'KRW-SOL', 'KRW-TRX', 'KRW-KAVA', 'KRW-SAND', 'KRW-NEO', 'KRW-ARB', 'KRW-EOS', 'KRW-MTL',
            'KRW-WAVES', 'KRW-MASK', 'KRW-MATIC', 'KRW-ADA', 'KRW-APT', 'KRW-PLA', 'KRW-AXS', 'KRW-ELF', 'KRW-LINK', 'KRW-IOTA',
            'KRW-ALGO', 'KRW-KNC', 'KRW-GMT', 'KRW-1INCH', 'KRW-POWR', 'KRW-SXP', 'KRW-GAS', 'KRW-STRAX', 'KRW-ICX', 'KRW-MANA',
            'KRW-QTUM', 'KRW-LSK', 'KRW-DOT', 'KRW-NEAR', 'KRW-ATOM', 'KRW-GLM', 'KRW-IMX', 'KRW-POLYX', 'KRW-BAT', 'KRW-AERGO',
            'KRW-AVAX', 'KRW-HIVE', 'KRW-ONG', 'KRW-STEEM', 'KRW-ENJ', 'KRW-PUNDIX', 'KRW-THETA', 'KRW-GRT', 'KRW-AAVE', 'KRW-XTZ'
        ], "isOnlyRealtime": True},
        {"format": "SIMPLE"}
    ]
    subscribe_data = json.dumps(subscribe)

    async with websockets.connect(uri, ping_interval=60) as websocket:
        await websocket.send(subscribe_data)

        while True:
            data = await websocket.recv()
            q.put(json.loads(data))

# 웹소켓 클라이언트 시작 함수
def start_upbit_client(q):
    asyncio.run(upbit_client(q))

# 코드와 변수를 연결하는 함수
def update_variable(code, value):
    variable = code_to_variable.get(code)
    if variable:
        variable.set(format(value, ",d"))

# 데이터 소비자
def consumer(q):
    while True:
        data = q.get()
        code = data['cd']
        value = int(data.get('tp'))
        update_variable(code, value)

# 종료 시 처리 함수
def on_closing():
    sys.exit(0)

# 루트 윈도우 생성
root = tk.Tk()
root.title("Upbit Websocket")
root.geometry("1600x400")
root.protocol("WM_DELETE_WINDOW", on_closing)

# 코드와 변수의 매핑 딕셔너리
code_to_variable = {
    'KRW-BTC': tk.StringVar(), 'KRW-XRP': tk.StringVar(), 'KRW-SEI': tk.StringVar(), 'KRW-XLM': tk.StringVar(),
    'KRW-BCH': tk.StringVar(), 'KRW-SUI': tk.StringVar(), 'KRW-STORJ': tk.StringVar(), 'KRW-ETH': tk.StringVar(),
    'KRW-STX': tk.StringVar(), 'KRW-ZRX': tk.StringVar(), 'KRW-FLOW': tk.StringVar(), 'KRW-ETC': tk.StringVar(),
    'KRW-SOL': tk.StringVar(), 'KRW-TRX': tk.StringVar(), 'KRW-KAVA': tk.StringVar(), 'KRW-SAND': tk.StringVar(),
    'KRW-NEO': tk.StringVar(), 'KRW-ARB': tk.StringVar(), 'KRW-EOS': tk.StringVar(), 'KRW-MTL': tk.StringVar(),
    'KRW-WAVES': tk.StringVar(), 'KRW-MASK': tk.StringVar(), 'KRW-MATIC': tk.StringVar(), 'KRW-ADA': tk.StringVar(),
    'KRW-APT': tk.StringVar(), 'KRW-PLA': tk.StringVar(), 'KRW-AXS': tk.StringVar(), 'KRW-ELF': tk.StringVar(),
    'KRW-LINK': tk.StringVar(), 'KRW-IOTA': tk.StringVar(), 'KRW-ALGO': tk.StringVar(), 'KRW-KNC': tk.StringVar(),
    'KRW-GMT': tk.StringVar(), 'KRW-1INCH': tk.StringVar(), 'KRW-POWR': tk.StringVar(), 'KRW-SXP': tk.StringVar(),
    'KRW-GAS': tk.StringVar(), 'KRW-STRAX': tk.StringVar(), 'KRW-ICX': tk.StringVar(), 'KRW-MANA': tk.StringVar(),
    'KRW-QTUM': tk.StringVar(), 'KRW-LSK': tk.StringVar(), 'KRW-DOT': tk.StringVar(), 'KRW-NEAR': tk.StringVar(),
    'KRW-ATOM': tk.StringVar(), 'KRW-GLM': tk.StringVar(), 'KRW-IMX': tk.StringVar(), 'KRW-POLYX': tk.StringVar(),
    'KRW-BAT': tk.StringVar(), 'KRW-AERGO': tk.StringVar(), 'KRW-AVAX': tk.StringVar(), 'KRW-HIVE': tk.StringVar(),
    'KRW-ONG': tk.StringVar(), 'KRW-STEEM': tk.StringVar(), 'KRW-ENJ': tk.StringVar(), 'KRW-PUNDIX': tk.StringVar(),
    'KRW-THETA': tk.StringVar(), 'KRW-GRT': tk.StringVar(), 'KRW-AAVE': tk.StringVar(), 'KRW-XTZ': tk.StringVar()
}

# 코드에 따른 엔트리 위젯 생성
row_num = 0
col_num = 0

for code in code_to_variable.keys():
    label = tk.Label(root, text=f"{code}:")
    label.grid(row=row_num, column=col_num, padx=10, pady=5, sticky="e")

    entry = tk.Entry(root, textvariable=code_to_variable[code])
    entry.grid(row=row_num, column=col_num+1, padx=10, pady=5, sticky="w")

    row_num += 1
    if row_num % 10 == 0:
        row_num = 0
        col_num += 2

q = Queue()

upbit_thread = threading.Thread(target=start_upbit_client, args=(q,))
upbit_thread.daemon = True
upbit_thread.start()

consumer_thread = threading.Thread(target=consumer, args=(q,))
consumer_thread.daemon = True
consumer_thread.start()

root.mainloop()
