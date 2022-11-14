程序说明
运行环境 python3.10
配置环境 client: numpy 模块, time 模块, datetime 模块, sys 模块, socket 模块
        server: random 模块, socket 模块
        OS: CentOS 7
        host: 192.168.182.100(host: redis001)
        port: 8080

udpmessage.py
编写报文类，报文结构安排如下表所示
seq_no(2B)	ver(1B)	flag(1B)
message_time(8B)
message_content(191B)
报文类包含两种构造函数和str方法：
def __init__(self, **kwargs)	# 使用赋值的方法初始化
def __str__(self)	# 将类封装成字符串


udpclient.py
设置全局变量记录程序状态：
send_times 列表，表示客户端的发送报文的时间
RTTs 列表，表示每个报文的RTT
response_time 列表，记录了服务器第一次响应和最后一次响应的时间
udp_send 记录发送的报文
udp_receive 记录收到的报文
关键点:
设置超时时间 0.1s
client_socket.settimeout(0.1)
超时重发机制（返回 flag 为是否收到， response)
def time_out_retry():
    try:
        response, address = client_socket.recvfrom(2048)  # 接收server的报文字节
        response_str = response.decode()
        if server_time[0] == '':
            server_time[0] = response_str[4:12].rstrip()
        server_time[1] = response_str[4:12].rstrip()
        return 1, response
    except:
        return 0, 0
三次握手
客户端服务端此时所有报文的flag=0
四次挥手
客户端服务端此时所有报文的flag=2

udpserver.py
对于每个 response 如果筛子 > 3, 则发送 response 报文, 否则不发送, 对于客户端则为报文被丢弃, 要重发报文