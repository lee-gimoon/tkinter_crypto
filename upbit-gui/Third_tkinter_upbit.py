# 여러 개의 연속적인 if 문과 elif 문을 비교할 때, 파이썬 인터프리터는 각각의 조건을 순차적으로 평가하면서 첫 번째로 True로 평가되는 블록을 실행합니다. 
# 따라서 if-elif 구조를 사용하는 경우, 첫 번째로 True로 평가되는 조건에 따라 해당하는 블록만 실행되며 나머지 블록들은 평가되지 않습니다. 이로 인해 if-elif 구조가 성능 상 이점을 가질 수 있습니다.
# 반면에 여러 개의 연속적인 if 문을 사용하는 경우, 각 if 문은 독립적으로 모든 조건을 평가하게 됩니다.

# Second_tkinter_upbit.py 파일 업그레이드 버전.
# if elif 대신 사용 하는 딕셔너리 매핑 코드.
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
