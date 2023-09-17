# 단, 1개의 코인의 가격을 출력해보자.
import asyncio
from binance import AsyncClient, BinanceSocketManager

async def binance_client():
    client = await AsyncClient.create()
    bm = BinanceSocketManager(client, user_timeout=60)

    ts_btc = bm.trade_socket('BTCUSDT') 

    async with ts_btc as tscm_btc:
        while True:
            data = await tscm_btc.recv()
            print('BTC:', round(float(data['p'])), 'USDT')
            # print(type(data)) # <class 'dict'>
            # print(type(data['p'])) # <class 'str'>
            # print(type(float(data['p']))) # <class 'float'>
            # print(type(round(float(data['p'])))) # <class 'int'>

# 웹소켓 클라이언트 시작 함수
def start_binance_client():
    asyncio.run(binance_client())

if __name__ == "__main__":
    start_binance_client()

# https://python-binance.readthedocs.io/en/latest/websockets.html#binancesocketmanager-websocket-usage 참조.