import websockets
import asyncio
import json
from binance import AsyncClient, BinanceSocketManager

async def upbit_client(upbit_queue):
    uri = "wss://api.upbit.com/websocket/v1"
    async with websockets.connect(uri, ping_interval=60) as websocket:
        subscribe = [{"ticket":"test"}, {"type":"ticker", "codes":["KRW-BTC"], "isOnlyRealtime": True}, {"format":"SIMPLE"}]
        subscribe = json.dumps(subscribe)
        await websocket.send(subscribe)

        while True:
            data = await websocket.recv()
            data = json.loads(data)
            data = round(data['tp'])
            upbit_queue.put_nowait(data)

async def binance_client(binance_queue):
    client = await AsyncClient.create()
    bm = BinanceSocketManager(client, user_timeout=60)
    ts = bm.trade_socket("BTCUSDT")
    async with ts as tscm:
        while True:
            data = await tscm.recv()
            data = round(float(data['p']))
            binance_queue.put_nowait(data)

async def kimp_client(upbit_queue, binance_queue):
    while True:
        upbit_data = await upbit_queue.get()
        binance_data = await binance_queue.get() 
        binance_krw = binance_data * 1330
        kimp = round(((upbit_data - binance_krw) / binance_krw) * 100, 2)
        print(f"Kimp: {kimp} %")

async def main():
    upbit_queue = asyncio.Queue()
    binance_queue = asyncio.Queue()

    upbit_task = asyncio.create_task(upbit_client(upbit_queue))
    binance_task = asyncio.create_task(binance_client(binance_queue))
    kimp_task = asyncio.create_task(kimp_client(upbit_queue, binance_queue))

    await asyncio.gather(upbit_task, binance_task, kimp_task)

if __name__ == '__main__':
    asyncio.run(main())
