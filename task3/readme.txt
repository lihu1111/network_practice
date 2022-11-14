程序说明
运行环境 python3.10
配置环境 client:  random 模块, sys 模块, socket模块
        server:  socket 模块
        OS: CentOS 7
        host: 192.168.182.100(host: redis001)
        port: 8080


udpclient.py
设置全局变量记录程序状态：
# 记录块的内容
request_datas = []

关键点:
# 服务器设置为非阻塞， 能同时处理2个以上的client请求
server_socket.setblocking(False) # 将server_socket

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
    request_data = str(initialization).ljust(2, ' ') + str(N).ljust(4, ' ') # 填充空格
    client_socket.send(request_data.encode())
    # 接受 agree
    client_socket.recv(1024)

udpserver.py
设置server_socket为非阻塞server_socket.setblocking(False) # 将server_socket
对于每一个到来的client_socket， 也将他们设置为非阻塞