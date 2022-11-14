import time
from socket import *
# socket的默认情况下是阻塞模式：socket.accept()方法在没有接受到连接之前不能处理已经建立连接的其他操作，
# 以及在recv()方法或者其他接受数据的方法时候都是阻塞的，如果没有接受到数据就会一直处于阻塞状态，
# 来等待接受数据，这种情况只有通过开启新的进程或者线程来解决来自不同客户端的连接请求或者接受数据；
# socket可以支持非阻塞的模式；可以使用以下两种方法来设置socket的非阻塞模式：# 设置套接字为阻塞或非阻塞模式：如果 flag 为 false，则将套接字设置为非阻塞，否则设置为阻塞。
# # socket.setblocking(flag)
# # 如果value赋为 0，则套接字将处于非阻塞模式。如果指定为 None，则套接字将处于阻塞模式。
# # socket.settimeout(value)
# # 阻塞
# sock.setblocking(True)
# sock.settimeout(None)
# # 非阻塞
# sock.setblocking(False)
# sock.settimeout(0.0)
# 在非阻塞模式下可以实现在单线程模式下实现与多个客户端连接的交互：


# 实现字符串逆序
def reverse(obj):
    string = []
    for x in obj:
        string.append(x)
    string.reverse()
    return "".join(string)


#
agree = 2
#
reverseAnswer = 4


server_name = '192.168.182.100'
server_port = 8080
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((server_name, server_port))
server_socket.listen(128)
server_socket.setblocking(False)
client_socket_list = []
while True:
    try:
        client_socket, client_socket_addr = server_socket.accept()
    # 因为这里是非阻塞 所以当没有连接请求时这里会产生异常
    except Exception as Ex:
        pass
    else:
        # 设置新的客户端为非阻塞
        client_socket.setblocking(False)
        client_socket_list.append(client_socket)
    for cli_socket in client_socket_list:
        try:
            data = cli_socket.recv(1024)
        # 这里同样 因为是非阻塞 会来看是否有数据 如果没有会产生异常
        except Exception as Ex:
            # 没有数据
            pass
        else:
            #  这里没有异常 这里有两种情况 一种是客户端使用close()关闭链接但是没有数据  一种是有数据
            if data:  # 有数据
                time.sleep(1)
                # 请求
                request = data.decode()
                # print(request)
                # 字符串型
                request_type = request[0:2].rstrip()
                # int 型
                request_type_int = int(request_type)
                # 构造回送数据
                answer = ''
                if request_type_int == 1:  # 如果是init
                    # print("init")
                    cli_socket.send(str(agree).encode())
                else:  # 如果是request
                    # 构造answer。
                    answer = (str(reverseAnswer).ljust(2) + request[2:6] + reverse(request[6:])).encode()
                    # print('answer=' + answer.decode())
                    cli_socket.send(answer)

            else:
                # 无数据
                client_socket_list.remove(cli_socket)
                cli_socket.close()
