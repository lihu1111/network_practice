import time
from random import randint
from socket import *
from udpmessage import udp_message


# 发送 udp 报文
def send_message(seq_no, flag, message_content):
    response = udp_message(seq_no=seq_no,
                           ver=ver,
                           flag=flag,
                           message_time=time.strftime('%H:%M:%S', time.localtime(time.time())),
                           message_content=message_content)
    # 发送 response
    server_socket.sendto(str(response).encode(), client_address)


# 接受报文
def receive():
    request, address = server_socket.recvfrom(1024)  # 接收server的报文字节
    return request


def tree_hand_shake():
    # 接收 syn
    syn, client_address = server_socket.recvfrom(1024)
    syn_str = syn.decode()
    print("i am in syn_receive")
    # 发送 syn_ack
    syn_ack = udp_message(seq_no=int(syn_str[0:2]),
                          ver=ver,
                          flag=int(syn_str[3:4]),
                          message_time=time.strftime('%H:%M:%S', time.localtime(time.time())),
                          message_content="syn_ack message coming")
    server_socket.sendto(str(syn_ack).encode(), client_address)
    # 收到第三次握手
    ack = receive()
    print('established')


def four_hand_bye(seq_no):
    # 发送 ack 都以2为标志
    send_message(seq_no, 2, "2nd: your fin i have received")
    print("2nd: your fin i have received")
    # 发送 fin
    send_message(seq_no + 1, 2, "3rd: fin message to client")
    print("3rd: fin message to client")
    # 接受 ack
    ack = receive()
    # time.sleep(3)
    # server_socket.close()
    print('disconnected')


ver = 2
server_name = '192.168.182.100'
# server_name = 'localhost'
server_port = 8080
# 构造socket
server_socket = socket(AF_INET, SOCK_DGRAM)
# 绑定
server_socket.bind((server_name, server_port))
print('The server is already!')
# 三次握手
tree_hand_shake()
while 1:
    # 接受客户端消息
    try:
        request, client_address = server_socket.recvfrom(1024)
        # 将 udp message 对象转换成 str， 得到 request
        request_str = request.decode()
        # print(request_str)
        request_seq_no = request_str[0:2].rstrip()
        # flag
        request_flag = int(request_str[3:4].rstrip())
        # 模拟筛子 <= 3丢弃 > 3 响应
        die = randint(1, 6)
        seq_no = int(request_seq_no)
        # print(request_flag)
        if request_flag == 2:
            # 四次挥手
            send_message(seq_no, 2, "2nd: your fin i have received")
            print("2nd: your fin i have received")
            # 发送 fin
            send_message(seq_no + 1, 2, "3rd: fin message to client")
            print("3rd: fin message to client")
            # 接受 ack
            ack = receive()
            # time.sleep(3)
            server_socket.close()
            print('disconnected')
            break
        if die > 3:
            # 构造 response
            response = udp_message(seq_no=int(request_seq_no),
                                   ver=ver,
                                   flag=request_flag,
                                   message_time=time.strftime('%H:%M:%S', time.localtime(time.time())),
                                   message_content='reply for reqeust' + request_seq_no)
            # 发送 response
            server_socket.sendto(str(response).encode(), client_address)
    except:
        break
