# 단, 1개의 코인의 가격을 tkinter gui 에 출력해보자.
import json
import tkinter as tk
import websockets
from queue import Queue
import threading
import sys
import asyncio

# 비동기로 업비트 웹소켓에 연결하여 데이터 수신하는 함수
async def upbit_client(q):
    uri = "wss://api.upbit.com/websocket/v1"
    subscribe = [{"ticket": "test"}, {"type": "trade", "codes": ["KRW-BTC"], "isOnlyRealtime": True}, {"format": "SIMPLE"}]
    subscribe_data = json.dumps(subscribe)

    async with websockets.connect(uri, ping_interval=60) as websocket:
        await websocket.send(subscribe_data)

        while True:
            data = await websocket.recv()  # 웹소켓 데이터 수신. 어떤 data가 들어오는지 보고 싶으면 print(data)로 확인해보자.
            q.put(json.loads(data))  # 받은 데이터 큐에 넣음

# 큐에서 데이터를 가져와 GUI를 업데이트하는 함수
def consumer(q):
    while True:
        data = q.get()  # 큐에서 데이터 가져옴
        update_gui(data)

# GUI 업데이트 함수
def update_gui(data):
    btc_value.set(format(int(data.get('tp')), ",d"))  # 받은 데이터에서 'tp' 값을 추출하여 포맷팅 후 GUI 변수에 설정
    # root.after(0, root.update)  # GUI 업데이트를 스케줄링

# 웹소켓 클라이언트 시작 함수
def start_upbit_client(q):
    asyncio.run(upbit_client(q))

# 창을 닫을 때 실행할 함수
def on_closing():
    sys.exit(0) # sys.exit(0)라는 줄은 종료 코드가 0인 상태로 프로그램을 종료하는 데 사용됩니다. 
    # 종료 코드는 프로그램이 성공적으로 종료되었는지(종료 코드 0) 또는 오류를 만났는지(0이 아닌 종료 코드) 운영 체제에 알리는 방법입니다.
    # 종료 코드가 0인 상태로 프로그램을 종료하는 것은 일반적으로 프로그램이 오류 없이 종료되었음을 나타냅니다.

q = Queue()  # 데이터를 담을 큐 생성

# 웹소켓 클라이언트 스레드 생성 및 실행
upbit_thread = threading.Thread(target=start_upbit_client, args=(q,))
upbit_thread.daemon = True
upbit_thread.start()

# Tkinter 창 생성
root = tk.Tk()
root.title("Upbit Websocket")
root.geometry("400x200")
root.protocol("WM_DELETE_WINDOW", on_closing)

btc_value = tk.StringVar()  # Bitcoin 가격을 담을 변수 생성
btc_label = tk.Label(root, text="Bitcoin:")  # 라벨 생성
btc_label.place(x=10, y=10)  # 라벨 위치 설정
btc_entry = tk.Entry(root, textvariable=btc_value)  # 엔트리 위젯 생성 및 변수 연결
btc_entry.place(x=100, y=10)  # 엔트리 위젯 위치 설정

# 데이터를 받아와 GUI를 업데이트하는 스레드 생성 및 실행
consumer_thread = threading.Thread(target=consumer, args=(q,))
consumer_thread.daemon = True
consumer_thread.start()

root.mainloop()  # Tkinter 이벤트 루프 실행
