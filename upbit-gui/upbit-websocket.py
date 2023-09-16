# 업비트 웹소켓.
import websockets
import asyncio
import json

async def upbit_client():
    uri = "wss://api.upbit.com/websocket/v1"

    # connect() can be used as a asynchronous context manager.
    async with websockets.connect(uri, ping_interval=60) as websocket: # ping_interval: 수신 끊기는 것을 예방. 60초 간격으로 신호 보냄.
        print(type(websocket)) # WebSocketClientProtocol provides recv() and send() coroutines for receiving and sending messages.
        print(websocket)

        # websockets.connect의 async def __aenter__(self) 메서드 시작됨.

        subscribe = [{"ticket":"test"}, {"type":"trade", "codes":["KRW-BTC", "KRW-ETH"], "isOnlyRealtime": True}, {"format":"SIMPLE"}]
        
        subscribe = json.dumps(subscribe) # 인코딩 (Python 객체를 JSON 문자열로 변환)
        await websocket.send(subscribe) # # websocket.send() 는 코루틴임.

        while True:
            data = await websocket.recv() # websocket.recv() 는 코루틴임. websocket.recv() 코루틴의 return 값이 data변수로 들어감.
            data = json.loads(data) # 디코딩 (JSON 문자열을 Python 객체로 변환)
            print(data)
            # print(type(data)) # <class 'dict'>
            # print(type(data['tp'])) # <class 'float'>
            # print(data['tp'])
            

        #  websockets.connect의 async def __aexit__(self) 메서드 시작됨.

if __name__ == "__main__":
    asyncio.run(upbit_client())

# JSON(JavaScript Object Notation).
# json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}]) => output: '["foo", {"bar": ["baz", null, 1.0, 2]}]'
# json.loads('["foo", {"bar":["baz", null, 1.0, 2]}]') => output: ['foo', {'bar': ['baz', None, 1.0, 2]}]


# https://websockets.readthedocs.io/en/stable/reference/asyncio/client.html 참조.