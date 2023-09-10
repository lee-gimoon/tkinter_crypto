import asyncio
from binance import AsyncClient, BinanceSocketManager

async def handle_btc_socket(ts_btc):
    async with ts_btc as tscm_btc:
        while True:
            res_btc = await tscm_btc.recv()
            print('BTC:', round(float(res_btc['p'])), 'USDT')

async def handle_eth_socket(ts_eth):
    async with ts_eth as tscm_eth:
        while True:
            res_eth = await tscm_eth.recv()
            print('ETH:', round(float(res_eth['p'])), 'USDT')

async def binance_client():
    client = await AsyncClient.create()
    bm = BinanceSocketManager(client, user_timeout=60)
    
    # start trade sockets for BTCUSDT and ETHUSDT
    ts_btc = bm.trade_socket('BTCUSDT')
    ts_eth = bm.trade_socket('ETHUSDT')
    
    # Handle both sockets concurrently
    await asyncio.gather(handle_btc_socket(ts_btc), handle_eth_socket(ts_eth))

# 웹소켓 클라이언트 시작 함수
def start_binance_client():
    asyncio.run(binance_client())

if __name__ == "__main__":
    start_binance_client()

# binance-websocket.py 에서 업그레이드 버전이다.
# asyncio.gather()를 통해 BTC와 ETH 웹소켓을 병렬로 처리한다는 것입니다. 이렇게 함으로써 각 통화의 가격 정보를 동시에, 그리고 각각의 속도에 맞춰서 갱신할 수 있습니다.