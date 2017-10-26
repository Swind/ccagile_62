import socket

# 連線
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 5037))

# 溝通
cmd = "host:devices"

## 建立指令並送出 - 使用 4 bytes 來表示後面的資料長度
b_cmd = cmd.encode('utf-8')
b_length = "{0:04X}".format(len(b_cmd)).encode('utf-8')

adb_cmd = b_length + b_cmd

print(adb_cmd)
s.send(adb_cmd)

## 取得 adb server 回應確認指令是否正確 - 正確的話會回傳 'OKAY'
result = s.recv(4).decode('utf-8')
print(result)

## 取得指令執行結果
length = int(s.recv(4).decode('utf-8'), 16)
result = s.recv(length)
print(result)
