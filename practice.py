import json
import tkinter as tk
import websockets
from queue import Queue
import threading
import sys
import asyncio

class CryptoInputField:
    def __init__(self, root, label_text, y):
        self.value = tk.StringVar()
        self.label = tk.Label(root, text=label_text)
        self.label.grid(row=y, column=0, sticky='w')
        self.entry = tk.Entry(root, textvariable=self.value)
        self.entry.grid(row=y, column=1)

class CryptoValueTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Crypto Value Tracker")

        crypto_info = [
            ("Bitcoin", "KRW-BTC"),
            ("Ethereum", "KRW-ETH"),
            ("NEO", "KRW-NEO")
        ]

        self.crypto_values = {}
        for index, (label, code) in enumerate(crypto_info):
            y = 2 + index
            field = CryptoInputField(root, f"{label}:", y)
            self.crypto_values[code] = field.value

        self.q = Queue()
        self.upbit_thread = threading.Thread(target=self.start_upbit_client)
        self.upbit_thread.daemon = True
        self.upbit_thread.start()

        self.consumer_thread = threading.Thread(target=self.consumer)
        self.consumer_thread.daemon = True
        self.consumer_thread.start()

        root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def start_upbit_client(self):
        asyncio.run(self.upbit_client(self.q))

    async def upbit_client(self, q):
        uri = "wss://api.upbit.com/websocket/v1"
        subscribe = [{"ticket": "test"}, {"type": "trade", "codes": ["KRW-BTC", "KRW-ETH", "KRW-NEO"], "isOnlyRealtime": True}, {"format": "SIMPLE"}]
        subscribe_data = json.dumps(subscribe)

        async with websockets.connect(uri, ping_interval=60) as websocket:
            await websocket.send(subscribe_data)

            while True:
                data = await websocket.recv()
                q.put(json.loads(data))

    def consumer(self):
        while True:
            data = self.q.get()
            self.update_gui(data)

    def update_gui(self, data):
        code = data['cd']
        value = int(data.get('tp'))

        if code in self.crypto_values:
            self.crypto_values[code].set(format(value, ",d"))

    def on_closing(self):
        sys.exit(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoValueTrackerApp(root)
    root.mainloop()
