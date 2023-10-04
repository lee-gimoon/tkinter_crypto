
# Second_tkinter_upbit.py 파일 업그레이드 버전.
# if elif 대신 사용 하는 딕셔너리 매핑 코드. (if-elif 구문을 사용해서 몇 개의 문자열 값을 비교하는 것은 자원 소모 측면에서 거의 무시할 수 있는 수준입니다. 그럼에도 불구하고, 더 효율적이고 확장성 있는 방법을 원한다면, 딕셔너리를 사용하여 이를 개선할 수 있습니다.)
# 딕셔너리 매핑: 코드를 간결하게 만들고 분류 속도를 향상시키기 위해 딕셔너리 매핑을 사용할 수 있습니다. 코드와 값을 직접 매핑한 딕셔너리를 사용하여 해당 코드에 대한 값을 설정할 수 있습니다.
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
    subscribe = [{"ticket": "test"}, {"type": "trade", "codes": ["KRW-BTC", "KRW-ETH", "KRW-NEO", "KRW-BCH", "KRW-EOS", "KRW-STX", "KRW-SOL", "KRW-TRX", "KRW-WAVES", "KRW-MATIC", "KRW-ADA"], "isOnlyRealtime": True}, {"format": "SIMPLE"}]
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
    if variable: # variable이 즉, 변수가 0이 아니거나 빈 문자열이 아닌 경우 True로 처리되어 코드블록 실행.
        variable.set(format(value, ",d")) # ",d"의 의미 => 1,234,567처럼 1000단위 마다 ,로 보기쉽게 해줌.

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

root = tk.Tk()  # 루트 윈도우 생성
root.title("Upbit Websocket")
root.geometry("800x500")
root.protocol("WM_DELETE_WINDOW", on_closing)

# 코드와 변수의 매핑 딕셔너리
code_to_variable = {
    'KRW-BTC': tk.StringVar(),
    'KRW-ETH': tk.StringVar(),
    'KRW-NEO': tk.StringVar(),
    'KRW-BCH': tk.StringVar(),
    'KRW-EOS': tk.StringVar(),
    'KRW-STX': tk.StringVar(),
    'KRW-SOL': tk.StringVar(),
    'KRW-TRX': tk.StringVar(),
    'KRW-WAVES': tk.StringVar(),
    'KRW-MATIC': tk.StringVar(),
    'KRW-ADA': tk.StringVar()
}

# 코드에 따른 엔트리 위젯 생성
y_position = 10
for code in code_to_variable.keys():
    label = tk.Label(root, text=f"{code}:")
    label.place(x=10, y=y_position)
    entry = tk.Entry(root, textvariable=code_to_variable[code])
    entry.place(x=100, y=y_position)
    y_position += 30

q = Queue()

upbit_thread = threading.Thread(target=start_upbit_client, args=(q,))
upbit_thread.daemon = True
upbit_thread.start()

consumer_thread = threading.Thread(target=consumer, args=(q,))
consumer_thread.daemon = True
consumer_thread.start()

root.mainloop()
