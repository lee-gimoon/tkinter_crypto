
from binance import AsyncClient, BinanceSocketManager
import tkinter as tk
from queue import Queue
import threading
import sys
import asyncio

async def binance_client(q_btc, q_neo, q_flm):
    client = await AsyncClient.create()
    bm = BinanceSocketManager(client, user_timeout=60)
    
    # Define trade sockets for each coin
    coins = ['BTCUSDT', 'NEOUSDT', 'FLMUSDT']
    ts_coins = [bm.trade_socket(coin) for coin in coins]
    
    async def receive_and_put_data(tscm, q):
        async with tscm as tscm_instance:
            while True:
                data = await tscm_instance.recv()
                q.put(data)
    
    # Start receiving messages for each coin in parallel
    await asyncio.gather(*[receive_and_put_data(ts, q) for ts, q in zip(ts_coins, [q_btc, q_neo, q_flm])])

# 웹소켓 클라이언트 시작 함수
def start_binance_client(q_btc, q_neo, q_flm):
    asyncio.run(binance_client(q_btc, q_neo, q_flm))

# GUI 업데이트 함수
def update_gui(data_btc, data_neo, data_flm):
    btc_value.set(f"{round(float(data_btc['p'])):,d} USDT") # f"텍스트 {표현식}". {} 안에 표현식을 삽입하여 변수나 값의 포맷을 지정할 수 있습니다.
    neo_value.set(f"{float(data_neo['p']):} USDT")
    flm_value.set(f"{float(data_flm['p']):} USDT")
    root.after(0, root.update)

# 데이터 소비자
def consumer(q_btc, q_neo, q_flm):
    while True:
        data_btc = q_btc.get()
        data_neo = q_neo.get()
        data_flm = q_flm.get()
        update_gui(data_btc, data_neo, data_flm)

# 종료 시 처리 함수
def on_closing():
    sys.exit(0) # sys.exit(0)을 호출하여 메인 프로세스를 종료하면 다른 모든 스레드도 종료됩니다. 따라서 모든 스레드가 안전하게 종료되며, 프로그램이 깔끔하게 종료됩니다.

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

neo_value = tk.StringVar()  # Bitcoin 가격을 담을 변수 생성
neo_label = tk.Label(root, text="Neo:")  # 라벨 생성
neo_label.place(x=10, y=40)  # 라벨 위치 설정
neo_entry = tk.Entry(root, textvariable=neo_value)  # 엔트리 위젯 생성 및 변수 연결
neo_entry.place(x=100, y=40)  # 엔트리 위젯 위치 설정

flm_value = tk.StringVar()  # Bitcoin 가격을 담을 변수 생성
flm_label = tk.Label(root, text="Flamingo")  # 라벨 생성
flm_label.place(x=10, y=70)  # 라벨 위치 설정
flm_entry = tk.Entry(root, textvariable=flm_value)  # 엔트리 위젯 생성 및 변수 연결
flm_entry.place(x=100, y=70)  # 엔트리 위젯 위치 설정

q_btc = Queue() # asyncio.Queue 보다는 queue.Queue가 더 적합함. (asyncio.Queue는 코드 실행이 되는지도 불확실.)
q_neo = Queue()
q_flm = Queue()

upbit_thread = threading.Thread(target=start_binance_client, args=(q_btc, q_neo, q_flm,))
upbit_thread.daemon = True
upbit_thread.start()

consumer_thread = threading.Thread(target=consumer, args=(q_btc, q_neo, q_flm,))
consumer_thread.daemon = True
consumer_thread.start()

root.mainloop()