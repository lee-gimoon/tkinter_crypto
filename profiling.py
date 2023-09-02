import cProfile

def my_function():
    # 프로파일링하려는 코드
    import json
    import tkinter as tk
    import websockets
    from queue import Queue
    import threading
    import sys
    import asyncio

    async def upbit_client(q):
        uri = "wss://api.upbit.com/websocket/v1"
        subscribe = [{"ticket": "test"}, {"type": "trade", "codes": ["KRW-BTC", "KRW-ETH", "KRW-NEO", "KRW-BCH", "KRW-EOS", "KRW-STX", "KRW-SOL", "KRW-TRX", "KRW-WAVES", "KRW-MATIC", "KRW-ADA"], "isOnlyRealtime": True}, {"format": "SIMPLE"}]
        subscribe_data = json.dumps(subscribe)

        async with websockets.connect(uri, ping_interval=60) as websocket:
            await websocket.send(subscribe_data)

            while True:
                data = await websocket.recv()
                q.put(json.loads(data))

    def start_upbit_client(q):
        asyncio.run(upbit_client(q))

    def consumer(q):
        while True:
            data = q.get()
            update_gui(data)

    def update_gui(data):
        code = data['cd']
        value = int(data.get('tp'))

        if code == 'KRW-BTC':
            btc_value.set(format(value, ",d"))
        elif code == 'KRW-ETH':
            eth_value.set(format(value, ",d"))
        elif code == 'KRW-NEO':
            neo_value.set(format(value, ",d"))
        elif code == 'KRW-BCH':
            bch_value.set(format(value, ",d"))
        elif code == 'KRW-EOS':
            eos_value.set(format(value, ",d"))
        elif code == 'KRW-STX':  # 추가: 스택스(STX)
            stx_value.set(format(value, ",d"))
        elif code == 'KRW-SOL':  # 추가: 솔라나(SOL)
            sol_value.set(format(value, ",d"))
        elif code == 'KRW-TRX':  # 추가: 트론(TRX)
            trx_value.set(format(value, ",d"))
        elif code == 'KRW-WAVES':  # 추가: 웨이브(WAVES)
            waves_value.set(format(value, ",d"))
        elif code == 'KRW-MATIC':  # 추가: 폴리곤(MATIC)
            matic_value.set(format(value, ",d"))
        elif code == 'KRW-ADA':    # 추가: 에이다(ADA)
            ada_value.set(format(value, ",d"))


    def on_closing():
        sys.exit(0)

    root = tk.Tk()
    root.title("Upbit Websocket")
    root.geometry("800x500")
    root.protocol("WM_DELETE_WINDOW", on_closing)

    btc_value = tk.StringVar()
    btc_label = tk.Label(root, text="Bitcoin:")
    btc_label.place(x=10, y=10)
    btc_entry = tk.Entry(root, textvariable=btc_value)
    btc_entry.place(x=100, y=10)

    eth_value = tk.StringVar()
    eth_label = tk.Label(root, text="Ethereum:")
    eth_label.place(x=10, y=40)
    eth_entry = tk.Entry(root, textvariable=eth_value)
    eth_entry.place(x=100, y=40)

    neo_value = tk.StringVar()
    neo_label = tk.Label(root, text="NEO:")
    neo_label.place(x=10, y=70)
    neo_entry = tk.Entry(root, textvariable=neo_value)
    neo_entry.place(x=100, y=70)

    bch_value = tk.StringVar()
    bch_label = tk.Label(root, text="Bitcoin Cash:")
    bch_label.place(x=10, y=100)
    bch_entry = tk.Entry(root, textvariable=bch_value)
    bch_entry.place(x=100, y=100)

    eos_value = tk.StringVar()
    eos_label = tk.Label(root, text="EOS:")
    eos_label.place(x=10, y=130)
    eos_entry = tk.Entry(root, textvariable=eos_value)
    eos_entry.place(x=100, y=130)

    stx_value = tk.StringVar()
    stx_label = tk.Label(root, text="STX:")
    stx_label.place(x=10, y=160)
    stx_entry = tk.Entry(root, textvariable=stx_value)
    stx_entry.place(x=100, y=160)

    sol_value = tk.StringVar()
    sol_label = tk.Label(root, text="SOL:")
    sol_label.place(x=10, y=190)
    sol_entry = tk.Entry(root, textvariable=sol_value)
    sol_entry.place(x=100, y=190)

    trx_value = tk.StringVar()
    trx_label = tk.Label(root, text="TRX:")
    trx_label.place(x=10, y=220)
    trx_entry = tk.Entry(root, textvariable=trx_value)
    trx_entry.place(x=100, y=220)

    waves_value = tk.StringVar()
    waves_label = tk.Label(root, text="WAVES:")
    waves_label.place(x=10, y=250)
    waves_entry = tk.Entry(root, textvariable=waves_value)
    waves_entry.place(x=100, y=250)

    matic_value = tk.StringVar()
    matic_label = tk.Label(root, text="MATIC:")
    matic_label.place(x=10, y=280)
    matic_entry = tk.Entry(root, textvariable=matic_value)
    matic_entry.place(x=100, y=280)

    ada_value = tk.StringVar()
    ada_label = tk.Label(root, text="ADA:")
    ada_label.place(x=10, y=310)
    ada_entry = tk.Entry(root, textvariable=ada_value)
    ada_entry.place(x=100, y=310)


    q = Queue()

    upbit_thread = threading.Thread(target=start_upbit_client, args=(q,))
    upbit_thread.daemon = True
    upbit_thread.start()

    consumer_thread = threading.Thread(target=consumer, args=(q,))
    consumer_thread.daemon = True
    consumer_thread.start()

    root.mainloop()


if __name__ == "__main__":
    cProfile.run('my_function()', filename='my_function_profile.txt')