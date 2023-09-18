# 코인 2개 이상의 김프를 계산해보자.
import websockets
import asyncio
import json
from binance import AsyncClient, BinanceSocketManager

async def upbit_client(upbit_btc_queue, upbit_neo_queue):
    uri = "wss://api.upbit.com/websocket/v1"
    async with websockets.connect(uri, ping_interval=60) as websocket:
        subscribe = [{"ticket":"test"}, 
                     {"type":"ticker", "codes":["KRW-BTC", "KRW-NEO"], "isOnlyRealtime": True},
                     {"format":"SIMPLE"}]
        subscribe = json.dumps(subscribe)
        await websocket.send(subscribe)

        while True:
            data = await websocket.recv()
            data = json.loads(data)
            price = round(data['tp'])
            if data['cd'] == 'KRW-BTC':
                upbit_btc_queue.put_nowait(price)
            elif data['cd'] == 'KRW-NEO':
                upbit_neo_queue.put_nowait(price)

import logging

logging.basicConfig(level=logging.INFO)

async def handle_socket(ts, q, coin_type):
    try:
        async with ts as tscm:
            while True:
                res = await tscm.recv()
                if coin_type == 'BTC': # 조건1(BTC)이 참일 때 실행될 코드
                    # Handle BTC case
                    await q.put(round(float(res['p'])))
                elif coin_type == 'NEO': # 조건1이 거짓이고 조건2(NEO)가 참일 때 실행될 코드
                    # Handle NEO case
                    await q.put(float(res['p']))
    except Exception as e:
        logging.error(f"Error in handle_socket: {e}")

async def binance_client(binance_btc_queue, binance_neo_queue):
    client = await AsyncClient.create()
    bm = BinanceSocketManager(client, user_timeout=60)

    ts_btc = bm.trade_socket('BTCUSDT')
    ts_neo = bm.trade_socket('NEOUSDT')

    await asyncio.gather(
        handle_socket(ts_btc, binance_btc_queue, 'BTC'),
        handle_socket(ts_neo, binance_neo_queue, 'NEO'),
    )
            

async def btc_kimp_client(upbit_btc_queue, binance_btc_queue):
    last_upbit_data = None
    last_binance_data = None
    last_kimp = None
    
    while True:
        updated = False

        if not upbit_btc_queue.empty():
            last_upbit_data = await upbit_btc_queue.get()
            updated = True

        if not binance_btc_queue.empty():
            last_binance_data = await binance_btc_queue.get()
            updated = True

        if last_upbit_data is not None and last_binance_data is not None and updated: # 이 조건문은 세 가지 조건이 모두 참일 때만 코드 블록 내의 로직을 실행합니다.
            binance_krw = last_binance_data * 1330  # Convert USD to KRW
            kimp = round(((last_upbit_data - binance_krw) / binance_krw) * 100, 2)

            if kimp != last_kimp:
                print(f"BTC Kimp: {kimp} %")
                last_kimp = kimp
                
        await asyncio.sleep(0.1)


async def neo_kimp_client(upbit_neo_queue, binance_neo_queue): 
    last_upbit_neo_data = None # 마지막으로 알려진 데이터 사용(if not). (실시간 시스템에서 사용하는 패턴.)
    last_binance_neo_data = None
    last_kimp_neo = None
    
    while True:
        updated = False

        if not upbit_neo_queue.empty(): # 업비트 네오 큐가 비어있지 않으면 가격을 가져와 업데이트.
            last_upbit_neo_data = await upbit_neo_queue.get()
            updated = True

        if not binance_neo_queue.empty(): # 바이낸스 네오 큐가 비어있지 않으면 가격을 가져와 업데이트.
            last_binance_neo_data = await binance_neo_queue.get()
            updated = True

        if last_upbit_neo_data is not None and last_binance_neo_data is not None and updated: # 이 조건문은 세 가지 조건이 모두 참일 때만 코드 블록 내의 로직을 실행합니다.
            binance_neo_krw = last_binance_neo_data * 1330  # Convert USD to KRW
            kimp_neo = round(((last_upbit_neo_data - binance_neo_krw) / binance_neo_krw) * 100, 2)

            if kimp_neo != last_kimp_neo:
                print(f"NEO Kimp: {kimp_neo} %")
                last_kimp_neo = kimp_neo
                
        await asyncio.sleep(0.1)


async def main():
    upbit_btc_queue = asyncio.Queue()
    binance_btc_queue = asyncio.Queue()
    upbit_neo_queue = asyncio.Queue()
    binance_neo_queue = asyncio.Queue()

    upbit_task = asyncio.create_task(upbit_client(upbit_btc_queue, upbit_neo_queue))
    binance_task = asyncio.create_task(binance_client(binance_btc_queue, binance_neo_queue))
    btc_kimp_task = asyncio.create_task(btc_kimp_client(upbit_btc_queue, binance_btc_queue))
    neo_kimp_task = asyncio.create_task(neo_kimp_client(upbit_neo_queue, binance_neo_queue))

    await asyncio.gather(upbit_task, binance_task, btc_kimp_task, neo_kimp_task)


if __name__ == '__main__':
    asyncio.run(main())
