import socket


class AdbSocket:
    def __init__(self, host="127.0.0.1", port=5037):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect((self.host, self.port))

    def close(self):
        self.socket.close()

    def encode_length(self, length):
        return "{0:04X}".format(length)

    def encode_cmd(self, cmd):
        b_cmd = cmd.encode('utf-8')
        b_length = self.encode_length(len(b_cmd)).encode('utf-8')
        return b"".join([b_length, b_cmd])

    def send(self, cmd):
        adb_cmd = self.encode_cmd(cmd)
        self.socket.send(adb_cmd)

        result = self.socket.recv(4).decode('utf-8')

    def recv(self):
        length = int(self.socket.recv(4).decode('utf-8'), 16)
        result = self.socket.recv(length)

        return result.decode('utf-8')

    def read(self):
        data = bytearray()

        while True:
            recv = self.socket.recv(4096)
            if not recv:
                break;

            data += recv

        return data


class AdbDevice:
    def __init__(self, serialno, host="127.0.0.1", port=5037):
        self.serialno = serialno
        self.host = host
        self.port = port

    def create_connection(self):
        s = AdbSocket(self.host, self.port)
        s.connect()
        s.send("host:transport:{}".format(self.serialno))
        return s

    def shell(self, cmd):
        s = self.create_connection()
        s.send("shell:{}".format(cmd))
        result = s.read().decode('utf-8').strip()
        s.close()
        return result


device = AdbDevice("emulator-5554")

for index in range(0, 10):
    print(device.shell('getprop ro.build.version.release'))
