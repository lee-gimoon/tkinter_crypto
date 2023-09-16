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

last_upbit_data = None
last_binance_data = None

last_upbit_data = None
last_binance_data = None
last_kimp = None

async def kimp_client(upbit_queue, binance_queue):
    global last_upbit_data, last_binance_data, last_kimp
    
    while True:
        updated = False  # 플래그를 이용해 어떤 큐가 업데이트되었는지 확인

        if not upbit_queue.empty():
            last_upbit_data = await upbit_queue.get()
            updated = True

        if not binance_queue.empty():
            last_binance_data = await binance_queue.get()
            updated = True

        if last_upbit_data is not None and last_binance_data is not None and updated:
            binance_krw = last_binance_data * 1330
            kimp = round(((last_upbit_data - binance_krw) / binance_krw) * 100, 2)

            if kimp != last_kimp:  # 이전에 계산한 김치 프리미엄과 다른 경우에만 출력. (중복 방지!!!)
                print(f"Kimp: {kimp} %")
                last_kimp = kimp  # 마지막으로 계산된 김치 프리미엄 값을 저장

        await asyncio.sleep(0.1)  # Sleep to prevent high CPU usage

async def main():
    upbit_queue = asyncio.Queue()
    binance_queue = asyncio.Queue()

    upbit_task = asyncio.create_task(upbit_client(upbit_queue))
    binance_task = asyncio.create_task(binance_client(binance_queue))
    kimp_task = asyncio.create_task(kimp_client(upbit_queue, binance_queue))

    await asyncio.gather(upbit_task, binance_task, kimp_task)

if __name__ == '__main__':
    asyncio.run(main())
