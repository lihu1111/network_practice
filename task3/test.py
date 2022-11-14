import random


def randon_split():
    with open('example.txt', 'r') as f:
        line = f.read()
        length = f.tell()
        # 获取内容长度
        # length = len(line)
        f.close()
        return line, length


# # 打开文件，读取文件大小和文件内容
# def dealFile():
#     # 读取文件内容，文件只有一行
#     with open("example.txt") as readFile:
#         line = readFile.readline()
#     # 获取内容长度
#     totalLength = len(line)
#     return line, totalLength

# line, length = randon_split()
# print(line)
# print(length)
blocks = []
LMin = 50
LMax = 100


# def randon_split():
#     with open('example.txt', 'r') as f:
#         line = f.read()
#         # 获取内容长度
#         length = len(line)
#         N = 0
#         while length:
#             file_block_size = random.randint(LMin, LMax)
#             if length < file_block_size:
#                 file_block_size = length
#             block_content = line[0:file_block_size]
#             blocks.append(block_content)
#             line = line[file_block_size:]  # 更新变数
#             N += 1
#             length -= file_block_size
#     return N


# N = randon_split()
# print(N)
# print(blocks)
str1 = '123'
print(len(str1))
line, length = randon_split()
print(length)
print(line)

print(str(3).ljust(2, '*'))