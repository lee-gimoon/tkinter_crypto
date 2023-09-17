# First_kimp.py 파일의 코드를 업그레이드한 버전. (마지막으로 알려진 데이터 사용)
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
            last_upbit_data = await upbit_queue.get() # asyncio.Queue() 이기 때문에 await을 붙여야함.
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

# asyncio.create_task()를 사용하면 여러 코루틴을 쉽고 효율적으로 병렬로 실행할 수 있습니다. 
# 이를 통해 upbit_client는 Upbit 데이터를, binance_client는 Binance 데이터를, 그리고 kimp_client는 두 데이터를 비교하여 "김치 프리미엄"을 계산합니다. 
# 이 모든 작업이 동시에 이루어져야 하기 때문에 create_task를 사용하여 각 코루틴을 병렬 작업으로 만드는 것이 유용합니다. 실제로는 진짜 병렬 작업이 아닌 동시성 작업이다.