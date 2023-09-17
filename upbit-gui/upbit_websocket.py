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

        subscribe = [{"ticket":"test"}, {"type":"trade", "codes":["KRW-NEO"], "isOnlyRealtime": True}, {"format":"SIMPLE"}]
        
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

# NEO코인 같이 체결이 오랫동안 안될시 웹소켓 연결이 끊길 수 있다.
# websockets.exceptions.ConnectionClosedError: no close frame received or sent 오류는 웹소켓 연결이 예기치 않게 닫혔을 때 발생합니다. 
# 다음은 이 문제를 해결할 수 있는 몇 가지 방법입니다:
# Reconnection Mechanism: 연결이 끊기면 자동으로 재연결하도록 코드를 수정할 수 있습니다.
# Keep-Alive Messages: 서버나 클라이언트 측에서 정기적인 keep-alive 메시지를 보내 연결을 유지하도록 할 수 있습니다.