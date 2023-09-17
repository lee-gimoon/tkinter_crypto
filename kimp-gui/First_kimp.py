# 1가지의 코인의 김프를 계산해보자.
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
            data = data['tp']
            upbit_queue.put_nowait(data)

async def binance_client(binance_queue):
    client = await AsyncClient.create()
    bm = BinanceSocketManager(client, user_timeout=60)
    ts = bm.trade_socket("BTCUSDT")
    async with ts as tscm:
        while True:
            data = await tscm.recv()
            data = float(data['p']) # data['p']는 문자열이기 때문에 float로 바꿔주기.
            binance_queue.put_nowait(data)

async def kimp_client(upbit_queue, binance_queue):
    while True:
        upbit_data = await upbit_queue.get() # 김프에서는 await으로 인한 딜레이 문제를 해결 위해 tkinter_binance_Final.py 파일에서의 코드처럼 gather()를 사용하고 컨슈머를 코인마다 각각 만드는 방법을 쓰지 못한다.
        binance_data = await binance_queue.get() # 왜냐하면 한 함수안에서 업비트, 바이낸스 웹소켓 데이터를 계산해서 gui에 출력해야하기 때문에. 따라서 Second_kimp 파일처럼 if not을 이용.

        upbit_data = round(upbit_data) # 티커가 비트코인이기 때문에 round로 정수만 출력.
        binance_data = round(binance_data) # 티커가 비트코인이기 때문에 round로 정수만 출력.
        binance_krw = binance_data * 1330
        kimp = round(((upbit_data - binance_krw) / binance_krw) * 100, 2)
        print(f"Kimp: {kimp} %")

async def main():
    upbit_queue = asyncio.Queue()
    binance_queue = asyncio.Queue()

    # create_task() 로 코루틴을 래핑하여 병렬로 실행. 진짜 병렬이 아닌 동시에 실행. 즉, 동시성.
    upbit_task = asyncio.create_task(upbit_client(upbit_queue)) 
    binance_task = asyncio.create_task(binance_client(binance_queue))
    kimp_task = asyncio.create_task(kimp_client(upbit_queue, binance_queue))

    await asyncio.gather(upbit_task, binance_task, kimp_task)

if __name__ == '__main__':
    asyncio.run(main())
