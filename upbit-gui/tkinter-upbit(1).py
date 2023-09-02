# jit 컴파일러를 적용하려면 Numba 라이브러리를 사용해야 합니다. 그러나 이 코드에서는 Numba로 컴파일하기 어려운 부분이 있을 수 있습니다. 

# Numba는 숫자 계산과 관련된 함수를 주로 최적화하는 데 사용되지만, tkinter 및 웹소켓과 같은 외부 라이브러리와의 상호 작용이 포함되어 있으므로 Numba로 컴파일하는 것은 적절하지 않을 수 있습니다.

# Numba로 컴파일하려면 아래와 같이 @jit 데코레이터를 사용하여 함수를 명시적으로 JIT 컴파일할 수 있습니다. 다음은 format_number 함수를 JIT 컴파일하는 예시입니다: