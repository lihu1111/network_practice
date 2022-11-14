from datetime import datetime
from socket import *
from udpmessage import udp_message
import time
from numpy import *
import sys

# 序号从 1 开始递增
seq_no = 1
# ver == 2
ver = 2
# 记录发送时间, 以计算 RTT
send_times = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
# 记录每个报文的 RTT， 方便计算
RTTs = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
# 发送 udp 报文
udp_send = 0
# 接收 udp 报文
udp_receive = 0
# 响应时间差
server_time = ["", ""]
# 从命令行获取参数
server_name = sys.argv[1]
server_port = int(sys.argv[2])


# 发送 udp 报文
def send_message(seq_no, flag, message_content):
    float_time = time.time()
    send_time = time.localtime(float_time)  # 记录发送时间时间戳 float 格式
    message_time = time.strftime('%H:%M:%S', send_time)  # 以时：分：秒构造时间
    request = udp_message(seq_no=seq_no,
                          ver=ver,
                          flag=flag,
                          message_time=message_time,
                          message_content=message_content)
    # 如果是 psh 报文， 则在
    if flag == 1:
        send_times[seq_no] = float_time
    # 发送 udp request 报文
    client_socket.sendto(str(request).encode(), (server_name, server_port))


# 接受报文
def receive():
    response, address = client_socket.recvfrom(1024)  # 接收server的报文字节
    return response.decode()


# 超时重发机制
def time_out_retry():
    try:
        response, address = client_socket.recvfrom(1024)  # 接收server的报文字节
        response_str = response.decode()
        if server_time[0] == '':
            server_time[0] = response_str[4:12].rstrip()
        server_time[1] = response_str[4:12].rstrip()
        return 1, response
    except:
        return 0, 0


# 三次握手
def tree_hand_shake():
    send_message(-2, 0, "syn message")
    print('i am in syn_sent')
    # 收到 syn_ack
    # while True:
    #     count = 0
    #     flag, receive_time, syn_ack = time_out_retry()
    #     if flag == 1:
    #         break  # 收到了syn_ack
    #     else:
    #         if count == 2:
    #             break  # 重传了两次
    #         else:
    #             count += 1  # 重传次数+1
    #             send_message(1, 0, "syn message" + str(count) + "retry")
    # 接手第二次握手
    syn_ack = receive()
    print('i am in established')
    # 第三次握手
    send_message(-1, 0, "ack message")


def four_hand_bye():
    # 客户端第一次发送 fin 报文， 表示我要断开连接
    send_message(seq_no, 2, "1st:fin message to server")
    print("1st:fin message to server")
    # 接受第二次挥手
    ack1_str = receive()
    # 接受第三次报文
    fin_str = receive()
    # 发送第四次报文
    send_message(seq_no + 1, 2, "4th: disconnecting...time_wait....")
    print("4th: disconnecting...time_wait....")
    # 模拟 time_wait
    time.sleep(5)
    client_socket.close()
    print('disconnected')


# 获取socket
client_socket = socket(AF_INET, SOCK_DGRAM)
# 设置超时时间 0.1s
client_socket.settimeout(0.1)
# 三次握手
tree_hand_shake()
# 发 12 个请求
for i in range(12):
    send_message(seq_no=seq_no, flag=1, message_content="sending " + str(seq_no) + " message")
    udp_send += 1
    count = 0
    time.sleep(0.001)  # 避免出现RTT = 0.0, 因为float精度不够

    # 接受 udp response
    while True:
        # 记录每个报文的重传次数
        flag, response_from_server = time_out_retry()
        if flag == 1:
            # 获得响应
            udp_receive += 1
            response_str = response_from_server.decode()
            RTTs[seq_no] = int(round((time.time() - send_times[seq_no]) * 1000))
            print('seq_no: ' + str(seq_no) +
                  ", serverIP:port: " + server_name + ":" + str(server_port) +
                  ', RTT: ' + str(RTTs[seq_no]) + "ms")
            break
        if flag == 0:
            if count == 2:
                print('seq_no: ' + str(seq_no) + '重传已经重传两次')
                break
            else:
                send_message(seq_no=seq_no, flag=1, message_content="message" + str(seq_no) + " retry")
                count += 1
                udp_send += 1
                print('seq_no: ' + str(seq_no) + '重传')
                time.sleep(0.001)  # 避免出现RTT = 0.0, 因为float精度不够
    seq_no += 1
    time.sleep(0.5)  # 输出清晰
lost_packet = 1 - (udp_receive / udp_send)
# 去除第 0 号
send_times.pop(0)
for RTT in RTTs[:]:
    if RTT == 0.0:
        RTTs.remove(RTT)
print("send udp message:{} except syn and syn_ack".format(udp_send))
# print("receive udp message:{} except first ack".format(udp_receive))
print("the rate of the lost udppackets: " + str(lost_packet))
print("maxRTT:{} ms".format(max(RTTs)))
print("minRTT:{} ms".format(min(RTTs)))
print("avgRTT:{} ms".format(mean(RTTs)))
print("standard deviation:{} ms".format(std(RTTs, ddof=1)))
# 转换成时分秒
response_time = datetime.strptime(server_time[1], "%H:%M:%S") - datetime.strptime(server_time[0], "%H:%M:%S")
print("response time:{}".format(response_time))
# 四次挥手
try:
    four_hand_bye()
except timeout:
    print("没有收到server的响应")
    client_socket.close()
