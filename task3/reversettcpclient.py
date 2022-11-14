import random
from socket import *
import sys

initialization = 1
reverseRequest = 3
# 指定ip、port
server_name = sys.argv[1]
server_port = int(sys.argv[2])
LMin = int(sys.argv[3])
LMax = int(sys.argv[4])
# 建立连接
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((server_name, server_port))
# 块
request_datas = []


# 划分不同块, 返回块数
def random_split():
    with open('example.txt', 'r') as f:
        line = f.read()
        # 获取内容长度
        length = len(line)
        N = 0
        while length:
            # 在[LMin, LMax] 中随机选择块的大小
            block_size = random.randint(LMin, LMax)
            # 最后一块小于 block_size, 则覆盖block_size
            if length < block_size:
                block_size = length
            # 取块内容
            block_content = line[0:block_size]
            request_datas.append(block_content)
            line = line[block_size:]  # 更新内容
            length -= block_size  # 文件长度更新
            N += 1  # 块数+1
    return N


def init_connection(N):
    # 构造初始化语句
    request_data = str(initialization).ljust(2, ' ') + str(N).ljust(4, ' ')
    client_socket.send(request_data.encode())
    # 接受 agree
    client_socket.recv(1024)


# 获得块数
N = random_split()
# print(N)
# print(request_datas)
# 初始化
init_connection(N)
answer = ''
count = 0
for request_data in request_datas:
    count += 1
    # 构造reverse——reqeust
    data = str(reverseRequest).ljust(2, ' ') + str(len(request_data)).ljust(4, ' ') + request_data  # ljust 右边补空格
    client_socket.send(data.encode())
    reverse_answer = client_socket.recv(1024).decode()
    # print(reverse_answer)
    answer += reverse_answer[6:]
    print(str(count) + ": " + reverse_answer[6:])
with open('answer.txt', 'w') as f:
    f.write(answer)
client_socket.close()
