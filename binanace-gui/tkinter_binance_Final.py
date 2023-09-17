# tkinter-binance(1) 코드에서 코인 가격 갱신 딜레이 해결.
# asyncio.gather()를 이용하여 병렬로 웹소켓 클라이언트를 실행하게 수정한 버전입니다. 
# 이렇게 하면 각 코인의 웹소켓 업데이트가 독립적으로 실행되어, 한 코인의 업데이트가 느려도 다른 코인들의 업데이트에 영향을 주지 않습니다.
# 참고로 gather()를 사용하는 궁극적인 목적이 q.put(data) 이 부분을 독립적으로 하기 위해서이다. 따라서 q.get(data) 이 부분도 독립적으로 만들어야 한다.

from binance import AsyncClient, BinanceSocketManager
import tkinter as tk
from queue import Queue
import threading
import sys
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

async def handle_socket(ts, q):
    try:
        async with ts as tscm:
            while True:
                res = await tscm.recv()
                q.put(res)
    except Exception as e:
        logging.error(f"Error in handle_socket: {e}") # 로깅: 문제가 발생했을 때 원인을 찾기 쉽도록 로깅을 추가할 수 있습니다.
    
async def binance_client(q_btc, q_neo, q_flm):
    client = await AsyncClient.create()
    bm = BinanceSocketManager(client, user_timeout=60)

    ts_btc = bm.trade_socket('BTCUSDT')
    ts_neo = bm.trade_socket('NEOUSDT')
    ts_flm = bm.trade_socket('FLMUSDT')

    await asyncio.gather(
        handle_socket(ts_btc, q_btc),
        handle_socket(ts_neo, q_neo),
        handle_socket(ts_flm, q_flm),
    )

def start_binance_client(q_btc, q_neo, q_flm):
    asyncio.run(binance_client(q_btc, q_neo, q_flm))

# 기존의 consumer 함수를 세 가지 코인에 대해 각각 정의합니다. q.put() 부분도 분리했으니 q.get()도 분리해야 delay가 안생긴다.
def consumer_btc(q_btc):
    while True:
        data_btc = q_btc.get()
        # GUI 업데이트 부분을 분리할 수도 있고, 그대로 둘 수도 있습니다.
        btc_value.set(f"{round(float(data_btc['p'])):,d} USDT")

def consumer_neo(q_neo):
    while True:
        data_neo = q_neo.get()
        neo_value.set(f"{float(data_neo['p']):} USDT")

def consumer_flm(q_flm):
    while True:
        data_flm = q_flm.get()
        flm_value.set(f"{float(data_flm['p']):} USDT")
        # root.after(0, root.update) 이 코드를 각 consumer마다 호출하면 문제가 생길 수 있다.


# 종료 시 처리 함수
def on_closing():
    sys.exit(0) # sys.exit(0)을 호출하여 메인 프로세스를 종료하면 다른 모든 스레드도 종료됩니다. 따라서 모든 스레드가 안전하게 종료되며, 프로그램이 깔끔하게 종료됩니다.

# 루트 윈도우 생성
root = tk.Tk()
root.title("binance Websocket")
root.geometry("400x200")
root.protocol("WM_DELETE_WINDOW", on_closing)

# 명시적으로 GUI 업데이트를 제어하려면, 메인 스레드에서 일정 시간 간격으로 화면을 업데이트하는 방식을 고려할 수 있습니다.
def periodic_update():
    root.update()
    root.after(100, periodic_update)  # 100ms마다 화면을 업데이트

root.after(100, periodic_update)

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

q_btc = Queue(maxsize=100) # asyncio.Queue 보다는 queue.Queue가 더 적합함. (asyncio.Queue는 코드 실행이 되는지도 불확실.)
q_neo = Queue(maxsize=50) # Queue를 생성할 때, 큐의 크기를 미리 정해두면 메모리 사용량을 제한할 수 있습니다. 
q_flm = Queue(maxsize=50)

upbit_thread = threading.Thread(target=start_binance_client, args=(q_btc, q_neo, q_flm,))
upbit_thread.daemon = True
upbit_thread.start()

# 각 consumer 함수에 대한 별도의 스레드를 생성합니다.
consumer_btc_thread = threading.Thread(target=consumer_btc, args=(q_btc,))
consumer_btc_thread.daemon = True
consumer_btc_thread.start()

consumer_neo_thread = threading.Thread(target=consumer_neo, args=(q_neo,))
consumer_neo_thread.daemon = True
consumer_neo_thread.start()

consumer_flm_thread = threading.Thread(target=consumer_flm, args=(q_flm,))
consumer_flm_thread.daemon = True
consumer_flm_thread.start()

root.mainloop()