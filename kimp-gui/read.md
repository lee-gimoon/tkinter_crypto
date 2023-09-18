# kimp-gui 폴더에 있는 파일에 대해 알아보자.

- upbit_binance_websocket.py => 김프 계산에 앞서 업비트와 바이낸스 코인들의 가격이 동시에 잘 콘솔창에 출력하는 확인하는 코드.

- First_kimp.py => 업비트와 바이낸스 코인 1가지의 김프를 게산한 파일.
- Second_kimp.py => 업비트와 바이낸스에서 가져오는 코인 체결 간격, 즉, 갱신되는 시간이 달라 발생하는 문제를 해결. (explation 폴더에서 kimp-problem 파일 참조.)
- Third_kimp.py => 코인 2개 이상의 김프를 계산한 코드. (여기서는 kimp 함수를 비동기 함수로 쓰고 큐도 비동기 큐를 사용.)

- tkinter_kimp_First.py => 업비트와 바이낸스 코인 1가지의 김프를 tkinter gui 화면에 출력. (단, kimp 계산 함수(consumer 함수)를 별도의 스레드에서 실행하기 때문에 비동기 함수가 아닌 일반 함수를 쓰고 일반 큐를 씀)
- tkinter_kimp_Second.py => 업비트와 바이낸스 코인 2가지 이상의 김프를 tkinter gui 화면에 출력.