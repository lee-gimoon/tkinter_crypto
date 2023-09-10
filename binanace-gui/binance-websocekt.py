import asyncio
from binance import AsyncClient, BinanceSocketManager

async def binance_client():
    client = await AsyncClient.create()
    bm = BinanceSocketManager(client, user_timeout=60)
    
    # start trade sockets for BTCUSDT and ETHUSDT
    ts_btc = bm.trade_socket('BTCUSDT') # 참고로 티커를 하나씩만 지정해야됨. ('BTCUSDT', 'ETHUSDT') 이런식으로는 지원하지 않음.
    ts_eth = bm.trade_socket('ETHUSDT')
    
    # then start receiving messages for both symbols
    async with ts_btc as tscm_btc, ts_eth as tscm_eth: # with a as b 와 with c as d를 한 문장으로 적은것. 참고로 업비트 웹소켓 코드와 비교해보면 웹소켓 연결하는 코드임을 알 수 있음. (ts.btc가 websocket.connetc()라 할 수 있음)
        while True:
            res_btc = await tscm_btc.recv()
            res_eth = await tscm_eth.recv()
            
            print('BTC:', round(float(res_btc['p'])), 'USDT')
            print('ETH:', round(float(res_eth['p'])), 'USDT')

# 웹소켓 클라이언트 시작 함수
def start_binance_client():
    asyncio.run(binance_client())

if __name__ == "__main__":
    start_binance_client()

# https://python-binance.readthedocs.io/en/latest/websockets.html#binancesocketmanager-websocket-usage 참조.