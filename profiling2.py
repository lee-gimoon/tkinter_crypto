import cProfile

def my_function():
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

if __name__ == "__main__":
    cProfile.run('my_function()', filename='my_function_profile2.txt')

