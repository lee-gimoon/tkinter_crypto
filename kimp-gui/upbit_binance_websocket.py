import websockets
import asyncio
import json
from binance import AsyncClient, BinanceSocketManager

# Upbit code
async def upbit_client():
    uri = "wss://api.upbit.com/websocket/v1"
    async with websockets.connect(uri, ping_interval=60) as websocket:
        subscribe = [{"ticket":"test"}, {"type":"trade", "codes":["KRW-BTC", "KRW-ETH"], "isOnlyRealtime": True}, {"format":"SIMPLE"}]
        subscribe = json.dumps(subscribe)
        await websocket.send(subscribe)

        while True:
            data = await websocket.recv()
            data = json.loads(data)
            print("Upbit BTC or ETH:", data['tp'])

# Binance code
async def handle_btc_socket(ts_btc):
    async with ts_btc as tscm_btc:
        while True:
            res_btc = await tscm_btc.recv()
            print('Binance BTC:', round(float(res_btc['p'])), 'USDT')

async def handle_eth_socket(ts_eth):
    async with ts_eth as tscm_eth:
        while True:
            res_eth = await tscm_eth.recv()
            print('Binance ETH:', round(float(res_eth['p'])), 'USDT')

async def binance_client():
    client = await AsyncClient.create()
    bm = BinanceSocketManager(client, user_timeout=60)
    ts_btc = bm.trade_socket('BTCUSDT')
    ts_eth = bm.trade_socket('ETHUSDT')
    await asyncio.gather(handle_btc_socket(ts_btc), handle_eth_socket(ts_eth))

# Combine both
async def combined_client():
    await asyncio.gather(upbit_client(), binance_client())

if __name__ == "__main__":
    asyncio.run(combined_client())