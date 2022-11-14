# 以字符串模拟
class udp_message:

    def __init__(self, **kwargs):
        self.seq_no = kwargs.get('seq_no')  # 2B
        self.ver = kwargs.get('ver')  # 1B
        self.flag = kwargs.get('flag')  # 1B flag = 0 表示 syn  flag = 1 表示 psh flag = 2 表示 fin
        self.message_time = kwargs.get('message_time')  # 8Bytes
        self.message_content = kwargs.get('message_content')  # 191B

    # 重写str方法
    def __str__(self):
        seq_no = str(self.seq_no)
        if len(seq_no) < 2:
            seq_no = seq_no.ljust(2)
        else:
            seq_no = seq_no[0:2]
        ver = str(self.ver)
        if len(ver) < 1:
            ver = ver.ljust(1)
        else:
            ver = ver[0:1]
        flag = str(self.flag)
        if len(flag) < 1:
            flag = flag.ljust(1)
        else:
            flag = flag[0:1]
        if len(self.message_time) < 8:
            message_time = self.message_time.ljust(8)
        else:
            message_time = self.message_time[0:8]

        if len(self.message_content) < 191:
            message_content = self.message_content.ljust(191)
        else:
            message_content = self.message_content[0:191]

        head = seq_no + ver + flag + message_time
        return head + message_content

