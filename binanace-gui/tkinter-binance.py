
from binance import AsyncClient, BinanceSocketManager
import tkinter as tk
from queue import Queue
import threading
import sys
import asyncio

async def binance_client(q):
    client = await AsyncClient.create()
    bm = BinanceSocketManager(client, user_timeout=60)
    # start any sockets here, i.e a trade socket
    ts = bm.trade_socket('BTCUSDT')
    # then start receiving messages
    async with ts as tscm:
        while True:
            data = await tscm.recv()
            q.put(data)
            # print('BTC:', round(float(data['p'])), 'usdt')

# 웹소켓 클라이언트 시작 함수
def start_binance_client(q):
    asyncio.run(binance_client(q))

# GUI 업데이트 함수
def update_gui(data):
    btc_value.set(f"{round(float(data['p'])):,d} USDT") # f"텍스트 {표현식}". {} 안에 표현식을 삽입하여 변수나 값의 포맷을 지정할 수 있습니다.

# 데이터 소비자
def consumer(q):
    while True:
        data = q.get()
        update_gui(data)

# 종료 시 처리 함수
def on_closing():
    sys.exit(0)

# 루트 윈도우 생성
root = tk.Tk()
root.title("binance Websocket")
root.geometry("400x200")
root.protocol("WM_DELETE_WINDOW", on_closing)

btc_value = tk.StringVar()  # Bitcoin 가격을 담을 변수 생성
btc_label = tk.Label(root, text="Bitcoin:")  # 라벨 생성
btc_label.place(x=10, y=10)  # 라벨 위치 설정
btc_entry = tk.Entry(root, textvariable=btc_value)  # 엔트리 위젯 생성 및 변수 연결
btc_entry.place(x=100, y=10)  # 엔트리 위젯 위치 설정

q = Queue()

upbit_thread = threading.Thread(target=start_binance_client, args=(q,))
upbit_thread.daemon = True
upbit_thread.start()

consumer_thread = threading.Thread(target=consumer, args=(q,))
consumer_thread.daemon = True
consumer_thread.start()

root.mainloop()



if __name__ == "__main__":
    asyncio.run(start_binance_client())
