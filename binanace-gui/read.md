# binance gui 폴더에 있는 파일에 대해 설명.

- First_binance_websocket.py => 바이낸스 웹소켓에서 코인 데이터를 받아와 출력하는 파일. (단, 1개의 코인만 출력하는 파일.)
- Second_binance_websocket.py => 바이낸스 웹소켓에서 2개이상의 코인 데이터를 받아와 출력하는 파일. (2개 이상의 코인을 출력하나 출력에 딜레이가 생기는 코드)
- Tecond_binance_websocket.py => 바이낸스 웹소켓에서 2개이상의 코인 데이터를 받아와 출력하는 파일로 Seocnd_binance_websocket.py을 업그레이드함. (2개 이상의 코인을 출력함에 있어서 딜레이가 생기는 부분을 해결한 코드)

- tkinter_binance_First.py => 바이낸스 웹소켓에서 코인데이터을 받아와 tkinter gui 화면에 출력하는 파일. (단, 1개의 코인만을 받아와서 출력하는 파일.)
- tkinter_binance_Second.py => 2개이상의 코인데이터를 받아와 tkinter gui 화면에 출력하는 파일. (Second_binance_websocket.py 과 같은 방식으로 코드를 짜 같은 문제가 발생함. 딜레이가 gui 화면에 확연히 보임.)
- tkinter_binacne_Final.py => tkinter_binance_Second.py의 문제를 해결한 코드. (2개 이상의 코인을 tkinter gui 화면에 출력에 있어서 가장 이상적인 코드라 생각함.)