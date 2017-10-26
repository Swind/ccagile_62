import socket


class AdbSocket:
    def __init__(self, host="127.0.0.1", port=5037):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def encode_length(self, length):
        return "{0:04X}".format(length)

    def encode_cmd(self, cmd):
        b_cmd = cmd.encode('utf-8')
        b_length = self.encode_length(len(b_cmd)).encode('utf-8')
        return b"".join([b_length, b_cmd])

    def send(self, cmd):
        adb_cmd = self.encode_cmd(cmd)
        print(adb_cmd)
        self.socket.send(adb_cmd)

        result = self.socket.recv(4).decode('utf-8')
        print(result)

    def recv(self):
        length = int(self.socket.recv(4).decode('utf-8'), 16)
        result = self.socket.recv(length)

        return result.decode('utf-8')


s = AdbSocket()
s.send("host:devices")
print(s.recv())
