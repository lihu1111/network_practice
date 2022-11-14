# import time
# from random import randint
#
# time1 = time.strftime('%H:%M:%S', time.localtime(time.time()))
# print(time1)
#
# time0 = time.time()
# # time.sleep(0.0000000001)
# print(time.time() - time0)


# 实现字符串逆序
def reverse(obj):
    string = []
    for x in obj:
        string.append(x)
    string.reverse()
    return "".join(string)


request = 'abc 1234'
print(reverse(request))
