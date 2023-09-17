# upbit gui 폴더에 있는 파일에 대해 설명.

- upbit-websocekt.py => 업비트 웹소켓을 이용해 코인 가격 출력.

- First_tkiner_upbit.py => 업비트 웹소켓에서 받아온 코인 가격을 tkinter gui 화면에 출력. (단, 코인1개만 출력하는 코드임.)
- Second_tkinter_upbit.py => First_tkinter_upbit.py 와 동일하지만 코인 2개이상을 출력하는 코드임.
- Third_tkinter_upbit.py => Second_tkinter_upbit.py 에서 최적화한 파일. if-else 문을 사용하는 대신 딕셔너리 매핑으로 속도를 올림.

- Final_tkinter_upbit.py => 업비트 웹소켓에서 받아온 여러개의 코인들의 가격을 tkinter gui 화면에 출력. 위 파일들의 최적화를 완료한 파일.