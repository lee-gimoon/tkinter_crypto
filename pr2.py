import time
import queue

start_time = time.time()

# 큐 생성
my_queue = queue.Queue()

# 큐에 데이터 추가
for _ in range(50):
    my_queue.put("data1")
for _ in range(50):
    my_queue.put("data2")
for _ in range(50):
    my_queue.put("data3")

# 이곳에 수십 개의 데이터 추가

# 딕셔너리에 문자열 변수 매핑
data_mapping = {
    "data1": "data1_variable",
    "data2": "data2_variable",
    "data3": "data3_variable",
    # 나머지 데이터에 대한 변수 추가
}

# 변수 정의
data1_variable = "Data 1 Value"
data2_variable = "Data 2 Value"
data3_variable = "Data 3 Value"

# 큐에서 데이터 분류 및 처리
while not my_queue.empty():
    data = my_queue.get()
    
    # 데이터에 대응하는 변수 이름 가져오기
    variable_name = data_mapping.get(data, None)
    
    if variable_name:
        variable_value = globals().get(variable_name, None)
        if variable_value is not None:
            print(f"{data} 처리 완료: {variable_value}")
        else:
            print(f"{data}에 대한 변수가 정의되지 않았습니다.")
    else:
        print("기타 데이터 처리")

# 큐가 비어있을 때까지 모든 데이터가 처리됩니다.

end_time = time.time()

execution_time = end_time - start_time
print(f"실행 시간: {execution_time} 초")